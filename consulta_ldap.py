# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# LDAP/AD Consult script that returns it in JSON
# Fonts:
#   Stack Over Flow: https://stackoverflow.com/questions/4784775/ldap-query-in-python
#   LDAP3 Documentation (https://ldap3.readthedocs.io/index.html)

import ldap3
import sys
import json


class ConsultaLDAP:

    def __init__(self):
        # super.__init__()
        # connection attributes
        self.server = ldap3.Server('ldaps://auth.test.com:636')
        self.username = "CN=Path,OU=To,OU=ReadUser,DC=test,DC=com"
        self.password = "user_password"
        self.basedn = "DC=test,DC=com"
        # the filter "userAccountControl" is a definition to ignore disabled users
        # here we user the filter class to find users, member of a specific group, ignore disabled users
        # filter to not get class of computer and groups
        self.searchFilter = "(&(objectclass=user)(memberOf=CN=zabbix.admins,OU=PathTo,OU=UserGroupWithAccess," \
                            "DC=test,DC=com)(!(userAccountControl:1.2.840.113556.1.4.803:=2))" \
                            "(!(objectclass=computer))(!(objectclass=group)))"
        # attributes that you want the LDAP/AD to return
        self.searchAttribute = ['sAMAccountName', 'givenName', 'sn']
        # this will scope the entire subtree under UserUnits
        self.searchScope = ldap3.SUBTREE
        self.dereference_aliases = ldap3.DEREF_ALWAYS

    # This function open a connection and binds to the server
    def ldap_bind(self):
        try:
            self.server.protocol_version = ldap3.version
            ldap_conn = ldap3.Connection(self.server, self.username, self.password)
            ldap_conn.bind()
        except ldap3.core.exceptions.LDAPInvalidCredentialsResult:
            print("Your username or password is incorrect.")
            sys.exit(0)
        except ldap3.core.exceptions.LDAPBindError as e:
            if type(e.message) == dict and 'desc' in e.message:
                print(e.message['desc'])
            else:
                print(e)
            sys.exit(0)
        return ldap_conn

    # This function searches for the attributes and filters you selected
    # and return a dictionary of users
    def ldap_search(self):
        ldap_conn = ConsultaLDAP().ldap_bind()
        i = 0
        users = {}
        try:
            # Search the LDAP/AD with the parameters received from the object creation
            entry_list = ldap_conn.extend.standard.paged_search(
                self.basedn, self.searchFilter, self.searchScope, self.dereference_aliases, self.searchAttribute
            )
            for entry in entry_list:
                i = str(i)
                users['user'+i] = dict(entry['attributes'])
                i = int(i)
                i += 1
        except ldap3.core.exceptions.LDAPBindError as e:
            print(e)
        # unbind the session with the LDAP/AD server
        ldap_conn.unbind()
        # transform the users result into json
        users_json = json.dumps(users)
        return users_json


# Script beginning
if __name__ == "__main__":
    print(ConsultaLDAP().ldap_search())
