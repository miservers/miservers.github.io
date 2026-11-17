---
layout: default
title: OpenSeaech
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

### Configuration des Snapshots sur OpenSearch 1.3

- Choisir un repository, Soit sur NFS,  S3(necessite un plugin), Ajouter dans `/etc/opensearch/opensearch.yml` :

  ```yaml
  path.repo: ["/mnt/snapshots"]
  ```

- Puis Redémarrer OpenSearch 

- Enregistrer le repository(une seule fois, depuis n'importe quel nœud):

  ```bash
  curl -X PUT "localhost:9200/_snapshot/mon_repo" \
    -H 'Content-Type: application/json' -d '{
    "type": "fs",
    "settings": {
      "location": "/mnt/snapshots",
      "compress": true
    }
  }'
  ```

- Créer un snapshot

  ```bash
  curl -X PUT "localhost:9200/_snapshot/mon_repo/snapshot_01?wait_for_completion=true"
  ```


- Lister et restaurer

  ```bash
  # Lister tous les snapshots
  curl -X GET "localhost:9200/_snapshot/mon_repo/_all"
  
  # Restaurer un snapshot
  curl -X POST "localhost:9200/_snapshot/mon_repo/snapshot_01/_restore"
  ```

---

- Automatiser avec cron (cron sur node-1 uniquement)

  ```bash
  crontab -e
  # Snapshot quotidien à 2h00
  0 2 * * * curl -X PUT "localhost:9200/_snapshot/mon_repo/snapshot_$(date +\%Y\%m\%d)?wait_for_completion=true"
  ```
  
- Vérifications utiles
  ```
  # Vérifier l'état du cluster (depuis n'importe quel nœud)
  curl -X GET "localhost:9200/_cluster/health?pretty"
  # Liste des nœuds
  curl -X GET "localhost:9200/_cat/nodes?v"
  
  # Nœud master élu
  curl -X GET "localhost:9200/_cat/master?v"
  
  # État des shards
  curl -X GET "localhost:9200/_cat/shards?v"
  ```

## Docs

- https://docs.opensearch.org/1.3/security/configuration/security-admin/
- Troobleshooting: https://docs.opensearch.org/latest/troubleshoot/security-admin/









