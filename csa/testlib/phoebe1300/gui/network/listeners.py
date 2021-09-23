#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/network/listeners.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon
from sal.containers import cfgholder

# locators
# Add/Edit listener. Main locators.
LISTENERS_TABLE = "//*/table[@class='cols']"
ADD_LISTENER_BUTTON = "//input[@value='Add Listener...']"
LISTENER_DELETE_CONFIRM = "//*[@type='button' and text()='Delete']"
LISTENER_DELETE_CANCEL = "//*[@type='button' and text()='Cancel']"
LISTENER_NAME = "//*[@id='list_name']"
LISTENER_PORT = "//*[@id='list_port']"
LISTENER_TYPE_PUBLIC = "//*[@id='type_public']"
LISTENER_TYPE_PRIVATE = "//*[@id='type_private']"
LISTENER_INTERFACE = "//*/select[@name='interface']"
LISTENER_BOUNCE_PROFILE = "//*/select[@name='bounce_profile']"
LISTENER_DISCLAIMER_ABOVE = "//*/select[@name='heading_rsrc']"
LISTENER_DISCLAIMER_BELOW = "//*/select[@name='footer_rsrc']"
LISTENER_SMTP_AUTH = "//*/select[@name='smtpauth_profile']"
LISTENER_CERTIFICATE = "//*/select[@name='certificate']"

# Add/Edit listener. Address parsing.
ADRESS_PARSING_ARROW_CLOSED = "//div[@id='parsingLinkClosed']"
ADDRESS_PARSING_PARSER_TYPE = "//*/select[@name='address_parser_type']"
ADDRESS_PARSING_ALLOW_EIGHT_BIT_USERNAME = lambda x: "//*[@id='8bit_user%d']" % x
ADDRESS_PARSING_ALLOW_EIGHT_BIT_DOMAIN = lambda x: "//*[@id='8bit_domain%d']" % x
ADDRESS_PARSING_ALLOW_PARTIAL_DOMAIN = lambda x: "//*[@id='partial_domain%d']" % x
ADDRESS_PARSING_DEFAULT_DOMAIN = "//*[@id='default_domain']"
ADDRESS_PARSING_SOURCE_ROUTING_STRIP = "//*[@id='source_routing_disgard']"
ADDRESS_PARSING_SOURCE_ROUTING_REJECT = "//*[@id='source_routing_reject']"
ADDRESS_PARSING_UNKNOWN_ADDRESS_LITERALS = lambda x: "//*[@id='accept_unknown_literal%d']" % x
ADDRESS_PARSING_REJECT_CHARS_IN_USERNAME = "//*[@name='reject_username_chars']"

# Add/Edit listener. Advanced settings.
ADVANCED_SETTINGS_ARROW_CLOSED = "//div[@id='optionsLinkClosed']"
ADVANCED_SETTINGS_MAX_CONCURRENCY = "//*[@name='max_concurrency']"
ADVANCED_SETTINGS_LISTEN_QUEUE_SIZE = "//*[@name='listen_queue_size']"
ADVANCED_SETTINGS_CR_AND_LF_HANDLING = lambda x: "//*[@id='clean_%s']" % x
ADVANCED_SETTINGS_ADD_RECEIVED_HEADER = "//*[@id='enable_received_header']"
ADVANCED_SETTINGS_USE_SENDERBASE = "//*[@id='use_sb']"
ADVANCED_SETTINGS_QUERIES_TIMEOUT = "//*[@id='sb_timeout']"
ADVANCED_SETTINGS_CONNECTION_TIMEOUT = "//*[@id='sc_timeout']"

# Add/Edit listener. LDAP queries.
LDAP_QUERIES_ARROW_CLOSED = "//div[@id='ldapLinkClosed']"
# Accept
LDAP_ACCEPT_QUERY_ARROW_CLOSED = "//div[@id='ldapAcceptLinkClosed']"
LDAP_ACCEPT_QUERY_NAME = "//*[@id='accept_query']"
LDAP_ACCEPT_APPLY_AT = lambda x: "//*[@id='action_%s']" % x
LDAP_ACCEPT_NON_MATCHING_RCPTS = "//*[@id='rat_action']"
LDAP_ACCEPT_SERV_UNREACHABLE = lambda x: "//*[@id='ldapaction_%s']" % x
LDAP_ACCEPT_SERV_UNREACHABLE_TIMEOUT_CODE = "//*[@id='timeout_code']"
LDAP_ACCEPT_SERV_UNREACHABLE_TIMEOUT_MSG = "//*[@id='timeout_message']"

# Routing
LDAP_ROUTING_QUERY_ARROW_CLOSED = "//div[@id='ldapRoutingLinkClosed']"
LDAP_ROUTING_QUERY_NAME = "//*[@id='routing_query']"
# Group
LDAP_GROUP_QUERY_ARROW_CLOSED = "//div[@id='ldapGroupLinkClosed']"
LDAP_GROUP_QUERY_NAME = "//*[@id='group_query']"

# Masquerade
LDAP_MASQUERADE_QUERY_ARROW_CLOSED = "//div[@id='ldapMasqueradeLinkClosed']"
LDAP_MASQUERADE_QUERY_NAME = "//*[@id='masquerade_query']"
LDAP_MASQUERADE_ENVELOPE_SENDER = "//*[@id='mail_from']"
LDAP_MASQUERADE_FROM = "//*[@id='from']"
LDAP_MASQUERADE_TO = "//*[@id='to']"
LDAP_MASQUERADE_CC = "//*[@id='cc']"
LDAP_MASQUERADE_REPLY_TO = "//*[@id='reply-to']"

# Global settings
GLOBAL_SETTINGS_TABLE = "//*/table[@class='pairs']"
EDIT_GLOBAL_SETTINGS_BUTTON = "//input[@value='Edit Global Settings...']"
GLOBAL_SETTINGS_MAX_CONCURRENCY = "//*[@name='max_concurrency']"
GLOBAL_SETTINGS_MAX_TLS_CONCURRENCY = "//*[@name='max_tls_concurrency']"
GLOBAL_SETTINGS_COUNTERS_RESET_PERIOD = "//*[@name='injection_control_period']"
GLOBAL_SETTINGS_TIMEOUT = "//*[@name='inbound_conversation_timeout']"
GLOBAL_SETTINGS_TIME_LIMIT = "//*[@name='inbound_connection_timeout']"


class Listeners(GuiCommon):
    """
    Library to interact with 'Network > Listeners' page.
    """

    def get_keyword_names(self):
        return ['listeners_edit_global_settings',
                'listeners_get_global_settings',
                'listeners_add',
                'listeners_edit',
                'listeners_delete',
                'listeners_get_list',
                'listeners_configure_smtp_address_parsing',
                'listeners_configure_ldap_accept_query',
                'listeners_configure_ldap_routing_query',
                'listeners_configure_ldap_group_query',
                'listeners_configure_ldap_masquerade_query',
                'listeners_configure_advanced_settings']

    def _open_page(self):
        self._navigate_to('Network', 'Listeners')

    def _open_edit_listener_page(self, listener_name=None):
        # open listener to edit
        if listener_name:
            self._open_page()
            listener_link = self._get_element_link(LISTENERS_TABLE, listener_name)
            self.click_element(listener_link)

    def _select_interface(self, interface=None):
        self.select_from_dropdown_list(LISTENER_INTERFACE, interface)

    def _select_bounce_profile(self, profile=None):
        self.select_from_dropdown_list(LISTENER_BOUNCE_PROFILE, profile)

    def _select_disclaimer_above(self, disclaimer=None):
        self.select_from_dropdown_list(LISTENER_DISCLAIMER_ABOVE, disclaimer)

    def _select_disclaimer_below(self, disclaimer=None):
        self.select_from_dropdown_list(LISTENER_DISCLAIMER_BELOW, disclaimer)

    def _select_smtp_auth(self, profile=None):
        self.select_from_dropdown_list(LISTENER_SMTP_AUTH, profile)

    def _select_certificate(self, certificate=None):
        self.select_from_dropdown_list(LISTENER_CERTIFICATE, certificate)

    def _define_listener_type(self, listener_type=None):
        if listener_type is not None:
            if listener_type.lower() == 'public':
                self._click_radio_button(LISTENER_TYPE_PUBLIC)
            elif listener_type.lower() == 'private':
                self._click_radio_button(LISTENER_TYPE_PRIVATE)
            else:
                raise ValueError \
                    ("Listener type should be: 'public' or 'private'")

    def _define_listener_name(self, name=None):
        self._input_text_if_not_none(LISTENER_NAME, name)

    def _define_listener_port(self, port=None):
        self._input_text_if_not_none(LISTENER_PORT, port)

    def _add_listener_basic(self,
                            name=None,
                            type=None,
                            port=None,
                            interface=None,
                            bounce_profile=None,
                            disclaimer_above=None,
                            disclaimer_below=None,
                            smtp_auth_profile=None,
                            certificate=None):
        self._info('Adding new %s listener %s' % (type, name))
        self._open_page()
        self.click_button(ADD_LISTENER_BUTTON)
        self._define_listener_name(name=name)
        self._define_listener_type(listener_type=type)
        self._define_listener_port(port=port)
        self._select_interface(interface=interface)
        self._select_bounce_profile(profile=bounce_profile)
        self._select_disclaimer_above(disclaimer=disclaimer_above)
        self._select_disclaimer_below(disclaimer=disclaimer_below)
        self._select_smtp_auth(profile=smtp_auth_profile)
        self._select_certificate(certificate=certificate)

    def _edit_listener_basic(self,
                             name=None,
                             new_name=None,
                             port=None,
                             interface=None,
                             bounce_profile=None,
                             disclaimer_above=None,
                             disclaimer_below=None,
                             smtp_auth_profile=None,
                             certificate=None):
        self._info('Edit listener %s' % name)
        self._open_edit_listener_page(listener_name=name)
        self._define_listener_name(name=new_name)
        self._define_listener_port(port=port)
        self._select_interface(interface=interface)
        self._select_bounce_profile(profile=bounce_profile)
        self._select_disclaimer_above(disclaimer=disclaimer_above)
        self._select_disclaimer_below(disclaimer=disclaimer_below)
        self._select_smtp_auth(profile=smtp_auth_profile)
        self._select_certificate(certificate=certificate)

    @set_speed(0)
    def listeners_edit_global_settings(self,
                                       max_concurrency=None,
                                       max_tls_concurrency=None,
                                       counters_reset_period=None,
                                       timeout=None,
                                       time_limit=None):
        """
        Edit listeners Global Settings.

        *Parameters*:
        - `max_concurrency`: The global Maximum Concurrent Connections setting
         limits the number of simultaneous connections across all listeners combined.
         Must be a number from 1 to 5000.
        - `max_tls_concurrency`: The global Maximum Concurrent TLS Connections setting
         limits the number of simultaneous TLS connections across all listeners combined.
         Must be a number from 0 to 5000.
        - `counters_reset_period`: The Injection Counters Reset Period is the amount of
        time to wait before resetting the injection counters.
        Usage: 'h' - hours, 'm' - minutes, 's' - seconds. Combined values are allowed.
        (e.g. 120s, 5m 30s, 4h)
        - `timeout`: Timeout for Unsuccessful Inbound Connections.
        Usage: 'h' - hours, 'm' - minutes, 's' - seconds. Combined values are allowed.
        (e.g. 120s, 5m 30s, 4h)
        - `time_limit`: Total Time Limit for All Inbound Connections.
        Usage: 'h' - hours, 'm' - minutes, 's' - seconds. Combined values are allowed.
        (e.g. 120s, 5m 30s, 4h)

        *Return*:
        None

        *Examples*:
        | Listeners Edit Global Settings |
        | ... | max_concurrency=4000 |
        | ... | max_tls_concurrency=3500 |
        | ... | counters_reset_period=2h |
        | ... | timeout=10m |
        | ... | time_limit=30m |
        """
        self._info('Edit Global Settings')
        self._open_page()
        self.click_button(EDIT_GLOBAL_SETTINGS_BUTTON)
        self._input_text_if_not_none \
            (GLOBAL_SETTINGS_MAX_CONCURRENCY, max_concurrency)
        self._input_text_if_not_none \
            (GLOBAL_SETTINGS_MAX_TLS_CONCURRENCY, max_tls_concurrency)
        self._input_text_if_not_none \
            (GLOBAL_SETTINGS_COUNTERS_RESET_PERIOD, counters_reset_period)
        self._input_text_if_not_none \
            (GLOBAL_SETTINGS_TIMEOUT, timeout)
        self._input_text_if_not_none \
            (GLOBAL_SETTINGS_TIME_LIMIT, time_limit)
        self._click_submit_button()

    @set_speed(0)
    def listeners_get_global_settings(self, use_normalize=True):
        """
        Get Global Settings.

        *Parameters*:
        None

        *Return*:
        - `settings`: CfgHolder instance.

        *Examples*:
        | ${gl_settings} | Listeners Get Global Settings |
        | Log Dictionary | ${gl_settings} |

        | ${gl_settings} | Listeners Get Global Settings |
        | ... | use_normalize=${False} |
        | Log Dictionary | ${gl_settings} |
        """
        self._info('Get Global Settings')
        self._open_page()
        settings = cfgholder.CfgHolder()
        rows = \
            int(self.get_matching_xpath_count('%s//tr' % GLOBAL_SETTINGS_TABLE))
        rowno = 1
        text = \
            lambda row: self.get_text('%s//tr[%s]' % (GLOBAL_SETTINGS_TABLE, row))
        while rowno <= rows:
            tmp = text(rowno)
            if tmp:
                key, value = text(rowno).split(':')
                settings.__setattr__ \
                    (self._normalize(key, use_normalize=use_normalize), value)
            rowno += 1
        return settings

    def listeners_add(self,
                      listener_name=None,
                      type=None,
                      port=None,
                      interface=None,
                      bounce_profile=None,
                      disclaimer_above=None,
                      disclaimer_below=None,
                      smtp_auth_profile=None,
                      certificate=None,
                      submit=True):
        """
        Add new listener.

        *Parameters*:
        - `listener_name`: The name of the listener. String. Mandatory.
        - `type`: Listener's type. Options are: 'public' or 'private'. Case-insensitive.
        - `port`: TCP port to listen on. String.
        - `interface`: Bind listener to the selected interface. String. Case-insensitive.
        - `bounce_profile`: Select bounce profile to use. Select from list. String.
        - `disclaimer_above`: Disclaimer text to apply above the message body. Select from list. String.
        - `disclaimer_below`: Disclaimer text to apply below the message body. Select from list. String.
        - `smtp_auth_profile`: Radio-button. Unknown Address Literals. 'Reject' or 'Accept'. Case-insensitive.
        - `certificate`: The certificate to use with this listener. Select from list. String.
        - `submit`: If True, press Submit button. Boolean.

        *Return*:
        None

        *Examples*:
        | Listeners Add |
        | ... | listener_name=${pub_basic} |
        | ... | type=public |
        | ... | port=222 |
        | ... | interface=management |
        | ... | submit=${True} |

        | Listeners Add |
        | ... | listener_name=${pr_basic} |
        | ... | type=private |
        | ... | port=333 |
        | ... | interface=management |
        | ... | submit=${True} |

        The example below shows how to use all keywords together.
        The same can be done for `Listener Edit` action.
        Use keywords:
        `Listeners Configure SMTP Address Parsing`,
        `Listeners Configure Advanced Settings`,
        `Listeners Configure Ldap Accept Query`,
        `Listeners Configure Ldap Routing Query`,
        `Listeners Configure Ldap Group Query`,
        `Listeners Configure Ldap Masquerade Query`.

        | Listeners Add |
        | ... | listener_name=PublicAdvanced |
        | ... | type=public |
        | ... | port=444 |
        | ... | interface=a001 |
        | ... | bounce_profile=bounce1 |
        | ... | disclaimer_above=above1 |
        | ... | disclaimer_below=below1 |
        | ... | smtp_auth_profile=auth1 |
        | ... | certificate=cert1 |
        | ... | submit=${False} |
        | Listeners Configure SMTP Address Parsing |
        | ... | parser_type=loose |
        | ... | allow_eight_bit_username=${False} |
        | ... | allow_eight_bit_domain_name=${False} |
        | ... | allow_partial_domains=${True} |
        | ... | default_domain=qa |
        | ... | source_routing_action=reject |
        | ... | unknown_address_literals_action=accept |
        | ... | reject_chars_in_username=^& |
        | ... | submit=${False} |
        | Listeners Configure Advanced Settings |
        | ... | max_concurrency=450 |
        | ... | listen_queue_size=100 |
        | ... | crlf_hadling=reject |
        | ... | add_received_header=${True} |
        | ... | use_senderbase=${True} |
        | ... | timeout_for_queries=10 |
        | ... | timeout_per_connection=40 |
        | ... | submit=${False} |
        | Listeners Configure Ldap Accept Query |
        | ... | query_name=sully |
        | ... | apply_at=smtp |
        | ... | ldap_unreachable_action=allow |
        | ... | ldap_unreachable_err_code=452 |
        | ... | ldap_unreachable_err_msg=LDAPServUnreachable |
        | ... | submit=${False} |
        | Listeners Configure Ldap Routing Query |
        | ... | query_name=sully |
        | ... | submit=${False} |
        | Listeners Configure Ldap Group Query |
        | ... | query_name=sully |
        | ... | submit=${False} |
        | Listeners Configure Ldap Masquerade Query |
        | ... | query_name=sully |
        | ... | masq_envelope_sender=${True} |
        | ... | masq_from=${True} |
        | ... | masq_to=${True} |
        | ... | masq_cc=${True} |
        | ... | masq_reply_to=${True} |
        | ... | submit=${True} |
        """
        self._info('Create new listener: %s' % listener_name)
        self._add_listener_basic(name=listener_name,
                                 type=type,
                                 port=port,
                                 interface=interface,
                                 bounce_profile=bounce_profile,
                                 disclaimer_above=disclaimer_above,
                                 disclaimer_below=disclaimer_below,
                                 smtp_auth_profile=smtp_auth_profile,
                                 certificate=certificate)
        self._handle_submit(submit)

    @set_speed(0)
    def listeners_delete(self, listener_name, confirm=True):
        """
        Delete listener.

        *Parameters*:
        - `listener_name`: The name of the listener to be deleted. String.
        - `confirm`: Confirm delete operation. Boolean.

        *Return*:
        None

        *Examples*:
        | Listeners Delete | ${pub_basic} |

        | Listeners Delete | ListenerName |
        """
        self._info('Delete listener: %s' % listener_name)
        self._open_page()
        del_link = self._get_element_delete_link(LISTENERS_TABLE, listener_name)
        self.click_element(del_link, "don't wait")
        if confirm:
            self.click_button(LISTENER_DELETE_CONFIRM)
        else:
            self.click_button(LISTENER_DELETE_CANCEL)

    def listeners_edit(self,
                       listener_name=None,
                       new_name=None,
                       port=None,
                       interface=None,
                       bounce_profile=None,
                       disclaimer_above=None,
                       disclaimer_below=None,
                       smtp_auth_profile=None,
                       certificate=None,
                       submit=True):
        """
        Edit listener.

        *Parameters*:
        - `listener_name`: If listener name is given then open page to edit the listener.
        Otherwise, consider that we are at the needed page. String.
        - `port`: TCP port to listen on. String.
        - `interface`: Bind listener to the selected interface. String. Case-insensitive.
        - `bounce_profile`: Select bounce profile to use. Select from list. String.
        - `disclaimer_above`: Disclaimer text to apply above the message body. Select from list. String.
        - `disclaimer_below`: Disclaimer text to apply below the message body. Select from list. String.
        - `smtp_auth_profile`: Radio-button. Unknown Address Literals. 'Reject' or 'Accept'. Case-insensitive.
        - `certificate`: The certificate to use with this listener. Select from list. String.
        - `submit`: If True, press Submit button. Boolean.

        *Return*:
        None

        *Examples*:
        Each from the keywords below can be run separately.
        Submit can be done from any keyword.
        | Listeners Edit |
        | ... | listener_name=${pub_advanced} |
        | ... | port=777 |
        | ... | interface=management |
        | ... | submit=${False} |

        | Listeners Edit |
        | ... | listener_name=PublicAdvanced |
        | ... | port=444 |
        | ... | interface=a001 |
        | ... | bounce_profile=bounce1 |
        | ... | disclaimer_above=above1 |
        | ... | disclaimer_below=below1 |
        | ... | smtp_auth_profile=auth1 |
        | ... | certificate=cert1 |
        | ... | submit=${False} |

        | Listeners Edit |
        | ... | listener_name=PublicAdvanced |
        | ... | new_name=ChangedName |
        | ... | port=456 |
        | ... | interface=manag |
        | ... | bounce_profile=default |
        | ... | disclaimer_above=none |
        | ... | disclaimer_below=none |
        | ... | smtp_auth_profile=none |
        | ... | certificate=system |
        | ... | submit=${False} |
        """
        self._info('Edit listener')
        self._edit_listener_basic(name=listener_name,
                                  new_name=new_name,
                                  port=port,
                                  interface=interface,
                                  bounce_profile=bounce_profile,
                                  disclaimer_above=disclaimer_above,
                                  disclaimer_below=disclaimer_below,
                                  smtp_auth_profile=smtp_auth_profile,
                                  certificate=certificate)
        self._handle_submit(submit)

    @set_speed(0)
    def listeners_get_list(self):
        """
        Get list of configured listeners.

        *Parameters*:
        None

        *Return*:
        List of listeners names.

        *Examples*:
        | ${listeners} | Listeners Get List |
        | Should Be Empty | ${listeners} |

        | ${listeners} | Listeners Get List |
        | Should Contain | ${listeners} | ABC |
        """
        self._info('Get list of configured listeners')
        self._open_page()
        return self._get_element_list(LISTENERS_TABLE)

    def listeners_configure_smtp_address_parsing(self,
                                                 listener_name=None,
                                                 parser_type=None,
                                                 allow_eight_bit_username=None,
                                                 allow_eight_bit_domain_name=None,
                                                 allow_partial_domains=None,
                                                 default_domain=None,
                                                 source_routing_action=None,
                                                 unknown_address_literals_action=None,
                                                 reject_chars_in_username=None,
                                                 submit=True):
        """
        Add/Edit listener. Configure SMTP Address Parsing options.

        *Parameters*:
        - `listener_name`: If listener name is given then open page to edit the listener.
        Otherwise, consider that we are at the needed page. String.
        - `parser_type`: Address Parser Type. Options are: 'Loose', 'Strict'. Case-insensitive.
        - `allow_eight_bit_username`: Radio-button. Allow 8-bit User Names. Boolean. ${True} or ${False}.
        - `allow_eight_bit_domain_name`: Radio-button. Allow 8-bit Domain Names. Boolean. ${True} or ${False}.
        - `allow_partial_domains`: Radio-button. Allow Partial Domains. Boolean. ${True} or ${False}.
        - `default_domain`: Add Default Domain. String.
        - `source_routing_action`: Radio-button. Source Routing. Can be: 'Strip' or 'Reject'. Case-insensitive.
        - `unknown_address_literals_action`: Radio-button. Unknown Address Literals. 'Reject' or 'Accept'. Case-insensitive.
        - `reject_chars_in_username`: Reject These Characters in User Names. String.
        - `submit`: If True, press Submit button. Boolean.

        *Return*:
        None

        *Examples*:
        | Listeners Configure SMTP Address Parsing |
        | ... | parser_type=loose |
        | ... | allow_eight_bit_username=${True} |
        | ... | allow_eight_bit_domain_name=${True} |
        | ... | allow_partial_domains=${False} |
        | ... | source_routing_action=strip |
        | ... | unknown_address_literals_action=reject |
        | ... | reject_chars_in_username=*@ |
        | ... | submit=${False} |

        | Listeners Configure SMTP Address Parsing |
        | ... | litener_name=SomeName |
        | ... | parser_type=strict |
        | ... | allow_eight_bit_username=${False} |
        | ... | allow_eight_bit_domain_name=${False} |
        | ... | allow_partial_domains=${True} |
        | ... | default_domain=qa |
        | ... | submit=${True} |
        """
        self._info('Configure SMTP Address parsing')
        self._open_edit_listener_page(listener_name=listener_name)
        if self._is_visible(ADRESS_PARSING_ARROW_CLOSED):
            self.click_element(ADRESS_PARSING_ARROW_CLOSED)
        # self._select_from_list_use_regex\
        #            (ADDRESS_PARSING_PARSER_TYPE, parser_type, starts_with=True)
        # self.select_from_dropdown_list(ADDRESS_PARSING_PARSER_TYPE, parser_type)

        self.select_from_list(ADDRESS_PARSING_PARSER_TYPE, parser_type)
        if allow_eight_bit_username is not None:
            if allow_eight_bit_username:
                self._click_radio_button \
                    (ADDRESS_PARSING_ALLOW_EIGHT_BIT_USERNAME(1))
            else:
                self._click_radio_button \
                    (ADDRESS_PARSING_ALLOW_EIGHT_BIT_USERNAME(0))
        if allow_eight_bit_domain_name is not None:
            if allow_eight_bit_domain_name:
                self._click_radio_button \
                    (ADDRESS_PARSING_ALLOW_EIGHT_BIT_DOMAIN(1))
            else:
                self._click_radio_button \
                    (ADDRESS_PARSING_ALLOW_EIGHT_BIT_DOMAIN(0))
        if allow_partial_domains is not None:
            if allow_partial_domains:
                self._click_radio_button \
                    (ADDRESS_PARSING_ALLOW_PARTIAL_DOMAIN(1))
                self._input_text_if_not_none \
                    (ADDRESS_PARSING_DEFAULT_DOMAIN, default_domain)
            else:
                self._click_radio_button \
                    (ADDRESS_PARSING_ALLOW_PARTIAL_DOMAIN(0))
        if source_routing_action is not None:
            if source_routing_action.lower() == 'strip':
                self._click_radio_button(ADDRESS_PARSING_SOURCE_ROUTING_STRIP)
            elif source_routing_action.lower() == 'reject':
                self._click_radio_button(ADDRESS_PARSING_SOURCE_ROUTING_REJECT)
            else:
                raise ValueError \
                    ("The 'Source Routing' should be: 'Strip' or 'Reject'")
        if unknown_address_literals_action is not None:
            if unknown_address_literals_action.lower() == 'accept':
                self._click_radio_button \
                    (ADDRESS_PARSING_UNKNOWN_ADDRESS_LITERALS(1))
            elif unknown_address_literals_action.lower() == 'reject':
                self._click_radio_button \
                    (ADDRESS_PARSING_UNKNOWN_ADDRESS_LITERALS(0))
            else:
                raise ValueError \
                    ("The 'Unknown Address Literals' should be: 'Accept' or 'Reject'")
        self._input_text_if_not_none \
            (ADDRESS_PARSING_REJECT_CHARS_IN_USERNAME, reject_chars_in_username)
        self._handle_submit(submit)

    @set_speed(0)
    def listeners_configure_ldap_accept_query(self,
                                              listener_name=None,
                                              query_name=None,
                                              apply_at=None,
                                              invalid_rcpt=None,
                                              ldap_unreachable_action=None,
                                              ldap_unreachable_err_code=None,
                                              ldap_unreachable_err_msg=None,
                                              submit=True):
        """
        Add/Edit listener. Configure LDAP Accept Query.

        *Parameters*:
        - `listener_name`: If listener name is given then open page to edit the listener.
        Otherwise, consider that we are at the needed page. String.
        - `query_name`: LDAP Accept query name. String. Case-insensitive. Allows to use 'begins with'.
        - `apply_at`: On which stage the accept query should be applied. Either 'work' or 'smtp'.
        - `invalid_rcpt`: When accept query applied at Work queue and recipient is not matched. Actions: 'Drop' or 'Bounce'. String. Case-insensitive.
        - `ldap_unreachable_action`: The action to apply if the LDAP server is unreachable. Options are: 'Allow' or 'Error'.
        - `ldap_unreachable_err_code`: The error code to return if the LDAP server is unreachable. String.
        - `ldap_unreachable_err_msg`: The error message to return if the LDAP server is unreachable. String.
        - `submit`: If True, press Submit button. Boolean.

        *Return*:
        None

        *Examples*:
        | Listeners Configure Ldap Accept Query |
        | ... | query_name=sully |
        | ... | apply_at=smtp |
        | ... | ldap_unreachable_action=allow |
        | ... | submit=${False} |

        | Listeners Configure Ldap Accept Query |
        | ... | query_name=sully |
        | ... | apply_at=work |
        | ... | ldap_unreachable_action=error |
        | ... | ldap_unreachable_err_code=452 |
        | ... | ldap_unreachable_err_msg=LDAPServUnreachable |
        | ... | submit=${True} |
        """
        self._info('Configure LDAP Accept query')
        self._open_edit_listener_page(listener_name=listener_name)
        if self._is_visible(LDAP_QUERIES_ARROW_CLOSED):
            self.click_element(LDAP_QUERIES_ARROW_CLOSED)
        if self._is_visible(LDAP_ACCEPT_QUERY_ARROW_CLOSED):
            self.click_element(LDAP_ACCEPT_QUERY_ARROW_CLOSED)
        self.select_from_dropdown_list(LDAP_ACCEPT_QUERY_NAME, query_name)
        if query_name is not None:
            if apply_at is not None:
                _work = 'work'
                _smtp = 'smtp'
                if apply_at.lower() == _work:
                    self._click_radio_button(LDAP_ACCEPT_APPLY_AT(_work))
                    self.select_from_dropdown_list \
                        (LDAP_ACCEPT_NON_MATCHING_RCPTS,
                         invalid_rcpt)
                elif apply_at.lower() == _smtp:
                    _error = 'error'
                    self._click_radio_button(LDAP_ACCEPT_APPLY_AT(_smtp))
                    if ldap_unreachable_action is not None:
                        if ldap_unreachable_action.lower() == 'allow':
                            self._click_radio_button \
                                (LDAP_ACCEPT_SERV_UNREACHABLE('drop'))
                        elif ldap_unreachable_action.lower() == 'error':
                            self._click_radio_button \
                                (LDAP_ACCEPT_SERV_UNREACHABLE(_error))
                            self._input_text_if_not_none \
                                (LDAP_ACCEPT_SERV_UNREACHABLE_TIMEOUT_CODE,
                                 ldap_unreachable_err_code)
                            self._input_text_if_not_none \
                                (LDAP_ACCEPT_SERV_UNREACHABLE_TIMEOUT_MSG,
                                 ldap_unreachable_err_msg)
                        else:
                            raise ValueError \
                                ("The 'LDAP unreachable action' can be: 'allow' or 'error'")
                else:
                    raise ValueError \
                        ("The 'LDAP accept query' can be applied at: 'work' or 'smtp'")
        self._handle_submit(submit)

    @set_speed(0)
    def listeners_configure_ldap_routing_query(self,
                                               listener_name=None,
                                               query_name=None,
                                               submit=True):
        """
        Add/Edit listener. Configure LDAP Routing Query.

        *Parameters*:
        - `listener_name`: If listener name is given then open page to edit the listener.
        Otherwise, consider that we are at the needed page. String.
        - `query_name`: LDAP Group query name. String. Case-insensitive. Allows to use 'begins with'.
        - `submit`: If True, press Submit button. Boolean.

        *Return*:
        None

        *Examples*:
        | Listeners Configure Ldap Routing Query |
        | ... | query_name=sully |
        | ... | submit=${False} |

        | Listeners Configure Ldap Routing Query |
        | ... | listener_name=NameOfTheListener |
        | ... | query_name=none |
        | ... | submit=${True} |
        """
        self._info('Configure LDAP Routing query')
        self._open_edit_listener_page(listener_name=listener_name)
        if self._is_visible(LDAP_QUERIES_ARROW_CLOSED):
            self.click_element(LDAP_QUERIES_ARROW_CLOSED)
        if self._is_visible(LDAP_ROUTING_QUERY_ARROW_CLOSED):
            self.click_element(LDAP_ROUTING_QUERY_ARROW_CLOSED)
        self.select_from_dropdown_list(LDAP_ROUTING_QUERY_NAME, query_name)
        self._handle_submit(submit)

    @set_speed(0)
    def listeners_configure_ldap_group_query(self,
                                             listener_name=None,
                                             query_name=None,
                                             submit=True):
        """
        Add/Edit listener. Configure LDAP Group Query.

        *Parameters*:
        - `listener_name`: If listener name is given then open page to edit the listener.
        Otherwise, consider that we are at the needed page. String.
        - `query_name`: LDAP Routing query name. String. Case-insensitive. Allows to use 'begins with'.
        - `submit`: If True, press Submit button. Boolean.

        *Return*:
        None

        *Examples*:
        | Listeners Configure Ldap Group Query |
        | ... | query_name=sully |
        | ... | submit=${False} |

        | Listeners Configure Ldap Group Query |
        | ... | listener_name=BooName |
        | ... | query_name=sully |
        | ... | submit=${True} |
        """
        self._info('Configure LDAP Group query')
        self._open_edit_listener_page(listener_name=listener_name)
        if self._is_visible(LDAP_QUERIES_ARROW_CLOSED):
            self.click_element(LDAP_QUERIES_ARROW_CLOSED)
        if self._is_visible(LDAP_GROUP_QUERY_ARROW_CLOSED):
            self.click_element(LDAP_GROUP_QUERY_ARROW_CLOSED)
        self.select_from_dropdown_list(LDAP_GROUP_QUERY_NAME, query_name)
        self._handle_submit(submit)

    @set_speed(0)
    def listeners_configure_ldap_masquerade_query(self,
                                                  listener_name=None,
                                                  query_name=None,
                                                  masq_envelope_sender=None,
                                                  masq_from=None,
                                                  masq_to=None,
                                                  masq_cc=None,
                                                  masq_reply_to=None,
                                                  submit=True):
        """
        Add/Edit listener. Configure LDAP Masquerade Query.

        *Parameters*:
        - `listener_name`: If listener name is given then open page to edit the listener.
        Otherwise, consider that we are at the needed page. String.
        - `query_name`: LDAP Masquerade query name. String. Case-insensitive. Allows to use 'begins with'.
        Addresses to Masquerade:
        - `masq_envelope_sender`: Masquerade 'Envelope Sender'. Boolean. ${True} or ${False}.
        - `masq_from`: Masquerade 'From' header. Boolean. ${True} or ${False}.
        - `masq_to`: Masquerade 'To' header. Boolean. ${True} or ${False}.
        - `masq_cc`: Masquerade 'Cc' header. Boolean. ${True} or ${False}.
        - `masq_reply_to`: Masquerade 'To' header. Boolean. ${True} or ${False}.
        - `submit`: If True, press Submit button. Boolean.

        *Return*:
        None

        *Examples*:
        | Listeners Configure Ldap Masquerade Query |
        | ... | query_name=sully |
        | ... | masq_envelope_sender=${True} |
        | ... | masq_from=${True} |
        | ... | masq_to=${True} |
        | ... | masq_cc=${True} |
        | ... | masq_reply_to=${True} |
        | ... | submit=${True} |

        | Listeners Configure Ldap Masquerade Query |
        | ... | listener_name=NameBoo |
        | ... | query_name=sully |
        | ... | masq_envelope_sender=${False} |
        | ... | masq_from=${False} |
        | ... | masq_to=${False} |
        | ... | masq_cc=${False} |
        | ... | masq_reply_to=${False} |
        | ... | submit=${False} |
        """
        self._info('Configure LDAP Masquerade query')
        self._open_edit_listener_page(listener_name=listener_name)
        if self._is_visible(LDAP_QUERIES_ARROW_CLOSED):
            self.click_element(LDAP_QUERIES_ARROW_CLOSED)
        if self._is_visible(LDAP_MASQUERADE_QUERY_ARROW_CLOSED):
            self.click_element(LDAP_MASQUERADE_QUERY_ARROW_CLOSED)
        self.select_from_dropdown_list(LDAP_MASQUERADE_QUERY_NAME, query_name)
        if query_name is not None:
            self._select_unselect_checkbox \
                (LDAP_MASQUERADE_ENVELOPE_SENDER, masq_envelope_sender)
            self._select_unselect_checkbox \
                (LDAP_MASQUERADE_FROM, masq_from)
            self._select_unselect_checkbox \
                (LDAP_MASQUERADE_TO, masq_to)
            self._select_unselect_checkbox \
                (LDAP_MASQUERADE_CC, masq_cc)
            self._select_unselect_checkbox \
                (LDAP_MASQUERADE_REPLY_TO, masq_reply_to)
        self._handle_submit(submit)
        return None

    @set_speed(0)
    def listeners_configure_advanced_settings(self,
                                              listener_name=None,
                                              max_concurrency=None,
                                              listen_queue_size=None,
                                              crlf_hadling=None,
                                              add_received_header=None,
                                              use_senderbase=None,
                                              timeout_for_queries=None,
                                              timeout_per_connection=None,
                                              submit=True):
        """
        Add/Edit listener. Configure Advanced Settings.

        *Parameters*:
        - `listener_name`: If listener name is given then open page to edit the listener.
        Otherwise, consider that we are at the needed page. String.
        - `max_concurrency`: Maximum Concurrent Connections. String.
        - `listen_queue_size`: TCP Listen Queue Size. String.
        - `crlf_hadling`: CR and LF Handling.
           Options are:
              'clean'- Clean messages of bare CR and LF characters;
              'reject' - Reject messages with bare CR or LF characters;
              'uncelan' - Allow messages with bare CR or LF characters (DEPRECATED).
        - `add_received_header`: Add Received Header. Boolean. ${True} or ${False}.
        - `use_senderbase`: Use SenderBase IP Profiling. Boolean. ${True} or ${False}.
        - `timeout_for_queries`: Timeout for Queries. String.
        - `timeout_per_connection`: SenderBase Timeout per Connection. String.
        - `submit`: If True, press Submit button. Boolean.

        *Return*:
        None

        *Examples*:
        | Listeners Configure Advanced Settings |
        | ... | max_concurrency=100 |
        | ... | listen_queue_size=50 |
        | ... | crlf_hadling=clean |
        | ... | add_received_header=${False} |
        | ... | use_senderbase=${False} |
        | ... | submit=${True} |

        | Listeners Configure Advanced Settings |
        | ... | crlf_hadling=unclean |
        | ... | add_received_header=${True} |
        | ... | use_senderbase=${True} |
        | ... | timeout_for_queries=30 |
        | ... | timeout_per_connection=60 |
        | ... | submit=${False} |

        | Listeners Configure Advanced Settings |
        | ... | listener_name=${pub_advanced} |
        | ... | max_concurrency=120 |
        | ... | submit=${True} |
        """
        self._info('Configure LDAP Advanced settings')
        self._open_edit_listener_page(listener_name=listener_name)
        if self._is_visible(ADVANCED_SETTINGS_ARROW_CLOSED):
            self.click_element(ADVANCED_SETTINGS_ARROW_CLOSED)
        self._input_text_if_not_none \
            (ADVANCED_SETTINGS_MAX_CONCURRENCY, max_concurrency)
        self._input_text_if_not_none \
            (ADVANCED_SETTINGS_LISTEN_QUEUE_SIZE, listen_queue_size)
        if crlf_hadling is not None:
            _clean = 'clean'
            _reject = 'reject'
            _unclean = 'unclean'
            if crlf_hadling.lower() == _clean:
                self._click_radio_button \
                    (ADVANCED_SETTINGS_CR_AND_LF_HANDLING(_clean))
            elif crlf_hadling.lower() == _reject:
                self._click_radio_button \
                    (ADVANCED_SETTINGS_CR_AND_LF_HANDLING(_reject))
            elif crlf_hadling.lower() == _unclean:
                self._click_radio_button \
                    (ADVANCED_SETTINGS_CR_AND_LF_HANDLING(_unclean))
            else:
                raise ValueError \
                    ("The 'CR and LF Handling' should be one from: '%s', '%s', '%s'" % \
                     (_clean, _reject, _unclean))
        if add_received_header is not None:
            if add_received_header:
                self._select_checkbox(ADVANCED_SETTINGS_ADD_RECEIVED_HEADER)
            else:
                self._unselect_checkbox(ADVANCED_SETTINGS_ADD_RECEIVED_HEADER)
        if use_senderbase is not None:
            if use_senderbase:
                self._select_checkbox(ADVANCED_SETTINGS_USE_SENDERBASE)
                self._input_text_if_not_none \
                    (ADVANCED_SETTINGS_QUERIES_TIMEOUT, timeout_for_queries)
                self._input_text_if_not_none \
                    (ADVANCED_SETTINGS_CONNECTION_TIMEOUT, timeout_per_connection)
            else:
                self._unselect_checkbox(ADVANCED_SETTINGS_USE_SENDERBASE)
        self._handle_submit(submit)
