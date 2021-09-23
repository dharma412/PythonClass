#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/mail_policies_def/base_policy_entry_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.inputs_owner import InputsOwner

ADVANCED_LINK = "//a/img[@alt='open']"
ADVANCED_LINK_BY_IDX = lambda idx: "xpath=(%s)[%d]" % (ADVANCED_LINK, idx)
SUBMIT_BUTTON = "//input[@value='Submit' and @type!='hidden']"


class BasePolicyEntrySettings(InputsOwner):
    def _generate_common_settings_pairs(self,
                                        category_items_mapping,
                                        categories_prefixes_mapping):
        pairs = []
        for category_locator_prefix, category_name_prefix in \
                categories_prefixes_mapping.iteritems():
            for item_name_suffix, item_properties_tuple in \
                    category_items_mapping.iteritems():
                item_locator_pattern, setter_name = item_properties_tuple
                name = '%s %s' % (category_name_prefix, item_name_suffix)
                if isinstance(item_locator_pattern, dict):
                    # radiogroup detected
                    locator = {}
                    for key, value in item_locator_pattern.iteritems():
                        locator[key] = value.format(category_locator_prefix)
                else:
                    locator = item_locator_pattern.format(category_locator_prefix)
                pairs.append((name, locator))
        return pairs

    def _open_advanced_entries(self):
        links_count = int(self.gui.get_matching_xpath_count(ADVANCED_LINK))
        for link_idx in xrange(1, 1 + links_count):
            self.gui.click_element(ADVANCED_LINK_BY_IDX(link_idx),
                                   'don\'t wait')

    def _fill_categories_settings(self, new_value,
                                  category_items_mapping,
                                  categories_prefixes_mapping):
        for category_locator_prefix, category_name_prefix in \
                categories_prefixes_mapping.iteritems():
            for item_name_suffix, item_properties_tuple in \
                    category_items_mapping.iteritems():
                item_locator_pattern, setter_name = item_properties_tuple
                name = '%s %s' % (category_name_prefix, item_name_suffix)
                if isinstance(item_locator_pattern, dict):
                    # radiogroup detected
                    locator = {}
                    for key, value in item_locator_pattern.iteritems():
                        locator[key] = value.format(category_locator_prefix)
                else:
                    locator = item_locator_pattern.format(category_locator_prefix)
                dest_control = (name, locator)
                setter = getattr(self, setter_name)
                setter(new_value, dest_control)

    def _verify_extra_keys_presense(self, new_value, pairs_list):
        available_keys = dict(pairs_list).keys()
        if not set(new_value.keys()).issubset(set(available_keys)):
            raise ValueError('Unknown parameter name(s) "%s". ' \
                             'Available parameters are: %s' % \
                             (list(set(available_keys) - set(new_value.keys())),
                              available_keys))

    def set(self, new_value):
        self._open_advanced_entries()

    def submit_changes(self):
        self.gui.click_button(SUBMIT_BUTTON)
        self.gui._check_action_result()
