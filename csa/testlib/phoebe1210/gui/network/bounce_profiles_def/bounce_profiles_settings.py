#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/network/bounce_profiles_def/bounce_profiles_settings.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

INITIAL_RETRY = ('Initial Period to Wait Before Retrying an Unreachable Host',
                 "//input[@name='initial_retry']")
MAX_RETRY_TIMEOUT = ('Maximum Interval Allowed Between Retries to an Unreachable Host',
                     "//input[@name='max_retry_timeout']")


class BounceProfilesSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_edits(new_value,
                        INITIAL_RETRY,
                        MAX_RETRY_TIMEOUT)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()
