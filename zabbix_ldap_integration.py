# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix and LDAP Integration

from zabbix_user_get import ZabbixGetModule
from zabbix_user_create import ZabbixCreateModule
from zabbix_api_connection import ZabbixConnectionModule
from ldap_query import LDAPQuery


class ZabbixLDAPIntegration:

    def __init__(
            self,
            zabbix_server,
            zabbix_username,
            zabbix_password,
            ldap_server,
            ldap_username,
            ldap_password,
            ldap_basedn,
            ldap_memberof
    ):
        self.zabbix_server = zabbix_server
        self.zabbix_username = zabbix_username
        self.zabbix_password = zabbix_password

        self.zabbix_connection_obj = ZabbixConnectionModule(
            self.zabbix_server,
            self.zabbix_username,
            self.zabbix_password
        )

        self.ldap_server = ldap_server
        self.ldap_username = ldap_username
        self.ldap_password = ldap_password
        self.ldap_basedn = ldap_basedn
        self.ldap_memberof = ldap_memberof

    def get_zabbix_users_function(self):
        zabbix_user_list = ZabbixGetModule(self.zabbix_connection_obj.zabbix_api_connect())
        return zabbix_user_list.get_zabbix_user_list()

    def get_ldap_users_function(self):
        query_object = LDAPQuery(
            self.ldap_server,
            self.ldap_username,
            self.ldap_password,
            self.ldap_basedn,
            self.ldap_memberof
        )
        return query_object.ldap_search(query_object.ldap_bind())

    def create_zabbix_users_function(self, ldap_samaccountname, ldap_givenname, ldap_sn):
        zabbix_create_user = ZabbixCreateModule(self.zabbix_connection_obj.zabbix_api_connect())
        zabbix_create_user.create_zabbix_user(ldap_samaccountname, ldap_givenname, ldap_sn)
        exit()

    def update_zabbix_users_function(self, ldap_samaccountname, ldap_givenname, ldap_sn):
        exit()

    def disable_zabbix_users_function(self, ldap_samaccountname, ldap_givenname, ldap_sn):
        exit()

    def delete_zabbix_users_function(self, ldap_samaccountname, ldap_givenname, ldap_sn):
        exit()


def compare_users_function(zabbix_login_list, ldap_user_list):
    for account_name in ldap_user_list:
        if account_name['sAMAccountName'] not in zabbix_login_list:
            print(account_name['sn'])
            ZabbixLDAPIntegration.create_zabbix_users_function(
                account_name['sAMAccountName'],
                account_name['givenName'],
                account_name['sn']
            )


if __name__ == "__main__":
    zabbix_server_input = input("Enter the Zabbix server address:\n")
    zabbix_user_input = input("Enter the Zabbix user to login:\n")
    zabbix_pass_input = input("Enter the Zabbix user password:\n")

    ldap_server_input = input(
        "Enter the server connection:\n"
        "e.g.: 'ldaps://auth.test.com:636'\n"
    )
    ldap_username_input = input(
        "Enter user to bind the ldap/ad:\n"
        "e.g.: 'CN=Path,OU=To,OU=ReadUser,DC=test,DC=com'\n"
    )
    ldap_password_input = input(
        "Enter the user password:\n"
    )
    ldap_basedn_input = input(
        "Enter the base DN to search through:\n"
        "e.g.: 'DC=test,DC=com'\n"
    )
    ldap_memberof_input = input(
        "Enter member group do filter users:\n"
        "e.g.: 'CN=zabbix.admins,OU=PathTo,OU=UserGroupWithAccess,DC=test,DC=com'\n"
    )

    compare_obj = ZabbixLDAPIntegration(
        zabbix_server_input,
        zabbix_user_input,
        zabbix_pass_input,
        ldap_server_input,
        ldap_username_input,
        ldap_password_input,
        ldap_basedn_input,
        ldap_memberof_input
    )

    zbx_usr_list = compare_obj.get_zabbix_users_function()
    ldap_usr_list = compare_obj.get_ldap_users_function()
    compare_users_function(zbx_usr_list, ldap_usr_list)
    exit()
