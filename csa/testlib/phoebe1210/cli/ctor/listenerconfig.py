#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/listenerconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import clictorbase as ccb
from sal.exceptions import ConfigError
import re
from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES, NO
from sal.containers import CfgHolder

REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
NO_DEFAULT = ccb.NO_DEFAULT


class listenerconfig(ccb.IafCliConfiguratorBase):
    """listenerconfig"""

    newlines = 1

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Please enter a value.',
             EXACT): ccb.IafCliValueError,
            ('A Recipient Access Table address can be one of the following',
             EXACT): ccb.IafCliValueError,
        })

    def _is_blackhole_injector(self, injector_type):
        return self._is_injector_type(injector_type, 'blackhole')

    def _is_public_injector(self, injector_type):
        return self._is_injector_type(injector_type, 'public')

    def _is_private_injector(self, injector_type):
        return self._is_injector_type(injector_type, 'private')

    def _is_injector_type(self, injector_type, type_str):
        if injector_type.lower().find(type_str) == 0:
            return True
        else:
            return False

    def __call__(self):
        import handlecluster
        self._writeln('listenerconfig')

        # to handle clustered environment
        handlecluster.handle_cluster_questions(self._sess)

        return self

    # this is the new "process_input" implementation
    def new(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='created.')
        param_map['injector_type'] = ['type of listener', DEFAULT, 1]
        param_map['injector_name'] = ['create a name', REQUIRED]
        param_map['qtodisk'] = ['queued', DEFAULT]
        param_map['ip_interface'] = ['IP interface', DEFAULT, 1]
        param_map['mail_protocol'] = ['protocol', DEFAULT, 1]
        param_map['mail_port'] = ['TCP port', NO_DEFAULT]
        param_map['accept_for_addresses'] = ['accept mail for', NO_DEFAULT]
        param_map['enable_sbrs'] = ['based on SenderBase', DEFAULT]
        param_map['relay_hosts'] = ['relay email', NO_DEFAULT]
        param_map['rate_limiting_bool'] = ['rate limiting', DEFAULT]
        param_map['default_max_rcpts_per_hour'] \
            = ['Enter the maximum', NO_DEFAULT]
        param_map['change_default_hat_bool'] = ['host access', DEFAULT]
        param_map['bounce_profile'] = ['bounce profile', DEFAULT, 1]
        param_map['max_msg_size'] = ['maximum message size.', DEFAULT]
        param_map['max_concurrency'] = ['maximum number of concurrent' \
                                        ' connections', DEFAULT]
        param_map['mmps'] = ['maximum number of messages per' \
                             ' connection.', DEFAULT]
        param_map['mrpm'] = ['maximum number of recipients per' \
                             ' message.', DEFAULT]
        param_map['use_override_hostname'] = ['Do you want to override the ' \
                                              'hostname in the SMTP banner?', \
                                              DEFAULT]

        param_map['modify_smtp_banner'] = ['Would you like to specify a ' \
                                           'custom SMTP response?', \
                                           DEFAULT]

        param_map['modify_acpt_banner'] = ['Would you like to specify a ' \
                                           'custom SMTP acceptance ' \
                                           'response?', DEFAULT]

        param_map['modify_reject_banner'] = ['Would you like to specify ' \
                                             'a custom SMTP rejection ' \
                                             'response?', DEFAULT]

        param_map['enable_mrph'] = ['per host?', DEFAULT]
        param_map['mrph'] = ['Enter the maximum number of ' \
                             'recipients per hour from a ' \
                             'remote host.', DEFAULT]
        param_map['modify_mrph_banner'] = ['Would you like to specify a ' \
                                           'custom SMTP limit exceeded ' \
                                           'response?', NO]

        param_map['enable_sb'] = ['flow control by default?', DEFAULT]
        param_map['enable_host_grouping'] = ['Would you like to group ' \
                                             'hosts by the similarity of ' \
                                             'their IP addresses?', DEFAULT]
        param_map['spam_check'] = ['Would you like to enable ' \
                                   'anti-spam scanning?', DEFAULT]
        param_map['virus_check'] = ['Would you like to enable ' \
                                    'anti-virus scanning?', \
                                    DEFAULT]
        param_map['tls'] = ['Do you want to allow ' \
                            'encrypted TLS connections?', \
                            DEFAULT]
        param_map['dk_signing'] = ['Would you like to enable ' \
                                   'DomainKeys signing', DEFAULT]
        param_map['smime_publickeyharvest'] = ['Would you like to enable S/MIME Public Key Harvesting', DEFAULT]
        param_map['harvest_certificate'] = ['Would you like to harvest certificateon verification failure', DEFAULT]
        param_map['harvest_updatedcert'] = ['Would you like to harvest updated certificate', DEFAULT]
        param_map['smime_signing'] = ['Would you like to enable S/MIME gateway decryption/verification', DEFAULT]
        param_map['smime_signature'] = ['Select the appropriate operation for the S/MIME signature processing', DEFAULT]
        param_map['sender_vrfy'] = ['Would you like to enable ' \
                                    'envelope sender ' \
                                    'verification?', DEFAULT]
        param_map['domain_exception'] = ['Would you like to enable use ' \
                                         'of the domain exception table?', DEFAULT]
        param_map['untagged_bounces'] = ['accept untagged bounces?', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, name):

        self._query_parse_input_list()
        self._writeln('EDIT')
        self._query()
        self._select_list_item(name)
        return listenerconfigEdit(self._get_sess())

    def delete(self, name, confirm_continue=YES):
        self._query_parse_input_list()
        self._writeln('DELETE')
        self._query()
        self._select_list_item(name)
        # if injector to delete references filters, you get a warning message
        if self._query('WARNING', self._sub_prompt) == 0:
            self._query_response(confirm_continue)
            self._to_the_top(self.newlines)
        else:
            self._writeln()
            self._to_the_top(self.newlines - 1)

    def setup(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['max_concurrency'] = \
            ['global limit for concurrent connection', DEFAULT]
        param_map['max_tls_concurrency'] = \
            ['global limit for concurrent TLS', DEFAULT]
        param_map['max_headers'] = \
            ['number of message header lines', DEFAULT]
        param_map['sb_cache'] = ['Allow SenderBase', DEFAULT, 1]
        param_map['sb_cache_time'] = ['Enter the time, in', DEFAULT]
        param_map['inj_ctrl_rate'] = ['at which injection', DEFAULT]
        param_map['inbound_conn_timeout'] = ['unsuccessful inbound', DEFAULT]
        param_map['inbound_conn_max_time'] = ['maximum connection', DEFAULT]
        param_map['received_hostname'] = \
            ['hostname should Received:', DEFAULT, 1]
        param_map['add_msg_id_header'] = \
            ['system will always add', DEFAULT]
        param_map['msg_rcpt_level_reject'] = ['rejection at the message ' \
                                              'recipient level instead', DEFAULT]
        param_map['max_size_of_subject'] = ['Enter the maximum size of the subject', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def _get_listeners(self):
        """
        Returns the raw information about listeners configured.
        """
        raw = None
        try:
            raw = self._read_until('Choose the operation')
            if not re.search('^1\.', raw, re.MULTILINE):
                # Detected none listeners
                raw = None
        finally:
            # return to the CLI prompt
            self._to_the_top(self.newlines)
        return raw

    def get_listeners_info(self):
        """
        Returns ListenersInfo object which has all the info about listeners
        configured.
        """
        return ListenersInfo(self._get_listeners())

    def clusterset(self):
        raise ccb.IafCliCtorNotImplementedError

    def clustershow(self):
        raise ccb.IafCliCtorNotImplementedError


class listenerconfigEdit(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT """

    newlines = 3

    def name(self, name, confirm_continue=YES):
        self._query_response('NAME')
        self._query_response(name)
        # listener referenced by filters which will become invalid.  Continue?
        if self._query('Continue?', self._sub_prompt) == 0:
            self._query_response(confirm_continue)
            self._to_the_top(self.newlines)
        else:
            self._writeln()
            self._to_the_top(self.newlines - 1)

    def interface(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['ip_interface'] = ['choose an IP interface', DEFAULT, True]
        param_map['mail_protocol'] = ['Choose a protocol', DEFAULT, True]
        param_map['mail_port'] = ['enter the TCP por', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('interface')
        return self._process_input(param_map)

    def limits(self, max_connection='', qsize=''):
        self._query_response('LIMITS')
        self._query_response(str(max_connection))
        self._query_response(str(qsize))
        self._to_the_top(self.newlines)

    def setup(self):

        self._query_response('SETUP')
        return listenerconfigEditSetup(self._get_sess())

    def hostaccess(self):

        self._query_response('HOSTACCESS')
        return listenerconfigEditHostaccess(self._get_sess())

    def rcptaccess(self):

        self._query_response('RCPTACCESS')
        return listenerconfigEditRcptaccess(self._get_sess())

    def callahead(self, enable_bool, profile_name=DEFAULT):

        self._query_response('CALLAHEAD')
        self._query_response(enable_bool)
        if enable_bool:
            self._query_select_list_item(profile_name)

        self._to_the_top(self.newlines)

    def bounceconfig(self, bounce_profile, profile_name=None):
        self._query_response('BOUNCECONFIG')
        self._query_select_list_item(bounce_profile)
        if re.search('New Profile', bounce_profile, re.IGNORECASE):
            if profile_name:
                self._query_response(profile_name)
            else:
                raise ccb.IafCliValueError('profile_name=None for New profile')
        self._to_the_top(self.newlines)

    def masquerade(self, input_dict=None, **kwargs):

        param_map = ccb.IafCliParamMap(end_of_command='Domain Masquerading')
        param_map['use_LDAP_masquerading'] = ['to use LDAP for masquerading?', \
                                              DEFAULT]
        param_map['m_query'] = ['Available Masquerade Queries', DEFAULT, '1']
        param_map.update(input_dict or kwargs)

        self._query_response('MASQUERADE')
        self._process_input(param_map, do_restart=False, timeout=700)
        return listenerconfigEditMasquerade(self._get_sess())

    def setipmm(self, enable_bool):
        if not self._check_feature('merge_xmrg'):
            raise RuntimeError, 'ipmm not available'
        self._query_response('SETIPMM')
        self._query_response(enable_bool)
        self._to_the_top(self.newlines)

    def domainmap(self):

        self._query_response('DOMAINMAP')
        return listenerconfigEditDomainmap(self._get_sess())

    def ldapaccept(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['query'] = ['Acceptance Queries', DEFAULT, True]
        param_map['place'] = ['query be done in the work queue', DEFAULT, True]
        param_map['action'] = ['drop recipients or bounce', DEFAULT, True]
        param_map['ldap_timeout_action'] = ['action should be taken', \
                                            DEFAULT, True]
        param_map['ldap_response'] = ['LDAP server timeout', DEFAULT]
        param_map['ldap_response_code'] = ['451 is the standard', DEFAULT]
        param_map['dhap_response'] = ['DHAP response', DEFAULT]
        param_map['dhap_response_code'] = ['550 is the standard', DEFAULT]
        param_map['custom_response'] = ['custom SMTP response', [DEFAULT,
                                                                 DEFAULT]]
        param_map['drop'] = ['Directory Harvest Attack', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('LDAPACCEPT')
        return self._process_input(param_map)

    def ldaprouting(self, query_type):
        self._query_response('LDAPROUTING')
        self._query_select_list_item(query_type)
        self._to_the_top(self.newlines)

    def ldapgroup(self, query_type):
        self._query_response('LDAPGROUP')
        self._query_select_list_item(query_type)
        self._to_the_top(self.newlines)

    def smtpauth(self, enable_bool, profile_name):
        self._query_response('SMTPAUTH')
        self._query_response(enable_bool)
        if enable_bool:
            self._query_select_list_item(profile_name)
        self._to_the_top(self.newlines)

    def certificate(self, name):
        self._query_response('CERTIFICATE')
        self._query_select_list_item(name)
        self._to_the_top(self.newlines)


class listenerconfigEditSetup(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP"""

    newlines = 4

    def defaultdomain(self, default_domain, partial_domain_bool):
        self._query_response('DEFAULTDOMAIN')
        self._query_response(default_domain)
        if self._query(re.compile('reject.*partial domain\?', re.IGNORECASE),
                       self._sub_prompt) == 0:
            self._query_response(partial_domain_bool)
            self._to_the_top(self.newlines)
        else:
            self._writeln()
            self._to_the_top(self.newlines - 1)

    def received(self, enable_received_header_bool):
        self._query_response('RECEIVED')
        self._query_response(enable_received_header_bool)
        self._to_the_top(self.newlines)

    def cleansmtp(self, clean_smtp, confirm_continue=YES):
        self._query_response('CLEANSMTP')
        self._query_select_list_item(clean_smtp)
        # if Unclean is selected, you get a warning message
        if self._query('allow unclean messages?', self._sub_prompt) == 0:
            self._query_response(confirm_continue)
            self._to_the_top(self.newlines)
        else:
            self._writeln()
            self._to_the_top(self.newlines - 1)

    def senderbase(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Enable SenderBase'
                                                      ' Reputation Filters and IP Profiling')
        param_map['enable_sbrs'] = \
            ['enable SenderBase Reputation Filters', DEFAULT]
        param_map['timeout_sbrs'] = \
            ['a timeout, in seconds, for SenderBase', DEFAULT]
        param_map['timeout_sbrs_perconn'] = \
            ['all SenderBase queries per connection', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SENDERBASE')
        return self._process_input(param_map)

    def footer(self, footer_rsrc_bool, footer_rsrc=None,
               remove_footer_rsrc_bool=None):
        self._query_response('FOOTER')

        # assume footer text resources has been configured!
        i = self._query('Would you like', 'Footer stamping', 'No message')
        if i == 0:
            self._query_response(footer_rsrc_bool)
            if footer_rsrc_bool == YES:
                self._query_select_list_item(footer_rsrc)
        elif i == 1:
            self._query_response(remove_footer_rsrc_bool)
        elif i == 2:
            pass  # nothing to input
        else:
            raise RuntimeError, 'unexpected CLI output'
        self._to_the_top(self.newlines)

    def address(self):

        self._query_response('ADDRESS')
        return listenerconfigEditSetupAddress(self._get_sess())


class listenerconfigEditSetupAddress(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP -> ADDRESS"""
    newlines = 4

    def type(self, address_parser_type):
        self._query_response('TYPE')
        self._query_select_list_item(address_parser_type)
        self._to_the_top(self.newlines)

    def eightbituser(self, eight_bit_user_bool):
        self._query_response('8BITUSER')
        self._query_response(eight_bit_user_bool)
        self._to_the_top(self.newlines)

    def eightbitdomain(self, eight_bit_domain_bool):
        self._query_response('8BITDOMAIN')
        self._query_response(eight_bit_domain_bool)
        self._to_the_top(self.newlines)

    def partial(self, partial_domain_bool, confirm_enable_partial_domain_bool,
                confirm_disable_partial_domain_bool):
        self._query_response('PARTIAL')

        self._query_response(partial_domain_bool)
        if partial_domain_bool:
            # if no default domain
            if self._query('enable partial domain', self._sub_prompt) == 0:
                self._query_response(confirm_enable_partial_domain_bool)
                self._to_the_top(self.newlines)
            else:
                self._writeln()
                self._to_the_top(self.newlines - 1)
        else:
            if self._query('disable partial domain', self._sub_prompt) == 0:
                self._query_response(confirm_disable_partial_domain_bool)
                self._to_the_top(self.newlines)
            else:
                self._writeln()
                self._to_the_top(self.newlines - 1)

    def source(self, source_routing):
        self._query_response('SOURCE')
        self._query_select_list_item(source_routing)
        self._to_the_top(self.newlines)

    def literal(self, accept_unknown_literal):
        self._query_response('LITERAL')
        self._query_select_list_item(accept_unknown_literal)
        self._to_the_top(self.newlines)

    def special(self, reject_username_chars):
        self._query_response('SPECIAL')
        self._query_response(reject_username_chars)
        self._to_the_top(self.newlines)


class EditHatParameters(ccb.IafCliConfiguratorBase):

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)

    def _edit_hat_params(self, hat_params, input_dict=None):

        # First param map
        param_map1 = ccb.IafCliParamMap(end_of_command='Do you want to ' \
                                                       'enable rate limiting')

        param_map1['max_msg_size'] = ['maximum message size.', DEFAULT]
        param_map1['max_concurrency'] = ['maximum number of concurrent' \
                                         ' connections', DEFAULT]
        param_map1['mmps'] = ['maximum number of messages per' \
                              ' connection.', DEFAULT]
        param_map1['mrpm'] = ['maximum number of recipients per' \
                              ' message.', DEFAULT]
        param_map1['use_override_hostname'] = ['Do you want to override the ' \
                                               'hostname in the SMTP banner?', \
                                               DEFAULT]
        param_map1['override_hostname'] = ['Enter the hostname to use in' \
                                           ' the SMTP banner', NO_DEFAULT]
        param_map1['modify_smtp_banner'] = ['Would you like to specify a ' \
                                            'custom SMTP response?', \
                                            DEFAULT]
        param_map1['modify_acpt_banner'] = ['Would you like to specify a ' \
                                            'custom SMTP acceptance ' \
                                            'response?', DEFAULT]
        param_map1['acpt_banner_code'] = ['220 is the standard ' \
                                          'code.', DEFAULT]

        param_map1['modify_reject_banner'] = ['Would you like to specify ' \
                                              'a custom SMTP rejection ' \
                                              'response?', DEFAULT]
        param_map1['reject_banner_code'] = ['554 is the standard ' \
                                            'code.', DEFAULT]

        # Second part of param map
        param_map2 = ccb.IafCliParamMap(end_of_command='Would you like to ' \
                                                       'use SenderBase for')

        # This answer is not default, the default one depends on the type of
        # listener and the policy
        param_map2['enable_dhap'] = ['Do you want to enable ' \
                                     'Directory Harvest Attack ' \
                                     'Prevention per host?', NO]  # not DEFAULT
        param_map2['dhap_limit'] = ['Enter the maximum number of ' \
                                    'invalid recipients per hour ' \
                                    'from a remote host.', DEFAULT]
        param_map2['dhap_action'] = ['Select an action to apply when ' \
                                     'a recipient is rejected', \
                                     DEFAULT, 1]
        param_map2['dhap_SMTP_response'] = ['specify a custom SMTP DHAP ' \
                                            'response', DEFAULT]
        param_map2['dhap_SMTP_code'] = ['550 is the standard', DEFAULT]
        param_map2['enable_mrph'] = ['per host?', DEFAULT]
        param_map2['mrph'] = ['Enter the maximum number of ' \
                              'recipients per hour from a ' \
                              'remote host.', DEFAULT]
        param_map2['modify_mrph_banner'] = ['Would you like to specify a ' \
                                            'custom SMTP limit exceeded ' \
                                            'response?', NO]
        param_map2['mrph_banner_code'] = ['452 is the standard code.', \
                                          DEFAULT]
        param_map2['enable_mrpes'] = ['per envelope sender?', DEFAULT]
        param_map2['mrpes'] = ['Enter the maximum number of ' \
                               'recipients ', \
                               DEFAULT]
        param_map2['mrpes_interval'] = ['interval in minutes for ' \
                                        'Envelope Sender Rate Limiting', DEFAULT]
        param_map2['exceed_smtp_limit'] = ['custom SMTP limit ' \
                                           'exceeded response?', DEFAULT]
        param_map2['smtp_code'] = ['SMTP code to use in ' \
                                   'the response', DEFAULT]
        param_map2['smtp_response'] = ['Enter your custom ' \
                                       'SMTP response', DEFAULT]
        param_map2['addr_list'] = ['Address List to ' \
                                   'define exceptions', DEFAULT]

        # Third part of param map
        param_map3 = ccb.IafCliParamMap(end_of_command= \
                                            'Default Policy Parameters')

        param_map3['enable_sb'] = ['flow control by default?', DEFAULT]
        param_map3['enable_host_grouping'] = ['Would you like to group ' \
                                              'hosts by the similarity of ' \
                                              'their IP addresses?', DEFAULT]
        param_map3['significant_bits'] = ['Enter the number of bits of ' \
                                          'IP address to treat as ' \
                                          'significant', DEFAULT]
        param_map3['delayed_sb'] = ['Will this IronPort ' \
                                    'applicance need to fetch ' \
                                    'the incoming address ' \
                                    '(for SenderBase) from ' \
                                    'a trusted relay\'s ' \
                                    'header?', NO_DEFAULT]
        param_map3['delayed_sb_header'] = ['Enter the header name ' \
                                           'containing the IP ' \
                                           'address', NO_DEFAULT]
        param_map3['spam_check'] = ['Would you like to enable ' \
                                    'anti-spam scanning?', DEFAULT]
        param_map3['virus_check'] = ['Would you like to enable ' \
                                     'anti-virus scanning?', \
                                     DEFAULT]
        param_map3['tls'] = ['Do you want to allow ' \
                             'encrypted TLS connections?', \
                             DEFAULT]
        param_map3['addr_list_tls'] = ['Choose address list to ' \
                                       'enforce TLS', DEFAULT]
        param_map3['really_use_demo_cert_bool'] = ['You may use the demo ' \
                                                   'certificate to test TLS,' \
                                                   'but this will not be ' \
                                                   'secure. Do you really ' \
                                                   'wish to us', DEFAULT]
        param_map3['smtpauth_allow'] = ['Do you want to allow SMTP ' \
                                        'authentication?', DEFAULT, 1]
        param_map3['smtpauth_requiretls'] = ['Require TLS to offer SMTP ' \
                                             'authentication?', NO_DEFAULT]
        param_map3['dk_signing'] = ['Would you like to enable ' \
                                    'DKIM/DomainKeys signing', DEFAULT]
        param_map3['smime_publickeyharvest'] = ['Would you like to enable S/MIME Public Key Harvesting', DEFAULT]
        param_map3['harvest_certificate'] = ['Would you like to harvest certificate on verification failure', DEFAULT]
        param_map3['harvest_updatedcert'] = ['Would you like to harvest updated certificate', DEFAULT]
        param_map3['smime_signing'] = ['Would you like to enable S/MIME gateway decryption/verification', DEFAULT]
        param_map3['smime_signature'] = ['Select the appropriate operation for the S/MIME signature processing',
                                         DEFAULT]
        param_map3['dk_vrfy'] = ['Would you like to enable ' \
                                 'DKIM verification?', DEFAULT]
        param_map3['dk_vrfy_profile'] = ['Select the DKIM verification' \
                                         ' profile to use', DEFAULT]
        param_map3['spf_change'] = ['change SPF', DEFAULT]
        param_map3['spf_vrfy'] = ['perform SPF',
                                  DEFAULT]
        param_map3['spf_level'] = ['What Conformance Level',
                                   DEFAULT]
        param_map3['spf_pra_vrfy'] = ['Downgrade PRA verification' \
                                      ' result', DEFAULT]
        param_map3['spf_helo'] = ['Would you like to have the ' \
                                  'HELO check performed?', DEFAULT]
        param_map3['spf_vrfy_timeout'] = ['Verification timeout', DEFAULT]
        param_map3['smtp_after_spf'] = ['Would you like to change SMTP actions' \
                                        ' taken as result of the SPF verification?', DEFAULT]
        param_map3['dmarc_vrfy'] = ['enable DMARC verification', DEFAULT]
        param_map3['dmarc_vrfy_profile'] = ['DMARC verification profile to use' \
            , DEFAULT]
        param_map3['dmarc_send_reports'] = ['send aggregate reports', DEFAULT]
        param_map3['sender_vrfy'] = ['Would you like to enable ' \
                                     'envelope sender verification?', DEFAULT]
        param_map3['domain_exception'] = ['Would you like to enable use ' \
                                          'of the domain exception table?', \
                                          DEFAULT]
        param_map3['untagged_bounces'] = ['accept untagged bounces?', DEFAULT]
        param_map3['modify_rmes_banner'] = ['Would you like to specify a ' \
                                            'custom SMTP response for ' \
                                            'malformed envelope senders?', \
                                            DEFAULT]
        param_map3['rmes_banner_code'] = ['553 is the standard code', DEFAULT]
        param_map3['comment'] = ['Enter a comment', DEFAULT]

        ## TODO TODO TODO:
        ## - Passing YES (and sometimes DEFAULT) to these two variables
        ##   will throw an exeception because the custom response has
        ##   been special cased (see below) for rmes_banner_code.
        ########
        param_map3['env_sender_domain_dont_resolve'] = ['Would you like to ' \
                                                        'specify a custom SMTP response for envelope sender ' \
                                                        'domains which do not resolve?', NO]

        param_map3['env_sender_domain_dont_exist'] = ['Would you like to ' \
                                                      'specify a custom SMTP response for envelope sender domains ' \
                                                      'which do not exist?', NO]

        # Processing param map parts

        # Processing param_map part 1
        actual_dict = {}
        for param in hat_params.keys():
            if param in param_map1._map.keys():
                actual_dict[param] = hat_params[param]
        param_map1.update(input_dict or actual_dict)

        if hat_params.has_key('modify_smtp_banner') and \
                hat_params['modify_smtp_banner'] == YES:
            param_map1.set_ending_string("Enter the SMTP code to use in the"
                                         " response")
            self._process_input(param_map1, do_restart=False)
            self._query_response(hat_params['smtp_banner_code'])
            self._writeln(hat_params['smtp_banner_text'])
            self._writeln()

        if hat_params.has_key('modify_reject_banner') and \
                hat_params['modify_reject_banner'] == YES:
            param_map1.set_ending_string("Enter your custom SMTP response")
            self._process_input(param_map1, do_restart=False)
            self._writeln(hat_params['reject_banner_text'])
            self._writeln()

        if hat_params.has_key('modify_acpt_banner') and \
                hat_params['modify_acpt_banner'] == YES:
            param_map1.set_ending_string("Enter your custom SMTP response")
            self._process_input(param_map1, do_restart=False)
            self._writeln(hat_params['acpt_banner_text'])
            self._writeln()

        param_map1.set_ending_string("enable rate limiting")
        self._process_input(param_map1, do_restart=False)

        # Processing param_map part 2
        actual_dict = {}
        for param in hat_params.keys():
            if param in param_map2._map.keys():
                actual_dict[param] = hat_params[param]
        param_map2.update(input_dict or actual_dict)

        if hat_params.has_key('modify_mrph_banner') and \
                hat_params['modify_mrph_banner'] == YES:
            param_map2.set_ending_string("Enter your custom SMTP response.")
            self._process_input(param_map2, do_restart=False)
            self._writeln(hat_params['mrph_banner_text'])
            self._writeln()
        elif hat_params.has_key('enable_dhap') and \
                hat_params['enable_dhap'] == YES:
            param_map2.set_ending_string("Enter your custom SMTP response")
            self._process_input(param_map2, do_restart=False)
            self._writeln(hat_params['dhap_response_text'])
            self._writeln()

        param_map2.set_ending_string("Would you like to use SenderBase for")
        self._process_input(param_map2, do_restart=False)

        # Processing param map part 3
        actual_dict = {}
        for param in hat_params.keys():
            if param in param_map3._map.keys():
                actual_dict[param] = hat_params[param]
        param_map3.update(input_dict or actual_dict)

        # Leaving off the "== YES" makes DEFAULT return True
        if hat_params.get('modify_rmes_banner') == YES:
            param_map3.set_ending_string("Enter your custom SMTP response")
            self._process_input(param_map3, do_restart=False)
            self._writeln(hat_params['sender_vrfy_bad_domain_smtp_text'])
            self._writeln()

        if hat_params.has_key('comment'):
            param_map3.set_ending_string("Enter a comment")
            self._process_input(param_map3, do_restart=False)
            self._writeln(hat_params['comment'])
            self._writeln()
        param_map3.set_ending_string("Choose the operation")
        self._process_input(param_map3, do_restart=False)
        return


class listenerconfigEditHostaccess(EditHatParameters):
    """listenerconfig -> EDIT -> HOSTACCESS"""

    newlines = 3

    def __init__(self, sess):
        EditHatParameters.__init__(self, sess)
        self._set_local_err_dict({
            ('Connecting host PTR record does not exist in DNS',
             EXACT): ccb.IafCliValueError,
            ('Connecting host PTR record lookup fails due to temporary',
             EXACT): ccb.IafCliValueError,
            ('Connecting host reverse DNS lookup (PTR) does not match',
             EXACT): ccb.IafCliValueError,
            ('The hostaccess "import" command requires a filename',
             EXACT): ccb.IafCliValueError,
            ('The hostaccess "export" command requires a filename.',
             EXACT): ccb.IafCliValueError,
            ('No policies to edit.', EXACT): ccb.IafUnknownOptionError,
            ('The hostaccess "delete" command requires either \
                        "sendergroup" or "policy" and a name.',
             EXACT): ccb.IafCliValueError,
            ('Invalid hostaccess "delete" command:',
             EXACT): ccb.IafUnknownOptionError,
            ('The hostaccess "move" command requires a sendergroup',
             EXACT): ccb.IafCliValueError,
            ('Invalid selected behavior:', EXACT): ccb.IafCliValueError,
            ('Invalid "max_size" value:', EXACT): ccb.IafCliValueError,
            ('"max_conn" can only be "default" when working with policies.',
             EXACT): ccb.IafCliValueError,
            ('Invalid "max_conn" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "max_msgs" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "max_rcpt" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "override" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "cust_acc" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "acc_code" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "cust_rej" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "rej_code" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "rate_lim" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "rate_lim" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "cust_lim" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "lim_code" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "use_sb" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "as_scan" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "av_scan" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "sig_bits" value:', EXACT): ccb.IafCliValueError,
            ('Invalid "dhap" value:', EXACT): ccb.IafCliValueError,
            ('Invalid value.', EXACT): ccb.IafCliValueError,
        })

    def new(self, entry_type, new_name, host_list, access_behavior,
            hat_change_bool=NO, hat_params=None, comment=None):
        """hat_params: an object"""
        self._writeln('NEW')
        self._query()
        self._query_parse_input_list()
        is_sender_group = self._select_list_item(entry_type)
        self._query_response(new_name)
        if is_sender_group == 1:
            self._query_response(host_list)
        self._query_parse_input_list()
        self._select_list_item(access_behavior)
        self._query_response(hat_change_bool)
        if hat_change_bool == YES:
            self._edit_hat_params(hat_params)
        if is_sender_group == 1:
            self._query_response(comment)
        self._to_the_top(self.newlines)

    def edit(self, sg_or_policy, name, access_behavior, hat_change_bool=NO,
             hat_params=None):
        """sg_or_policy is a string: 'Policy' or 'Sender Group'"""

        self.clearbuf()
        self._query_response('EDIT')
        idx = self._query('HAT sender groups', 'HAT policies', self._sub_prompt)
        if idx == 2:
            self._select_list_item(sg_or_policy.title(),
                                   text_block=self.getbuf())
        if sg_or_policy.lower() == 'sender group':
            self._query_select_list_item(name)
            return listenerconfigEditHostaccessEditSenderGroup(self._get_sess())
        elif sg_or_policy.lower() == 'policy':
            self._query_select_list_item(name)
            self._query_select_list_item(access_behavior)
            self._query_response(hat_change_bool)
            if hat_change_bool == YES:
                self._edit_hat_params(hat_params)
            self._to_the_top(self.newlines)

    def delete(self, sg_or_policy, name, confirm_policy_deletion_bool=YES):
        """sg_or_policy is a string: 'Policy' or 'Sender Group'"""
        self.clearbuf()
        self._query_response('DELETE')
        idx = self._query('HAT sender groups', 'HAT policies', self._sub_prompt)
        if idx == 2:
            self._select_list_item(sg_or_policy.title(),
                                   text_block=self.getbuf())
        if sg_or_policy.lower() == 'sender group':
            self._query_select_list_item(name)
            self._to_the_top(self.newlines)
        elif sg_or_policy.lower() == 'policy':
            self._query_select_list_item(name)
            # at least one sender group references this policy. delete anyway?
            if self._query('continue?', self._sub_prompt) == 0:
                self._query_response(confirm_policy_deletion_bool)
                self._to_the_top(self.newlines)
            else:
                self._writeln()
                self._to_the_top(self.newlines - 1)

    def move(self, sg_to_move, sg_to_insert_before):
        self._query_response('MOVE')
        self._query_select_list_item(sg_to_move)
        self._query_select_list_item(sg_to_insert_before)
        self._to_the_top(self.newlines)

    def default(self, hat_params):
        """hat_params:"""
        self._query_response('DEFAULT')
        self._edit_hat_params(hat_params)
        self._to_the_top(self.newlines)

    def Print(self):
        self._query_response('PRINT')
        self._query()
        output = self._get_last_matched_text()
        result = re.findall("PRINT(.*)Choose the operation", output, re.DOTALL)
        if result:
            print_output = result[0].strip()
        else:
            print_output = None
        self._to_the_top(self.newlines)
        return print_output

    def Import(self, filename):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def export(self, filename):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def clear(self):
        self._query_response('RESET')
        self._to_the_top(self.newlines)


class listenerconfigEditHostaccessEditSenderGroup(EditHatParameters):
    """listenerconfig -> EDIT -> SETUP -> HOSTACCESS -> EDIT"""

    newlines = 5

    def __init__(self, sess):
        EditHatParameters.__init__(self, sess)

    def new(self, host_list, confirm_add_sender=YES):
        self._query_response('NEW')
        self._query_response(host_list)
        # sender group already has sender host. add anyway?
        if self._query('Add anyway?', self._sub_prompt) == 0:
            self._query_select_list_item(confirm_add_sender)
            self._to_the_top(self.newlines)
        else:
            self._writeln()
            self._to_the_top(self.newlines - 1)

    def delete(self, host):
        self._query_response('DELETE')
        self._query_select_list_item(host)
        self._to_the_top(self.newlines)

    def move(self, host_to_move, host_to_insert_before):
        self._query_response('MOVE')
        self._query_select_list_item(host_to_move)
        self._query_select_list_item(host_to_insert_before)
        self._to_the_top(self.newlines)

    def country(self):
        self._query_response('COUNTRY')
        return listenerconfigEditHostaccessEditSenderGroupEditCountry(self._get_sess())

    def externalthreatfeeds(self):
        self._query_response('EXTERNAL THREAT FEED SOURCE')
        return listenerconfigEditHostaccessEditSenderGroupEditExternalthreatfeeds(self._get_sess())

    def policy(self, access_behavior, change_policy_parameters_bool, \
               hat_params):
        """hat_params:"""
        self._query_response('POLICY')
        self._query_select_list_item(access_behavior)
        self._query_response(change_policy_parameters_bool)
        self._edit_hat_params(hat_params)
        self._to_the_top(self.newlines)

    def Print(self):
        self._query_response('PRINT')
        self._to_the_top(self.newlines)

    def rename(self, new_name):
        self._query_response('RENAME')
        self._query_response(new_name)
        self._to_the_top(self.newlines)


class listenerconfigEditHostaccessEditSenderGroupEditCountry(EditHatParameters):
    newlines = 5

    def add(self, countries):
        self._query_response('ADD')
        self._query_response(countries)
        self._to_the_top(self.newlines)

    def delete(self, countries):
        self._query_response('DELETE')
        self._query_response(countries)
        self._to_the_top(self.newlines)

    def Print(self):
        self._query_response('PRINT')
        self._query()
        output = self.getbuf()
        result = re.findall("> PRINT(.*)Choose the operation", output, re.DOTALL)
        if result:
            print_output = result[0].strip()
        else:
            print_output = None
        self._to_the_top(self.newlines - 1)
        return print_output


class listenerconfigEditHostaccessEditSenderGroupEditExternalthreatfeeds(EditHatParameters):
    newlines = 5

    def add(self, source_names):
        self._query_response('ADD')
        self._query_response(source_names)
        self._to_the_top(self.newlines)

    def delete(self, source_names):
        self._query_response('DELETE')
        self._query_response(source_names)
        self._to_the_top(self.newlines)

    def Print(self):
        self._query_response('PRINT')
        self._query()
        output = self.getbuf()
        result = re.findall("> PRINT(.*)Choose the operation", output, re.DOTALL)
        if result:
            print_output = result[0].strip()
        else:
            print_output = None
        self._to_the_top(self.newlines - 1)
        return print_output


class listenerconfigEditRcptaccess(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP -> RCPTACCESS"""

    newlines = 4

    def new(self, addrs=REQUIRED,
            action=DEFAULT,
            smtp_response=DEFAULT,
            smtp_response_code=DEFAULT,
            smtp_response_text="",
            bypass_injection_control=DEFAULT,
            bypass_ldap_accept=DEFAULT,
            smtp_call_ahead=DEFAULT):
        param_map = ccb.IafCliParamMap( \
            end_of_command='specify a custom SMTP response')
        param_map['addrs'] = ['recipient address for this entry', DEFAULT]
        param_map['action'] = ['action to apply to this address', DEFAULT, True]

        input_dict = {}
        for key in ['addrs', 'action']:
            if locals()[key]:
                input_dict[key] = locals()[key]

        param_map.update(input_dict)
        self._query_response('NEW')
        self._process_input(param_map, do_restart=False)

        # if smtp response needs to be provided
        if (smtp_response == YES or smtp_response.lower() == 'yes') or \
                (smtp_response == DEFAULT and self._is_last_default_yes()):
            self._query_response(smtp_response)
            self._query_response(smtp_response_code)
            self._writeln(smtp_response_text)
            self._writeln("")  # write blank line to terminate input
            self._query()
        else:
            self._query_response(smtp_response)

        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['bypass_injection_control'] = ['receiving control for this ' \
                                                 'entry', DEFAULT]
        param_map['bypass_ldap_accept'] = ['to bypass LDAP ACCEPT', DEFAULT]
        param_map['smtp_call_ahead'] = ['to bypass SMTP Call-Ahead', DEFAULT]

        input_dict = {}
        for key in ['bypass_injection_control', 'bypass_ldap_accept', \
                    'smtp_call_ahead']:
            if locals()[key]:
                input_dict[key] = locals()[key]
        param_map.update(input_dict)
        return self._process_input(param_map)

    def edit(self, address=REQUIRED,
             access=DEFAULT,
             custom_smtp_response=DEFAULT,
             smtp_response_code=DEFAULT,
             smtp_response_text="",
             bypass_injection_control=DEFAULT,
             bypass_ldap_accept=DEFAULT,
             smtp_call_ahead=DEFAULT):
        param_map = ccb.IafCliParamMap( \
            end_of_command='specify a custom SMTP response')
        param_map['address'] = ['Enter the address to edit', DEFAULT]
        param_map['access'] = ['What access for', DEFAULT, True]

        input_dict = {}
        for key in ['address', 'access']:
            if locals()[key]:
                input_dict[key] = locals()[key]

        param_map.update(input_dict)
        self._query_response('EDIT')
        self._process_input(param_map, do_restart=False)

        # if smtp response needs to be provided
        if (custom_smtp_response == YES or \
            custom_smtp_response.lower() == 'yes') or \
                (custom_smtp_response == DEFAULT and self._is_last_default_yes()):
            self._query_response(custom_smtp_response)
            self._query_response(smtp_response_code)
            self._writeln(smtp_response_text)
            self._writeln("")  # write blank line to terminate input
            self._query()
        else:
            self._query_response(custom_smtp_response)
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['bypass_injection_control'] = ['receiving control for this ' \
                                                 'entry', DEFAULT]
        param_map['bypass_ldap_accept'] = ['to bypass LDAP ACCEPT', DEFAULT]
        param_map['smtp_call_ahead'] = ['to bypass SMTP Call-Ahead', DEFAULT]

        input_dict = {}
        for key in ['bypass_injection_control', 'bypass_ldap_accept', \
                    'smtp_call_ahead']:
            if locals()[key]:
                input_dict[key] = locals()[key]
        param_map.update(input_dict)
        return self._process_input(param_map)

    def delete(self, address):
        try:
            self._query_response('DELETE')
            self._query_response(address)
        finally:
            self._to_the_top(self.newlines)

    def Print(self, print_all_entries_bool=YES):
        """ Parse RAT entries from CLI and return as dictionary """
        self._query_response('PRINT')

        # Execute subcommand and get raw text
        if self._query('could take a while', 'Recipient Access Table') == 0:
            self._query_response(print_all_entries_bool)
            self._query('Recipient Access Table')
            table_text = self._get_last_matched_text()
        else:
            table_text = self._get_last_matched_text()

        self._to_the_top(self.newlines)

        # These are strings in the raw text that we use to make
        # sure the right data will be parsed
        expected_cli_cruft = ['PRINT', 'Recipient Access Table', '']
        rat_lines = table_text.splitlines()

        for phrase in expected_cli_cruft:
            if phrase not in rat_lines:
                raise ConfigError, "RcptAccess --> PRINT did not yield " \
                                   "expected text. Actual output follows: \n\n%s\n" \
                                   % table_text

        # Strip out whitespace and CLI cruft from the RAT entry list.
        rat_lines = [line.strip() for line in rat_lines if line not in \
                     expected_cli_cruft]

        return self._parse_rat_text_into_dict(rat_lines)

    def _parse_rat_text_into_dict(self, rat_lines):
        """ Take a list of printed RAT entries and return a RAT dictionary """
        rat_dict = {}
        for line in rat_lines:
            # Should use rsplit(), but releng uses Python 2.3
            split_line = line.strip().split(' ')
            entry = ' '.join(split_line[:-1]).strip()
            policy = split_line[-1].strip()

            rat_dict[entry] = policy

        return rat_dict

    def Import(self, filename):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def export(self, filename):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def clear(self, default_access_behavior):
        self._query_response('CLEAR')
        self._query_select_list_item(default_access_behavior)
        self._to_the_top(self.newlines)


class listenerconfigEditDomainmap(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP -> DOMAINMAP"""
    newlines = 4

    def new(self, orig_dom, new_dom):
        self._query_response('NEW')
        self._query_response(orig_dom)
        self._query_response(new_dom)
        self._to_the_top(self.newlines)

    def edit(self, orig_dom, new_dom):
        self._query_response('EDIT')
        self._query_response(orig_dom)
        self._query_response(new_dom)
        self._to_the_top(self.newlines)

    def delete(self, orig_dom):
        self._query_response('DELETE')
        self._query_response(orig_dom)
        self._to_the_top(self.newlines)

    def Print(self):
        self._query_response('PRINT')
        self._to_the_top(self.newlines)

    def Import(self, filename):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def export(self, filename):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.newlines)


class listenerconfigEditMasquerade(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP -> MASQUERADE"""
    newlines = 4

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Error:', EXACT): ccb.IafCliError,
        })

    def new(self, left, right):
        self._query_response('NEW')
        self._query_response(left)
        if right:
            self._query_response(right)
        self._to_the_top(self.newlines)

    def delete(self, to_delete):
        self._query_response('DELETE')
        self._query_response(to_delete)
        self._to_the_top(self.newlines)

    def Print(self, print_all=True):
        self._query_response('PRINT')
        if self._query('This could take a while', self._sub_prompt) == 0:
            self._query_response(print_all)
            self._to_the_top(self.newlines)
        else:
            self._writeln()
            self._to_the_top(self.newlines - 1)

    def Import(self, filename, timeout=ccb.default_timeout):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._read_until('Domain Masquerading', timeout=timeout)
        self._to_the_top(self.newlines)

    def export(self, filename):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def config(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['mail_from_bool'] = ['querade Envelope Sender?', DEFAULT]
        param_map['from_bool'] = ['From headers?', DEFAULT]
        param_map['to_bool'] = ['To headers?', DEFAULT]
        param_map['cc_bool'] = ['CC headers?', DEFAULT]
        param_map['reply_to_bool'] = ['Reply-To headers?', DEFAULT]

        param_map.update(input_dict or kwargs)
        self._query_response('CONFIG')
        self._process_input(param_map)
        self._to_the_top(1)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.newlines)


class ListenersInfo(object):

    def __init__(self, raw):
        """
        Container to represent information about configured listeners.
        - `raw`: Output returned after 'listenerconfig' CLI command.
        - `all`: List containing all listeners.
        - `public`: List containing public listeners.
        - `private`: List containing private listeners.
        - `black`: List containing BlackHole listeners.

        Each entry in the list is CfgHolder.
        """
        self.raw = raw
        self.all_listeners = []
        self.public = []
        self.private = []
        self.black = []
        self.parse_output()

    def parse_output(self):
        """
        Parse raw output returned after 'listenerconfig' CLI command.
        """
        if not self.raw:
            # No listeners configured
            return
        else:
            re_listener_info = re.compile('^\d\.' +
                                          '\s+(\S+)' +
                                          '\s+\(on\s+(.+?),\s+(.+?)' +
                                          '(,\s+(.*))*\)' +
                                          '\s+(\S+)' +
                                          '\s+(\S+)' +
                                          '\s+Port\s+(\d+)' +
                                          '\s+(\S+)', re.MULTILINE)
            matches = re_listener_info.finditer(self.raw)
            for match in matches:
                self.listener = CfgHolder()
                self.listener.name = match.group(1)
                self.listener.interface = match.group(2)
                self.listener.ipv4 = match.group(3)
                self.listener.ipv6 = match.group(5)
                self.listener.type = match.group(6)
                self.listener.protocol = match.group(7)
                self.listener.port = match.group(8)
                self.listener.scope = match.group(9)
                self.all_listeners.append(self.listener)
                if self.listener.scope.find('Public') != -1:
                    self.public.append(self.listener)
                elif self.listener.scope.find('Private') != -1:
                    self.private.append(self.listener)
                elif self.listener.scope.find('Black') != -1:
                    self.black.append(self.listener)
                else:
                    raise ValueError \
                        ('Unknown listener scope: %s' % self.listener.scope)

    def __str__(self):
        res = ''
        for lr in self.all_listeners:
            res += ','.join \
                (['%s: %s' % (key, value) for (key, value) \
                  in lr.iteritems() if value])
            res += '\n'
        return res

    def findlisteners(self, **kwargs):
        """
        Returns the list of listeners matched criteria provided.
        Pass arguments you are interested in only and be sure to skip the rest.
        kwargs may contain these parameters:

        - name
        - interface
        - ipv4
        - ipv6
        - type
        - protocol
        - port
        - scope
        """
        res = []
        if not any(kwargs.values()):
            return self.all_listeners
        # build dictionary with value!=None
        given_params = {}
        for k, v in kwargs.iteritems():
            if v is not None:
                given_params[k] = v
        for listener in self.all_listeners:
            # maybe it would be more convenient to compare with lower()
            # but ESA's listeners names are case sensitive,
            # so 'Listener' and 'listener' are different values.
            if all(listener[param] == given_params[param] for param in \
                   given_params.keys()):
                res.append(listener)
        return res
