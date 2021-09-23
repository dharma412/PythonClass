#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/system_setup.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
from common.util.misc import Misc
from common.util.systools import SysTools
import re
import os


class SystemSetup(CliKeywordBase):
    """
    Configures system setup parameters.
    The actual command execution is done using `System Setup Run` keyword.
    All other keywords do not interact with CLI, but used to fill in all needed parameters.
    """

    def get_keyword_names(self):
        return ['system_setup_configure_interface',
                'system_setup_configure_router',
                'system_setup_configure_cluster',
                'system_setup_configure_web',
                'system_setup_configure_dns',
                'system_setup_configure_listener',
                'system_setup_configure_hat',
                'system_setup_configure_scanning_engines',
                'system_setup_configure_alerts_and_reports',
                'system_setup_configure_time_settings',
                'system_setup_run', ]

    def system_setup_configure_interface(self, *args):
        """
        Configures interface(s).

        Parameters:
        - `ethernet`: The interface to configure.
        Must be: 'management' or 'data1' or 'data2' ... or 'dataN'
        - `hostname`: Hostname of the IronPort appliance. String. Optional.
        - `enable_ipv4`: Enable IPv4. YES or NO. Default - YES.
        - `ipv4`: The IP address to assign to the interface. Mandatory. String.
        - `netmask`: Netmask to use with ipv4.
        Allows entries as "24", "255.255.255.0" or "0xffffff00". String. Optional.
        - `enable_ipv6`: Enable IPv6. YES or NO. Default - NO.
        - `ipv6`: IPv6 Address. String. Mandatory.
        - `prefix`: Prefix length to use with ipv6. String. Optional.

        Return:
        None

        Examples:
        | System Setup Configure Interface |
        | ... | ethernet=management |
        | ... | enable_ipv4=YES |
        | ... | ipv4=10.92.145.159 |
        | ... | enable_ipv6=YES |
        | ... | ipv6=2620:101:2004:4201::9f |
        | ... | prefix=64 |

        | System Setup Configure Interface |
        | ... | ethernet=data1 |
        | ... | enable=yes |
        | ... | nickname=a001.d1 |
        | ... | enable_ipv4=YES |
        | ... | enable_ipv6=YES |
        | ... | ipv4=10.0.2.6 |
        | ... | ipv6=2620:101:2004:42c0::206 |
        | ... | prefix=61 |

        | System Setup Configure Interface |
        | ... | ethernet=data2 |
        | ... | enable=yes |
        | ... | nickname=a001.d2 |
        | ... | enable_ipv4=YES |
        | ... | enable_ipv6=YES |
        | ... | ipv4=10.1.2.6 |
        | ... | ipv6=2620:101:2004:42e0::206 |
        | ... | prefix=63 |
        """
        _d = self._convert_to_dict(args)
        _ethernet = _d.pop('ethernet', None)
        _err = 'The interface can be one of the: "management", "data1", "data2", ... "dataN"'
        if _ethernet:
            if _ethernet.lower() != 'management' and not _ethernet.lower().startswith('data'):
                raise ValueError(_err)
        else:
            raise ValueError(_err)
        kwargs = {'ethernet': _ethernet.lower()}
        for k in _d.keys():
            kwargs['%s_%s' % (_ethernet, k)] = _d[k]
        self._cli.systemsetup.configure_interface(**kwargs)

    def system_setup_configure_router(self, *args):
        """
        Configures default router(s).

        Parameters:
        - `enable_gw_ipv4`: Configure a default router for your IPv4 network. YES or NO. Default - YES.
        - `gw_ip`: The IP address of the default router (gateway) on your IPv4 network. String.
        - `enable_gw_ipv6`: Configure a default router for your IPv6 network. YES or NO. Default - NO. Optional.
        - `gw_ipv6`: The IP address of the default router (gateway) on your IPv6 network. String. Mandatory.

        Return:
        None

        Examples:
        | System Setup Configure Router |
        | ... | enable_gw_ipv4=YES |
        | ... | gw_ipv4=10.92.145.1 |
        | ... | enable_gw_ipv6=YES |
        | ... | gw_ipv6=2620:101:2004:4201::1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.systemsetup.configure_router(**kwargs)

    def system_setup_configure_cluster(self, *args):
        """
        Configures clustering.

        Parameters:
        - `create_cluster`: Join or create a cluster.
        Options are: 'No, configure as standalone',
                     'Create a new cluster',
                     'Join an existing cluster over SSH',
                     'Join an existing cluster over CCS.'
        - `cluster_name`: The name of the cluster. String.
        - `enable_cluster`: Enable the Cluster Communication Service. YES or NO.
        - `cluster_interface`: The interface on which to enable the Cluster. String.
        - `cluster_port`: The port on which to enable the Cluster. String.
        - `cluster_communicate`: How will hosts communicate with each other: by hostname or by IP address.
        - `cluster_communicate_ip`: The IP address should other machines use to communicate. String.
        - `cluster_machine_ip`: The IP address of a machine in the cluster. String.
        - `cluster_machine_port`: The remote port to connect to. String.
        - `cluster_adm`: The name of an administrator present on the remote machine. String.
        - `cluster_group`: The name of the group to place the machine in. String.
        - `commit_and_continue`: Commit changes now. YES or NO. (Used when creating/joining a cluster).

        Return:
        None

        Examples:
        | System Setup Configure Cluster |
        |... | create_cluster=No, configure as standalone |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.systemsetup.configure_cluster(**kwargs)

    def system_setup_configure_web(self, *args):
        """
        Configures WEB settings.

        Parameters:
        - `use_web_interface`: Enable the web interface on the Management interface. YES or NO. Default - YES.
        - `use_https`: Use secure HTTPS. YES or NO. Default - YES.

        Return:
        None

        Examples:
        | System Setup Configure Web |
        | ... | use_web_interface=YES |
        | ... | use_https=YES |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.systemsetup.configure_web(**kwargs)

    def system_setup_configure_dns(self, *args):
        """
        Configures DNS settings.

        Parameters:
        - `dns_server`: Use the Internet's root DNS servers or own DNS servers.
        Options are: 'Use Internet root DNS servers'(default), 'Use my own DNS servers'.
        - `dns_ip`: The IP address of DNS server (own). String. Mandatory.
        - `use_another_dns_server`: Enter another DNS server. YES or NO. Default - NO.
        - `another_dns_server_ip`: The IP address of another DNS server. String. Mandatory.

        Return:
        None

        Examples:
        | System Setup Configure Dns |
        | ... | dns_server=Use my own DNS servers |
        | ... | dns_ip=10.92.144.4 |
        | ... | use_another_dns_server=NO |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.systemsetup.configure_dns(**kwargs)

    def system_setup_configure_listener(self, *args):
        """
        Configures listener(s).

        Parameters:
        - `listener_type`: type of the listener to configure. Must be 'public' or 'private'. String. Mandatory.
        - `name`: A name of the listener. String. Mandatory.
        - `port`: The TCP port for the listener. String. Mandatory. Appears only if port 25 is in use already.
        - `interface`: An IP interface for this Listener. The name of the configured interface. String.
        - `domain_or_email`: The domain names or specific email addresses to accept mail for. String. Mandatory.
        - `relay_mail_for_int_hosts`: Configure the appliance to relay mail for internal hosts. YES or NO. Default - YES.
        - `use_smtp_route`: Configure SMTP routes for the RAT entry. YES or NO. Default - YES.
        - `destination_server`:Destination mail server mail for RAT entry to be delivered.
        Separate multiple entries with commas. String. Mandatory.
        - `relay_mail`: Specify the systems allowed to relay email through the appliance.
        Hostnames such as "example.com" are allowed. Partial hostnames such as ".example.com" are allowed.
        IP addresses, IP address ranges, and partial IP addresses are allowed. Separate multiple entries with commas.
        - `use_senderbase`: Enable filtering based on SBRS for the listener. YES or NO. Default - YES.
        - `use_rate_limiting`: Enable rate limiting for the listener.YES or NO. Default - YES.
        - `rate_limiting`: The maximum number of recipients per hour to accept from a remote domain. String.

        Return:
        None

        Examples:
        | System Setup Configure Listener |
        | ... | listener_type=public |
        | ... | name=InBoundMail |
        | ... | use_rate_limiting=yes |
        | ... | rate_limiting=77 |
        | ... | interface=a001.d1 |
        | ... | domain_or_email=.qa |
        | ... | use_smtp_route=YES |
        | ... | destination_server=10.92.145.224 |
        | ... | use_senderbase=yes |

        | System Setup Configure Listener |
        | ... | listener_type=private |
        | ... | use_relay_mail_for_int_hosts=YES |
        | ... | name=OutBoundMail |
        | ... | use_rate_limiting=NO |
        | ... | interface=a001.d2 |
        | ... | relay_mail=10. |
        """
        _err = 'The listener type should be: "public" or "private"'
        _d = self._convert_to_dict(args)
        _type = _d.pop('listener_type', None)
        if _type:
            if _type.lower() not in ('public', 'private'):
                raise ValueError(_err)
        else:
            raise ValueError(_err)
        kwargs = {'listener_type': _type.lower()}
        for k in _d.keys():
            kwargs['%s_listener_%s' % (_type, k)] = _d[k]
        self._cli.systemsetup.configure_listener(**kwargs)

    def system_setup_configure_hat(self, *args):
        """
        Configures HAT settings.

        Parameters:
        - `hat_type`: The HAT to configure. Must be: 'public' or 'private'.Mandatory.
        - `change_hat_policy`: Modify the default host access policy. YES or NO.
        - `max_msg_size`: The default maximum message size. String. Optional.
        Add a trailing k for kilobytes, M for megabytes, or no letter for bytes.
        - `max_concurrency`: The maximum number of concurrent connections allowed from a single IP address. String. Optional.
        - `max_msgs_per_conn`: The maximum number of messages per connection. String. Optional.
        - `max_recipients_per_msg`: The maximum number of recipients per message. String. Optional.
        - `override_smtp_banner`: Override the hostname in the SMTP banner. YES or NO. Default - NO.
        - `hostname_in_smtp_banner`: The hostname to use in the SMTP banner, or enter 'NONE'. String.
        - `use_smtp_accept_response`: Specify a custom SMTP acceptance response. YES or NO. Default - NO.
        - `smtp_accept_code`: The SMTP code to use in the response. 220 is the standard code. String. Optional.
        - `smtp_accept_response`: Custom SMTP response.  Press Enter on a blank line to finish. String. Optional.
        - `use_smtp_reject_response`: Specify a custom SMTP rejection response. YES or NO. Default - NO.
        - `smtp_reject_code`: The SMTP code to use in the response.554 is the standard code.
        - `smtp_reject_response`: Custom SMTP response. String..
        - `use_rate_limiting_per_host`: Enable rate limiting per host. YES or NO.
        - `rate_limiting_per_host`: The maximum number of recipients per hour from a remote host. String.
        - `use_smtp_exceed_response`: Specify a custom SMTP limit exceeded response. YES or NO.
        - `smtp_exceed_code`: The SMTP code to use in the response.452 is the standard code.
        - `smtp_exceed_response`: Custom SMTP response. String.
        - `use_rate_limiting_per_envelope_sender`: Enable rate limiting per envelope sender. YES or NO. Default - NO.
        - `rate_limiting_per_envelope_sender`: The maximum number of recipients from an envelope sender.
        - `rate_limiting_per_envelope_sender_interval`: The time interval in minutes for Envelope Sender Rate Limiting. String.
        - `enable_dhap`: Enable Directory Harvest Attack Prevention per host. YES or NO.
        - `dhap_limit`: The maximum number of invalid recipients per hour from a remote host.
        - `dhap_action`: The action to apply when a recipient is rejected due to DHAP. options are: 'Drop' or 'Code'.
        - `use_dhap_smtp_response`: Specify a custom SMTP DHAP response. YES or NO.
        - `dhap_smtp_response_code`: The SMTP code to use in the response. 550 is the standard code.
        - `dhap_smtp_response`: Custom SMTP response. String.
        - `use_senderbase`: Use SenderBase for flow control by default. YES or NO. Default - YES.
        - `enable_antispam`: Enable anti-spam scanning. YES or NO. Default - YES.
        - `enable_antivirus`: Enable anti-virus scanning. YES or NO. Default - YES.
        - `allow_tls`: Allow encrypted TLS connections. Options are: 'No', 'Preferred', 'Required'. String. Optional.
        - `allow_smtp_auth`: Allow SMTP authentication. YES or NO.
        - `require_tls_to_offer_smtp`: Require TLS to offer SMTP. YES or NO.
        - `enable_domainkeys`: Enable DKIM/DomainKeys signing. YES or NO. Default - NO.
        - `enable_dkim`: Enable DKIM verification. YES or NO.
        - `dkim_profile`: The DKIM verification profile to use. String.
        - `change_spf`: Change SPF/SIDF settings. YES or NO.
        - `use_spf_ver`: Perform SPF/SIDF Verification. YES or NO.
        - `spf_conformance_level`: The SPF Conformance Level to use. String.
        - `change_smtp_actions_after_spf`: Change SMTP actions taken as result of the SPF verification. YES or NO.
        - `change_smtp_actions_after_mail_from`: Change SMTP actions taken for the MAIL FROM identity. YES or NO.
        - `mail_from_none`: The action to perform if MAIL FROM check returns None. Options are: 'Accept'(default) or 'Reject'.
        - `mail_from_neutral`: The action to perform if MAIL FROM check returns Neutral. Options are: 'Accept'(default) or 'Reject'.
        - `mail_from_temp_error`: The action to perform if MAIL FROM check returns TempError. Options are: 'Accept'(default) or 'Reject'.
        - `mail_from_soft_fail`: The action to perform if MAIL FROM check returns SoftFail. Options are: 'Accept'(default) or 'Reject'.
        - `mail_from_fail`: The action to perform if MAIL FROM check returns Fail. Options are: 'Accept'(default) or 'Reject'.
        - `mail_from_perm_error`: The action to perform if MAIL FROM check returns PermError. Options are: 'Accept'(default) or 'Reject'.
        - `change_smtp_actions_for_pra`: Change SMTP actions taken for the PRA identity. YES or NO.
        - `pra_none`: The action to perform if PRA check returns None. Options are: 'Accept'(default) or 'Reject'.
        - `pra_neutral`: The action to perform if PRA check returns Neutral. Options are: 'Accept'(default) or 'Reject'.
        - `pra_temp_error`: The action to perform if PRA check returns TempError. Options are: 'Accept'(default) or 'Reject'.
        - `pra_soft_fail`: The action to perform if PRA check returns SoftFail. Options are: 'Accept'(default) or 'Reject'.
        - `pra_fail`: The action to perform if PRA check returns Fail. Options are: 'Accept'(default) or 'Reject'.
        - `pra_perm_error`: The action to perform if PRA check returns PermError. Options are: 'Accept'(default) or 'Reject'.
        - `verification_timeout`: Verification timeout in seconds.
        - `downgrade_pra`: Downgrade PRA verification result. YES or NO.
        - `helo_check`: Perform the HELO check. YES or NO.
        - `change_smtp_actions_for_helo`: Change SMTP actions taken for the HELO identity. YES or NO.
        - `helo_none`: The action to perform if HELO check returns None. Options are: 'Accept'(default) or 'Reject'.
        - `helo_neutral`: The action to perform if HELO check returns Neutral. Options are: 'Accept'(default) or 'Reject'.
        - `helo_temp_error`: The action to perform if HELO check returns TempError. Options are: 'Accept'(default) or 'Reject'.
        - `helo_soft_fail`: The action to perform if HELO check returns SoftFail. Options are: 'Accept'(default) or 'Reject'.
        - `helo_fail`: The action to perform if HELO check returns Fail. Options are: 'Accept'(default) or 'Reject'.
        - `helo_perm_error`: The action to perform if HELO check returns PermError. Options are: 'Accept'(default) or 'Reject'.
        - `change_smtp_actions_for_reject`: Change SMTP response settings for the REJECT action. YES or NO.
        - `reject_action_response_code`: The SMTP response code to return.
        - `reject_action_response_text`: The SMTP response text to return.
        - `reject_action_response_text_temp_error`: The SMTP response code toe return for TempError.
        - `get_smtp_response_code_from_spf_publisher`: Get SMTP response text from SPF publisher. YES or NO.
        - `enable_envelope_sender_ver`: Enable envelope sender verification. YES or NO.
        - `use_envelope_sender_malformed`: Specify a custom SMTP response for malformed envelope senders. YES or NO.
        - `envelope_sender_malformed_code`: The SMTP code to use in the response. 553 is the standard code.
        - `envelope_sender_malformed_response`: Custom SMTP response. String.
        - `use_envelope_sender_not_resolved`: Specify a custom SMTP response for envelope sender domains which do not resolve. YES or NO.
        - `envelope_sender_not_resolved_code`: The SMTP code to use in the response. 451 is the standard code.
        - `envelope_sender_not_resolved_response`: Custom SMTP response. String.
        - `use_envelope_sender_not_exist`: Specify a custom SMTP response for envelope sender domains which do not exist. YES or NO.
        - `envelope_sender_not_exist_code`: The SMTP code to use in the response. 553 is the standard code.
        - `envelope_sender_not_exist_response`: Custom SMTP response. String.
        - `use_domain_exception_table`: Enable use of the domain exception table. YES or NO.
        - `accept_untagged_bounces`: Accept untagged bounces. YES or NO.
        - `bounce_profile`: A bounce profile to use. String.

        Return:
        None

        Examples:
        | System Setup Configure Hat |
        | ... | hat_type=public |
        | ... | change_hat_policy=YES |
        | ... | max_msg_size=10M |
        | ... | max_concurrency=100 |
        | ... | max_msgs_per_conn=10 |
        | ... | max_recipients_per_msg=25 |
        | ... | override_smtp_banner=yes |
        | ... | hostname_in_smtp_banner=boo.qa |
        | ... | use_smtp_accept_response=yes |
        | ... | smtp_accept_code=111 |
        | ... | smtp_accept_response=Welcome\n${EMPTY} |
        | ... | use_smtp_reject_response=yes |
        | ... | smtp_reject_code=112 |
        | ... | smtp_reject_response=Go Away\n${EMPTY} |
        | ... | use_smtp_exceed_response=yes |
        | ... | smtp_exceed_code=123 |
        | ... | smtp_exceed_response=Limit reached\n${EMPTY} |
        | ... | use_rate_limiting_per_host=yes |
        | ... | rate_limiting_per_host=100 |
        | ... | use_rate_limiting_per_envelope_sender=yes |
        | ... | rate_limiting_per_envelope_sender=5 |
        | ... | rate_limiting_per_envelope_sender_interval=10 |
        | ... | enable_dhap=yes |
        | ... | dhap_limit=100 |
        | ... | dhap_action=Drop |
        | ... | use_dhap_smtp_response=yes |
        | ... | dhap_smtp_response_code=114 |
        | ... | dhap_smtp_response=Stopped By DHAP\n${EMPTY} |
        | ... | use_senderbase=yes |
        | ... | enable_antispam=yes |
        | ... | enable_antivirus=yes |
        | ... | enable_domainkeys=yes |
        | ... | enable_dkim=yes |
        | ... | change_spf=yes |
        | ... | use_spf_ver=yes |
        | ... | spf_conformance_level=SIDF strict |
        | ... | change_smtp_actions_after_spf=yes |
        | ... | change_smtp_actions_after_mail_from=yes |
        | ... | mail_from_none=Accept |
        | ... | mail_from_neutral=Accept |
        | ... | mail_from_temp_error=Accept |
        | ... | mail_from_soft_fail=Reject |
        | ... | mail_from_fail=Reject |
        | ... | mail_from_perm_error=Reject |
        | ... | change_smtp_actions_for_pra=yes |
        | ... | pra_none=Accept |
        | ... | pra_neutral=Accept |
        | ... | pra_temp_error=Reject |
        | ... | pra_soft_fail=Reject |
        | ... | pra_fail=Reject |
        | ... | pra_perm_error=Reject |
        | ... | verification_timeout=60 |
        | ... | enable_envelope_sender_ver=yes |
        | ... | envelope_sender_malformed_code=115 |
        | ... | envelope_sender_malformed_response=Malformed\n${EMPTY} |
        | ... | use_envelope_sender_not_resolved=yes |
        | ... | envelope_sender_not_resolved_code=211 |
        | ... | envelope_sender_not_resolved_response=Not Resolved\n${EMPTY} |
        | ... | use_envelope_sender_not_exist=yes |
        | ... | envelope_sender_not_exist_code=212 |
        | ... | envelope_sender_not_exist_response=Not Exist\n${EMPTY} |
        | ... | use_domain_exception_table=yes |
        | ... | accept_untagged_bounces=yes |

        | System Setup Configure Hat |
        | ... | hat_type=private |
        | ... | change_hat_policy=no |
        """
        _err = 'The HAT type should be: "public" or "private"'
        _d = self._convert_to_dict(args)
        _type = _d.pop('hat_type', None)
        if _type:
            if _type.lower() not in ('public', 'private'):
                raise ValueError(_err)
        else:
            raise ValueError(_err)
        kwargs = {'hat_type': _type.lower()}
        for k in _d.keys():
            kwargs['%s_%s' % (_type, k)] = _d[k]
        self._cli.systemsetup.configure_hat(**kwargs)

    def system_setup_configure_scanning_engines(self, *args):
        """
        Configures scanning engines: antivirus, antispam, VOF.

        Parameters:
        - `use_as`: Use Anti-Spam scanning in the default Incoming Mail policy. YES or NO.
        - `use_sq`: Enable the Spam Quarantine. YES or NO.
        - `default_as_engine`: The Anti-Spam engine to use on the default Incoming Mail policy. String
        - `use_av`: Use Anti-Virus scanning in the default Incoming and Outgoing Mail policies. YES or NO.
        - `default_av_engine`: The Anti-Virus engine to use on the default Incoming Mail policy. String.
        - 'use_amp': Use Advanced Malware Engine to use on the default Incoming Mail Policy.
        - `use_vof`: Enable Outbreak Filters. YES or NO.
        - `share_senderbase_stats`: Allow the sharing of limited data with SenderBase. YES or NO.

        Return:
        None

        Examples:
        | System Setup Configure Scanning Engines |
        | ... | use_as=YES |
        | ... | default_as_engine=IronPort Anti-Spam |
        | ... | use_av=YES |
        | ... | default_av_engine=Sophos Anti-Virus |
        | ... | use_amp=YES |
        | ... | use_vof=YES |
        | ... | share_senderbase_stats=YES |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.systemsetup.configure_scanning_engines(**kwargs)

    def system_setup_configure_alerts_and_reports(self, *args):
        """
        Configures alerts and reports.

        Parameters:
        - `alert_email`: The email address(es) to send alerts to. Separate multiple addresses with commas.
        - `use_autosupport`: Enable Cisco IronPort AutoSupport. YES or NO.
        - `receive_weekly_reports`: Receive weekly AutoSupport reports. YES or NO.
        - `shcheduled_reports_email`: The email address(es) to deliver scheduled reports to.
        Leave blank to only archive reports on-box. Separate multiple addresses with commas.

        Return:
        None

        Examples:
        | System Setup Configure Alerts And Reports |
        | ... | alert_email=user1@mail.qa, user2@mail.qa, user3@mail.qa |
        | ... | use_autosupport=NO |
        | ... | shcheduled_reports_email=user1@mail.qa, user2@mail.qa |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.systemsetup.configure_alerts_and_reports(**kwargs)

    def system_setup_configure_time_settings(self, *args):
        """
        Configures time settings.

        Parameters:
        - `offset_from_gmt`: The offset from GMT. String.
        - `continent`: Configure system time settings. Choose continent. String.
        - `country`: The country. String.
        - `timezone`: The timezone. String.
        - `use_ntp`: Use NTP to set system time. YES or NO
        - `ntp_ip_or_host`: The hostname of the ntp server. String. Optional.
        - `time`: Use NTP to set system time. YES or NO.

        Return:
        None

        Examples:
        | System Setup Configure Time Settings |
        | ... | continent=Europe |
        | ... | country=Ukraine |
        | ... | timezone=most locations (Kiev) |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.systemsetup.configure_time_settings(**kwargs)

    def system_setup_run(self, *args):
        """
        Runs systemsetup.

        Parameters:
        - `old_password`: Default value is 'ironport'. String. Optional.
        - `use_system_generated_password`: Yes or No. Default - No. Optional.
        - `proceed_with_system_generated_password`: Yes or No. Default - No. Optional.
        - `new_password`: Default value is the same as 'old_password'. String. Optional.
        - `retype_new_password`: Default value is the same as 'new_password'. String. Optional.
        - `license_agreement`: YES or NO. Default - YES. Optional.
        - `use_syssetup`: run system setup or not. YES or NO. YES by default.
        - `license_file`: Absolute path of the license file . Default is vesalicense.xml

        All other parameters needed for 'systemsetup' are gathered
        with other keywords from this module.

        Return:
        None

        Examples:
        | System Setup Run |
        | ... | old_password=ironport |
        | ... | new_password=12345678 |
        | ... | commit_changes=YES |
        | System Setup Run |
        | ... | old_password=ironport |
        | ... | use_system_generated_password=Yes|
        | ... | proceed_with_system_generated_password=Yes |
        """
        kwargs = self._convert_to_dict(args)
        license_file = kwargs.pop('license_file', None)

        self.isVirtual = SysTools(self.dut, self.dut_version). \
            _is_dut_a_virtual_model()
        if self.isVirtual:
            self._add_license(license_file=license_file)
        self._cli.systemsetup(**kwargs)

    def _add_license(self, license_file=None):
        cli = SysTools(self.dut, self.dut_version)._get_cli()
        if not license_file:
            license_file = os.environ["SARF_HOME"] + os.sep + \
                           os.path.join('tests', 'testdata', 'virtual', 'vesalicense.xml')
        filename = license_file.rpartition('/')[2]
        destination = os.sep + os.path.join('data', 'pub', 'configuration') + \
                      os.sep + filename
        Misc(self.dut, self.dut_version).copy_file_to_dut \
            (license_file, destination)
        license_status = cli.showlicense()
        self._info('Output from showicense')
        self._info(license_status)
        if not re.search('No License Installed', license_status):
            return
        self._info('Adding license during SystemSetup:')
        licensetext = cli.loadlicense()._load_license_from_file \
            (filename=filename)
        self._info('Output from loadlicense command(SSW)')
        self._info(licensetext)
