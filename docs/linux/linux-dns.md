---
layout: default
title: DNS
parent: Linux
nav_order: 7
---

**Bind**   
is used on the most majority of name servers existing in the world(root dns servers included).

**Install Bind** on ubuntu 18.04
> sudo apt install bind9 dnsutils

**Start/stop the NameServer**
> $ sudo /etc/init.d/bind9 restart

**We want to configure a dns server for:**
- zone/domain : safarit.com
- ip class address: 192.168.43.0/24
- name server @ip : 192.168.43.80

**Bind options**: to change listen addr or port
~~~
$ nano /etc/bind/named.conf.options
  listen-on port 2053 { 192.168.43.80;};
  listen-on-v6 { none; };
  allow-recursion { 127.0.0.1;};
~~~

**Add safarit.com and reverse Zones**
~~~
/etc/bind$ cat named.conf.local 

zone "safarit.com" {
       type master;
       file "/etc/bind/db.safarit.com";
       forwarders{};
};


// zone inverse : resolution d'@ip au fqdn 
zone "43.168.192.in-addr.arpa" {
       type master;
       file "/etc/bind/db.safarit.com.reverse";
       forwarders{};
};
~~~

**Configure safarit.com zone: fqdn to @ip**
~~~
/etc/bind$ cat db.safarit.com

$TTL 1H
@  IN SOA ns1.safarit.com. root.safarit.com.  (
                    20200322   ; Serial.
                    1H         ;Refresh 
                    15M        ; Retry
                    2W         ; Expire
                    3M )       ; min TTL  

; name servers - NS records
    IN NS ns1.safarit.com.

; ns A records 
ns1.safarit.com.  IN  A  192.168.43.80 


; 192.168.43.0/24 Name-to-address mapping
redmi   A 192.168.43.1 
pprd    A 192.168.43.10
prod    A 192.168.43.11 
 

; Alias 
pop  CNAME redmi 
smtp CNAME redmi 
www  CNAME redmi
ldap CNAME ns1
taba CNAME ns1
~~~

**Configure reverse zone: @ip to fqdn**
~~~
/etc/bind$ cat db.safarit.com.reverse

$TTL 1H
@  IN SOA ns1.safarit.com. root.safarit.com.  (
           20200323   ; Serial.
           1H         ;Refresh 
           15M        ; Retry
           2W         ; Expire
           3M )       ; min TTL  

; name servers
IN NS ns1.safarit.com.

; Address to name mapping
80  IN  PTR  ns1.safarit.com.    ; 192.168.43.80
1   IN  PTR  redmi.safarit.com.  ; 192.168.43.1
10  IN  PTR  pprd.safarit.com.   ; 192.168.43.10
11  IN  PTR  prod.safarit.com.   ; 192.168.43.11
~~~

**Check zone configuration**   
> $ named-checkzone   safarit.com   db.safarit.com  
> $ named-checkzone   43.168.192.in-addr.arpa   db.safarit.com.reverse


**Edit resolv.conf**  
~~~
$ cat /etc/resolv.conf
search safarit.com
nameserver 192.168.43.80
~~~

**Nslookup**, on other port than default one 53  
> $ nslookup -debug -port=2053 ub1.safarit.com  
> $ dig -p 2053 prod.safarit.com


**Default DNS port**: 53

**Vocabulary**  
|          |                       |
|----------|-----------------------|
|**SOA**   | Authority for the zone|
|**NS**    |Nameserver record      |
|**CNAME** |Canonical name. alias  |
|**A**     |Name-to-address mapping|
|**PTR**   |Address-to-name mapping|
|**IN**    |Internet               |
|||

**NOTA BENE**  
FQDN must end with a dot, "ns1.safarit.com." , mandatory on the dns server side, implied on the client side.
