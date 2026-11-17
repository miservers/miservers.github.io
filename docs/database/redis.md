---
layout: default
title: Redis Cache
parent: Data Base
nav_order: 6
---

### Config
/etc/redis.conf

Sur Le master
~~~
bind 10.0.0.1
protected-mode yes
replicaof 10.0.0.1 6379
requirepass redispassword
# pour se connecter au master, quand ce master devient slave
masterauth redispassword
~~~

Sur les replicas
~~~
bind 10.0.0.x
protected-mode yes

replicaof 10.0.0.1 6379
requirepass redispassword
# pour se connecter au master
masterauth redispassword
~~~

/etc/redis-sentinel.conf: sur les 3 vm
~~~
port 26379
bind 0.0.0.0
protected-mode no

### qorum de 2: exige deux sentinel pour dire madter down
sentinel monitor mymaster 10.0.0.1 6379 2
sentinel auth-pass mymaster redispassword
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 10000
sentinel parallel-syncs mymaster 1
~~~

### Redis Server
~~~
redis-cli -h localhost -p 6379

# PING : test de connectivité
127.0.0.1:6379> PING
PONG

# SET/GET : écrire et lire une clé
127.0.0.1:6379> SET ma_cle "valeur"
127.0.0.1:6379> GET ma_cle

# KEYS : lister les clés (à éviter en production si beaucoup de données)
127.0.0.1:6379> KEYS *

# DEL : supprimer une clé
127.0.0.1:6379> DEL ma_cle

# INFO : voir l’état du serveur
127.0.0.1:6379> INFO

# MONITOR : voir toutes les commandes en temps réel
127.0.0.1:6379> MONITOR
~~~

### Sentinel
Joue le role d'un loadbalancer pour le cluster Redis

~~~
redis-cli -h localhost -p 26379

# Voir les masters suivis par Sentinel
127.0.0.1:26379> SENTINEL masters

# Voir les slaves d’un master
127.0.0.1:26379> SENTINEL slaves mymaster
~~~

**Forcer un failover** pour elire un autre master
~~~
127.0.0.1:26379> SENTINEL failover mymaster
~~~

### Notes
- Avec TLS: ``redis-cli -h hostname -p 6379 --tls``
- Les masters: ``redis-cli -p 26379 sentinel masters``

### Les logs

- **Redis logs** : */var/log/redis/redis-server.log*
- **Sentinel logs** : */var/log/redis/sentinel.log* 


### Connexion via Sentinel

Tu ne peux pas te connecter directement à Sentinel avec redis-cli comme à Redis. Tu dois :

utiliser Sentinel pour découvrir le master :

~~~
redis-cli -p 26379 sentinel get-master-addr-by-name <nom_du_master>
~~~

Ensuite 
~~~
redis-cli -h <ip_master> -p <port>
~~~

