# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/administration/configuration_file.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

import re
import common.gui.guiexceptions as guiexceptions

from common.gui.guicommon import GuiCommon


DOWNLOAD_CONFIG_RADIOBUTTON = 'id=download_operation_id'
EMAIL_CONFIG_RADIOBUTTON = 'id=email_operation_id'
EMAIL_ADDRS_TEXTBOX = 'id=mailto_id'
SAVE_CONFIG_RADIOBUTTON = 'id=save_operation_id'
SAVE_CONFIG_TO_PC_RADIOBUTTON= 'id=download_operation_id'
MASK_PASSWORDS_CHECKBOX = 'id=mask_passwords'
ENCRYPT_PASSWORDS_RADIOBUTTON = 'id=encrypt'
MASK_PASSWORDS_RADIOBUTTON = 'id=mask'
LOAD_CONFIG_RADIOBUTTON = 'id=load_from_appliance_id'
UPLOAD_CONFIG_RADIOBUTTON = 'id=load_from_local_id'
PASTE_CONFIG_RADIOBUTTON = 'id=load_from_buffer_id'
FILE_PATH_TEXTBOX = 'id=local_file_id'
CONFIG_FILENAME_LIST = 'id=appliance_filename_id'
CONFIG_TEXTBOX = 'id=config_buffer_id'
LOAD_BUTTON = 'xpath=//input[@value="Load"]'
BACKUP_NOW_BUTTON = 'xpath=//input[@value="Backup Now"]'
RESTORE_BUTTON = 'xpath=//input[@name="slbl_restore"]'
RESTORE_BUTTON_DISABLED = \
    'xpath=//input[@name="slbl_restore" and contains(@class, "disabled")]'
BACKUP_FILES_LIST = 'id=slbl_filename_id'
IGNORE_INVALID_CHECKBOX = 'id=ignore_invalid_addresses'
RESET_BUTTON = 'xpath=//input[@value="Reset"]'


class ConfigurationFile(GuiCommon):

    """
    Keyword library for WebUI page Management Appliance -> System Administration
    ->Configuration File
    """

    def get_keyword_names(self):
        return [
                'configuration_file_download_config',
                'configuration_file_save_config',
                'configuration_file_email_config',
                'configuration_file_load_config',
                'configuration_file_upload_config',
                'configuration_file_paste_config',
                'configuration_file_backup_slbl',
                'configuration_file_restore_slbl',
                'configuration_file_reset',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration',
                               'Configuration File')

    def _click_download_to_local_computer(self):
        self._click_radio_button(DOWNLOAD_CONFIG_RADIOBUTTON)
        self._info('Clicked "Download to local computer" radiobutton.')

    def _click_email_config_file(self):
        self.click_button(EMAIL_CONFIG_RADIOBUTTON, "don't wait")
        self._info('Clicked "Email file to" radio button.')

    def _click_save_to_appliance(self):
        self._click_radio_button(SAVE_CONFIG_RADIOBUTTON)
        self._info('Clicked "Save to appliance" radiobutton.')

    def _click_save_to_local_computer(self):
        self._click_radio_button(SAVE_CONFIG_TO_PC_RADIOBUTTON)
        self._info('Clicked "Save to local computer" radiobutton.')


    def _get_filename(self):
        cfg_file_patt = re.compile('as \'(.*?)\'')
        text = self.get_text('//*[@id=\'action-results-message\']')
        result = cfg_file_patt.search(text)
        if result:
            return result.group(1)

    def _fill_email_addrs(self, email_addrs):
        self.input_text(EMAIL_ADDRS_TEXTBOX, email_addrs)
        self._info('Set email address(es) to "%s".' % (email_addrs))

    def _enable_passwords_masking(self, enable):
        if enable:
            try:
               self.select_checkbox(MASK_PASSWORDS_CHECKBOX)
               self._info('Enabled passwords masking.')
            except:
               self.click_button(MASK_PASSWORDS_RADIOBUTTON, "don't wait")
               self._info('Mask passphrases.')
        else:
            try:
               self.unselect_checkbox(MASK_PASSWORDS_CHECKBOX)
               self._info('Disabled passwords masking.')
            except:
               self.click_button(ENCRYPT_PASSWORDS_RADIOBUTTON, "don't wait")
               self._info('Encrypt passphrases.')

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
            raise ValueError('"%s" config filename is not present.' % (filename,))
        self.select_from_list(CONFIG_FILENAME_LIST, filename)
        self._info('Selected "%s" config file.' % (filename,))

    def _fill_configuration_textbox(self, configuration):
        self.input_text(CONFIG_TEXTBOX, configuration)
        self._info('Pasted configuration into textbox.')

    def _click_load_button(self):
        self.click_button(LOAD_BUTTON, "don't wait")
        self._check_action_result()
        self._info('Clicked "Load" button.')

    def _is_slbl_enabled(self):
        if self._is_element_present(BACKUP_NOW_BUTTON) and\
           self._is_element_present(RESTORE_BUTTON):
            return True
        return False

    def _click_backup_now_button(self):
        self.click_button(BACKUP_NOW_BUTTON, "don't wait")
        self._info('Clicked "Backup Now" button.')

    def _get_slbl_filename(self):
        self._check_action_result()
        # Page will be reloaded one more time
        text = self.get_text('id=action-results-message')
        result = re.search('was saved to\s+(.*?\.csv)', text)
        self._info("Was Saved to : %s" %(result,))
        if result:
            return result.group(1)

    def _click_restore_button(self):
        if self._is_element_present(RESTORE_BUTTON_DISABLED):
            raise guiexceptions.GuiError(
                            'Restore button is disabled.')

        self.click_button(RESTORE_BUTTON)
        self._info('Clicked "Select File to Restore" button.')

    def _select_slbl_file(self, filename):
        backup_files = self.get_list_items(BACKUP_FILES_LIST)

        if filename not in backup_files:
            raise ValueError('%s backup filename does not exist.' % (filename,))

        self.select_from_list(BACKUP_FILES_LIST, filename)
        self._info('Selected "%s" file.' % (filename,))

    def _check_ignore_invalid(self, ignore):
        if ignore:
            self.select_checkbox(IGNORE_INVALID_CHECKBOX)
            self._info('Checked "Ignore Invalid" checkbox.')
        else:
            self.unselect_checkbox(IGNORE_INVALID_CHECKBOX)
            self._info('Unchecked "Ignore Invalid" checkbox.')

    def _click_reset_button(self):
        self.click_button(RESET_BUTTON, "don't wait")
        self._info('Clicked "Reset" button.')

    def _wait_for_slbl_restore_complete(self):
        completed_msg = 'Restore of the Safelist/Blocklist database is complete'
        self.wait_until_page_contains(completed_msg, 120)

    def configuration_file_download_config (self, mask_passwd=False):
        """Download current configuration to local computer.
        ("Configure Autodownload For Browser" keyword should be used before using this keyword)

        *Parameters*
            - `mask_passwd`: mask passwords in the configuration file. Boolean.
            Default value is ${False}.

        *Exeptions*
            None.

        *Examples*
        | Configure Autodownload For Browser | ${TEMPDIR} | text/xml |
        | Launch DUT Browser |
        | Log Into DUT |
        | ${start_time}= | Get Time |
        | Configuration File Download Config |
        | ${saved_config1}= | Wait For Download | .xml | start_time=${start_time} |
        | ${start_time}= | Get Time |
        | Configuration File Download Config | mask_passwd=${True} |
        | ${saved_config2}= | Wait For Download | .xml | start_time=${start_time} |
        """
        self._info('Saving configuration file to appliance.')

        self._open_page()

        self._click_download_to_local_computer()

        self._enable_passwords_masking(mask_passwd)

        self._click_submit_button(wait=False, skip_wait_for_title=True)

    def configuration_file_save_config (self, mask_passwd=False):
        """Save current configuration to the appliance.

        *Parameters*
            - `mask_passwd`: mask passwords in the configuration file. Boolean.
            Default value is ${False}.

        *Return*
            String containing name of the configuration file saved on the
            appliance.

        *Exeptions*
            None.

        *Examples*
            | Configuration File Save Config |
            | Configuration File Save Config | mask_passwd=${True} |
        """
        self._info('Saving configuration file to appliance.')

        self._open_page()

        self._click_save_to_appliance()

        self._enable_passwords_masking(mask_passwd)

        self._click_submit_button()

        return self._get_filename()

    def configuration_file_email_config(self, email_addrs, mask_passwd=False):
        """Email current configuration of the appliance.

        *Parameters*
            - `email_addrs`: comma-separated string of email addresses to send
                configuration to.
            - `mask_passwd`: mask passwords in the configuration file. Boolean.
            Default value is ${False}.

        *Return*
            None.

        *Exeptions*
            None.

        *Examples*
            | Configuration File Email Config | user@site.com  |
            | Configuration File Email Config |
            | ... | anyuser@anysite.com, anyuser1@anysite.com | mask_passwd=${True} |

        """
        self._info('Emailing configuration file.')

        self._open_page()

        self._click_email_config_file()

        self._fill_email_addrs(email_addrs)

        self._enable_passwords_masking(mask_passwd)

        self._click_submit_button()

    def configuration_file_load_config(self, filename):
        """Load configuration from the appliance.

        *Parameters*
            - `filename`: name of the file to load.

        *Return*
            None.

        *Exceptions*
            - `ValueError`: if desired filename does not exist

        *Examples*
            | Configuration File Load Config | /data/myconf.xml |
            | Configuration File Load Config | file.xml |
        """
        self._info('Loading "%s" configuration file.' % (filename,))

        self._open_page()

        self._click_load_from_appliance()

        self._select_config_file(filename)

        self._click_load_button()

        self._click_continue_button()

        self._info('Loaded configuration from "%s" file.' % (filename,))

    def configuration_file_upload_config (self, filepath):
        """Upload configuration file from local machine to appliance.

        *Parameters*
            - `filepath`: path to the configuration file on local machine.

        *Return*
            None.

        *Exception*
            None.

        *Examples*
            | Configuration File Upload Config | /data/myconf.xml |
            | Configuration File Upload Config | myconf.xml |

        """
        self._info('Uploading configuration file to the appliance.')

        self._open_page()

        self._click_load_from_local()

        self._fill_local_file_path(filepath)

        self._click_load_button()

        self._click_continue_button()

        self._info('Uploaded configuration from "%s" file.' % (filepath,))


    def configuration_file_paste_config(self, configuration):
        """Paste configuration into appliance.

        *Parameters*
            - `configuration`: string containing XML configuration to paste
                 into appliance.

        *Return*
            None.

        *Exceptions*
            None.

        *Examples*
        | Configuration File Paste Config |
        | ... | <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE config SYSTEM "config.dtd"><config><update_interval>600</update_interval></config> |
        """
        self._info('Pasting configuration into appliance.')

        self._open_page()

        self._click_paste_config()

        self._fill_configuration_textbox(configuration)

        self._click_load_button()

        self._click_continue_button()

        self._info('Pasted configuration into appliance.')

    def configuration_file_backup_slbl(self):
        """Backup SLBL Database.  SLBL have to be  enabled.

        *Return*
            String containing name of the backup file saved on the appliance.

        *Exceptions*
            - `GuiFeatureDisabledError`: if SLBL is disabled

        *Examples*
            | Configuration File Backup Slbl |
        """
        self._info('Backing up SLBL Database')

        self._open_page()

        if not self._is_slbl_enabled():
            raise guiexceptions.GuiFeatureDisabledError(
                    'SLBL must be enabled first.')

        self._click_backup_now_button()

        return self._get_slbl_filename()


    def configuration_file_restore_slbl(self, filename, ignore_invalid=None):
        """Restore SLBL Database.  SLBL have to be  enabled.

        *Parameters*
            - `filename`: name of the file to restore database from.
            - `ignore_invalid`: ignore invalid entries. Boolean or ${None}.
                ${None} to use system default. Default value is ${None}.

        *Return*
            None.

        *Exceptions*
            - `ValueError`: if backup filename does not exist
            - `GuiFeatureDisabledError`: if SLBL is disabled

        *Examples*
            | Configuration File Restore Slbl | filename.back |
            | Configuration File Restore Slbl | myfilename | ignore_invalid=${False} |
        """
        self._info('Restoring SLBL Database %s ' %(filename,))

        self._open_page()

        if not self._is_slbl_enabled():
            raise guiexceptions.GuiFeatureDisabledError(
                            'SLBL must be enabled first.')

        self._click_restore_button()

        self._select_slbl_file(filename)

        if ignore_invalid is not None:
            self._check_ignore_invalid(ignore_invalid)

        self._click_submit_button(wait=False, accept_confirm_dialog=True)
        self._wait_for_slbl_restore_complete()

        self._info('Restored SLBL Database from "%s" file.' %\
                         (filename,))

    def configuration_file_reset(self):
        """Reset current configuration to factory default settings.

        *Return*
            None.

        *Exceptions*
            None.

        *Examples*
            | Configuration File Reset |
        """
        self._info('Resetting current configuration.')

        self._open_page()

        self._click_reset_button()

        self._click_continue_button()

        self._info('Configuration has been reset.')
