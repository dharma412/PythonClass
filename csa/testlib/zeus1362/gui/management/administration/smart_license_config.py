#!/usr/bin/env python -tt
#$Id: //prod/main/sarf_centos/testlib/zeus1362/gui/management/administration/smart_license_config.py#1 $
#$DateTime: 2020/06/10 22:29:20 $
#$Author: sarukakk $

import functools
import re

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon, Wait
import common.gui.guiexceptions as guiexceptions

ENABLE_BUTTON = "//input[@id='enable_sl']"
ENABLE_OK_BUTTON = "//input[@id='sl_ok']"
URL_EDIT_BUTTON = "//a[contains(@onclick, 'sl_transport_settings_edit')]"
DIRECT_RADIO = "//input[@id='transport_direct_tb']"
TRNSPORT_GATEWAY_RADIO = "//input[@id='transport_gateway_tb']"
TG_URL_TEXTBOX =  "//input[@id='transport_gateway_url']"
TG_OK_BUTTON  = "//button[@id='yui-gen21-button']"
REGISTER_SSM_BUTTON = "//input[@id='register']"
TOKEN_TEXTBOX = "//input[@id='register_token']"
REGISTER_BUTTON = "//input[@value='Register']"
REGISTER_IF_ALREADY_REGISTERED_CHECKBOX="//input[@id='Checkbox']"
ACTION_COMBO = "//select[@id='config_action']"
ACTION = "//input[@value='Go']"
REMOVE_AND_REGISTER_BUTTON= "//button[text()='Remove and Register']"
DEREGISTER_CONFIRM_BUTTON  = "//button[contains(text(),'Submit')]"

SMART_LICENSING_TABLE = "//table[@class='pairs']"
HEADER_NAMES = "%s/tbody/tr[th]/th" % (SMART_LICENSING_TABLE,)
# idx starts from 1
HEADER_BY_IDX = lambda row: '%s//tr[%s]/th' % (SMART_LICENSING_TABLE, row)
ROW_BY_IDX = lambda row: '%s//tr[%s]/td' % (SMART_LICENSING_TABLE, row)

PAGE_PATH = ('System Administration', 'Smart Software Licensing')

def check_smart_licensing(need_to_raise_exc):
    """This decorator is used to navigate and check  if smart
    licensing is enabled

    *Parameters:*
    - `need_to_raise_exc`: whether to raise GuiFeatureDisabledError if
    smart licensing is disabled. Either True or False

    *Exceptions:*
    - `GuiFeatureDisabledError`: if smart licensing is disabled
    and need_to_raise_exc is set to True
    """
    def decorator(func):
        @functools.wraps(func)
        def worker(self, *args, **kwargs):
            if not self.smart_license_is_enabled():
                if need_to_raise_exc:
                    raise guiexceptions.GuiFeatureDisabledError(
                        'smart licensing is not enabled')
            return func(self, *args, **kwargs)
        return worker
    return decorator

class SmartLicenseConfig(GuiCommon):
    """Keywords for SMA GUI interaction with 'System Administration-->
       Smart Software Licensing'
    """

    def get_keyword_names(self):
        return ['smart_license_enable',
                'smart_license_is_enabled',
                'smart_license_configure_url',
                'smart_license_register',
                'smart_license_get_status_details',
                'smart_license_perform_action']

    def _register(self, *args):
        settings = self._parse_args(args)
        if settings:
            if not settings.has_key('sl_action'):
                if self._is_element_present(REGISTER_SSM_BUTTON):
                    self.click_button(REGISTER_SSM_BUTTON)
                else:
                    raise GuiControlNotFoundError('Register option is not available')

            if settings.has_key('token_id'):
                self.input_text(TOKEN_TEXTBOX, settings['token_id'])
            else:
                raise ValueError('Token id is mandatory for registration/reregistration')

            if settings.has_key('force_register_flag'):
                if settings['force_register_flag'] is True:
                    self._select_checkbox(REGISTER_IF_ALREADY_REGISTERED_CHECKBOX)
                else:
                    self._unselect_checkbox(REGISTER_IF_ALREADY_REGISTERED_CHECKBOX)

            if self._is_element_present(REGISTER_BUTTON):
                self.click_button(REGISTER_BUTTON, 'don\'t wait')
                if settings.has_key('sl_action'):
                    if self._is_element_present(REMOVE_AND_REGISTER_BUTTON):
                        self.click_button(REMOVE_AND_REGISTER_BUTTON)
                    else:
                        raise GuiControlNotFoundError('Confirmation message is not displayed')
            else:
                raise GuiControlNotFoundError('Register button is not available')

    def _get_updated_result(self, result):
        """Helper function
          It splits the following values and creates new key, value paris
          Input Dictionary:
             {u'Evaluation Period Remaining': u'89 days, 4 hr, 54 min, 42 sec',
              u'Evaluation Period': u'Not In Use',
              u'Registration Status':u'Registered ( 22 Aug 2018 07:21)
                Registration Expires on: 22 Aug 2019 07:15',
              u'License Authorization Status: u'Out_of_compliance
               ( 22 Aug 2018 07:21) Authorization Expires on : 20 Nov 2018 07:15',
              u'Last Authorization Renewal Attempt Status: u'SUCCEEDED on 22 Aug 2018 07:21',
              u'Last Registration Renewal Attempt Status: u'SUCCEEDED on 22 Aug 2018 16:22',
              u'Transport Settings': u'Direct (https://smartreceiver.cisco.com/licservice/license) (Edit)'
              u'Smart Account': u'InternalTestDemoAccount9.cisco.com',
              u'Product Instance Name': u'vm30sma0011.ibqa',
              u'Virtual Account': u'SMA'}

          Output Dictionary:
             {u'Evaluation Period Remaining': u'89 days, 4 hr, 54 min, 42 sec',
              u'Evaluation Period': u'Not In Use',
              u'Registration Status': u'Registered',
              u'License Authorization Status': u'Authorized',
              u'Last Registration Renewal Status': u'SUCCEEDED',
              u'Last Registration Renewal Date': u'18 Aug 2018 07:25',
              u'Last Authorization Renewal Status': u'SUCCEEDED',
              u'Last Authorization Renewal Date': u'21 Aug 2018 11:40',
              u'Transport Settings': u'Direct',
              u'Smart Account': u'InternalTestDemoAccount9.cisco.com',
              u'Product Instance Name': u'vm30sma0011.ibqa',
              u'Virtual Account': u'SMA'}

        """
        new_result_dict = {}
        for key, value in result.items():
            if key == 'Transport Settings':
               val = re.split('\s\(', value)[0]
               new_result_dict[key] = val
               continue;
            if key == 'Registration Status' or \
                key == 'License Authorization Status':
                if not ('Unregistered' in value or \
                       'Evaluation Mode' in value or \
                       'No License In Use' in value):
                    val = re.split(" ", value, 1)[0]
                    new_result_dict[key] = val
                    continue;
            if key == 'Last Authorization Renewal Attempt Status' or \
                key == 'Last Registration Renewal Attempt Status':
                if value != 'No communication attempted':
                    key = key.rsplit(' ', 2)[0]
                    val = re.split(' ', value, 2)
                    new_result_dict["".join('%s Status' % key)] = val[0]
                    new_result_dict["".join('%s Date' % key)] = val[2]
                    continue;
            new_result_dict[key] = value
        return new_result_dict

    @go_to_page(PAGE_PATH)
    def smart_license_enable(self):
        """Enables SmartLicensing license mode

        *Parameters:*
         None

        *Examples:*
        | Smart License Enable |

        """
        if self._is_element_present(ENABLE_BUTTON):
            self.click_button(ENABLE_BUTTON)
            if self._is_element_present(ENABLE_OK_BUTTON):
                self.click_button(ENABLE_OK_BUTTON)
            else:
                raise GuiControlNotFoundError('Confirmation message is not displayed')
        else:
            raise GuiControlNotFoundError('Enable option is not available')

    @go_to_page(PAGE_PATH)
    def smart_license_is_enabled(self):
        """Get current smart license enabled status

        *Parameters:*
        None

        *Return*
        True or False: whether smart license are enabled or disabled

        *Examples:*
        | ${status}= | Smart License Is Enabled |
        """
        return (not self._is_element_present(ENABLE_BUTTON))

    @check_smart_licensing(True)
    @go_to_page(PAGE_PATH)
    def smart_license_configure_url(self, *args):
        """Configure URL

        *Parameters:*
        - transport_setting': direct or transport_gateway
        - url': url of transport gateway/satellite.


        *Examples:*
        | Smart License Configure URL                 |
        | ... | transport_settings=transport_gateway  |
        | ... | url=${url}                            |

        | Smart License Configure URL      |
        | ... | transport_settings=direct  |
        """
        settings = self._parse_args(args)
        transport_settings = settings['transport_settings']
        if settings:
            self.click_button(URL_EDIT_BUTTON, 'don\'t wait')
            if transport_settings.lower() == 'direct':
                self._click_radio_button(DIRECT_RADIO)
            elif transport_settings.lower() == 'transport_gateway':
                if settings.has_key('url'):
                    self._click_radio_button(TRNSPORT_GATEWAY_RADIO)
                    self.input_text(TG_URL_TEXTBOX, settings['url'])
                else:
                    raise ValueError('url argument is mandatory for "%s" option' % \
                                 (transport_setting,))
            else:
                raise ValueError('Unknown option "%s" is passed' % (transport_settings,))
            self.click_button(TG_OK_BUTTON)

    @check_smart_licensing(True)
    @go_to_page(PAGE_PATH)
    def smart_license_register(self, *args):
        """Registers DUT with Software Smart Manager

        *Parameters:*
         - token_id: Token Id used for registering the product
           with Smart Software Manager
         - force_register_flag: Boolean flag to Reregister the
           product instance if it is already registered
           Default value: ${False}

        *Examples:*
        | Smart License Register   |
        |... |token_id=${token_id} |

        | Smart License Register           |
        |... |token_id=${token_id}         |
        |... |force_register_flag=${True}  |

        | Smart License Register            |
        |... |token_id=${token_id}          |
        |... | force_register_flag=${False} |

        """
        self._register(*args)

    @check_smart_licensing(True)
    @go_to_page(PAGE_PATH)
    def smart_license_get_status_details(self):
        """
        Get Smart License Status Details

        *Parameters*:
        None

        *Examples*:
         |${details}= | Smart License Get Status Details|
         |${trans}=  | Get From Dictionary              |
         |...  | ${details}  Transport Settings         |

        """
        result = {}
        headers_count = int(self.get_matching_xpath_count(HEADER_NAMES))
        for col_idx in xrange(1, headers_count + 1):
            header = self.get_text(HEADER_BY_IDX(col_idx)).strip()
            header = header.strip(':')
            result[header] = []
            cell_text = self.get_text(ROW_BY_IDX(col_idx)).strip()
            result[header] = cell_text
        del result['Action']
        new_result = self._get_updated_result(result)
        return new_result

    @check_smart_licensing(True)
    @go_to_page(PAGE_PATH)
    def smart_license_perform_action(self, *args):
        """
        Perform Smart Licensing actions:
        1) Renew authorization manually
        2) Renew certificate manually
        3) Reregister
        4) Deregister

        *Parameters*:
        - sl_action: type of SL action
        - token_id: Token Id used for reregistering the product
           with Smart Software Manager
        - force_register_flag: Boolean flag to Reregister the
           product instance if it is already registered
           Default value: ${False}

         *Examples:*
        | Smart License Perform Action |
        |... | sl_action='renew authorization now'  |

        | Smart License Perform Action |
        |... |sl_action='renew certificates now'   |

        | Smart License Perform Action |
        |...  |sl_action='deregister'  |

        | Smart License Perform Action |
        | sl_action='reregister'       |
        |...  | token_id=${token_id}        |

        """
        kwargs = self._parse_args(args)
        sl_action = kwargs['sl_action']
        if sl_action.lower() == 'renew authorization now':
            self.select_from_list(ACTION_COMBO,sl_action)
            self.click_button(ACTION)
        elif sl_action.lower() == 'renew certificates now':
            self.select_from_list(ACTION_COMBO,sl_action)
            self.click_button(ACTION)
        elif sl_action.lower() == 'deregister':
            self.select_from_list(ACTION_COMBO,sl_action)
            self.click_button(ACTION, 'don\'t wait')
            self.click_button(DEREGISTER_CONFIRM_BUTTON)
        elif sl_action.lower() == 'reregister':
            self.select_from_list(ACTION_COMBO,sl_action)
            self.click_button(ACTION)
            self._register(*args)
        else:
            raise ValueError('Unknown option "%s" is passed' % (sl_action,))
