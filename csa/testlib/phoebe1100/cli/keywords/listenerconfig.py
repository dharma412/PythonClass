#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/listenerconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT
from sal.containers.yesnodefault import YES, NO
import ast


class Listenerconfig(CliKeywordBase):
    """
    cli -> listenerconfig

    Class designed to provide keywords for ESA listenerconfig command.
    """

    def get_keyword_names(self):
        return ['listenerconfig_new',
                'listenerconfig_edit_name',
                'listenerconfig_edit_interface',
                'listenerconfig_edit_limits',
                'listenerconfig_edit_callahead',
                'listenerconfig_edit_bounceconfig',
                'listenerconfig_edit_setipmm',
                'listenerconfig_edit_ldapaccept',
                'listenerconfig_edit_ldaprouting',
                'listenerconfig_edit_ldapgroup',
                'listenerconfig_edit_smtpauth',
                'listenerconfig_edit_certificate',
                'listenerconfig_edit_setup_defaultdomain',
                'listenerconfig_edit_setup_received',
                'listenerconfig_edit_setup_cleansmtp',
                'listenerconfig_edit_setup_senderbase',
                'listenerconfig_edit_setup_footer',
                'listenerconfig_edit_setup_address_type',
                'listenerconfig_edit_setup_address_eightbituser',
                'listenerconfig_edit_setup_address_eightbitdomain',
                'listenerconfig_edit_setup_address_partial',
                'listenerconfig_edit_setup_address_source',
                'listenerconfig_edit_setup_address_literal',
                'listenerconfig_edit_setup_address_special',
                'listenerconfig_edit_hostaccess_new',
                'listenerconfig_edit_hostaccess_edit_policy',
                'listenerconfig_edit_hostaccess_edit_sendergroup_new',
                'listenerconfig_edit_hostaccess_edit_sendergroup_delete',
                'listenerconfig_edit_hostaccess_edit_sendergroup_move',
                'listenerconfig_edit_hostaccess_edit_sendergroup_country_add',
                'listenerconfig_edit_hostaccess_edit_sendergroup_country_delete',
                'listenerconfig_edit_hostaccess_edit_sendergroup_country_print',
                'listenerconfig_edit_hostaccess_edit_sendergroup_policy',
                'listenerconfig_edit_hostaccess_edit_sendergroup_Print',
                'listenerconfig_edit_hostaccess_edit_sendergroup_rename',
                'listenerconfig_edit_hostaccess_delete',
                'listenerconfig_edit_hostaccess_move',
                'listenerconfig_edit_hostaccess_default',
                'listenerconfig_edit_hostaccess_Print',
                'listenerconfig_edit_hostaccess_Import',
                'listenerconfig_edit_hostaccess_export',
                'listenerconfig_edit_hostaccess_reset',
                'listenerconfig_edit_rcptaccess_new',
                'listenerconfig_edit_rcptaccess_edit',
                'listenerconfig_edit_rcptaccess_delete',
                'listenerconfig_edit_rcptaccess_Print',
                'listenerconfig_edit_rcptaccess_Import',
                'listenerconfig_edit_rcptaccess_export',
                'listenerconfig_edit_rcptaccess_clear',
                'listenerconfig_edit_masquerade_new',
                'listenerconfig_edit_masquerade_delete',
                'listenerconfig_edit_masquerade_Print',
                'listenerconfig_edit_masquerade_Import',
                'listenerconfig_edit_masquerade_export',
                'listenerconfig_edit_masquerade_config',
                'listenerconfig_edit_masquerade_clear',
                'listenerconfig_edit_domainmap_new',
                'listenerconfig_edit_domainmap_edit',
                'listenerconfig_edit_domainmap_delete',
                'listenerconfig_edit_domainmap_Print',
                'listenerconfig_edit_domainmap_Import',
                'listenerconfig_edit_domainmap_export',
                'listenerconfig_edit_domainmap_clear',
                'listenerconfig_setup',
                'listenerconfig_delete',
                'listenerconfig_get_info',
                'listenerconfig_find_listeners',
                ]

    def listenerconfig_get_info(self):
        """
        The information about listeners configured.

        CLI command: listenerconfig

        *Parameters*:
        None

        *Examples*:
        | ${info}= | Listenerconfig Get Info |
        | Log | ${info} |
        | Log List | ${info.public} |
        | Log List | ${info.private} |
        | ${pub_listener}= | Get From List | ${info.public} | 0 |
        | Log Dictionary | ${pub_listener} |
        | Log | Public Listener IPv4: ${pub_listener.ipv4} |
        | Log | Public Listener Port: ${pub_listener.port} |
        | Log | Public Listener name: ${pub_listener.name} |

        *Return*:
        ListenerInfo class.

        You can refer to these attributes of ListenerInfo class:
        | *Attribute* | *Type* | *Type of listener* |
        | all | List | All listeners |
        | public | List | Public listeners |
        | private | List | Private listeners |
        | black  | List | Blackhole listeners |

        Each entry in all these lists is CfgHolder(dictionary).
        """
        return self._cli.listenerconfig().get_listeners_info()

    def listenerconfig_find_listeners(self, *args):
        """
        Fetch the information about configured listeners using search criteria.
        Pass arguments you are interested in only and be sure to skip the rest.
        All arguments are case sensitive.

        CLI command: listenerconfig

        *Parameters*:
        - `name`: Find by name. Defaults to None.
        - `interface`: Find by interface. Defaults to None.
        - `ipv4`: Find by IP v4 address. Defaults to None.
        - `ipv6_address`: Find by IP v6 address. Defaults to None.
        - `type`: Find by type. Defaults to None.
        - `protocol`: Find by protocol. Defaults to None.
        - `port`: Find by port. Defaults to None.
        - `scope`: Find by scope. Either 'Public', 'Private' or 'Black'. Defaults to None.

        *Examples*:
        | ${public_listeners}= | Listenerconfig Find Listeners |
        | ... | scope=Public |
        | Log List | ${public_listeners} |
        | ${public_listener}= | Get From List | ${public_listeners} | 0 |
        | Log | IPv4: ${public_listener.ipv4} |

        *Return*:
        List.
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.listenerconfig(). \
            get_listeners_info().findlisteners(**kwargs)

    def listenerconfig_new(self, *args):
        """
        This will create a new listener interface

        listenerconfig -> new

        *Parameters*
        - `injector_type`: The type of listener you want to create
        - `injector_name`: Name for this listener
        - `ip_interface`: IP interface for this Listener
        - `qtodisk`: Messages to be queued onto disk? Either 'yes' or 'no'
        - `mail_protocol`: Select protocol.
        - `mail_port`: TCP port for this listener
        - `relay_hosts`: Systems allowed to relay email through the ESA.
          Hostnames such as "example.com" are allowed. Partial hostnames such
          as ".example.com" are allowed. IP addresses, IP address ranges,
          and partial IP addresses are allowed. Separate multiple entries
          with commas.
        - `accept_for_addresses`: domain names or specific email addresses
          you want to accept mail for
        - `enable_sbrs`: Enable filtering based on SenderBase Reputation
          Service (SBRS) Scores for this listener. Either 'yes' or 'no'
        - `rate_limiting_bool`: Enable rate limiting for this listener
          Either 'yes' or 'no'
        - `default_max_rcpts_per_hour`: Maximum number of recipients per hour
          to accept from a remote domain
        - `change_default_hat_bool`: Change the default host access policy.
          Either 'yes' or 'no'
        - `bounce_profile`: specify bounce profile to be used
        - `max_msg_size`: Maximum message size. Add a trailing k for kilobytes,
          M for megabytes, or no letter for bytes
        - `max_concurrency`: Maximum number of concurrent connections allowed
          from a single IP address
        - `mmps`: Maximum number of messages per connection
        - `mrpm`: Maximum number of recipients per message
        - `use_override_hostname`: Override the hostname in the SMTP banner.
          Either 'yes' or 'no'
        - `modify_acpt_banner`: Specify a custom SMTP acceptance response.
          Either 'yes' or 'no'
        - `modify_reject_banner`: Specify a custom SMTP rejection response.
          Either 'yes' or 'no'
        - `enable_mrph`: Enable rate limiting per host
          Either 'yes' or 'no'
        - `mrph`: Maximum number of recipients per hour from a remote host
        - `modify_mrph_banner`: Specify a custom SMTP limit exceeded response
          Either 'yes' or 'no'
        - `enable_sb`: Use SenderBase for flow control by default.
          Either 'yes' or 'no'
        - `enable_host_grouping`: Group hosts by the similarity of their
          IP addresses? . Either 'yes' or 'no'
        - `spam_check`: Enable anti-spam scanning
        - `virus_check`: Enable anti-virus scanning
        - `tls`: Allow encrypted TLS connections
        - `dk_signing`: Enable DKIM/DomainKeys signing. Either 'yes' or 'no'
        - `smime_signing`: Would you like to enable S/MIME gateway decryption/verification. Either 'yes' or 'no'
        - `smime_publickeyharvest`: Would you like to enable S/MIME Public Key Harvesting. Either 'yes' or 'no'
        - `harvest_certificate`: Would you like to harvest certificate on verification failure. Either 'yes' or 'no'
        - `harvest_updatedcert`: Would you like to harvest updated certificate. Either 'yes' or 'no'
        - `smime_signature`: Select the appropriate operation for the S/MIME signature processing, 'Number'
        - `sender_vrfy`: Enable envelope sender verification.
          Either 'yes' or 'no'
        - `domain_exception`: Enable use of the domain exception table
          Either 'yes' or 'no'
        - `untagged_bounces`: Accept untagged bounces. Either 'yes' or 'no'

        *Examples*
         | Listenerconfig New | injector_type=2 | ip_interface=2 |
         | ... | injector_name=TestInt1 | mail_port=6132 |
         | ... | accept_for_addresses=.ibqa | rate_limiting_bool=no |
         | ... | change_default_hat_bool=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.listenerconfig().new(**kwargs)

    def listenerconfig_setup(self, *args):
        """
        This can be used to change global settings of listenerconfig

        listenerconfig -> setup

        *Parameters*
        - `max_concurrency`: Global limit for concurrent connections to be
          allowed across all listeners
        - `max_tls_concurrency`: Global limit for concurrent TLS connections
          to be allowed across all listeners
        - `max_headers`: Maximum number of message header lines.
          0 indicates no limit
        - `inj_ctrl_rate`: Rate at which injection control counters are reset
        - `inbound_conn_timeout`: Timeout for unsuccessful inbound connections
        - `inbound_conn_max_time`: Maximum connection time for
          inbound connections
        - `received_hostname`: Select hostname which should have Received:
          header stamped
        - `add_msg_id_header`: Add a Message-ID header to all incoming messages.
          Either 'yes' or 'no'
        - `msg_rcpt_level_reject`: Reject connections with a HAT REJECT policy
          at the message recipient level for more detailed logging of rejected
          mail. By default connections with a HAT REJECT policy will be closed
          with a banner message at the start of the SMTP conversation
          Either 'yes' or 'no'
        - `sb_cache`: Allow senderbase to determine cache time.
          Either 'yes' or 'no'
        - `sb_cache_time`: specify cache time if 'sb_cache' value is 'no'

        *Examples*
        | Listenerconfig Setup | max_concurrency=500 | max_tls_concurrency=300 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.listenerconfig().setup(**kwargs)

    def listenerconfig_delete(self, name, confirm='yes'):
        """
        This will delete listener interface.

        listenerconfig -> delete

        *Parameters*
        - `name`: Name of the interface
        - `confirm`: Confirm deletion. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Delete | TestInt1 | confirm=yes |
        """
        self._cli.listenerconfig().delete(name, self._process_yes_no(confirm))

    def listenerconfig_edit_name(self, intf_name, new_name, confirm='yes'):
        """
        Edit the name of the listener interface.

        listenerconfig -> edit -> name

        *Parameters*
        - `intf_name`: Name of the listener interface whose name is to be
          changed
        - `new_name`: New name of this listener interface
        - `confirm`: Confirm deletion. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Name | TestInt1 | NewTestInt1 | confirm=yes |
        """
        self._cli.listenerconfig().edit(name=intf_name). \
            name(new_name, self._process_yes_no(confirm))

    def listenerconfig_edit_interface(self, intf_name, *args):
        """
        Change the interface of the listener

        listenerconfig -> edit -> interface

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `ip_interface`: IP interface for this Listener
        - `mail_protocol`: Select protocol.
        - `mail_port`: TCP port for this listener

        *Examples*
        | Listenerconfig Edit Interface | TestInt1 | mail_port=6135 |
        | ... | ip_interface=2 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.listenerconfig().edit(name=intf_name). \
            interface(**kwargs)

    def listenerconfig_edit_limits(self, intf_name, *args):
        """
        Change the injection limits of the listener

        listenerconfig -> edit -> limits

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `max_connection`: maximum concurrent connections allowed for this
          listener
        - `qsize`: TCP listen queue size

        *Examples*
        |  Listenerconfig Edit Limits | TestInt1 | max_connection=300 |
        | ... | qsize=50 |
        """
        kwargs = self._convert_to_dict(args)
        arg = {'max_connection': '', 'qsize': ''}

        for key in kwargs.keys():
            if key in arg.keys():
                arg[key] = kwargs[key]
                del kwargs[key]
        self._cli.listenerconfig().edit(name=intf_name). \
            limits(arg['max_connection'], arg['qsize'])

    def listenerconfig_edit_callahead(self, intf_name, enable_bool,
                                      profile_name=DEFAULT):
        """
        Change the callahead settings of the listener

        listenerconfig -> edit -> callahead

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `enable_bool`: Enable. Either 'yes' or 'no'
        - `profile_name`: Name of the profile

        *Examples*
        | Listenerconfig Edit Callahead | TestInt1 | yes |
        | ... | profile_name=testing |
        """
        self._cli.listenerconfig().edit(name=intf_name). \
            callahead(self._set_yes_no_object(enable_bool), profile_name)

    def listenerconfig_edit_bounceconfig(self, intf_name, bounce_profile,
                                         profile_name=None):
        """
        This is used to choose the bounce profile to use for messages injected
        on this listener

        listenerconfig -> edit -> bounceconfig

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `bounce_profile`: Use Default or to use New Profile.
          values are 'Default' & 'New Profile'
        - `profile_name`: Name of the new bounce profile

        *Examples*
        | Listenerconfig Edit Bounceconfig | TestInt1 | New Profile |
        | ... | test_name |
        """
        self._cli.listenerconfig().edit(name=intf_name). \
            bounceconfig(bounce_profile, profile_name)

    def listenerconfig_edit_setipmm(self, intf_name, enable_bool):
        """
        This is used to choose the bounce profile to use for messages injected
        on this listener

        listenerconfig -> edit -> bounceconfig

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `enable_bool`: Enable. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Setipmm | TestInt1 | yes |
        """
        self._cli.listenerconfig().edit(name=intf_name).setipmm(enable_bool)

    def listenerconfig_edit_ldapaccept(self, intf_name, *args):
        """
        This is used to configure an LDAP query to determine whether a recipient
        address should be accepted or bounced/dropped

        listenerconfig -> edit -> ldapaccept

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `query`: Select Recipient Acceptance Query
        - `place`: Specify if recipient acceptance query be done in the work
          queue or during the SMTP conversation
        - `ldap_timeout_action`: Select action which should be taken when there
          is an LDAP server timeout
        - `ldap_response`: Modify the LDAP server timeout response
          Either 'yes' or 'no'
        - `ldap_response_code`: Specify the SMTP code to use in the response
        - `custom_response`: Enter your custom SMTP response
        - `action`: Specify if the recipient acceptance query should drop
          recipients or bounce them
        - `dhap_response`: Modify DHAP response. Either 'yes' or 'no'
        - `dhap_response_code`: Specify the DHAP code to use in the response
        - `drop`: drop the connection if the Directory Harvest Attack Prevention
          threshold is reached. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Ldapaccept | TestInt1 | query=2 | place=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.listenerconfig().edit(name=intf_name). \
            ldapaccept(**kwargs)

    def listenerconfig_edit_ldaprouting(self, intf_name, query_type):
        """
        This is used to configure an LDAP query to reroute messages

        listenerconfig -> edit -> ldaprouting

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `query_type`: Select Routing Query

        *Examples*
        | Listenerconfig Edit Ldaprouting | TestInt1 | None |
        """
        self._cli.listenerconfig().edit(name=intf_name).ldaprouting(query_type)

    def listenerconfig_edit_ldapgroup(self, intf_name, query_type):
        """
        This is used to configure an LDAP query to determine whether a sender
        or recipient is in a specified group

        listenerconfig -> edit -> ldapgroup

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `query_type`: Select Group Query

        *Examples*
        | Listenerconfig Edit Ldapgroup | TestInt1 | None |
        """
        self._cli.listenerconfig().edit(name=intf_name).ldapgroup(query_type)

    def listenerconfig_edit_smtpauth(self, intf_name, enable_bool,
                                     profile_name):
        """
        This is used to configure SMTP Auth

        listenerconfig -> edit -> smtpauth

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `enable_bool`: Enable. Either 'yes' or 'no'
        - `profile_name`: Specify the profile name

        *Examples*
        | Listenerconfig Edit Smtpauth | TestInt1 | yes | temp_profile |
        """
        self._cli.listenerconfig().edit(name=intf_name). \
            smtpauth(self._set_yes_no_object(enable_bool), profile_name)

    def listenerconfig_edit_certificate(self, intf_name, name):
        """
        This is used to choose the certificate

        listenerconfig -> edit -> certificate

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Certificate name

        *Examples*
        | Listenerconfig Edit Certificate | TestInt1 | imported_cert |
        """
        self._cli.listenerconfig().edit(name=intf_name).certificate(name)

    def listenerconfig_edit_setup_defaultdomain(self, intf_name,
                                                default_domain, partial_domain_bool):
        """
        This is used to configure default domain name for this listener
        interface

        listenerconfig -> edit -> setup -> defaultdomain

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `default_domain`: Default domain to be used for email addresses
          without a fully qualified domain name
        - `partial_domain_bool`: Reject addresses that only have a partial
          domain. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Setup Defaultdomain | TestInt1 | domain.com | no |
        | Listenerconfig Edit Setup Defaultdomain | TestInt1 | delete | yes |
        """
        self._cli.listenerconfig().edit(name=intf_name). \
            setup().defaultdomain(default_domain, partial_domain_bool)

    def listenerconfig_edit_setup_received(self, intf_name,
                                           enable_received_header_bool):
        """
        This is used to specify whether or not a Received: header should be
        added

        listenerconfig -> edit -> setup -> received

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `enable_received_header_bool`: Enable. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Setup Received | TestInt1 | yes |
        """
        self._cli.listenerconfig().edit(name=intf_name). \
            setup().received(enable_received_header_bool)

    def listenerconfig_edit_setup_cleansmtp(self, intf_name,
                                            clean_smtp, confirm_continue=YES):
        """
        This is used to specify whether or not to repair bare CR and LF
        in messages

        listenerconfig -> edit -> setup -> cleansmtp

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `cleansmtp`: Select the behavior you want for messages that contain
          invalid SMTP character sequences
        - `confirm_continue`: Confirm continue. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Setup Cleansmtp | TestInt1 | Clean |
        """
        self._cli.listenerconfig().edit(name=intf_name). \
            setup().cleansmtp(clean_smtp, confirm_continue)

    def listenerconfig_edit_setup_senderbase(self, intf_name, *args):
        """
        This is used to set SenderBase options

        listenerconfig -> edit -> setup -> senderbase

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `enable_sbrs`: Enable SenderBase Reputation Filters and IP Profiling
          support. Either 'yes' or 'no'
        - `timeout_sbrs`: timeout, in seconds, for SenderBase queries
        - `timeout_sbrs_perconn`: timeout, in seconds, for all SenderBase
          queries per connection

        *Examples*
        | Listenerconfig Edit Setup Senderbase | TestInt1 | enable_sbrs=yes |
        | ... | timeout_sbrs_perconn=6 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.listenerconfig().edit(name=intf_name). \
            setup().senderbase(**kwargs)

    def listenerconfig_edit_setup_footer(self, intf_name, footer_rsrc_bool,
                                         footer_rsrc=None, remove_footer_rsrc_bool=None):
        """
        This provided configure options to add a footer to every message

        listenerconfig -> edit -> setup -> footer

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `footer_rsrc_bool`: Attach a footer to all mail on this listener.
          Either 'yes' or 'no'
        - `footer_rsrc`: Specify the footer to attach to all mail messages

        *Examples*
        | Listenerconfig Edit Setup Footer | TestInt1 | yes | footer_rsrc=foot |
        """
        self._cli.listenerconfig().edit(name=intf_name). \
            setup().footer(footer_rsrc_bool, footer_rsrc, remove_footer_rsrc_bool)

    def listenerconfig_edit_setup_address_type(self, intf_name,
                                               address_parser_type):
        """
        This is used to configure email address restrictions.This is used to
        choose "loose" or "strict" parsing

        listenerconfig -> edit -> setup -> address -> type

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `address_parser_type`: Specify the parsing type to be used

        *Examples*
        | Listenerconfig Edit Setup Address Type | TestInt1 | 1 |
        """
        self._cli.listenerconfig().edit(name=intf_name).setup().address(). \
            type(address_parser_type)

    def listenerconfig_edit_setup_address_eightbituser(self, intf_name,
                                                       eight_bit_user_bool):
        """
        This is used to configure email address restrictions.This is used to
        set whether to allow 8-bit usernames

        listenerconfig -> edit -> setup -> address -> eightbituser

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `eight_bit_user_bool`: Allow 8-bit usernames. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Setup Address Eightbituser | TestInt1 | yes |
        """
        self._cli.listenerconfig().edit(name=intf_name).setup().address(). \
            eightbituser(eight_bit_user_bool)

    def listenerconfig_edit_setup_address_eightbitdomain(self, intf_name,
                                                         eightbitdomain):
        """
        This is used to configure email address restrictions.This is used to
        set whether to allow 8-bit domain names

        listenerconfig -> edit -> setup -> address -> eightbitdomain

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `eightbitdomain`: Allow 8-bit domain names. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Setup Address Eightbitdomain | TestInt1 | yes |
        """
        self._cli.listenerconfig().edit(name=intf_name).setup().address(). \
            eightbitdomain(eightbitdomain)

    def listenerconfig_edit_setup_address_partial(self, intf_name,
                                                  partial_domain_bool, confirm_enable_partial_domain_bool=NO,
                                                  confirm_disable_partial_domain_bool=NO):
        """
        This is used to configure email address restrictions.This is used to
        set whether or not to allow partial domain names

        listenerconfig -> edit -> setup -> address -> partial

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `partial_domain_bool`: Allow partial domains in email addresses.
          Either 'yes' or 'no'
        - `confirm_enable_partial_domain_bool`: confirm enable.
          Either 'yes' or 'no'
        - `confirm_disable_partial_domain_bool`: confirm disable.
          Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Setup Address Partial | TestInt1 | yes |
        | ... | confirm_enable_partial_domain_bool=yes |
        | Listenerconfig Edit Setup Address Partial | TestInt1 | no |
        | ... | confirm_disable_partial_domain_bool=no |
        """
        self._cli.listenerconfig().edit(name=intf_name).setup().address(). \
            partial(partial_domain_bool, confirm_enable_partial_domain_bool,
                    confirm_disable_partial_domain_bool)

    def listenerconfig_edit_setup_address_source(self, intf_name,
                                                 source_routing):
        """
        This is used to configure email address restrictions.This is used to
        set how to handle email addresses with source routing

        listenerconfig -> edit -> setup -> address -> source

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `source_routing`: Specify how to handle source routing in email
          addresses

        *Examples*
        | Listenerconfig Edit Setup Address Source | TestInt1 | 1 |
        """
        self._cli.listenerconfig().edit(name=intf_name).setup().address(). \
            source(source_routing)

    def listenerconfig_edit_setup_address_literal(self, intf_name,
                                                  accept_unknown_literal):
        """
        This is used to configure email address restrictions.This is used to
        set how unknown address literals are handled

        listenerconfig -> edit -> setup -> address -> literal

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `accept_unknown_literal`: Specify how to handle non-IPv4 address
          literal types

        *Examples*
        | Listenerconfig Edit Setup Address Literal | TestInt1 | 2 |
        """
        self._cli.listenerconfig().edit(name=intf_name).setup().address(). \
            literal(accept_unknown_literal)

    def listenerconfig_edit_setup_address_special(self, intf_name,
                                                  reject_username_chars):
        """
        This is used to configure email address restrictions.This is used to
        set special characters to reject in usernames

        listenerconfig -> edit -> setup -> address -> special

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `reject_username_chars`: Specify the characters that you wish to
          reject from usernames

        *Examples*
        | Listenerconfig Edit Setup Address Special | TestInt1 | %!: |
        """
        self._cli.listenerconfig().edit(name=intf_name).setup().address(). \
            special(reject_username_chars)

    def listenerconfig_edit_hostaccess_new(self, intf_name, entry_type,
                                           new_name, host_list, access_behavior, *args):
        """
        This is used to add a new entry to the Host Access Table

        listenerconfig -> edit -> hostaccess -> new

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `entry_type`: Specify if 'sender group' or 'policy' is to be added.
        - `new_name`: Name for this sender group/policy
        - `host_list`: senders to add to this sender group/policy
        - `access_behavior': behavior for this entry
        - `hat_change_bool`: Change the host access policy. Either 'yes' or 'no'

        *Host Access Parameters which can be specified if `hat_change_bool` is
        'yes'*
        - `max_msg_size`: Default maximum message size. Add a trailing k for
           kilobytes, M for megabytes, or no letter for bytes
        - `max_concurrency`: Maximum number of concurrent connections allowed
          from a single IP address
        - `mmps`: maximum number of messages per connection
        - `mrpm`: maximum number of recipients per message
        - `use_override_hostname`: override the hostname in the SMTP banner.
          Either 'yes' or 'no'
        - `override_hostname`: specify the hostname to use in the SMTP banner
        - `modify_smtp_banner`: enable custom SMTP response.
          Either 'yes' or 'no'
        - `modify_acpt_banner`: enable custom SMTP acceptance response.
          Either 'yes' or 'no'
        - `acpt_banner_code`: specify custom SMTP acceptance banner code
        - `modify_reject_banner`: enable custom SMTP rejection response
          Either 'yes' or 'no'
        - `reject_banner_code`: specify a custom SMTP rejection banner code
        - `enable_dhap`: Enable Directory Harvest Attack Prevention per host
          Either 'yes' or 'no'
        - `dhap_limit`: maximum number of invalid recipients per hour from a
          remote host
        - `dhap_action`: specify action to apply when a recipient is rejected
        - `dhap_SMTP_response`: enable custom SMTP DHAP response
          Either 'yes' or 'no'
        - `dhap_SMTP_code`: specify a custom SMTP DHAP response code
        - `enable_mrph`: Enable maximum number of recipients per host.
          Either 'yes' or 'no'
        - `mrph`: specify maximum number of recipients per host from a remote
          host
        - `modify_mrph_banner`: enable custom SMTP limit exceeded response
          Either 'yes' or 'no'
        - `mrph_banner_code`: specify custom SMTP limit exceeded response code
        - `enable_mrpes`: Enable maximum number of receipients per envelope
          sender. Either 'yes' or 'no'
        - `mrpes`: maximum number of recipients from an envelope sender
        - `mrpes_interval`: interval in minutes for Envelope Sender Rate
          Limiting
        - `exceed_smtp_limit`: enable custom SMTP limit exceeded response
        - `smtp_code`: custom SMTP code to use in response
        - `smtp_response`: specify custom SMTP response
        - `addr_list`: Address List to define exceptions
        - `enable_sb`: use SenderBase for flow control by default.
          Either 'yes' or 'no'
        - `enable_host_grouping`: enable grouping of hosts by the similarity
          of their IP addresses. Either 'yes' or 'no'
        - `significant_bits`: number of bits of IP address to treat as
          significant
        - `delayed_sb`: specify if the Ironport applicance need to fetch the
          incoming address (for SenderBase) from a trusted relay
        - `delayed_sb_header`: specify the header name containing the IP address
        - `spam_check`: enable anti-spam scanning. Either 'yes' or 'no'
        - `virus_check`: enable anti-virus scanning. Either 'yes' or 'no'
        - `tls`: allow encrypted TLS connections. Either 'yes' or 'no'
        - addr_list_tls`: address list to enforce TLS
        - `really_use_demo_cert_bool`: use demo certificate to test TLS.
          Either 'yes' or 'no'
        - `smtpauth_allow`: allow SMTP authentication. Choose from the following
          | 1 | No |
          | 2 | Preferred |
          | 3 | Required |
        - `smtpauth_requiretls`: specify if TLS is Require to offer SMTP
          authentication. Either 'yes' or 'no'
        - `dk_signing`: enable DKIM/DomainKeys signing. Either 'yes' or 'no'
        - `smime_signing`: Would you like to enable S/MIME gateway decryption/verification. Either 'yes' or 'no'
        - `smime_publickeyharvest`: Would you like to enable S/MIME Public Key Harvesting. Either 'yes' or 'no'
        - `harvest_certificate`: Would you like to harvest certificate on verification failure. Either 'yes' or 'no'
        - `harvest_updatedcert`: Would you like to harvest updated certificate. Either 'yes' or 'no'
        - `smime_signature`: Select the appropriate operation for the S/MIME signature processing, 'Number'
        - `dk_vrfy`: enable DKIM verification. Either 'yes' or 'no'
        - `dk_vrfy_profile`: specify the DKIM verification profile to use
        - `spf_change`: change spf. Either 'yes' or 'no'
        - `spf_vrfy`: perform spf. Either 'yes' or 'no'
        - `spf_level`: specify Conformance Level.
        - `spf_pra_vrfy`: Downgrade PRA verification result.Either 'yes' or 'no'
        - `spf_helo`:specify if HELO test should be done. Either 'yes' or 'no'
        - `smtp_after_spf`: whether you'd like to change SMTP actions taken as
        result of the SPF verification. Either 'yes' or 'no'
        - `spf_vrfy_timeout`: timeout for SPF verification (number of seconds)
        - `dmarc_vrfy` : enable DMARC verification. Either 'yes' or 'no' or
                         'default'
        - `dmarc_vrfy_profile` : Select the DMARC verification profile to use
        - `dmarc_send_reports` : send aggregate reports. Either 'yes' or 'no'
                                 or 'default'
        - `sender_vrfy`: enable envelope sender verification.
          Either 'yes' or 'no'
        - `domain_exception`: enable use of the domain exception table.
          Either 'yes' or 'no'
        - `untagged_bounces`: accept untagged bounces. Either 'yes' or 'no'
        - `modify_rmes_banner`: enable custom SMTP response for malformed
          envelope senders. Either 'yes' or 'no'
        - `rmes_banner_code`: specify custom SMTP response for malformed
          envelope senders.
        - `comment`: enter a comment for the sender group

        *Examples*
        | ${hat_dict} | Create Dictionary | max_msg_size | 30M |
        | ... | max_concurrency | 200 | use_override_hostname | no |
        | ... | mmps | 200 |
        | Listenerconfig Edit Hostaccess New | TestInt1 | New Sender Group |
        | ... | newhost | .example.com | 1 | hat_change_bool=yes |
        | ... | hat_params=${hat_dict} |
        | Listenerconfig Edit Hostaccess New | TestInt1 | New Sender Group |
        | ... | newhost1 | .example1.com | 1 | hat_change_bool=no |
        | Listenerconfig Edit Hostaccess New | TestInt1 | Policy | newhost2 |
        | ... | .example2.com | 1 | hat_change_bool=yes |
        | ... | hat_params=${hat_dict} |
        | Listenerconfig Edit Hostaccess New | TestInt1 | Policy |
        | ... | newhost3 | .example3.com | 1 | hat_change_bool=no |
        """
        kwargs = self._convert_to_dict(args)
        arg = {'hat_change_bool': 'no', 'hat_params': None}

        for key in kwargs.keys():
            if key in arg.keys():
                arg[key] = kwargs[key]
                del kwargs[key]
        if arg['hat_params']:
            arg['hat_params'] = ast.literal_eval(arg['hat_params'])
        arg['hat_change_bool'] = self._set_yes_no_object(arg['hat_change_bool'])

        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            new(entry_type, new_name, host_list, access_behavior,
                arg['hat_change_bool'], arg['hat_params'])

    def listenerconfig_edit_hostaccess_edit_policy(self, intf_name,
                                                   name, access_behavior, *args):
        """
        This is used to edit a policy entry in the Host Access Table

        listenerconfig -> edit -> hostaccess -> edit -> policy

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this policy
        - `access_behavior': behavior for this entry
        - `hat_change_bool`: Change the host access policy. Either 'yes' or 'no'

        If `hat_change_bool` is 'yes', Host Access parameters specified under
        'Listenerconfig Edit Hostaccess New' can be used here

        *Examples*
        | Listenerconfig Edit Hostaccess Edit Policy | TestInt1 | ACCEPTED |
        | ... | ${Empty} | hat_params=${hat_dict} | hat_change_bool=yes |
        """
        kwargs = self._convert_to_dict(args)
        arg = {'hat_change_bool': 'no', 'hat_params': None}

        for key in kwargs.keys():
            if key in arg.keys():
                arg[key] = kwargs[key]
                del kwargs[key]
        if arg['hat_params']:
            arg['hat_params'] = ast.literal_eval(arg['hat_params'])
        arg['hat_change_bool'] = self._set_yes_no_object(arg['hat_change_bool'])

        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('policy', name, access_behavior,
                 arg['hat_change_bool'], arg['hat_params'])

    def listenerconfig_edit_hostaccess_edit_sendergroup_new(self, intf_name,
                                                            name, host_list, confirm_add_sender=YES):
        """
        This is used to add a new host in the sender group in the Host Access
        Table

        listenerconfig -> edit -> hostaccess -> edit -> sendergroup -> new

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this sender group
        - `host_list`: host to add to this sender group
        - `confirm_add_sender`: confirm adding entry. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Hostaccess Edit Sendergroup New | TestInt1 |
        | ... | WHITELIST | .example.com |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('sender group', name, None).new(host_list, confirm_add_sender)

    def listenerconfig_edit_hostaccess_edit_sendergroup_delete(self, intf_name,
                                                               name, host):
        """
        This is used to delete a host in the sender group in the Host Access
        Table

        listenerconfig -> edit -> hostaccess -> edit -> sendergroup -> delete

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this sender group
        - `host`: host to delete from this sender group

        *Examples*
        | Listenerconfig Edit Hostaccess Edit Sendergroup Delete | TestInt1 |
        | ... | WHITELIST | .example.com |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('sender group', name, None).delete(host)

    def listenerconfig_edit_hostaccess_edit_sendergroup_move(self, intf_name,
                                                             name, host_to_move, host_to_insert_before):
        """
        This is used to move a host's position in the sender group in the Host
        Access Table

        listenerconfig -> edit -> hostaccess -> edit -> sendergroup -> move

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this sender group
        - `host_to_move`: host to move in this sender group
        - `host_to_insert_before`: Position to insert before

        *Examples*
        | Listenerconfig Edit Hostaccess Edit Sendergroup Move | TestInt1 |
        | ... | WHITELIST | .example1.com | 1 |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('sender group', name, None).move(host_to_move,
                                                  host_to_insert_before)

    def listenerconfig_edit_hostaccess_edit_sendergroup_country_add(self, intf_name, name, countries):
        """
        This is used to move a host's position in the sender group in the Host
        Access Table

        listenerconfig -> edit -> hostaccess -> edit -> sendergroup -> country -> add

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this sender group
        - `countries`: List of the countries to be added.
              Values- index, index range, county name(s) or combination of all.

        *Examples*
        | Listenerconfig Edit Hostaccess Edit Sendergroup Country Add |
        | InBoundMail | UNKNOWNLIST | 1 |
        | Listenerconfig Edit Hostaccess Edit Sendergroup Country Add |
        | InBoundMail | UNKNOWNLIST | 1-10 |
        | Listenerconfig Edit Hostaccess Edit Sendergroup Country Add |
        | InBoundMail | UNKNOWNLIST | China,Ukraine |
        | Listenerconfig Edit Hostaccess Edit Sendergroup Country Add |
        | InBoundMail | UNKNOWNLIST | 1-10,Somalia |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('sender group', name, None).country().add(countries)

    def listenerconfig_edit_hostaccess_edit_sendergroup_country_delete(self, intf_name, name, countries):
        """
        This is used to move a host's position in the sender group in the Host
        Access Table

        listenerconfig -> edit -> hostaccess -> edit -> sendergroup -> country -> add

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this sender group
        - `countries`: List of the countries to be added.
              Values- index, index range, county name(s) or combination of all.

        *Examples*
        | Listenerconfig Edit Hostaccess Edit Sendergroup Country Delete |
        | InBoundMail | UNKNOWNLIST | 1 |
        | Listenerconfig Edit Hostaccess Edit Sendergroup Country Delete |
        | InBoundMail | UNKNOWNLIST | 1-10 |
        | Listenerconfig Edit Hostaccess Edit Sendergroup Country Delete |
        | InBoundMail | UNKNOWNLIST | China,Ukraine |
        | Listenerconfig Edit Hostaccess Edit Sendergroup Country Delete |
        | InBoundMail | UNKNOWNLIST | 1-10,Somalia |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('sender group', name, None).country().delete(countries)

    def listenerconfig_edit_hostaccess_edit_sendergroup_country_print(self, intf_name, name):
        """
        This is used to move a host's position in the sender group in the Host
        Access Table

        listenerconfig -> edit -> hostaccess -> edit -> sendergroup -> country -> add

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this sender group

        *Examples*
        | ${countries}= | Listenerconfig Edit Hostaccess Edit Sendergroup Country Print |
        | InBoundMail | UNKNOWNLIST |
        """
        return self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('sender group', name, None).country().Print()

    def listenerconfig_edit_hostaccess_edit_sendergroup_policy(self, intf_name,
                                                               name, access_behavior, change_policy_parameters_bool,
                                                               hat_params):
        """
        This is used to change the policy settings and options of the sender
        group in the Host Access Table

        listenerconfig -> edit -> hostaccess -> edit -> sendergroup -> policy

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this sender group
        - `access_behavior': behavior for this entry
        - `change_policy_parameters_bool`: Change the policy parameter.
          Either 'yes' or 'no'
        - `hat_params`: a dictionary containing any of the Host Access
        parameters specified under 'Listenerconfig Edit Hostaccess New'
        can be used here

        *Examples*
        | Listenerconfig Edit Hostaccess Edit Sendergroup Policy | TestInt1 |
        | ... | WHITELIST | 1 | yes | ${hat_dict} |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('sender group', name, None).policy(access_behavior,
                                                    change_policy_parameters_bool, hat_params)

    def listenerconfig_edit_hostaccess_edit_sendergroup_Print(self, intf_name,
                                                              name):
        """
        This is used to display the current definition of the sender group in
        the Host Access Table

        listenerconfig -> edit -> hostaccess -> edit -> sendergroup -> print

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this sender group

        *Examples*
        | Listenerconfig Edit Hostaccess Edit Sendergroup Print | TestInt1 |
        | ... | WHITELIST |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('sender group', name, None).Print()

    def listenerconfig_edit_hostaccess_edit_sendergroup_rename(self, intf_name,
                                                               name, new_name):
        """
        This is used to rename the sender group in the Host Access Table

        listenerconfig -> edit -> hostaccess -> edit -> sendergroup -> rename

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `name`: Name for this sender group
        - `new_name`: new name for this sender group

        *Examples*
        | Listenerconfig Edit Hostaccess Edit Sendergroup Rename | TestInt1 |
        | ... | WHITELIST | NEW_WHITELIST |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            edit('sender group', name, None).rename(new_name)

    def listenerconfig_edit_hostaccess_delete(self, intf_name, sg_or_policy,
                                              name, confirm_policy_deletion_bool=YES):
        """
        This is used to delete a host entry from the Host Access Table

        listenerconfig -> edit -> hostaccess -> delete

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `sg_or_policy`: Specify if 'sender group' or 'policy' is to be delete
        - `name`: Name for this sender group/policy
        - `confirm_policy_deletion_bool`: confirm deletion. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Hostaccess Delete | TestInt1 | policy | ACCEPTED |
        | ... | confirm_policy_deletion_bool=yes |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            delete(sg_or_policy, name, confirm_policy_deletion_bool)

    def listenerconfig_edit_hostaccess_move(self, intf_name, sg_to_move,
                                            sg_to_insert_before):
        """
        This is used to change a host's position in the Host Access Table

        listenerconfig -> edit -> hostaccess -> move

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `sg_or_policy`: Specify name of 'sender group' to be moved
        - `sg_to_insert_before`: position to insert before

        *Examples*
        | Listenerconfig Edit Hostaccess Move | TestInt1 | SUSPECTLIST | 1 |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            move(sg_to_move, sg_to_insert_before)

    def listenerconfig_edit_hostaccess_default(self, intf_name, hat_params):
        """
        This is used to set the defaults for Host Access parameters

        listenerconfig -> edit -> hostaccess -> default

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `hat_params`: a dictionary containing any of the Host Access
        parameters specified under 'Listenerconfig Edit Hostaccess New'
        can be used here

        *Examples*
        | Listenerconfig Edit Hostaccess Default | TestInt1 | ${hat_dict} |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            default(hat_params)

    def listenerconfig_edit_hostaccess_Print(self, intf_name):
        """
        This is used to print the Host Access Table

        listenerconfig -> edit -> hostaccess -> Print

        *Parameters*
        - `intf_name`: Name of the listener interface

        *Examples*
        | Listenerconfig Edit Hostaccess Print | TestInt1 |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess().Print()

    def listenerconfig_edit_hostaccess_Import(self, intf_name, filename):
        """
        This is used to import the Host Access Table

        listenerconfig -> edit -> hostaccess -> import

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `filename`: File from which it has to be imported

        *Examples*
        | Listenerconfig Edit Hostaccess Import | TestInt1 | filename.txt |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            Import(filename)

    def listenerconfig_edit_hostaccess_export(self, intf_name, filename):
        """
        This is used to export the Host Access Table

        listenerconfig -> edit -> hostaccess -> export

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `filename`: File to which it has to be exported

        *Examples*
        | Listenerconfig Edit Hostaccess export | TestInt1 | filename.txt |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess(). \
            export(filename)

    def listenerconfig_edit_hostaccess_reset(self, intf_name):
        """
        This is used to reset the Host Access Table

        listenerconfig -> edit -> hostaccess -> reset

        *Parameters*
        - `intf_name`: Name of the listener interface

        *Examples*
        | Listenerconfig Edit Hostaccess Clear | TestInt1 |
        """
        self._cli.listenerconfig().edit(name=intf_name).hostaccess().clear()

    def listenerconfig_edit_rcptaccess_new(self, intf_name, addrs, *args):
        """
        This is used to add a new entry to the Recipient Access Table

        listenerconfig -> edit -> rcptaccess -> new

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `addrs`: recipient address entry to be added.
        - `action`: specify the action to apply on this address
        - `smtp_response`: enable custom SMTP response. Either 'yes' or 'no'
        - `smtp_response_code`: SMTP code to use in the response
        - `smtp_response_text`: specify custom SMTP response
        - `bypass_injection_control`: bypass receiving control for this entry
          Either 'yes' or 'no'
        - `bypass_ldap_accept`: bypass LDAP ACCEPT for this entry
          Either 'yes' or 'no'
        - `smtp_call_ahead`: bypass SMTP Call-Ahead for this entry
          Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Rcptaccess New | TestInt1 | rcptdom.com |
        | ... | action=1 | smtp_response=yes | smtp_response_code=${Empty} |
        | ... | smtp_response_text=smtp text value |
        | ... | bypass_injection_control=${Empty} |
        | ... | bypass_ldap_accept=yes | smtp_call_ahead=yes |
        """
        kwargs = self._convert_to_dict(args)
        arg = {'action': DEFAULT, 'smtp_response': DEFAULT,
               'smtp_response_code': DEFAULT, 'smtp_response_text': '',
               'bypass_injection_control': DEFAULT,
               'bypass_ldap_accept': DEFAULT, 'smtp_call_ahead': DEFAULT}

        for key in kwargs.keys():
            if key in arg.keys():
                arg[key] = kwargs[key]
                del kwargs[key]

        self._cli.listenerconfig().edit(name=intf_name).rcptaccess(). \
            new(addrs, arg['action'], arg['smtp_response'],
                arg['smtp_response_code'], arg['smtp_response_text'],
                arg['bypass_injection_control'], arg['bypass_ldap_accept'],
                arg['smtp_call_ahead'])

    def listenerconfig_edit_rcptaccess_edit(self, intf_name, addrs, *args):
        """
        This is used to edit an entry in the Recipient Access Table

        listenerconfig -> edit -> rcptaccess -> edit

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `addrs`: recipient address entry to be edited.
        - `access`: specify the action to apply on this address
        - `custom_smtp_response`: enable custom SMTP response.
          Either 'yes' or 'no'
        - `smtp_response_code`: SMTP code to use in the response
        - `smtp_response_text`: specify custom SMTP response
        - `bypass_injection_control`: bypass receiving control for this entry
          Either 'yes' or 'no'
        - `bypass_ldap_accept`: bypass LDAP ACCEPT for this entry
          Either 'yes' or 'no'
        - `smtp_call_ahead`: bypass SMTP Call-Ahead for this entry
          Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Rcptaccess Edit | TestInt1 | rcptdom.com |
        | ... | access=2 | custom_smtp_response=yes |
        | ... | smtp_response_code=${Empty} |
        | ... | smtp_response_text=smtp new value |
        """
        kwargs = self._convert_to_dict(args)
        arg = {'access': DEFAULT, 'custom_smtp_response': DEFAULT,
               'smtp_response_code': DEFAULT, 'smtp_response_text': '',
               'bypass_injection_control': DEFAULT, 'bypass_ldap_accept': DEFAULT,
               'smtp_call_ahead': DEFAULT}

        for key in kwargs.keys():
            if key in arg.keys():
                arg[key] = kwargs[key]
                del kwargs[key]

        self._cli.listenerconfig().edit(name=intf_name).rcptaccess(). \
            edit(addrs, arg['access'], arg['custom_smtp_response'],
                 arg['smtp_response_code'], arg['smtp_response_text'],
                 arg['bypass_injection_control'], arg['bypass_ldap_accept'],
                 arg['smtp_call_ahead'])

    def listenerconfig_edit_rcptaccess_delete(self, intf_name, address):
        """
        This is used to delete an entry in the Recipient Access Table

        listenerconfig -> edit -> rcptaccess -> delete

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `address`: recipient address entry to be deleted.

        *Examples*
        | Listenerconfig Edit Rcptaccess Delete | TestInt1 | rcptdom.com |
        """
        self._cli.listenerconfig().edit(name=intf_name).rcptaccess(). \
            delete(address)

    def listenerconfig_edit_rcptaccess_Print(self, intf_name,
                                             print_all_entries_bool=YES):
        """
        This is used to print entries in the Recipient Access Table

        listenerconfig -> edit -> rcptaccess -> Print

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `print_all_entries_bool`: print all. Either 'yes' or 'no'

        *Examples*
        | Listenerconfig Edit Rcptaccess Print | TestInt1 |
        """
        self._cli.listenerconfig().edit(name=intf_name).rcptaccess(). \
            Print(print_all_entries_bool)

    def listenerconfig_edit_rcptaccess_Import(self, intf_name, filename):
        """
        This is used to import entries in the Recipient Access Table

        listenerconfig -> edit -> rcptaccess -> Import

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `filename`: file from which it has to be imported

        *Examples*
        | Listenerconfig Edit Rcptaccess Import | TestInt1 | rcptimport.txt |
        """
        self._cli.listenerconfig().edit(name=intf_name).rcptaccess(). \
            Import(filename)

    def listenerconfig_edit_rcptaccess_export(self, intf_name, filename):
        """
        This is used to export entries from the Recipient Access Table

        listenerconfig -> edit -> rcptaccess -> export

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `filename`: file to which it has to be exported

        *Examples*
        | Listenerconfig Edit Rcptaccess export | TestInt1 | rcptimport.txt |
        """
        self._cli.listenerconfig().edit(name=intf_name).rcptaccess(). \
            export(filename)

    def listenerconfig_edit_rcptaccess_clear(self, intf_name,
                                             default_access_behavior):
        """
        This is used to clear entries from the Recipient Access Table

        listenerconfig -> edit -> rcptaccess -> clear

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `default_access_behavior`: default access for the new empty RAT

        *Examples*
        | Listenerconfig Edit Rcptaccess Clear | TestInt1 | Reject |
        """
        self._cli.listenerconfig().edit(name=intf_name).rcptaccess(). \
            clear(default_access_behavior)

    def listenerconfig_edit_masquerade_new(self, intf_name, left, right, *args):
        """
        This is used to add a new entry to the domain masquerading table

        listenerconfig -> edit -> masquerade -> new

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `left`: source address or domain to be masqueraded
        - `right`: masqueraded address
        - `use_LDAP_masquerading`: use LDAP for masquerading
        - `m_query`: Specify the Masquerade Query

        *Examples*
        | Listenerconfig Edit Masquerade New | TestInt1 | @example.com |
        | ... | @example1.com |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.listenerconfig().edit(name=intf_name). \
            masquerade(**kwargs).new(left, right)

    def listenerconfig_edit_masquerade_delete(self, intf_name, to_delete, *args):
        """
        This is used to delete a entry from the domain masquerading table

        listenerconfig -> edit -> masquerade -> delete

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `to_delete`: address to be deleted
        - `use_LDAP_masquerading`: use LDAP for masquerading
        - `m_query`: Specify the Masquerade Query

        *Examples*
        | Listenerconfig Edit Masquerade Delete | TestInt1 | @example.com |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.listenerconfig().edit(name=intf_name). \
            masquerade(**kwargs).delete(to_delete)

    def listenerconfig_edit_masquerade_Print(self, intf_name, *args):
        """
        This is used to print the domain masquerading table

        listenerconfig -> edit -> masquerade -> print

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `use_LDAP_masquerading`: use LDAP for masquerading
        - `m_query`: Specify the Masquerade Query

        *Examples*
        | Listenerconfig Edit Masquerade Print | TestInt1 |
        """
        kwargs = self._convert_to_dict(args)
        print_all_value = True
        if 'print_all' in kwargs.keys():
            print_all_value = kwargs['print_all']
            del kwargs['print_all']
        self._cli.listenerconfig().edit(name=intf_name). \
            masquerade(**kwargs).Print(print_all_value)

    def listenerconfig_edit_masquerade_Import(self, intf_name, filename, *args):
        """
        This is used to import entries into the domain masquerading table

        listenerconfig -> edit -> masquerade -> import

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `filename`: file from which it has to be imported
        - `use_LDAP_masquerading`: use LDAP for masquerading
        - `m_query`: Specify the Masquerade Query

        *Examples*
        | Listenerconfig Edit Masquerade Import | TestInt1 | maskfile.txt |
        | ... | timeout=15 |
        """
        kwargs = self._convert_to_dict(args)
        timeout_value = 10
        if 'timeout' in kwargs.keys():
            timeout_value = kwargs['timeout']
            del kwargs['timeout']
        self._cli.listenerconfig().edit(name=intf_name). \
            masquerade(**kwargs).Import(filename, int(timeout_value))

    def listenerconfig_edit_masquerade_export(self, intf_name, filename, *args):
        """
        This is used to export entries from the domain masquerading table

        listenerconfig -> edit -> masquerade -> export

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `filename`: file to which it has to be exported
        - `use_LDAP_masquerading`: use LDAP for masquerading
        - `m_query`: Specify the Masquerade Query

        *Examples*
        | Listenerconfig Edit Masquerade export | TestInt1 | maskfile.txt |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.listenerconfig().edit(name=intf_name). \
            masquerade(**kwargs).export(filename)

    def listenerconfig_edit_masquerade_config(self, intf_name, *args):
        """
        This is used to configure masqueraded headers in the domain masquerading
        table

        listenerconfig -> edit -> masquerade -> config

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `mail_from_bool`: masquerade Envelope Sender. Either 'yes' or 'no'
        - `from_bool`: masquerade From headers. Either 'yes' or 'no'
        - `to_bool`: masquerade To headers. Either 'yes' or 'no'
        - `cc_bool`: masquerade CC headers. Either 'yes' or 'no'
        - `reply_to_bool`: masquerade Reply-To headers. Either 'yes' or 'no'
        - `use_LDAP_masquerading`: use LDAP for masquerading
        - `m_query`: Specify the Masquerade Query

        *Examples*
        | Listenerconfig Edit Masquerade Config | TestInt1 | to_bool=no |
        | ... | mail_from_bool=yes | from_bool=yes | reply_to_bool=${Empty} |
        | ... | to_bool=no | use_LDAP_masquerading=yes | m_query=${Empty} |
        """
        kwargs = self._convert_to_dict(args)
        list1 = ('use_LDAP_masquerading', 'm_query')
        list2 = ('mail_from_bool', 'from_bool', 'to_bool',
                 'cc_bool', 'reply_to_bool')
        arg1 = {}
        arg2 = {}
        for key in kwargs.keys():
            if key in list1:
                arg1[key] = kwargs[key]
            elif key in list2:
                arg2[key] = kwargs[key]
            else:
                raise KeyError('Invalid key [%s] specified' % (key))
        self._cli.listenerconfig().edit(name=intf_name). \
            masquerade(arg1).config(arg2)

    def listenerconfig_edit_masquerade_clear(self, intf_name, *args):
        """
        This is used to clear entries from the domain masquerading table

        listenerconfig -> edit -> masquerade -> clear

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `use_LDAP_masquerading`: use LDAP for masquerading
        - `m_query`: Specify the Masquerade Query

        *Examples*
        | Listenerconfig Edit Masquerade Clear | TestInt1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.listenerconfig().edit(name=intf_name). \
            masquerade(**kwargs).clear()

    def listenerconfig_edit_domainmap_new(self, intf_name, orig_dom, new_dom):
        """
        This is used to add a new entry to domain mapping table

        listenerconfig -> edit -> domainmap -> new

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `orig_dom`: original domain for this entry such as "@example.com",
          "@.example.com", "test@example.com" & "test@.example.com" are allowed
        - `new_dom`: email address for this entry. This must be a complete
          email address such as "test@example.com"

        *Examples*
        | Listenerconfig Edit Domainmap New | TestInt1 | @.example.com |
        | ... | @domain.com |
        """
        self._cli.listenerconfig().edit(name=intf_name).domainmap(). \
            new(orig_dom, new_dom)

    def listenerconfig_edit_domainmap_edit(self, intf_name, orig_dom, new_dom):
        """
        This is used to edit an entry in domain mapping table

        listenerconfig -> edit -> domainmap -> edit

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `orig_dom`: original domain for this entry such as "@example.com",
          "@.example.com", "test@example.com" & "test@.example.com" are allowed
        - `new_dom`: email address for this entry. This must be a complete
          email address such as "test@example.com"

        *Examples*
        | Listenerconfig Edit Domainmap Edit | TestInt1 | @.abc.com | @dom.com |
        """
        self._cli.listenerconfig().edit(name=intf_name).domainmap(). \
            edit(orig_dom, new_dom)

    def listenerconfig_edit_domainmap_delete(self, intf_name, orig_dom):
        """
        This is used to delete an entry in domain mapping table

        listenerconfig -> edit -> domainmap -> delete

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `orig_dom`: original domain for this entry such as "@example.com",
          "@.example.com", "test@example.com" & "test@.example.com" are allowed

        *Examples*
        | Listenerconfig Edit Domainmap Delete | TestInt1 | @.example.com |
        """
        self._cli.listenerconfig().edit(name=intf_name).domainmap(). \
            delete(orig_dom)

    def listenerconfig_edit_domainmap_Print(self, intf_name):
        """
        This is used to display all domain mappings

        listenerconfig -> edit -> domainmap -> Print

        *Parameters*
        - `intf_name`: Name of the listener interface

        *Examples*
        | Listenerconfig Edit Domainmap Print | TestInt1 |
        """
        self._cli.listenerconfig().edit(name=intf_name).domainmap().Print()

    def listenerconfig_edit_domainmap_Import(self, intf_name, filename):
        """
        This is used to import domain mappings from a file

        listenerconfig -> edit -> domainmap -> Import

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `filename`: file from which it has to be imported

        *Examples*
        | Listenerconfig Edit Domainmap Import | TestInt1 | domainmap.txt |
        """
        self._cli.listenerconfig().edit(name=intf_name).domainmap(). \
            Import(filename)

    def listenerconfig_edit_domainmap_export(self, intf_name, filename):
        """
        This is used to export domain mappings to a file

        listenerconfig -> edit -> domainmap -> export

        *Parameters*
        - `intf_name`: Name of the listener interface
        - `filename`: file to which it has to be exported

        *Examples*
        | Listenerconfig Edit Domainmap Export | TestInt1 | domainmap.txt |
        """

        self._cli.listenerconfig().edit(name=intf_name).domainmap(). \
            export(filename)

    def listenerconfig_edit_domainmap_clear(self, intf_name):
        """
        This is used to clear all domain mappings

        listenerconfig -> edit -> domainmap -> clear

        *Parameters*
        - `intf_name`: Name of the listener interface

        *Examples*
        | Listenerconfig Edit Domainmap Clear | TestInt1 |
        """
        self._cli.listenerconfig().edit(name=intf_name).domainmap().clear()
