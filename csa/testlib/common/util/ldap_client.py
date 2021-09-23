#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/ldap_client.py#1 $ $DataTime:$ $Author: aminath $

from pprint import pformat

from common.util.utilcommon import UtilCommon

import sal.servers.ldap as ldap
import common.util.connectioncache as connectioncache


def rf_value_to_ldap_mod_value(rf_value):
    if isinstance(rf_value, basestring):
        if rf_value.find(',') >= 0:
            return map(lambda x: str(x.strip()), rf_value.split(','))
        else:
            return str(rf_value)
    else:
        return rf_value


class LdapClient(UtilCommon):
    """
    Keywords for working with ldap clients. All keywords from this library
    depends on currently active instance of ldap connection, if multiple
    connection excist. When you use `Ldap Client Connect` keyword it return you
    new index wich you can use to switch connection. If you provide `alias`
    parameter to this `Ldap Client Connect` keyword, you can use alias to switch
    connection.
    """

    _cache = connectioncache.ConnectionCache(no_current_msg="No connected"
                                                            " clients")

    def get_keyword_names(self):
        return [
            'ldap_client_connect',
            'ldap_client_switch',
            'ldap_client_disconnect',
            'ldap_client_create_modlist',
            'ldap_client_add_custom_entry',
            'ldap_client_add_user',
            'ldap_client_add_group',
            'ldap_client_delete_custom_entry',
            'ldap_client_delete_user',
            'ldap_client_delete_group',
            'ldap_client_modify_custom_entry',
            'ldap_client_modify_user',
            'ldap_client_modify_group',
            'ldap_client_create_user',
            'ldap_client_create_group',
            'ldap_client_search_custom_entries',
            'ldap_client_get_user',
            'ldap_client_get_group',
        ]

    def ldap_client_disconnect(self):
        """
        Disconnect from ldap server. After this opperation current active
        session will be changed to the previous connected. It is strongly
        recomend switch session manualy after running this keyword.

        *Parameters*
            None

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Client Disconnect |
        """
        self._cache.current.disconnect()
        self._cache.delete(self._cache.current_index)
        return self._cache.current_index

    def ldap_client_switch(self, alias):
        """
        Switch current connection.

        *Parameters*
         - `alias`: string wich will indicate this connection. String.

        *Return*
            None.

        *Exceptions*
         - ValueError: if provided alias wich doesn't excist.

        *Example*
        | Ldap Client Switch | connection_to_openldap |
        | ${index} | Ldap Client Connect 10.10.10.10 |
        | Ldap Client Switch | ${index} |
        """
        self._cache.switch(alias)

    def ldap_client_connect(self, host, ldap_server_type="openldap", port=None,
                            binddn=None, password=None, basedn=None, alias=None):
        """
        Make connection to ldap server.

        *Parameters*
        - `host`: host to which you want to connect. String.
        - `ldap_server_type`: type of running on host ldap server software.
          String. Posible values are 'openldap', 'ad', 'sunone'. Default is
          'openldap'.
        - `port`: port on which ldap server is listened. String. Default is 389.
        - `binddn`: full canonical name of user as wich you want to be
          authenticated to the server. Default is
          'uid=rblaes,ou=people,ou=corporate,dc=qa'.
        - `password`: password for user provided in `binddn`. String. Default
          is 'rblaes'.
        - `basedn`: Context relative to which all object in ldap will be taking.
          String. Default is "ou=testdata, dc=qa".
        - `alias`: identificator of this connection.

        *Return*
            Index of connection

        *Exceptions*
            NotImplementedError if you provide unknown type of ldap server.

        *Examples*
        | Ldap Client Connect | sma19.sma | ldap_server_type=openldap |
        | ... | port=389 | binddn=cn=admin,dc=sma19,dc=sma |
        | ... | password=ironport  basedn=ou=People,dc=sma19,dc=sma |
        | ... | alias=sma19 |
        | Ldap Client Connect | openldap.qa | alias=openldap |
        """
        if ldap_server_type.lower() == "openldap":
            return self._cache.register(ldap.EuqOpenLdapClient(host, port, binddn,
                                                               password, basedn).connect(), alias)
        elif ldap_server_type.lower() == "ad":
            return self._cache.register(ldap.EuqAdLdapClient(host, port, binddn,
                                                             password, basedn).connect(), alias)
        elif ldap_server_type.lower() == "sunone":
            return self._cache.register(ldap.EuqSunOneLdapClient(host, port,
                                                                 binddn, password, basedn).connect(), alias)
        else:
            raise NotImplementedError, "Unknown server type"

    def ldap_client_create_modlist(self, *args):
        """Creates modlist parameter for further use in add/modify
        custom entries.

        *Parameters:*
        - `MODOPS`: special flag. If present then modify parameter
        is expected for each chunk
        - 'SEPARATOR': special flag. Sets custom separator char for
        LDAP attribute values. Comma (",") by default. Usage: SEPARATOR=;
        - `*args`: modlist values. If this is modlist for add operation
        then each chunk should contain 2 elements: attribute name and
        attribute value. Attribute value could be list. Each list item is
        separated by SEPARATOR char. If this parameter is for modifying
        LDAP entry then MODOPS flag is mandatory and each chunk's first
        arameter should be operation name and then attribute name and value.
        Possible operation values are:
        | ADD |
        | REMOVE |
        | REPLACE |
        Also, the specially reserved "auto" keyword may be used as attribute
        value. Put it as attribute value if it is necessary to generate some
        unique (within current LDAP BASE DN) integer identifier for the
        particular attribute.
        Read http://www.packtpub.com/article/python-ldap-applications-more-ldap-operations-and-the-ldap-url-library
        for more details about how to construct modlists. Also, note that each modlist
        may contain several mandatory parameters depending on objectClass used.

        *Exceptions:*
        - `ValueError`: if count of arguments in modlist does not satisfy
        documented requirements

        *Examples:*
        | ${modlist}= | LDAP Client Create Modlist |
        | ... | objectClass | posixAccount,inetOrgPerson |
        | ... | uid | ${CUSTOM_LDAP_UID} |
        | ... | userPassword | ${CUSTOM_LDAP_UID_PASSWORD} |
        | ... | cn | ${CUSTOM_LDAP_UID_FULL_NAME} |
        | ... | mail | ${CUSTOM_LDAP_UID_EMAIL} |
        | ... | gidNumber | auto |
        | ... | homeDirectory | /home/${CUSTOM_LDAP_UID} |
        | ... | sn | ${CUSTOM_LDAP_UID_SERIAL} |
        | ... | uidNumber | auto |
        | LDAP Client Add Custom Entry | uid=${CUSTOM_LDAP_UID},${LDAP_BASEDN} |
        | ... | ${modlist} |
        | ${edit_modlist}= | LDAP Client Create Modlist | MODOPS |
        | ... | REPLACE | userPassword | 1234 |
        | ... | ADD | ou |
        | LDAP Client Modify Custom Entry | uid=${CUSTOM_LDAP_UID},${LDAP_BASEDN} |
        | ... | ${edit_modlist} |
        """
        args = tuple(map(str, args))
        result = self._cache.current.create_modlist(*args)
        self._info('Modlist value:\n%s' % (pformat(result),))
        return result

    def ldap_client_add_custom_entry(self, dn, modlist):
        """Add custom entry to LDAP

        *Parameters:*
        - `dn`: the distinguished name (DN) of the entry to add
        - `modlist`: a list of attributes to be added. Result of
        `LDAP Client Create Modlist` keyword

        *Exceptions:*
        - http://www.python-ldap.org/doc/html/ldap.html#exceptions

        *Examples:*
        | ${modlist}= | LDAP Client Create Modlist |
        | ... | objectClass | posixAccount,inetOrgPerson |
        | ... | uid | ${CUSTOM_LDAP_UID} |
        | ... | userPassword | ${CUSTOM_LDAP_UID_PASSWORD} |
        | ... | cn | ${CUSTOM_LDAP_UID_FULL_NAME} |
        | ... | mail | ${CUSTOM_LDAP_UID_EMAIL} |
        | ... | gidNumber | auto |
        | ... | homeDirectory | /home/${CUSTOM_LDAP_UID} |
        | ... | sn | ${CUSTOM_LDAP_UID_SERIAL} |
        | ... | uidNumber | auto |
        | LDAP Client Add Custom Entry | uid=${CUSTOM_LDAP_UID},${LDAP_BASEDN} |
        | ... | ${modlist} |
        """
        self._cache.current.add_custom_entry(str(dn), modlist)

    def ldap_client_delete_custom_entry(self, dn):
        """Delete custom entry from LDAP

        *Parameters:*
        - `dn`: the distinguished name (DN) of the entry to delete

        *Exceptions:*
        - http://www.python-ldap.org/doc/html/ldap.html#exceptions

        *Examples:*
        | LDAP Client Delete Custom Entry | uid=${CUSTOM_LDAP_UID},${LDAP_BASEDN} |
        """
        self._cache.current.delete_custom_entry(str(dn))

    def ldap_client_modify_custom_entry(self, dn, modlist):
        """Modify custom entry in LDAP

        *Parameters:*
        - `dn`: the distinguished name (DN) of the entry to be edited
        - `modlist`: a list of attributes to be edited. Result of
        `LDAP Client Create Modlist` keyword

        *Exceptions:*
        - http://www.python-ldap.org/doc/html/ldap.html#exceptions

        *Examples:*
        | ${edit_modlist}= | LDAP Client Create Modlist | MODOPS |
        | ... | REPLACE | userPassword | 1234 |
        | ... | ADD | ou | Cisco |
        | LDAP Client Modify Custom Entry | uid=${CUSTOM_LDAP_UID},${LDAP_BASEDN} |
        | ... | ${edit_modlist} |
        """
        self._cache.current.modify_custom_entry(str(dn), modlist)

    def ldap_client_search_custom_entries(self, base, scope, filterstr, timeout=60):
        """Search custom entry in LDAP

        *Parameters:*
        - `base`: the DN of the entry at which to start the search
        - `scope`: one of
        | BASE | to search the object itself |
        | ONELEVEL | to search the object's immediate children |
        | SUBTREE | to search the object and all its descendants |
        - `filterstr`: string representation of the filter to apply in the search.
        See also RFC 4515 - Lightweight Directory Access Protocol (LDAP):
        String Representation of Search Filters
        - `timeout`: maximum timout in seconds to return entries defined
        by filterstr. 60 seconds by default

        *Return:*
        List of tuples. Each tuple is of the form (dn, attrs), where dn is a string
        containing the DN (distinguished name) of the entry, and attrs is a
        dictionary containing the attributes associated with the entry.
        The keys of attrs are strings, and the associated values are lists of strings.

        *Exceptions:*
        - http://www.python-ldap.org/doc/html/ldap.html#exceptions

        *Examples:*
        | ${query}= | Set Variable | (&(ou=${CUSTOM_LDAP_UID_OU})(objectClass=posixAccount)) |
        | ${result}= | LDAP Client Search Custom Entries | ${LDAP_BASEDN} |
        | ... | SUBTREE | ${query} |
        | Log | ${result} |
        | Should Not Be Empty | ${result} |
        """
        return self._cache.current.search_custom_entries(str(base),
                                                         str(scope),
                                                         str(filterstr),
                                                         int(timeout))

    def ldap_client_add_user(self, *args):
        """
        Add user to ldap.

        *Parameters*
         - `uid`: uid for user. String.
         - `password`: password for account. String.
         - `mail`: email address for user. String.
         - `mail_alternate_address`: value for 'mailAlternateAddress' ldap
           attribute. String. By default left empty.
         - `mail_local_address`: value for 'mailLocalAddress' ldap attribute.
           String. By default left empty.
         - `mail_routing_address`: value for 'mailRoutingAddress' ldap
           attribute. String. By default left empty.
         - `posixAccount`: Add 'posixAccout' class to this object. Boolean. By
           default ${False}.
         - `uidNumber`: value for 'uidNumber' ldap attribute. Can be provided
           only if you make this object will belong to 'posixAccount' class. By
           default autogenerate.
         - `gidNumber`: value for 'gidNumber' ldap attribute. Can be provided
           only if you make this object will belong to 'posixAccount' class. By
           default autogenerate.
         - `homeDirectory`: value for 'homeDirectory' ldap attribute.
           Can be provided only if you make this object will belong to
           'posixAccount' class. By default '/homedir/uid_of_object'.
         - `basedn`: context in which you want create user. String. By default
           equal to basedn which was provided to 'Ldap Client Connect'.
        - `objectclass`: comma separated object classes to which the user
                         belongs.

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Client Add User |  uid=vpyvovar | password=password1 |
        | ... | mail=vpyvovar@mail.qa |
        | ... | mail_alternate_address=alt_mail@mail.qa |
        | ... | mail_local_address=local_mail1@mail.qa |
        | ... | mail_routing_address=mail.qa | posixAccount=${False} |
        | Ldap Client Add User |  uid=delete_me | password=any_word |
        | ... | mail=delete_me@mail.qa |
        | ... | posixAccount=${True} | objectclass=inetorgperson,person |
        """
        kwargs = self._parse_args(args)
        if kwargs.get("posixAccount", None):
            if kwargs.get('posixAccount') == "False":
                del kwargs['posixAccount']
        self._cache.current.add_user(**kwargs)

    def ldap_client_delete_user(self, uid, basedn=None):
        """
        Delete user from ldap.

        *Parameters*
        - `uid`: uid of user to delete. String.
        - `basedn`: context in which you want delete user. String. By default
           equal to basedn which was provided to 'Ldap Client Connect'.

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Clien Delete User | vpyvovar |
        | Ldap Clien Delete User | ready_to_be_deleted |
        | ... | ou=people,dc=cisco,dc=com |
        """
        self._cache.current.delete_user(uid, basedn=None)

    def ldap_client_add_group(self, cn, gid=None, members=None, basedn=None):
        """
        Add group to ldap.

        *Parameters*
        - `cn`: value for 'cn' ldap attribute. String.
        - `gid`: value for 'gid' ldap attribute. String. By default will be
          generated automaticals.
        - `members`: ldap user which you want to associate with group.
            String.By default empty.
        - `basedn`: context in which you want create group. String. By default
           equal to basedn which was provided to 'Ldap Client Connect'.

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Client Add Group | delete_me | gid=8925 | members=me, you, they |
        | Ldap Client Add Group | delete_me |
        """
        self._cache.current.add_group(cn, gid, members, basedn)

    def ldap_client_delete_group(self, cn, basedn=None):
        """
        Delete group from ldap.

        *Parameters*
        - `cn`: 'cn' of object which you want delete from ldap. String.
        - `basedn`: context in which you want delete group. String. By default
           equal to basedn which was provided to 'Ldap Client Connect'.
            None

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Client Delete Group | group_name |
        | Ldap Client Delete Group | group_name | ou=people,dc=cisco,dc=com |
        """
        self._cache.current.delete_group(cn, basedn=basedn)

    def ldap_client_modify_user(self, uid, mod_param_name, mod_param_value,
                                mod_add=False, basedn=None):
        """
        Modify excisted in ldap user.

        *Parameters*
         - `uid`: uid for user. String.
         - `mod_param_name`: name of ldap attribute to modify. String.
         - `mod_param_value`: value for `mod_param_name` attribute in ldap.
           String.
         - `mod_add`: Boolean. Default ${False}. If ${True}, provided values will be
           added to excisting. If ${False}, provided values will replace
           excisting.
         - `basedn`: context in which you want create user. String. By default
           equal to basedn which was provided to 'Ldap Client Connect'.

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Client Modify User | vpyvovar | sn | v.pyvovar |
        | Ldap Client Modify User | uid=vpyvovar |
        | ... | mail | vpyvovar@mail.qa | ou=people,dc=cisco,dc=com |
        """
        self._cache.current.modify_user(uid, mod_param_name,
                                        rf_value_to_ldap_mod_value(mod_param_value),
                                        mod_add, basedn)

    def ldap_client_modify_group(self, cn, mod_param_name, mod_param_value,
                                 basedn=None):
        """
        Modify excisted in ldap group.

        *Parameters*
         - `uid`: uid for group. String.
         - `mod_param_name`: name of ldap attribute to modify. String.
         - `mod_param_value`: value for `mod_param_name` attribute in ldap.
           String.
         - `basedn`: context in which you want modify group. String. By default
           equal to basedn which was provided to 'Ldap Client Connect'.

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Client Modify Group | delete_me | gidNumber | 9090 |
        | Ldap Client Modify Group | delete_me | members | he, she, it |
        """
        self._cache.current.modify_group(cn, mod_param_name,
                                         rf_value_to_ldap_mod_value(mod_param_value),
                                         basedn=None)

    def ldap_client_get_group(self, cn, basedn=None):
        """
        Get attributes from group.

        *Parameters*
        - `cn`:  cn of group, which attributes you want to know. String.
        - `basedn`: context in which you want look for the group. String.
        By default equal to basedn which was provided to 'Ldap Client Connect'.

        *Return*
        Dictionary, keys of which represent attributes name and values of this
        dictionary contains value of attributes. Example of returning value:
        \n
        {'objectClass': ['posixGroup'], 'memberUid': ["'he, she, it'"],
        'gidNumber': ['9090'], 'cn': ['delete_me']}

        *Exceptions*
            None.

        *Example*
        | ${out} | Ldap Client Get Group | group_name |
        | ${out} | Ldap Client Get Group | group_name |
        | ... | ou=people,dc=cisco,dc=com |
        """
        result = self._cache.current.get_group(cn, basedn)
        if result:
            return result[0][1]
        else:
            return None

    def ldap_client_get_user(self, uid, basedn=None):
        """
        Get attributes from user's object.

        *Parameters*
        - `cn`:  cn of user, which attributes you want to know. String.
        - `basedn`: context in which you want look for the user. String.
        By default equal to basedn which was provided to 'Ldap Client Connect'.

        *Return*
        Dictionary, keys of which represent attributes name and values of this
        dictionary contains value of attributes. Example of returning value:
        \n
        {'uid': ['vpyvovar'], 'objectClass': ['person', 'account',
        'inetorgperson', 'mailrecipient', 'inetlocalmailrecipient',
        'posixAccount'], 'mailLocalAddress': ['local_mail1@mail.qa'],
        'uidNumber': ['1'], 'mailAlternateAddress': ['alt_mail@mail.qa'],
        'gidNumber': ['1'], 'mailHost': ['mail.qa'], 'mailRoutingAddress':
        ['mail.qa'], 'sn': ['v.pyvovar'], 'homeDirectory': ['/home/vpyvovar'],
        'mail': ['vpyvovar@mail.qa'], 'userPassword': ['password1'], 'cn':
        ['vpyvovar']}

        *Exceptions*
            None.

        *Example*
        | ${out} | Ldap Client Get Group | user |
        | ${out} | Ldap Client Get Group | user |
        | ... | ou=people,dc=cisco,dc=com |
        """
        result = self._cache.current.get_user(uid, basedn)
        if result:
            return result[0][1]
        else:
            return None

    def ldap_client_create_user(self, *args):
        """
        Create user in ldap if it not present. If such user excist, it will be
        modified accourding to provided parameter.

        *Parameters*
         - `uid`: uid for user. String.
         - `password`: password for account. String.
         - `mail`: email address for user. String.
         - `mail_alternate_address`: value for 'mailAlternateAddress' ldap
           attribute. String. By default left empty.
         - `mail_local_address`: value for 'mailLocalAddress' ldap attribute.
           String. By default left empty.
         - `mail_routing_address`: value for 'mailRoutingAddress' ldap
           attribute. String. By default left empty.
         - `posixAccount`: Add 'posixAccout' class to this object. Boolean. By
           default ${False}.
         - `uidNumber`: value for 'uidNumber' ldap attribute. Can be provided
           only if you make this object will belong to 'posixAccount' class. By
           default autogenerate.
         - `gidNumber`: value for 'gidNumber' ldap attribute. Can be provided
           only if you make this object will belong to 'posixAccount' class. By
           default autogenerate.
         - `homeDirectory`: value for 'homeDirectory' ldap attribute.
           Can be provided only if you make this object will belong to
           'posixAccount' class. By default '/homedir/uid_of_object'.
         - `basedn`: context in which you want create user. String. By default
           equal to basedn which was provided to 'Ldap Client Connect'.
         - `use_mod_add_for`: Comma-separated string of ldap attributes which will
           be added to excisting values instead of replasing it.

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Client Create User |  uid=vpyvovar | password=password1 |
        | ... | mail=vpyvovar@mail.qa |
        | ... | mail_alternate_address=alt_mail@mail.qa |
        | ... | mail_local_address=local_mail1@mail.qa |
        | ... | mail_routing_address=mail.qa | posixAccount=${False} |
        | Ldap Client Create User |  uid=delete_me | password=any_word |
        | ... | mail=delete_me@mail.qa |
        | ... | mail_alternate_address=alt_mail@mail.qa |
        | ... | posixAccount=${True} | use_mod_add_for= mail |
        """
        kwargs = self._parse_args(args)
        if kwargs.get("posixAccount", None):
            if kwargs.get('posixAccount') == "False":
                del kwargs['posixAccount']
        print "kwargs= %s" % kwargs
        self._cache.current.create_user(**kwargs)

    def ldap_client_create_group(self, cn, gid=None, members=None, basedn=None):
        """
        Create group in ldap if it not present. If such group excist, it will be
        modified accourding to provided parameter.

        *Parameters*
        - `cn`: value for 'cn' ldap attribute. String.
        - `gid`: value for 'gid' ldap attribute. String. By default will be
          generated automaticaly.
        - `members`: ldap user which you want to associate with group. String.By
          default empty.
        - `basedn`: context in which you want create group. String. By default
           equal to basedn which was provided to 'Ldap Client Connect'.

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Client Create Group | delete_me | gid=8925 | members=me, you, they |
        | Ldap Client Create Group | delete_me |
        """
        self._cache.current.create_group(cn, gid,
                                         rf_value_to_ldap_mod_value(members),
                                         basedn)
