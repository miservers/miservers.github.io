---
layout: default
title: OpenSearch
parent: Data Base
nav_order: 5
has_toc: true
---

# OpenSearch 1.3 — Exploitation

**Chemins :** `/etc/opensearch` (config) · `/var/lib/opensearch` (data) · `/var/log/opensearch` (logs) · `/usr/share/opensearch` (binaires).

**Notions :** *shard* = partition d'index ; *replica* = copie sur un autre data node ; *quorum* = majorité des nœuds éligibles au master.

## Cluster : 2 data + 1 témoin

| Nœud | Adresse | `node.roles` | NFS |
|:--|:--|:--|:--|
| os-node1 | 10.0.0.11 | `[master, data, ingest]` | Oui |
| os-node2 | 10.0.0.12 | `[master, data, ingest]` | Oui |
| os-witness | 10.0.0.13 | `[master]` | **Non** |

**Quorum : 2/3.** Le témoin est **master-éligible** (pas `voting_only`) : il peut devenir master. Pas de shards sur ce nœud.

Commun aux trois `/etc/opensearch/opensearch.yml` :

~~~yaml
cluster.name: opensearch-prod
discovery.seed_hosts: ["10.0.0.11:9300", "10.0.0.12:9300", "10.0.0.13:9300"]
# Premier démarrage UNIQUEMENT : retirer après formation du cluster
cluster.initial_master_nodes: [os-node1, os-node2, os-witness]
http.port: 9200
transport.port: 9300
path.repo: ["/mnt/opensearch-backup"]
~~~

Paramètres propres à chaque nœud :

~~~yaml
# os-node1
node.name: os-node1
node.roles: [master, data, ingest]
network.host: 10.0.0.11
~~~

~~~yaml
# os-node2
node.name: os-node2
node.roles: [master, data, ingest]
network.host: 10.0.0.12
~~~

~~~yaml
# os-witness
node.name: os-witness
node.roles: [master]
network.host: 10.0.0.13
~~~

**Prérequis :** TLS transport, TCP 9300, `number_of_replicas: 1`. Retirer `cluster.initial_master_nodes` après bootstrap.

### Diagnostic rapide (Dev Tools)

~~~http
GET /_cluster/health?pretty
GET /_cat/nodes?v
GET /_cat/master?v
GET /_cat/shards?v
GET /_cat/indices?v
GET /_cluster/allocation/explain
GET /_nodes/stats/jvm,fs,process
GET /_cat/thread_pool?v
~~~

**États :** `green` = OK ; `yellow` = réplique manquante ; `red` = primaire manquant. Quorum : 2/3.

## Snapshots sur NFS

**Contrainte actuelle :** seuls les deux data nodes voient le NFS ; le témoin ne le voit pas. Un repository `fs` exige un accès depuis les nœuds master-éligibles et data pour un fonctionnement fiable. Le test `verify=false` ci-dessous est **diagnostique**, pas une validation de production après bascule master.

### Repository

Sur les nœuds autorisés, monter `nfs-backup:/exports/opensearch` sur `/mnt/opensearch-backup` (montage persistant, droits utilisateur `opensearch`). `path.repo` doit être configuré sur les trois nœuds et OpenSearch redémarré.

Sur chaque data node :

~~~bash
findmnt /mnt/opensearch-backup
df -hT /mnt/opensearch-backup
sudo -u opensearch test -r /mnt/opensearch-backup
sudo -u opensearch test -w /mnt/opensearch-backup
# Contrôler également UID/GID et permissions côté serveur NFS
id opensearch
~~~

Ne pas modifier les fichiers du repository manuellement.

~~~http
PUT /_snapshot/backup_nfs?verify=false
{
  "type": "fs",
  "settings": {
    "location": "/mnt/opensearch-backup",
    "compress": true
  }
}

GET /_snapshot/backup_nfs
POST /_snapshot/backup_nfs/_verify
~~~

`verify=false` évite **seulement** le contrôle à la création. L'appel `_verify` peut échouer sur le témoin : **ne pas ignorer ce résultat**.

### Test complet : écriture → snapshot → restauration

~~~http
GET /_cat/master?v

PUT /test-snapshot
{
  "settings": {"number_of_shards": 1, "number_of_replicas": 1}
}

PUT /test-snapshot/_doc/1?refresh=true
{"message":"test backup","valeur":123}

GET /test-snapshot/_count

PUT /_snapshot/backup_nfs/test-snapshot-001?wait_for_completion=true
{
  "indices": "test-snapshot",
  "include_global_state": false,
  "partial": false
}

GET /_snapshot/backup_nfs/test-snapshot-001
GET /_snapshot/backup_nfs/test-snapshot-001/_status
GET /_cat/snapshots/backup_nfs?v
~~~

**Attendu :** `state: SUCCESS`, aucun shard en échec.

**Restaurer sans écraser l'index source :**

~~~http
POST /_snapshot/backup_nfs/test-snapshot-001/_restore?wait_for_completion=true
{
  "indices": "test-snapshot",
  "include_global_state": false,
  "rename_pattern": "test-snapshot",
  "rename_replacement": "test-snapshot-restore"
}

GET /test-snapshot-restore/_count
GET /test-snapshot-restore/_doc/1
GET /_cat/recovery?v
~~~

**Attendu :** 1 document, `valeur: 123`. Adapter les noms si nécessaire.

**Diagnostics en cas d'échec :**

| Symptomatique | Vérifier |
|:--|:--|
| `repository_verification_exception` | NFS / permissions sur les nœuds master + data |
| `repository_missing_exception` | Repository non enregistré / mauvais nom |
| `snapshot_missing_exception` | Snapshot absent ou autre repository |
| `PARTIAL` ou `FAILED` | `failures`, état des shards, logs du master |
| `yellow` après restauration | Nombre de replicas et allocation sur les deux data nodes |

~~~bash
journalctl -u opensearch --since "30 minutes ago" --no-pager
grep -Ei 'snapshot|repository|exception' /var/log/opensearch/opensearch.log | tail -40
~~~


**Limite :** réussite avec un data node élu master ≠ garantie quand le témoin devient master. Ne pas automatiser en production sans accès NFS correct sur le témoin.

## Sauvegarde quotidienne : Bash + cron

`/usr/local/sbin/opensearch-snapshot.sh` — exécuter **sur un seul serveur**. Prérequis : `curl`, `jq`, `flock`, GNU `date`.

~~~bash
#!/usr/bin/env bash
set -Eeuo pipefail
API="https://os-node1.example.local:9200"
REPO="backup_nfs"
CA="/etc/opensearch/certs/root-ca.pem"
NETRC="/etc/opensearch/snapshot.netrc"
SNAP="auto-$(date -u +%Y%m%dT%H%M%SZ)"

api() {
  curl -fsS --connect-timeout 10 --max-time 21600 \
    --cacert "$CA" --netrc-file "$NETRC" "$@"
}
trap 'echo "ERREUR snapshot $(date -Is)" >&2' ERR

r=$(api -X PUT -H 'Content-Type: application/json' \
  -d '{"indices":"*","include_global_state":false,"partial":false}' \
  "$API/_snapshot/$REPO/$SNAP?wait_for_completion=true")

[[ $(jq -r '.snapshot.state // "UNKNOWN"' <<<"$r") == SUCCESS ]] || {
  echo "Snapshot échoué : $SNAP" >&2; exit 1;
}
echo "SUCCESS $SNAP"

# Purge : uniquement après succès ; uniquement les auto- SUCCESS > 30 j
cutoff=$(( $(date -u -d '30 days ago' +%s) * 1000 ))
api "$API/_snapshot/$REPO/_all" |
  jq -r --argjson c "$cutoff" '
    .snapshots[]
    | select(.snapshot | startswith("auto-"))
    | select(.state == "SUCCESS" and .start_time_in_millis < $c)
    | .snapshot' |
  while IFS= read -r old; do
    echo "DELETE $old"
    api -X DELETE "$API/_snapshot/$REPO/$old" >/dev/null
  done
~~~

Authentification `/etc/opensearch/snapshot.netrc` : `machine os-node1.example.local`, `login snapshot_service`, `password ...`. **Permissions 600**, compte dédié, TLS vérifié. Ne pas stocker de secret dans Git.

~~~text
machine os-node1.example.local
login snapshot_service
password MOT_DE_PASSE_A_REMPLACER
~~~

`401/403` : vérifier les droits du compte Snapshot.

~~~bash
sudo chmod 600 /etc/opensearch/snapshot.netrc
sudo chmod 750 /usr/local/sbin/opensearch-snapshot.sh
sudo crontab -e
~~~

~~~cron
# 02h00 chaque jour (heure du serveur), exécution unique sur ce serveur
0 2 * * * /usr/bin/flock -n /run/lock/opensearch-snapshot.lock /usr/local/sbin/opensearch-snapshot.sh >> /var/log/opensearch-snapshot.log 2>&1
~~~

~~~bash
sudo /usr/local/sbin/opensearch-snapshot.sh
tail -50 /var/log/opensearch-snapshot.log
~~~

Ne jamais supprimer les fichiers du repository directement sur le NFS : utiliser l'API `DELETE /_snapshot/backup_nfs/NOM`.

## Supervision : scripts / AppDynamics

Interroger les API toutes les 1–5 min depuis un **Machine Agent**, puis publier des *Custom Metrics* et créer des *Health Rules* :

| Métrique | Alerte |
|:--|:--|
| `cluster.status` | `red` 2 min ; `yellow` 5 min |
| `number_of_nodes` | < 3 |
| `number_of_data_nodes` | < 2 |
| `snapshot.last_success_age_minutes` | > 1560 (26 h) |
| `snapshot.last_state` | `FAILED` / `PARTIAL` |
| `api.available` | 0 |
| `backup_nfs.free_percent` | < 15 % |

~~~http
GET /_cluster/health
GET /_snapshot/backup_nfs/_all
~~~

**Exemple de métriques Bash** (à transmettre au Machine Agent) :

~~~bash
# "$health" est le JSON de GET /_cluster/health
nodes=$(jq -r '.number_of_nodes' <<<"$health")
data=$(jq -r '.number_of_data_nodes' <<<"$health")
status=$(jq -r '.status' <<<"$health")
case "$status" in green) level=2;; yellow) level=1;; *) level=0;; esac

echo "name=Custom Metrics|OpenSearch|Nodes,value=$nodes,aggregator=OBSERVATION,time-rollup=CURRENT,cluster-rollup=INDIVIDUAL"
echo "name=Custom Metrics|OpenSearch|Data Nodes,value=$data,aggregator=OBSERVATION,time-rollup=CURRENT,cluster-rollup=INDIVIDUAL"
echo "name=Custom Metrics|OpenSearch|Cluster Status,value=$level,aggregator=OBSERVATION,time-rollup=CURRENT,cluster-rollup=INDIVIDUAL"
~~~

Snapshot : calculer `age_min=(now-end_time_in_millis/1000)/60` sur le dernier `auto-*` `SUCCESS`. Alerter aussi sur l'absence de métriques du Machine Agent.

**Ne pas superviser uniquement le cron :** contrôler le dernier snapshot `SUCCESS`, l'échec de la collecte et l'âge de la dernière sauvegarde. Faire un test de restauration périodique.

## Administration

~~~bash
/usr/share/opensearch/bin/opensearch-plugin list
# Security Admin : applique les fichiers YAML dans l'index de sécurité,
# peut écraser les modifications réalisées par API/UI.
# Exiger un certificat ADMIN dédié (différent du certificat node).
~~~

~~~bash
./securityadmin.sh -cd /chemin/securityconfig \
  -cacert /chemin/root-ca.pem -cert /chemin/admin.pem \
  -key /chemin/admin.key -icl -nhnv
~~~

Users/roles applicatifs : préférer l'API Security / Dashboards. Conserver les comptes de service nécessaires ; désactiver les identifiants par défaut inutilisés.

## Références

- [OpenSearch 1.3 — cluster](https://eliatra.com/docs/1.3/tuning-your-cluster/)
- [OpenSearch 1.3 — snapshots](https://eliatra.com/docs/1.3/api-reference/snapshots/create-snapshot/)
- [Vérification du repository](https://eliatra.com/docs/1.3/api-reference/snapshots/verify-snapshot-repository/)
- [Suppression d'un snapshot](https://eliatra.com/docs/1.3/api-reference/snapshots/delete-snapshot/)
- [OpenSearch — stockage partagé NFS](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [AppDynamics — Custom Metrics](https://docs.appdynamics.com/display/ONPREM/Extensions+and+Custom+Metrics)
- [OpenSearch 1.3 — Security Admin](https://docs.opensearch.org/1.3/security/configuration/security-admin/)
