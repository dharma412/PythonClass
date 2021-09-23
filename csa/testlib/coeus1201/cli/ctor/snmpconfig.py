#! /usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/snmpconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
    IAF 2 CLI ctor - snmpconfig
"""
# TODO: add ability to verify paramaters against xml settings file
# TODO: create a parameter class to place in param_map, move functionality there

import os
import re
import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
                IafCliError, IafIpHostnameError, IafUnknownOptionError, \
                process_cli, REQUIRED, DEFAULT
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO

DEBUG = True


class snmpconfig(clictorbase.IafCliConfiguratorBase):
    """
    snmpconfig
    """
    # Give the top level command name for this class, required
    _top_level_command = 'snmpconfig'

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('The SNMPv3 password must be at least', EXACT) : ValueError,
            ('A port must be a number', EXACT): ValueError,
            ('The trap target must be host name', EXACT): ValueError,
        })

    def __call__(self):
        self.clearbuf()
        self._writeln('snmpconfig')
        return self

    def setup(self, input_dict=None, **kwargs):
        """
        Sole configuration method.
        """
        self._query_response('setup')
        param_map = \
            clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['enable_snmp'] = ['enable SNMP?', DEFAULT]
        param_map['ip_interface'] = \
            ['Please choose an IP interface', DEFAULT, True]
        param_map['snmp_port'] = \
            ['Which port shall the SNMP daemon listen on', DEFAULT]
        param_map['snmpv3_auth'] = ['SNMPv3 authentication type', DEFAULT, True]
        param_map['snmpv3_prot'] = ['SNMPv3 privacy protocol', DEFAULT, True]
        param_map['snmpv3_passphrase'] = \
            ['Enter the SNMPv3 authentication passphrase', DEFAULT]
        param_map['snmpv3_passphrase_again'] = \
            ['enter the SNMPv3 authentication passphrase again to', DEFAULT]
        param_map['snmpv3_privacy_passphrase'] = \
            ['Enter the SNMPv3 privacy passphrase', DEFAULT]
        param_map['snmpv3_privacy_passphrase_again'] = \
            ['enter the SNMPv3 privacy passphrase again', DEFAULT]
        param_map['snmpv3_set_other_passwords'] = \
            ['Do you want to set other passwords', DEFAULT]
        param_map['snmpv3_passphrase_diff_pass'] = \
            ['Enter the SNMPv3 authentication passphrase', DEFAULT]
        param_map['snmpv3_passphrase_again_diff_pass'] = \
            ['enter the SNMPv3 authentication passphrase again to', DEFAULT]
        param_map['snmpv3_privacy_passphrase_diff_pass'] = \
            ['Enter the SNMPv3 privacy passphrase', DEFAULT]
        param_map['snmpv3_privacy_passphrase_again_diff_pass'] = \
            ['enter the SNMPv3 privacy passphrase again', DEFAULT]
        """
        param_map['snmpv3_passphrase'] = \
            ['SNMPv3 authentication passphrase', [DEFAULT, DEFAULT]]
        param_map['snmpv3_privacy_passphrase'] = \
            ['SNMPv3 privacy passphrase', [DEFAULT, DEFAULT]]
        """
        param_map['snmpv1v2_enabled'] = \
            ['Service SNMP V1/V2c requests?', DEFAULT]
        param_map['snmpv1v2_community'] = \
            ['Enter the SNMP V1/V2c community string.', DEFAULT]
        param_map['snmpv1v2_permit_via_ipv4'] = \
            ['Shall SNMP V2c requests be serviced from IPv4 addresses',
             DEFAULT]
        param_map['snmpv1v2_network'] = \
            ['From which IPv4 networks shall SNMP V1/V2c requests be allowed',
             DEFAULT]
        param_map['snmpv1v2_permit_via_ipv6'] = \
            ['Shall SNMP V2c requests be serviced from IPv6 addresses',
             DEFAULT]
        param_map['snmpv1v2_ipv6_network'] = \
            ['From which IPv6 networks shall SNMP V1/V2c requests be allowed',
             DEFAULT]
        param_map['trap_target'] = ['Enter the Trap target', DEFAULT]
        param_map['trap_community'] = ['Trap Community string.', DEFAULT]
        param_map['change_trap_status'] = ['Enterprise Trap Status',
            [DEFAULT, DEFAULT]]
        # Would be nice if the next two could be combined
        param_map['disable_traps'] = ['Do you want to disable', DEFAULT]
        param_map['traps_to_disable'] = \
            ['Enter number or numbers of traps to disable', DEFAULT]
            #This might hang
        param_map['enable_traps'] = ['Do you want to enable', DEFAULT]
        param_map['traps_to_enable'] = \
            ['Enter number or numbers of traps to enable', DEFAULT]
            #This might hang
        param_map['system_location_string'] = \
            ['System Location string', DEFAULT]
        param_map['system_contact_string'] = \
            ['System Contact string', DEFAULT]
        param_map['cpu_util_threshold'] = \
            ['threshold would you like to set for CPU utilization', DEFAULT]
        param_map['conn_fail_url'] = \
            ['URL to check for connectivity failure', DEFAULT]
        param_map['mem_util_threshold'] = \
            ['threshold would you like to set for memory utilization', DEFAULT]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map, timeout=5)

    def is_snmp_enabled(self):
        self._to_the_top(1)
        cli_buf = self.getbuf()

        if re.search('SNMP.*?Enabled', cli_buf):
            return True
        elif re.search('SNMP.*?Disabled', cli_buf):
            return False
        else:
            raise IafCliError, 'Failed to retrieve SNMP status via CLI'

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    sc = snmpconfig(cli_sess)

    sc().setup()
    sc().setup(input_dict={'enable_snmp':'Y',
                           'ip_interface':'Management',
                           'snmpv3_passphrase':['ironport', 'ironport'],
                           'snmp_port':'161',
                           'snmpv3_set_other_passwords':'N',
                           'snmpv1v2_enabled':'Y',
                           'snmpv1v2_community':'ironport',
                           'snmpv1v2_network':'172.0.0.0/8',
                           'trap_target':'127.0.0.1',
                           'trap_community':'ironport',
                           'change_trap_status':'N',
                           'system_location_string':'unknown',
                           'system_contact_string':'snmp@localhost'})
