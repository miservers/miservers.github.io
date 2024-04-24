---
layout: default
title: Templates
parent:  Ansible
grand_parent: DevOps
nav_order: 1.5
---

Template are proccessed by [Jinja2 template language](http://jinja.pocoo.org/docs/)

Example of template personalising tomcat http port:
- Define vars:
~~~yaml
vars:
    tomcat_http_port: 8180
    catalina_home: /opt/tomcat
~~~

- Copy server.xml into  templates/server.xml.j2 and edit it:
{% raw %}
  ~~~xml
  <Connector port="{{ tomcat_http_port }}" protocol="HTTP/1.1"
               connectionTimeout="20000"
  ~~~
{% endraw %}

- Create task
{% raw %}  
  ~~~yaml
  - name: Apply server.xml Template
       template:
         src: templates/server.xml.j2
         dest: "{{catalina_home}}/conf/server.xml"
  ~~~
{% endraw %}

- Apply the playbook
~~~sh
ansible-playbook -i ../prod-inventory playbook.yml
~~~
