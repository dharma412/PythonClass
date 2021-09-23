#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/applianceconfig.py#1 $
# $DateTime: 2020/05/25 00:19:30 $
# $Author: sarukakk $

"""
SARF CLI command: applianceconfig
"""

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliError, \
                                     IafCliConfiguratorBase
from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class applianceconfig(clictorbase.IafCliConfiguratorBase):

    class DuplicateIPError(IafCliError): pass
    class DuplicateNameError(IafCliError): pass
    class InvalidNameError(IafCliError): pass
    class NoSuchHostError(IafCliError): pass
    class ReportingLimitError(IafCliError): pass
    class TrackingLimitError(IafCliError): pass
    class AuthError(IafCliError): pass
    class RemoteConnectionError(IafCliError): pass
    class VersionMismatchError(IafCliError): pass
    class ConfigurationMasterDisabledError(IafCliError): pass

    CONNECT_TIMEOUT = 120

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('IP .+ already exists', REGEX) : self.DuplicateIPError,
            ('The name .+ is already in use', REGEX) : self.DuplicateNameError,
            ('IP .+ does not exist', REGEX) : self.NoSuchHostError,
            ('reporting \(.+\) has already been reached',
             REGEX) : self.ReportingLimitError,
            ('tracking \(.+\) has already been reached',
             REGEX) : self.TrackingLimitError,
            ('Authentication to .+ failed', REGEX) : self.AuthError,
            ('Error while trying to connect',
             EXACT) : self.RemoteConnectionError,
            ('version and release number must be exactly the same',
             EXACT) : self.VersionMismatchError,
            ('Please use 20 characters or less for the appliance name',
             EXACT): self.InvalidNameError,
            ('Appliance is only compatible with configuration masters which '\
                    'are\r\ndisabled',
             EXACT): self.ConfigurationMasterDisabledError,
            })

    level = 1

    def __call__(self, batch_cmd=None):
        self.clearbuf()
        # hack for appliance list batch command
        if batch_cmd:
            self._writeln('applianceconfig ' + batch_cmd)
            return self._read_until(timeout=self.CONNECT_TIMEOUT) # read until prompt

        # non-batch commands
        self._restart()
        self._writeln('applianceconfig')
        return self

    def add(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
                         end_of_command='Choose the operation')
        param_map['ip_addr'] = ['appliance to transfer data with', REQUIRED]
        param_map['name'] = ['identify this appliance', REQUIRED]
        param_map['ssh_transfer'] = ['transfer access for this appliance',
                                     DEFAULT]
        param_map['cust_ssh_port'] = ['use a custom ssh port to connect',
                                      DEFAULT]
        param_map['ssh_port'] = ['Port:', DEFAULT]
        param_map['username'] = ['Username:', DEFAULT]
        param_map['password'] = ['Password:', DEFAULT]
        param_map['type']     = ['enter the type of', DEFAULT, True]

        param_map.update(input_dict or kwargs)

        self._query_response('ADD')
        self._process_input(param_map, timeout=self.CONNECT_TIMEOUT)

    def edit(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
                         end_of_command='Choose the operation')
        param_map['edit_name'] = ['appliance you wish to edit', REQUIRED]
        param_map['ip_addr'] = ['appliance to transfer data with', DEFAULT]
        param_map['name'] = ['identify this appliance', DEFAULT]
        param_map['ssh_transfer'] = ['transfer access for this appliance',
                                     DEFAULT]
        param_map['cust_ssh_port'] = ['use a custom ssh port to connect',
                                      DEFAULT]
        param_map['ssh_port'] = ['Port:', DEFAULT]
        param_map['username'] = ['Username:', REQUIRED]
        param_map['password'] = ['Password:', REQUIRED]
        param_map['type']     = ['enter the type of', DEFAULT, True]

        param_map.update(input_dict or kwargs)

        self._query_response('EDIT')
        self._process_input(param_map, timeout=self.CONNECT_TIMEOUT)

    def delete(self, name_num):
        self._query_response('DELETE')
        self._query_response(name_num)
        self._to_the_top(self.level)

    def test(self, name_num):
        self._query_response('TEST')
        self._query_response(name_num)
        result = self._read_until('Choose the operation', timeout=self.CONNECT_TIMEOUT)
        self._to_the_top(self.level)
        return result

    def services(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Enter the ')
        param_map['name_num'] = ['name or number of the appliance', REQUIRED]
        param_map['email_quarantine'] = ['Centralized Policy Quarantine to be', DEFAULT]
        param_map['email_slbl'] = ['Safelist/Blocklist to be', DEFAULT]
        param_map['email_reporting'] = ['Email Reporting to be', DEFAULT]
        param_map['email_tracking'] = ['Tracking to be', DEFAULT]
        param_map['web_config_mgr'] = \
            ['Centralized Configuration Manager to be enabled', DEFAULT]
        param_map['web_reporting'] = \
            ['Centralized Web Reporting to be enabled', DEFAULT]
        param_map['assign_master'] = \
            ['assign this appliance to a configuration master', DEFAULT]
        param_map['cm_version'] = \
            ['Please choose a configuration master', DEFAULT, True]
        param_map.update(input_dict or kwargs)

        self._query_response('SERVICES')
        self._read_until('Enter the ')
        # Configuration Manager needs more than 75 s to timeout
        self._process_input(param_map, timeout=self.CONNECT_TIMEOUT)

    def status(self, *args, **kwargs):
        self._query_response('STATUS')
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw

    def port(self, port):
        self._query_response('PORT')
        self._query_response(port)
        self._to_the_top(self.level)
