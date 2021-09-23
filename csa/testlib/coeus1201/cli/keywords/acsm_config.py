#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/acsm_config.py#1 $

from common.cli.clicommon import CliKeywordBase

class AcsmConfig(CliKeywordBase):
    """Configure settings for AnyConnect Secure Mobility."""

    def get_keyword_names(self):
        return [
            'acsm_ip_range_new',
            'acsm_ip_range_delete',
            'acsm_ip_range_edit',
            'acsm_asa_host_new',
            'acsm_asa_host_delete',
            'acsm_asa_host_edit',
            'acsm_asa_host_shared_secret',
            'acsm_disable',
            'acsm_edit',
        ]

    def acsm_ip_range_new(self, ip_range=''):

        """Enter an IP Range.
        musconfig > configure_ip > new

        Parameters:
        - `ip_range`: string with ip ranges value. The value can be one of the
            following examples: 10.1.1.0/24, 10.1.1.10, 10.1.1.1-10.

        Examples:
        | ACSM IP Range New | ip_range=10.1.1.0/24 |
        | ACSM IP Range New | ip_range=10.1.1.10 |
        | ACSM IP Range New | ip_range=10.1.1.1-10 |
        """
        self._cli.musconfig().new(item=ip_range, mode='ip')

    def acsm_ip_range_delete(self, ip_range=''):
        """Delete an IP Range.

        musconfig > configure_ip > delete

        Parameters:
        - 'ip_range': existing IP range to be deleted.
            Use 'all' to remove all configured IP ranges.

        Examples:
        | ACSM IP Range Delete | ip_range=10.1.1.10 |
        | ACSM IP Range Delete | ip_range=all |
        """
        self._cli.musconfig().delete(item=ip_range, mode='ip')

    def acsm_ip_range_edit(self, old_ip_range='', new_ip_range=''):

        """Edit an IP Range.
        musconfig > configure_ip > edit

        Parameters:
        - `old_ip_range`: existing IP range to be modified.
        - `new_ip_range`: new value for IP range.

        Examples:
        | ACSM IP Range Edit | old_ip_range=1.1.1.1 | new_ip_range=1.2.1.2 |
        """
        self._cli.musconfig().edit(item_old=old_ip_range,
                                            item_new=new_ip_range,
                                            mode='ip')

    def acsm_asa_host_new(self, asa_host='', asa_port=''):

        """Add an ASA server configuration.
        musconfig > configure_asa > new

        Parameters:
        - `asa_host`: host name or IP address of the ASA.
        - `asa_port`: port number of the ASA. Default is 11999.

        Examples:
        | ACSM ASA Host New | asa_host=asa_test.com | asa_port=10000 |
        """
        self._cli.musconfig().new(item=asa_host, port=asa_port, mode='asa')

    def acsm_asa_host_delete(self, asa_host=''):
        """Remove an ASA server configuration.
        musconfig > configure_asa > delete

        Parameters:
        - 'asa_host': existing ASA host to be deleted.
            Use 'all' to remove all configured IP ranges.

        Examples:
        | ACSM ASA Host Delete | asa_host=10.1.1.10 |
        | ACSM ASA Host Delete | asa_host=all |
        """
        self._cli.musconfig().delete(item=asa_host, mode='asa')

    def acsm_asa_host_edit(self, old_asa_host='', new_asa_host='', port=''):

        """Edit an IP Range.
        musconfig > configure_asa > edit

        Parameters:
        - `old_asa_host`: existing IP range to be modified.
        - `new_asa_host`: new value for IP range.
        - `port`: new value for ASA port selected to be modified.

        Examples:
        | ACSM ASA Host Edit | old_asa_host=1.1.1.1 | new_asa_host=1.2.1.2 | port=11111 |
        """
        self._cli.musconfig().edit(item_old=old_asa_host,
                                   item_new=new_asa_host,
                                   mode='asa')

    def acsm_asa_host_shared_secret(self, secret=''):

        """Configure shared secret for ASA-WSA communication.
        musconfig > configure_asa > shared_secret

        Parameters:
        - `secret`: shared secret for ASA-WSA communication.
            A valid ASA Access Password must contain 8-20 characters.

        Examples:
        | ACSM ASA Host Shared Secret | secret='ironport' |
        """
        self._cli.musconfig().shared_secret(secret)

    def acsm_disable(self):

        """Disable AnyConnect Secure Mobility.
        musconfig setup no

        Examples:
        | ACSM Disable |
        """
        self._cli.musconfig().disable()

    def acsm_edit(self, mode=''):

        """Enable or edit AnyConnect Secure Mobility.
        musconfig setup yes

        Parameters:
        - `mode`: set AnyConnect Secure Mobility to use IP ranges or Cisco ASA
            Integration. Either 'IP' or 'ASA'

        Examples:
        | ACSM Edit |
        | ACSM Edit | mode=IP |
        | ACSM Edit | mode=ASA |
        """
        self._cli.musconfig().enable(mode)

