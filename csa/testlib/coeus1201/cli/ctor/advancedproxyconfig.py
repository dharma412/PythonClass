#!/usr/bin/env python

# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/advancedproxyconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
    IAF 2 CLI ctor - advancedproxyconfig
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
                IafCliError, IafIpHostnameError, IafUnknownOptionError, \
                REQUIRED, DEFAULT
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class DuplicateEntry(IafCliError): pass
class UnknownOptionError(IafCliError): pass

class advancedproxyconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 2
    """advancedproxyconfig
        - will return -1 when there's no Sophos feature key
    """
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
         ('Unknown option', EXACT) : UnknownOptionError,
         ('The IP address must be 4 numbers', EXACT) : ValueError,
         ('Each number must be a value from', EXACT) : ValueError,
         ('The IP address cannot start with.', EXACT) : ValueError,
         ('Comma separated IP addresses.', EXACT) : ValueError,
         ('style must be either "fulluri" or "stripquery"', EXACT) : ValueError,
         ('Duplicate entries are not allowed.', EXACT): DuplicateEntry
         })

    def __call__(self):
        self._restart()
        self._writeln('advancedproxyconfig')
        return self

    def settracktime(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose a parameter')
        param_map['interval']    = ['interval in seconds between printing',
                                    DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('SETTRACKTIME')
        return self._process_input(param_map)

    def authentication(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose a parameter')
        param_map['forward_auth']   = ['forward authorization request',
                                       DEFAULT, 1]
        param_map['proxy_auth']     = ['the Proxy Authorization Realm', DEFAULT]
        param_map['log']            = ['to log the username', DEFAULT]
        param_map['use_group_attr'] = ['Group Membership attribute be used',
                                       DEFAULT]
        param_map['adv_ad']          = ['use advanced Active Directory',
                                        DEFAULT]
        param_map['case_insensitive'] = ['allow case insensitive username',
                                         DEFAULT]
        param_map['wild_card']      = ['allow wild card matching', DEFAULT]
        param_map['charset']        = ['charset used by the clients', DEFAULT]
        param_map['ldap_referrals'] = ['enable referrals for LDAP', DEFAULT]
        param_map['secure_auth']    = ['enable secure authentication', DEFAULT]
        param_map['redirect_port']  = ['redirect port for secure', DEFAULT]
        param_map['hostname']       = ['the hostname to redirect', DEFAULT]
        param_map['user_timeout']   = ['timeout for user credentials', DEFAULT]
        param_map['machine_timeout'] = ['timeout for machine credentials',
                                        DEFAULT]
        param_map['broken_auth_timeout'] = ['timeout in the case traffic permitted',
                                            DEFAULT]
        param_map['cache_timeout'] = ['user-ip mapping cache timeout in proxy', DEFAULT]
        param_map['thread_count'] = ['ISE DB thread count', DEFAULT]
        param_map['re_auth']        = ['re-auth on request', DEFAULT]
        param_map['send_negotiate'] = ['send Negotiate header', DEFAULT, 1]
        param_map['mapping_update'] = ['mapping update interval', DEFAULT]
        param_map['transparent_id'] = ['for transparent user identification',
                                       DEFAULT]
        param_map['masking']        = ['username and IP address masking',
                                       DEFAULT, 1]
        param_map.update(input_dict or kwargs)

        self._query_response('AUTHENTICATION')
        return self._process_input(param_map)

    def caching(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose a parameter')
        param_map['cache_option']        = ['configuring advanced caching '\
                                            'options', DEFAULT, 1]
        param_map['allow_hits']          = ['allow objects with a heurisitic '\
                                            'expiration', DEFAULT]
        param_map['allow_etag']          = ['allow ETAG mismatch', DEFAULT]
        param_map['allow_cache_request'] = ['caching when requests', DEFAULT]
        param_map['allow_cache_server']  = ['caching from servers', DEFAULT]
        param_map['max_age_with']        = ['maximum age to cache the document'\
                                            ' with', DEFAULT]
        param_map['max_age_without']     = ['maximum age to cache the document'\
                                            ' without', DEFAULT]
        param_map['age_error_cache']     = ['age to cache errors', DEFAULT]
        param_map['ignore_client']       = ['ignore client directive', DEFAULT]
        param_map['reload_interval']     = ['interval during which reload',
                                            DEFAULT]
        param_map['allow_convert']       = ['allow proxy to convert reload',
                                            DEFAULT]
        param_map['ims_request_time']    = ['explicit IMS Refresh request',
                                            DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('CACHING')
        return self._process_input(param_map)

    def dns(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose a parameter')
        param_map['sucess_time']        = ['time to cache successful DNS ' \
                                           'results ', DEFAULT]
        param_map['error_time']         = ['time to cache results of DNS ' \
                                           'errors ', DEFAULT]
        param_map['url_format']         = ['the URL format for the', DEFAULT]
        param_map['issue_redirect']     = ['proxy to issue a HTTP 307 ' \
                                           'redirection', DEFAULT]
        param_map['failover']           = ['proxy not to automatically failover',                                           DEFAULT]
        param_map['find_web']           = ['Find web server by', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('DNS')
        return self._process_input(param_map)

    def ftpoverhttp(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose a parameter')
        param_map['login']        = ['login name to be used', DEFAULT]
        param_map['password']     = ['password to be used', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('FTPOVERHTTP')
        return self._process_input(param_map)

    def nativeftp(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose a parameter')
        param_map['enable']              = ['enable FTP proxy', DEFAULT]
        param_map['port']                = ['ports that FTP proxy', DEFAULT]
        param_map['port_range_passive']  = ['listen on for passive FTP',
                                            DEFAULT]
        param_map['port_range_active']   = ['listen on for active FTP',
                                            DEFAULT]
        param_map['use_active']          = ['use active mode when', DEFAULT]
        param_map['auth_format']         = ['the authentication format',
                                            DEFAULT, 1]
        param_map['enable_cache']        = ['like to enable caching', DEFAULT]
        param_map['enable_spoof']        = ['enable server IP spoofing',
                                            DEFAULT]
        param_map['pass_msg']            = ['pass FTP server welcome message',
                                            DEFAULT]
        param_map['cust_msg']            = ['customized server welcome ' \
                                            'message', DEFAULT]
        param_map['max_path_size']       = ['max path size for the ftp ' \
                                            'server', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('NATIVEFTP')
        return self._process_input(param_map)

    def https(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose a parameter')
        param_map['uri_style'] = ['HTTPS URI Logging Style', DEFAULT]
        param_map['decrypt'] = ['decrypt unauthenticated transparent',
                                   DEFAULT]
        param_map['action'] = ['Action to be taken when', DEFAULT, 1]
        param_map['sni'] = ['enable server name indication', DEFAULT]
        param_map['inter_certs'] = ['download of missing Intermediate Certificates', DEFAULT]
        param_map['decrypt_https'] = ['decrypt HTTPS requests', DEFAULT]
        param_map['session_resumption'] = ['enable session resumption', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('HTTPS')
        return self._process_input(param_map)

    def scanning(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose a parameter')
        param_map['mw_scan'] = ['proxy to do malware scanning', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SCANNING')
        return self._process_input(param_map)

    def miscellaneous(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose a parameter')
        param_map['health_chk']    = ['proxy to respond to health checks',
                                      DEFAULT]
        param_map['dynamic_adj']   = ['adjustment of TCP receive window',
                                      DEFAULT]
        param_map['dynamic_adj_send']   = ['adjustment of TCP send window',
                                      DEFAULT]
        param_map['cache_https']   = ['caching of HTTPS responses',
                                      DEFAULT]
        param_map['min_idle_timeout']   = ['minimum idle timeout for',
                                           DEFAULT]
        param_map['max_idle_timeout']   = ['maximum idle timeout for',
                                           DEFAULT]
        param_map['listen_p2']   = ['proxy to listen on P2', DEFAULT]
        param_map['mode']   = ['Mode of the proxy', DEFAULT, 1]
        param_map['spoof']   = ['Spoofing of the client IP', DEFAULT, 1]
        param_map['pass_http']   = ['pass HTTP X-Forwarded-For', DEFAULT]
        param_map['enable_server_sharing']   = ['enable server connection sharing', DEFAULT]
        param_map['tunneling']   = ['permit tunneling of non-HTTP', DEFAULT]
        param_map['block_nonssl'] = ['block tunneling of non-SSL', DEFAULT]
        param_map['log_values']  = ['to log values from X-Forwarded-For',
                                    DEFAULT]
        param_map['throttle']    = ['proxy to throttle content served',
                                    DEFAULT]
        param_map['use_client_ip'] = ['use client IP addresses', DEFAULT]
        param_map['fwd_tcp_rst'] = ['forward TCP RST sent by server', DEFAULT]
        param_map['enable_url_case_conversion'] = ['lower case conversion for velocity regex', DEFAULT]
        param_map['enter_ip'] = ['enter the IP addresses for trusted',
                                 REQUIRED]
        param_map['buffer_clientside']   = ['send buffer for client-side socket',
                                     DEFAULT]
        param_map['wccp_health_check']   = ['wccp proxy health check',
                                     DEFAULT]
        param_map['disable_host_ip']   = ['disable IP address in Host',
                                     DEFAULT]
        param_map['filter_non_http']  =  ['filter non-http responses', DEFAULT]
        param_map['schedule_proxy_restart']  =  ['schedule a proxy restart', DEFAULT]
        param_map['cleanup_stale_connections'] = ['Cleanup Stale/leak connections', DEFAULT]
        param_map['time_to_connection_leak'] = ['Maximum idle time to detect the connection leak', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('MISCELLANEOUS')
        return self._process_input(param_map)

    def proxyconn(self):
        self._query_response('PROXYCONN')
        return self

    def _add_user_agent(self, user_agent):
        self._query_response('new')
        self._read_until(patt='>', timeout=5)
        self._writeln(user_agent)
        self._to_the_top(2)

    def _delete_user_agent(self, user_agent):
        self._query_response('delete')
        self._query_select_list_item(user_agent)
        self._to_the_top(2)

    def customHeaderNew(self, header, domains):
        self._query_response('CUSTOMHEADERS')
        self._query_response('NEW')
        self._query('Please enter the custom HTTP header')
        self._writeln(header)
        self._query('Please enter the list of suffix of domains')
        self._writeln(domains)
        self._to_the_top(self.newlines)

    def customHeaderEdit(self, header, newheader, newdomains):
        self._query_response('CUSTOMHEADERS')
        self._query_response('EDIT')
        self._query('Currently defined custom headers')
        self._query_select_list_item(header)
        self._query('Please enter the custom HTTP header')
        self._writeln(newheader)
        self._query('Please enter the list of suffix of domains')
        self._writeln(newdomains)
        self._to_the_top(self.newlines)

    def customHeaderDelete(self, header):
        self._query_response('CUSTOMHEADERS')
        self._query_response('DELETE')
        self._query('Currently defined custom headers')
        self._query_select_list_item(header)
        self._to_the_top(self.newlines)

    def contentencoding(self, type='', enable=''):
        self._query_response('CONTENT-ENCODING')
        self._query('select an option')
        self._query_select_list_item(type, self.getbuf())
        i = self._query('is currently allowed','is currently blocked')
        if i == 1 and enable.lower() == 'yes':
            self._query_response('y')
        elif i == 0 and enable.lower() == 'no':
            self._query_response('y')
        else :
            self._query_response('')
        self._to_the_top(1)

