from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs

class CloudServiceSettings(InputsOwner):
    THREAT_RESPONSE = ("Threat Response", "//input[@id='threat_resp_status']")
    THREAT_RESPONSE_SERVER_COMBO = ('Threat Response Server',
                             "//select[@id='threat_resp_server']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def set(self, new_value):

        self._set_checkboxes(new_value,
                self.THREAT_RESPONSE,)
        self._set_combos(new_value,
                         self.THREAT_RESPONSE_SERVER_COMBO,)

    def get(self):
        raise NotImplementedError()


class CiscoSuccessNetwork(InputsOwner):
    CSN_SETTINGS = ("Cisco Success Network Settings", "//input[@id='csn_status']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def set(self, new_value):
        self._set_checkboxes(new_value,
                self.CSN_SETTINGS,)

    def get(self):
        raise NotImplementedError()
