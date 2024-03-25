---
layout: default
title: Jenkins
parent: DevOps
nav_order: 1
---

### Concepts
C**I/CD**: Continuous Integration/Delivery

**Pipeline**: 

**JenkinsFile**: 

### Architecture

![alt](/docs/images/jenkins-DevOps-tools.webp)

### Getting Started
**Start Jenkins**
~~~sh
systemctl start jenkins
~~~

### Pipeline
Example 
![alt](/docs/images/jenkins-pipeline-flow.png)

### Config Files
On Linux(Ubuntu 22.04):
- user: jenkins
- JENKINS_HOME=/var/lib/jenkins
- service script: /lib/systemd/system/jenkins.service


### Jenkins, Git and Maven Integration
Git and Maven must be installed on the machine.

**Integrate Maven into Jenkins**
1. Install Maven Plugin 
![alt](/docs/images/jenkins-maven-plugin.png)
2. Setup Maven Installation Home
![alt](/docs/images/jenkins-maven-tool.png)

### Change Maven Version Inside Pipeline
**Jenkinsfile**
~~~grouvy
pipeline {
    agent any
    tools {
      // maven installation declared in Jenkins "Global Tool Configuration"
      maven 'maven-3.8.7'
    }
    stages {
        stage('Build') { 
            steps {
                 sh 'mvn -B -DskipTests clean package'
            }
        }
    }
}
~~~ 

### Jenkins & Ansible
1. Install Ansible Plugin in Jenkins
2. Configure Ansible in Jenkins
![alt](/docs/images/jenkins-ansible-tools.png)