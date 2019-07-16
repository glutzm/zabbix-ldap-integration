# Zabbix LDAP Integration

## Description

> This code was made to help improve the integration between LDAP/AD with Zabbix.
    
## Problem

> Zabbix does already integrate with LDAP/AD, but only authentication. In order to 
use it you have to manually add the user to Zabbix frontend.

## Requirements

- Python 3.x.x
  - pyzabbix
  - ldap3
- Zabbix 4.2 (only version tested)

⚠ *Warnings*

> *The script at the moment only creates and deletes users based on a single AD group, if you
plan to have separate functions like viewer, editor and admin, it is not implemented yet.*

## How to use

> You can create a cron job that calls the script "zabbix_ldap_integration.py" and 
receives the connection conf file like the example:

### Method 1

1. Download or clone the repository;
    ```bash
    clone https://github.com/GLutzBR/zabbix-ldap-integration.git /PATH/OF/YOUR/CHOICE/
    ```
    
2. Edit the connection.conf example;

3. Create the crontab;
    ```bash
    sudo crontab -e
    ```
    
4. Insert the following line:
    ```bash
    */30 * * * *    python3 /PATH/OF/YOUR/CHOICE/zabbix_ldap_integration.py < connection.conf  >   /dev/null
    ```

### Method 2

> You can use the following ansible script: 
[Ansible Zabbix LDAP Integration](https://github.com/GLutzBR/ansible-zabbix-ldap-integration)