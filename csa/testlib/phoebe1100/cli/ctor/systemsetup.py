# !/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/systemsetup.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
IAF2 CLI Command: systemsetup
"""

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap, ConfigError
from sal.containers.yesnodefault import YES, NO
from credentials import *
# from common.util.misc import Misc
import re


class systemsetup(clictorbase.IafCliConfiguratorBase):
    def __init__(self, args, **kwargs):
        # questions may or may not appear depending
        # on answers for previous question(s)
        # eg 'port' parameter will appear only if two
        # listeners are being configured on the same interface
        self._warn('Will ignore unanswered questions!')
        clictorbase.set_ignore_unanswered_questions(ignore=True)
        ending_strings = re.compile('(Enter passphrase:)|(User Guide.)')
        self.param_map = IafCliParamMap(end_of_command=ending_strings)
        super(self.__class__, self).__init__(args, **kwargs)

    def configure_interface(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed for interface configuration.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        _ethernet = kwargs.pop('ethernet')
        if _ethernet == 'management':
            self.param_map['%s_hostname' % _ethernet] = \
                ['create a fully qualified hostname', DEFAULT]
        else:
            self.param_map['%s_enable' % _ethernet] = \
                ['use the Ethernet interface', DEFAULT]
            self.param_map['%s_nickname' % _ethernet] = \
                ['create a nickname', REQUIRED]
        self.param_map['%s_enable_ipv4' % _ethernet] = \
            ['Would you like to configure an IPv4 address for this interface',
             DEFAULT]
        self.param_map['%s_ipv4' % _ethernet] = ['IPv4 Address', NO_DEFAULT]
        self.param_map['%s_netmask' % _ethernet] = ['Netmask', DEFAULT]
        self.param_map['%s_enable_ipv6' % _ethernet] = \
            ['Would you like to configure an IPv6 address for this interface',
             DEFAULT]
        self.param_map['%s_ipv6' % _ethernet] = ['IPv6 Address', REQUIRED]
        self.param_map['%s_prefix' % _ethernet] = ['Prefix length', DEFAULT]

        ## This workaround is need till lab team fixes
        ## #140939 Need to resolve Data 3 interface for C670 models
        self.param_map['data3_enable'] = \
            ['use the Ethernet interface labeled Data 3', NO]
        self.param_map.update(input_dict or kwargs)

    def configure_router(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed for router(s) configuration.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        self.param_map['enable_gw_ipv4'] = \
            ['default router for your IPv4 ', DEFAULT]
        self.param_map['gw_ipv4'] = \
            ['IP address of the default router', DEFAULT]
        self.param_map['enable_gw_ipv6'] = \
            ['default router for your IPv6 ', DEFAULT]
        self.param_map['gw_ipv6'] = \
            ['IP address of the default router', DEFAULT]
        self.param_map.update(input_dict or kwargs)

    def configure_cluster(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed for cluster configuration.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        self.param_map['create_cluster'] = \
            ['to join or create a cluster?', DEFAULT, 1]
        self.param_map['cluster_name'] = \
            ['name of the new cluster.', NO_DEFAULT]
        self.param_map['enable_cluster'] = \
            ['enable the Cluster Communication Service', DEFAULT]
        self.param_map['cluster_interface'] = \
            ['Choose the interface on which to enable the Cluster', DEFAULT]
        self.param_map['cluster_port'] = \
            ['port on which to enable the Cluster', DEFAULT]
        self.param_map['cluster_communicate'] = \
            ['cluster communicate with each other by hostname or by IP address',
             DEFAULT]
        self.param_map['cluster_communicate_ip'] = \
            ['IP address should other machines use to communicate', DEFAULT]
        self.param_map['cluster_machine_ip'] = \
            ['IP address of a machine in the cluster.', NO_DEFAULT]
        self.param_map['cluster_machine_port'] = \
            ['remote port to connect', NO_DEFAULT]
        self.param_map['cluster_adm'] = \
            ['name of an administrator present on the remote machine', DEFAULT]
        self.param_map['cluster_group'] = \
            ['group to place this machine in.', NO_DEFAULT]
        self.param_map['commit_and_continue'] = \
            ['need to be committed before continuing', YES]
        self.param_map.update(input_dict or kwargs)

    def configure_web(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed for web configuration.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        self.param_map['use_web_interface'] = \
            ['enable the web interface', DEFAULT]
        self.param_map['use_https'] = ['use secure HTTPS?', DEFAULT]
        self.param_map.update(input_dict or kwargs)

    def configure_dns(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed for DNS configuration.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        self.param_map['dns_server'] = ['own DNS servers?', DEFAULT, 1]
        self.param_map['dns_ip'] = ['IP address of your DNS server.', DEFAULT]
        self.param_map['use_another_dns_server'] = \
            ['enter another DNS server?', NO]
        self.param_map.update(input_dict or kwargs)

    def configure_listener(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed for listeners configuration.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        _type = kwargs.pop('listener_type')
        _listener = '%s_listener' % _type
        self.param_map['%s_name' % _listener] = \
            ['create a name for this listener', REQUIRED]
        self.param_map['%s_interface' % _listener] = \
            ['choose an IP interface for this Listener.', DEFAULT, 1]
        if _listener.startswith('public'):
            self.param_map['%s_domain_or_email' % _listener] = \
                ['domain names or specific email addresses', NO_DEFAULT]
            self.param_map['%s_use_smtp_route' % _listener] = \
                ['configure SMTP routes', DEFAULT]
            self.param_map['%s_destination_server' % _listener] = \
                ['destination mail server', DEFAULT]
            self.param_map['%s_use_senderbase' % _listener] = \
                ['(SBRS) Scores for this listener?', DEFAULT]
        self.param_map['%s_use_rate_limiting' % _listener] = \
            ['enable rate limiting for this listener?', DEFAULT]
        self.param_map['%s_rate_limiting' % _listener] = \
            ['the maximum number of recipients per hour to accept',
             NO_DEFAULT]
        if _listener.startswith('private'):
            self.param_map['%s_use_relay_mail_for_int_hosts' % _listener] = \
                ['relay mail for internal hosts?', DEFAULT]
            self.param_map['%s_port' % _listener] = \
                ['enter the TCP port for this listener.', NO_DEFAULT]
            self.param_map['%s_relay_mail' % _listener] = \
                ['allowed to relay email through the Cisco IronPort', NO_DEFAULT]
        self.param_map.update(input_dict or kwargs)

    def configure_hat(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed for HAT configuration.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        _type = kwargs.pop('hat_type')
        self.param_map['%s_change_hat_policy' % _type] = \
            ['change the default host access policy?', DEFAULT]
        self.param_map['%s_max_msg_size' % _type] = \
            ['maximum message size.', DEFAULT]
        self.param_map['%s_max_concurrency' % _type] = \
            ['maximum number of concurrent connections', DEFAULT]
        self.param_map['%s_max_msgs_per_conn' % _type] = \
            ['maximum number of messages', DEFAULT]
        self.param_map['%s_max_recipients_per_msg' % _type] = \
            ['maximum number of recipients per message.', DEFAULT]
        self.param_map['%s_override_smtp_banner' % _type] = \
            ['override the hostname in the SMTP banner?', DEFAULT]
        self.param_map['%s_hostname_in_smtp_banner' % _type] = \
            ['hostname to use in the SMTP banner', NO_DEFAULT]
        self.param_map['%s_use_smtp_accept_response' % _type] = \
            ['custom SMTP acceptance response?', DEFAULT]
        self.param_map['%s_smtp_accept_code' % _type] = \
            ['220 is the standard code', DEFAULT]
        self.param_map['%s_smtp_accept_response' % _type] = \
            ['Enter your custom SMTP response', NO_DEFAULT, 0, 0]
        self.param_map['%s_use_smtp_reject_response' % _type] = \
            ['custom SMTP rejection response?', DEFAULT]
        self.param_map['%s_smtp_reject_code' % _type] = \
            ['554 is the standard code', DEFAULT]
        self.param_map['%s_smtp_reject_response' % _type] = \
            ['Press Enter on a blank line to finish', NO_DEFAULT]
        self.param_map['%s_use_rate_limiting_per_host' % _type] = \
            ['enable rate limiting per host?', DEFAULT]
        self.param_map['%s_rate_limiting_per_host' % _type] = \
            ['maximum number of recipients per hour from a remote host', NO_DEFAULT]
        self.param_map['%s_use_smtp_exceed_response' % _type] = \
            ['specify a custom SMTP limit exceeded response?', DEFAULT]
        self.param_map['%s_smtp_exceed_code' % _type] = \
            ['452 is the standard code', DEFAULT]
        self.param_map['%s_smtp_exceed_response' % _type] = \
            ['Enter your custom SMTP response.  Press Enter on a blank line to finish.',
             NO_DEFAULT]
        self.param_map['%s_use_rate_limiting_per_envelope_sender' % _type] = \
            ['enable rate limiting per envelope sender', DEFAULT]
        self.param_map['%s_rate_limiting_per_envelope_sender' % _type] = \
            ['maximum number of recipients from an envelope sender', NO_DEFAULT]
        self.param_map['%s_rate_limiting_per_envelope_sender_interval' % _type] = \
            ['time interval in minutes for Envelope Sender Rate Limiting', DEFAULT]
        # bug in CLI systemsetup. the questions below are asked twice. why???
        #### need this
        self.param_map['%s_use_smtp_exceed_response1' % _type] = \
            ['Would you like to specify a custom SMTP limit exceeded', NO]
        ####
        self.param_map['%s_enable_dhap' % _type] = \
            ['enable Directory Harvest Attack Prevention per host', YES]
        self.param_map['%s_dhap_limit' % _type] = \
            ['maximum number of invalid recipients per hour from a remote host',
             DEFAULT]
        self.param_map['%s_dhap_action' % _type] = \
            ['action to apply when a recipient is rejected due to DHAP',
             DEFAULT, True]
        self.param_map['%s_use_dhap_smtp_response' % _type] = \
            ['specify a custom SMTP DHAP response?', DEFAULT]
        self.param_map['%s_dhap_smtp_response_code' % _type] = \
            ['550 is the standard code', DEFAULT]
        self.param_map['%s_dhap_smtp_response' % _type] = \
            ['your custom SMTP response.', NO_DEFAULT]
        self.param_map['%s_use_senderbase' % _type] = \
            ['SenderBase for flow control by default?', DEFAULT]
        self.param_map['%s_enable_antispam' % _type] = \
            ['enable anti-spam scanning?', DEFAULT]
        self.param_map['%s_enable_antivirus' % _type] = \
            ['enable anti-virus scanning?', DEFAULT]
        self.param_map['%s_allow_tls' % _type] = \
            ['allow encrypted TLS connections?', DEFAULT, 1]
        self.param_map['%s_allow_smtp_auth' % _type] = \
            ['allow SMTP authentication?', DEFAULT, 1]
        self.param_map['%s_require_tls_to_offer_smtp' % _type] = \
            ['Require TLS to offer SMTP', DEFAULT, 1]
        self.param_map['%s_enable_domainkeys' % _type] = \
            ['enable DKIM/DomainKeys signing?', DEFAULT]
        self.param_map['%s_enable_dkim' % _type] = \
            ['enable DKIM verification?', DEFAULT]
        self.param_map['%s_dkim_profile' % _type] = \
            ['the DKIM verification profile to use', DEFAULT]
        self.param_map['%s_change_spf' % _type] = \
            ['change SPF/SIDF settings?', DEFAULT]
        self.param_map['%s_use_spf_ver' % _type] = \
            ['perform SPF/SIDF Verification?', DEFAULT]
        self.param_map['%s_spf_conformance_level' % _type] = \
            ['What Conformance Level would you like to use', DEFAULT, True]
        self.param_map['%s_change_smtp_actions_after_spf' % _type] = \
            ['change SMTP actions taken as result of the SPF verification',
             DEFAULT]
        self.param_map['%s_change_smtp_actions_after_mail_from' % _type] = \
            ['change SMTP actions taken for the MAIL FROM identity', DEFAULT]
        self.param_map['%s_mail_from_none' % _type] = \
            ['should be taken if MAIL FROM check returns None?', DEFAULT, 1]
        self.param_map['%s_mail_from_neutral' % _type] = \
            ['should be taken if MAIL FROM check returns Neutral?', DEFAULT, 1]
        self.param_map['%s_mail_from_temp_error' % _type] = \
            ['should be taken if MAIL FROM check returns TempError?', DEFAULT, 1]
        self.param_map['%s_mail_from_soft_fail' % _type] = \
            ['should be taken if MAIL FROM check returns SoftFail?', DEFAULT, 1]
        self.param_map['%s_mail_from_fail' % _type] = \
            ['should be taken if MAIL FROM check returns Fail?', DEFAULT, 1]
        self.param_map['%s_mail_from_perm_error' % _type] = \
            ['should be taken if MAIL FROM check returns PermError?', DEFAULT, 1]
        self.param_map['%s_change_smtp_actions_for_pra' % _type] = \
            ['change SMTP actions taken for the PRA identity?', DEFAULT]
        self.param_map['%s_pra_none' % _type] = \
            ['should be taken if PRA check returns None?', DEFAULT, 1]
        self.param_map['%s_pra_neutral' % _type] = \
            ['should be taken if PRA check returns Neutral?', DEFAULT, 1]
        self.param_map['%s_pra_temp_error' % _type] = \
            ['should be taken if PRA check returns TempError?', DEFAULT, 1]
        self.param_map['%s_pra_soft_fail' % _type] = \
            ['should be taken if PRA check returns SoftFail?', DEFAULT, 1]
        self.param_map['%s_pra_fail' % _type] = \
            ['should be taken if PRA check returns Fail?', DEFAULT, 1]
        self.param_map['%s_pra_perm_error' % _type] = \
            ['should be taken if PRA check returns PermError?', DEFAULT, 1]
        self.param_map['%s_verification_timeout' % _type] = \
            ['Verification timeout (seconds)', DEFAULT]
        self.param_map['%s_downgrade_pra' % _type] = \
            ['Downgrade PRA verification result', DEFAULT]
        self.param_map['%s_helo_check' % _type] = \
            ['Would you like to have the HELO check performed?', DEFAULT]
        self.param_map['%s_change_smtp_actions_for_helo' % _type] = \
            ['change SMTP actions taken for the HELO identity?', DEFAULT]
        self.param_map['%s_helo_none' % _type] = \
            ['should be taken if HELO check returns None?', DEFAULT, 1]
        self.param_map['%s_helo_neutral' % _type] = \
            ['should be taken if HELO check returns Neutral?', DEFAULT, 1]
        self.param_map['%s_helo_temp_error' % _type] = \
            ['should be taken if HELO check returns TempError?', DEFAULT, 1]
        self.param_map['%s_helo_soft_fail' % _type] = \
            ['should be taken if HELO check returns SoftFail?', DEFAULT, 1]
        self.param_map['%s_helo_fail' % _type] = \
            ['should be taken if HELO check returns Fail?', DEFAULT, 1]
        self.param_map['%s_helo_perm_error' % _type] = \
            ['should be taken if HELO check returns PermError?', DEFAULT, 1]
        self.param_map['%s_change_smtp_actions_for_reject' % _type] = \
            ['change SMTP response settings for the REJECT action?', DEFAULT]
        self.param_map['%s_reject_action_response_code' % _type] = \
            ['What SMTP response code should be returned', DEFAULT]
        self.param_map['%s_reject_action_response_text' % _type] = \
            ['What SMTP response text should be returned (', DEFAULT]
        self.param_map['%s_reject_action_response_text_temp_error' % _type] = \
            ['What SMTP response code should be returned for TempError', DEFAULT]
        self.param_map['%s_reject_action_response_text_temp_error' % _type] = \
            ['What SMTP response text should be returned for TempError', DEFAULT]
        self.param_map['%s_get_smtp_response_code_from_spf_publisher' % _type] = \
            ['get SMTP response text from SPF publisher domain for', DEFAULT]
        self.param_map['%s_enable_envelope_sender_ver' % _type] = \
            ['enable envelope sender verification?', DEFAULT]
        self.param_map['%s_use_envelope_sender_malformed' % _type] = \
            ['specify a custom SMTP response for malformed envelope senders?',
             DEFAULT]
        self.param_map['%s_envelope_sender_malformed_code' % _type] = \
            ['553 is the standard code', DEFAULT]
        self.param_map['%s_envelope_sender_malformed_response' % _type] = \
            ['Enter your custom SMTP response.', DEFAULT]
        self.param_map['%s_use_envelope_sender_not_resolved' % _type] = \
            ['specify a custom SMTP response for envelope sender domains which do not resolve?',
             DEFAULT]
        self.param_map['%s_envelope_sender_not_resolved_code' % _type] = \
            ['451 is the standard code', DEFAULT]
        self.param_map['%s_envelope_sender_not_resolved_response' % _type] = \
            ['custom SMTP response.  Press Enter on a blank line', NO_DEFAULT]
        self.param_map['%s_use_envelope_sender_not_exist' % _type] = \
            ['specify a custom SMTP response for envelope sender domains which do not exist?',
             DEFAULT]
        self.param_map['%s_envelope_sender_not_exist_code' % _type] = \
            ['553 is the standard code. [553]', DEFAULT]
        self.param_map['%s_envelope_sender_not_exist_response' % _type] = \
            ['.  Press Enter on a blank line to finish.', DEFAULT]
        self.param_map['%s_use_domain_exception_table' % _type] = \
            ['use of the domain exception table?', DEFAULT]
        self.param_map['%s_accept_untagged_bounces' % _type] = \
            ['accept untagged bounces?', DEFAULT]
        self.param_map['%s_bounce_profile' % _type] = \
            ['a bounce profile to apply.', DEFAULT]
        self.param_map.update(input_dict or kwargs)

    def configure_scanning_engines(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed to configure antispam, antivirus, vof, sbrs.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        # antispam
        self.param_map['use_as'] = ['use Anti-Spam scanning in the default', NO]
        self.param_map['use_sq'] = ['enable the Spam Quarantine?', YES]
        self.param_map['default_as_engine'] = \
            ['number of the Anti-Spam engine', NO_DEFAULT, True]
        # ['number of the Anti-Spam engine',NO_DEFAULT, True]
        # antivirus
        self.param_map['use_av'] = ['use Anti-Virus scanning in the default', NO]
        self.param_map['default_av_engine'] = \
            ['number of the Anti-Virus engine', NO_DEFAULT, True]
        # anti-malware
        self.param_map['use_amp'] = \
            ['use Anti-Malware scanning in the default', NO]
        # vof
        self.param_map['use_vof'] = ['enable Outbreak Filters?', DEFAULT]
        # senderbase
        self.param_map['share_senderbase_stats'] = \
            ['sharing of limited data with SenderBase?', DEFAULT]
        self.param_map.update(input_dict or kwargs)

    def configure_alerts_and_reports(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed to configure alerts and reports.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        # alerts
        self.param_map['alert_email'] = \
            ['email address(es) to send alerts.', REQUIRED]
        self.param_map['use_autosupport'] = \
            ['enable Cisco IronPort AutoSupport', DEFAULT]
        # reporting
        self.param_map['shcheduled_reports_email'] = \
            ['deliver scheduled reports to.', DEFAULT]
        self.param_map.update(input_dict or kwargs)

    def configure_time_settings(self, input_dict=None, **kwargs):
        """
        Fills in the 'param_map' with parameters
        needed for time settings configuration.
        Does not perform any processing of these parameters,
         just packs them into 'param_map'.
        """
        # timezone
        self.param_map['offset_from_gmt'] = ['your offset from GMT', DEFAULT, 1]
        self.param_map['continent'] = ['choose your continent:', DEFAULT, 1]
        self.param_map['country'] = ['choose your country:', DEFAULT, 1]
        self.param_map['timezone'] = ['choose your timezone:', DEFAULT, 1]
        # time/ntp
        self.param_map['use_ntp'] = ['use NTP to set system time?', DEFAULT]
        self.param_map['ntp_ip_or_host'] = \
            ['hostname or IP address of your NTP server', DEFAULT]
        self.param_map['time'] = ['enter the time', REQUIRED]
        self.param_map.update(input_dict or kwargs)

    def __call__(self, input_dict=None, **kwargs):
        """
        Updates the 'param_map'.
        Processes all parameters gathered during system setup.
        """
        # eula
        self.param_map['license_agreement'] = ['license agreement?', YES]
        self._writeln(self.__class__.__name__)
        use_syssetup = kwargs.pop('use_syssetup', YES)
        self._query_response(use_syssetup)

        timeout_for_query = 15
        idx = self._query('Old passphrase:',
                          self._sub_prompt,
                          timeout=timeout_for_query)
        if idx == 0:
            self._writeln(DUT_ADMIN_PASSWORD)
            # self._writeln(Misc(None, None).get_admin_password(self.dut))
            idx = self._query('Would you like to get a system generated passphrase',
                              self._sub_prompt,
                              timeout=timeout_for_query)
            if idx == 0:
                use_system_generated_password = \
                    kwargs.pop('use_system_generated_password', NO)
                self._writeln(use_system_generated_password)
                if re.match(r'yes|y', str(use_system_generated_password), re.I):
                    idx = self._query('Do you want to proceed with this',
                                      self._sub_prompt,
                                      timeout=timeout_for_query)
                    if idx == 1:
                        proceed_with_system_generated_password = \
                            kwargs.pop('proceed_with_system_generated_password', NO)
                        self._writeln(proceed_with_system_generated_password)
                else:
                    idx = self._query('[]>',
                                      self._sub_prompt,
                                      timeout=timeout_for_query)
                    if idx == 1:
                        new_password = kwargs.pop('new_password', DUT_ADMIN_SSW_PASSWORD)
                        # new_password=kwargs.pop('new_password', \
                        #        Misc(None, None).get_admin_password(self.dut))
                        self._writeln(new_password)
                        idx = self._query('Please enter the new passphrase again:',
                                          self._sub_prompt,
                                          timeout=timeout_for_query)
                        if idx == 1:
                            retype_new_password = \
                                kwargs.pop('retype_new_password', new_password)
                            self._writeln(retype_new_password)
        else:
            self._restart_nosave()
            return None
        # commit
        self.param_map['commit_changes'] = \
            ['commit these changes at this time?', YES]
        self.param_map.update(input_dict or kwargs)
        try:
            return self._process_input(self.param_map)
        except ConfigError as err:
            self._warn(err)
            self._restart_nosave()
