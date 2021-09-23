#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/configuration_file.py#2 $
# $DateTime: 2019/11/21 22:03:55 $
# $Author: uvelayut $

import re
import time
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

EMAIL_CONFIG_RADIOBUTTON = 'id=email_operation_id'
EMAIL_ADDRS_TEXTBOX = 'id=mailto_id'
SAVE_CONFIG_RADIOBUTTON = 'id=save_operation_id'
SYSTEM_FILENAME_RADIOBUTTON = 'id=system_filename_id'
USER_FILENAME_RADIOBUTTON = 'id=user_filename_id'
USER_FILENAME_TEXTBOX = 'id=filename_name_id'
MASK_PASSWORDS_RADIOBUTTON = 'id=mask_passwords'
ENCRYPT_PASSWORDS_RADIOBUTTON = 'id=encrypt_passwords'
LOAD_CONFIG_RADIOBUTTON = 'id=load_from_appliance_id'
UPLOAD_CONFIG_RADIOBUTTON = 'id=load_from_local_id'
PASTE_CONFIG_RADIOBUTTON = 'id=load_from_buffer_id'
FILE_PATH_TEXTBOX = 'id=local_file_id'
CONFIG_FILENAME_LIST = 'id=appliance_filename_id'
CONFIG_TEXTBOX = 'id=config_buffer_id'
LOAD_BUTTON = 'xpath=//input[@value="Load"]'
RESET_BUTTON = 'name=action:Reset'

class ConfigurationFile(GuiCommon):
    """Keywords for interaction with "System Administration > Configuration
    File" GUI page.
    """
    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return [
                'configuration_file_save',
                'configuration_file_email',
                'configuration_file_load',
                'configuration_file_upload',
                'configuration_file_paste',
                'configuration_file_reset',
                ]

    def _open_page(self):
        self._navigate_to('System Administration', 'Configuration File')
        time.sleep(5)

    def _click_email_config_file(self):
        self.click_button(EMAIL_CONFIG_RADIOBUTTON, "don't wait")
        self._info('Clicked "Email file to" radio button.')

    def _click_save_to_appliance(self):
        self._click_radio_button(SAVE_CONFIG_RADIOBUTTON)
        self._info('Clicked "Save to appliance" radiobutton.')

    def _get_filename(self):
        cfg_file_patt = re.compile('as \'(.*?)\'')
        text = self.get_text('//*[@id=\'action-results-message\']')
        result = cfg_file_patt.search(text)
        if result:
            return result.group(1)
        else:
            raise guiexceptions.GuiValueError('Cannot parse configuration file name')

    def _fill_email_addrs(self, email_addrs):
        emails = ','.join(self._convert_to_tuple(email_addrs))
        self.input_text(EMAIL_ADDRS_TEXTBOX, emails)
        self._info('Set email address(es) to "%s".' % (emails,))

    def _set_filename(self, filename):
        if filename is None:
            self._click_radio_button(SYSTEM_FILENAME_RADIOBUTTON)
            self._info('Selected to use system-generated filename.')
        else:
            self._click_radio_button(USER_FILENAME_RADIOBUTTON)
            self.input_text(USER_FILENAME_TEXTBOX, filename)
            self._info('Selected to use user-defined filename. Set '\
                             'name to "%s".' % (filename,))

    def _enable_passwords_masking(self, enable):
        if enable:
            self._click_radio_button(MASK_PASSWORDS_RADIOBUTTON)
            self._info('Enabled passwords masking.')
        else:
            self._click_radio_button(ENCRYPT_PASSWORDS_RADIOBUTTON)
            self._info('Enabled encrypt passwords ')

    def _click_load_from_appliance(self):
        self.click_button(LOAD_CONFIG_RADIOBUTTON, "don't wait")
        self._info('Clicked "Load from appliance" radio button.')

    def _click_load_from_local(self):
        self.click_button(UPLOAD_CONFIG_RADIOBUTTON, "don't wait")
        self._info('Clicked "Load from local computer" radio button.')

    def _click_paste_config(self):
        self.click_button(PASTE_CONFIG_RADIOBUTTON, "don't wait")
        self._info('Clicked "Paste your configuration" radio button.')

    def _fill_local_file_path(self, filepath):
        self.choose_file(FILE_PATH_TEXTBOX, filepath)
        self._info('Set local file path to "%s".' % (filepath,))

    def _select_config_file(self, filename):
        config_files = self.get_list_items(CONFIG_FILENAME_LIST)
        if filename not in config_files:
            raise ValueError('"%s" config filename is not present.' \
                    % (filename,))
        self.select_from_list(CONFIG_FILENAME_LIST, filename)
        self._info('Selected "%s" config file.' % (filename,))

    def _fill_configuration_textbox(self, configuration):
        self.input_text(CONFIG_TEXTBOX, configuration)
        self._info('Pasted configuration into textbox.')

    def _click_load_button(self):
        self.click_button(LOAD_BUTTON, "don't wait")
        self._info('Clicked "Load" button.')

    def _click_reset_button(self):
        self.click_button(RESET_BUTTON, "don't wait")
        self._info('Clicked "Reset" button.')

    def configuration_file_save(self, mask_passwd=False, filename=None):
        """Save current configuration to the appliance.

        Parameters:
            - `mask_passwd`: mask passwords in the configuration file. Default
                             to False.
            - `filename`: name to use for configuration file. If None,
                          system-generated name will be used.

        Return:
            String containing name of the configuration file saved on the
            appliance.

        Examples:
        | Configuration File Save | mask_passwd=${True} | filename=preupgrade.xml |
        | ${config_file} = | Configuration File Save | |
        """
        self._info('Saving configuration file to appliance.')
        self._open_page()
        self._click_save_to_appliance()
        self._enable_passwords_masking(mask_passwd)
        self._set_filename(filename)
        self._click_submit_button()

        return self._get_filename()

    def configuration_file_email(self, email_addrs, mask_passwd=False,
            filename=None):
        """Email current configuration of the appliance.

        Parameters:
            - `email_addrs`: a string of comma separated email addresses to send
                configuration to.
            - `mask_passwd`: mask passwords in the configuration file. Default
                to False.
            - `filename`: name to use for configuration file. If None,
                          system-generated name will be used.

        Examples:
        | Configuration File Email | mymoroz@mail.qa, testuser@mail.qa |
        | Configuration File Email | mymoroz@mail.qa | mask_passwd=${True} | filename=customconfig.xml |
        """
        self._info('Emailing configuration file.')
        self._open_page()
        self._click_email_config_file()
        self._fill_email_addrs(email_addrs)
        self._enable_passwords_masking(mask_passwd)
        self._set_filename(filename)
        self._click_submit_button()

    def _load_network_settings(self, load_network_settings):
        """
        If load_network_settings='yes', check the corresponding box,
        elif if load_network_settings='no', uncheck the corresponding box
        else log a warning of unexpected value
        """
        CHECKBOX = 'xpath=//input[@id="load_nw_settings"]'
        if load_network_settings == 'yes':
            self.select_checkbox(CHECKBOX)
            self._info('Enabled Loading Network Settings')
        elif load_network_settings == 'no':
            self.unselect_checkbox(CHECKBOX)
            self._info('Disabled Loading Network Settings')
        else:
            self._warn('Invalid setting of load_network_settings=%s' +
                ' accepted yalues yes and no' % load_network_settings)

    def configuration_file_load(self, filename,
        load_network_settings='yes'):
        """Load configuration from the appliance.

        Parameters:
            - `filename`: name of the file to load.
            - `load_network_settings`: - whether to load network settings;
             accepted values are: None, 'yes', and 'no'

        Examples:
        | Configuration File Load | preupgrade.xml |
        | Configuration File Load | preupgrade.xml | load_network_settings=no |
        """
        self._info('Loading "%s" configuration file.' % (filename,))
        self._open_page()
        self._click_load_from_appliance()
        if load_network_settings:
            self._load_network_settings(load_network_settings)
        self._select_config_file(filename)
        self._click_load_button()
        self._click_continue_button()

    def configuration_file_upload(self, filepath):
        """Upload configuration file from local machine to appliance.

        Parameters:
            - `filepath`: path to the configuration file on local machine.

        Examples:
        | Configuration File Upload | /home/user/preupgrade.xml |
        """
        self._info('Uploading configuration file to the appliance.')
        self._open_page()
        self._click_load_from_local()
        self._fill_local_file_path(filepath)
        self._click_load_button()
        self._click_continue_button()

    def configuration_file_paste(self, configuration):
        """Paste configuration into appliance.

        Parameters:
            - `configuration`: string containing XML configuration to paste
                               into appliance.

        | Configuration File Paste | <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE config SYSTEM "config.dtd"><config><update_interval>600</update_interval></config> |
        """
        self._info('Pasting configuration into appliance.')
        self._open_page()
        self._click_paste_config()
        self._fill_configuration_textbox(configuration)
        self._click_load_button()
        self._click_continue_button()

    def _reset_network(self, reset_network):
        """
        If reset_network='yes', check the corresponding box,
        elif if reset_network='no', uncheck the corresponding box
        else log a warning of unexpected value
        """
        CHECKBOX = 'xpath=//input[@id="reset_network"]'
        if reset_network == 'yes':
            self.select_checkbox(CHECKBOX)
            self._info('Reset Network Settings')
        elif reset_network == 'no':
            self.unselect_checkbox(CHECKBOX)
            self._info('Did not reset Network Settings')
        else:
            self._warn('Invalid setting of reset_network=%s' +
                ' accepted yalues yes and no' % reset_network)

    def configuration_file_reset(self,
        reset_network=None):

        """Reset current configuration to factory default settings.

        Parameters:
            - `reset_network`: - whether to reset network settings;
             accepted values are: None, 'yes', and 'no'

        Examples:
        | Configuration File Reset |
        | Configuration File Reset | reset_network=no |
        """
        self._info('Resetting current configuration.')
        self._open_page()
        if reset_network:
            self._reset_network(reset_network)
        self._click_reset_button()
        self._click_continue_button()
        self._info('Configuration has been reset.')
