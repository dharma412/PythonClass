#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/mail_policies_def/antivirus_entry_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $


from common.gui.decorators import set_speed
from common.gui.inputs_owner import get_object_inputs_pairs
from common.util.ordered_dict import OrderedDict

from base_policy_entry_settings import BasePolicyEntrySettings


class AntivirusEntrySettings(BasePolicyEntrySettings):
    ENABLE_AS_RADIOGROUP = ('Anti-Virus Scanning',
                            {'Use Default Settings': "//input[@id='enable_avDefault']",
                             'Yes': "//input[@id='enable_avYes']",
                             'No': "//input[@id='enable_avNo']"})
    USE_SOPHOS_CHECKBOX = ('Use Sophos Anti-Virus',
                           "//input[@id='Sophos']")
    USE_MCAFEE_CHECKBOX = ('Use McAfee Anti-Virus',
                           "//input[@id='McAfee']")
    MESSAGE_SCANNING_ACTION_COMBO = ('Message Scanning Action',
                                     "//select[@id='clean']")
    DROP_ATTACHEMENTS_CHECKBOX = ('Drop Attachments',
                                  "//input[@id='drop_attachments']")
    INCLUDE_X_HEADER_CHECKBOX = ('Include X-header',
                                 "//input[@id='include_X_header']")
    CATEGORY_ITEMS_MAPPING = OrderedDict([
        ('Apply Action', ("//select[@id='{0}_action']", '_set_combos')),
        ('Archive Original', ({'No': "//input[@id='{0}_archive0']",
                               'Yes': "//input[@id='{0}_archive1']"},
                              '_set_radio_groups')),
        ('Modify Subject', ({'No': "//input[@id='{0}_subj_no']",
                             'Prepend': "//input[@id='{0}_subj_pre']",
                             'Append': "//input[@id='{0}_subj_app']"},
                            '_set_radio_groups')),
        ('Add Subject Text', ("//input[@id='{0}_subj_txt']",
                              '_set_edits')),
        ('Add Custom Header', ({'Yes': "//input[@id='{0}_hdr_yes']",
                                'No': "//input[@id='{0}_hdr_no']"},
                               '_set_radio_groups')),
        ('Add Custom Header Name', ("//input[@id='{0}__hdr_n']",
                                    '_set_edits')),
        ('Add Custom Header Value', ("//input[@id='{0}__hdr_t']",
                                     '_set_edits')),
        ('Container Notification', ("//select[@id='{0}_msg_text_tmpl_id']",
                                    '_set_combos')),
        ('Other Notification Rcpt Sender', ("//input[@id='{0}_generic_sender']",
                                            '_set_checkboxes')),
        ('Other Notification Rcpt Recipient', ("//input[@id='{0}_generic_recipient']",
                                               '_set_checkboxes')),
        ('Other Notification Rcpt Others', ("//input[@id='{0}_generic_other']",
                                            '_set_checkboxes')),
        ('Other Notification Rcpt Others Emails',
         ("//input[@id='{0}_notify_other_text']", '_set_edits')),
        ('Other Notification Template', ("//select[@id='{0}_notify_text_tmpl_id']",
                                         '_set_combos')),
        ('Other Notification Subject', ("//input[@id='{0}notify_subject']",
                                        '_set_edits')),
        ('Modify Recipient', ({'Yes': "//input[@id='{0}_rbyes']",
                               'No': "//input[@id='{0}_rbno']"},
                              '_set_radio_groups')),
        ('Modified Recipient Address', ("//input[@id='{0}_rbaddr']",
                                        '_set_edits')),
        ('Send To Alternate Host', ({'Yes': "//input[@id='{0}_altyes']",
                                     'No': "//input[@id='{0}_altno']"},
                                    '_set_radio_groups')),
        ('Alternate Host', ("//input[@id='{0}_alttxt']",
                            '_set_edits'))])
    CATEGORIES_PREFIXES_MAPPING = {'safe': 'Repaired Messages',
                                   'enc': 'Encrypted Messages',
                                   'unscan': 'Unscannable Messages',
                                   'unsafe': 'Virus Infected Messages'}

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self) + \
               self._generate_common_settings_pairs(
                   self.CATEGORY_ITEMS_MAPPING,
                   self.CATEGORIES_PREFIXES_MAPPING)

    @set_speed(1, 'gui')
    def set(self, new_value):
        super(AntivirusEntrySettings, self).set(new_value)

        self._set_radio_groups(new_value,
                               self.ENABLE_AS_RADIOGROUP)
        self._set_checkboxes(new_value,
                             self.USE_MCAFEE_CHECKBOX,
                             self.USE_SOPHOS_CHECKBOX)
        self._set_combos(new_value,
                         self.MESSAGE_SCANNING_ACTION_COMBO)
        self._set_checkboxes(new_value,
                             self.DROP_ATTACHEMENTS_CHECKBOX,
                             self.INCLUDE_X_HEADER_CHECKBOX)
        self._fill_categories_settings(new_value,
                                       self.CATEGORY_ITEMS_MAPPING,
                                       self.CATEGORIES_PREFIXES_MAPPING)
