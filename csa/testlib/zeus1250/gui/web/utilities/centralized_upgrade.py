#!/usr/bin/env python
# $Id:
# $DateTime:
# $Author:

import re
import time
from common.util.sarftime import CountDownTimer
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import (GuiCommon, Wait)
import common.Variables
from common.cli.clicommon import CliKeywordBase


UPGRADE_APPLIANCE = "xpath=//input[@id='upgradeButton']"
SELECT_WEB_APPLIANCE = lambda row: "//input[@value='%s']" %(row)
SELECT_ALL_WEB_APPLIANCE = "//input[@id='select_all']"
APPLIANCES_NAME_CELL = lambda row: "//div[@id='datatable_container']/div[3]/table//tbody[2]/tr[%s]/td[2]/div/a" %(row)
SELECT_APPLAINCE = lambda row: "//div[@id='datatable_container']/div[3]/table//tbody[2]/tr[%s]/td[1]/div/input[@name='wsa[]']" %(row)
DOWNLOAD_INSTALL = "xpath=//input[@id='downloadinstall']"
CLICK_NEXT = "xpath=//input[@id='fetch_upgrade_button']"
SELECT_VERSION = lambda row: "//div[@id='datatable_container']/div[3]/table//tbody[2]/tr[%s]/td[1]/div/input[@id='available']" %(row)
upgrade_locator = lambda row: "//div[@id='datatable_container']/div[3]/table//tbody[2]/tr[%s]/td[2]/div" %(row)
SUBMIT_BUTTON = "xpath=//input[@class='submit']"
DOWNLOAD = "xpath=//input[@id='begin_upgrade']"
MASK_PASSWORD = 'mask_passwd'
EMAIL_ADDRESS = "xpath=//input[@id='addr_list']"
APPLIANCE_NAME = lambda row: "//div[@id='upgrade']/table/tbody/tr[%s]/td/a" %(row)
UPGRADE_STATUS = lambda row: "//div[@id='upgrade']/table/tbody/tr[%s]/td[5]/div/div[2]" %(row)
FETCH_UPGRADE_VERIFY = "xpath=//*[contains(text(),'Completed Fetching Available Upgrades')]"
DOWNLOAD_WIZARD = "xpath=//input[@id='download']"
CANCEL_BUTTON = "xpath=//input[@value='Cancel']"
INSTALL_CANCEL = "xpath=//a[ contains( @onclick, 'doUpgradeCancel')]"
'xpath=//a[ contains( @onclick, "select_all_checkboxes")]'
CONFIRM_CANCEL = "xpath=//button[contains(text(),'Confirm Cancel')]"
CONTINUE_WIZARD = "xpath=//button[contains(text(),'Continue Wizard')]"
PAGE = lambda current,tab: "//*[@class='%s' and contains(text(), '%s')]" %(current,tab)
INFO1 = "xpath=//label[@class='label' and contains(text(),'Following appliances looks good to be upgraded.')]"
INFO2 = "xpath=//*[contains(text(),'After upgrade, each appliance will be rebooted.')]"
INFO3 = "xpath=//span[text()[contains(.,'You can view the status')]]"
INFO4 = "xpath=//label[@class='label' and contains(text(),'Following appliances seems to have warning.')]"
INFO5 = "xpath=//*[contains(text(),'Download Complete')]"
WSAWARN = "xpath=//input[@name='wsawarn[]']"
UPGRADE_STATUS_PAGE = "xpath=//*[contains(text(), 'Upgrade Status')]"
APPLIANCE_UPGRADE_STATUS = lambda app: "//*[@id='status_%s' and contains(text(),'in progress')]" %(app)
DOWNLOAD_COMPLETE = "xpath=//div[contains(text(), 'Download Complete')]"
WSA_APPLIANCE= lambda app : "//input[@value='%s']" %(app)
INSTALL_WIZARD = "xpath=//input[@id='downloadinstall' and @value='Install Wizard']"
UPGRADE_TO_VERSION = "xpath=//div[@id='upgrade']/table/tbody/tr[2]/td[4]"
DELETE_ICON = lambda version : "//td[5][contains(text(), '%s')]/span/img[contains(@onclick,'doConfirmDelete')]" %(version)
CONFIRM_DELETE= "xpath=//button[contains(text(),'Delete')]"
DOWNLOADED_VERSION = lambda version : "//td[5][contains(text(), '%s')]" %(version)
CURRENT_VERSION = "xpath=//dl/dd/div[1]/div[2]/table/tbody[2]/tr/td[4]/div[1]"
EMAIL_FILE_TO = "xpath=//*[@id='email_operation_id']"
EMAIL_TEXTBOX= "xpath=//*[@id='mailto_id']"
EMAIL_SUBMIT_BUTTON = "xpath=//input[@class='button']"
SMA_HOME = "xpath=//input[@class='button']"
CLOSE_CONTAINER = "xpath=//*[@class='container-close']"
INSTALL_CANCEL_MSG= "xpath=//div[@id='confirmation_dialog']/div[2][contains(text(), 'install cancelled']"

class CentralizedUpgrade(GuiCommon):

    """Keywords for Web -> Utilities -> Centralized Upgrade"""
    def get_keyword_names(self):
        return ['centralized_upgrade_download_and_install',
                'centralized_upgrade_status',
                'choose_fetch_upgrade_option',
                'confirm_cancel_wizard',
                'continue_from_cancel_wizard',
                'navigate_to_tab',
                'delete_available_upgrade',
                'centralized_upgrade_download',
                'email_configuration_file',
                'cancel_install_upgrade',
                'multiple_centralized_upgrade_download_and_install',
                'multiple_centralized_upgrade_download_only',
                'version_of_duts'
                ]

    def version_of_duts(self):
        '''
        Displays the version of duts used.
        :return: returns the base version i.e. version of first DUT, since atleast one dut needs to be added
        '''

        var = common.Variables.get_variables()
        for key in var.keys():
            if re.match("\${WSA[\d]*?_BUILD}", key):
                print(' '.join(str(key)[2:-1].split('_', 1)) + ':' + str(var.get(key)))
            elif re.match("\${WSA[\d]*?}",key):
                print(str(key)[2:-1] + ' HOSTNAME' + ':' + str(var.get(key)))

        base_build=str(var.get('${WSA_BUILD}'))
        return ('.'.join(base_build.rsplit('-', 4)[1:][:3])+'-'+base_build.rsplit('-', 4)[1:][3])

    def _open_page(self):
        try:
            self._navigate_to('Web', 'Utilities', 'Centralized Upgrade')
        except Exception as error:
            # Handle only the case when Centralized Upgrade are not
            # initialized, 'Publish to Web Appliances' menu item is not present
            # then.
            if re.search('Centralized Upgrade.*?not found',
                error.message):
                raise guiexceptions.GuiFeatureDisabledError(
                    'Centralized Upgrade are not initialized')
            # dont care about the rest, let the caller handle this
            raise

    def _get_available_appliances_names(self):
        num_of_rows = int(
            self.get_matching_xpath_count(APPLIANCES_NAME_CELL('*')))
        self._info("%d" % num_of_rows)
        return [self.get_text(APPLIANCES_NAME_CELL(row))\
                for row in range(1, num_of_rows + 1)]

    def select_applaince(self,appliances):
        available_appliances = self._get_available_appliances_names()
        self._info(available_appliances)
        for appliance in self._convert_to_tuple(appliances):
            if appliance in available_appliances:
                row = available_appliances.index(appliance) + 1
                self.select_checkbox(SELECT_APPLAINCE(row))
            else:
                raise guiexceptions.GuiValueError(
                    '%s appliance is not in Appliances table' %\
                    (appliance,))

    def select_multiple_appliances(self, **kwargs):
        '''
        Select multiples appliances to upgrade.
        :param kwargs: accepts appliances to be upgraded as parameter and stores in a dictionary.
            Select Multiple Appliances  ${arg1}=${WSA}  ${arg2}=${WSA2}
        :return:
        '''
        args = tuple(kwargs.values())
        if 'all' in args:
            self.select_checkbox(SELECT_ALL_WEB_APPLIANCE)
        else:
            for appliance in range(0,len(args)):
               self._wait_until_element_is_present(SELECT_WEB_APPLIANCE(args[appliance]), timeout=100)
               self.select_checkbox(SELECT_WEB_APPLIANCE(args[appliance]))

    def multiple_centralized_upgrade_download_and_install(self, version=None, mask_password=True,email='', **kwargs):
        '''
        End-to-end flow for upgrading multiples security appliances using downloadinstall upgrade option
        '''
        self._open_page()
        self.click_button(UPGRADE_APPLIANCE, 'dont wait')
        self.select_multiple_appliances(**kwargs)
        self.click_button(DOWNLOAD_INSTALL, 'dont wait')
        # time for upgrade to complete
        time.sleep(60)
        self.click_button(CLICK_NEXT, 'dont wait')
        time.sleep(10)
        self._select_upgrade_file(version)
        self._wait_until_element_is_present(SUBMIT_BUTTON)
        self.click_button(SUBMIT_BUTTON, 'dont wait')
        self._enable_passwords_masking(mask_password)
        self.input_text(EMAIL_ADDRESS, email)
        self.click_button(SUBMIT_BUTTON, 'dont wait')
        time.sleep(10)
        self.click_button(SUBMIT_BUTTON, 'dont wait')
        time.sleep(60)
        try:
            self._wait_until_element_is_present(INFO1, 30)
            self._wait_until_element_is_present(INFO2)
            self._wait_until_element_is_present(INFO3)
        except:
            self._wait_until_element_is_present(INFO4, 30)
            #self.click_element(WSAWARN)
            self.select_multiple_appliances(**kwargs)
        self.click_button(DOWNLOAD, 'dont wait')
        self._wait_until_element_is_present(UPGRADE_STATUS_PAGE, timeout=20)

    def multiple_centralized_upgrade_download_only(self, version=None, **kwargs):
        '''
        End-to-end flow for upgrading multiples security appliances using download upgrade option
        '''

        warning_msg = ""
        self._open_page()
        self.click_button(UPGRADE_APPLIANCE, 'dont wait')
        time.sleep(5)
        self.select_multiple_appliances(**kwargs)
        self.click_button(DOWNLOAD_WIZARD, 'dont wait')
        # time for upgrade to complete
        time.sleep(60)
        self.click_button(CLICK_NEXT, 'dont wait')
        time.sleep(10)
        self._select_upgrade_file(version)
        self._wait_until_element_is_present(SUBMIT_BUTTON, 5)
        if self._is_element_present(SUBMIT_BUTTON):
            self.click_button(SUBMIT_BUTTON, 'dont wait')
        self._wait_until_element_is_present(SUBMIT_BUTTON, 5)
        if self._is_element_present(SUBMIT_BUTTON):
            self.click_button(SUBMIT_BUTTON, 'dont wait')
        time.sleep(20)
        if self._is_element_present(SUBMIT_BUTTON):
            self.click_button(SUBMIT_BUTTON, 'dont wait')
        try:
           self._wait_until_element_is_present(INFO1, 50)
        except:
           self._wait_until_element_is_present(INFO4, 50)
           #self.click_element(WSAWARN)
           self.select_multiple_appliances(**kwargs)
           warning_msg = "WSA shows warning"
        self.click_button(DOWNLOAD, 'dont wait')
        self._wait_until_element_is_present(UPGRADE_STATUS_PAGE, timeout=20)
        time.sleep(400)
        self._wait_until_element_is_present(INFO5, 2500)
        self.click_button(UPGRADE_APPLIANCE, 'dont wait')
        self.select_multiple_appliances(**kwargs)
        self._wait_until_element_is_present(INSTALL_WIZARD, 5)
        self.click_button(INSTALL_WIZARD, 'dont wait')
        self._wait_until_element_is_present(SUBMIT_BUTTON, 5)
        self.click_button(SUBMIT_BUTTON, 'dont wait')
        time.sleep(60)
        self._wait_until_element_is_present(SUBMIT_BUTTON, 5)
        self.click_button(SUBMIT_BUTTON, 'dont wait')
        try:
           self._wait_until_element_is_present(INFO1, 50)
           self._wait_until_element_is_present(INFO2)
           self._wait_until_element_is_present(INFO3)
        except:
           self._wait_until_element_is_present(INFO4, 50)
           #self.click_element(WSAWARN)
           self.select_multiple_appliances(**kwargs)
           warning_msg = "WSA shows warning"
        self.click_button(DOWNLOAD, 'dont wait')
        return warning_msg

    def _get_available_upgrades(self):
        num_of_rows = int(
            self.get_matching_xpath_count(upgrade_locator('*')))
        upgrade_version = []
        for row in range(1, num_of_rows + 1):
            upgrade_version.append(self.get_text(upgrade_locator(row)))
        return upgrade_version

    def _select_upgrade_file(self, version=None):
        """Select upgrade file from the upgrade list"""

        format_of_version = \
            re.match("\d{1,2}\.\d{1}\.\d{1}\-\d{1,3}", version)
        if not format_of_version:
            raise ValueError, 'Please specify version in X.X.X-XXX format'
        upgrade_list = self._get_available_upgrades()
        id_build = version.split('-')
        upgrade_str = id_build[0] + ' build ' +  id_build[1]
        for upgrade in upgrade_list:
            if re.match(upgrade_str,upgrade):
                self._info('Selected upgrade %s' % upgrade)
                row= upgrade_list.index(upgrade) + 1
                self.select_checkbox(SELECT_VERSION(row))
                self._info('Selected upgrade %s' % upgrade)
                self.click_button(SUBMIT_BUTTON, 'dont wait')
                return
        else:
            raise guiexceptions.GuiControlNotFoundError\
             ('"%s" upgrade version' % (version,), 'Centralized Upgrade')

    def _enable_passwords_masking(self, enable):
        if enable:
            self.select_checkbox(MASK_PASSWORD)
        else:
            self.unselect_checkbox(MASK_PASSWORD)

    def centralized_upgrade_download_and_install(self,applainces, appliances_ip, version=None,mask_password=True,email=''):
        self._open_page()
        self.click_button(UPGRADE_APPLIANCE, 'dont wait')
        self.select_applaince(applainces)
        self.click_button(DOWNLOAD_INSTALL, 'dont wait')
        self._wait_until_element_is_present(APPLIANCE_UPGRADE_STATUS(appliances_ip), timeout=15)
        # time for upgrade to complete
        time.sleep(60)
        self.click_button(CLICK_NEXT, 'dont wait')
        time.sleep(10)
        self._select_upgrade_file(version)
        self.click_button(SUBMIT_BUTTON, 'dont wait')
        self._enable_passwords_masking(mask_password)
        self._wait_until_element_is_present(EMAIL_ADDRESS, timeout=20)
        self.input_text(EMAIL_ADDRESS, email)
        self.click_button(SUBMIT_BUTTON, 'dont wait')
        self._wait_until_element_is_present(SUBMIT_BUTTON, timeout=30)
        self.click_button(SUBMIT_BUTTON, 'dont wait')
        time.sleep(60)
        self._wait_until_element_is_present(INFO1, 30)
        self._wait_until_element_is_present(INFO2)
        self._wait_until_element_is_present(INFO3)
        self.click_button(DOWNLOAD, 'dont wait')
        self._wait_until_element_is_present(UPGRADE_STATUS_PAGE, timeout=20)

    def centralized_upgrade_download(self,applainces,version=None,mask_password=True,email=''):
        '''


        :param applainces: security appliance to be selected
        :param version: version to be upgraded to
        :param mask_password: Takes boolean value True by default
        :param email: Empty string by default
        :return:
        '''
        self.choose_fetch_upgrade_option(applainces, upgrade_option = 'download', version = version)
        self.navigate_to_tab('download', tab='Review', version=version, mask_password=mask_password, email=email)
        self.click_button(DOWNLOAD, 'dont wait')
        self._wait_until_element_is_present(UPGRADE_STATUS_PAGE, timeout=20)
        self._wait_until_element_is_present(DOWNLOAD_COMPLETE, timeout=120)
        self.click_button(UPGRADE_APPLIANCE, 'dont wait')
        self.select_applaince(applainces)


    def choose_fetch_upgrade_option(self,applainces='',upgrade_option=None, version = None):
        '''
        Verifies whether centralized upgrades are fetched successfully or not
        :param applainces: the appliance to be selected for upgrade
        :param upgrade_option: Type of download option to be selected i.e. downloadinstall or download
        :return:
        Example : Choose Fetch Upgrade Option  ${WSA}  downloadinstall
        '''


        self._open_page()
        self.click_button(UPGRADE_APPLIANCE, 'dont wait')
        # Ensures if upgrade image is already downloaded
        if self._is_element_present(DOWNLOADED_VERSION(version)):
            pass
        else:
            self.select_applaince(applainces)
            if upgrade_option == 'download':
                self.click_button(DOWNLOAD_WIZARD, 'dont wait')
            elif upgrade_option == 'downloadinstall':
                self.click_button(DOWNLOAD_INSTALL, 'dont wait')
            # self._wait_until_element_is_present(FETCH_UPGRADE_VERIFY, timeout=20)
            return upgrade_option

    def confirm_cancel_wizard(self):
        '''
        Click on 'Cancel' button, then click on 'Confirm Cancel' from the pop-up window
        :return:
        Example:  Confirm Cancel Wizard
        '''

        self.click_button(CANCEL_BUTTON, 'dont wait')
        self.click_button(CONFIRM_CANCEL)

    def cancel_install_upgrade(self, appliance='None'):
        time.sleep(30)
        try:
            self._wait_until_element_is_present(INFO1, 30)
        except:
            self._wait_until_element_is_present(INFO4, 30)
            warning_msg = "WSA shows warning"
            self.click_element(WSAWARN)
        self.click_button(DOWNLOAD, 'dont wait')
        self.click_link(INSTALL_CANCEL, 'dont wait')
        self.click_button(CONFIRM_CANCEL)
        self.click_link(CLOSE_CONTAINER, 'dont wait')

    def continue_from_cancel_wizard(self):
        '''
        Click on 'Cancel' button, then click on 'Continue Wizard' from the pop-up window
        :param applainces: appliance to be upgraded
        :return:
        Example: Continue From Cancel Wizard
        '''

        url = self.get_location()
        self.click_button(CANCEL_BUTTON, 'dont wait')
        self.click_button(CONTINUE_WIZARD)
        if url != self.get_location():
            raise ValueError, 'Page url do not match'

    def delete_available_upgrade(self, appliances=None, version= None):
        '''
        :param appliances: select the checkbox for the specific appliance
        :param version: checks the image to be deleted
        :return:
        '''

        self._open_page()
        self.click_button(UPGRADE_APPLIANCE, 'dont wait')
        self.select_checkbox(WSA_APPLIANCE(appliances))
        self.click_element(DELETE_ICON(version))
        self.click_button(CONFIRM_DELETE)

    def navigate_to_tab(self, upgrade_option, applainces=None, tab=None, version=None, mask_password=True, email=''):
        '''
        :param upgrade_option: specifies the upgrade version download or downloadinstall
        :param applainces : appliance to be upgraded
        :param tab:The tab to be navigated to in Centralized Upgrade as per GUI like 'Available Upgrades','Summary' etc.
               Example: Choose Fetch Upgrade Option  ${WSA}  downloadinstall
                         Navigate To Tab  Summary  11.5.0-614
        :param version: The version to be selected on 'Available Upgrades' tab
               Example: Navigate To Tab  Upgrade Selection  11.5.0-614
        :param mask_password: Takes boolean value. True by default
        :param email: Email id to be entered in 'Upgrade Preparation' tab. Empty String by default
        '''
        global warning_msg
        warning_msg = ""
        def available_upgrade():

            self.click_button(CLICK_NEXT, 'dont wait')

        def upgrade_selection():
            available_upgrade()
            self._wait_until_element_is_present(PAGE('current','Available Upgrades'), timeout=50)
            self._select_upgrade_file(version)

        def upgrade_preparation():
            global warning_msg
            if upgrade_option == 'download':
                # if downloaded image is already available proceed with install wizard button else start all over again from centralized upgrade page
                if self._is_element_present(DOWNLOADED_VERSION(version)):
                    self.select_checkbox(WSA_APPLIANCE(applainces))
                    self.click_button(INSTALL_WIZARD, 'dont wait')
                else:
                    review()
                    self._wait_until_element_is_present(PAGE('last current', 'Review'))
                    try:
                        self._wait_until_element_is_present(INFO1, 30)
                        warning_msg = ""
                    except:
                        self._wait_until_element_is_present(INFO4, 30)
                        warning_msg = "WSA shows warning"
                        self.click_element(WSAWARN)
                    self.click_button(DOWNLOAD, 'dont wait')
                    self._wait_until_element_is_present(UPGRADE_STATUS_PAGE, timeout=60)
                    status = self.get_text(UPGRADE_TO_VERSION)
                    if status != version:
                        raise ValueError, 'Upgrade version mismatch'
                    else:
                        self._wait_until_element_is_present(DOWNLOAD_COMPLETE, timeout=2500)
                        self.click_button(UPGRADE_APPLIANCE, 'dont wait')
                        self.select_checkbox(WSA_APPLIANCE(applainces))
                        self.click_button(INSTALL_WIZARD, 'dont wait')
            else:
                upgrade_selection()
                time.sleep(5)
                if self._is_element_present(SUBMIT_BUTTON):
                    self.click_button(SUBMIT_BUTTON, 'dont wait')

        def summary():
            if upgrade_option == 'downloadinstall':
                upgrade_preparation()
                self._enable_passwords_masking(mask_password)
                self.input_text(EMAIL_ADDRESS, email)
            elif upgrade_option == 'download':
                upgrade_selection()
            time.sleep(20)
            self.click_button(SUBMIT_BUTTON, 'dont wait')

        def review():
            summary()
            time.sleep(30)
            self.click_button(SUBMIT_BUTTON, 'dont wait')

        if tab == 'Available Upgrades':
            available_upgrade()
            self._wait_until_element_is_present(PAGE('current',tab), timeout=20)

        elif tab == 'Upgrade Selection':
            upgrade_selection()
            self._wait_until_element_is_present(PAGE('current',tab))

        elif tab == 'Upgrade Preparation':
            upgrade_preparation()
            if upgrade_option == 'downloadinstall':
                self._wait_until_element_is_present(PAGE('current',tab))
            else:
                self._wait_until_element_is_present(PAGE('first current', 'Upgrade Preparation'), timeout=20)

        elif tab == 'Summary':
            summary()
            self._wait_until_element_is_present(PAGE('current',tab))

        elif tab == 'Review':
            review()
            self._wait_until_element_is_present(PAGE('last current',tab))
            time.sleep(20)

        # Review page under Install Wizard
        elif tab == 'InstallWizardReview':
            upgrade_preparation()
            self.click_button(SUBMIT_BUTTON, 'dont wait')
            # self._validate_presence(SUBMIT_BUTTON)
            Wait(until=self._is_element_present(SUBMIT_BUTTON), timeout=30)
            self.click_button(SUBMIT_BUTTON, 'dont wait')
            # self._wait_to_click_button(SUBMIT_BUTTON, 'Next')
            self._wait_until_element_is_present(PAGE('last current', 'Review'), timeout=20)
            try:
                self._wait_until_element_is_present(INFO1, 30)
                warning_msg = ""
            except:
                self._wait_until_element_is_present(INFO4, 30)
                warning_msg = "WSA shows warning"
        return (tab, warning_msg)

    def email_configuration_file(self, email=''):
        self._navigate_to('Management Appliance', 'System Administration', 'Configuration File')
        self._click_radio_button(EMAIL_FILE_TO)
        self.input_text(EMAIL_TEXTBOX,email)
        self.click_button(EMAIL_SUBMIT_BUTTON, 'dont wait')
        return email

    def centralized_upgrade_status(self,appliance):
        num_of_rows = int(
            self.get_matching_xpath_count(APPLIANCE_NAME('*')))
        appliance_list=[]
        for row in range(2, num_of_rows + 1):
            appliance_list.append(self.get_text(APPLIANCE_NAME(row)))
        self._info("name: %s" %appliance_list)
        for appliance_name in self._convert_to_tuple(appliance):
            if appliance_name in appliance_list:
                row = appliance_list.index(appliance_name) + 2
                self._info("%s" % row)
                status = self.get_text(UPGRADE_STATUS(row))
                self._info("status: %s" % status)
                if status == 'Upgrade Complete':
                    self._info("Upgrade Completed Successfully")
                else:
                    raise guiexceptions.GuiValueError(
                        'Upgrade Not Completed')
            else:
                raise guiexceptions.GuiValueError(
                    '%s appliance is not in Appliances table' %\
                    (appliance,))
        return status

