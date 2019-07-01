# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix user.get via API

from zabbix_api_connection import ZabbixConnectionModule
import logging
import pyzabbix


class ZabbixGetModule(ZabbixConnectionModule):

    def __init__(self, zabbix_server):
        super(ZabbixConnectionModule, self).__init__()
        self.zabbix_server = zabbix_server

    def get_zabbix_user_list(self):
        try:
            user_list = self.zabbix_server.user.get(output="extend")
            logging.info("User list extracted.")
            return user_list
        except pyzabbix.ZabbixAPIException:
            logging.exception("Couldn't get users list.")
            return 0
