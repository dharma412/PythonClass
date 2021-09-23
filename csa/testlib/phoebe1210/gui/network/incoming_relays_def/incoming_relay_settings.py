#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/network/incoming_relays_def/incoming_relay_settings.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

NAME = ('Name',
        "//input[@name='newName']")
IP_ADDRESS = ('IP Address',
              "//input[@name='net']")
HEADER_RADIO_GROUP = ('Header',
                      {'Custom header': "//input[@id='specify']",
                       'Parse the "Received" header': "//input[@id='parse']"})
CUSTOM_HEADER = ('Custom Header',
                 "//input[@id='_header']")
MATCH_AFTER = ('Begin parsing after',
               "//input[@id='match_after']")
HOP_COMBO = ('Hop', "//select[@id='recv_idx']")


class IncomingRelaySettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_edits(new_value,
                        NAME,
                        IP_ADDRESS)
        self._set_radio_groups(new_value,
                               HEADER_RADIO_GROUP)
        self._set_edits(new_value,
                        CUSTOM_HEADER,
                        MATCH_AFTER)
        self._set_combos(new_value, HOP_COMBO)

    def get(self):
        raise NotImplementedError()
