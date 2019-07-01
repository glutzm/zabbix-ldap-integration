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


class ZabbixCreateModule(ZabbixConnectionModule):

    def __init__(self, zabbix_server):
        super(ZabbixConnectionModule, self).__init__()
        self.zabbix_server = zabbix_server
        self.new_zabbix_user = {}
        self.new_zabbix_user_defaults = {
            'autologin': 0,
            'type': 3,
            'usrgrps': [{'usrgrpid': '7'}],
            'lang': "pt_BR"
        }

    def create_zabbix_user(self, alias, name, surname):
        self.new_zabbix_user['alias'] = alias
        self.new_zabbix_user['name'] = name
        self.new_zabbix_user['surname'] = surname
        self.new_zabbix_user.update(self.new_zabbix_user_defaults)

        # The variable user_object can be an array/list of users
        try:
            self.zabbix_server.do_request('user.create', self.new_zabbix_user)
        except pyzabbix.ZabbixAPIException:
            logging.exception(f"User {self.new_zabbix_user['name']} {self.new_zabbix_user['surname']} NOT created.")
            return 0
        return 1
