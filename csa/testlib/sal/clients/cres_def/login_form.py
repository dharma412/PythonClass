#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/cres_def/login_form.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

NAME = ('Name',
        "//input[@name='id']")
PASSWORD = ('Password',
            "//input[@name='password']")


class LoginForm(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_edits(new_value,
                        NAME,
                        PASSWORD)

    def get(self):
        raise NotImplementedError()
