# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix user.create via API
#
# Method based on zabbix-ldap-sync project
# Maintained by Marc Schöchlin ms@256bit.org
# Source: https://github.com/zabbix-tooling/zabbix-ldap-sync

from zabbix_api_connection import ZabbixConnectionModule
import logging
import pyzabbix


class ZabbixDeleteModule(ZabbixConnectionModule):

    def __init__(self, zabbix_server):
        super(ZabbixConnectionModule, self).__init__()
        self.zabbix_server = zabbix_server
        self.zabbix_user_id = {}

    def delete_zabbix_user(self, zabbix_user_id, zabbix_user_name, zabbix_user_surname):
        self.zabbix_user_id = {
            "userids": f"{zabbix_user_id}"
        }

        try:
            self.zabbix_server.do_request('user.delete', self.zabbix_user_id)
        except pyzabbix.ZabbixAPIException:
            logging.exception(f"User {zabbix_user_name, zabbix_user_surname} NOT removed!")
            return 0
        return 1
