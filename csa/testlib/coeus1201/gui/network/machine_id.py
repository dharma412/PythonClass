#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/machine_id.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

REALM_SELECT_ID = 'id=realm'
CONTINUE_RADIOBUTTON = 'id=continue'
DROP_RADIOBUTTON = 'id=drop'

class MachineIdentificationService(GuiCommon):

    """Machine Identification Service settings page interaction class.
    'Network -> Machine ID Service' section.
    """

    def get_keyword_names(self):
        return [
            'machine_identification_service_enable',
            'machine_identification_service_disable',
            'machine_identification_service_edit_settings'
            ]

    def _open_machine_identification_service_page(self):
        """Go to Machine Identification Service configuration page."""

        self._navigate_to('Network', 'Machine ID Service')

    def machine_identification_service_enable(self,
        realm_name=None,
        failure_handling=None):

        """Enables Machine Identification Service

        Parameters:
        - `realm_name`: Name of realm to be selected from the drop-down
        - `failure_handling`: Specify how to handle transactions when machine
                              ID cannot be obtained.
                              Valid Options -Continue Or Drop

        Example:
        | Machine Identification Service Enable  |
        | ... | realm_name=iaf1 |
        | ... | failure_handling=continue |
        """
        self._open_machine_identification_service_page()
        self._enable_or_edit()
        if realm_name is not None:
            self.select_from_list(REALM_SELECT_ID, 'label=%s' % (realm_name))
        if failure_handling is not None:
            if failure_handling.lower() == 'continue':
                self._click_radio_button(CONTINUE_RADIOBUTTON)
            if failure_handling.lower() == 'drop':
                self._click_radio_button(DROP_RADIOBUTTON)
        self._click_submit_button(wait=False)

    def _enable_or_edit(self):
        """Enable and edit Machine Identification Service"""

        enable_machine_id_button =\
                "xpath=//input[@value='Enable and Edit Settings']"
        if self._check_feature_status(feature='machine_id'):
            self._click_edit_settings_button()
        else:
            self.click_button(enable_machine_id_button)

    def machine_identification_service_disable(self):
        """Disables Machine Identification Service

        Example:
        | Machine Identification Service Disable |
        """
        machine_id_service_checkbox = 'id=enabled'
        self._open_machine_identification_service_page()
        if not self._check_feature_status(feature='machine_id'):
            return
        self._click_edit_settings_button()
        self.unselect_checkbox(machine_id_service_checkbox)
        self._click_submit_button(wait=False,accept_confirm_dialog=True)

    def machine_identification_service_edit_settings(self,
        realm_name=None,
        failure_handling=None):
        """Sets Machine Identification Service settings.

        Parameters:
         - `realm_name`: Name of realm to be selected from the drop-down
        - `failure_handling`: Specify how to handle transactions when machine
                              ID cannot be obtained.
                              Valid Options -Continue Or Drop

        Example:

        | Machine Identification Service Edit Settings |
        | ... | realm_name=iaf1 |
        | ... | failure_handling=continue |
        """
        self._open_machine_identification_service_page()
        if not self._check_feature_status(feature='machine_id'):
            raise guiexceptions.GuiFeatureDisabledError\
                    ('Cannot edit Machine Identification Service as disabled')
        self._click_edit_settings_button()
        if realm_name is not None:
            self.select_from_list(REALM_SELECT_ID, 'label=%s' % (realm_name))
        if failure_handling is not None:
            if failure_handling.lower() == 'continue':
                self._click_radio_button(CONTINUE_RADIOBUTTON)
            if failure_handling.lower() == 'drop':
                self._click_radio_button(DROP_RADIOBUTTON)
        self._click_submit_button(wait=False)

