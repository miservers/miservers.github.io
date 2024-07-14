---
layout: default
title: APT - Yum - PKG
parent: Linux
nav_order: 2
---


### Yum

```sh
$ yum install pkg-name
$ yum remove pkg-name
$  yum search pkg-name
$ yum list available
$ yum list installed
$ yum list installed | grep nfs

```

**Yum History**

```sh
# yum history
yum history

# View details of a transactionb 43
yum history info 42

# Undo/redo a specific transaction
yum history undo 42
yum history redo 43

# List packages changed in a specific transaction
yum history list 42

# Rollback to a specific transaction
yum history rollback 42

# Reinstall packages from a specific transaction
yum history reinstall 42

```



### Apt

debian package managment. apt-get is dpkg top couch  

```sh
	apt update  # update the available package list.
	apt --only-upgrade install <pkg> # update a single pkg
	apt list --installed             # list installed packages
	apt list --installed | grep pkg  # search installed package
	apt search <pkg> 
	apt-cache search pkg-name # search package to install
	apt install pkg
	apt remove package # remove pkg
	apt remove --purge package # remove pkg and its config files
	apt autoremove # Remove automatically all unused packages
	apt upgrade # upgrade the hole system
	apt upgrade-dist # linux distribution upgrade
```

**To disable downloading translations**

    echo 'Acquire::Languages "none";' >> /etc/apt/apt.conf.d/99translations

### Dpkg

dpkg: https://www.cyberciti.biz/howto/question/linux/dpkg-cheat-sheet.php  

```sh
	dpkg -l # list of installed packages.
    dpkg -l | grep gdb
	dpkg -i /root/bochs.81-1_i386.deb # install manually
	dpkg [--remove | --purge] bochs
	dpkg -L {package} : list	where files were installed
	dpkg -s {package} : output package status, if installed or not, vesrion, dependencies
```

**Install a special version of a pkg**

```sh
	apt-cache showpkg <package-name> # lists all available versions. 
	apt install <package-name>=<version-number>
```

**Misc commands**

    dpkg -l libgtk[0-9]* | grep ^i  ; search in installed



