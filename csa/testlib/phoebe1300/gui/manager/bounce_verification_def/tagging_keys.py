#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/manager/bounce_verification_def/tagging_keys.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs


class TaggingKeyAddForm(InputsOwner):
    NEW_KEY = ('Address Tagging Key',
               "//input[@id='key_input']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_edits(new_value,
                        self.NEW_KEY)

    def get(self):
        raise NotImplementedError()


class TaggingKeyPurgeForm(InputsOwner):
    PURGE_COMBO = ('Option',
                   "//select[@id='keys_to_purge_id']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_combos(new_value,
                         self.PURGE_COMBO)

    def get(self):
        raise NotImplementedError()
