#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/admin/users_def/sf_priv_settings.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner

PARENT_TABLE = "//table[@class='layout']/tbody/tr/td/table[@class='layout']/tbody"
PREDEFINED_ROLE_LABEL = \
    "%s//tr[.//td[normalize-space()='Predefined Roles']]" \
    "//label[@class='label']" % (PARENT_TABLE,)
PREDEFINED_ROLE_LABEL_IDX = lambda idx: \
    "%s//tr[.//td[normalize-space()='Predefined Roles']]" \
    "//label[@class='label'][%d]" % (PARENT_TABLE, idx)
PREDEFINED_ROLE_CHECKBOX_IDX = lambda idx: \
    "%s//tr[.//td[normalize-space()='Predefined Roles']]" \
    "//label[@class='label'][%d]/" \
    "preceding-sibling::input[@type='checkbox'][1]" % \
    (PARENT_TABLE, idx)
CUSTOM_ROLE_LABEL = \
    "%s//tr[.//td[normalize-space()='Custom Roles']]" \
    "//label[@class='label']" % (PARENT_TABLE,)
CUSTOM_ROLE_LABEL_IDX = lambda idx: \
    "%s//tr[.//td[normalize-space()='Custom Roles']]" \
    "//label[@class='label'][%d]" % (PARENT_TABLE, idx)
CUSTOM_ROLE_CHECKBOX_IDX = lambda idx: \
    "%s//tr[.//td[normalize-space()='Custom Roles']]" \
    "//label[@class='label'][%d]/" \
    "preceding-sibling::input[@type='checkbox'][1]" % \
    (PARENT_TABLE, idx)


class SecondFactorPrivSettings(InputsOwner):
    @set_speed(0, 'gui')
    def _get_checkbox_mapping(self):
        if hasattr(self, '_cached_mapping'):
            return self._cached_mapping
        else:
            self._cached_mapping = {}

        predefined_cnt = \
            int(self.gui.get_matching_xpath_count(PREDEFINED_ROLE_LABEL))
        predefined_checkboxes = map(lambda cb_idx: \
                                        (self.gui.get_text(PREDEFINED_ROLE_LABEL_IDX(cb_idx)).strip(),
                                         PREDEFINED_ROLE_CHECKBOX_IDX(cb_idx)), xrange(1, 1 + predefined_cnt))
        custom_cnt = \
            int(self.gui.get_matching_xpath_count(CUSTOM_ROLE_LABEL))
        custom_checkboxes = map(lambda cb_idx: \
                                    (self.gui.get_text(CUSTOM_ROLE_LABEL_IDX(cb_idx)).strip(),
                                     CUSTOM_ROLE_CHECKBOX_IDX(cb_idx)), xrange(1, 1 + custom_cnt))
        self._cached_mapping = dict(predefined_checkboxes + custom_checkboxes)
        return self._cached_mapping

    def _get_registered_inputs(self):
        return self._get_checkbox_mapping().items()

    @set_speed(0, 'gui')
    def set(self, settings):
        self._set_checkboxes(settings,
                             *self._get_checkbox_mapping().items())
