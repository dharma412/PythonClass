#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/help/technical_support_def/contact_techsupport_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs, \
    check_new_settings

SEND_BUTTON = "//input[@type='button' and @value='Send']"
DONE_BUTTON = "//form[@id='form']//input[@class='button' and contains(@value, 'Done')]"

CISCO_CUSTOMER_SUPPORT_CHECKBOX = ('Cisco IronPort Customer Support',
                                   "//table[@id='content-container']//input[@id='send_to_cust_support_id']")
TECHNILOGY_COMBO = ('Technology', "//select[@id='technology']")
SUB_TECHNILOGY_COMBO = ('Sub Technology', "//select[@id='sub_technology']")
PROBLEM_CODE_COMBO = ('Problem Code', "//select[@id='problem_code']")

OTHER_RECIPIENTS = ('Other Recipients', "//input[@id='send_config_to_id']")

CONTACT_INFO_NAME = ('Contact Information Name', "//input[@id='customer_name_id']")
CONTACT_INFO_EMAIL = ('Contact Information Email', "//input[@id='customer_email_id']")
CONTACT_INFO_PHONE1 = ('Contact Information Phone1', "//input[@id='customer_phone1_id']")
CONTACT_INFO_PHONE2 = ('Contact Information Phone2', "//input[@id='customer_phone2_id']")
CONTACT_INFO_OTHER = ('Contact Information Other', "//input[@id='customer_other_info_id']")

ISSUE_SUBJECT = ('Issue Subject', "//input[@id='problem_subject_id']")
ISSUE_DESCRIPTION = ('Issue Description', "//textarea[@id='problem_description_id']")

CUSTOMER_SUPPORT_CASE_NUMBER = ('Customer Support Case Number', "//input[@id='ticket_id']")

ESA_SUBGROUPS_LOCATOR = "//select[@id='problem_code']//optgroup[@label]"
ESA_VIRTUAL_LOCATOR = "//select[@id='problem_code']"

ALL_VALUES_COUNT = lambda subgroups_locator, subgroup_idx: \
    "%s[%s]//option[@value]" % (subgroups_locator, subgroup_idx)
VALUE_ELEMENT = lambda subgroups_locator, subgroup_idx, value_idx: \
    "%s[%s]//option[%s]@value" % (subgroups_locator, subgroup_idx, value_idx)
CONTRACT_VALUE = ('Contract ID', "//input[@id='contract_number_id']")


class TechnicalSupportSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                             CISCO_CUSTOMER_SUPPORT_CHECKBOX, )

        self._set_combos(new_value,
                         TECHNILOGY_COMBO,
                         SUB_TECHNILOGY_COMBO)

        self._set_edits(new_value,
                        OTHER_RECIPIENTS,
                        CONTRACT_VALUE,
                        CONTACT_INFO_NAME,
                        CONTACT_INFO_EMAIL,
                        CONTACT_INFO_PHONE1,
                        CONTACT_INFO_PHONE2,
                        CONTACT_INFO_OTHER,
                        ISSUE_SUBJECT,
                        ISSUE_DESCRIPTION,
                        CUSTOMER_SUPPORT_CASE_NUMBER)

        if new_value.has_key(PROBLEM_CODE_COMBO[0]):
            all_problem_code_options = self._get_all_available_problem_code_options()
            value_to_set = new_value[PROBLEM_CODE_COMBO[0]]
            if value_to_set not in all_problem_code_options:
                raise ValueError('There is no option named "%s" in ' \
                                 'setting "%s"' % (value_to_set,
                                                   PROBLEM_CODE_COMBO[0]))
            self.gui.select_from_list(PROBLEM_CODE_COMBO[1], value_to_set)

    def get(self):
        raise NotImplementedError()

    def _get_all_available_problem_code_options(self):
        if self.gui._is_element_present(ESA_SUBGROUPS_LOCATOR):
            subgroups_locator = ESA_SUBGROUPS_LOCATOR
            all_subgroups_count = int(self.gui.get_matching_xpath_count(ESA_SUBGROUPS_LOCATOR))
            first_value_idx = 1
        else:
            subgroups_locator = ESA_VIRTUAL_LOCATOR
            all_subgroups_count = 1
            first_value_idx = 2

        all_problem_code_options = []
        for subgroup_idx in xrange(1, all_subgroups_count + 1):
            all_values_count = int(self.gui.get_matching_xpath_count(ALL_VALUES_COUNT(subgroups_locator, subgroup_idx)))
            for value_idx in xrange(first_value_idx, all_values_count + 1):
                value_element = self.gui.get_element_attribute(
                    VALUE_ELEMENT(subgroups_locator, subgroup_idx, value_idx))
                all_problem_code_options.append(value_element)
        return all_problem_code_options
