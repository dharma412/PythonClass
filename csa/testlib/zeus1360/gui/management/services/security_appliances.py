# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/services/security_appliances.py#1 $
# $DateTime: 2020/03/05 19:45:32 $
# $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import (GuiCommon, Wait)
from sma.constants import sma_config_masters

from common.util.sarftime import CountDownTimer
import time
import re


EMAIL_APPL_TYPE = 'Email'
WEB_APPL_TYPE = 'Web'

APPLIANCES_STATUS_TEXT = lambda appl_type, row:\
    "//div[@class='group']/s[contains(text(), '%s')]"\
    "/following::div[@class='text-info'][%s]" % (appl_type, row)
APPL_NAME_FIELD = 'name'
APPL_ADDRESS_FIELD = 'ip'
CONNECTION_STATUS_TEXT = 'establish-status'

EMAIL_APPL_TABLE_PREFIX = "//div[@class='group']/s[contains(text(), 'Email')]"\
    "/following::"
ADD_EMAIL_APPL_BUTTON = 'AddEmailAppliance'
DELETE_EMAIL_APPL_TABLE_CELL = lambda row: EMAIL_APPL_TABLE_PREFIX + \
    "table[following-sibling::div[@class='group']][1]//tr[%s]/td[8]/img" % (row,)
EDIT_EMAIL_APPL_TABLE_CELL = lambda row: EMAIL_APPL_TABLE_PREFIX + \
    "table[following-sibling::div[@class='group']][1]//tr[%s]/td/a" % (row,)
EMAIL_ISQ_SERVICE_CHECKBOX = 'euq'
EMAIL_PVO_SERVICE_CHECKBOX= 'cpq'
EMAIL_REPORTING_SERVICE_CHECKBOX = 'reporting'
EMAIL_TRACKING_SERVICE_CHECKBOX = 'tracking'

WEB_APPL_TABLE_PREFIX = "//div[@class='group']/s[contains(text(), 'Web')]"\
    "/following::"
ADD_WEB_APPL_BUTTON = 'AddWebAppliance'
DELETE_WEB_APPL_TABLE_CELL = lambda row: WEB_APPL_TABLE_PREFIX + \
    "table[not(following-sibling::div[@class='group'])][1]//tr[%s]/td[9]/img" % (row,)
EDIT_WEB_APPL_TABLE_CELL = lambda row: WEB_APPL_TABLE_PREFIX + \
    "table[not(following-sibling::div[@class='group'])][1]//tr[%s]/td[1]/a" % (row,)
WEB_REPORTING_SERVICE_CHECKBOX = 'web_reporting'
WEB_UPGRADE_SERVICE_CHECKBOX = 'upgrade'
WEB_ICCM_SERVICE_CHECKBOX = 'iccm'
WEB_CONFIRM_ICCM_DISABLE_BUTTON =\
    "//button[@type='button' and contains(text(), 'Ok')]"
WEB_NO_MASTER_ASSIGN_RADIOBUTTON = 'not_assigned'
WEB_MASTER_75_RADIOBUTTON = 'coeus_7_5'
WEB_MASTER_77_RADIOBUTTON = 'coeus_7_7'
WEB_MASTER_80_RADIOBUTTON = 'coeus_8_0'
WEB_MASTER_91_RADIOBUTTON = 'coeus_8_5'
WEB_MASTER_105_RADIOBUTTON = 'coeus_10_5'
WEB_MASTER_110_RADIOBUTTON = 'coeus_10_0'
WEB_MASTER_115_RADIOBUTTON = 'coeus_10_0'
WEB_MASTER_117_RADIOBUTTON = lambda master: 'coeus_11_7-%s'  % (master,)

ESTABLISH_CONNECTION_DIALOG = "//div[@id='config_host']"
ESTABLISH_CONNECTION_BUTTON = 'btnConf'
ESTABLISH_CONNECTION_USER_TEXTBOX = 'remote_host_username'
ESTABLISH_CONNECTION_PASSWD_TEXTBOX = 'remote_host_passwd'
ESTABLISH_CONNECTION_LOGIN_BUTTON = "//button[text() = 'Establish Connection']"


class SecurityAppliances(GuiCommon):

    """Keywords for Management Appliance -> Centralized Services -> Security
    Appliances
    """

    def get_keyword_names(self):
        return ['security_appliances_add_email_appliance',
                'security_appliances_edit_email_appliance',
                'security_appliances_delete_email_appliance',
                'security_appliances_get_email_appliance_names',
                'security_appliances_get_email_appliance_data',
                'security_appliances_add_web_appliance',
                'security_appliances_edit_web_appliance',
                'security_appliances_delete_web_appliance',
                'security_appliances_get_web_appliance_names',
                'security_appliances_get_web_appliance_data',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'Centralized Services',
            'Security Appliances')

    def _click_add_email_appliance_button(self):
        self._check_appliances_status(EMAIL_APPL_TYPE, True)
        self.click_button(ADD_EMAIL_APPL_BUTTON)

    def _fill_esa_appliance_page(self, name, address, isq, pvo, reporting,
        tracking):
        self._fill_appliance_name(name)

        self._fill_appliance_address(address)

        self._select_esa_services(isq, pvo, reporting, tracking)

    def _select_esa_services(self, isq, pvo, reporting, tracking):
        services = (
            (EMAIL_ISQ_SERVICE_CHECKBOX, isq, 'Spam Quarantine'),
            (EMAIL_PVO_SERVICE_CHECKBOX, pvo, 'Policy, Virus and Outbreak Quarantines'),
            (EMAIL_REPORTING_SERVICE_CHECKBOX, reporting,
                'Centralized Reporting'),
            (EMAIL_TRACKING_SERVICE_CHECKBOX, tracking, 'Message Tracking')
        )
        for service_option in services:
            self._set_service_status(*service_option)

    def _click_add_web_appliance_button(self):
        self._check_appliances_status(WEB_APPL_TYPE, True)
        self.click_button(ADD_WEB_APPL_BUTTON)

    def _fill_web_appliance_page(self, name, address, iccm, reporting, upgrade):
        self._fill_appliance_name(name)

        self._fill_appliance_address(address)

        self._select_wsa_services(iccm, reporting, upgrade)

    def _select_wsa_services(self, iccm, reporting, upgrade):
        if iccm is not None:
            iccm = bool(iccm)
            if self._is_element_disabled(WEB_ICCM_SERVICE_CHECKBOX):
                raise guiexceptions.GuiFeatureDisabledError(
                    'ICCM service is disabled')

            if iccm and not self._is_checked(WEB_ICCM_SERVICE_CHECKBOX):
                self.click_button(WEB_ICCM_SERVICE_CHECKBOX, 'dont wait')
            elif not iccm and self._is_checked(WEB_ICCM_SERVICE_CHECKBOX):
                self.click_button(WEB_ICCM_SERVICE_CHECKBOX, 'dont wait')

                # A dialog is shown when disabling ICCM for appliance that has
                # been assigned to Configuration Master.
                if self._is_element_present(WEB_CONFIRM_ICCM_DISABLE_BUTTON):
                    self.click_button(WEB_CONFIRM_ICCM_DISABLE_BUTTON, 'dont wait')

        self._set_service_status(WEB_REPORTING_SERVICE_CHECKBOX, reporting,
            'Centralized Web Reporting')

        self._set_service_status(WEB_UPGRADE_SERVICE_CHECKBOX, upgrade, 'Centralized Upgrades')

    def _select_config_master(self, master):
        if master is None:
            return

        masters_map = {
            sma_config_masters.CM77: WEB_MASTER_77_RADIOBUTTON,
            sma_config_masters.CM80: WEB_MASTER_80_RADIOBUTTON,
            sma_config_masters.CM91: WEB_MASTER_91_RADIOBUTTON,
            sma_config_masters.CM105: WEB_MASTER_105_RADIOBUTTON,
            sma_config_masters.CM110: WEB_MASTER_110_RADIOBUTTON,
            sma_config_masters.CM115: WEB_MASTER_115_RADIOBUTTON,
            sma_config_masters.CM117: WEB_MASTER_117_RADIOBUTTON
        }

        if not master:
            self._click_radio_button(WEB_NO_MASTER_ASSIGN_RADIOBUTTON)
            return


        master = re.sub('Configuration Master ','', master)
        locator = "//table[@class='pairs']//tr[5]/td/table/tbody/tr"
        element_count = int(self.get_matching_xpath_count(locator))
        for i in range(1, element_count+1):
            locator =  lambda i: "//table[@class='pairs']//tr[5]/td/table/tbody/tr[%s]/td/input" % (i,)
            _id = self.get_element_attribute("xpath="+locator(i)+"@id")

            if master in _id:
                self._click_radio_button(_id)
                break
        else:
            raise ValueError('Config Master %s Not Present' % (master))

        #master_loc = masters_map.get(master)
        #if re.match(r"[A-Za-z]+(\d+_\d+)",master):
        #    master_new = re.sub (r'_',r'.', conf_master.group(1))
        #    master_new = "Configuration Master " + master
        #    print master_new
        #    master_loc = masters_map.get(master_new)

        #if master_loc is None:
        #    raise guiexceptions.GuiValueError('Invalid `%s` value for CM '\
        #         'name' % (master,))

        #if self.get_text(CONNECTION_STATUS_TEXT).strip() == 'Not established.':
        #    raise guiexceptions.ConfigError('Connection to WSA appliance '\
        #        'must be established first')

        #if not self._is_element_present(master_loc) or\
        #    self._is_element_disabled(master_loc):
        #    raise guiexceptions.GuiFeatureDisabledError('`%s` is not '\
        #        'available' % (master,))

        #master = re.sub('Configuration Master ','', master)
        #self._click_radio_button(master_loc(master))

    def _click_edit_appliance_link(self, name, appl_type):
        self._check_appliances_status(appl_type, True, True)
        delete_cell, edit_cell = self._get_table_cells_locators(appl_type)
        index = self._get_appliance_row_index(name, delete_cell, edit_cell)
        self.click_element(edit_cell(index))

    def _click_delete_appliance_link(self, name, appl_type):
        self._check_appliances_status(appl_type, True, True)
        delete_cell, edit_cell = self._get_table_cells_locators(appl_type)
        index = self._get_appliance_row_index(name, delete_cell, edit_cell)

        self.click_element(delete_cell(index), 'dont wait')
        self._click_continue_button()

    def _fill_appliance_name(self, name):
        if name is None:
            return

        self.input_text(APPL_NAME_FIELD, name)

    def _fill_appliance_address(self, address):
        if address is None:
            return

        self.input_text(APPL_ADDRESS_FIELD, address)

    def _establish_connection(self, credentials, timeout):
        print "timeout in establish %s" % (timeout,)
        if credentials is None:
            return

        try:
            username, password = credentials.split(':')
        except ValueError:
            raise guiexceptions.GuiValueError('`ssh_credentials` should be '\
                'in `username:password` format.')

        self.click_button(ESTABLISH_CONNECTION_BUTTON, 'dont wait')

        try:
            Wait(
                lambda: self._is_visible(ESTABLISH_CONNECTION_DIALOG),
                timeout=timeout
            ).wait()
        except guiexceptions.TimeoutError:
            pass
        self.input_text(ESTABLISH_CONNECTION_USER_TEXTBOX, username)
        self.input_text(ESTABLISH_CONNECTION_PASSWD_TEXTBOX, password)

        self.click_button(ESTABLISH_CONNECTION_LOGIN_BUTTON, 'dont wait')

        # It may take some time to establish connection.
        try:
            Wait(
                lambda: not self._is_visible(ESTABLISH_CONNECTION_DIALOG),
                timeout=timeout
            ).wait()
        except guiexceptions.TimeoutError:
            pass

        self._check_action_result()

    def _is_element_disabled(self, locator):
        if len(locator)>6 and locator[:6] == 'xpath=':
            locator = locator[6:]
        if (len(locator)>2 and locator[:2] != '//') or len(locator)<=2:
            locator = "//*[@id='%s']" % (locator,)
        disabled_loc = locator + "/self::*[@disabled='disabled']"
        element_count = int(self.get_matching_xpath_count(disabled_loc))
        return (element_count > 0)

    def _get_appliances_status_text(self, appl_type):
        web_status, email_status = '', ''
        num_of_entries = int(self.get_matching_xpath_count(
            APPLIANCES_STATUS_TEXT(EMAIL_APPL_TYPE, "'*'")))

        if num_of_entries == 2:
            email_status, web_status = map(lambda row: self.get_text(
                APPLIANCES_STATUS_TEXT(EMAIL_APPL_TYPE, row)),
                range(1, 3))
        elif num_of_entries == 1:
            if self._is_element_present(
                APPLIANCES_STATUS_TEXT(WEB_APPL_TYPE, "'*'")):
                web_status = self.get_text(
                    APPLIANCES_STATUS_TEXT(WEB_APPL_TYPE, 1))
            else:
                email_status = self.get_text(
                    APPLIANCES_STATUS_TEXT(EMAIL_APPL_TYPE, 1))

        return web_status if appl_type == WEB_APPL_TYPE else email_status

    def _check_appliances_status(self, appl_type, services=False,
        appliances=False):
        status_text = self._get_appliances_status_text(appl_type)
        services_disabled_msg = 'No centralized services are currently'\
            ' available'
        no_appliances_msg = 'No appliances have been added'

        if services and services_disabled_msg in status_text:
            raise guiexceptions.GuiFeatureDisabledError(services_disabled_msg)

        if appliances and no_appliances_msg in status_text:
            raise guiexceptions.ConfigError(no_appliances_msg)

    def _set_service_status(self, locator, value, name):
        if value is None:
            return

        if self._is_element_disabled(locator):
            raise guiexceptions.GuiFeatureDisabledError(
                '%s service is disabled' % (name,))

        if value:
            self.select_checkbox(locator)
        else:
            self.unselect_checkbox(locator)

    def _get_appliance_row_index(self, name, delete_cell, edit_cell):
        #num_of_rows = int(self.get_matching_xpath_count(delete_cell('*')))
        num_of_rows = int(self.get_matching_xpath_count(edit_cell('*')))

        for row in range(3, num_of_rows + 3):
            appl_name = self.get_text(edit_cell(row))
            if appl_name == name:
                return row
        else:
            raise guiexceptions.GuiValueError(
                '`%s` appliance was not found' % (name,))

    def _get_table_cells_locators(self, appl_type):
        if appl_type == EMAIL_APPL_TYPE:
            return (DELETE_EMAIL_APPL_TABLE_CELL, EDIT_EMAIL_APPL_TABLE_CELL)
        else:
            return (DELETE_WEB_APPL_TABLE_CELL, EDIT_WEB_APPL_TABLE_CELL)

    def _get_names(self, appl_type):
        _names = []

        if appl_type == WEB_APPL_TYPE:
            _TABLE_LOC = WEB_APPL_TABLE_PREFIX + "table[not(following-sibling::div[@class='group'])][1]"

        if appl_type == EMAIL_APPL_TYPE:
            _TABLE_LOC = EMAIL_APPL_TABLE_PREFIX + "table[following-sibling::div[@class='group']][1]"

        _TABLE_ROWS = _TABLE_LOC + "//tr"

        num_of_entries = int(self.get_matching_xpath_count(
            _TABLE_ROWS))
        self._debug(_TABLE_ROWS)
        self._debug(num_of_entries)
        for row in range(2, num_of_entries):
            _cell_value = self.get_text(_TABLE_ROWS + "[" + str(row+1) + "]/td[1]")
            _names.append(_cell_value.strip())
            self._debug(_TABLE_ROWS + "[" + str(row+1) + "]/td[1]")

        return _names

    def _get_appliance_data(self, appl_type, name):
        _data = {}

        if appl_type == WEB_APPL_TYPE:
            _TABLE_LOC = WEB_APPL_TABLE_PREFIX + "table[not(following-sibling::div[@class='group'])][1]"

        if appl_type == EMAIL_APPL_TYPE:
            _TABLE_LOC = EMAIL_APPL_TABLE_PREFIX + "table[following-sibling::div[@class='group']][1]"

        _APPLIANCE_ROW = _TABLE_LOC + "//tr/td[1]/a[normalize-space(text())='" + \
                         name + "']/parent::*/parent::*"

        num_of_entries = int(self.get_matching_xpath_count(
                _APPLIANCE_ROW))
        if num_of_entries == 0:
            raise guiexceptions.GuiValueError(
                '`%s` appliance was not found' % (name,))

        num_of_first_heads = int(self.get_matching_xpath_count(
                _TABLE_LOC + "//tr[1]/th"))
        num_of_cols = int(self.get_matching_xpath_count(
                _APPLIANCE_ROW + "[1]/td"))

        # get data of first column
        _head_loc = _TABLE_LOC + "//tr[1]/th[1]"
        _head_text = self.get_text(_head_loc)
        _data_loc = _APPLIANCE_ROW + "[1]/td[1]"
        _data_text = self.get_text(_data_loc)
        _data[_head_text] = _data_text

        # get data of second column
        _head_loc = _TABLE_LOC + "//tr[1]/th[2]"
        _head_text = self.get_text(_head_loc)
        _data_loc = _APPLIANCE_ROW + "[1]/td[2]"
        _data_text = self.get_text(_data_loc)
        _data[_head_text] = _data_text

        # get data of last data column
        _head_loc = _TABLE_LOC + "//tr[1]/th[" + str(num_of_first_heads-1) + "]"
        _head_text = self.get_text(_head_loc)
        _data_loc = _APPLIANCE_ROW + "[1]/td[" + str(num_of_cols-1) + "]"
        _data_text = self.get_text(_data_loc)
        _data[_head_text] = _data_text

        # get data of services data column
        for col in range(3, num_of_cols-1):
            _head_loc = _TABLE_LOC + "//tr[2]/th[" + str(col-2) + "]"
            _head_text = self.get_text(_head_loc)
            _data_loc = _APPLIANCE_ROW + "[1]/td[" + str(col) + "]"
            _check_loc = _data_loc + "/img[contains(@src, '/check.')]"
            num_of_checks = int(self.get_matching_xpath_count(
                    _check_loc))
            if num_of_checks > 0:
                _data_value = True
            else:

                _data_value = False
            _data[_head_text] = _data_value

        return _data

    def _wait_for_confirmation_text(self, text, timeout=900, interval=2):
        """Waits until confirmation text be present on page"""
        Wait(
            self._is_text_present,
            interval=interval,
            timeout=timeout
        ).wait(text)

    def security_appliances_add_email_appliance(self, name, address, isq=None,
        pvo=None, reporting=None, tracking=None, ssh_credentials=None, establish_timeout=60):
        """Add Email security appliance.

        Parameters:
        - `name`: name for the email security appliance.
        - `address`: IP address or hostname of the appliance.
        - `isq`: enable spam quarantine service. Boolean.
        - `reporting`: enable centralized reporting service. Boolean.
        - `tracking`: enable centralized message tracking service. Boolean.
        - `ssh_credentials`: credentials to establish an SSH connection to the
           appliance in 'username:password' format.
        - `establish_timeout`: timeout in seconds for establishing
           ssh connection to the appliance.

        Examples:
        | Security Appliances Add Email Appliance | myESA | c600-01.qa |
        | ... | ssh_credentials=admin:Cisco123$ |
        | Security Appliances Add Email Appliance | myESA | c600-01.qa |
        | ... | ${True} | ${False} | ${True} |

        Exceptions:
        - `GuiValueError`: in case of invalid `credentials` format.
        - `GuiFeatureDisabledError`: in case any of the selected centralized
           services or all of the centralized services are not available.
        """
        self._open_page()

        self._click_add_email_appliance_button()

        self._fill_esa_appliance_page(name, address, isq, pvo, reporting, tracking)

        self._establish_connection(ssh_credentials, establish_timeout)

        self._click_submit_button()

        ready_msg = ' added'
        try:
            self._wait_for_confirmation_text(ready_msg)
        except:
            time.sleep(20)
            if self._is_text_present(ready_msg):
                return
            else:
                raise TimeoutError, 'Appliance has not been added'

    def security_appliances_edit_email_appliance(self, name, newname=None,
        address=None, isq=None, pvo=None, reporting=None, tracking=None,
        ssh_credentials=None, establish_timeout=60):
        """Edit Email security appliance.

        Parameters:
        - `name`: name of the email security appliance to edit.
        - `newname`: new name for the email security appliance.
        - `address`: IP address or hostname of the appliance.
        - `isq`: enable spam quarantine service. Boolean.
        - `reporting`: enable centralized reporting service. Boolean.
        - `tracking`: enable centralized message tracking service. Boolean.
        - `ssh_credentials`: credentials to establish an SSH connection to the
           appliance in 'username:password' format.
        - `establish_timeout`: timeout in seconds for establishing
           ssh connection to the appliance.

        Examples:
        | Security Appliances Edit Email Appliance | myESA | newname |
        | ... | esabox.qa | ${True} | ${True} | ${False} |
        | Security Appliances Edit Email Applaince | myESA |
        | ... | reporting=${False} | tracking=${True} |

        Exceptions:
        - `GuiValueError`: in case of invalid `credentials` format or email
           appliance is not present in the table.
        - `ConfigError`: in case no email appliances have been added.
        - `GuiFeatureDisabledError`: in case any of the selected centralized
           services or all of the centralized services are not available.
        """
        self._open_page()

        self._click_edit_appliance_link(name, EMAIL_APPL_TYPE)

        self._fill_esa_appliance_page(newname, address, isq, pvo, reporting,
            tracking)

        self._establish_connection(ssh_credentials, establish_timeout)

        self._click_submit_button(wait=False)

        ready_msg = 'Appliance %s has been updated' % (newname or name)
        self._wait_for_confirmation_text(ready_msg)

    def security_appliances_delete_email_appliance(self, name):
        """Delete Email security appliance

        Parameters:
        - `name`: name of the email security appliance to delete.

        Examples:
        | Security Appliances Delete Email Appliance | myESA |

        Exceptions:
        - `GuiValueError`: in case email appliance is not present in the table.
        - `ConfigError`: in case no email appliances have been added.
        - `GuiFeautureDisabledError`: in case all of the centralized services
           are not available.
        """
        self._open_page()

        self._click_delete_appliance_link(name, EMAIL_APPL_TYPE)

    def security_appliances_get_email_appliance_names(self):
        """Get names of present Email security appliances.

        Return:
        List with names of present Email appliances.

        Examples:
        | ${names}= | Security Appliances Get Email Appliance Names |
        | Log Many | ${names} |
        """
        self._open_page()

        return self._get_names(EMAIL_APPL_TYPE)

    def security_appliances_get_email_appliance_data(self, name):
        """Get status data of specified Email security appliance.

        Return:
        Dictionary with data of indicated Email appliance.
        (Boolean 'True' is returned for checkboxes.)

        Examples:
        | ${appliance_data}= | Security Appliances Get Email Appliance Data | ESA1 |
        | Log | ${appliance_data['IP Address or Hostname']} |
        | Log | ${appliance_data['Spam Quarantine']} |
        | Log | ${appliance_data['Reporting']} |
        | Log | ${appliance_data['Tracking']} |
        | Log | ${appliance_data['Connection Established?']} |

        Exceptions:
        - `GuiValueError`: in case email appliance is not present in the table.
         """
        self._open_page()

        return self._get_appliance_data(EMAIL_APPL_TYPE, name)

    def security_appliances_add_web_appliance(self, name, address, iccm=None,
        reporting=None, upgrade=None, ssh_credentials=None, config_master=None, establish_timeout=360):
        """Add Web security appliance.

        Parameters:
        - `name`: name for the web security appliance.
        - `address`: IP address or hostname of the appliance.
        - `iccm`: enable centralized configuration manager. Boolean.
        - `reporting`: enable centralized web reporting. Boolean.
        - `ssh_credentials`: credentials to establish an SSH connection to the
           appliance in 'username:password' format.
        - `establish_timeout`: timeout in seconds for establishing
           ssh connection to the appliance.
        - `config_master`: name of the configuration master to assign appliance
           to. ${False} to not assign appliance to configuration master. It is
           suggested to use sma_config_masters constants from sma/constants.py
           variables file.

        Examples:
        | Security Appliances Add Web Applaince | myWSA | wsabox.qa | ${True} |
        | ... | ${False} | admin:Cisco123$ | config_master=${sma_config_masters.CM77} |
        | Security Appliances Add Web Appliance | myWsa | wsabox.qa |
        | ... | iccm=${False} |

        Exceptions:
        - `GuiValueError`: in case of invalid `credentials` format or wrong
           configuration master name.
        - `ConfigError`: when trying to assign appliance to configuration
           master, but connection has not been established yet.
        - `GuiFeatureDisabledError`: in case any of the selected centralized
           services or all of the centralized services are not available.
        """
        self._open_page()

        self._click_add_web_appliance_button()

        self._fill_web_appliance_page(name, address, iccm, reporting, upgrade)

        self._establish_connection(ssh_credentials, establish_timeout)

        self._select_config_master(config_master)

        self._click_submit_button(wait=False, check_result=False)

        ready_msg = ' added'
        self._wait_for_confirmation_text(ready_msg)

    def security_appliances_edit_web_appliance(self, name, newname=None,
        address=None, reporting=None, iccm=None, upgrade=None, ssh_credentials=None,
        config_master=None, config_master_edit=False, establish_timeout=60):
        """Edit Web security appliance.

        Parameters:
        - `name`: name of the web security appliance to edit.
        - `newname`: new name for the web security appliance.
        - `address`: IP address or hostname of the appliance.
        - `iccm`: enable centralized configuration manager. Boolean.
        - `reporting`: enable centralized web repoting. Boolean.
        - `ssh_credentials`: credentials to establish an SSH connection to the
           appliance in 'username:password' format.
        - `establish_timeout`: timeout in seconds for establishing
           ssh connection to the appliance.
        - `config_master`: name of the configuration master to assign appliance
           to. ${False} to not assign appliance to configuration master. It is
           suggested to use sma_config_masters constants from sma/constants.py
           variables file.

        Examples:
        | Security Appliances Edit Web Appliance | myWSA |
        | ... | config_master=${False} |
        | Security Appliances Edit Web Appliance | myWsa | oldWSA |
        | ... | ${False} | ${True} | config_master=${sma_config_masters.CM77} |

        Exceptions:
        - `GuiValueError`: in case of invalid `credentials` format, web
           appliance is not present in the table or wrong configuration master
           name.
        - `ConfigError`: in case no web appliances have been added or when
           trying to assign appliance to configuration master, but connection
           has not been established yet.
        - `GuiFeatureDisabledError`: in case any of the selected centralized
           services or all of the centralized services are not available.
        """
        if config_master_edit==False:
            self._open_page()

        self._click_edit_appliance_link(name, WEB_APPL_TYPE)

        self._fill_web_appliance_page(newname, address, iccm, reporting, upgrade)

        self._establish_connection(ssh_credentials, establish_timeout)

        self._select_config_master(config_master)

        self._click_submit_button(wait=False)

        ready_msg = 'Appliance %s has been updated' % (newname or name)
        self._wait_for_confirmation_text(ready_msg)

    def security_appliances_delete_web_appliance(self, name):
        """Delete Web security appliance.

        Parameters:
        - `name`: name of the web appliance to delete.

        Examples:
        | Security Appliances Delete Web Appliance | myWSA |

        Exceptions:
        - `GuiValueError`: in case web appliance is not present in the table.
        - `ConfigError`: in case no web appliances have been added.
        - `GuiFeautureDisabledError`: in case all of the centralized services
           are not available.
        """
        self._open_page()

        self._click_delete_appliance_link(name, WEB_APPL_TYPE)

    def security_appliances_get_web_appliance_names(self):
        """Get names of present Web security appliances.

        Return:
        List with names of present Web appliances.

        Examples:
        | ${names}= | Security Appliances Get Web Appliance Names |
        | Log Many | ${names} |
        """
        self._open_page()

        return self._get_names(WEB_APPL_TYPE)

    def security_appliances_get_web_appliance_data(self, name):
        """Get status data of specified Web security appliance.

        Return:
        Dictionary with data of indicated Web appliance.
        (Boolean 'True' is returned for checkboxes.)

        Examples:
        | ${appliance_data}= | Security Appliances Get Web Appliance Data | WSA1 |
        | Log | ${appliance_data['IP Address or Hostname']} |
        | Log | ${appliance_data['Configuration Manager']} |
        | Log | ${appliance_data['Reporting']} |
        | Log | ${appliance_data['Connection Established?']} |

        Exceptions:
        - `GuiValueError`: in case email appliance is not present in the table.
         """
        self._open_page()

        return self._get_appliance_data(WEB_APPL_TYPE, name)
