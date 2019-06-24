# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix user.create via API
#
# Method based on zabbix-ldap-sync project
# Maintained by Marc Schöchlin ms@256bit.org
# Source: https://github.com/zabbix-tooling/zabbix-ldap-sync

from zabbix_api_connection import ZabbixConnectionModule
import sys
import pyzabbix


class ZabbixDeleteModule(ZabbixConnectionModule):

    def __init__(self, zabbix_server):
        super(ZabbixConnectionModule, self).__init__()
        self.zabbix_server = zabbix_server
        self.zabbix_user_id = {}

    def delete_zabbix_user(self, ids):
        self.zabbix_user_id = {
            "userids": f"{ids}"
        }

        try:
            self.zabbix_server.do_request('user.delete', self.zabbix_user_id)
        except pyzabbix.ZabbixAPIException as error_message:
            if 'Error -32602' in error_message:
                print(f"Was not possible to delete user {self.zabbix_user_id}!\n", error_message)
            else:
                print(error_message)
                sys.exit()


if __name__ == "__main__":
    zabbix_server_input = input("Enter the Zabbix server address:\n")
    zabbix_user_input = input("Enter the Zabbix user to login:\n")
    zabbix_pass_input = input("Enter the Zabbix user password:\n")

    zabbix_id_input = input("Enter Zabbix user ID:\n")

    zabbix_connection_obj = ZabbixConnectionModule(zabbix_server_input, zabbix_user_input, zabbix_pass_input)
    zabbix_delete_user = ZabbixDeleteModule(zabbix_connection_obj.zabbix_api_connect())
    zabbix_delete_user.delete_zabbix_user(zabbix_id_input)
    exit()
