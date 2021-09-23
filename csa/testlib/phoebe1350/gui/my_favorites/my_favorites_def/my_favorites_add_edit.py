#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/my_favorites/my_favorites_def/my_favorites_add_edit.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs


PATH_KEY = 'Path'
NEW_NAME_KEY = 'New Name'
DESCRIPTION_KEY = 'Description'

MY_FAVORITES_FORM = "//form[contains(dl/dt, 'Edit My Favorite') or "\
    "@name='my_tasks_form']"
PATH = (PATH_KEY, MY_FAVORITES_FORM + "//select[@name='screen']")
NEW_NAME = (NEW_NAME_KEY, MY_FAVORITES_FORM + "//input[@id='task_name']")
DESCRIPTION = (DESCRIPTION_KEY,
    MY_FAVORITES_FORM + "//textarea[@name='description']")


class MyFavoritesAddEdit(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        settings = self._get_values(NEW_NAME)
        settings.update(new_value)
        if PATH_KEY in new_value:
            new_value[PATH_KEY] = new_value[PATH_KEY][1]
            self._set_combos(new_value, PATH)
        self._set_edits(new_value, NEW_NAME, DESCRIPTION)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()

