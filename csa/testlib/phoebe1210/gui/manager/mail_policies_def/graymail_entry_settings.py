#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/manager/mail_policies_def/graymail_entry_settings.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import get_object_inputs_pairs
from common.util.ordered_dict import OrderedDict

from base_policy_entry_settings import BasePolicyEntrySettings


class GraymailEntrySettings(BasePolicyEntrySettings):
    ENABLE_GRAYMAIL_DETECTION_RADIOGROUP = (
        'Graymail Detection',
        {'Use Default Settings': "//input[@id='enable_gm_default']",
         'Use Graymail Detection': "//input[@id='enable_gm_yes']",
         'Disable Graymail Detection': "//input[@id='enable_gm_no']"},
    )
    ENABLE_GRAYMAIL_UNSUBSCRIPTION_RADIOGROUP = (
        'Graymail Un-subscription', {
            'Use Graymail Un-subscription': "//input[@id='enable_unsubscription_yes']",
            'Disable Graymail Un-subscription': "//input[@id='enable_unsubscription_no']", }
    )
    GRAYMAIL_UNSUBSCRIPTION_PERFORM_ACTION_RADIOGROUP = (
        'Perform this action for', {
            'All Messages': "//input[@id='unsubscribe_all']",
            'Unsigned Messages': "//input[@id='unsubscribe_signed']", }
    )
    ENABLE_MARKETING_SCANNING_CHECKBOX = ('Enable Marketing Email Scanning',
                                          "//input[@id='marketing_enable_action']")

    ENABLE_SOCIAL_NETWORKING_SCANNING_CHECKBOX = ('Enable Social Networking Email Scanning',
                                                  "//input[@id='social_enable_action']")

    ENABLE_BULK_SCANNING_CHECKBOX = ('Enable Bulk Email Scanning',
                                     "//input[@id='bulk_enable_action']")
    CATEGORY_ITEMS_MAPPING = OrderedDict(
        [('Apply Action', ("//select[@id='{0}_action']", '_set_combos')),
         ('Alternate Host', ("//input[@id='{0}_alt_host_email']", '_set_edits')),
         ('Subject Text Action', ({'No': "//input[@id='{0}_subj_no']",
                                   'Prepend': "//input[@id='{0}_subj_prepend']",
                                   'Append': "//input[@id='{0}_subj_append']"},
                                  '_set_radio_groups')),
         ('Add Subject Text', ("//input[@id='{0}_subj_text']",
                               '_set_edits')),
         ('Add Custom Header Name', ("//input[@name='{0}_header_name']",
                                     '_set_edits')),
         ('Add Custom Header Text', ("//input[@name='{0}_header_text']",
                                     '_set_edits')),
         ('Alternate Envelope Recipient', ("//input[@name='{0}_alt_rcpt_to']",
                                           '_set_edits')),
         ('Archive Message', ({'No': "//input[@id='{0}__archive_no']",
                               'Yes': "//input[@id='{0}__archive_yes']"},
                              '_set_radio_groups'))])
    CATEGORIES_PREFIXES_MAPPING = {'social': 'Social Networking Email',
                                   'bulk': 'Bulk Email',
                                   'marketing': 'Marketing Email'}
    ARROW_CLOSED = "(//*[@id='arrow_closed')[1]"

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self) + \
               self._generate_common_settings_pairs(
                   self.CATEGORY_ITEMS_MAPPING,
                   self.CATEGORIES_PREFIXES_MAPPING)

    @set_speed(0, 'gui')
    def set(self, new_value):
        super(GraymailEntrySettings, self).set(new_value)

        self._set_radio_groups(
            new_value,
            self.ENABLE_GRAYMAIL_DETECTION_RADIOGROUP)
        if self.gui._is_text_present('Enable Graymail Unsubscribing'):
            self._set_radio_groups(
                new_value,
                self.ENABLE_GRAYMAIL_UNSUBSCRIPTION_RADIOGROUP,
                self.GRAYMAIL_UNSUBSCRIPTION_PERFORM_ACTION_RADIOGROUP)
        self._set_checkboxes(
            new_value,
            self.ENABLE_MARKETING_SCANNING_CHECKBOX,
            self.ENABLE_SOCIAL_NETWORKING_SCANNING_CHECKBOX,
            self.ENABLE_BULK_SCANNING_CHECKBOX)
        self._fill_categories_settings(
            new_value,
            self.CATEGORY_ITEMS_MAPPING,
            self.CATEGORIES_PREFIXES_MAPPING)
