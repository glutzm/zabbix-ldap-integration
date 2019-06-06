# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix connection to API

from pyzabbix import ZabbixAPI


class ZabbixConnectionModule(object):

    def __init__(self, zabbix_server, zabbix_username, zabbix_password):
        self.zabbix_server = zabbix_server
        self.zabbix_username = zabbix_username
        self.zabbix_password = zabbix_password
        self.zabbix_server = ZabbixAPI(self.zabbix_server)

    def zabbix_api_connect(self):

        self.zabbix_server.login(self.zabbix_username, self.zabbix_password)
        print("Connected to Zabbix API Version %s" % self.zabbix_server.api_version())
        return self.zabbix_server


if __name__ == "__main__":
    zabbix_server_input = input("Enter the Zabbix server address:\n")
    zabbix_user_input = input("Enter the Zabbix user to login:\n")
    zabbix_pass_input = input("Enter the Zabbix user password:\n")
