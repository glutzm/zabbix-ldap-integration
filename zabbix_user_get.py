# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix user.get via API

import sys
import requests
import json
from ldap_query import LDAPQuery


def get_zabbix_user():
    sys.exit()


if __name__ == "__main__":
    server_input = input(
        "Enter the server connection:\n"
        "e.g.: 'ldaps://auth.test.com:636'\n"
    )
    username_input = input(
        "Enter user to bind the ldap/ad:\n"
        "e.g.: 'CN=Path,OU=To,OU=ReadUser,DC=test,DC=com'\n"
    )
    password_input = input(
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
    users_list = LDAPQuery(server_input, username_input, password_input, basedn_input, memberof_input)
    print(users_list.ldap_search(users_list.ldap_bind()))
