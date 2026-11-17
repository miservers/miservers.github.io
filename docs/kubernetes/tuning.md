
~~~
# Rediriger le port 80 reçu sur l’IP publique 1.2.3.4 vers 192.168.1.100:8080
iptables -t nat -A PREROUTING -d 1.2.3.4 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.100:8080

# Autoriser le forwarding vers le serveur interne
iptables -A FORWARD -d 192.168.1.100 -p tcp --dport 8080 -j ACCEPT
~~~



### CPU Resource
Cpu resource specifie la puissance  CPU par second alloué à un Pod ou conteneur. 1000m est equivalent à une puissance d'un vCPU.  Mais cela ne va dire que le noyau alloue une seule cpu, le nombre de cpu n'est pas limité.

Si ton app lance 5 threads, et que chacun utilise la cpu avec intensité, et que tu a défini la limite de cpu à 1000m, alors ton app utilisera 5 cpu, chaque thread va tourner  200ms puis attendre 800ms.

### Resource Resuests/Limits
- `CPU/Memory Resuests`: on peux les depasser

- `CPU Limits`: si l'utilisation de la cpu s'approche de cette limite,  le **noyau** linux va restreindre/freiner le conteneur sur son urilisation de cpu. on parle de **throtteling**.

- `Memory Limits`: le comportement est diffrent de cpu limit. si le conteneur depasse la limite fixée, le **noyau** le tue. on parle de **OOM kill**(Out Of Memory Kill).



### Favoris
- [Blog de Pretius](https://pretius.com/blog/jvm-kubernetes/)

- [Doc officielle](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#how-pods-with-resource-limits-are-run)

