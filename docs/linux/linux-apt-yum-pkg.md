---
layout: default
title: APT - Yum - PKG
parent: Linux
nav_order: 2
---

# {{page.title}}
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

### Apt

debian package managment. apt-get is dpkg top couch  

```sh
	apt update  # update the available package list.
	apt --only-upgrade install <pkg> # update a single pkg
	sudo apt search <pkg> 
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


### Yum

	$ yum install [package-name]
	$ yum remove [package-name]
	$ yum list available
	$ yum list installed
	$ yum list installed | grep nfs
