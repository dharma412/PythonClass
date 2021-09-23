#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/manager/mail_policies_def/content_filters_entry_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import get_object_inputs_pairs

from base_policy_entry_settings import BasePolicyEntrySettings

FILTERS_TABLE = "//table[@class='cols']"
FILTER_ROWS = "%s//tr[count(td)>=2]" % (FILTERS_TABLE,)
FILTER_NAME_BY_IDX = lambda idx: "xpath=%s[%d]/td[2]" % (FILTER_ROWS, idx)
FILTER_CHECKBOX_BY_IDX = lambda idx: "xpath=%s[%d]/td[4]/input" % \
                                     (FILTER_ROWS, idx)


class ContentFiltersEntrySettings(BasePolicyEntrySettings):
    ENABLE_AS_COMBO = ('Content Filters', "//select[@id='enableSf']")
    ENABLE_ALL = ('Enable All', None)

    def _get_registered_inputs(self):
        # Verification is done in runtime for this class
        return []

    def _generate_filter_pairs_list(self):
        pairs = []
        filters_count = int(self.gui.get_matching_xpath_count(FILTER_ROWS))
        for filter_idx in xrange(1, 1 + filters_count):
            filter_name = self.gui.get_text(
                FILTER_NAME_BY_IDX(filter_idx)).strip()
            filter_cb_locator = FILTER_CHECKBOX_BY_IDX(filter_idx)
            pairs.append((filter_name, filter_cb_locator))
        return pairs

    @set_speed(0, 'gui')
    def set(self, new_value):
        super(ContentFiltersEntrySettings, self).set(new_value)

        self._set_combos(new_value,
                         self.ENABLE_AS_COMBO)
        filters_pairs = self._generate_filter_pairs_list()
        self._verify_extra_keys_presense(new_value,
                                         filters_pairs + get_object_inputs_pairs(self))
        values_to_set = new_value.copy()
        if self.ENABLE_ALL[0] in new_value:
            for filter_name, _ in filters_pairs:
                values_to_set[filter_name] = new_value[self.ENABLE_ALL[0]]
        self._set_checkboxes(values_to_set, *filters_pairs)
