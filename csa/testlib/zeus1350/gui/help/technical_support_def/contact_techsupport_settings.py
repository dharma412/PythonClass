#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/help/technical_support_def/contact_techsupport_settings.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

SEND_BUTTON = "//input[@type='button' and @value='Send']"
DONE_BUTTON = "//form[@id='form']//input[@class='button' and contains(@value, 'Done')]"

CISCO_CUSTOMER_SUPPORT_CHECKBOX = ('Cisco IronPort Customer Support',
                                   "//table[@id='content-container']//input[@id='send_to_cust_support_id']")

OTHER_RECIPIENTS = ('Other Recipients', "//input[@id='send_config_to_id']")

CCO_USER_ID = ('CCO User ID', "//input[@id='new_cco_name_id']")
CONTRACT_ID = ('Contract ID', "//input[@id='contract_number_id']")
CONTACT_INFO_NAME = ('Contact Information Name', "//input[@id='customer_name_id']")
CONTACT_INFO_EMAIL = ('Contact Information Email', "//input[@id='customer_email_id']")
CONTACT_INFO_PHONE1 = ('Contact Information Phone1', "//input[@id='customer_phone1_id']")
CONTACT_INFO_PHONE2 = ('Contact Information Phone2', "//input[@id='customer_phone2_id']")
CONTACT_INFO_OTHER = ('Contact Information Other', "//input[@id='customer_other_info_id']")

TECHNOLOGY = ('Technology', 'xpath=//select [@id="technology"]')
SUB_TECHNOLOGY = ('Sub Technology', 'xpath=//select [@id="sub_technology"]')
PROBLEM_CODE = ('Problem Code', 'xpath=//select [@id="problem_code"]')

ISSUE_SUBJECT = ('Issue Subject', "//input[@id='problem_subject_id']")
ISSUE_DESCRIPTION = ('Issue Description', "//textarea[@id='problem_description_id']")

CUSTOMER_SUPPORT_CASE_NUMBER = ('Customer Support Case Number', "//input[@id='ticket_id']")


class TechnicalSupportSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                             CISCO_CUSTOMER_SUPPORT_CHECKBOX)

        self._set_edits(new_value,
                        OTHER_RECIPIENTS,
                        CONTACT_INFO_NAME,
                        CCO_USER_ID,
                        CONTRACT_ID,
                        CONTACT_INFO_EMAIL,
                        CONTACT_INFO_PHONE1,
                        CONTACT_INFO_PHONE2,
                        CONTACT_INFO_OTHER,
                        ISSUE_SUBJECT,
                        ISSUE_DESCRIPTION,
                        CUSTOMER_SUPPORT_CASE_NUMBER)
        self._set_combos(new_value,
                         TECHNOLOGY,
                         SUB_TECHNOLOGY,
                         PROBLEM_CODE,
                         )

    def get(self):
        raise NotImplementedError()
