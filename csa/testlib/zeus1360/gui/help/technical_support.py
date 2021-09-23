#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/help/technical_support.py#1 $
# $DateTime: 2020/03/05 19:45:32 $
# $Author: sarukakk $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
from common.gui.guicommon import Wait

from technical_support_def.contact_techsupport_settings import TechnicalSupportSettings, \
                                                               SEND_BUTTON, DONE_BUTTON

PAGE_PATH = ('Help and Support', 'Contact Technical Support')
TIMEOUT = 60


SEND_TO_IRONPORT_CHECKBOX = 'send_to_cust_support_id'
OTHER_RECIPIENTS_TEXTBOX = 'send_config_to_id'
CUSTOMER_NAME_TEXTBOX = 'customer_name_id'
CUSTOMER_EMAIL_TEXTBOX = 'customer_email_id'
CUSTOMER_PHONE1_TEXTBOX = 'customer_phone1_id'
CUSTOMER_PHONE2_TEXTBOX = 'customer_phone2_id'
CUSTOMER_OTHER_INFO_TEXTBOX = 'customer_other_info_id'
ISSUE_PRIORITY_LIST = 'problem_priority_id'
ISSUE_SUBJECT_TEXTBOX = 'problem_subject_id'
ISSUE_DESCRIPTION_TEXTBOX = 'problem_description_id'
CASE_NUMBER_TEXTBOX = 'ticket_id'
SEND_REQUEST_BUTTON = 'send_request'

class TechnicalSupport(GuiCommon):
    """ Keywords for "Help and Support ->Contact Technical Support """

    def get_keyword_names(self):
        return [
                'support_contact_technical_support',
                ]

    def _open_page(self):
        self._navigate_to('Help and Support', 'Contact Technical Support')

    def _get_techsupport_settings_controller(self):
        if not hasattr(self, '_techsupport_settings_controller'):
            self._techsupport_settings_controller = TechnicalSupportSettings(self)
        return self._techsupport_settings_controller

    @go_to_page(PAGE_PATH)
    def support_contact_technical_support(self, settings={}):
        """
        *Parameters:*
        Dictionary with keys:\n
            | `Cisco IronPort Customer Support` |  boolean. ${True} or ${False} |
            | `Other Recipients` |  Optional parameter. string. Multiple email addresses separated with commas. |
            | `Contact Information Name` | string |
            | `CCO User ID` | string |
            | `Contract ID` | string |
            | `Contact Information Email` | string |
            | `Contact Information Phone1` | Optional parameter. string |
            | `Contact Information Phone2` | Optional parameter. string |
            | `Contact Information Other` | Optional parameter. string |
            | `Technology` | Optional parameter, string |
            | `Sub Technology` | string |
            | `Problem Code` | string |
            | `Issue Subject` | string |
            | `Issue Description` | string |
            | `Customer Support Case Number` | Optional parameter. string |

        *Examples:*
            | ${support_settings}= | Create Dictionary |
            | ... | Cisco IronPort Customer Support |  ${True} |
            | ... | Other Recipients | test@test.com |
            | ... | Contact Information Name | Leon |
            | ... | Contact Information Email | leon@test.com |
            | ... | Contact Information Phone1 | 0931234567 |
            | ... | Contact Information Phone2 | 0991234567 |
            | ... | Contact Information Other | pager number 123456789 |
            | ... | Technology | Security - Management |
            | ... | Sub Technology | Other issue |
            | ... | Problem Code | Password Recovery |
            | ... | Issue Subject | Logs cannot be shown |
            | ... | Issue Description | Logs are not shown in CLI |
            | ... | Customer Support Case Number | 123456789 |

            | Support Contact Technical Support |
            | ... | ${support_settings} |
        """
        controller = self._get_techsupport_settings_controller()
        controller.set(settings)
        self.click_button(SEND_BUTTON)
        Wait(self._is_element_present, timeout=TIMEOUT,
            msg='DONE button did not appear within %d-seconds timeout after Support Case sending'\
                % (TIMEOUT)).wait(DONE_BUTTON)
        self.click_button(DONE_BUTTON)
