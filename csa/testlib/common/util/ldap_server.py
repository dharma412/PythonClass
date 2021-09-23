#!/usr/bin/env python

# $Id: //prod/main/sarf_centos/testlib/common/util/ldap_server.py#1 $ $DataTime:$ $Author: aminath $
from common.util.utilcommon import UtilCommon

import sal.servers.ldap as ldap


class LdapServer(UtilCommon):
    """
    Keywords for working with openldap deamon.
    """

    def get_keyword_names(self):
        return [
            'ldap_server_start',
            'ldap_server_stop',
            'ldap_server_restart',
            'ldap_server_set_ldap_options',
        ]

    def ldap_server_start(self, hostname,
                          deamon_script='/usr/local/etc/rc.d/slapd'):
        """
        Start ldap daemon.

        *Parameters*
        - `hostname`: host  on which you want to start ldap server. String.
        - `deamon_script`: fullpath to deamon script. String. Default is
          '/usr/local/etc/rc.d/slapd'

        *Return*
            None.

        *Exceptions*
           Warning if ldap deamon already runing.

        *Examples*
        | Ldap Server Start | sma19.sma |
        | Ldap Server Start | sma19.sma | /etc/rc.d/slapd |
        """
        if not (ldap.OpenLdapServer(hostname, deamon_script).start()):
            self._warn("LDAP server already running.")

    def ldap_server_stop(self, hostname,
                         deamon_script='/usr/local/etc/rc.d/slapd'):
        """
        Stop ldap daemon.

        *Parameters*
        - `hostname`:  host  on which you want to stop ldap server. String.
        - `deamon_script`: fullpath to deamon script. String. Default is
          '/usr/local/etc/rc.d/slapd'

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Server Stop | sma19.sma |
        | Ldap Server Stop | sma19.sma | /etc/rc.d/slapd |
        """
        ldap.OpenLdapServer(hostname, deamon_script).stop()

    def ldap_server_restart(self, hostname,
                            deamon_script='/usr/local/etc/rc.d/slapd'):
        """
         Restart ldap daemon.

        *Parameters*
        - `hostname`:  host  on which you want to restart ldap server. String.
        - `deamon_script`: fullpath to deamon script. String. Default is
          '/usr/local/etc/rc.d/slapd'

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Server Restart | sma19.sma |
        | Ldap Server Restart | sma19.sma | /etc/rc.d/slapd |
        """
        ldap.OpenLdapServer(hostname, deamon_script).restart()

    def ldap_server_set_ldap_options(self, hostname,
                                     deamon_script='/usr/local/etc/rc.d/slapd', ldap_enable=None,
                                     ldaps_enable=None, tls_enable=None, anon_enable=None,
                                     ldap_address=None, ldaps_address=None, ldap_port=None,
                                     ldaps_port=None, save_old_local=None):
        """
         Change ldap server options.
         Options such as secure/non-secure, address, and port must be set
         in the flags passed to slapd at startup.  So we create an
         rc.conf.local file with just the slapd_flags variable included
         and copy it over to /etc on the ldap server after saving whatever
         rc.conf.local file is there already.

        *Parameters*
        - `hostname`:  host on which you want to restart ldap server. String.
        - `ldap_enable`: enable ldap protocol. Boolean. Default  ${True}
        - `ldaps_enable`: enable secure ldap protocol. Boolean. Default ${False}
        - `tsl_enable`:
        - `anon_enable`: add anonymous access to ldap. Boolean. Default
          ${False}.
        - `ldap_address`: network interface on which ldap server will listen.
        - `ldaps_addres`: network interface on which secure ldap will listen.
        - `ldap_port`: port on which ldap server will listen. String.
          Default 389.
        - `ldaps_port`: port on which secure ldap will listen. String.
          Default 636.
        - `save_old_local`: save old /etc/rc.conf.local config to local /tmp
          dir. Boolean. Default ${False}
        - `deamon_script`: fullpath to deamon script. String. Default is
          '/usr/local/etc/rc.d/slapd'

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Ldap Server Set Ldap Options | ldap_port=600 | save_old_local=${True} |
        | Ldap Server Set Ldap Options | tls_enable=${True} |
        """
        ldap.OpenLdapServer(hostname, deamon_script).set_ldap_options(ldap_enable,
                                                                      ldaps_enable, tls_enable, anon_enable,
                                                                      ldap_address,
                                                                      ldaps_address, ldap_port, ldaps_port,
                                                                      save_old_local)
