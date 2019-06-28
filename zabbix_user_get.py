# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix user.get via API

from zabbix_api_connection import ZabbixConnectionModule
import datetime
import pyzabbix


class ZabbixGetModule(ZabbixConnectionModule):

    def __init__(self, zabbix_server):
        super(ZabbixConnectionModule, self).__init__()
        self.zabbix_server = zabbix_server
        self.current_time = datetime.datetime.now()

    def get_zabbix_user_list(self):
        try:
            return self.zabbix_server.user.get(output="extend")
        except pyzabbix.ZabbixAPIException as error_message:
            print(self.current_time.strftime("[%Y-%m-%d %H:%M:%S]"), error_message)
            return 0


if __name__ == "__main__":
    zabbix_server_input = input("Enter the Zabbix server address:\n")
    zabbix_user_input = input("Enter the Zabbix user to login:\n")
    zabbix_pass_input = input("Enter the Zabbix user password:\n")

    zabbix_connection_obj = ZabbixConnectionModule(zabbix_server_input, zabbix_user_input, zabbix_pass_input)
    zabbix_user_list = ZabbixGetModule(zabbix_connection_obj.zabbix_api_connect())
    zabbix_user_list = zabbix_user_list.get_zabbix_user_list()
    print(zabbix_user_list)
