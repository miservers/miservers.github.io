### Wich process use Swap
~~~shell
$ find /proc -maxdepth 2 -path "/proc/[0-9]*/status" -readable -exec awk -v FS=":" '{process[$1]=$2;sub(/^[ \t]+/,"",process[$1]);} END {if(process["VmSwap"] && process["VmSwap"] != "0 kB") printf "%10s %-30s %20s\n",process["Pid"],process["Name"],process["VmSwap"]}' '{}' \; | awk '{print $(NF-1),$0}' | sort -h | cut -d " " -f2-
~~~


### Extend Swap
[Reference] 
   (https://www.linuxtechi.com/extend-swap-space-using-swap-file-in-linux/)

This worked fine on ubuntu 20.04

***Steps to extends swap***

**check the swap situation**  

    free -m
    swapon -s

**Create a new swap file**  

    sudo dd if=/dev/zero of=/swapfile2 bs=1G count=1
    sudo chmod 600 /swapfile2

**format the file with swap filesystem format**   

    sudo mkswap /swapfile2

**Add swap file to fstab**  

    sudo nano /etc/fstab

**Activate the new swap file**  

    sudo swapon /swapfile2

**To disable the swapfile**   

    swapoff /swapfile2

