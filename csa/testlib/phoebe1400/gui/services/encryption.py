#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/services/encryption.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import functools
import time

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
from common.util.sarftime import CountDownTimer
from common.logging import Logger

# General stuff
ENABLE_TEXT_DIV = "//table[@class='pairs']/tbody/tr[1]/td"
ENABLE_BUTTON = "//input[@name='action:Enable']"
ACCEPT_LIC_BUTTON = "//input[@name='AcceptLicense']"
PROFILES_TABLE = "//dl[.//dt[normalize-space()='Email Encryption Profiles']]"
PROFILE_EDIT_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                                 (PROFILES_TABLE, name)
PROFILE_DELETE_LINK = lambda name: \
    "%s//td[.//a[normalize-space()='%s']]/following-sibling::td[3]/img" % \
    (PROFILES_TABLE, name)
PROFILE_PROVISION_BUTTON = lambda name: "//input[@title='Provision' and "\
                   "@type='button' and contains(@onclick, 'inprogress_%s')]" % \
                   (name,)
PROFILE_PROVISION_STATUS = lambda name: \
    "%s//td[.//a[normalize-space()='%s']]/following-sibling::td[2]" % \
    (PROFILES_TABLE, name)
PROFILE_ADD_BUTTON = "//input[@value='Add Encryption Profile...']"
UPDATE_NOW_BUTTON = "//input[@name='UpdateNow']"
ACTION_RESULTS = "//div[@id='action-results']"

# Settings
DISABLE_CHECK_BOX = "//input[@id='enabled']"
EDIT_SETTINGS_BUTTON = "//input[@name='action:FormEditGlobal']"
ENABLE_PROXY_CB = "//input[@id='proxy_enabled']"
P_TYPE_MAP = {'HTTP': 'web',
              'SOCKS 4': 'socks4',
              'SOCKS 5': 'socks5'}
PROXY_TYPE_RB = lambda p_type: "//input[@id='proxy_type_%s']" % \
                (P_TYPE_MAP[p_type],)
HOSTNAME_TB = "//input[@id='hostname']"
PORT_TB = "//input[@id='port']"
USERNAME_TB = "//input[@id='user']"
PASSWORD_TB = "//input[@id='password']"
CONFIRM_PWD_TB = "//input[@id='password1']"
MAX_MSG_SIZE_TB = "//input[@id='enc_max_msg_size']"
EMAIL_ADDRESS_TB = "//input[@id='account_email_admin']"
COMMON_CONFIRM_DIALOG = "//*[@id='confirmation_dialog']"
COMMON_CONFIRM_BUTTON = lambda text: \
"%s//button[normalize-space()='%s']" % (COMMON_CONFIRM_DIALOG, text)


# Profile settings
CANCEL_BUTTON = "//input[@type='button' and @value='Cancel']"
PROF_NAME_TB = "//input[@name='profile_name']"
KEY_SER_TYPE_DD = "//select[@id='profile_type']"
USE_PROXY_CB = "//input[@id='use_proxy']"
PROXY_NOT_CONFIGURED_MARK = 'A proxy server is not currently configured.'
INTERNAL_URL_TB = "//input[@name='internal_url']"
EXTERNAL_URL_TB = "//input[@name='external_url_local']"
CISCO_URL_TB = "//input[@name='external_url_hosted']"
KEY_SERVER_SETTINGS_ADVANCED = "//div[@id='arrow_closed_gpt_url']"
PAYLOAD_TRANSPORT_URL_MAP = {
'Use the Cisco Registered Envelope Service URL with HTTP': 'http_external_url',
'Use the Cisco Registered Envelope Service URL with HTTPs': 'external_url',
'Use a separate URL for payload transport': 'gpt_url'}
PAYLOAD_TRANSPORT_RADIO = lambda transport_type: \
                                "//input[@id='gpt_opt_%s' and @type='radio']" % \
                                 (PAYLOAD_TRANSPORT_URL_MAP[transport_type],)
PAYLOAD_CUSTOM_TRANSPORT_URL = "//input[@id='gpt_url' and @type='text']"

MSG_SEC_MAP = {'High Security': 50,
               'Medium Security': 10,
               'No Password Required': 0}
MSG_SEC_RB = lambda m_type: "//input[@id='sensitivity_%d']" % \
                            (MSG_SEC_MAP[m_type],)
LOGO_LINK_MAP = {'No link': 'no',
                 'Custom link URL': 'yes'}
LOGO_LINK_RB = lambda val: "//input[@id='logo_link_%s']" % (LOGO_LINK_MAP[val],)
LOGO_LINK_TB = "//input[@name='logo_url']"
READ_RCPTS_CB = "//input[@id='return_receipt']"
ENVELOPE_SETTINGS_ADVANCED = "//div[@id='arrow_closed_envelope']"

ENC_QUEUE_TIMEOUT_TB = "//input[@name='max_queue_lifetime']"
ENCODING_ALGORITHMS_MAP = {'ARC4': 'arc4',
                           'AES-192': 'aes_192',
                           'AES-256': 'aes_256'}
ENC_ALGO_RB = lambda algo: "//input[@id='encryption_algorithm_%s']" % \
                           (ENCODING_ALGORITHMS_MAP[algo],)
USE_DECRYPTION_CB = "//input[@id='use_applet']"

ENABLE_REPLY_ALL_CB = "//input[@id='replyall_enabled']"
ENABLE_FWD_CB = "//input[@id='forward_enabled']"

LOCALIZED_ENVELOPE_CB = "//input[@id='localized_envelope']"
DEFAULT_LOCALE_DD = "//select[@id='default_locale']"
HTML_NOTIFIC_DD = "//select[@id='html_text_resource_id']"
TEXT_NOTIFIC_DD = "//select[@id='plain_text_resource_id']"
FAILURE_SUBJ_TB = "//input[@name='bounce_subject']"
FAILURE_MSG_BODY_DD = "//select[@id='bounce_template_id']"
ATTACHED_FILENAME_TB = "//input[@name='envelope_filename']"


def check_iee_feature(need_to_raise_exc):
    """This decorator is used to navigate to Ironport Email Encryption
    feature. Decorator can be applied only to Encryption class methods

    *Parameters:*
    - `need_to_raise_exc`: whether to raise GuiFeatureDisabledError if
    IEE feature is disabled. Either True or False
    """
    def decorator(func):
        @functools.wraps(func)
        def worker(self, *args, **kwargs):
            if not self.ironport_email_encryption_is_enabled():
                if need_to_raise_exc:
                    raise guiexceptions.GuiFeatureDisabledError(
                        'IronPort Email Encryption feature is not enabled')
            return func(self, *args, **kwargs)
        return worker
    return decorator


def set_properties(selenium, obj, all_props, props_to_set):
    """Sets values for elements given in props_to_set dictionary

    *Parameters:*
    - `selenium`: ExtendedSeleniumLibrary instance
    - `obj`: object containing custom setters and getters
    - `all_props`: dictionary whose keys are element identifiers and values
    contains corresponding element attributes. One dictionary entry has the next format:
    | getter | name of the method which returns element's value, for
    example get_value; method should take no mandatory arguments |
    | setter | name of the method which sets some value to an element;
    this method should take element locator as the first parameter and
    and
    | locator | Selenium-compatible element locator |
    for single-element controls (like edit box, checkbox, combobox, etc, or
    | possible_value1 | {'locator': <element_locator1>} |
    | possible_valueN | {'locator': <element_locatorN>} |
    for groups, like radio group
    If setter is not set (target element is text label for example) then this
    method will simply ignore setting it
    - `props_to_set`: dictionary whose keys are element identifiers (must match
    to corresponding identifiers in all_props dictionary) and values are element
    values to be set

    *Exceptions:*
    - `ValueError`: if there is no record for particular property in all_props
    dictionary
    """

    for element_id, value in props_to_set.items():
        if not all_props.has_key(element_id):
            raise ValueError('Unknown "%s" property can not be set to "%s"'\
                             % (element_id, value))
        props = all_props[element_id]
        if props.has_key('setter'):
            setter_name = props['setter']
            if hasattr(obj, setter_name):
                setter = getattr(obj, setter_name)
            elif hasattr(selenium, setter_name):
                setter = getattr(selenium, setter_name)
            else:
                raise ValueError('There is no method named "%s" in Selenium and'\
                                 ' in class "%s"' % (setter_name, obj.__class__.__name__))
            # get corresponding Selenium setter dynamically
            # and set corresponding value to element
            if props.has_key('locator'):
                setter(props['locator'], props_to_set[element_id])
            else:
                # Radio group detected
                # finding locator by value to set
                value_to_set = props_to_set[element_id]
                target_locator = props[value_to_set]['locator']
                setter(target_locator)

def get_properties(selenium, obj, props_to_get):
    """Get values from elements given in props_to_get dictionary

    *Parameters:*
    - `selenium`: ExtendedSeleniumLibrary instance
    - `obj`: object containing custom setters and getters
    - `props_to_get`: dictionary whose keys are element identifiers and values
    contains corresponding element attributes. One dictionary entry has the next format:
    | getter | name of the method which returns element's value, for
    example get_value; method should take no mandatory arguments |
    | setter | name of the method which sets some value to an element;
    this method should take element locator as the first parameter and
    value as the second |
    and
    | locator | Selenium-compatible element locator |
    for single-element controls (like edit box, checkbox, combobox, etc, or
    | possible_value1 | {'locator': <element_locator1>} |
    | possible_valueN | {'locator': <element_locatorN>} |
    for groups (like radio group)

    *Return*:
    Dictionary whose keys are element identifiers (same as in props_to_get dict) and
    values are taken from GUI (all are converted to strings)
    """
    details_dict = {}
    for element_id, props in props_to_get.items():
        getter_name = props['getter']
        if hasattr(obj, getter_name):
            getter = getattr(obj, getter_name)
        elif hasattr(selenium, getter_name):
            getter = getattr(selenium, getter_name)
        else:
            raise ValueError('There is no method named "%s" in Selenium and'\
                             ' in class "%s"' % (getter_name, obj.__class__.__name__))
        # get corresponding Selenium getter dynamically
        # and receive corresponding element value
        if props.has_key('locator'):
            details_dict[element_id] = str(getter(props['locator']))
        else:
            # Radio group detected
            possible_values = filter(lambda x: x not in ('setter', 'getter'),
                                     props)
            for value in possible_values:
                target_locator = props[value]['locator']
                if str(getter(target_locator)) == str(value):
                    details_dict[element_id] = value
                    break
    return details_dict


class EnvelopeProfile(object):
    """Controller class for envelope profile edit form
    """

    IEE_PROFILE_EDIT_FORM_ELEMENTS = {
    'profile_name': {'setter': 'input_text',
                     'getter': 'get_value',
                     'locator': PROF_NAME_TB},
    'key_service_type': {'setter': 'select_from_list',
                         'getter': 'get_value',
                         'locator': KEY_SER_TYPE_DD},
    'use_proxy': {'setter': '_set_use_proxy',
                  'getter': '_get_use_proxy',
                  'locator': USE_PROXY_CB},
    'internal_url':{'setter': 'input_text',
                   'getter': 'get_value',
                   'locator': INTERNAL_URL_TB},
    'external_url':{'setter': 'input_text',
                    'getter': 'get_value',
                    'locator': EXTERNAL_URL_TB},
    'envelope_url': {'setter': 'input_text',
                     'getter': 'get_value',
                     'locator': CISCO_URL_TB},
    'payload_transport_ext_url': {'setter': '_set_ext_payload_transport_url',
                                  'getter': '_get_ext_payload_transport_url',
                                  'locator': '<not used>'},
    'msg_security': {'setter': '_click_radio_button',
                     'getter': '_is_checked',
                     'High Security': {'locator': MSG_SEC_RB('High Security')},
                     'Medium Security': {'locator': MSG_SEC_RB('Medium Security')},
                     'No Password Required': {'locator': \
                                              MSG_SEC_RB('No Password Required')}},
    'logo_link': {'setter': '_set_logo_link',
                  'getter': '_get_logo_link',
                  'locator': '<not used>'},
    'read_receipts': {'setter': '_set_checkbox_state',
                      'getter': '_is_checked',
                      'locator': READ_RCPTS_CB},
    'queue_timeout': {'setter': 'input_text',
                      'getter': 'get_value',
                      'locator': ENC_QUEUE_TIMEOUT_TB},
    'encryption_algo': {'setter': '_click_radio_button',
                        'getter': '_is_checked',
                        'ARC4': {'locator': ENC_ALGO_RB('ARC4')},
                        'AES-192': {'locator': ENC_ALGO_RB('AES-192')},
                        'AES-256': {'locator': ENC_ALGO_RB('AES-256')}},
    'attachment_decryption': {'setter': '_set_checkbox_state',
                              'getter': '_is_checked',
                              'locator': USE_DECRYPTION_CB},
    'secure_reply_all': {'setter': '_set_checkbox_state',
                         'getter': '_is_checked',
                         'locator': ENABLE_REPLY_ALL_CB},
    'secure_msg_forwarding': {'setter': '_set_checkbox_state',
                              'getter': '_is_checked',
                              'locator': ENABLE_FWD_CB},
    'localized_envelope': {'setter': '_set_checkbox_state',
                           'getter': '_is_checked',
                           'locator': LOCALIZED_ENVELOPE_CB},
    'default_locale': {'setter': 'select_from_list',
                       'getter': 'get_value',
                       'locator': DEFAULT_LOCALE_DD},

    'encrypted_msg_html_notification': {'setter': '_set_encrypted_msg_html_notificationy',
                                        'getter': '_get_encrypted_msg_html_notification',
                                        'locator': HTML_NOTIFIC_DD},
    'encrypted_msg_text_notification': {'setter': '_set_encrypted_msg_text_notification',
                                        'getter': '_get_encrypted_msg_text_notification',
                                        'locator': TEXT_NOTIFIC_DD},
    'encryption_fail_msg_subj': {'setter': 'input_text',
                                 'getter': 'get_value',
                                 'locator': FAILURE_SUBJ_TB},
    'encryption_fail_msg_body': {'setter': '_set_encryption_fail_msg_body',
                                 'getter': '_get_encryption_fail_msg_body',
                                 'locator': FAILURE_MSG_BODY_DD},
    'attached_filename': {'setter': 'input_text',
                          'getter': 'get_value',
                          'locator': ATTACHED_FILENAME_TB}}

    def __init__(self, gui_common):
        self.gui = gui_common

    def _open_advanced_sections(self):
        for locator in (KEY_SERVER_SETTINGS_ADVANCED,
                        ENVELOPE_SETTINGS_ADVANCED):
            self.gui.click_button(locator, 'don\'t wait')
        time.sleep(0.5)

    def _set_use_proxy(self, locator, new_value):
        if self.gui._is_text_present(PROXY_NOT_CONFIGURED_MARK):
            raise guiexceptions.ConfigError('Proxy server should be configured'\
                                            ' in order to set it for encryption'\
                                            ' profile')
        self.gui._set_checkbox_state(locator, new_value)

    def _get_use_proxy(self, locator):
        if self.gui._is_text_present(PROXY_NOT_CONFIGURED_MARK):
            return PROXY_NOT_CONFIGURED_MARK
        return self.gui._is_checked(locator)

    def _set_encryption_fail_msg_body(self, locator, new_value):
        if not self.gui._is_element_present(FAILURE_MSG_BODY_DD):
            raise guiexceptions.ConfigError('"Bounce and Encryption Failure'\
                            ' Notification Template" should be configured'\
                            ' in order to set it for encryption failure'\
                            ' notification')
        self.gui.select_from_list(FAILURE_MSG_BODY_DD, new_value)

    def _get_encryption_fail_msg_body(self, locator):
        if not self.gui._is_element_present(FAILURE_MSG_BODY_DD):
            return 'System Generated'
        return self.gui.get_value(locator)

    def _set_encrypted_msg_html_notification(self, locator, new_value):
        if not self.gui._is_element_present(HTML_NOTIFIC_DD):
            raise guiexceptions.ConfigError('"Encryption Notification Template'\
                            '- HTML" should be configured'\
                            ' in order to set it for encryption message'\
                            ' html notification')
        self.gui.select_from_list(HTML_NOTIFIC_DD, new_value)

    def _get_encrypted_msg_html_notification(self, locator):
        if not self.gui._is_element_present(HTML_NOTIFIC_DD):
            return 'System Generated'
        return self.gui.get_value(locator)

    def _set_encrypted_msg_text_notification(self, locator, new_value):
        if not self.gui._is_element_present(TEXT_NOTIFIC_DD):
            raise guiexceptions.ConfigError('"Encryption Notification Template'\
                            '- Text" should be configured'\
                            ' in order to set it for encryption message'\
                            ' text notification')
        self.gui.select_from_list(TEXT_NOTIFIC_DD, new_value)

    def _get_encrypted_msg_text_notification(self, locator):
        if not self.gui._is_element_present(TEXT_NOTIFIC_DD):
            return 'System Generated'
        return self.gui.get_value(locator)

    def _set_ext_payload_transport_url(self, locator, new_value):
        if new_value in PAYLOAD_TRANSPORT_URL_MAP.keys():
            self.gui._click_radio_button(PAYLOAD_TRANSPORT_RADIO(new_value))
        else:
            self.gui._click_radio_button(PAYLOAD_TRANSPORT_RADIO(\
                        'Use a separate URL for payload transport'))
            self.gui.input_text(PAYLOAD_CUSTOM_TRANSPORT_URL, new_value)

    def _get_ext_payload_transport_url(self, locator):
        for key in PAYLOAD_TRANSPORT_URL_MAP.iterkeys():
            if self.gui._is_checked(PAYLOAD_TRANSPORT_RADIO(key)):
                if key == 'Use a separate URL for payload transport':
                    return self.gui.get_value(PAYLOAD_CUSTOM_TRANSPORT_URL)
                else:
                    return key

    def _set_logo_link(self, locator, new_value):
        if new_value == 'No link':
            self.gui._click_radio_button(LOGO_LINK_RB(new_value))
        else:
            self.gui._click_radio_button(LOGO_LINK_RB('Custom link URL'))
            self.gui.input_text(LOGO_LINK_TB, new_value)

    def _get_logo_link(self, locator):
        if self.gui._is_checked(LOGO_LINK_RB('No link')):
            return 'No link'
        else:
            return self.gui.get_value(LOGO_LINK_TB)

    def set(self, props): 
        self._open_advanced_sections()
        set_properties(self, self.gui,
                       self.IEE_PROFILE_EDIT_FORM_ELEMENTS,
                       props)

    def get(self):
        self._open_advanced_sections()
        return get_properties(self, self.gui,
                              self.IEE_PROFILE_EDIT_FORM_ELEMENTS)

class Encryption(GuiCommon):
    """Keywords for interaction with
    ESA GUI Security Services -> IronPort Email Encryption page
    """

    IIE_EDIT_FORM_ELEMENTS = {
    'max_message_size': {'setter': 'input_text',
                          'getter': 'get_value',
                          'locator': MAX_MSG_SIZE_TB},
    'email_address': {'setter': 'input_text',
                      'getter': 'get_value',
                      'locator': EMAIL_ADDRESS_TB},
    'enable_proxy': {'setter': '_set_checkbox_state',
                     'getter': '_is_checked',
                     'locator': ENABLE_PROXY_CB},
    'proxy_type': {'setter': '_click_radio_button',
                   'getter': '_is_checked',
                   'HTTP': {'locator': PROXY_TYPE_RB('HTTP')},
                   'SOCKS 4': {'locator': PROXY_TYPE_RB('SOCKS 4')},
                   'SOCKS 5': {'locator': PROXY_TYPE_RB('SOCKS 5')}},
    'hostname': {'setter': 'input_text',
                 'getter': 'get_value',
                 'locator': HOSTNAME_TB},
    'port': {'setter': 'input_text',
             'getter': 'get_value',
             'locator': PORT_TB},
    'username': {'setter': 'input_text',
                 'getter': 'get_value',
                 'locator': USERNAME_TB},
    'password': {'setter': 'input_text',
                 'getter': 'get_value',
                 'locator': PASSWORD_TB},
    'confirm_password': {'setter': 'input_text',
                         'getter': 'get_value',
                         'locator': CONFIRM_PWD_TB}}

    def get_keyword_names(self):
        return ['ironport_email_encryption_is_enabled',
                'ironport_email_encryption_enable',
                'ironport_email_encryption_disable',
                'ironport_email_encryption_edit_settings',
                'ironport_email_encryption_add_profile',
                'ironport_email_encryption_edit_profile',
                'ironport_email_encryption_delete_profile',
                'ironport_email_encryption_get_profile_details',
                'ironport_email_encryption_provision_profile',
                'ironport_email_encryption_update_pxe_engine']

    def ironport_email_encryption_is_enabled(self):
        """Return IronPort Email Encryption feature state

        *Return:*
        True if IEE feature is enabled or False otherwise

        *Examples:*
        | ${iee_state}= | IronPort Email Encryption Is Enabled |
        """
        PAGE_PATH = ('Security Services', 'Cisco IronPort Email Encryption')
        self._debug('Opening "%s" page' % (' -> '.join(PAGE_PATH),))
        self._navigate_to(*PAGE_PATH)

        DISABLED_MARK = 'The Cisco IronPort Email Encryption feature is currently disabled.'
        return not self._is_text_present(DISABLED_MARK)

    @check_iee_feature(False)
    def ironport_email_encryption_enable(self):
        """Enable IronPort Email Encryption feature.
        Does nothing is IEE feature is already enabled

        *Examples:*
        | ${iee_state}= | IronPort Email Encryption Is Enabled |
        | Run Keyword If | ${iee_state} == ${False} | IronPort Email Encryption Enable |
        """
        LICENSE_AGREEMENT_MARK = 'License Agreement'

        if self._is_element_present(ENABLE_BUTTON):
            self.click_button(ENABLE_BUTTON)
            if self._is_text_present(LICENSE_AGREEMENT_MARK):
                self.click_button(ACCEPT_LIC_BUTTON)
            self._check_action_result()

    @check_iee_feature(False)
    def ironport_email_encryption_disable(self):
        """Disable IronPort Email Encryption feature.
        Does nothing is IEE feature is already disabled

        *Examples:*
        | ${iee_state}= | IronPort Email Encryption Is Enabled |
        | Run Keyword If | ${iee_state} == ${True} | IronPort Email Encryption Disable |
        """
        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            self._unselect_checkbox(DISABLE_CHECK_BOX)
            self._click_submit_button()

    @check_iee_feature(True)
    def ironport_email_encryption_edit_settings(self, **kwargs):
        """Edit IronPort Email Encryption settings

        *Parameters:*
        - `max_message_size`: Maximum Message Size to Encrypt. Add a trailing K or M to indicate units.
        - `email_address`: Email address of the encryption account administrator.
        - `enable_proxy`: Configure proxy for use in encryption profiles or not.
        Either ${True} or ${False}
        - `proxy_type`: Type of proxy to be used as given in the web page. Applicable
        if `enable_proxy` is set to ${true}.
        Supported proxy types are:
        | HTTP |
        | SOCKS 4 |
        | SOCKS 5 |
        - `hostname`: Hostname/IP address of the proxy server.
        Mandatory if `enable_proxy` is set to ${True}
        - `port`: Proxy port number. Applicable if `enable_proxy` is set to ${True}
        - `username`: Username for proxy authentication.
        Applicable if `enable_proxy` is set to ${True}
        - `password`: Password for proxy authentication.
        Applicable if `enable_proxy` is set to ${True}

        *Exceptions:*
        - `GuiFeatureDisabledError`: if IIE feature is disabled
        - `ValueError`: if any of passes values is not correct

        *Examples:*
        | IronPort Email Encryption Edit Settings | enable_proxy=${True} |
        | ... | proxy_type=SOCKS 4 | hostname=myproxy.com | port=3128 |
        | ... | username=user | password=secretpassword |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        if 'password' in kwargs.keys():
            # Automatically set the same password value to
            # Confirm Password field
            kwargs.update({'confirm_password': kwargs['password']})

        if 'enable_proxy' in kwargs and kwargs['enable_proxy']:
            self._select_checkbox(ENABLE_PROXY_CB)

        set_properties(self, self, self.IIE_EDIT_FORM_ELEMENTS, kwargs)
        self._click_submit_button(wait=False, skip_wait_for_title=True)
        tmr = CountDownTimer(10).start()
        while tmr.is_active():
            time.sleep(1)
            try:
                if self._is_visible(COMMON_CONFIRM_DIALOG):
                    self.click_button(COMMON_CONFIRM_BUTTON('Continue'))
                    break
            except:
                pass
        else:
            return
        self.wait_until_page_loaded(timeout=60)

    @check_iee_feature(True)
    def ironport_email_encryption_add_profile(self, profile_name, **kwargs):
        """Add new encryption envelope profile to IEE

        *Parameters:*
        - `profile_name`: the name of new encryption profile
        - `key_service_type`: the type of key encryption service. Either:
        | Cisco Registered Envelope Service |
        | Cisco IronPort Encryption Appliance (in network) |
        - `use_proxy`: whether to proxy (must be already set in
        settings; will raise ConfigError if not set). Either ${True} or
        ${False}
        - `internal_url`: This URL will be used by the Cisco IronPort Email
            Security Appliance to contact Cisco IronPort Encryption Appliance.
        - `external_url`: This URL will be used by IronPort PXE messages to access
            keys and other services of the Cisco IronPort Encryption Appliance.
            This is an inbound HTTPS request from recipients to the issuer's
            Cisco IronPort Encryption Appliance.
        - `envelope_url`: Cisco Registered Envelope Service URL
        - `payload_transport_ext_url`: external URL for Payload Transport.
        Either:
        | Use the Cisco Registered Envelope Service URL with HTTP |
        | Use the Cisco Registered Envelope Service URL with HTTPs |
        | <your custom URL for Payload Transport> |
        - `msg_security`: message security. Either:
        | High Security |
        | Medium Security |
        | No Password Required |
        - `logo_link`: logo link URL. Can be
        | No link |
        or your custom http resource
        - `read_receipts`: whether to enable or disable receipts reading, Either
        ${True} or ${False}
        - `queue_timeout`: encryption queue timeout (in seconds)
        - `encryption_algo`: encryption algorithm. Either:
        | ARC4 |
        | AES-192 |
        | AES-256 |
        - `attachment_decryption`: whether to use Message Attachment Decryption.
        Disabling this setting will cause message attachments to be
        decrypted at the key server. They will take longer to open,
        but they don't require a Java plug-in. Either ${True} or ${False}
        - `secure_reply_all`: whether to enable secure Reply All. Either
        ${True} or ${False}
        - `secure_msg_forwarding`: whether to enable secure Message Forwarding.
        Either ${True} or ${False}
        - `localized_envelope`: whether to use localized envelope.
        Either ${True} or ${False}.After creating a new profile,
        commit your changes and return to profile edit to set the default locale.
        - `default_locale`: Select the language from the drop down. String
        - `encrypted_msg_html_notification`: name of profile defined in
        "Mail Policies > Text Resources > Encryption Notification Template - HTML"
        to be used as encrypted message HTML notification. Returns "System Generated"
        by default
        - `encrypted_msg_text_notification`: name of profile defined in
        "Mail Policies > Text Resources > Encryption Notification Template - Text"
        to be used as encrypted message Text notification. Returns "System Generated"
        by default
        - 'encryption_fail_msg_subj': subject of message to be used in encryption
        failure notification message
        - `encryption_fail_msg_body`: name of profile defined in
        "Mail Policies > Text Resources > DSN Bounce and Encryption Failure
        Notification Template" to be used as message body in encryption
        failure notification message. Returns "System Generated" by default
        - `attached_filename`: file name of the envelope attached to the
        encryption notification

        *Exceptions:*
        - `GuiFeatureDisabledError`: if IIE feature is disabled
        - `ValueError`: if some value is not correct
        - `ConfigError`: if some value is set but dependent setting is not configured
        properly

        *Examples:*
        | \
        IronPort Email Encryption Add Profile | my_new_enc_profile |
        | ... | key_service_type=Cisco Registered Envelope Service |
        | ... | envelope_url=https://res.cisco.com |
        | ... | payload_transport_ext_url=Use the Cisco Registered Envelope Service URL with HTTPs |
        | ... | msg_security=Medium Security |
        | ... | logo_link=http://k.img.com.ua/img/forall/a/13840/91.jpg |
        | ... | read_receipts=${True} |
        | ... | queue_timeout=15000 |
        | ... | encryption_algo=AES-256 |
        | ... | attachment_decryption=${False} |
        | ... | secure_reply_all=${False} |
        | ... | secure_msg_forwarding=${True} |
        | ... | encryption_fail_msg_subj=Failed Subj |
        | ... | attached_filename=securedoc_T${time}.html |
        """
        self.click_button(PROFILE_ADD_BUTTON)
        profile = self._get_envelope_profile_controller()
        kwargs.update({'profile_name': profile_name})
        profile.set(kwargs)
        self._click_submit_button()

    @check_iee_feature(True)
    def ironport_email_encryption_edit_profile(self, old_profile_name, **kwargs):
        """Edit encryption envelope profile

        *Parameters:*
        - `old_profile_name`: the name of existing encryption profile
        - `profile_name`: the new name of encryption profile (leaving it
        not set will not change existing profile name)
        - `key_service_type`: the type of key encryption service. Either:
        | Cisco Registered Envelope Service |
        | Cisco IronPort Encryption Appliance (in network) |
        - `use_proxy`: whether to proxy (must be already set in
        settings; will raise ConfigError if not set). Either ${True} or
        ${False}
        - `envelope_url`: Cisco Registered Envelope Service URL
        - `payload_transport_ext_url`: external URL for Payload Transport.
        Either:
        | Use the Cisco Registered Envelope Service URL with HTTP |
        | Use the Cisco Registered Envelope Service URL with HTTPs |
        | <your custom URL for Payload Transport> |
        - `msg_security`: message security. Either:
        | High Security |
        | Medium Security |
        | No Password Required |
        - `logo_link`: logo link URL. Can be
        | No link |
        or your custom http resource
        - `read_receipts`: whether to enable or disable receipts reading, Either
        ${True} or ${False}
        - `queue_timeout`: encryption queue timeout (in seconds)
        - `encryption_algo`: encryption algorithm. Either:
        | ARC4 |
        | AES-192 |
        | AES-256 |
        - `attachment_decryption`: whether to use Message Attachment Decryption.
        Disabling this setting will cause message attachments to be
        decrypted at the key server. They will take longer to open,
        but they don't require a Java plug-in. Either ${True} or ${False}
        - `secure_reply_all`: whether to enable secure Reply All. Either
        ${True} or ${False}
        - `secure_msg_forwarding`: whether to enable secure Message Forwarding.
        Either ${True} or ${False}
        - `localized_envelope`: whether to use localized envelope.
        Either ${True} or ${False}.After creating a new profile,
        commit your changes and return to profile edit to set the default locale.
        - `default_locale`: Select the language from the drop down. String
        - `encrypted_msg_html_notification`: name of profile defined in
        "Mail Policies > Text Resources > Encryption Notification Template - HTML"
        to be used as encrypted message HTML notification. Returns "System Generated"
        by default
        - `encrypted_msg_text_notification`: name of profile defined in
        "Mail Policies > Text Resources > Encryption Notification Template - Text"
        to be used as encrypted message Text notification. Returns "System Generated"
        by default
        - 'encryption_fail_msg_subj': subject of message to be used in encryption
        failure notification message
        - `encryption_fail_msg_body`: name of profile defined in
        "Mail Policies > Text Resources > DSN Bounce and Encryption Failure
        Notification Template" to be used as message body in encryption
        failure notification message. Returns "System Generated" by default
        - `attached_filename`: file name of the envelope attached to the
        encryption notification

        *Exceptions:*
        - `GuiFeatureDisabledError`: if IIE feature is disabled
        - `ValueError`: if some of passed values is not correct
        - `ConfigError`: if some value is set but dependent setting is not configured
        properly

        *Examples:*
        | IronPort Email Encryption Edit Profile | my_existing_enc_profile |
        | ... | profile_name=new_profile_name |
        | ... | key_service_type=Cisco Registered Envelope Service |
        | ... | envelope_url=https://res.cisco.com |
        | ... | payload_transport_ext_url=Use the Cisco Registered Envelope Service URL with HTTPs |
        | ... | msg_security=Medium Security |
        | ... | logo_link=http://k.img.com.ua/img/forall/a/13840/91.jpg |
        | ... | read_receipts=${True} |
        | ... | queue_timeout=15000 |
        | ... | encryption_algo=AES-256 |
        | ... | attachment_decryption=${False} |
        | ... | secure_reply_all=${False} |
        | ... | secure_msg_forwarding=${True} |
        | ... | encryption_fail_msg_subj=Failed Subj |
        | ... | attached_filename=securedoc_T${time}.html |
        """
        try:
            self.click_button(PROFILE_EDIT_LINK(old_profile_name))
        except Exception:
            raise ValueError('Envelope profile named "%s" is not found' % \
                             (old_profile_name,))

        if 'key_service_type' in kwargs:
            current_service_type = self.get_value(KEY_SER_TYPE_DD)
            if current_service_type != kwargs['key_service_type']:
                self.select_from_list(KEY_SER_TYPE_DD, kwargs['key_service_type'])
                tmr = CountDownTimer(10).start()
                while tmr.is_active():
                    time.sleep(1)
                    try:
                        if self._is_visible(COMMON_CONFIRM_DIALOG):
                            self.click_button(COMMON_CONFIRM_BUTTON('Continue'))
                            break
                        else:
                            return
                    except:
                        pass
                self.wait_until_page_loaded(timeout=60)

        profile = self._get_envelope_profile_controller()
        profile.set(kwargs)
        self._click_submit_button()

    @check_iee_feature(True)
    def ironport_email_encryption_delete_profile(self, profile_name):
        """Delete existing encryption envelope profile

        *Parameters:*
        -`profile_name`: existing encryption profile name to be deleted

        *Exceptions*:
        - `GuiFeatureDisabledError`: if IIE feature is disabled
        - `ValueError`: if given profile name does not exist

        *Examples:*
        | IronPort Email Encryption Delete Profile | my_existing_enc_profile |
        """
        try:
            self.click_button(PROFILE_DELETE_LINK(profile_name), 'don\'t wait')
        except Exception:
            raise ValueError('Envelope profile named "%s" is not found' % \
                             (profile_name,))
        self._click_continue_button()

    @check_iee_feature(True)
    def ironport_email_encryption_get_profile_details(self, profile_name):
        """Get existing encryption envelope profile details

        *Return:*
        Dictionary which items are:
        | `profile_name` | the name of encryption profile |
        | `key_service_type` | the type of key encryption service. Either:
        "Cisco Registered Envelope Service" or "Cisco IronPort Encryption
        Appliance (in network)" |
        | `use_proxy` | whether to proxy profile configured in settings |
        | `envelope_url` | Cisco Registered Envelope Service URL |
        | `payload_transport_ext_url` | external URL for Payload Transport.
        Either: "Use the Cisco Registered Envelope Service URL with HTTP" or
        "Use the Cisco Registered Envelope Service URL with HTTPs" or
        your custom URL for Payload Transport |
        | `msg_security` | message security. Either: "High Security" or
        "Medium Security" or "No Password Required" |
        | `logo_link` | logo link URL. Can be "No link" or your custom http resource |
        | `read_receipts` | whether receipts reading is enabled or disabled |
        | `queue_timeout` | encryption queue timeout (in seconds) |
        | `encryption_algo` | encryption algorithm. Either: "ARC4" or "AES-192"
        or "AES-256" |
        | `attachment_decryption` | whether Message Attachment Decryption is used |
        | `secure_reply_all` | whether secure Reply All is enabled |
        | `secure_msg_forwarding` | whether secure Message Forwarding is enabled |
        | `localized_envelope` |  whether localized envelope is enabled |
        | `default_locale`| language used for localized envelope |
        | `encrypted_msg_html_notification` | name of profile defined in
        "Mail Policies > Text Resources > Encryption Notification Template - HTML"
        and is used as encrypted message HTML notification. Returns "System Generated"
        by default |
        | `encrypted_msg_text_notification` | name of profile defined in
        "Mail Policies > Text Resources > Encryption Notification Template - Text"
        and is used as encrypted message Text notification. Returns "System Generated"
        by default |
        | 'encryption_fail_msg_subj' | subject of message used in encryption
        failure notification message |
        | `encryption_fail_msg_body` | name of profile defined in
        "Mail Policies > Text Resources > DSN Bounce and Encryption Failure
        Notification Template" and is used as message body in encryption
        failure notification message. Returns "System Generated" by default |
        | `attached_filename` | file name of the envelope attached to the
        encryption notification |

        *Exceptions:*
        - `GuiFeatureDisabledError`: if IIE feature is disabled
        - `ValueError`: if given profile name is not found

        *Examples:*
        | ${details} | IronPort Email Encryption Get Profile Details |
        | ... | my_existing_enc_profile |
        | ${proxy}= | Get From Dictionary | ${details} | use_proxy |
        | Log | ${proxy} |
        """
        try:
            self.click_button(PROFILE_EDIT_LINK(profile_name))
        except Exception:
            raise ValueError('Envelope profile named "%s" is not found' % \
                             (profile_name,))

        profile = self._get_envelope_profile_controller()
        details = profile.get()
        self.click_button(CANCEL_BUTTON)
        return details

    @check_iee_feature(True)
    def ironport_email_encryption_provision_profile(self, profile_name):
        """Provision particular encryption envelope profile

        *Parameters:*
        -`profile_name`: existing encryption profile name to be provisioned

        *Exceptions*:
        - `GuiFeatureDisabledError`: if IIE feature is disabled
        - `ValueError`: if given profile name does not exist
        - `TimeoutError`: if it is impossible to get provisioning result
        message within 5 minutes timeout
        - `ConfigError`: if "Provision" button is not available for the
        particular profile

        *Return:*
        provisioning status message or "not applicable" if provisioning action
        can not be applied to this particular profile

        *Examples:*
        | ${result}= | IronPort Email Encryption Provision Profile | my_profile |
        | Log | ${result} |
        """
        if not self._is_element_present(PROFILE_EDIT_LINK(profile_name)):
            raise ValueError('Profile named "%s" does not exist' % \
                             (profile_name,))

        if not self._is_element_present(PROFILE_PROVISION_BUTTON(profile_name)):
            raise guiexceptions.ConfigError('Profile changes should be commited'\
                                            ' before they can be provisioned')

        NOT_APPLICABLE_MARK = 'not applicable'
        current_status = self.get_text(PROFILE_PROVISION_STATUS(profile_name))
        if current_status.lower().find(NOT_APPLICABLE_MARK) >= 0:
            return current_status

        self.click_button(PROFILE_PROVISION_BUTTON(profile_name), "don't wait")
        time.sleep(0.5)

        PROVISIONING_MARK = "was successfully provisioned"
        TIMEOUT = 60 * 5
        results_present = False
        timer = CountDownTimer(TIMEOUT).start()
        while timer.is_active():
            if self._is_text_present(PROVISIONING_MARK):
                results_present = True
                break
            time.sleep(1.0)
        if not results_present:
            raise guiexceptions.TimeoutError('Cannot get provisioning action result '\
                                             'within %d seconds timeout' % (TIMEOUT,))
        else:
            return self.get_text(ACTION_RESULTS)

    @check_iee_feature(True)
    def ironport_email_encryption_update_pxe_engine(self):
        """Force PXE engine update

        *Exceptions:*
        - `GuiFeatureDisabledError`: if IIE feature is disabled

        *Examples:*
        | IronPort Email Encryption Update PXE Engine |
        """
        self.click_button(UPDATE_NOW_BUTTON)
        self._check_action_result()

    def _set_checkbox_state(self, element, state):
        # Fix for base class method parameters order
        self._set_checkbox(state, element)

    def _get_envelope_profile_controller(self):
        if not hasattr(self, '_envelope_profile'):
            self._envelope_profile = EnvelopeProfile(self)
        return self._envelope_profile
