#!/usr/bin/env python -tt
# $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

NAME = ('Name',
        "//input[@name='name']")
DESCRIPTION = ('Description',
               "//textarea[@name='desc']")
HASHES = ('File Hash',
          "//textarea[@name='filehashes']")
FILE_HASH_SELECT_GROUP = ('File Hash Type',
                          {'MD5': "//*[@id='enable_md5']",
                           'SHA256': "//*[@id='enable_sha256']",
                           'Both of the above': "//*[@id='enable_both_md5_sha256']"})


class FileHashListSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_radio_groups(new_value,
                               FILE_HASH_SELECT_GROUP)

        self._set_edits(new_value,
                        NAME,
                        DESCRIPTION,
                        HASHES)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()
