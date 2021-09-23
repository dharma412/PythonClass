##!/usr/bin/env python
# -*- coding: latin-1 -*-
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/administration/system_upgrade.py#2 $
# $DateTime: 2019/09/26 01:36:10 $
# $Author: kathirup $

import re
import time
from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions

SAVE_CONF_CHECKBOX = 'save_config'
DELETE_FILE_BUTTON = "//table[@id='download_ready' and not(" \
                     "contains(@style, 'display: none'))]//input[@value='Delete File']"

CANCEL_DOWNLOAD_BUTTON = "//table[@id='download_progress' and not(" \
                         "contains(@style, 'display: none'))]//input[@value='Cancel Download']"
upgrade_options_button = "//input[@value='Upgrade Options...']"
download_install_options_button = "//input[@id='upgrade_operation_upgrade']"
download_options_button = "//input[@id ='upgrade_operation_download']"
install_options_button = "//input[@id='upgrade_operation_install']"
proceed_download_button = "xpath=//input[@type='submit']"
proceed_button = 'xpath=//input[contains(@value, "Proceed »")]'
cancel_button = 'xpath=//input[@value="Cancel Download"]'
MASK_PASSWORDS_RADIOBUTTON = 'id=mask_passwords'
PLAIN_PASSWORDS_RADIOBUTTON = 'id=plain_passwords'
email_field = 'config_email'
CONTINUE_BUTTON = 'xpath=//input [contains(@value,"Continue")]'
CURRENT_TASK = "//* [text() = 'Current Task']/.."


class SystemUpgrade(GuiCommon):
    """Keywords for interaction with "System Administration > System Upgrade"
    GUI page."""

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['system_upgrade',
                'system_upgrade_download_and_install',
                'system_upgrade_cancel',
                'system_upgrade_download',
                'system_upgrade_download_start',
                'system_upgrade_install']

    def _open_page(self):
        """Open 'System Upgrade' page """

        self._navigate_to('Management Appliance', 'System Administration', 'System Upgrade')

    def _click_upgrade_options_button(self):
        """Click 'Upgrade Options...' button"""

        self.click_button(upgrade_options_button)
        self._info("Clicked 'Upgrade Options...'")

    def _click_download_install_button(self):
        """Click 'Download Install' button"""

        self.click_button(download_install_options_button)
        self._info("Clicked 'download_install_button...'")

    def _click_download_button(self):
        """Click 'Download ' button"""
        self.click_button(download_options_button)
        self._info("Clicked 'download_button...'")

    def _click_install_button(self):
        """Click 'Install ' button"""
        self.click_button(install_options_button)
        self._info("Clicked 'install_button...'")

    def _click_proceed_button_download(self):
        """Click 'Proceed >>' button"""

        self.click_button(proceed_download_button)
        self._info("Clicked 'Proceed >>' button")

    def _click_proceed_button(self):
        """Click 'Proceed >>' button"""

        self.click_button(proceed_button, "don't wait")
        self._info("Clicked 'Proceed >>' button")

    def _click_cancel_button(self):
        """Click cancel burron"""
        time.sleep(180)
        self.click_button(cancel_button)
        self._info("Clicked cancel button")

    def _delete_button(self):
        self._wait_until_element_is_present(DELETE_FILE_BUTTON, 36000)

    def _select_upgrade_file(self, version=None):
        """Select upgrade file from the upgrade list"""

        upgrade_locator = 'upgrade_file'
        format_of_version = \
            re.match("\d{1,2}\.\d{1}\.\d{1}\-\d{1,3}", version)
        if not format_of_version:
            raise ValueError, 'Please specify version in X.X.X-XXX format'
        upgrade_list = self.get_list_items(upgrade_locator)
        id_build = version.split('-')
        upgrade_str = id_build[0] + ' build ' + id_build[1]
        for upgrade in upgrade_list:
            if upgrade_str in upgrade:
                self.select_from_list(upgrade_locator, upgrade)
                self._info('Selected upgrade %s' % upgrade)
                return
        else:
            raise guiexceptions.GuiControlNotFoundError \
                ('"%s" upgrade version' % (version,), 'System Upgrade')

    def _enable_save_config(self, save_config=None):

        if save_config is not None:
            if save_config:
                self.select_checkbox(SAVE_CONF_CHECKBOX)
                self._info('Checked save config checkbox')
            else:
                self.unselect_checkbox(SAVE_CONF_CHECKBOX)
                self._info('Unchecked save config checkbox')

    def _enable_mask_password(self, mask_password=None):

        if mask_password is not None:
            if not self._is_checked(SAVE_CONF_CHECKBOX):
                raise guiexceptions.GuiValueError \
                    ('Cannot enable Mask password checkbox as Save Config ' \
                     'checkbox is Disabled')
            if mask_password:
                self._click_radio_button(MASK_PASSWORDS_RADIOBUTTON)
                self._info('Selected mask password RadioButton')
            else:
                self._click_radio_button(PLAIN_PASSWORDS_RADIOBUTTON)
                self._info('Selected plain password RadioButton')

    def _email_config_file(self, email=None):

        if email is not None:
            if not self._is_checked(SAVE_CONF_CHECKBOX):
                raise guiexceptions.GuiValueError \
                    ('Cannot set email as Save Config checkbox is Disabled')
            self.input_text(email_field, email)
            self._info("Setting email to send config. file to '%s'" % email)

    def system_upgrade(self,
                       version=None,
                       save_config=None,
                       mask_password=None,
                       email=None):
        """System Upgrade

        Parameter:
           - `version`: AsyncOS version-build ID for the Web Security Appliance.
           - `save_config`: True to save the current configuration to
                            the configuration directory before upgrading.
                            False otherwise.
           - `mask_password`: True to mask passwords in the configuration file
                            if `save_config` is True
           - `email`: a string of comma separated email addresses to email
                            configuration file to if `save_config` is True

        Exceptions:
            - `GuiControlNotFoundError`: in case version is not
                                         available on the upgrade page
            - `GuiFeatureDisabledError`: in case Save Config checkbox is
                                         unchecked
            - `ValueError`: in case errors in entered values

        Examples:
        | System Upgrade | 7.5.0-180 |
        | System Upgrade | version=7.5.0-180 | save_config=${True} | mask_password=${False} | email=mymoroz@mail.qa, testuser@mail.qa |
        """
        self._info('Beginning system upgrade process...')
        self._open_page()
        self._click_upgrade_options_button()
        self._select_upgrade_file(version)
        self._enable_save_config(save_config)
        self._enable_mask_password(mask_password)
        self._email_config_file(email)
        self._click_proceed_button()
        self._process_continue()
        self._wait_to_click_button('xpath=//input[@value="Reboot Now"]', 'Reboot', 600)

    def system_upgrade_download_and_install(self,
                                            version=None,
                                            save_config=None,
                                            mask_password=None,
                                            email=None):
        """System Upgrade

        Parameter:
           - `version`: AsyncOS version-build ID for the Web Security Appliance.
           - `save_config`: True to save the current configuration to
                            the configuration directory before upgrading.
                            False otherwise.
           - `mask_password`: True to mask passwords in the configuration file
                            if `save_config` is True
           - `email`: a string of comma separated email addresses to email
                            configuration file to if `save_config` is True

        Exceptions:
            - `GuiControlNotFoundError`: in case version is not
                                         available on the upgrade page
            - `GuiFeatureDisabledError`: in case Save Config checkbox is
                                         unchecked
            - `ValueError`: in case errors in entered values

        Examples:
        | System Upgrade Download And Install | 7.5.0-180 |
        | System Upgrade Download And Install| version=7.5.0-180 | save_config=${True} | mask_password=${False} | email=mymoroz@mail.qa, testuser@mail.qa |
        """
        self._info('Beginning system upgrade process...')
        self._open_page()
        self._click_upgrade_options_button()
        self._click_download_install_button()
        self._select_upgrade_file(version)
        self._enable_save_config(save_config)
        self._enable_mask_password(mask_password)
        self._email_config_file(email)
        self._click_proceed_button()
        self._process_continue()
        self._wait_to_click_button('xpath=//input[@value="Reboot Now"]', 'Reboot', 600)

    def system_upgrade_download(self, version=None):

        """System Upgrade Download

        Parameter:
           - `version`: AsyncOS version-build ID for the Web Security Appliance.
           - `save_config`: True to save the current configuration to
                            the configuration directory before upgrading.
                            False otherwise.
           - `mask_password`: True to mask passwords in the configuration file
                            if `save_config` is True
           - `email`: a string of comma separated email addresses to email
                            configuration file to if `save_config` is True

        Exceptions:
            - `GuiControlNotFoundError`: in case version is not
                                         available on the upgrade page
            - `GuiFeatureDisabledError`: in case Save Config checkbox is
                                         unchecked
            - `ValueError`: in case errors in entered values

        Examples:
        | System Upgrade Download | 7.5.0-180 |
        | System Upgrade Download | version=7.5.0-180 | save_config=${True} | mask_password=${False} | email=mymoroz@mail.qa, testuser@mail.qa |
        """
        self._info('Beginning system upgrade process...')
        self._open_page()
        self._click_upgrade_options_button()
        self._click_download_button()
        self._select_upgrade_file(version)
        self._click_proceed_button()
        self._delete_button()

    def system_upgrade_download_start(self, version=None):

        """System Upgrade Download Start

        Parameter:
           - `version`: AsyncOS version-build ID for the Web Security Appliance.
           - `save_config`: True to save the current configuration to
                            the configuration directory before upgrading.
                            False otherwise.
           - `mask_password`: True to mask passwords in the configuration file
                            if `save_config` is True
           - `email`: a string of comma separated email addresses to email
                            configuration file to if `save_config` is True

        Exceptions:
            - `GuiControlNotFoundError`: in case version is not
                                         available on the upgrade page
            - `GuiFeatureDisabledError`: in case Save Config checkbox is
                                         unchecked
            - `ValueError`: in case errors in entered values

        Examples:
        | System Upgrade Download | 7.5.0-180 |
        | System Upgrade Download | version=7.5.0-180 | save_config=${True} | mask_password=${False} | email=mymoroz@mail.qa, testuser@mail.qa |
        """
        self._info('Beginning system upgrade process...')
        self._open_page()
        self._click_upgrade_options_button()
        self._click_download_button()
        self._select_upgrade_file(version)
        self._click_proceed_button()

    def _process_continue(self):
        time.sleep(180)
        while True:
            try:

                # If there is a task, log the details
                if self._is_visible(CURRENT_TASK):
                    _text = self.get_text(CURRENT_TASK)

                    if _text.find('WARNING') > -1:
                        self._warn(_text)

                    else:
                        self._info(_text)

                    # if the page has a continue button, click continue_button
                    if self._is_visible(CONTINUE_BUTTON):
                        self.click_button(CONTINUE_BUTTON)

                else:
                    # there are no more tasks
                    self._info("No Tasks running")
                    break

                time.sleep(30)

            except Exception as e:
                self._info('Exception occurred')
                print(e)
                break

    def system_upgrade_cancel(self,
                              version=None):
        """System Upgrade Cancel

        Parameter:
           - `version`: AsyncOS version-build ID for the Web Security Appliance.

        Exceptions:
            - `GuiControlNotFoundError`: in case version is not
                                         available on the upgrade page
            - `GuiFeatureDisabledError`: in case Save Config checkbox is
                                         unchecked
            - `ValueError`: in case errors in entered values

        Examples:
        | System Upgrade Cancel | 7.5.0-180 |

        """

        self._click_cancel_button()

    def system_upgrade_install(self,
                               version=None,
                               save_config=None,
                               mask_password=None,
                               email=None):
        """System Upgrade Install

        Parameter:
           - `version`: AsyncOS version-build ID for the Web Security Appliance.
           - `save_config`: True to save the current configuration to
                            the configuration directory before upgrading.
                            False otherwise.
           - `mask_password`: True to mask passwords in the configuration file
                            if `save_config` is True
           - `email`: a string of comma separated email addresses to email
                            configuration file to if `save_config` is True

        Exceptions:
            - `GuiControlNotFoundError`: in case version is not
                                         available on the upgrade page
            - `GuiFeatureDisabledError`: in case Save Config checkbox is
                                         unchecked
            - `ValueError`: in case errors in entered values

        Examples:
        | System Upgrade Cancel | 7.5.0-180 |
        | System Upgrade | version=7.5.0-180 | save_config=${True} | mask_password=${False} | email=mymoroz@mail.qa, testuser@mail.qa |
        """
        self._info('Beginning system upgrade process...')
        self._open_page()
        self._click_upgrade_options_button()
        self._click_install_button()
        self._click_proceed_button()
        self._process_continue()
        self._wait_to_click_button('xpath=//input[@value="Reboot Now"]', 'Reboot', 600)
