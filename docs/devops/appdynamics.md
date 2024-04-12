---
layout: default
title: AppDynamics
parent: DevOps
nav_order: 5
has_toc: true
---

### Installation
Install the Console:
~~~sh
./platform-setup-64bit-linux.sh
~~~

Config Min: 4 cpu, 2 RAM, 50 Go

### Requirement Limits
Edit platform-admin/archives/controller/24.2.1-10085/playbooks/controller-demo.groovy
~~~
controller_min_ram_in_mb = 3 * 1024
controller_min_cpus = 2
controller_data_min_disk_space_in_mb = 50 * 1024
remote_controller_min_ram_in_mb = 3 * 1024
remote_controller_min_cpus = 2
~~~

### Appdynamics Console
Start the Console
~~~sh
platform-admin/bin/platform-admin.sh start-platform-admin
~~~

Access the Console:  <a>https://localhost:9191</a>
  - login: admin

### Controller


