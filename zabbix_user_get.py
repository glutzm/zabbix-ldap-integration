# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix user.get via API

from zabbix_api_connection import ZabbixConnectionModule


class ZabbixGetModule(ZabbixConnectionModule):

    def __init__(self, zabbix_server):
        super(ZabbixConnectionModule, self).__init__()
        self.zabbix_server = zabbix_server
        self.zabbix_user_id_list = []

    def get_zabbix_user_list(self):
        # print(self.zabbix_server.user.get(output="extend"))
        for self.id in self.zabbix_server.user.get(output="extend"):
            self.zabbix_user_id_list.append(self.id['alias'])
        return self.zabbix_user_id_list


if __name__ == "__main__":
    zabbix_server_input = input("Enter the Zabbix server address:\n")
    zabbix_user_input = input("Enter the Zabbix user to login:\n")
    zabbix_pass_input = input("Enter the Zabbix user password:\n")

    zabbix_connection_obj = ZabbixConnectionModule(zabbix_server_input, zabbix_user_input, zabbix_pass_input)
    zabbix_user_list = ZabbixGetModule(zabbix_connection_obj.zabbix_api_connect())
    zabbix_user_list = zabbix_user_list.get_zabbix_user_list()
    print(zabbix_user_list)
