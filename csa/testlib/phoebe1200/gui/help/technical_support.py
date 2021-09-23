#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/help/technical_support.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
from common.gui.guicommon import Wait

from technical_support_def.contact_techsupport_settings import TechnicalSupportSettings, \
    SEND_BUTTON, DONE_BUTTON
from technical_support_def.contact_techsupport_output_analysis import \
    TechnicalSupportOutputAnalysis

PAGE_PATH = ('Help and Support', 'Contact Technical Support')
TIMEOUT = 60
CCO_NEW_RADIO = "//input[@id='new_cco']"
CCO_EXISTING_RADIO = "//input[@id='existing_cco']"
CCO_NEW_VALUE = "//input[@id='new_cco_name_id']"
CCO_EXISTING_VALUE = "//select[@id='existing_cco_list']"
DELETE_LINK = "//a[contains(text(),'Delete CCO User IDs')]"
DEL_OPT = lambda userid: "//input[@id='%s']" % userid


class TechnicalSupport(GuiCommon):
    """ Keywords for "Help and Support ->Contact Technical Support """

    def get_keyword_names(self):
        return [
            'support_contact_technical_support',
            'delete_cco_user_ids',
        ]

    def _get_cached_controller(self, cls):
        attr_name = '_{0}'.format(cls.__name__.lower())
        if not hasattr(self, attr_name):
            setattr(self, attr_name, cls(self))
        return getattr(self, attr_name)

    @go_to_page(PAGE_PATH)
    def support_contact_technical_support(self, settings, ccoid_option=None, ccoid_value=None):
        """Keywords for "Help and Support ->Contact Technical Support

        *Parameters:*
        - ccoid_option :- Either new or select
        - ccoid_value :- ccoid_value of the CCO user id
        - settings :- This is a dictionary pair as below
        Dictionary with keys:\n
            | `Cisco IronPort Customer Support` |  boolean. ${True} or ${False} |
            | `Other Recipients` |  Optional parameter. string. Multiple email addresses separated with commas. |
            | `Contact Information Name` | string |
            | `Contract ID` | string |
            | `Contact Information Email` | string |
            | `Contact Information Phone1` | Optional parameter. string |
            | `Contact Information Phone2` | Optional parameter. string |
            | `Contact Information Other` | Optional parameter. string |
            | `Technology` | string. Can be one of two values: |
            |       | 'Security - Email and Web' |
            |       | 'Security - Management' |
            | `Sub Technology` | string. Can be one of the following values: |
            |       | 'Cisco Email Security Appliance (C1x0,C3x0, C6x0, X10x0) - Misclassified Messages' |
            |       | 'Cisco Email Security Appliance (C1x0,C3x0, C6x0, X10x0) - SBRS' |
            |       | 'Cisco Email Security Appliance (c1x0,C3x0, C6x0, X10x0) - Other' |
            |       | 'Email Security Appliance - Virtual' |
            | `Problem Code` | string. Can be one of the following values: |
            |       | 'Installation/Software Failure' |
            |       | 'Installation/Password Recovery' |
            |       | 'Installation/Configuration Assistance' |
            |       | 'Installation/Interoperability' |
            |       | 'Installation/Hardware Failure' |
            |       | 'Installation/Software Selection/Download Assistance' |
            |       | 'Installation/Licensing' |
            |       | 'Installation/Data Corruption' |
            |       | 'Installation/Error Messages, Logs' |
            |       | 'Installation/Install, Uninstall or Upgrade' |
            |       | 'Configuration/Data Corruption' |
            |       | 'Configuration/Configuration Assistance' |
            |       | 'Configuration/Password Recovery' |
            |       | 'Configuration/Interoperability' |
            |       | 'Configuration/Hardware Failure' |
            |       | 'Configuration/Error Messages, Logs' |
            |       | 'Configuration/Licensing' |
            |       | 'Configuration/Software Failure' |
            |       | 'Operate/Interoperability' |
            |       | 'Operate/Password Recovery' |
            |       | 'Operate/Licensing' |
            |       | 'Operate/Hardware Failure' |
            |       | 'Operate/Error Messages, Logs' |
            |       | 'Operate/Software Failure' |
            |       | 'Upgrade/Error Messages, Logs' |
            |       | 'Upgrade/Hardware Failure' |
            |       | 'Upgrade/Interoperability' |
            |       | 'Upgrade/Configuration Assistance' |
            |       | 'Upgrade/Install, Uninstall or Upgrade' |
            |       | 'Upgrade/Software Failure' |
            |       | 'Upgrade/Licensing' |
            |       | 'Upgrade/Data Corruption' |
            |       | 'Upgrade/Software Selection/Download Assistance' |
            |       | 'Upgrade/Password Recovery' |
            |       | 'Virtual/Installation' |
            |       | 'Virtual/Licensing' |
            | `Issue Subject` | string |
            | `Issue Description` | string |
            | `Customer Support Case Number` | Optional parameter. string |

        *Examples:*
            | ${support_settings}= | Create Dictionary |
            | ... | Cisco IronPort Customer Support |  ${True} |
            | ... | Other Recipients | test@test.com |
            | ... | Contact Information Email | leon@test.com |
            | ... | Contact Information Phone1 | 0931234567 |
            | ... | Contact Information Phone2 | 0991234567 |
            | ... | Contact Information Other | pager number 123456789 |
            | ... | Technology  Security - Email and Web |
            | ... | Sub Technology | Cisco Email Security Appliance (C1x0,C3x0, C6x0, X10x0) - Misclassified Messages |
            | ... | Problem Code | Configuration/Error Messages, Logs |
            | ... | Issue Subject | Logs cannot be shown |
            | ... | Issue Description | Logs are not shown in CLI |
            | ... | Customer Support Case Number | 123456789 |

            | Support Contact Technical Support |
            | ... | ${support_settings} |
            | ... | ccoid_option=new
            | ... | ccoid_value=contract

        *Return:*
            Dictionary with keys:\n
                - `Sent to`
                - `Contact Information`
                - `Technology`
                - `Sub Technology`
                - `Problem Code`
                - `Issue Description`
                - `Customer Support Case Number`

        """
        settings_controller = self._get_cached_controller(
            TechnicalSupportSettings)
        if ccoid_option == 'new':
            self._info('This is to select a new cco user id')
            self._click_radio_button(CCO_NEW_RADIO)
            self.input_text(CCO_NEW_VALUE, ccoid_value)
        elif ccoid_option == 'select':
            self._info('This is to select an existing cco user id from the list')
            self._click_radio_button(CCO_EXISTING_RADIO)
            self.select_from_list(CCO_EXISTING_VALUE, ccoid_value)
        settings_controller.set(settings)
        self.click_button(SEND_BUTTON)
        Wait(self._is_element_present, timeout=TIMEOUT,
             msg='DONE button did not appear within %d-seconds' \
                 ' timeout after Support Case sending' \
                 % (TIMEOUT)).wait(DONE_BUTTON)
        results_controller = self._get_cached_controller(
            TechnicalSupportOutputAnalysis)
        support_request_content_dict = \
            results_controller.get_element_text_fields()
        self.click_button(DONE_BUTTON)
        return support_request_content_dict

    @go_to_page(PAGE_PATH)
    def delete_cco_user_ids(self, userid):
        """Keywords for "Help and Support ->Contact Technical Support
        Deletes CCO user id 'userid'
        *Parameters:*
        - 'userid' :- Value of the userid to be deleted. String

        Return:
            None

        *Examples:*
        | Delete Cco User Ids | anup |
        """
        self._info('Deleting CCO USER ID %s' % userid)
        self.click_element(DELETE_LINK, "don't wait")
        self._select_checkbox(DEL_OPT(userid))
        self._click_continue_button()
