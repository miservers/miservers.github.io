

### crictl

CLI de bas niveau pour interagir directement avec le container runtime
(containerd, CRI-O) sans passer par Kubernetes.
Utile quand l'API server est down et que `kubectl` ne répond plus.

#### Commandes essentielles

| Commande | Description |
|----------|-------------|
| `crictl ps -a` | Lister tous les conteneurs |
| `crictl ps -a \| grep kube \| grep -v pause` | Filtrer les composants kube |
| `crictl logs <ID>` | Logs d'un conteneur |
| `crictl pods` | Lister les pods (sandboxes) |
| `crictl images` | Lister les images |

### Configuration

```yaml
# /etc/crictl.yaml
runtime-endpoint: unix:///var/run/containerd/containerd.sock