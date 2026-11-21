---
layout: default
title: OpenSearch
parent: Data Base
nav_order: 5
---

### Chemins standards:
- Bin : /usr/share/opensearch
- Config : /etc/opensearch
- Data : /var/lib/opensearch
- Logs : /var/log/opensearch

### Concepts
### Shards
Opensearch divise données en unités plus petites nommées **shards**. Ainsi un index est decoupé en plusieurs **shards**. Une shard un index autonome. les shards sont distribuées à travers le cluster, ce qui permet la scalabilité horizontale. En générale la taille d'une shard est de 10-50Go. 

### Replicas
Le replicas consiste a repliquer un shard dit primaire sur un autre noeud du cluster. Ce qui permet à un index d'être completement operationnel meme si un neud du cluster est HS. un replicas de 1 permet de repliquer chaque shard sur un autre noeud du cluster.


### Quorum
Le maitre est choisi par quorum: par exemple si on 3 noeuds et quorum de 2, il faut que au moins deux noeud soient up pour que le cluster soit fonctionnel. En general le quorum=(nb of nodes)/2 + 1

### Users
Les utilisateurs OpenSearch créés via Dashboards ou l’API Security sont stockés dans l’index **.opensearch-security**, répliqué sur tous les nœuds.

### Les backend users/roles
Les backends users/roles sont ceux definés dans les yaml en dur(**internal_users.yml, roles.yml, roles_mapping.yml**).

Il est recommandé de ne pas les utiliser pour vos applications, il faut utiliser l'ACL pour en créer. Et surtout ne pas modifier les mots de passe definis par defaut dans *internal_users.yml* et supprimer les comptes par defaut non utiliser. mais il faut garder les comptes **admin** et **kibanaserver**


### Plugins
Les plugins les plus utilisés: Security (authentification/permissions), Dashboards (visualisation), Alerting (notifications), ISM (gestion cycle de vie), Reporting (rapports), Notebooks (analyses documentées), SQL/PPL (requêtes) et Performance Analyzer (monitoring).


**Afficher les plugins installés/activés**
~~~
./bin/opensearch-plugin list
~~~
ou
~~~
GET _cat/plugins?v
~~~

**Installer un plugin**
~~~
sudo ./bin/opensearch-plugin install <plugin_name>
~~~
puis relancer opensearch

### Securityadmin.sh
il applique les modif dansles fichiers de config dans plugins/opensearch-security/securityconfig.

Initialise l'index **.opendistro_security**. Il faut l'utiliser par precaution, car ecrase les modif apporté à l'index via le REST API.

Il necessite certificat **admin** qui doit être different des certificats utilisés par les noeuds.


**Configure the admin certificate**:You can’t use node certificates as admin certificates. The two must be separate.

creer le certificat
~~~
./opensearch-certutil admin
~~~

Enregistrer le certificat
~~~
plugins.security.authcz.admin_dn:
  - "CN=admin,OU=SSL,O=MyCompany,L=City,C=US"
 ~~~ 

~~~sh
./securityadmin.sh \
  -cd /path/to/securityconfig/ \
  -cacert /path/to/root-ca.pem \
  -cert /path/to/admin.pem \
  -key /path/to/admin.key \
  -icl \
  -nhnv
~~~

icl : ignore cluster name verif
  
nhnv: no hostname verif

## Cluster OpenSearch 1.3 : 2 data + 1 témoin

**Topologie :** os-node1 (10.0.0.11) et os-node2 (10.0.0.12) hébergent les données. os-witness (10.0.0.13) est dédié au rôle master. Les 3 participent aux élections : **quorum 2/3**. Ce n'est pas un témoin passif : il peut devenir le master élu.

| Nœud | Rôles | Stockage de shards |
|:--|:--|:--|
| os-node1 | master, data, ingest | Oui |
| os-node2 | master, data, ingest | Oui |
| os-witness | master | Non |

**Commun aux trois nœuds** — /etc/opensearch/opensearch.yml :

~~~yaml
cluster.name: opensearch-prod
discovery.seed_hosts:
  - 10.0.0.11:9300
  - 10.0.0.12:9300
  - 10.0.0.13:9300

# Seulement pour le tout premier bootstrap du cluster
cluster.initial_master_nodes: [os-node1, os-node2, os-witness]

http.port: 9200
transport.port: 9300
path.repo: ["/mnt/opensearch-backup"]
~~~

**Paramètres propres à chaque nœud** (à ajouter aux paramètres communs) :

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

Configurer aussi le **TLS transport** et les certificats de nœuds (Security Plugin). Autoriser TCP/9300 entre les nœuds. Le témoin conserve l'état du cluster dans son répertoire data, mais aucun shard.

**Après formation initiale du cluster, retirer cluster.initial_master_nodes** des configurations : ne jamais re-bootstrapper un cluster existant. Pour supporter la panne d'un data node, les index doivent avoir un primaire et au moins un réplica correctement alloué ; avec deux data nodes, vérifier que la réplication tient dans les ressources disponibles.

Contrôles via Dev Tools (ou requêtes HTTP authentifiées) :

~~~http
GET /_cat/nodes?v
GET /_cat/master?v
GET /_cluster/health?pretty
GET /_cat/shards?v
~~~

## Snapshots NFS : dépôt, sauvegarde, restauration

### 1. Préparer et déclarer le repository

Pour un repository `fs` fiable, monter **le même partage NFS au même chemin sur les 3 nœuds**, y compris os-witness : le master élu doit pouvoir accéder au dépôt. Les permissions doivent permettre à l'utilisateur OpenSearch de lire et écrire. Prévoir un montage persistant et un stockage de sauvegarde distinct du stockage des données. **Cas actuel : le témoin n'a pas accès au NFS ; voir le test ci-dessous, uniquement pour diagnostiquer, pas pour valider une configuration HA de production.**

Exemple de montage Linux (adapter l'export et /etc/fstab) :

~~~bash
sudo mkdir -p /mnt/opensearch-backup
sudo mount -t nfs4 nfs-backup:/exports/opensearch /mnt/opensearch-backup
~~~

Après configuration de path.repo et redémarrage OpenSearch sur chaque nœud, déclarer une seule fois le repository :

~~~http
PUT /_snapshot/backup_nfs
{
  "type": "fs",
  "settings": {
    "location": "/mnt/opensearch-backup",
    "compress": true
  }
}

POST /_snapshot/backup_nfs/_verify
GET /_cat/repositories?v
~~~

La vérification doit retourner les nœuds participants ; sinon, contrôler montage, droits et connectivité.

### 2. Snapshot manuel

~~~http
PUT /_snapshot/backup_nfs/manual-001?wait_for_completion=true
{
  "indices": "*",
  "ignore_unavailable": false,
  "include_global_state": false,
  "partial": false
}

GET /_cat/snapshots/backup_nfs?v
GET /_snapshot/backup_nfs/manual-001
~~~

Vérifier l'état **SUCCESS**. Les snapshots sont incrémentaux. L'exemple exclut l'état global ; prévoir séparément l'export des configurations et certificats nécessaires à une restauration complète.

### 3. Tester une restauration sans écraser la source

~~~http
POST /_snapshot/backup_nfs/manual-001/_restore
{
  "indices": "logs-*",
  "include_global_state": false,
  "rename_pattern": "(.+)",
  "rename_replacement": "restore-test-$1"
}

GET /_cat/indices/restore-test-*?v
GET /_cat/recovery?v
~~~

Le snapshot doit contenir les index demandés. En recette, comparer aussi le nombre de documents et la santé des shards. Ne pas restaurer les index système en aveugle.

## Test de fonctionnement : témoin sans accès NFS

**Contexte :** os-node1 et os-node2 accèdent au NFS, mais **os-witness (master-éligible) n'y accède pas**. Les commandes suivantes s'exécutent dans OpenSearch Dashboards / Dev Tools. Tester sur un **index dédié**, sans toucher aux données applicatives. `verify=false` **ignore la vérification à l'enregistrement**, mais ne rend pas le dépôt utilisable par le témoin.

### 1. Identifier le master et contrôler le repository

~~~http
GET /_cat/master?v
GET /_cat/nodes?v
GET /_snapshot/backup_nfs
POST /_snapshot/backup_nfs/_verify
~~~

**Résultat attendu avec le témoin non monté :** `_verify` peut échouer (repository non accessible sur tous les nœuds requis). Ne pas considérer `_verify` en échec comme un test réussi.

Si le repository n'est **pas encore enregistré** et qu'on souhaite tester son enregistrement en contournant uniquement la vérification initiale :

~~~http
PUT /_snapshot/backup_nfs?verify=false
{
  "type": "fs",
  "settings": {
    "location": "/mnt/opensearch-backup",
    "compress": true
  }
}
~~~

`path.repo: ["/mnt/opensearch-backup"]` doit être déclaré sur tous les nœuds master/data, y compris le témoin (redémarrage nécessaire). Le montage NFS, lui, reste absent sur le témoin dans **ce test de diagnostic**. Cela ne garantit pas la prise de snapshot.

### 2. Index de test et contrôle des données

~~~http
PUT /test-snapshot
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}

PUT /test-snapshot/_doc/1?refresh=true
{
  "message": "Test snapshot OpenSearch 1.3",
  "valeur": 123
}

GET /test-snapshot/_count
GET /_cat/shards/test-snapshot?v
~~~

Attendu : `count: 1` et primaire + réplica alloués aux deux nœuds data. Utiliser un autre suffixe si ces noms existent déjà.

### 3. Snapshot et vérification du résultat

~~~http
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

Attendu en cas de réussite : `state: SUCCESS` et **0 shard en échec**. En cas d'erreur, lire `failures`, le statut du master et les logs OpenSearch. Un master élu sans accès NFS peut empêcher l'opération.

### 4. Restaurer dans un autre index (sans écraser l'original)

**Seulement si le snapshot est SUCCESS :**

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
GET /_cat/shards/test-snapshot-restore?v
~~~

Attendu : `count: 1`, document ID `1`, `valeur: 123`. Si la restauration est répétée, choisir un **nouveau nom de destination** pour éviter un conflit avec un index existant.

**Interprétation :** une sauvegarde + restauration `SUCCESS` valide **ce test ponctuel** ; cela **ne valide pas** le fonctionnement après une élection du témoin comme master. **Pour des sauvegardes de production fiables, rendre le repository accessible à tous les nœuds master-éligibles et data.**

## Automatiser avec cron (OpenSearch 1.3)

**Politique de départ :** un snapshot chaque jour à 02h00, rétention 30 jours, nettoyage uniquement après un snapshot réussi, et un seul ordonnanceur actif. La fonctionnalité native Snapshot Management a été introduite en OpenSearch 2.1 : en 1.3, utiliser un cron externe.

### Script complet

Installer curl, jq, flock et l'outil GNU date. Placer le script dans **/usr/local/sbin/opensearch-snapshot.sh** sur un **seul** serveur d'administration capable d'accéder à l'API HTTPS (et non sur les trois nœuds).

~~~bash
#!/usr/bin/env bash
set -Eeuo pipefail

API="https://os-node1.example.local:9200"
REPO="backup_nfs"
PREFIX="auto-"
RETENTION_DAYS=30
CA="/etc/opensearch/certs/root-ca.pem"
NETRC="/etc/opensearch/snapshot.netrc"

SNAPSHOT="$(date -u +auto-%Y%m%dT%H%M%SZ)"

api() {
  curl -fsS --connect-timeout 10 --max-time 21600 \
    --cacert "$CA" --netrc-file "$NETRC" "$@"
}
trap 'echo "$(date -Is) ERREUR ligne $LINENO" >&2' ERR

echo "$(date -Is) Création du snapshot : $SNAPSHOT"

response=$(api -X PUT -H 'Content-Type: application/json' \
  -d '{"indices":"*","include_global_state":false,"partial":false}' \
  "$API/_snapshot/$REPO/$SNAPSHOT?wait_for_completion=true")

state=$(jq -r '.snapshot.state // "UNKNOWN"' <<<"$response")
if [[ "$state" != "SUCCESS" ]]; then
  echo "$(date -Is) ÉCHEC snapshot : $state" >&2
  exit 1
fi
echo "$(date -Is) Snapshot SUCCESS : $SNAPSHOT"

# Inventaire seulement après une sauvegarde réussie
inventory=$(api "$API/_snapshot/$REPO/_all")
cutoff=$(( $(date -u -d "$RETENTION_DAYS days ago" +%s) * 1000 ))

# Ne supprimer que NOS snapshots, âgés de plus de N jours
expired=$(jq -r --arg prefix "$PREFIX" --argjson cutoff "$cutoff" '
  .snapshots[]
  | select(.snapshot | startswith($prefix))
  | select(.state == "SUCCESS")
  | select(.start_time_in_millis < $cutoff)
  | .snapshot
' <<<"$inventory")

while IFS= read -r old; do
  [[ -n "$old" ]] || continue
  echo "$(date -Is) Suppression de $old"
  api -X DELETE "$API/_snapshot/$REPO/$old" >/dev/null
done <<<"$expired"

echo "$(date -Is) Sauvegarde terminée"
~~~

**Authentification :** créer /etc/opensearch/snapshot.netrc, uniquement lisible par le compte qui lance le cron :

~~~text
machine os-node1.example.local
login snapshot_service
password MOT_DE_PASSE_A_REMPLACER
~~~

~~~bash
sudo chmod 600 /etc/opensearch/snapshot.netrc
sudo chmod 750 /usr/local/sbin/opensearch-snapshot.sh
~~~

Le compte de service doit avoir les droits sur les API Snapshot ; adapter le certificat CA et le nom d'hôte à l'environnement réel. Ne jamais committer les vrais identifiants.

### Crontab et contrôle

Éditer la crontab **root sur un seul serveur** :

~~~bash
sudo crontab -e
~~~

~~~cron
# Tous les jours à 02h00 (fuseau horaire du serveur)
0 2 * * * /usr/bin/flock -n /run/lock/opensearch-snapshot.lock /usr/local/sbin/opensearch-snapshot.sh >> /var/log/opensearch-snapshot.log 2>&1
~~~

Le verrou flock empêche deux exécutions concurrentes **sur ce serveur**, mais pas sur plusieurs machines. Les caractères % restent dans le script (pas dans la ligne cron), et les noms de snapshots sont horodatés en UTC.

~~~bash
# Test manuel
sudo /usr/local/sbin/opensearch-snapshot.sh

# Vérifier le cron et les erreurs
sudo tail -50 /var/log/opensearch-snapshot.log
~~~

~~~http
GET /_cat/snapshots/backup_nfs?v
GET /_snapshot/backup_nfs/_all
GET /_cluster/health?pretty
~~~

**Exploitation :** alerter en cas de snapshot non SUCCESS ou d'absence de snapshot récent (ex. > 26 h), surveiller l'espace NFS, appliquer logrotate au log local et tester une restauration en recette régulièrement. La rétention s'applique uniquement aux snapshots auto- terminés en SUCCESS. Supprimer les snapshots avec l'API DELETE, jamais directement dans le NFS. Un cron local n'est pas hautement disponible : superviser aussi le serveur ordonnanceur.

## Références

- [OpenSearch 1.3 — création d'un cluster](https://eliatra.com/docs/1.3/tuning-your-cluster/)
- [OpenSearch 1.3 — création de snapshot](https://eliatra.com/docs/1.3/api-reference/snapshots/create-snapshot/)
- [OpenSearch 1.3 — suppression de snapshot](https://eliatra.com/docs/1.3/api-reference/snapshots/delete-snapshot/)
- [OpenSearch — vérifier un repository](https://docs.opensearch.org/latest/api-reference/snapshots/verify-snapshot-repository/)
- [OpenSearch — Snapshot Management disponible à partir de 2.1](https://opensearch.org/blog/snapshot-management/)
- [OpenSearch 1.3 — outil Security Admin](https://docs.opensearch.org/1.3/security/configuration/security-admin/)
