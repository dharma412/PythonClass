#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/interfaceconfig.py#1 $

"""
    IAF 2 CLI ctor - interfaceconfig
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
                IafCliError, IafIpHostnameError, IafUnknownOptionError, \
                REQUIRED, DEFAULT, NO_DEFAULT
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class interfaceconfig(clictorbase.IafCliConfiguratorBase):
    """interfaceconfig
        - will return -1 when there's no Sophos feature key
    """
    class MaxInterfacesReachedError(IafCliError): pass
    class InterfaceConflictError(IafCliError): pass
    class SubnetError(IafIpHostnameError): pass
    class PortAlreadyAssignedError(IafCliError): pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('You are only allowed to configure a maximum of \d+ interfaces',
                                       REGEX): self.MaxInterfacesReachedError,
             ('Error: the settings you chose conflict with the interface \S+',
                                       EXACT): self.InterfaceConflictError,
             ('IPs on the same subnet cannot be on different interfaces',
                                       EXACT): self.SubnetError,
             ('Port \d+ is currently assigned to \S+ Would you like to remove',
                                       REGEX) : self.PortAlreadyAssignedError,
             })

    def __call__(self):
        self._writeln('interfaceconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['if_name']        = ['enter a name', REQUIRED]
        param_map['address']        = ['IP Address (Ex:', REQUIRED]
        param_map['ethernet']       = ['Ethernet interface:', DEFAULT, 1]
        param_map['netmask']        = ['Netmask (Ex:', DEFAULT]
        param_map['hostname']       = ['Hostname:', REQUIRED]
        param_map['FTP']            = ['enable FTP', DEFAULT]
        param_map['FTP_port']       = ['use for FTP', DEFAULT]
        param_map['Telnet']         = ['enable Telnet', DEFAULT]
        param_map['Telnet_port']    = ['use for Telnet', DEFAULT]
        param_map['SSH']            = ['enable SSH', DEFAULT]
        param_map['SSH_port']       = ['use for SSH', DEFAULT]
        param_map['ccs']            = ['enable Cluster', DEFAULT]
        param_map['ccs_port']       = ['use for Cluster', DEFAULT]
        param_map['HTTP']           = ['enable HTTP', DEFAULT]
        param_map['HTTP_port']      = ['use for HTTP?', DEFAULT]
        param_map['HTTPS']          = ['enable HTTPS', DEFAULT]
        param_map['HTTPS_port']     = ['use for HTTPS', DEFAULT]
        param_map['EUQ_HTTP']       = ['enable Spam Quarantine HTTP',
                                        DEFAULT]
        param_map['EUQ_HTTP_port']  = ['use for Spam Quarantine HTTP?',
                                        DEFAULT]
        param_map['EUQ_HTTPS']      = ['enable Spam Quarantine HTTPS',
                                        DEFAULT]
        param_map['EUQ_HTTPS_port'] = ['use for Spam Quarantine HTTPS?',
                                        DEFAULT]
        param_map['use_demo_cert']  = ['use a demo certificate', DEFAULT]
        param_map['HTTP_redirect']  = ['should HTTP requests redirect', DEFAULT]
        param_map['EUQ_redirect']   = ['Spam Quarantine HTTP '\
                                       'requests redirect', DEFAULT]
        param_map['use_def_ipas']   = ['default interface for your Spam Quarantine',
                                        DEFAULT]
        param_map['use_custom_url'] = ['custom base URL in your Spam Quarantine',
                                            DEFAULT]
        param_map['custom_url'] = ['Enter the custom base URL',
                                        NO_DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, if_name, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['new_name']       = ['IP interface name', DEFAULT]
        param_map['address']        = ['IP Address (Ex:', DEFAULT]
        param_map['ethernet']       = ['Ethernet interface:', DEFAULT, 1]
        param_map['netmask']        = ['Netmask (Ex:', DEFAULT]
        param_map['hostname']       = ['Hostname:', DEFAULT]
        param_map['FTP']            = ['enable FTP', DEFAULT]
        param_map['FTP_port']       = ['use for FTP', DEFAULT]
        #param_map['Telnet']         = ['enable Telnet', DEFAULT]
        #param_map['Telnet_port']    = ['use for Telnet', DEFAULT]
        param_map['SSH']            = ['enable SSH', DEFAULT]
        param_map['SSH_port']       = ['use for SSH', DEFAULT]
        #param_map['ccs']            = ['enable Cluster', DEFAULT]
        #param_map['ccs_port']       = ['use for Cluster', DEFAULT]
        param_map['HTTP']           = ['enable HTTP', DEFAULT]
        param_map['HTTP_port']      = ['use for HTTP?', DEFAULT]
        param_map['HTTPS']          = ['enable HTTPS', DEFAULT]
        param_map['HTTPS_port']     = ['use for HTTPS', DEFAULT]
        param_map['EUQ_HTTP']       = ['enable Spam Quarantine HTTP',
                                        DEFAULT]
        param_map['EUQ_HTTP_port']  = ['use for Spam Quarantine HTTP?',
                                        DEFAULT]
        param_map['EUQ_HTTPS']      = ['enable Spam Quarantine HTTPS',
                                        DEFAULT]
        param_map['EUQ_HTTPS_port'] = ['use for Spam Quarantine HTTPS?',
                                        DEFAULT]
        param_map['use_demo_cert']  = ['use a demo certificate', DEFAULT]
        param_map['HTTP_redirect']  = ['HTTP requests redirect', DEFAULT]
        param_map['EUQ_redirect']   = ['Spam Quarantine HTTP '\
                                       'requests redirect', DEFAULT]
        param_map['use_def_ipas']   = ['default interface for your Spam Quarantine',
                                        DEFAULT]
        param_map['use_custom_url'] = ['custom base URL in your Spam Quarantine',
                                            DEFAULT]
        param_map['custom_url'] = ['Enter the custom base URL', DEFAULT]
        param_map['change_confirm'] = ['want to change it?', DEFAULT]
        param_map['filter_confirm'] = ['one or more filters', DEFAULT]
        param_map['asyncos_confirm'] = ['enable AsyncOS API HTTP', DEFAULT]
        param_map['asyncos_port'] = ['use for AsyncOS API HTTP', DEFAULT]
        param_map['asyncos_https'] = ['enable AsyncOS API HTTPS', DEFAULT]
        param_map['asyncoshttps_port'] = ['use for AsyncOS API HTTPS', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_parse_input_list()
        self._writeln('EDIT')
        self._query()
        self._select_list_item(if_name)

        return self._process_input(param_map)

    def groups(self):
        self._query_response('GROUPS')
        return interfaceconfigGroups(self._get_sess())

    def delete(self, if_name, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['filter_confirm']  = \
                             ['is referenced by one or more filters.', DEFAULT]
        param_map['current_confirm'] = ['logged into', DEFAULT]
        param_map['group_confirm']   = ['one or more IP groups.', DEFAULT]
        param_map['omh_choice']      = ['used for outgoing mail', DEFAULT, 1]
        param_map['omh_new']         = ['to use for outgoing mail', DEFAULT, 1]
        param_map['altsrchost_choice']= \
                           ['used by one or more Virtual Gateways', DEFAULT, 1]
        param_map['altsrchost_new']  = ['for Virtual Gateway', DEFAULT, 1]
        param_map['dns_choice']      = ['used for DNS traffic', DEFAULT, 1]
        param_map['dns_new']         = ['to use for DNS traffic', DEFAULT, 1]
        param_map['SNMP_choice']     = ['used for the SNMP agent', DEFAULT, 1]
        param_map['SNMP_new']        = ['to use for SNMP', DEFAULT, 1]
        param_map['listener_choice'] = ['used by listener', DEFAULT, 1]
        param_map['listener_new']    = ['for listener', DEFAULT, 1]
        param_map['tcp_port']        = ['enter the TCP port', DEFAULT]
        param_map['NTP_choice']      = ['used for NTP queries', DEFAULT, 1]
        param_map['NTP_new']         = ['to use for NTP traffic', DEFAULT, 1]
        param_map['cluster_choice']=['used by one or more cluster', DEFAULT, 1]
        param_map['cluster_new']    = ['to use for the route from', DEFAULT, 1]
        param_map['upgrade_choice'] = ['used for upgrades', DEFAULT, 1]
        param_map['upgrade_new']    = ['to use for upgrades', DEFAULT, 1]
        param_map['smtpauth_choice']= ['used for an SMTP Auth', DEFAULT, 1]
        param_map['smtpauth_new']   = ['to use for this SMTP Auth', DEFAULT, 1]
        param_map.update(input_dict or kwargs)

        self._query_parse_input_list()
        self._writeln('DELETE')
        self._query()
        self._select_list_item(if_name)

        return self._process_input(param_map)

class interfaceconfigGroups(clictorbase.IafCliConfiguratorBase):
    """interfaceconfig -> Groups """

    class InterfaceGroupNameError(IafUnknownOptionError): pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
                ('Unknown group name', REGEX): self.InterfaceGroupNameError,
                ('Unknown group number', REGEX): self.InterfaceGroupNameError,
                })

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['group_name']     = ['Enter the name for', REQUIRED]
        param_map['if_list']        = ['Enter the name or number', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, group_name, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['new_name']       = ['Enter the name', DEFAULT]
        param_map['if_list']        = ['Choose the interfaces', DEFAULT]
        param_map['filter_confirm'] = ['one or more filters', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_parse_input_list()
        self._writeln('EDIT')
        self._query()
        self._select_list_item(group_name)
        return self._process_input(param_map)

    def delete(self, group_name, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['filter_confirm']  = \
                             ['is referenced by one or more filters.', DEFAULT]
        param_map['omh_choice']      = ['used for outgoing mail', DEFAULT, 1]
        param_map['omh_new']         = ['to use for outgoing mail', DEFAULT, 1]
        param_map['altsrchost_choice'] = \
                           ['used by one or more Virtual Gateways', DEFAULT, 1]
        param_map['altsrchost_new']    = ['for Virtual Gateway', DEFAULT, 1]
        param_map.update(input_dict or kwargs)

        self._query_parse_input_list()
        self._writeln('DELETE')
        self._query()
        self._select_list_item(group_name)
        return self._process_input(param_map)

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ic = interfaceconfig(cli_sess)
    print 'Test interfaceconfig new:'
    print ic().new(input_dict={'if_name':'new',
                               'address':'1.1.1.1',
                               'hostname':'qa.qa',
                               'EUQ_HTTP':'y',
                               'FTP':'y',
                               'FTP_port':'26', #avoid PortAlreadyAssignedError
                               'Telnet':'y',
                               'Telnet_port':'27', #avoid PortAlreadyAssignedError
                               'HTTPS':YES,
                               'HTTPS_port':444,
                               'EUQ_HTTPS':'y',
                               'EUQ_HTTPS_port':'123',
                               'EUQ_redirect':'N',
                               'use_def_ipas':'Y',
                               'use_custom_url':'Y',
                               'custom_url':'http://isq.example.url:81/',
                               # 'use_demo_cert':YES
                              })

    print 'Test interfaceconfig edit:'
    id = {'HTTPS':YES,
          'HTTPS_port':555,
          'use_demo_cert':YES,
            }
    ic().edit(if_name='new', input_dict=id)

    ic().delete('new')
    ic().groups().new(group_name='new')
    ic().groups().edit(group_name='new', new_name='monkey')
    ic().groups().delete(group_name='monkey')

