# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix user.create via API

from zabbix_api_connection import ZabbixConnectionModule


class ZabbixCreateModule(ZabbixConnectionModule):

    def __init__(self, zabbix_server):
        super(ZabbixConnectionModule, self).__init__()
        self.zabbix_server = zabbix_server
        self.alias = ''
        self.name = ''
        self.surname = ''
        self.lang = "pt_BR"
        self.usrgrps = [
            {
                "usrgrpid": "7"
            }
        ]

    def create_zabbix_user(self, alias, name, surname):
        self.alias = alias
        self.name = name
        self.surname = surname

        # The variable user_object can be an array/list of users
        self.zabbix_server.user.create(
            self.alias,
            self.name,
            self.surname,
            self.lang,
            self.usrgrps
        )


if __name__ == "__main__":
    zabbix_server_input = input("Enter the Zabbix server address:\n")
    zabbix_user_input = input("Enter the Zabbix user to login:\n")
    zabbix_pass_input = input("Enter the Zabbix user password:\n")

    ldap_samaccountname = "glutz"
    ldap_givenname = "Gustavo"
    ldap_sn = "Lutz de Matos"

    zabbix_connection_obj = ZabbixConnectionModule(zabbix_server_input, zabbix_user_input, zabbix_pass_input)
    zabbix_create_user = ZabbixCreateModule(zabbix_connection_obj.zabbix_api_connect())
    zabbix_create_user.create_zabbix_user(ldap_samaccountname, ldap_givenname, ldap_sn)
