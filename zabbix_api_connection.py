# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# Zabbix connection to API

from pyzabbix import ZabbixAPI
import logging
import sys


class ZabbixConnectionModule(object):

    def __init__(self, zabbix_server, zabbix_username, zabbix_password):
        self.zabbix_server = zabbix_server
        self.zabbix_username = zabbix_username
        self.zabbix_password = zabbix_password
        self.zabbix_server = ZabbixAPI(self.zabbix_server)

    def zabbix_api_connect(self):
        try:
            self.zabbix_server.login(self.zabbix_username, self.zabbix_password)
            logging.info("Connected to Zabbix API Version %s" % self.zabbix_server.api_version())
            return self.zabbix_server
        except ZabbixAPI.ZabbixAPIException:
            logging.exception("Couldn't connect to Zabbix API.")
            sys.exit()
