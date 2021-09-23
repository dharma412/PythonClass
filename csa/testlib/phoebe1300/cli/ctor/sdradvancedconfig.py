#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/sdradvancedconfig.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, IafCliParamMap


class sdradvancedconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self, input_dict=None, **kwargs):
        self._writeln('sdradvancedconfig')
        param_map = IafCliParamMap(end_of_command=self._get_prompt())

        param_map['sdr_lookup_timeout_value'] = ['Enter the Sender Domain Reputation query timeout', DEFAULT]
        param_map['sdr_service_hostname'] = ['Enter the hostname of the Sender Domain Reputation service', DEFAULT]
        param_map['sdr_verify_server_certificate'] = ['Do you want to verify server certificate', DEFAULT]
        param_map['sdr_rpc_log_level'] = ['Enter the default log level for RPC server', DEFAULT]
        param_map['sdr_http_client_log_level'] = ['Enter the default log level for HTTP Client', DEFAULT]
        param_map['sdr_match_exceptions_envelope_from_domain'] = [
            'Do you want exception list matches based on envelope-from domain', DEFAULT]

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def batch(self, **kwargs):
        allowed_params = ['timeout', 'host', 'verify_peer', 'debug_rpc_server', 'debug_http_client']
        for param in kwargs.keys():
            if param not in allowed_params:
                raise ValueError('Invalid param {invalid_param} passed. '
                                 'Allowed params are: {allowed_params}'.
                                 format(invalid_param=action, allowed_params=allowed_params))

        timeout = kwargs.get('timeout')
        host = kwargs.get('host')
        verify_peer = kwargs.get('verify_peer')
        debug_rpc_server = kwargs.get('debug_rpc_server')
        debug_http_client = kwargs.get('debug_http_client')

        cmd = 'sdradvancedconfig'
        if timeout is not None:
            cmd += ' timeout=%s' % timeout
        if host is not None:
            cmd += ' host=%s' % host
        if verify_peer is not None:
            cmd += ' verify_peer=%s' % verify_peer
        if debug_rpc_server is not None:
            cmd += ' debug_rpc_server=%s' % debug_rpc_server
        if debug_http_client is not None:
            cmd += ' debug_http_client=%s' % debug_http_client

        self._info('BATCH COMMAND: %s' % cmd)
        self._to_the_top(1)
        self.clearbuf()
        self._writeln(cmd)
        self._wait_for_prompt()
        self._info(self.getbuf())
