#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/administration/system_upgrade_def/wizard_pages.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author

import re
import time

from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs
from common.gui.guiexceptions import TimeoutError
from common.util.sarftime import CountDownTimer
from common.util.systools import SysTools
from common.gui.guicommon import GuiCommon

OPERATIONS_KEY = 'Upgrade Operation'
UPGRADE_FILE_KEY = 'Upgrade File'

INSTALL_OPERATION = 'Install'
DOWNLOAD_AND_INSTALL_OPERATION = 'Download and install'
DOWNLOAD_ONLY_OPERATION = 'Download only'

DELETE_FILE_BUTTON = "//table[@id='download_ready' and not(" \
                     "contains(@style, 'display: none'))]//input[@value='Delete File']"
CANCEL_DOWNLOAD_BUTTON = "//table[@id='download_progress' and not(" \
                         "contains(@style, 'display: none'))]//input[@value='Cancel Download']"


def get_asyncos_upgrades_map(all_names):
    """Extracts AsyncOS-only upgrade names from upgrades list

    *Return:*
    Dictionary whose keys are version numbers in format x.x.x-xxx
    and values are corresponding AsyncOS item names in list
    """
    VERSION_NUMBER_PATTERN = re.compile(r'AsyncOS ([0-9]+\.[0-9]+\.[0-9]+)')
    BUILD_NUMBER_PATTERN = re.compile(r'build ([0-9]{3,})')

    result_map = {}
    for upgrade_name in all_names:
        version_match = VERSION_NUMBER_PATTERN.search(upgrade_name)
        build_match = BUILD_NUMBER_PATTERN.search(upgrade_name)
        if version_match and build_match:
            key = "%s-%s" % (version_match.group(1),
                             build_match.group(1))
            result_map[key] = upgrade_name
    return result_map


class BaseWizardPage(InputsOwner, GuiCommon):
    PROCEED_BUTTON = "//input[@id='submit_button']"

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    get_registered_inputs = _get_registered_inputs

    def next(self, timeout=1200):
        self.gui.click_button(self.PROCEED_BUTTON)

    def _wait_until_element_present(self, locator, timeout, err_msg):
        SLEEP_INTERVAL = 1
        tmr = CountDownTimer(timeout).start()
        while tmr.is_active():
            time.sleep(SLEEP_INTERVAL)
            if self.gui._is_element_present(locator):
                return
        else:
            raise TimeoutError(err_msg)


class BaseOptionsPage(BaseWizardPage):
    SAVE_CONFIG_CHECKBOX = ('Save the Current Configuration',
                            "//input[@id='save_config']")
    EMAIL_CONFIG = ('Email the Current Configuration to',
                    "//input[@id='config_email']")
    MASK_PASSWORDS_CHECKBOX = ('Mask Passwords in the Configuration File',
                               "//input[@id='mask_passwords']")
    AVAILABLE_UPGRADES_LIST = (UPGRADE_FILE_KEY,
                               "//select[@id='upgrade_file']")
    # This should be overriden in descendants
    UPGRADE_OPERATION_RADIOGROUP = (OPERATIONS_KEY, None)

    def _set_upgrade_name(self, name):
        all_names = self.gui.get_list_items(self.AVAILABLE_UPGRADES_LIST[1])
        if name in all_names:
            self._set_combos(new_value,
                             self.AVAILABLE_UPGRADES_LIST)
        else:
            asyncos_upgrades_map = get_asyncos_upgrades_map(all_names)
            if name in asyncos_upgrades_map:
                self.gui.select_from_list(self.AVAILABLE_UPGRADES_LIST[1],
                                          asyncos_upgrades_map[name])
            else:
                raise ValueError('There is no "%s" upgrade available' % \
                                 (name,))

    def get(self):
        # This takes a little time until content of this page is loaded dynamically
        time.sleep(1)
        result = {}
        result.update(self._get_radio_groups(self.UPGRADE_OPERATION_RADIOGROUP))
        result.update({UPGRADE_FILE_KEY: \
                           self.gui.get_list_items(self.AVAILABLE_UPGRADES_LIST[1])})
        result.update(self._get_values(self.EMAIL_CONFIG))
        result.update(self._get_checkboxes(self.SAVE_CONFIG_CHECKBOX,
                                           self.MASK_PASSWORDS_CHECKBOX))
        return result

    def set(self, new_value):
        # This takes a little time until content of this page is loaded dynamically
        time.sleep(1)
        self._set_radio_groups(new_value,
                               self.UPGRADE_OPERATION_RADIOGROUP)
        assert (UPGRADE_FILE_KEY in new_value)
        self._set_upgrade_name(new_value[UPGRADE_FILE_KEY])
        self._set_checkboxes(new_value,
                             self.SAVE_CONFIG_CHECKBOX,
                             self.MASK_PASSWORDS_CHECKBOX)
        self._set_edits(new_value, self.EMAIL_CONFIG)
        time.sleep(1)


class InitialOptionsPage(BaseOptionsPage):
    """This page appears if no upgrades are
    currently downloaded"""

    UPGRADE_OPERATION_RADIOGROUP = (OPERATIONS_KEY,
                                    {DOWNLOAD_AND_INSTALL_OPERATION: \
                                         "//input[@id='upgrade_operation_upgrade']",
                                     DOWNLOAD_ONLY_OPERATION: \
                                         "//input[@id='upgrade_operation_download']"})

    def next(self, timeout=1200):
        operation = self._get_radio_groups( \
            self.UPGRADE_OPERATION_RADIOGROUP)[OPERATIONS_KEY]
        if operation == DOWNLOAD_ONLY_OPERATION:
            self.gui.click_button(self.PROCEED_BUTTON, 'don\'t wait')
        else:
            self.gui.click_button(self.PROCEED_BUTTON)


class UpgradeDownloadedOptionsPage(BaseOptionsPage):
    """This page appears if an upgrade is
    currently downloaded"""

    DIALOG_OK_BUTTON = ("//div[@id='confirmation_dialog']"
                        "//button[normalize-space()='OK']")
    UPGRADE_OPERATION_RADIOGROUP = (OPERATIONS_KEY,
                                    {INSTALL_OPERATION:
                                         "//input[@id='upgrade_operation_install']",
                                     DOWNLOAD_AND_INSTALL_OPERATION: \
                                         "//input[@id='upgrade_operation_upgrade']",
                                     DOWNLOAD_ONLY_OPERATION: \
                                         "//input[@id='upgrade_operation_download']"})

    def delete_ugrade(self):
        self.gui.click_button(DELETE_FILE_BUTTON, 'don\'t wait')
        self.gui._click_continue_button()

    def next(self, timeout=1200):
        operation = self._get_radio_groups( \
            self.UPGRADE_OPERATION_RADIOGROUP)[OPERATIONS_KEY]
        if operation == INSTALL_OPERATION:
            super(UpgradeDownloadedOptionsPage, self).next(timeout)
        else:
            self.gui.click_button(self.PROCEED_BUTTON, 'don\'t wait')
            self._wait_until_element_present(self.DIALOG_OK_BUTTON, 5,
                                             'Failed to wait until confirmation dialog' \
                                             ' is shown')
            operation = self._get_radio_groups( \
                self.UPGRADE_OPERATION_RADIOGROUP)[OPERATIONS_KEY]
            if operation == DOWNLOAD_ONLY_OPERATION:
                self.gui.click_button(self.DIALOG_OK_BUTTON, 'don\'t wait')
            else:
                self.gui.click_button(self.DIALOG_OK_BUTTON)


class UpgradeProgressPage(BaseWizardPage):
    CONTINUE_BUTTON = "//input[contains(@value, 'Continue')]"
    REBOOT_BUTTON = "//input[@value='Reboot Now']"

    def set(self, new_value):
        # Nothing to set here
        pass

    def next(self, timeout=1200):
        SLEEP_INTERVAL = 2
        tmr = CountDownTimer(timeout).start()
        is_reboot_button_present = False
        while tmr.is_active():
            time.sleep(SLEEP_INTERVAL)
            if self.gui._is_element_present(self.CONTINUE_BUTTON):
                self.gui.click_button(self.CONTINUE_BUTTON)
                break
            elif self.gui._is_element_present(self.REBOOT_BUTTON):
                is_reboot_button_present = True
                break
        else:
            raise TimeoutError('Upgrade download has not been finished' \
                               ' within %d seconds timeout' % (timeout,))
        if not is_reboot_button_present:
            self._wait_until_element_present(self.REBOOT_BUTTON, timeout,
                                             'Upgrade setup has not been finished' \
                                             ' within %d seconds timeout' % (timeout,))
        self.gui.click_button(self.REBOOT_BUTTON)
        self.gui._check_action_result()


class DowloadProgressPage(BaseWizardPage):
    DOWNLOAD_STATUS_TEXT = "//table[@id='download_progress' and not(" \
                           "contains(@style, 'display: none'))]//td[@id='download_progress_text']"

    def set(self, new_value):
        # Nothing to set here
        pass

    def get_download_percentage(self):
        status = self.gui.get_text(self.DOWNLOAD_STATUS_TEXT)
        return int(re.search(r'(\d+)% complete', status).group(1))

    def next(self, timeout=1200):
        try:
            self._wait_until_element_present(CANCEL_DOWNLOAD_BUTTON,
                                             timeout,
                                             'Upgrade download has not been started' \
                                             ' within %d seconds timeout' % (timeout,))
        except TimeoutError:
            # We may call this if download has been already completed
            pass
        self._wait_until_element_present(DELETE_FILE_BUTTON,
                                         timeout,
                                         'Upgrade download has not been finished' \
                                         ' within %d seconds timeout' % (timeout,))
