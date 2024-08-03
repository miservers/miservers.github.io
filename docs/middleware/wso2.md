---
layout: default
title: WSO2
parent: Middleware
nav_order: 8
---

**Version 4.3.0**

## WSO2 Api Manager
 - WSO2 API Manager is used for securing, and exposing an enterprise's digital services as managed APIs 
 ![a](/docs/images/wso2apim-diagram.png)

1. Creating and publishing an API via the Publisher Portal of WSO2 API-M.
2. Deploy the API in a Gateway environment.
3. Publish the API in the Developer Portal. 
4. Subscribing to the API via the Developer Portal of WSO2 API-M and generating keys. <a>https://localhost:9443/devportal
5. Invoking the API with the generated keys.

### Install
Download from link above, setup JAVA_HOME, unzip the archive. Be carefull about the Java version. That's all!

- https://wso2.com/api-manager/
- Free : https://github.com/wso2/product-apim/releases/tag/v4.3.0

 

### Start/Stop
~~~bash
/opt/wso2am-4.3.0/bin$ sh api-manager.sh start
~~~

### Urls
- Mgt Console URL  : <a>https://localhost:9443/carbon/
- API Developer Portal : <a>https://localhost:9443/devportal
- API Publisher  : <a>https://localhost:9443/publisher

Login: admin/admin

### Publisher
- <a>https://localhost:9443/publisher/
   
  Login: admin/admin

### Super admin credentials
`<API-M_HOME>/repository/conf/deployment.toml`
```ini
[super_admin]
username = "admin"
password = "admin"
```
You cannot change password by modifying this file.


### Create a New Api
- Go to the Publish : <a>https://localhost:9443/publisher
![a](/docs/images/wso2-am-usecase1.png)
- **Incoming URL**: <a>http://localhost:8280/api/users/1.0
- Request Header : **Internal-Key** and use the API manager publisher to generate a key value.
- Use **Requestly** Chrome extension for example to modify the request header
- **Outcoming Url**: <a>https://jsonplaceholder.typicode.com/users


### Developer Portal
<a>https://localhost:9443/devportal/


### Logs
**<API_MANAGER_HOME>/repository/logs**
  * **wso2carbon.log**: server runtime logs
  * **http_access_.log**: all HTTP access logs, including information about incoming API requests. They are not enabled by default. <a>https://apim.docs.wso2.com/en/latest/observe/api-manager/monitoring-http-access-logs/

  * **wso2-apigw-errors.log**: API Gateway logs

**Logs Configuration** : `log4j2.properties` 

### Known Errors
- 403 Forbidden to acces Management Console https://localhost:9443/carbon
> Solution: Clear Brower cache. Try with incognito!

    