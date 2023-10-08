---
layout: default
title: Postgresql
parent: Data Base
nav_order: 3
---


Env: Centos 7, Postgresql 9

### SetUp 
    yum install postgresql-server

	postgresql-setup initdb

### Start/Stop
     systemctl enable/start postgresql


### Create a User and Database

Create a Database:    
	su - postgres

	createdb mywikidb

### Users and Roles

Create a User:
	
	su - postgres

	createuser  admin2

Change the user password

	psql mywikidb

	mywikidb=# alter user admin2 with encrypted password 'admin2';
	
Show Users:
> mywikidb=# \du

List of Roles

	mywikidb=# SELECT rolname FROM pg_roles;


Grand a User to Access the database

	grant all privileges on database mywikidb to admin2;

Exit from psql
>\q

### Access the Database
	su - postgres
	psql mywikidb

Show All Tables:
> mywikidb=# select * from pg_catalog.pg_tables;

Show Users:
> mywikidb=# \du

Show Listening Port:
>mywikidb=# \conninfo

### Nombre de connections ouverts
  
	select count(*) from pg_stat_activity;

### Errors
1. Testing a Datasource in Wildfly **FATAL: Ident authentication failed for user "admin"**. 

	1.1 Edit File **pg_hba.conf**

		mywikidb=# show hba_file ;
        	/var/lib/pgsql/data/pg_hba.conf

	1.2 With

		host    all             all             127.0.0.1/32         password
		host    all             all             REMOTE_IP            password

	1.3 Retart Postgres

		systemctl restart postgresql