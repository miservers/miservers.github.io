---
layout: default
title: IBM Packaging Utility
parent: WebSphere
grand_parent: Middleware
nav_order: 3
---

### SetUp
----------------------------------------------------------------------------------
**IBM Package Utility** is a tool to copy packages(from ibm.com) into repositories for consumption by **Installation Manager**. It can also copy packages from ibm repositories to local disk so Installation Manager can install them using local disk, ftp, http access.

![alt](/docs/images/ibm-packaging-utility-2.png)

**Install: Gui mode**: donwload it and unzip it

	./install     // install it as root	
	./userinst    // as user
	./groupinst

**Install: Console mode**
~~~sh
./installc	-acceptLicense    //root install

./userinstc -acceptLicense
~~~

By default It will be installed in `/opt/IBM/PackagingUtility`

Screens:

![a](/docs/images/ibm-packaging-utility-main.png)
![b](/docs/images/ibm-packaging-utility-copy.png)

### IBM Repositories
- [Trial WAS Repositories](https://www.ibm.com/docs/en/was/9.0.5?topic=installation-online-product-repositories-websphere-application-server-offerings)

### Provisioning Staging Machine
For provisioning the Adminitrator Staging Machine: 
- install the Packaging Utility to create local **repositories** used to deploy the packages on target machines. 
- Use Http/Https: you should setup an http server. Example here by [nginx](/docs/middleware/nginx/#nginx-as-a-static-file-server)
- Optionaly you can use Network Share or FTP to access the repository instead of http

### Provisioning the Target Machine
First, install the Installation Manager on the target machine

Second, install the packages using the installation Manager. Different modes can be used: graphic, console, command, silent.
