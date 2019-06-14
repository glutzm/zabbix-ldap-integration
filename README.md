# Zabbix LDAP Integration

## Description

> This code was made to help improve the integration between LDAP/AD with Zabbix.
    
## Problem

> Zabbix does already integrate with LDAP/AD, but only authentication. In order to 
use it you have to manually add the user to Zabbix frontend.
    
## How to use

> You can create a cron job that calls the script "zabbix_ldap_integration.py" and 
receives the connection conf file like the example:

```bash
*/30 * * * *    python3 zabbix_ldap_integration.py < connection.conf  >   /dev/null
```