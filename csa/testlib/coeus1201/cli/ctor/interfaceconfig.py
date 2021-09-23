#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/interfaceconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
    IAF 2 CLI ctor - interfaceconfig
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
                IafCliError, IafIpHostnameError, IafUnknownOptionError, \
                REQUIRED, DEFAULT
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class interfaceconfig(clictorbase.IafCliConfiguratorBase):
    """interfaceconfig - Configure the interfaces
    """
    class MaxInterfacesReachedError(IafCliError): pass
    class InterfaceConflictError(IafCliError): pass
    class AlreadyInUseError(IafCliError): pass
    class InterfaceAlreadyConfiguredError(IafCliError): pass
    class SubnetError(IafIpHostnameError): pass
    class PortAlreadyAssignedError(IafCliError): pass
    class InvalidIPAddressError(IafCliError): pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('You are only allowed to configure a maximum of \d+ interfaces',
                                       REGEX): self.MaxInterfacesReachedError,
             ('Error: the settings you chose conflict with the interface \S+',
                                       REGEX): self.InterfaceConflictError,
             ('The value must not already be in use',
                                       EXACT): self.AlreadyInUseError,
             ('IPs on the same subnet cannot be on different interfaces',
                                       EXACT): self.SubnetError,
             ('Port \d+ is currently assigned to \S+ Would you like to remove',
                                       REGEX): self.PortAlreadyAssignedError,
             ('Already configured',    EXACT): self.InterfaceAlreadyConfiguredError,
             ('The IP address must be a valid',
                                       EXACT): self.InvalidIPAddressError,
             })

    def __call__(self):
        self.clearbuf()
        self._writeln('interfaceconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['configure_ipv4'] = ['configure an IPv4 address', DEFAULT]
        param_map['ipv4_address']   = ['IPv4 Address (Ex:', DEFAULT]
        param_map['netmask']        = ['Netmask (Ex:', DEFAULT]

        param_map['configure_ipv6'] = ['configure an IPv6 address', DEFAULT]
        param_map['ipv6_address']   = ['IPv6 Address (Ex:', DEFAULT]
        param_map['prefix_len']     = ['Prefix length (Ex:', DEFAULT]

        param_map['ethernet']       = ['Ethernet interface:', DEFAULT, 1]
        param_map['hostname']       = ['Hostname:', REQUIRED]
        param_map['FTP']            = ['enable FTP', DEFAULT]
        param_map['FTP_port']       = ['use for FTP', DEFAULT]
        param_map['SSH']            = ['enable SSH', DEFAULT]
        param_map['SSH_port']       = ['use for SSH', DEFAULT]
        param_map['HTTP']           = ['enable HTTP', DEFAULT]
        param_map['HTTP_port']      = ['use for HTTP?', DEFAULT]
        param_map['HTTPS']          = ['enable HTTPS', DEFAULT]
        param_map['HTTPS_port']     = ['use for HTTPS', DEFAULT]
        param_map['use_demo_cert']  = ['use a demo certificate', DEFAULT]
        param_map['HTTP_redirect']  = ['HTTP requests redirect', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, if_name, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['if_name']        = ['interface you wish to edit', REQUIRED]

        param_map['configure_ipv4'] = ['configure an IPv4 address', DEFAULT]
        param_map['ipv4_address']   = ['IPv4 Address (Ex:', DEFAULT]
        param_map['netmask']        = ['Netmask (Ex:', DEFAULT]

        param_map['configure_ipv6'] = ['configure an IPv6 address', DEFAULT]
        param_map['ipv6_address']   = ['IPv6 Address (Ex:', DEFAULT]
        param_map['prefix_len']     = ['Prefix length (Ex:', DEFAULT]

        param_map['hostname']       = ['Hostname:', DEFAULT]
        param_map['FTP']            = ['enable FTP', DEFAULT]
        param_map['FTP_port']       = ['use for FTP', DEFAULT]
        param_map['SSH']            = ['enable SSH', DEFAULT]
        param_map['SSH_port']       = ['use for SSH', DEFAULT]
        param_map['HTTP']           = ['enable HTTP', DEFAULT]
        param_map['HTTP_port']      = ['use for HTTP?', DEFAULT]
        param_map['HTTPS']          = ['enable HTTPS', DEFAULT]
        param_map['HTTPS_port']     = ['use for HTTPS', DEFAULT]
        param_map['use_demo_cert']  = ['use a demo certificate', DEFAULT]
        param_map['HTTP_redirect']  = ['HTTP requests redirect', DEFAULT]
        param_map['change_confirm'] = ['want to change it?', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_parse_input_list()
        self._writeln('EDIT')
        self._query()
        self._select_list_item(if_name)
        return self._process_input(param_map)

    def delete(self, if_name, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['current_confirm'] = ['logged into', DEFAULT]
        param_map['dns_choice']      = ['used for DNS traffic', DEFAULT, 1]
        param_map['dns_new']         = ['to use for DNS traffic', DEFAULT, 1]
        param_map['SNMP_choice']     = ['used for the SNMP agent', DEFAULT, 1]
        param_map['SNMP_new']        = ['to use for SNMP', DEFAULT, 1]
        param_map['NTP_choice']      = ['used for NTP queries', DEFAULT, 1]
        param_map['NTP_new']         = ['to use for NTP traffic', DEFAULT, 1]
        param_map['upgrade_choice'] = ['used for upgrades', DEFAULT, 1]
        param_map['upgrade_new']    = ['to use for upgrades', DEFAULT, 1]
        param_map['confirm'] = ['interface may hinder', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_parse_input_list()
        self._writeln('DELETE')
        self._query()
        self._select_list_item(if_name)
        return self._process_input(param_map)

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ic = interfaceconfig(cli_sess)
    ic().delete('1')
    ic().new(input_dict={'address':'1.1.2.2',
                         'ethernet':'Management',
                         'hostname':'foo.qa',
                         })
    ic().new(input_dict={'address':'1.1.1.2',
                         'ethernet':'P1',
                         'hostname':'test.qa',
                         })
    ic().edit(if_name='2', address='2.2.2.2')
    ic().delete('2')
