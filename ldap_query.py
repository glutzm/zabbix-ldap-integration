# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# LDAP/AD Query script that returns it in JSON
# Fonts:
#   Stack Over Flow: https://stackoverflow.com/questions/4784775/ldap-query-in-python
#   LDAP3 Documentation (https://ldap3.readthedocs.io/index.html)

import ldap3
import sys


# This class receives the following parameters to initialize your object:
# server, username, password, basedn and memberof
# You call the 'ldap_bind' to connect to the ldap/ad server, then you call the method 'ldap_search' so you can get the
# users you need to query
class LDAPQuery:

    def __init__(self, server, username, password, basedn, memberof):
        # connection attributes
        self.server = ldap3.Server(server)
        self.username = username
        self.password = password
        self.basedn = basedn
        self.memberof = memberof
        # the filter "userAccountControl" is a definition to ignore disabled users
        # here we user the filter class to find users, member of a specific group, ignore disabled users
        # filter to not get class of computer and groups
        self.searchFilter = f"(&(objectclass=user)(memberOf={memberof})" \
                            "(!(userAccountControl:1.2.840.113556.1.4.803:=2))" \
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
    def ldap_search(self, ldap_conn):
        i = 0
        users = []
        try:
            # Search the LDAP/AD with the parameters received from the object creation
            entry_list = ldap_conn.extend.standard.paged_search(
                self.basedn, self.searchFilter, self.searchScope, self.dereference_aliases, self.searchAttribute
            )
            for entry in entry_list:
                i = str(i)
                users.append(dict(entry['attributes']))
                i = int(i)
                i += 1
        except ldap3.core.exceptions.LDAPBindError as e:
            print(e)
        # unbind the session with the LDAP/AD server
        ldap_conn.unbind()
        # transform the users result into json
        return users


# Script beginning
if __name__ == "__main__":
    server_input = input(
        "Enter the server connection:\n"
        "e.g.: 'ldaps://auth.test.com:636'\n"
    )
    username_input = input(
        "Enter user to bind the ldap/ad:\n"
        "e.g.: 'CN=Path,OU=To,OU=ReadUser,DC=test,DC=com'\n"
    )
    password_input = input(
        "Enter the user password:\n"
    )
    basedn_input = input(
        "Enter the base DN to search through:\n"
        "e.g.: 'DC=test,DC=com'\n"
    )
    memberof_input = input(
        "Enter member group do filter users:\n"
        "e.g.: 'CN=zabbix.admins,OU=PathTo,OU=UserGroupWithAccess,DC=test,DC=com'\n"
    )
    query_object = LDAPQuery(server_input, username_input, password_input, basedn_input, memberof_input)
    print(query_object.ldap_search(query_object.ldap_bind()))
