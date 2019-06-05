# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix user.get via API

import sys
import requests
import json
from ldap_query import LDAPQuery
from pyzabbix import ZabbixAPI


def get_zabbix_user_list(zabbix_server, zabbix_username, zabbix_password):
    zapi = ZabbixAPI(zabbix_server)
    zapi.login(zabbix_username, zabbix_password)
    print("Connected to Zabbix API Version %s" % zapi.api_version())
    print(zapi.user.get(output="extend"))

    # zapi.logout()


if __name__ == "__main__":
    zapi_srv_input = input("Enter the Zabbix server address:\n")
    zapi_user_input = input("Enter the Zabbix user to login:\n")
    zapi_pass_input = input("Enter the Zabbix user password:\n")
    srv_input = input(
        "Enter the LDAP/AD server address:\n"
        "e.g.: 'ldaps://auth.test.com:636'\n"
    )
    ldap_user_input = input(
        "Enter user to bind the ldap/ad:\n"
        "e.g.: 'CN=Path,OU=To,OU=ReadUser,DC=test,DC=com'\n"
    )
    ldap_pass_input = input(
        "Enter the user password:\n"
    )
    basedn_input = input(
        "Enter the base DN to search through:\n"
        "e.g.: 'DC=test,DC=com'\n"
    )
    memberof_input = input(
        "Enter member group do filter users:\n"
        "e.g.: 'CN = zabbix.admins, OU = PathTo, OU = UserGroupWithAccess,DC=test,DC=com'\n"
    )
    users_list = LDAPQuery(srv_input, ldap_user_input, ldap_pass_input, basedn_input, memberof_input)
    print(users_list.ldap_search(users_list.ldap_bind()))
    get_zabbix_user_list(zapi_srv_input, zapi_user_input, zapi_pass_input)
