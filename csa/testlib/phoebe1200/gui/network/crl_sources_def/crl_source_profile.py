#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/network/crl_sources_def/crl_source_profile.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import time

from common.gui.decorators import set_speed
from common.gui.guiexceptions import TimeoutError
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs
from common.util.sarftime import CountDownTimer

CRL_FILE_NAME = ('CRL File Name',
                 "//input[@name='name']")
CRL_FILE_TYPE_RADIOGROUP = ('CRL File Type',
                            {'ASN.1': "//input[@name='file_type' and @value='asn1']",
                             'PEM': "//input[@name='file_type' and @value='pem']"})
PRIMARY_URL = ('Primary source URL',
               "//input[@name='primary_url']")
SECONDARY_URL = ('Secondary source URL',
                 "//input[@name='secondary_url']")
AUTO_UPDATE_CHECKBOX = ('Enable Scheduled auto update of CRL file',
                        "//input[@id='auto_update']")
AUTO_UPDATE_PERIOD_RADIOGROUP = ('Auto Update Period',
                                 {'Daily': "//input[@id='scheduled_daily']",
                                  'Weekly': "//input[@id='scheduled_weekly']",
                                  'Monthly': "//input[@id='scheduled_monthly']"})
WEEKDAY_COMBO = ('Update on',
                 "//select[@id='scheduled_weekly_dow']")
SCHEDULED_TIME = ('Scheduled Time',
                  "//input[@id='scheduled_time']")
ENABLE_SOURCE_CHECKBOX = ('Enable this CRL Source',
                          "//input[@id='enabled']")

TEST_SOURCE_BTN = "//input[@value='Test CRL Source']"
TEST_SOURCE_RESULTS = "//textarea[@id='test_results']"


class CRLSourceProfile(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                             AUTO_UPDATE_CHECKBOX,
                             ENABLE_SOURCE_CHECKBOX)
        self._set_radio_groups(new_value,
                               CRL_FILE_TYPE_RADIOGROUP,
                               AUTO_UPDATE_PERIOD_RADIOGROUP)
        self._set_edits(new_value,
                        CRL_FILE_NAME,
                        PRIMARY_URL,
                        SECONDARY_URL,
                        SCHEDULED_TIME)
        self._set_combos(new_value,
                         WEEKDAY_COMBO)

    @set_speed(0, 'gui')
    def test(self):
        self.gui.click_button(TEST_SOURCE_BTN, 'don\'t wait')
        tmr = CountDownTimer(60).start()
        while tmr.is_active():
            time.sleep(1)
            current_results = self.gui.get_value(TEST_SOURCE_RESULTS).strip()
            if len(current_results) > 0:
                return current_results
        raise TimeoutError('Failed to get CRL Source test result within 60 seconds')
