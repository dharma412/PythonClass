#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/manager/mail_policies_def/dlp_entry_settings.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import get_object_inputs_pairs

from base_policy_entry_settings import BasePolicyEntrySettings

DLP_POLICIES_TABLE = "//table[@class='cols']"
DLP_POLICIES_ROWS = "%s//tr[count(td)>=2]" % (DLP_POLICIES_TABLE,)
DLP_POLICY_NAME_BY_IDX = lambda idx: "xpath=(%s)[%d]/td[1]" % \
                                     (DLP_POLICIES_ROWS, idx)
DLP_POLICY_CHECKBOX_BY_IDX = lambda idx: "xpath=(%s)[%d]/td[2]/input" % \
                                         (DLP_POLICIES_ROWS, idx)


class DLPEntrySettings(BasePolicyEntrySettings):
    ENABLE_AS_COMBO = ('DLP Policies', "//select[@id='enable_dlp']")
    ENABLE_ALL = ('Enable All', None)

    def _get_registered_inputs(self):
        # Verification is done in runtime for this class
        return []

    def _generate_dlp_policies_pairs_list(self):
        pairs = []
        policies_count = int(self.gui.get_matching_xpath_count(DLP_POLICIES_ROWS))
        for idx in xrange(1, 1 + policies_count):
            policy_name = self.gui.get_text(DLP_POLICY_NAME_BY_IDX(idx)).strip()
            cb_locator = DLP_POLICY_CHECKBOX_BY_IDX(idx)
            pairs.append((policy_name, cb_locator))
        return pairs

    @set_speed(1, 'gui')
    def set(self, new_value):
        super(DLPEntrySettings, self).set(new_value)

        self._set_combos(new_value,
                         self.ENABLE_AS_COMBO)
        policies_pairs = self._generate_dlp_policies_pairs_list()
        self._verify_extra_keys_presense(new_value,
                                         policies_pairs + get_object_inputs_pairs(self))
        values_to_set = new_value.copy()
        if self.ENABLE_ALL[0] in new_value:
            for policy_name, _ in policies_pairs:
                values_to_set[policy_name] = new_value[self.ENABLE_ALL[0]]
        self._set_checkboxes(values_to_set, *policies_pairs)
