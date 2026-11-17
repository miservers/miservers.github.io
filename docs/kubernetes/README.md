

### SetUp kunectl on Termux
1. Install kubectl: `pkg install kubectl`

1. Copy `.kube/config` from controle-plane to local .kube/config
2. Edit it, delete CA and enable insecure
```
cluster:
    server: https://127.0.0.1:6443
    insecure-skip-tls-verify: true
```
3. create a ssh tunnel: `ssh -L 6443:127.0.0.1:6443 kmaster -f -N`



