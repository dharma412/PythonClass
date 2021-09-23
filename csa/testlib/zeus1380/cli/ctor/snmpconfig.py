#! /usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/snmpconfig.py#1 $

"""
    IAF 2 CLI ctor - snmpconfig
"""

import re
import clictorbase
from clictorbase import IafCliError, REQUIRED, DEFAULT
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO


class snmpconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('The SNMPv3 password must be at least', EXACT) : ValueError,
            ('A port must be a number', EXACT): ValueError,
            ('The trap target must be host name', EXACT): ValueError,
        })

    def __call__(self):
        self._restart()
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['enable_snmp'] = ['enable SNMP?', DEFAULT]
        param_map['ip_interface'] = ['Please choose an IP interface for SNMP requests.', DEFAULT, True]
        param_map['snmpv3_passphrase'] = ['SNMPv3 authentication passphrase', [REQUIRED, REQUIRED]]
        param_map['snmp_port'] = ['Which port shall the SNMP daemon listen on', DEFAULT]
        param_map['ipv4_addresses'] = ['requests be serviced from IPv4 addresses', DEFAULT]
        param_map['snmpv1v2_enabled'] = ['Service SNMP V1/V2c requests?', DEFAULT]
        param_map['snmpv1v2_community'] = ['Enter the SNMP V1/V2c community string.', DEFAULT]
        param_map['snmpv1v2_network'] = ['networks shall SNMP V1/V2c requests be allowed?', DEFAULT]
        param_map['trap_target'] = ['Enter the Trap target', DEFAULT]
        param_map['trap_community'] = ['Trap Community string.', DEFAULT]
        param_map['change_trap_status'] = ['you want to change any of these', DEFAULT]
        param_map['disable_traps'] = ['Do you want to disable any of these traps?', DEFAULT]
        param_map['traps_to_disable'] = ['Enter number or numbers of traps to disable', DEFAULT] #This might hang
        param_map['enable_traps'] = ['Do you want to enable any of these traps?', DEFAULT]
        param_map['traps_to_enable'] = ['Enter number or numbers of traps to enable', DEFAULT] #This might hang
        param_map['system_location_string'] = ['System Location string', DEFAULT]
        param_map['system_contact_string'] = ['System Contact string', DEFAULT]
        param_map['cpu_util_threshold'] = ['threshold would you like to set for CPU utilization', DEFAULT]
        param_map['snmpv3_auth_type'] = ['SNMPv3 authentication type', [DEFAULT]]
        param_map['snmpv3_privacy_proto'] = ['SNMPv3 privacy protocol', [DEFAULT]]
        param_map['snmpv3_privacy_passwd'] = ['SNMPv3 privacy passphrase', [REQUIRED, REQUIRED]]

        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')

        return self._process_input(param_map)

    def is_snmp_enabled(self):
        self.clearbuf()
        self._to_the_top(1)
        cli_buf = self.getbuf()

        if re.search('SNMP.*?Enabled', cli_buf):
            return True
        elif re.search('SNMP Disabled', cli_buf):
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
    sc().setup(input_dict={'enable_snmp': YES,
                           'snmpv3_passphrase': ['ironport', 'ironport']})
    sc().setup(input_dict={'enable_snmp': YES,
                           'snmpv3_passphrase': ['ironport', 'ironport'],
                           'snmp_port': '161', 'snmpv1v2_enabled': YES,
                           'snmpv1v2_community': 'ironport',
                           'change_trap_status': [YES, NO], 'disable_traps': YES,
                           'traps_to_disable': '6, 7', 'enable_traps': YES,
                           'traps_to_enable': '1, 4, 9',
                           'system_location_string': 'system loc string',
                           'system_contact_string': 'test@localhost',
                           'cpu_util_threshold': '95',})
    sc().setup(input_dict={'enable_snmp': NO})
