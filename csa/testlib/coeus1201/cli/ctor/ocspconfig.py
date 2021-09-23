#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/ocspconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
import os
import re
import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
                IafCliError, IafIpHostnameError, IafUnknownOptionError, \
                process_cli, REQUIRED, DEFAULT
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class ocspconfig(clictorbase.IafCliConfiguratorBase):

    """Configures OCSP((Online Certificate Status Protocol) Settings
    cli -> ocspconfig

    Configures  OCSP CLI options.

    """
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._restart()
        self._writeln('ocspconfig')
        return self

    def enable(self, input_dict=None, **kwargs):
        """Enables OCSP with default options"""
        self._query_response('SETUP')
        param_map = clictorbase.IafCliParamMap(\
                    end_of_command='Choose the operation')
        param_map['Enable_OCSP'] = ['enable OCSP?', YES]
        param_map['OCSP_ValidCacheTimeout'] = \
        ['OCSP valid response cache timeout', DEFAULT]
        param_map['OCSP_InvalidCacheTimeout'] = \
        ['OCSP invalid response cache timeout', DEFAULT]
        param_map['OCSP_NetworkErrorCacheTimeout'] = \
        ['network error cache timeout', DEFAULT]
        param_map['OCSP_ClockSkew'] = \
        ['allowed clock skew between the OCSP responder and the WSA', DEFAULT]
        param_map['OCSP_MaxTimeForOCSPResponse'] = \
        ['maximum time for the WSA to wait for an OCSP response', DEFAULT]
        param_map['OCSP_UpstreamProxy'] = \
        ['Do you want to use an upstream proxy for OCSP checking', DEFAULT]
        param_map['OCSP_cryptnonce'] = \
        ['nonce to cryptographically bind OCSP requests and responses','NO']
        if kwargs['OCSP_UpstreamProxy'].lower() == 'y' \
                              or kwargs['OCSP_UpstreamProxy'].lower() == 'yes':
            param_map['OCSP_UpstreamProxySelect'] = \
            ['Select an upstream proxy group for OCSP checking', '1']
            param_map['OCSP_ServerExempt'] = \
            ['Do you want to configure servers exempt from upstream proxy', \
             DEFAULT]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def _processwithserverExemption(self, input_dict=None, **kwargs):
        """Deals with NEW/DELETE/CLEAR Exemption Servers OCSP CLI options"""
        self._query_response('SETUP')
        self._query_response('YES')
        self._query_response(kwargs['OCSP_ValidCacheTimeout'])
        self._query_response(kwargs['OCSP_InvalidCacheTimeout'])
        self._query_response(kwargs['OCSP_NetworkErrorCacheTimeout'])
        self._query_response(kwargs['OCSP_ClockSkew'])
        self._query_response(kwargs['OCSP_MaxTimeForOCSPResponse'])
        self._query_response(kwargs['OCSP_cryptnonce'])
        self._query_response('Y')
        if kwargs['OCSP_UpstreamProxySelect']:
            self._query_select_list_item(kwargs['OCSP_UpstreamProxySelect'])
        else:
            self._query_response('1')
        self._query_response('Y')
        if kwargs['OCSP_ServerExemptACTION'] == 'CLEAR':
            self._query_response('CLEAR')
        if kwargs['OCSP_ServerExemptACTION'] == 'NEW':
            self._query_response('NEW')
            self._query_response(kwargs['OCSP_ServerExemptList'])
        if kwargs['OCSP_ServerExemptACTION'] == 'DELETE':
            self._query_response('DELETE')
            self._query_select_list_item(kwargs['OCSP_ServerExemptList'])
        return

    def disable(self, input_dict=None, **kwargs):
        """Disables OCSP through CLI"""
        self._query_response('SETUP')
        self._query_response('N')
        self._query_response('')
        return
