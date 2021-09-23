#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/listenerconfig.py#1 $

# start: Fri Nov 18 16:37:08 PST 2005
# break: Fri Nov 18 17:47:11 PST 2005
#       10 min break?
#
# break: Fri Nov 18 18:47:13 PST 2005
# start timing: Sat Nov 19 12:16:31 PST 2005 [working maybe 2 hours?]

# HI PRI
# 2. test: handle looping ring buffer
# 3. test: bool [yes,no,true,false]
# 4. test: query()
# 5. test: newlines for to-the-top
# 2. if self._check_feature('merge_xmrg'):

# TODO: rename injector to listener
# YES
# if self._query('reject.*partial domain\?', self._sub_prompt) == 0: ##REGEX
#
#       note: if sub_prompt matches, it has already been read!!!!
#
# if self._is_policy()
# if self._is_sender_group()
#    def _to_the_top(self):
# if self._check_feature('merge_xmrg'):
# raise RuntimeError. define better exception
# bool: true, false, yes , no?
# use global timeout
# lambda alias re.compile(IGNORECASE)
# move exceptions to config.py file

import clictorbase as ccb
import re
from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES, NO
REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
NO_DEFAULT = ccb.NO_DEFAULT

class listenerconfig(ccb.IafCliConfiguratorBase):
    """listenerconfig"""
    newlines = 1

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
        #import handlecluster
        self._writeln('listenerconfig')

        # to handle clustered environment
        #handlecluster.handle_cluster_questions(self._sess)

        return self

    # this is the new "process_input" implementation
    def new(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='created.')
        param_map['injector_type']          = ['type of listener', DEFAULT, 1]
        param_map['injector_name']          = ['create a name', REQUIRED]
        param_map['qtodisk']                = ['queued', DEFAULT]
        param_map['ip_interface']           = ['IP interface', DEFAULT, 1]
        param_map['mail_protocol']          = ['protocol', DEFAULT, 1]
        param_map['mail_port']              = ['TCP port', NO_DEFAULT]
        param_map['accept_for_addresses']   = ['accept mail for', NO_DEFAULT]
        param_map['enable_sbrs']            = ['based on SenderBase', DEFAULT]
        param_map['relay_hosts']            = ['relay email', NO_DEFAULT]
        param_map['rate_limiting_bool']     = ['rate limiting', DEFAULT]
        param_map['default_max_rcpts_per_hour'] \
                                            = ['Enter the maximum', NO_DEFAULT]
        param_map['change_default_hat_bool']= ['host access', DEFAULT]
        param_map['bounce_profile']         = ['bounce profile', DEFAULT, 1]
        param_map['max_msg_size']           = ['maximum message size.', DEFAULT]
        param_map['max_concurrency'] = ['maximum number of concurrent' \
                                        ' connections',  DEFAULT]
        param_map['mmps']            = ['maximum number of messages per' \
                                        ' connection.', DEFAULT]
        param_map['mrpm']            = ['maximum number of recipients per' \
                                        ' message.', DEFAULT]
        param_map['use_override_hostname'] = ['Do you want to override the ' \
                                              'hostname in the SMTP banner?', \
                                               DEFAULT]

        param_map['modify_smtp_banner']    = ['Would you like to specify a ' \
                                              'custom SMTP response?', \
                                               DEFAULT]

        param_map['modify_acpt_banner']    = ['Would you like to specify a ' \
                                              'custom SMTP acceptance ' \
                                              'response?', DEFAULT]

        param_map['modify_reject_banner']  = ['Would you like to specify ' \
                                              'a custom SMTP rejection ' \
                                              'response?', DEFAULT]

        param_map['enable_mrph']           = ['per host?', DEFAULT]
        param_map['mrph']                  = ['Enter the maximum number of ' \
                                              'recipients per hour from a ' \
                                              'remote host.', DEFAULT]
        param_map['modify_mrph_banner']    = ['Would you like to specify a ' \
                                              'custom SMTP limit exceeded ' \
                                              'response?', NO]

        param_map['enable_sb']          = ['flow control by default?', DEFAULT]
        param_map['enable_host_grouping']  = ['Would you like to group ' \
                                              'hosts by the similarity of ' \
                                              'their IP addresses?', DEFAULT]
        param_map['spam_check']            = ['Would you like to enable ' \
                                              'anti-spam scanning?', DEFAULT]
        param_map['virus_check']           = ['Would you like to enable ' \
                                              'anti-virus scanning?', \
                                               DEFAULT]
        param_map['tls']                   = ['Do you want to allow ' \
                                              'encrypted TLS connections?', \
                                               DEFAULT]
        param_map['dk_signing']             = ['Would you like to enable ' \
                                               'DomainKeys signing', DEFAULT]
        param_map['sender_vrfy']            = ['Would you like to enable ' \
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
        param_map = ccb.IafCliParamMap(end_of_command = 'Choose the operation')
        param_map['max_concurrency'] = ['global limit for concurrent', DEFAULT]
        param_map['max_headers']  = \
                                    ['number of message header lines', DEFAULT]
        param_map['sb_cache']               = ['Allow SenderBase', DEFAULT, 1]
        param_map['sb_cache_time']          = ['Enter the time, in', DEFAULT]
        param_map['inj_ctrl_rate']          = ['at which injection', DEFAULT]
        param_map['inbound_conn_timeout']   = ['unsuccessful inbound', DEFAULT]
        param_map['inbound_conn_max_time']  = ['maximum connection', DEFAULT]
        param_map['received_hostname']      = \
  	                      ['hostname should Received:', DEFAULT, 1]
        param_map['msg_id_header']          = \
                              ['add a Message-ID header', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def get_listeners(self):
        """
        Print and returns the raw information about listeners configured.
        """
        raw =  None
        try:
            raw = self._read_until('Choose the operation')
            if not re.search('^1\.', raw, re.MULTILINE):
                #Detected none listeners
                raw =  None
        finally:
            # return to the CLI prompt
            self._to_the_top(self.newlines)
        return raw

    def clusterset(self):
        raise ccb.IafCliCtorNotImplementedError

    def clustershow(self):
        raise ccb.IafCliCtorNotImplementedError

class listenerconfigEdit(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT """
    newlines = 2

    def name(self,name, confirm_continue = YES):
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
        param_map = ccb.IafCliParamMap(end_of_command = 'Choose the operation')
        param_map['ip_interface']   = ['choose an IP interface', DEFAULT, True]
        param_map['mail_protocol']  = ['Choose a protocol', DEFAULT]
        param_map['mail_port']      = ['enter the TCP por', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('interface')
        return self._process_input(param_map)

    def limits(self, max_connection = '', qsize = ''):
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

    def bounceconfig(self,bounce_profile, profile_name=None):
        self._query_response('BOUNCECONFIG')
        self._query_select_list_item(bounce_profile)
        if re.search('New Profile', bounce_profile, re.IGNORECASE):
            if profile_name:
                self._query_response(profile_name)
            else:
                raise IafCliValueError('profile_name=None for New profile')
        self._to_the_top(self.newlines)

    def masquerade(self):
        self._query_response('MASQUERADE')
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
        param_map['ldap_response'] = ['LDAP server timeout', DEFAULT]
        param_map['ldap_response_code'] = ['451 is the standard', DEFAULT]
        param_map['dhap_response'] = ['DHAP response', DEFAULT]
        param_map['dhap_response_code'] = ['550 is the standard', DEFAULT]
        param_map['custom_response'] = ['custom SMTP response', [DEFAULT, DEFAULT]]
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

class listenerconfigEditSetup(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP"""
    newlines = 3

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

    def cleansmtp(self, clean_smtp_bool):
        self._query_response('CLEAMSMTP')
        self._query_response(clean_smtp_bool)
        self._to_the_top(self.newlines)

    def senderbase(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Enable SenderBase'
                                    ' Reputation Filters and IP Profiling')
        param_map['enable_sbrs'] =\
                        ['enable SenderBase Reputation Filters', DEFAULT]
        param_map['timeout_sbrs'] =\
                    ['a timeout, in seconds, for SenderBase', DEFAULT]
        param_map['timeout_sbrs_perconn'] =\
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
            pass # nothing to input
        else:
            raise RuntimeError, 'unexpected CLI output'
        self._to_the_top(self.newlines)

    def address(self):
        self._query_response('ADDRESS')
        return listenerconfigEditSetupAddress(self._get_sess())

class listenerconfigEditSetupAddress(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP -> ADDRESS"""
    newlines = 3
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


class EditHatParameters:
    def _edit_hat_params(self, hat_params, input_dict=None):

        # First param map
        param_map1 = ccb.IafCliParamMap(end_of_command='Do you want to allow ')

        param_map1['max_msg_size']    = ['maximum message size.', DEFAULT]
        param_map1['max_concurrency'] = ['maximum number of concurrent' \
                                         ' connections', DEFAULT]
        param_map1['mmps']            = ['maximum number of messages per' \
                                        ' connection.', DEFAULT]
        param_map1['mrpm']            = ['maximum number of recipients per' \
                                        ' message.', DEFAULT]
        param_map1['use_override_hostname'] = ['Do you want to override the ' \
                                              'hostname in the SMTP banner?', \
                                               DEFAULT]
        param_map1['override_hostname']     = ['Enter the hostname to use in' \
                                              ' the SMTP banner', NO_DEFAULT]
        param_map1['modify_smtp_banner']    = ['Would you like to specify a ' \
                                              'custom SMTP response?', \
                                               DEFAULT]
        param_map1['smtp_banner_code']      = ['554 is the standard ' \
                                              'code.', DEFAULT]
        param_map1['modify_acpt_banner']    = ['Would you like to specify a ' \
                                              'custom SMTP acceptance ' \
                                              'response?', DEFAULT]
        param_map1['acpt_banner_code']      = ['220 is the standard ' \
                                              'code.', DEFAULT]

        param_map1['modify_reject_banner']  = ['Would you like to specify ' \
                                              'a custom SMTP rejection ' \
                                              'response?', DEFAULT]
        param_map1['reject_banner_code']    = ['554 is the standard ' \
                                              'code.', DEFAULT]

        # Second part of param map
        param_map2 = ccb.IafCliParamMap(end_of_command=\
                                               'Default Policy Parameters')

        param_map2['tls']                   = [ 'encrypted TLS connections?', \
                                               DEFAULT]
        param_map2['smtpauth_allow']         = ['Do you want to allow SMTP ' \
                                               'authentication?', DEFAULT, 1]
        param_map2['smtpauth_requiretls']    = ['Require TLS to offer SMTP ' \
                                               'authentication?', NO_DEFAULT]
        param_map2['dk_signing']             = ['Would you like to enable ' \
                                               'DKIM/DomainKeys signing', DEFAULT]
        param_map2['dk_vrfy']                = ['Would you like to enable ' \
                                                'DKIM verification?', DEFAULT]
        param_map2['sender_vrfy']            = ['Would you like to enable ' \
                                               'envelope sender ' \
                                               'verification?', DEFAULT]
        param_map2['spf_change']             = ['change SPF', DEFAULT]
        param_map2['spf_vrfy']               = ['perform SPF', DEFAULT]
        param_map2['spf_level']              = ['What level of conformance ' \
                                                            'to apply', DEFAULT]
        param_map2['spf_pra_vrfy']           = ['Downgrade PRA verification' \
                                                             ' result', DEFAULT]
        param_map2['spf_helo']               = ['Should the HELO test be ' \
                                                               'done?', DEFAULT]
        param_map2['domain_exception'] = ['Would you like to enable use ' \
                                         'of the domain exception table?', \
                                         DEFAULT]
        param_map2['untagged_bounces'] = ['accept untagged bounces?', DEFAULT]
        param_map2['modify_rmes_banner'] = ['Would you like to specify a ' \
                                            'custom SMTP response for ' \
                                            'malformed envelope senders?', \
                                            DEFAULT]
        param_map2['rmes_banner_code'] = ['553 is the standard code', DEFAULT]

        ## TODO TODO TODO:
        ## - Passing YES (and sometimes DEFAULT) to these two variables
        ##   will throw an exeception because the custom response has
        ##   been special cased (see below) for rmes_banner_code.
        ########
        param_map2['env_sender_domain_dont_resolve'] =  ['Would you like to '\
            'specify a custom SMTP response for envelope sender '\
            'domains which do not resolve?', NO]

        param_map2['env_sender_domain_dont_exist'] = ['Would you like to ' \
            'specify a custom SMTP response for envelope sender domains '\
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
            param_map1.set_ending_string("Enter your custom SMTP response")
            self._process_input(param_map1, do_restart=False)
            self._writeln(hat_params['smtp_banner_text'])
            self._writeln()
        elif hat_params.has_key('modify_reject_banner') and \
           hat_params['modify_reject_banner'] == YES:
            param_map1.set_ending_string("Enter your custom SMTP response")
            self._process_input(param_map1, do_restart=False)
            self._writeln(hat_params['reject_banner_text'])
            self._writeln()
        elif hat_params.has_key('modify_acpt_banner') and \
           hat_params['modify_acpt_banner'] == YES:
            param_map1.set_ending_string("Enter your custom SMTP response")
            self._process_input(param_map1, do_restart=False)
            self._writeln(hat_params['acpt_banner_text'])
            self._writeln()
        else:
            self._process_input(param_map1, do_restart=False)

        # Processing param_map part 2
        actual_dict = {}
        for param in hat_params.keys():
            if param in param_map2._map.keys():
                actual_dict[param] = hat_params[param]
        param_map2.update(input_dict or actual_dict)

        # Leaving off the "== YES" makes DEFAULT return True
        if hat_params.get('modify_rmes_banner') == YES:
            param_map2.set_ending_string("Enter your custom SMTP response")
            self._process_input(param_map2, do_restart=False)
            self._writeln(hat_params['sender_vrfy_bad_domain_smtp_text'])
            self._writeln()
        else:
            self._process_input(param_map2, do_restart=False)
            self._writeln()

        return


class listenerconfigEditHostaccess(ccb.IafCliConfiguratorBase,
                                   EditHatParameters):
    """listenerconfig -> EDIT -> HOSTACCESS"""
    newlines = 3

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
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
            hat_change_bool, hat_params=NO, comment=None):
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

    def default(self,hat_params):
        """hat_params:"""
        self._query_response('DEFAULT')
        self._edit_hat_params(hat_params)
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

class listenerconfigEditHostaccessEditSenderGroup(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP -> HOSTACCESS -> EDIT"""
    newlines = 4

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

    def policy(self, access_behavior,change_policy_parameters_bool,hat_params):
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

class listenerconfigEditRcptaccess(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP -> RCPTACCESS"""
    newlines = 2

    def new(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['addrs'] = ['recipient address', REQUIRED]
        param_map['action'] = ['action to apply', DEFAULT, True]
        param_map['smtp_response'] = ['custom SMTP response?', DEFAULT]
        param_map['smtp_response_code'] = ['Enter the SMTP code', DEFAULT]
        param_map['smtp_response_text'] = ['Enter your custom', NO_DEFAULT]
        param_map['bypass_injection_control'] = ['receiving control', DEFAULT]
        param_map['bypass_ldap_accept'] = ['bypass LDAP ACCEPT', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, address = REQUIRED,
                   access = DEFAULT,
                   custom_smtp_response = DEFAULT,
                   smtp_response_code = DEFAULT,
                   smtp_response_text = "",
                   bypass_injection_control = DEFAULT,
                   bypass_ldap_accept= DEFAULT):
        self._query_response('EDIT')
        self._query_response(address)
        self._query_select_list_item(access)
        if (custom_smtp_response == YES) or \
           (custom_smtp_response == DEFAULT and self._is_last_default_yes()):
            self._query_response(custom_smtp_response)
            self._query_response(smtp_response_code)
            self._writeln(smtp_response_text)
            self._writeln("") # write blank line to terminate input
        else:
            self._query_response(custom_smtp_response)
        if self._query('bypass receiving control', 'Choose the operation') == 0:
            self._query_response(bypass_injection_control)
            self._query_response(bypass_ldap_accept)
        self._to_the_top(self.newlines+1)


    def delete(self, address):
        try:
            self._query_response('DELETE')
            self._query_response(address)
        finally:
            self._to_the_top(self.newlines+1)

    def Print(self, print_all_entries_bool):
        self._query_response('PRINT')
        if self._query('could take a while', self._sub_prompt) == 0:
            self._query_response(print_all_entries_bool)
            self._to_the_top(self.newlines)
        else:
            self._writeln()
            self._to_the_top(self.newlines - 1)

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
        self._to_the_top(self.newlines + 1)

class listenerconfigEditDomainmap(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP -> DOMAINMAP"""
    newlines = 2

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


class listenerconfigEditMasquerade(ccb.IafCliConfiguratorBase):
    """listenerconfig -> EDIT -> SETUP -> MASQUERADE"""
    newlines = 3
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

    def Import(self, filename):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def export(self, filename):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def config(self, mail_from_bool, from_bool, to_bool, reply_to_bool):
        self._query_response('CONFIG')
        self._query_response(mail_from_bool)
        self._query_response(from_bool)
        self._query_response(to_bool)
        self._query_response(reply_to_bool)
        self._to_the_top(self.newlines)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.newlines)


class Listener:
    def __init__ (self, name=None, ifc=None, ip=None, type=None, prot=None,
                  port=None, scope=None):
        """
        attributes values sample:
           name             ifc         ip       type prot   port  scope
        2. privat_qmqp (on a001.d1, 172.21.41.1) QMQP TCP Port 628 Private
        3. public_smtp (on a001.d2, 172.22.41.1) SMTP TCP Port 25 Public
        """
        self.name=name
        self.ifc=ifc
        self.ip=ip
        self.type=type
        self.prot=prot
        self.port=port
        self.scope=scope

    def __str__(self):
        res = 'Name: %s, interface: %s, IP: %s, type: %s, transport: %s, \
                port: %s, scope: %s' %\
                (self.name, self.ifc, self.ip, self.type, self.prot, self.port,
                 self.scope)
        return res

    def __eq__(self, other):
        """
        compares Listener's atributes (case sensitive, full match).
        Doesn't take attribute values 'None' into account.
        So use to provide attributes you are interested in only.
        """
        loexpr = False
        loexpr = (not other.name or (self.name == other.name)) and\
                (not other.ifc or (self.ifc == other.ifc)) and\
                (not other.ip or (self.ip == other.ip)) and\
                (not other.type or (self.type == other.type)) and\
                (not other.prot or (self.prot == other.prot)) and\
                (not other.port or (self.port == other.port)) and\
                (not other.scope or (self.scope == other.scope))
        return loexpr


class ListenersInfo:
    def __init__ (self, ctor=None):
        """
        accepts IafTestBase.cfg.dut.cli.listenerconfig ctor as the paramater
        Example of new instance creation in an IAF test:
            lif=ListenersInfo(self.cfg.dut.cli.listenerconfig)
        """
        self.all=[]
        self.public=[]
        self.private=[]
        self.ctor=ctor
        if self.ctor:
            self._refresh()

    def _refresh(self):
        """
        No need to call this right after creating new ListenersInfo instance
        with correct ctor provided.
        Be sure to call this _refresh any time you whant to update the
        listeners iformation. This will erase existing listeners information
        and acquire actual.
        """
        if not self.ctor:
            raise Exception, 'No ctor provided to ListenersInfo class!'
        raw = self.ctor().get_listeners()
        self.all=[]
        self.public=[]
        self.private=[]
        if not raw:
            #No listeners configured
            return
        else:
            #parse the raw listeners info
            lines=raw.split('\n')
            re_listener = re.compile('^\d\.', re.MULTILINE)
            #See description at Listener.__init__() for listener record sample
            re_listener_info = re.compile('^\d\.' +
                                          '\s+(\S+)' +
                                          '\s+\(on\s+(\S+),'+
                                          '\s+([\d\.]+).*\)' +
                                          '\s+(\S+)' +
                                          '\s+(\S+)' +
                                          '\s+Port\s+(\d+)' +
                                          '\s+(\S+)', re.MULTILINE)
            for line in lines:
                mo = re_listener_info.match(line)
                if mo: # matched a listener
                    lr = Listener(mo.group(1), mo.group(2), mo.group(3),
                                  mo.group(4), mo.group(5), mo.group(6),
                                  mo.group(7))
                    self.all.append(lr)
                    if lr.scope.find('Public') != -1:
                        self.public.append(lr)
                    elif lr.scope.find('Private') != -1:
                        self.private.append(lr)
                    else:
                        raise Exception, 'unknown listener scope (%s)!' %\
                                            lr.scope
                else:
                    continue

    def __str__(self):
        res = ''
        for lr in self.all:
            if res:
                res += '\n'
            res += str(lr)
        return res

    def findlisteners(self, name=None, ifc=None, ip=None, type=None, prot=None,
                            port=None, scope=None):
        """
        returns the list of listeners matched criteria provided.
        Pass arguments you are interested in only and be sure to skip the rest.
        """
        res = []
        if not (name or ifc or ip or type or prot or port or scope):
            return self.all
        else:
            li_crit = Listener(name, ifc, ip, type, prot, port, scope)
            for li in self.all:
                if li == li_crit:
                    res.append(li)
        return res


if __name__ == '__main__':
    from iafframework import iafcfg
    my_host = iafcfg.get_hostname()
    iface = 'management'
    publist = 'public_smtp'

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
        iface = 'main'
        publist = 'main_smtp'
    except NameError:
        cli_sess = ccb.get_sess()
        if my_host.find('.eng') > -1:
            iface = 'main'
            publist = 'main_smtp'

    lc = listenerconfig(cli_sess)

    print '0Listeners configured, raw: [\\n%s]' % lc().get_listeners()

    # lc().edit('public_smtp').ldaprouting('2')

    lc().new(injector_type = 'private', injector_name = 'testpublic', \
        ip_interface = iface, mail_protocol = 'smtp', \
        mail_port = '26', relay_hosts = '.qa', rate_limiting_bool = NO)

    # Testing edit HAT functionality

    # entry_type
    # 1. New Sender Group
    # 2. New Policy

    # access_behavior
    # 1. Accept
    # 2. Relay
    # 3. Reject
    # 4. TCP Refuse
    # 5. Continue
    # 6. Policy: BLOCKED
    # 7. Policy: RELAYED

    m={}
    m['max_msg_size']=1000
    m['enable_mrph']=YES
    m['mrph']=1000
    m['enable_sb']=YES
    lc().edit(name='1').hostaccess().new(entry_type='New Policy', \
                  new_name='test1', host_list='.qa', access_behavior='Accept', \
                  hat_change_bool=YES, hat_params=m, comment='test')
    lc().edit('testpublic').name('foo')

    lc().edit('foo').interface(ip_interface = iface,
                               mail_protocol = 'qmqp', mail_port = 552)
    print '1Listeners configured, raw: [\\n%s]' % lc().get_listeners()

    print '\n>>>Testing the ListenersInfo:'
    lif=ListenersInfo(lc)
    print 'The listeners configured: [%s]' % lif
    print 'There are %s public listener(s)' % len(lif.public)
    print 'There are %s private listener(s)' % len(lif.private)
    print 'There are total %s listener(s)' % len(lif.all)
    print 'Here is all public SMTP listeners:'
    for li in lif.findlisteners(type = 'SMTP', scope = 'Public'):
        print '\t%s' % li
    print 'Here is all listeners with port 25:'
    for li in lif.findlisteners(port = '25'):
        print '\t%s' % li
    lc().delete('foo')
    print 'Here is all public SMTP listeners:'
    lif._refresh()
    for li in lif.findlisteners(type = 'SMTP', scope = 'Public'):
        print '\t%s' % li
    print '\n<<<Testing the ListenersInfo.'
    print '2Listeners configured, raw: [\\n%s]' % lc().get_listeners()

    # test the edit -> hostaccess part
    lc().edit(publist).hostaccess().new('New Sender Group','test','.qa','',NO)
    lc().edit(publist).hostaccess()\
            .edit('sender group', 'test','','','').new('SBRS[-10.0:-9.0]')
    lc().edit(publist).hostaccess().delete('sender group', 'test')
    lc().edit(publist).hostaccess().new('New Policy', 'test','','',NO)
    lc().edit(publist).hostaccess().edit('policy', 'test', 'Relay')
    lc().edit(publist).hostaccess().delete('policy', 'test')

    print('Validation for incorrect message size')
    err_msg = "Value must be"
    try:
        lc().new(injector_type = 'private', injector_name = 'newlistener', \
            ip_interface = '1', mail_port = '27', relay_hosts = '.qa', \
            rate_limiting_bool = YES, default_max_rcpts_per_hour = '10', \
            change_default_hat_bool = YES, max_msg_size = '1000000001')
    except ccb.IafCliValueError, err:
        print "Received IafCliValueError, as expected"
        cli_sess.interrupt_writeln()
        cli_sess.interrupt_writeln()
        cli_sess.wait_for_prompt()
    else:
        raise "Did not receive IafCliValueError as expected"

    print("Setting GMHC to 10")
    lc().setup(max_concurrency = 10)

    print("Setting GMHC to 1000")
    lc().setup(max_concurrency = 1000)

    hat_param = {}
    hat_param['enable_mrph'] = NO
    hat_param['enable_sb'] = NO
    hat_param['virus_check'] = NO
    hat_param['sender_vrfy'] = YES
    hat_param['modify_rmes_banner'] = NO
    hat_param['modify_reject_banner'] = NO
    hat_param['env_sender_domain_dont_resolve'] = NO
    hat_param['env_sender_domain_dont_exist'] = NO

    lc().edit(name=publist).hostaccess().default(hat_params = hat_param)

