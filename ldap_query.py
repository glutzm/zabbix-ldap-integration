# Created by: Gustavo Antonio Lutz de Matos
# e-mail: gustavo.almatos@gmail.com
# LDAP/AD Query script that returns it in JSON
# Fonts:
#   Stack Over Flow: https://stackoverflow.com/questions/4784775/ldap-query-in-python
#   LDAP3 Documentation (https://ldap3.readthedocs.io/index.html)

import ldap3
import sys
import logging


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
            logging.info("Bind successful.")
        except ldap3.core.exceptions.LDAPInvalidCredentialsResult:
            logging.error("Your username or password is incorrect.")
            sys.exit(0)
        except ldap3.core.exceptions.LDAPBindError as e:
            if type(e.message) == dict and 'desc' in e.message:
                error_value = e.message['desc']
                str(error_value)
                logging.error("Failed to bind!\n", error_value)
            else:
                logging.exception("Failed to bind!")
            sys.exit(0)
        return ldap_conn

    # This function searches for the attributes and filters you selected
    # and return a dictionary of users
    def ldap_search(self, ldap_conn):
        users = []
        try:
            # Search the LDAP/AD with the parameters received from the object creation
            entry_list = ldap_conn.extend.standard.paged_search(
                self.basedn,
                self.searchFilter,
                self.searchScope,
                self.dereference_aliases,
                self.searchAttribute,
                paged_size=5,
                generator=False
            )
            # print(entry_list)
            for entry in entry_list:
                try:
                    users.append(dict(entry['attributes']))
                except KeyError:
                    continue
        except ldap3.core.exceptions.LDAPBindError:
            logging.exception("Failed to bind!")
        # unbind the session with the LDAP/AD server
        ldap_conn.unbind()
        return users
