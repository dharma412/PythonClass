#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/cres_def/provisioning_form.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

ACCOUNT_NAME = ('Account Name',
                "//input[@name='an']")
ADMIN_USERNAME = ('Administrator Username',
                  "//input[@name='aau']")
ACTIVATION_KEY = ('Activation Key',
                  "//textarea[@name='aak']")


class ProvisioningForm(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_edits(new_value,
                        ACCOUNT_NAME,
                        ADMIN_USERNAME,
                        ACTIVATION_KEY)

    def get(self):
        raise NotImplementedError()
