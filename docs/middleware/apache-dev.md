---
layout: default
title: Apache Development
parent: Middleware
nav_order: 4.5
---


### Object

Develop a new Module for Apache Httpd

Reference : https://httpd.apache.org/docs/trunk/developer/modguide.html

### Install APX Tool 

		sudo apt install apache2-dev

### Create a Modulte Template 

		apxs -g -n my_check

### Compile The Module: mod_my_check.so

		apxs -c -i mod_my_check.c

### Load Module 

	LoadModule my_check_module /usr/lib/apache2/modules/mod_my_check.so

	<Location /my_check>
   		SetHandler my_check
	</Location>

### Test

	lynx -mime_header http://localhost/my_check 

	HTTP/1.1 200 OK
	Date: Fri, 21 Jul 2023 15:03:38 GMT
	Server: Apache/2.4.41 (Ubuntu)
	Content-Length: 36
	Connection: close
	Content-Type: text/html

	The sample page from mod_my_check.c


### mod_my_check.c
```java
#include "httpd.h"
#include "http_config.h"
#include "http_protocol.h"
#include "ap_config.h"

/* Static Config*/
typedef struct {
    int         enabled;      /* Enable or disable our module */
    const char *path;         /* Some path to...something */
    int         typeOfAction; /* 1 means action A, 2 means action B and so on */
} my_check_config;

static my_check_config config;


/* The sample content handler */
static int my_check_handler(request_rec *r)
{
    if (strcmp(r->handler, "my_check")) {
        return DECLINED;
    }
    r->content_type = "text/plain";      

   ap_rprintf(r, "Enabled: %u\n", config.enabled);
   ap_rprintf(r, "Path: %s\n", config.path);
   ap_rprintf(r, "TypeOfAction: %x\n", config.typeOfAction);
 
   if (!r->header_only)
        ap_rputs("My CHECK : Hello, world!\n", r);
   return OK;
}

static void my_check_register_hooks(apr_pool_t *p)
{
	config.enabled = 1;
    config.path = "/fo/bar";
    config.typeOfAction = 0x00;
    
    ap_hook_handler(my_check_handler, NULL, NULL, APR_HOOK_MIDDLE);
}

/* Dispatch list for API hooks */
module AP_MODULE_DECLARE_DATA my_check_module = {
    STANDARD20_MODULE_STUFF, 
    NULL,                  /* create per-dir    config structures */
    NULL,                  /* merge  per-dir    config structures */
    NULL,                  /* create per-server config structures */
    NULL,                  /* merge  per-server config structures */
    NULL,                  /* table of config file commands       */
    my_check_register_hooks  /* register hooks                      */
};
```
