#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/destination_controls_def/destination_controls_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

CERTIFICATE_COMBO = ('Certificate',
                     "//select[@name='certificate']")
SEND_TLS_REQ_ALERT_CHECKBOX = ('Send an alert when a required TLS connection fails',
                               "//input[@id='send_tls_req_alert']")


class DestinationControlsSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_combos(new_value,
                         CERTIFICATE_COMBO)
        self._set_checkboxes(new_value,
                             SEND_TLS_REQ_ALERT_CHECKBOX)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()
