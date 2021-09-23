#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/services/scan_behaviour_def/global_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

SKIP_IF_IN_LIST_RADIOGROUP = ('Action for attachments',
                              {'Scan': "//input[@id='skip_if_in_list_scan']",
                               'Skip': "//input[@id='skip_if_in_list_skip']"})
MAX_DEPTH = ('Maximum depth of attachment recursion',
             "//input[@name='depth_limit']")
MAX_SIZE = ('Maximum attachment size',
            "//input[@name='size_limit']")
SCAN_METADATA_RADIOGROUP = ('Attachment Metadata scan',
                            {'Enabled': "//input[@id='scan_metadata_enabled']",
                             'Disabled': "//input[@id='scan_metadata_disabled']"})
SCAN_TIMEOUT = ('Attachment scanning timeout',
                "//input[@name='scan_timeout']")
ASSUME_PATTERN_RADIOGROUP = ('Assume attachment matches pattern',
                             {'Yes': "//input[@id='assume_dirty_yes']",
                              'No': "//input[@id='assume_dirty_no']"})
ACTION_DESCONSTR_RADIOGROUP = ('Action when message cannot be deconstructed',
                               {'Deliver': "//input[@id='mimeparse_fail_action_deliver']",
                                'Bounce': "//input[@id='mimeparse_fail_action_bounce']",
                                'Drop': "//input[@id='mimeparse_fail_action_drop']"})
ENCODING_COMBO = ('Encoding to use',
                  "//select[@name='default_text_encoding']")
CONVERT_OPAQUE_RADIOGROUP = ('Convert opaque-signed messages',
                             {'Enabled': "//input[@id='smime_unpack_enabled']",
                              'Disabled': "//input[@id='smime_unpack_disabled']"})


class GlobalSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_radio_groups(new_value,
                               SKIP_IF_IN_LIST_RADIOGROUP,
                               SCAN_METADATA_RADIOGROUP,
                               ASSUME_PATTERN_RADIOGROUP,
                               ACTION_DESCONSTR_RADIOGROUP,
                               CONVERT_OPAQUE_RADIOGROUP)
        self._set_edits(new_value,
                        MAX_DEPTH,
                        MAX_SIZE,
                        SCAN_TIMEOUT)
        self._set_combos(new_value,
                         ENCODING_COMBO)
