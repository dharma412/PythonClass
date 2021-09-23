#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/mail_policies_def/antispam_entry_settings.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import get_object_inputs_pairs
from common.util.ordered_dict import OrderedDict

from base_policy_entry_settings import BasePolicyEntrySettings


class AntispamEntrySettings(BasePolicyEntrySettings):
    ENABLE_AS_RADIOGROUP = ('Anti-Spam Scanning',
        {'Use Default Settings': "//input[@id='default_as']",
         'Use selected Anti-Spam services': "//input[@id='override_as']",
         'Use IronPort Intelligent Multi-Scan': "//input[@id='ims_as']",
         'Use IronPort Anti-Spam service': "//input[@id='case_as']",
         'Disabled': "//input[@id='no_as']"})
    USE_CASE_CHECKBOX = ('Use IronPort Anti-Spam',
                         "//input[@id='CASE']")
    USE_CLOUDMARK_CHECKBOX = ('Use Cloudmark Service Provider',
                              "//input[@id='Cloudmark']")
    ENABLE_SUSPECTED_SCANNING_RADIOGROUP = ('Enable Suspected Spam Scanning',
                                    {'No': "//input[@id='disable_sus']",
                                     'Yes': "//input[@id='enable_sus']"})

    CATEGORY_ITEMS_MAPPING = OrderedDict(
        [('Apply Action', ("//select[@id='{0}_action']", '_set_combos')),
         ('Alternate Host', ("//input[@id='{0}DivertHost']", '_set_edits')),
         ('Subject Text Action', ("//select[@id='{0}SubjectAction']",
                                  '_set_combos')),
         ('Add Subject Text', ("//input[@id='{0}SubjectText']",
                               '_set_edits')),
         ('Add Custom Header Name', ("//input[@name='{0}HeaderName']",
                                     '_set_edits')),
         ('Add Custom Header Text', ("//input[@name='{0}HeaderText']",
                                     '_set_edits')),
         ('Alternate Envelope Recipient', ("//input[@name='{0}AltRcptTo']",
                                           '_set_edits')),
         ('Archive Message', ({'No': "//input[@id='{0}_archive_no']",
                               'Yes': "//input[@id='{0}_archive_yes']"},
                              '_set_radio_groups'))])
    CATEGORIES_PREFIXES_MAPPING = {'pos': 'Positive Spam',
                                   'sus': 'Suspected Spam'}
    THRESHOLD_ITEMS_MAPPING = OrderedDict(
        [('Spam Thresholds', (
            {'Use the Default Thresholds': "//input[@id='recommended_{0}']",
             'Use Custom Settings': "//input[@id='custom_{0}']"},
                              '_set_radio_groups')),
         ('Positive Spam Score', ("//input[@id='threshold_pos_{0}']",
                                  '_set_edits')),
         ('Suspected Spam Score', ("//input[@id='threshold_sus_{0}']",
                                   '_set_edits'))])
    THRESHOLD_PREFIXES_MAPPING = \
        {'CASE': 'CASE',
         'Cloudmark': 'Cloudmark',
         'IMS': 'IMS'}

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self) + \
                    self._generate_common_settings_pairs(
                                    self.CATEGORY_ITEMS_MAPPING,
                                    self.CATEGORIES_PREFIXES_MAPPING) + \
                    self._generate_common_settings_pairs(
                                    self.THRESHOLD_ITEMS_MAPPING,
                                    self.THRESHOLD_PREFIXES_MAPPING)

    @set_speed(0, 'gui')
    def set(self, new_value):
        super(AntispamEntrySettings, self).set(new_value)

        self._set_radio_groups(new_value,
                               self.ENABLE_AS_RADIOGROUP,
                               self.ENABLE_SUSPECTED_SCANNING_RADIOGROUP)
        self._set_checkboxes(new_value,
                             self.USE_CLOUDMARK_CHECKBOX,
                             self.USE_CASE_CHECKBOX)
        self._fill_categories_settings(new_value,
                                       self.CATEGORY_ITEMS_MAPPING,
                                       self.CATEGORIES_PREFIXES_MAPPING)
        self._fill_categories_settings(new_value,
                                       self.THRESHOLD_ITEMS_MAPPING,
                                       self.THRESHOLD_PREFIXES_MAPPING)
