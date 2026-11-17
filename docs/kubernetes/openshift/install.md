

### Installation SNO sur KVMs manuellement
*SNO*: Single Node Openshift

- [Install Manuelle de SNO](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/installing_on_a_single_node/install-sno-installing-sno)
- https://community.ibm.com/community/user/blogs/tamil-selvam-r/2025/05/29/kvm-based-single-node-openshift-sno-cluster-with-g


**Sur la machine Hote**
  - Ajouter les entrées DNS suivantes dans `/etc/hosts` vers l'ip de la vm : 
    - api.cluster-name.example.local
    - console-openshift.apps.cluster-name.example.local 
    - oauth-openshift.apps.cluster-name.example.local
  - Le DNS est tres important, le mieux c'est d'utiliser un serveur DNS, ex dnsmasq pour la resolution wildcard.

**Config DHCP du reseau KVM**
```
sudo virsh net-edit default

<network>
  <name>default</name>
  <uuid>311411fa-0b2f-4f45-aba4-c3c8a3c78aa5</uuid>
  <forward mode='nat'/>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='52:54:00:6a:e5:7f'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.122.2' end='192.168.122.254'/>
    </dhcp>
  </ip>
</network>
```

**install-config.yaml**
  - Base domain ne doit pas être resolu sur le net : `baseDomain: example.local`
  - machineNetwork avec meme cidr que le dhcp de KVM:
      `cidr: 192.168.22.0/24`
  - `installationDisk: /dev/sda` 


Une fois que tout est pret, tu peux creer ta VM qui va demarrer sur l'image rhcos.

**VM Kvm**

```
# Installation
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients virtinst bridge-utils podman  virt-manager
sudo systemctl enable --now libvirtd
sudo usermod -aG libvirt,kvm $USER
```

```
sudo cp rhcos-live-fresh.iso /VMs/rhcos-live.iso

sudo chown anass: /VMs/rhcos-live.iso

cp install-config.yaml ocp/

./openshift-install --dir=ocp create single-node-ignition-config
alias coreos-installer='podman run --privileged --pull always --rm -v /dev:/dev -v /run/udev:/run/udev -v $PWD:/data -w /data quay.io/coreos/coreos-installer:release'

coreos-installer iso ignition embed -fi ocp/bootstrap-in-place-for-live-iso.ign rhcos-live.iso

mv rhcos-live.iso /VMs/rhcos-live.iso

# Demarrer la VM
sudo virt-install   --name sno   --ram 24000   --vcpus 8           --disk path=/VMs/sno.qcow2,bus=sata,size=100  --cdrom /VMs/rhcos-live.iso   --network network=default     --graphics vnc   --noautoconsole   --boot cdrom,hd --cpu host-passthrough --console pty,target_type=serial --noautoconsole --osinfo detect=on,name=linux2024
```
Si probleme de droits sur les repetoire il faut les accorder : `sudo chmod o+x ~/VMs`

Console KVM : `virt-manager`

Update ton Hosts, si tu veux pas utiliser dnsmasq. RECUPERE L'IP, et MEt A JOUR RAPIDEMENT LE HOSTS
```
192.168.122.45  sno
192.168.122.45  api.sno.safarit.local
192.168.122.45  api-int.sno.safarit.local
192.168.122.45  console-openshift-console.apps.sno.safarit.local
192.168.122.45  oauth-openshift.apps.sno.safarit.local
```

Suivre l'activité/telechargement avec `nload`

### Suivre l'installation
- Pour se connecter sur la vm: `ssh core@sno`
- Podman : `podman ps -a`
- `sudo podman logs -f jolly_mclean`
- `crictl images | ps`
- `systemctl status kubelet`

**Depuis le host control**:
```
export KUBECONFIG=~/install-ocp/ocp/auth/kubeconfig

oc get nodes
```
  
**Rebaser vers l'image OCP** : a faire quand kubelet n'a pas été correctement installé
- Sur le nœud SNO :
```
# avant de rebaser voir ce qui se passe
sudo podman logs -f jolly_mclean

sudo systemctl restart rpm-ostreed
sudo rpm-ostree status  -> note le sha-id

sudo rpm-ostree rebase --experimental \
  ostree-unverified-registry:quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:<sha-id>

# Apres reboot, suit l'avancement
sudo podman ps -a
sudo podman logs -f jolly_mclean

systemctl start kubelet


```

**Console**: 
- https://console-openshift-console.apps.sno.safarit.local
- User : kubeadmin
- Password : CHANGE_ME ~/install-ocp/auth/kubeadmin-password

### KVM
- Console de KVM pour gerer tes VMs : `sudo virt-manager`


### Probèmes
- **La vm sno n'arrive pas à se connecter sur le net** : faire `curl https://www.google.fr` depuis la vm peut relancer la connection!!!

