#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/configuration_file.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

import functools
import time
import re

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
from common.util.sarftime import CountDownTimer
from credentials import DUT_ADMIN_SSW_PASSWORD
from common.cli.clicommon import CliKeywordBase

ACTION_RESULTS = "//div[@id='action-results']"

# Current configuration
DOWNLOAD_TO_LOCAL_COMP_RADIO = "//input[@id='download_operation_id']"
SAVE_TO_APPLIANCE_RADIO = "//input[@id='save_operation_id']"
EMAIL_CONFIG_RADIO = "//input[@id='email_operation_id']"
EMAIL_ADDRS_TEXTBOX = "//input[@id='mailto_id']"
PLAIN_PASSWORD_RADIO = "//input[@id='plain']"
MASK_PASSWORD_RADIO = "//input[@id='mask']"
ENCRYPT_PASSWORD_RADIO = "//input[@id='encrypt']"
SUBMIT_BUTTON = "//input[@value='Submit']"

# Load configuration
LOAD_CONFIG_RADIO = "//input[@id='load_from_appliance_id']"
CONFIG_FILENAME_LIST = "//select[@id='appliance_filename_id']"
UPLOAD_CONFIG_RADIO = "//input[@id='load_from_local_id']"
PASTE_CONFIG_RADIO = "//input[@id='load_from_buffer_id']"
PASTE_CONFIG_TEXTBOX = "//textarea[@id='config_buffer_id']"
LOAD_BUTTON = 'xpath=//input[@value="Load"]'
ENTER_PASSWORD_TEXTBOX = "//input[@id='old_pwd']"
LOAD_CONFIG_FOR = "//select[@id='load_for']"
LOAD_CLUSTER_CONFIG_PAGE = "//div[@id='load_config_dialog_hd']"
APPLIANCE_GROUP_DROPDOWN = "//span[@class='add_info']/../../div/../../td[2]/div/select"
REVIEW_BUTTON = "//button[contains(text(), 'Review')]"
COMFIRM_BUTTON = "//button[contains(text(), 'Confirm')]"
REVIEW_CLUSTER_STRUCTURE = "//div[@id='review_h2']"

# End-User Safelist/Blocklist Database (Spam Quarantine)
SLBL_BACKUP_BUTTON = "//input[@value='Backup Now']"
SLBL_SELECT_TO_RESTORE_BUTTON = "//input[@value='Select File to Restore...']"
SLBL_FILE_LIST = "//select[@id='slbl_filename_id']"
SLBL_IGNORE_INVALID_ADDRESSES_CHECKBOX = "//input[@id='ignore_invalid_addresses']"

# Reset Configuration
RESET_BUTTON = 'xpath=//input[@value="Reset"]'

PAGE_PATH = ('System Administration', 'Configuration File')


def check_slbl_feature(func):
    """Decorator is used for ConfigurationFile class methods
    for checking if SLBL feature is enabled.

    *Exceptions:*
    - `GuiFeatureDisabledError`: if SLBL feature is not enabled
    """
    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        if not (self._is_element_present(SLBL_BACKUP_BUTTON) and \
                self._is_element_present(SLBL_SELECT_TO_RESTORE_BUTTON)):
            raise guiexceptions.GuiFeatureDisabledError('SLBL'\
                ' feature should be enabled on appliance in order to use '\
                ' this functionality')

        return func(self, *args, **kwargs)
    return decorator

class SSLConfig(CliKeywordBase):
    def ssl_tls_version_reset(self):
        try:
            kwargs = {'ssl_method':'TLS v1/TLS v1.2'}
            stat = self._cli.sslconfig().gui(**kwargs)
        except Exception:
            try:
                kwargs = {'ssl_method':'TLS v1.0'}
                stat = self._cli.sslconfig().gui(**kwargs)
            except Exception:
                kwargs = {'ssl_method':'3'}
                stat = self._cli.sslconfig().gui(**kwargs)
        self._cli.commit('SSL TLS version is changed..')

class ConfigurationFile(GuiCommon):
    """Keywords for interaction wit System Administration -> Configuration File
    page
    """

    def get_keyword_names(self):
        return ['configuration_save',
                'configuration_load',
                'configuration_slbl_backup',
                'configuration_slbl_restore',
                'configuration_reset']

    def _get_saved_config_name(self):
        result_msg = self.get_text(ACTION_RESULTS)
        m = re.search(r"'(.*)'", result_msg)
        return m.groups()[0]

    def _check_restore_result(self, timeout=60):
        """
        Check if SLBL database was restored successfully
        within timeout seconds.
        Consider all restore successful if actiob result is
        Success and message contains 'complete'.
        """
        timer = CountDownTimer(timeout).start()
        while timer.is_active():
            try:
                res, msg = self._check_action_result()
                result = '%s: %s' % (res, msg)
            except guiexceptions.GuiValueError as err:
                result = err
            time.sleep(1.0)
            if all([msg in result.lower() for msg in ('success', 'complete')]):
                return
        raise guiexceptions.TimeoutError\
            ('Failed to restore SLBL database within %s seconds timeout' \
            % (timeout,))

    def _check_if_gui_is_responsive(self, timeout=60):
        """Check if GUI is responsive to Selenium
        commands. It simply tries to navigate current
        page and repeat this if failed

        *Parameters:*
        - `timeout`: max. number of seconds to wait for
        GUI response

        *Exceptions:*
        - `TimeoutError`: if failed to navigate current page
        with Selenium within the current timeout
        """
        timer = CountDownTimer(timeout).start()
        while timer.is_active():
            try:
                self.navigate_to(*PAGE_PATH)
                return
            except Exception as e:
                self._debug(str(e))
            time.sleep(1.0)
        raise guiexceptions.TimeoutError('Failed to check if GUI is responsive'
                                         ' after configuration load within %d'\
                                         ' seconds timeout' % (timeout,))

    @go_to_page(PAGE_PATH)
    def configuration_save(self, save_mode, **kwargs):
        """Save appliance configuration

        *Parameters:*
        - `save_mode`: one of three save modes. Either:
        | Download file to local computer to view or save |
        | Save file to this appliance |
        | Email file to |
        - `email`: email to which config file should be sent.
        Mandatory if save_mode is set to `Email file to`
        - `should_mask_passwords`: whether to mask passwords
        in the generated config file. Either ${True} or ${False}.
        If it is given as ${False} and 'encrypt_passwords' is also ${False},
	then it is considered as plain passwords.
        - `encrypt_passwords`: provided 'should_mask_passwords' is given as ${False}.
        whether to encrypt the passwords in the generated config file.
        Either ${True} or ${False}. ${False} means plain passwords.

        *Exceptions*:
        - `ValueError`: if any of passed values is unknown or incorrect

        *Return:*
        Result configuration file name (only if save_mode is set to
        `Save file to this appliance`)

        *Examples:*
        | Configuration Save | Email file to | email=mm@example.com |
        | ... | should_mask_passwords=${True} |

        | ${filename}= | Configuration Save | Save file to this appliance |
        | ... | should_mask_passwords=${False} |

        | ${filename}= | Configuration Save | Save file to this appliance |
        | ... | should_mask_passwords=${False} | encrypt_passwords=${True} |

        | ${filename}= | Configuration Save | Save file to this appliance |
        | ... | should_mask_passwords=${False} | encrypt_passwords=${False} |
        """
        if save_mode.lower() == 'download file to local computer to view or save':
            self._click_radio_button(DOWNLOAD_TO_LOCAL_COMP_RADIO)
            raise NotImplementedError('Implement configuration file saving on local '\
                                      'computer')
        elif save_mode.lower() == 'save file to this appliance':
            self._click_radio_button(SAVE_TO_APPLIANCE_RADIO)
        elif save_mode.lower() == 'email file to':
            if kwargs.has_key('email'):
                self._click_radio_button(EMAIL_CONFIG_RADIO)
                self.input_text(EMAIL_ADDRS_TEXTBOX, kwargs['email'])
            else:
                raise ValueError('Email argument is mandatory for "%s" option' % \
                                 (save_mode,))
        else:
            raise ValueError('Unknown option "%s" is passed' % (save_mode,))

        if kwargs.has_key('should_mask_passwords') and kwargs['should_mask_passwords']:
            self._click_radio_button(MASK_PASSWORD_RADIO)
        elif kwargs.has_key('encrypt_passwords') and kwargs['encrypt_passwords']:
            self._click_radio_button(ENCRYPT_PASSWORD_RADIO)
        else:
            self._click_radio_button(MASK_PASSWORD_RADIO)


        self.click_button(SUBMIT_BUTTON)
        self._check_action_result()

        if save_mode.lower() == 'save file to this appliance':
            return self._get_saved_config_name()

    @go_to_page(PAGE_PATH)
    def configuration_load(self, load_mode, **kwargs):
        """Load appliance configuration

        *Parameters:*
        - `load_mode`: one of three load modes. Either:
        | Load a configuration file from the appliance |
        | Load a configuration file from local computer |
        | Paste configuration |
        - `filename`: name of file on appliance from which
        confguration will be loaded. Mandatory if load_mode
        is set to `Load a configuration file from the appliance`
        - `content`: custom content of config file (string).
        Mandatory if load_mode is set to `Paste configuration`
        - `password`: Provide user password to load the config.
        Default: admin password

        *Exceptions*:
        - `ValueError`: if any of passed values is unknown or incorrect

        *Examples:*
        | Configuration Load | Load a configuration file from the appliance |
        | ... | filename=C600-001143ECE913-54MNP61-20120807T121804.xml |
        | ... | password=Cisco123$ |

        | Configuration Load | Load a configuration file from the appliance |
        | ... | filename=C600-001143ECE913-54MNP61-20120807T121804.xml |
        | ... | password=${operator_password} |

        | Configuration Load | Paste configuration |
        | ... | content=ololo |
        """
        if load_mode.lower() == 'load a configuration file from the appliance':
            self._click_radio_button(LOAD_CONFIG_RADIO)
            if kwargs.has_key('filename'):
                try:
                    self.select_from_list(CONFIG_FILENAME_LIST,
                                          kwargs['filename'])
                except Exception:
                    raise ValueError('There is no file named "%s" present '\
                                     'in list' % (kwargs['filename'],))
            else:
                raise ValueError('Filename argument is mandatory for "%s" option' % \
                                 (load_mode,))
        elif load_mode.lower() == 'load a configuration file from local computer':
            self._click_radio_button(UPLOAD_CONFIG_RADIO)
            raise NotImplementedError('Implement configuration file loading from '\
                                      'the local computer')
        elif load_mode.lower() == 'paste configuration':
            if kwargs.has_key('content'):
                self._click_radio_button(PASTE_CONFIG_RADIO)
                self.input_text(PASTE_CONFIG_TEXTBOX, kwargs['content'])
            else:
                raise ValueError('Content argument is mandatory for "%s" option' % \
                                 (load_mode,))
        else:
            raise ValueError('Unknown option "%s" is passed' % (load_mode,))
        if self._is_element_present(LOAD_CONFIG_FOR):
            cluster_load_mode = "YES"
        else:
            cluster_load_mode = "NO"
        self.click_button(LOAD_BUTTON, 'don\'t wait')
        if cluster_load_mode.lower() == 'yes':
            value = "Main_Group"
            self._wait_until_element_is_present(LOAD_CLUSTER_CONFIG_PAGE, timeout=30)
            for dropdown in self.find_elements(APPLIANCE_GROUP_DROPDOWN):
		        self.select_from_list( dropdown, value)
            self.click_button(REVIEW_BUTTON, 'don\'t wait')
            self._is_element_present(REVIEW_CLUSTER_STRUCTURE)
            self.click_button(COMFIRM_BUTTON, 'don\'t wait')
        action_res = self._click_continue_button()
        self._check_if_gui_is_responsive()
        return action_res

    def _get_saved_slbl_config_name(self):
        result_msg = self.get_text(ACTION_RESULTS)
        m = re.search(r'The data was saved to (.*)\.', result_msg)
        return m.groups()[0]

    @go_to_page(PAGE_PATH)
    @check_slbl_feature
    def configuration_slbl_backup(self):
        """Backup appliance's SLBL database

        *Exceptions*:
        - `TimeoutError`: if backup has not been completed within
        acceptable timeout
        - `GuiFeatureDisabledError`: if SLBL feature is not enabled

        *Return:*
        Result SLBL backup file name.

        *Examples:*
        | ${filename}= | Configuration SLBL Backup |
        """
        self.click_button(SLBL_BACKUP_BUTTON)
        self._check_action_result()
        return self._get_saved_slbl_config_name()

    @go_to_page(PAGE_PATH)
    @check_slbl_feature
    def configuration_slbl_restore(self, filename, **kwargs):
        """Restore appliance's SLBL database

        *Parameters:*
        - `filename`: existing file name on appliance from where
        SLBL DB backup will be restored, mandatory
        - `should_ignore_invalid_addresses`: whether to ignore
        invalid addresses on restore

        *Exceptions*:
        - `ValueError`: if there is no file found on appliance
        with given name
        - `GuiFeatureDisabledError`: if SLBL feature is not enabled

        *Examples:*
        | Configuration SLBL Restore | my_slbl_backup.csv |
        | ... | should_ignore_invalid_addresses=${False} |
        """
        self.click_button(SLBL_SELECT_TO_RESTORE_BUTTON)
        try:
            self.select_from_list(SLBL_FILE_LIST, filename)
        except Exception:
            raise ValueError('There is no file named "%s" on appliance '\
                             'for SLBL database restore' % (filename,))
        if kwargs.has_key('should_ignore_invalid_addresses'):
            self._select_unselect_checkbox(SLBL_IGNORE_INVALID_ADDRESSES_CHECKBOX,
                                           kwargs['should_ignore_invalid_addresses'])

        self.click_button(SUBMIT_BUTTON, 'don\'t wait')
        self._click_continue_button()
        self._check_restore_result()

    @go_to_page(PAGE_PATH)
    def configuration_reset(self):
        """Reset appliance configuration

        *Examples:*
        | Configuration Reset |
        """
        self.click_button(RESET_BUTTON, 'don\'t wait')
        self._click_continue_button()
        SSLConfig(self.dut, self.dut_version).ssl_tls_version_reset()
        self._check_if_gui_is_responsive()
