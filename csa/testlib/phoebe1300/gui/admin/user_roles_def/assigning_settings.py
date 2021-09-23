#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/user_roles_def/assigning_settings.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

import inspect
import re
import sys

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner

PARENT_TABLE = "//table[@class='cols']"
ALL_ITEMS = "%s/tbody/tr[.//input]" % (PARENT_TABLE,)
# idx starts from 1 (header row is skipped automatically)
ITEM_NAME_BY_IDX = lambda row_idx, col_idx: "%s[%d]/td[%d]" % (ALL_ITEMS, row_idx,
                                                               col_idx)
ITEM_CB_BY_IDX = lambda row_idx: "%s[%d]/td[1]/input[@type='checkbox']" % \
                                 (ALL_ITEMS, row_idx)

ROLE_ROW_BY_NAME = lambda name: "%s/tbody/tr[.//a[normalize-space()='%s']]" % \
                                (PARENT_TABLE, name)


class AssigningSettings(InputsOwner):
    def _get_registered_inputs(self):
        return self._get_available_items()

    @set_speed(0, 'gui')
    def _get_available_items(self):
        if hasattr(self, '_cached_items'):
            return self._cached_items.items()
        else:
            self._cached_items = {}
        items_count = int(self.gui.get_matching_xpath_count(ALL_ITEMS))
        for item_num in xrange(1, 1 + items_count):
            item_name = self.gui.get_text(
                ITEM_NAME_BY_IDX(item_num,
                                 self._get_name_column_index())).strip()
            cb_locator = ITEM_CB_BY_IDX(item_num)
            self._cached_items[item_name] = cb_locator
        return self._cached_items.items()

    def _get_name_column_index(self):
        raise NotImplementedError()

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                             *self._get_available_items())

    @classmethod
    def get_main_entry_locator(cls, role_name):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()


def get_class_by_component_name(component_name):
    """Return component setter class by its name

    *Parameters:*
    - `component_name`: component name. Should equal to one of class
    names having spaces between lowercase and uppercase letters

    *Exceptions:*
    - `ValueError`: if no class is found for component with given name

    *Return:*
    Component class. This class is subclass of AssignmentSettings
    """
    base_class = AssigningSettings
    all_subclasses = [v for k, v in inspect.getmembers(sys.modules[__name__]) \
                      if inspect.isclass(v) and issubclass(v, base_class) and \
                      v != base_class]
    searched_class = filter(lambda x: re.sub(r'([a-z])([A-Z])',
                                             r'\1 \2', x.__name__).lower() == component_name.lower(),
                            all_subclasses)
    if searched_class:
        return searched_class[0]
    else:
        raise ValueError('Invalid component name: "%s".\nAvailable names are: %s' % \
                         (component_name,
                          map(lambda x: re.sub(r'([a-z])([A-Z])', r'\1 \2', x.__name__),
                              all_subclasses)))


class IncomingContentFilters(AssigningSettings):
    def _get_name_column_index(self):
        return 3

    @classmethod
    def get_main_entry_locator(cls, role_name):
        return ROLE_ROW_BY_NAME(role_name) + \
               "/td[2]/a[contains(text(), 'Content Filters:')][1]"


class OutgoingContentFilters(AssigningSettings):
    def _get_name_column_index(self):
        return 3

    @classmethod
    def get_main_entry_locator(cls, role_name):
        return ROLE_ROW_BY_NAME(role_name) + \
               "/td[2]/a[contains(text(), 'Content Filters:')][2]"


class IncomingMailPolicies(AssigningSettings):
    def _get_name_column_index(self):
        return 3

    @classmethod
    def get_main_entry_locator(cls, role_name):
        return ROLE_ROW_BY_NAME(role_name) + \
               "/td[2]/a[contains(text(), 'Policies:')][1]"


class OutgoingMailPolicies(AssigningSettings):
    def _get_name_column_index(self):
        return 3

    @classmethod
    def get_main_entry_locator(cls, role_name):
        return ROLE_ROW_BY_NAME(role_name) + \
               "/td[2]/a[contains(text(), 'Policies:')][2]"


class DlpPolicies(AssigningSettings):
    def _get_name_column_index(self):
        return 3

    @classmethod
    def get_main_entry_locator(cls, role_name):
        return ROLE_ROW_BY_NAME(role_name) + \
               "/td[3]/a[contains(text(), 'DLP Policies:')]"


class Quarantines(AssigningSettings):
    def _get_name_column_index(self):
        return 2

    @classmethod
    def get_main_entry_locator(cls, role_name):
        return ROLE_ROW_BY_NAME(role_name) + \
               "/td[7]/a[contains(text(), 'Quarantines:')]"


class EncryptionProfiles(AssigningSettings):
    def _get_name_column_index(self):
        return 2

    @classmethod
    def get_main_entry_locator(cls, role_name):
        return ROLE_ROW_BY_NAME(role_name) + \
               "/td[8]/a[contains(text(), 'Profiles:')]"
