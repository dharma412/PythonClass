#!/usr/bin/env python
# $Id $

from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions

class SensorBase(GuiCommon):
    """SensorBase Settings page interaction class.

    Use keywords provided by this class to interact with GUI elements of
    Security Services -> SensorBase page.
    """

    def get_keyword_names(self):
        return ['sensor_base_enable',
                'sensor_base_disable',
                'sensor_base_edit_settings',
                ]

    def _open_page(self):
        """Open 'SensorBase' page """

        self._navigate_to('Security Services', 'SensorBase')

    def _enable_sensorbase(self):
        """Enable SensorBase."""

        enable_sensorbase_button = "xpath=//input[@title='Enable...']"
        accept_license_button = "xpath=//input[@title='Accept'"
        self.click_button(enable_sensorbase_button)
        if self._is_text_present\
                         ('SensorBase License Agreement'):
            self.click_button(accept_license_button)

    def _click_edit_global_settings_button(self):
        """Click 'Edit Global Settings...' button"""

        edit_settings_button = \
                    "xpath=//input[@title='Edit Global Settings...']"
        self.click_button(edit_settings_button)

    def _set_excluded_domains_and_ip(self, excluded=None):

        excluded_field = "xpath=//textarea[@id='excluded_domains']"
        if excluded is not None:
            excluded = self._convert_to_tuple(excluded)
            excluded_text = ','.join(excluded)
            self.input_text(excluded_field, excluded_text)

    def _select_participation_level(self, level=None):

        level_radio_button = {'limited': 'level_Basic',
                              'standard': 'level_Enhanced'}
        if level is not None:
            if level.lower() == 'limited':
                self._click_radio_button(level_radio_button['limited'])
            else:
                self._click_radio_button(level_radio_button['standard'])

    def sensor_base_disable(self):
        """Disable SensorBase Settings.

        Use this method to disable Sensor Base global settings.

        Example:
        | Sensor Base Disable |
        """

        enable_sensorbase_checkbox = "xpath=//input[@id='sbrs_toggle']"
        self._open_page()
        if not self._check_feature_status(feature='sensorbase'):
            return
        self._click_edit_global_settings_button()
        self.unselect_checkbox(enable_sensorbase_checkbox)
        self._click_submit_button()

    def sensor_base_enable(self):
        """Enable SensorBase Settings.

        Use this method to enable Sensor Base global settings.

        Example:
        | Sensor Base Enable |
        """

        self._open_page()
        self._enable_sensorbase()

    def sensor_base_edit_settings(self,
                                 level=None,
                                 excluded=None):
        """Edit SensorBase Settings.

        Use this keyword to edit Sensor Base settings.

        :Parameters:
        - `level`: Participation Level. String. One of the values:
            * 'limited' - Summary URL information shared.
            * 'standard' - Full URL information shared. (Recommended)
        - `excluded`: comma separated values of Excluded Domains and IP
        Addresses to exclude from SensorBase traffic returned to IronPort.

        Example:
        | Sensor Base Edit Settings | standard | company.com, 192.168.1.1 |
        """

        self._open_page()
        # check if SensorBase disabled
        if not self._check_feature_status(feature='sensorbase'):
            raise guiexceptions.GuiFeatureDisabledError\
               ('SensorBase currently is disabled')
        self._click_edit_global_settings_button()
        self._select_participation_level(level)
        self._set_excluded_domains_and_ip(excluded)
        self._click_submit_button()
