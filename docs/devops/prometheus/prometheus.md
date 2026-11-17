
### Alertes
**CPU throttling**: Étouffement CPU. C’est le bridage volontaire du CPU par le système quand un conteneur dépasse ses limites CPU définies.

### TroubleShooting
**Grafana not READY**
  => Augmente les resources du conteneur: CPU et Memory Limits( à 500 mCPU et 400Mi)

**Grafana Health**
~~~
curl http://grafana.monitoring.svc.cluster.local:3000/api/health
~~~

### Favoris
- [Prometheus/Grafana Stack on Docker] (https://github.com/vegasbrianc/prometheus)