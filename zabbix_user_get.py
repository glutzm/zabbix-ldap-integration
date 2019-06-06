# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix user.get via API

import sys
import requests
import json
from ldap_query import LDAPQuery
from pyzabbix import ZabbixAPI


class ZabbixModule:

    def __init__(self, zabbix_server, zabbix_username, zabbix_password):
        self.zabbix_server = zabbix_server
        self.zabbix_username = zabbix_username
        self.zabbix_password = zabbix_password
        self.zapi = ZabbixAPI(self.zabbix_server)
        self.zapi.login(self.zabbix_username, self.zabbix_password)
        self.zabbix_user_id_list = []
        print("Connected to Zabbix API Version %s" % self.zapi.api_version())

    def get_zabbix_user_list(self):
        # print(self.zapi.user.get(output="extend"))
        for self.id in self.zapi.user.get(output="extend"):
            self.zabbix_user_id_list.append(self.id['alias'])
        return self.zabbix_user_id_list


class LDAPModule:

    def __init__(self, ldap_server, ldap_user, ldap_password, ldap_basedn, ldap_memberof):
        self.ldap_server = ldap_server
        self.ldap_user = ldap_user
        self.ldap_password = ldap_password
        self.ldap_basedn = ldap_basedn
        self.ldap_memberof = ldap_memberof
        self.ldap_connection_obj = LDAPQuery(
            self.ldap_server,
            self.ldap_user,
            self.ldap_password,
            self.ldap_basedn,
            self.ldap_memberof
        )
        self.ldap_users_list_obj = self.ldap_connection_obj.ldap_search(self.ldap_connection_obj.ldap_bind())
        self.ldap_ids = []

    def get_ldap_user_list(self):
        for account_name_filter in self.ldap_users_list_obj:
            self.ldap_ids.append(account_name_filter['sAMAccountName'])
        return self.ldap_ids


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
        "e.g.: 'CN=zabbix.admins,OU=PathTo,OU=UserGroupWithAccess,DC=test,DC=com'\n"
    )

    ldap_user_obj = LDAPModule(srv_input, ldap_user_input, ldap_pass_input, basedn_input, memberof_input)
    ldap_users_list = ldap_user_obj.get_ldap_user_list()

    zabbix_user_obj = ZabbixModule(zapi_srv_input, zapi_user_input, zapi_pass_input)
    zabbix_user_list = zabbix_user_obj.get_zabbix_user_list()

    for ldap_login in ldap_users_list:
        if ldap_login not in zabbix_user_list:
            print(ldap_login)
        else:
            print(
                f"{ldap_login} already in Zabbix!")
