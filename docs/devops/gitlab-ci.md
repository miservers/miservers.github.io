---
layout: default
title: Gitlab
parent: DevOps
nav_order: 2.8
---


## Gitlab
---------------------------------
### Install on Redhat 8
~~~sh
sudo dnf install -y curl policycoreutils openssh-server perl
sudo systemctl enable sshd
sudo systemctl start sshd
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo systemctl reload firewalld
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.rpm.sh | sudo bash
sudo EXTERNAL_URL="https://gitlab.safarit.com" dnf install -y gitlab-ee
~~~


### Config

Edit `/etc/gitlab/gitlab.rb`: 
~~~
external_url 'http://gitlab.safarit.com'
~~~

Apply  config modif: 
~~~sh
sudo gitlab-ctl reconfigure
~~~

### Start/Stop
~~~sh
gitlab-ctl start|status
~~~

### Console 
Url : http://gitlab.safarit.com/

User : root

Password: In /etc/gitlab/initial_root_password

## Runners
-------------------------------
GitLab Runner is an application that works with GitLab CI/CD to run jobs in a pipeline.


### Install a Runner on RHEL 8
~~~sh
 curl -LJO "https://s3.dualstack.us-east-1.amazonaws.com/gitlab-runner-downloads/latest/rpm/gitlab-runner_amd64.rpm"
 dnf install git -y
 rpm -i gitlab-runner_amd64.rpm

 ~~~

### Register a Runner

1. Gitlab Console: `Your_Project> Settings > CI/CD > Runners > new project runner` 

2. Register the created runner
~~~sh
gitlab-runner register  --url http://gitlab.safarit.com  --token glrt-dxnxs_C_ocwff9zQYmSS
~~~

3. Runner config will be set in `/etc/gitlab-runner/config.toml` 

4. See Runners: `Your_Project › Settings  › CI/CD  › Runners`

![a](/docs/images/gitlab-runners.png)

## Pipelines
--------------------------
Pipelines are defined in `.gitlab-ci.yml` file at the root of the project.

a Pipeline are structred as stages(compile, test, deploy) and jobs within stages:
  - **Stages** run sequentially. 
  - **Jobs** within the same stage run concurrently.

Example:
~~~yaml
stages:          # List of stages for jobs, and their order of execution
  - build
  - test
  - deploy

include:
  - template: Security/Dependency-Scanning.gitlab-ci.yml

build-job:       # This job runs in the build stage, which runs first.
  stage: build
  script:
    - mvn package

unit-test-job:   
  stage: test    
  script:
    - echo "Running unit tests... This will take about 60 seconds."
    - sleep 60
    - echo "Code coverage is 90%"

deploy-job:     
  environment: production 
  stage: deploy  
  script:
    - echo "Deploying application..."
    - echo "Application successfully deployed."
~~~

![a](/docs/images/gitlab-pipeline.png)








