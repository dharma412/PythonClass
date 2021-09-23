#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/manager/mail_policies_def/outbreak_filters_entry_settings.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

import re

from common.gui.decorators import set_speed
from common.gui.inputs_owner import get_object_inputs_pairs

from base_policy_entry_settings import BasePolicyEntrySettings

NUM_ATTACHMENTS_VIRAL = "//input[@name='virus_retention']"
METRIC_COMBO_VIRAL = "//select[@name='virus_retention_unit']"
NUM_ATTACHMENTS_OTHER = "//input[@name='threat_retention']"
METRIC_COMBO_OTHER = "//select[@name='threat_retention_unit']"

BYPASS_SCANNING_LINK = "//a[normalize-space()='Bypass Attachment Scanning:']"
BYPASS_EXTS_TABLE = "//table[@id='bypass_exts']"
DELETE_EXT_LINK = "%s//img[@title='Delete...']" % (BYPASS_EXTS_TABLE,)
CONFIRM_DELETE_EXT_BUTTON = \
    "//div[@id='confirmation_dialog']" \
    "//button[normalize-space()='Delete']"
MANUAL_EXT_INPUT_RADIO = "//input[@id='add_new_type']"
ADD_EXT = "//input[@id='add_type_field']"
ADD_EXT_BUTTON = "//input[@id='AddExtension']"


class OutbreakFiltersEntrySettings(BasePolicyEntrySettings):
    ENABLE_AS_COMBO = ('Outbreak Filters', "//select[@id='enable_AOF']")
    QUARANTINE_QTL_COMBO = ('Quarantine Threat Level',
                            "//select[@id='quarantine_gtl']")
    MAXIMUM_QUAR_RETENTION_VIRAL = \
        ('Maximum Quarantine Retention for Viral Attachments',
         None)
    MAXIMUM_QUAR_RETENTION_OTHER = \
        ('Maximum Quarantine Retention for Other Threats',
         None)
    BYPASS_ATTACHMENT_SCANNING = ('Bypass Attachment Scanning for',
                                  None)
    DELIVER_MESSAGES_WITHOUT_QUARANTINE_CHECKBOX = \
        ('Deliver Messages without Quarantining',
         "//input[@id='threat_deliver_without_quarantine']")
    ENABLE_THREAT_OPTIONS_CHECKBOX = ('Enable Message Modification',
                                      "//input[@id='enable_threat_options']")
    MSG_MODIF_THREAT_LEVEL_COMBO = ('Message Modification Threat Level',
                                    "//select[@id='modify_gtl']")
    MODIFIED_MESSAGE_SUBJECT_ACTION = ('Modified Message Subject Action',
                                       "//select[@id='threat_subject_action']")
    MODIFIED_MESSAGE_SUBJECT = ('Modified Message Subject',
                                "//input[@id='threat_subject_text']")
    INCLUDE_IRONPORT_OUTBREAK_HEADERS_RADIOGROUP = \
        ('Include the X-IronPort-Outbreak headers', \
         {'Enable only for threat-based outbreak': \
              "//input[@id='threat_status_header_outbreaks']", \
          'Enable for all messages': \
              "//input[@id='threat_status_header_all']", \
          'Disable': "//input[@id='threat_status_header_none']"})
    INCLUDE_IRONPORT_OUTBREAK_DESCRIPTION_RADIOGROUP = \
        ('Include the X-IronPort-Outbreak-Description header', \
         {'Enable': "//input[@id='threat_description_header_enable']",
          'Disable': "//input[@id='threat_description_header_disable']"})
    ALTERNATE_DESTINATION_HOST = \
        ('Alternate Destination Mail Host', \
         "//input[@id='threat_alt_mail_host']")
    URL_REWRITING_RADIOGROUP = ('URL Rewriting',
                                {'Enable only for unsigned messages': "//input[@id='rewrite_unsigned']",
                                 'Enable for all messages': "//input[@id='rewrite_all']",
                                 'Disable': "//input[@id='rewrite_none']"})
    BYPASS_DOMAIN_SCANNING = ('Bypass Domain Scanning for',
                              "//textarea[@id='preserve_domains']")
    THREAT_DISCLAIMER_COMBO = ('Threat Disclaimer',
                               "//select[@id='threat_disclaimer_resource']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def _set_minimum_quar_retention(self, value_to_set,
                                    count_input_locator,
                                    units_combo_locator):
        match = re.search(r'(\d+)\s+(\w+)', value_to_set)
        if not match:
            raise ValueError('Unexpected value "%s". ' \
                             'It should include count and units name' % (value_to_set,))
        attachments_count = match.group(1)
        self.gui.input_text(count_input_locator, attachments_count)
        units = match.group(2).capitalize()
        self.gui.select_from_list(units_combo_locator, units)

    def _set_bypass_attachment_scanning(self, exts_list):
        self.gui.click_button(BYPASS_SCANNING_LINK, 'don\'t wait')
        # Cleaning existing extensions in list
        while self.gui._is_element_present(DELETE_EXT_LINK):
            self.gui.click_button(DELETE_EXT_LINK, 'don\'t wait')
            self.gui.click_button(CONFIRM_DELETE_EXT_BUTTON, 'don\'t wait')
        self.gui._click_radio_button(MANUAL_EXT_INPUT_RADIO)
        for ext in exts_list:
            self.gui.input_text(ADD_EXT, ext)
            self.gui.click_button(ADD_EXT_BUTTON, 'don\'t wait')

    @set_speed(0, 'gui')
    def set(self, new_value):
        super(OutbreakFiltersEntrySettings, self).set(new_value)

        self._set_combos(new_value,
                         self.ENABLE_AS_COMBO,
                         self.QUARANTINE_QTL_COMBO)
        self._set_checkboxes(new_value,
                             self.ENABLE_THREAT_OPTIONS_CHECKBOX,
                             self.DELIVER_MESSAGES_WITHOUT_QUARANTINE_CHECKBOX)
        if self.MAXIMUM_QUAR_RETENTION_VIRAL[0] in new_value:
            self._set_minimum_quar_retention(
                new_value[self.MAXIMUM_QUAR_RETENTION_VIRAL[0]],
                NUM_ATTACHMENTS_VIRAL,
                METRIC_COMBO_VIRAL)
        if self.MAXIMUM_QUAR_RETENTION_OTHER[0] in new_value:
            self._set_minimum_quar_retention(
                new_value[self.MAXIMUM_QUAR_RETENTION_OTHER[0]],
                NUM_ATTACHMENTS_OTHER,
                METRIC_COMBO_OTHER)
        if self.BYPASS_ATTACHMENT_SCANNING[0] in new_value:
            value_to_set = map(lambda x: x.strip(),
                               new_value[self.BYPASS_ATTACHMENT_SCANNING[0]].split(','))
            self._set_bypass_attachment_scanning(value_to_set)
        self._set_combos(new_value,
                         self.MSG_MODIF_THREAT_LEVEL_COMBO,
                         self.MODIFIED_MESSAGE_SUBJECT_ACTION,
                         self.THREAT_DISCLAIMER_COMBO)
        self._set_edits(new_value,
                        self.MODIFIED_MESSAGE_SUBJECT)
        self._set_radio_groups(new_value,
                               self.INCLUDE_IRONPORT_OUTBREAK_HEADERS_RADIOGROUP,
                               self.INCLUDE_IRONPORT_OUTBREAK_DESCRIPTION_RADIOGROUP)
        self._set_edits(new_value, self.ALTERNATE_DESTINATION_HOST)
        self._set_radio_groups(new_value,
                               self.URL_REWRITING_RADIOGROUP)
        self._set_edits(new_value,
                        self.BYPASS_DOMAIN_SCANNING)
