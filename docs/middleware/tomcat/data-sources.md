---
layout: default
title: Data Sources
parent:  Tomcat
grand_parent: Middleware
nav_order: 3
---

Tomcat 7/8.

### Preventing Database Connection Pool Leaks

```sh
  removeAbandoned="true"
  removeAbandonedTimeout="600"
  logAbandoned="180"
  removeAbandonedTimeout="600" :  
              en seconds. recyclage des connections. Si trop bas, risque de recycler une 
              connection encore active, car la lecture de ResultSet n'est pas prise en compte.
								
  logAbandoned="true" : 
              Logging of abandoned connections, adds overhead for every connection borrowing, 
              because a stack trace has to be generated. The default value is false.
```


###  JDBC Connection Pool Oracle
Add to server.xml

```xml
 <GlobalNamingResources>
    <Resource name="jdbc/myDS" auth="Container"
       type="javax.sql.DataSource" driverClassName="oracle.jdbc.OracleDriver"
       url="jdbc:oracle:thin:@127.0.0.1:1521:mysid"
       username="scott" password="tiger" maxTotal="20" maxIdle="10" maxWaitMillis="-1"
	   removeAbandonedTimeout="180" 
       removeAbandoned="true" 
       logAbandoned="true" 
       testOnBorrow="true" 
       validationQuery="SELECT 1"
       factory="org.apache.tomcat.jdbc.pool.DataSourceFactory"/>
```

**Deprecated/New attributes**  
  maxActive -> maxTotal  
  maxWait -> maxWaitMillis

**Move from commons-dbcp to tomcat-jdbc-pool**: resolve Already created exception
```sh
    factory="org.apache.tomcat.jdbc.pool.DataSourceFactory"
```

###  JDBC Connection Pool MySQL
add to server.xml ou in context.xml(deploy the DS on all applications)

```xml
 <GlobalNamingResources>
    <Resource
    	  name="jdbc/mywikiDS"
    	  auth="Container"
    	  type="javax.sql.DataSource"
    	  factory="org.apache.tomcat.jdbc.pool.DataSourceFactory"
    	  initialSize="10"
    	  maxActive="200"
    	  maxIdle="150"
    	  minIdle="20"
    	  timeBetweenEvictionRunsMillis="34000"
    	  minEvictableIdleTimeMillis="55000"
    	  validationQuery="SELECT 1"
    	  validationInterval="36000"
    	  testOnBorrow="true"
    	  removeAbandoned="true"
    	  removeAbandonedTimeout="60"
          logAbandoned="false" 
          username="mywiki" password="changeit" 
    	  driverClassName="com.mysql.jdbc.Driver"
          url="jdbc:mysql://localhost:3306/mywikidb"
     />

   <Host...>   
    <Context docBase="simple-jee" path="/simple-jee" reloadable="true">
	  <ResourceLink name="jdbc/mywikiDS" global="jdbc/mywikiDS"
                        type="javax.sql.DataSource"/>
 	</Context>


```


### Postgres
- Copy the Postgres JDBC jar to $CATALINA_HOME/lib
- Datasource

```xml
<Resource name="jdbc/myDS" auth="Container" type="javax.sql.DataSource"
       username="postgres"
       password="postgres"
       driverClassName="org.postgresql.Driver"
       url="jdbc:postgresql://localhost:5432/yourDatabaseName"
       maxTotal="25"
       maxIdle="10"
       validationQuery="select 1" /> 
```
- **validationQuery**: validate connections before they are returned to the application. 
  needed? When a database server rebo	ots, or there is a network failure! 



