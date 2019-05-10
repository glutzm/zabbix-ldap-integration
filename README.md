# Zabbix LDAP Integration

## Description

> This code was made to help improve the integration between LDAP/AD with Zabbix.
    
## Problem

> Zabbix does integrates already with LDAP/AD, but only authentication. 
In order to use it you have to manually add the user to the Zabbix DB in the 
frontend.
    
## Proposition

> A script that automatically creates the users in Zabbix from a LDAP/AD group.