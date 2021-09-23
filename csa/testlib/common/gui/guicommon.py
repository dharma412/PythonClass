#!/usr/bin/env python
# -*- coding: utf-8 -*-

# $Id: //prod/main/sarf_centos/testlib/common/gui/guicommon.py#6 $
# $DateTime: 2019/09/17 02:02:56 $

import sys
import os
import time
import re
import codecs

# rf import
from selenium_abstraction import WrappedSeleniumLibrary
# from selenium_abstraction import RunOnFailure
from robot.libraries.BuiltIn import BuiltIn

# sarf import
import common.gui.guiexceptions as guiexceptions
import common.Variables
from common.util.sarftime import CountDownTimer
from common.util.firefoxprofilegen import FirefoxProfile
from common.logging import Logger
from common.arguments import ArgumentParser
from common.util.unset_https import UnsetHttps
from common.util.misc import Misc
from common.util.systools import SysTools
from wait import Wait


class GuiCommon(ArgumentParser):
    """Common GUI actions.
    """
    #  class level dictionary gives to possibility to have single instance of SeleniumLibrary per dut
    __shared_state = {}

    def __init__(self, dut=None, dut_version=None, dut_browser='firefox', timeout=60, server_host='localhost', \
                 run_on_failure='Handle GUI Failure', alias=''):

        self.dut = dut
        self.dut_version = dut_version
        if alias:
            session_name = "%s-%s-%s" % (self.dut, dut_browser, alias)
        else:
            session_name = "%s-%s" % (self.dut, dut_browser)
        if not GuiCommon.__shared_state.has_key(session_name):
            # initialize new selenium server
            self._seleniumlib = ExtendedSeleniumLibrary(dut, dut_version, dut_browser, timeout, server_host, \
                                                        run_on_failure, session_name)

            GuiCommon.__shared_state[session_name] = {'seleniumlib': self._seleniumlib, 'browser': dut_browser}
        else:
            self._seleniumlib = GuiCommon.__shared_state[session_name]['seleniumlib']

    # RF Hybrid API for Test Libraries , return all keywords from SeleniumLibrary + its own ones
    def get_keyword_names(self):
        exclude_list = ['ROBOT_LIBRARY_SCOPE', 'ROBOT_LIBRARY_VERSION', 'ROBOT_LIBRARY_LISTENER', 'log', 'dut',
                        'dut_version', 'timeout', 'implicit_wait', 'keywords', 'attributes', 'driver', 'speed',
                        'run_keyword','dut_browser','run_on_failure_keyword','screenshot_root_directory','Get WebElement',
                        'allowed_attempts', 'Get WebElements', 'selenium_server_host', 'session_name']

        self.common_keywords = [keyword for keyword in dir(self._seleniumlib) if keyword[0] != '_' and \
                                keyword not in exclude_list]

        print "common_keywords", self.common_keywords
        return self.common_keywords

    # redirects request for unknown attribures to the SeleniumLibrary
    def __getattr__(self, name):
        if name == '_seleniumlib':
            raise RuntimeError('SeleniumLibrary has not been initialized')
        return getattr(self._seleniumlib, name)


class ExtendedSeleniumLibrary(WrappedSeleniumLibrary):
    """ Extended Selenium Library """

    def __init__(self, dut=None, dut_version=None, dut_browser='firefox',
                 timeout=60.0, server_host='localhost', run_on_failure='Handle GUI Failure', session_name=''):

        super(self.__class__, self).__init__(timeout, server_host, run_on_failure)

        # dut variables
        self.dut = dut
        self.dut_version = dut_version
        self.dut_browser = dut_browser
        self.selenium_server_host = server_host
        self._server_host = server_host
        self.session_name = session_name
        # firefox settings
        self._ff_profile = None
        self.allowed_attempts = 3
        print "self.session_name : ExtendedSeleniumLibrary", self.session_name

    def _retry_dut_login(self, dut_url, dut_browser, delay, autodownload, download_folder):
        dut_browser = dut_browser or self.dut_browser
        for open_browser_attempt in range(self.allowed_attempts):
            try:
                self._open_browser(dut_url, browser=dut_browser, alias=self.session_name, autodownload=autodownload, download_folder=download_folder)
            except Exception as e:
                if open_browser_attempt < self.allowed_attempts - 1:
                    self._warn("Get exception from open_browser: %s. Will attempt open_browser again" % str(e))
                else:
                    self._warn("Get exception from open_browser: %s.Too many failed attempt for open_browser" % str(e))
                    raise
                try:
                    self.close_browser()
                except Exception as e:
                    self._warn("Get exception from selenium server: %s during close_browser" % str(e))
            else:
                break
        self.set_selenium_speed(delay)
        self.maximize_browser_window()

    def _log_into_dut_int(self, user, password, passcode=None, **kwargs):
        """Performs logging into DUT using specified user and password
           credential.

        Parameters:
           - `user`: name of authorized user.  Defaulted to 'admin'.
           - `password`: password of authorized user.  Defaulted to 'ironport'.
           - `passcode`: passcode if 2FA is enabled.
           - `disable_demo_certificate_popup`: True if no further demo certificate should be displayed, else False
        """
        username_field = 'username'
        pw_field = 'password'
        login_button = 'action:Login'
        self.input_text(username_field, user)
        self.input_password(pw_field, password)
        self.click_button(login_button)
        if passcode:
            passcode_field = 'passcode'
            self.input_password(passcode_field, passcode)
            self._click_button(login_button)

        ## Verify login status
        if 'welcome' in self.get_title().lower():
            raise guiexceptions.GuiError('%s user login with password %s FAILED' % (user, password))
        else:
            self._info('%s user login with password %s SUCCESSFUL' % (user, password))

        self._handle_whatfix_popup()
        return self.close_demo_cert_popup(**kwargs)

    def sso_login_to_dut(self, usertype='customer', sso_username=None, sso_password=None, idp='azure', username=None):
        """SSO LOGIN into DUT using specified username and password
        Parameters:
           - `sso_username`: name of sso user for sso authentication
           - `sso_password`: password of sso user  for sso authentication
           - `username`: username string for devops login for sso authentication
        """
        OPTIONS_BUTTON = "//a[contains(text(),'Options')]"
        username_field = 'username'

        if usertype == 'customer':
            SSO_LOGIN = "//*[@id='sso_link']"
        elif usertype == 'devops':
            SSO_LOGIN = "//*[@id='sso_devops']"
        else:
            raise guiexceptions.GuiError('Invalid User type for SSO Login')

        if usertype == 'devops':
            self.input_text(username_field, username)

        if self._is_element_present(SSO_LOGIN):
            self.click_element(SSO_LOGIN)
            self.set_selenium_speed(0.25)
            if idp == 'azure':
                self.do_azure_login_to_dut(sso_username, sso_password)
                if not self._is_element_present(OPTIONS_BUTTON):
                    self._check_azure_login_error()
            elif idp == 'duo':
                self._do_duo_login_to_dut(sso_username, sso_password)
                if not self._is_element_present(OPTIONS_BUTTON):
                    self._check_duo_login_error()
            else:
                raise guiexceptions.GuiError('Invalid IDP type for SSO Login')
            self._wait_until_element_is_present(OPTIONS_BUTTON, 15)
            if 'welcome' in self.get_title().lower():
                raise guiexceptions.GuiError('%s user SSO Login with password %s FAILED' % (sso_username, sso_password))
            else:
                self._info('%s user SSO Login with password %s SUCCESSFUL' % (sso_username, sso_password))
            self._handle_whatfix_popup()
            self.close_demo_cert_popup()
        else:
            raise Exception('SSO LOGIN link is not available in the page')

    def do_azure_login_to_dut(self, sso_username=None, sso_password=None):
        username_field = '//input[@type="email" and @name="loginfmt"]'
        next_button = '//input[@id="idSIButton9"]'
        pw_field = '//input[@type="password" and @name="passwd"]'
        try:
            self._handle_alert_message('alert not present already user authenticated')
            self._wait_until_element_is_present(next_button, 15)
            if 'sign in to your account' not in self.get_title().lower():
                raise guiexceptions.GuiError('Azure Gateway page is not loaded')
            else:
                self._info("Redirected to Azure Access Gateway")
            self.input_text(username_field, sso_username)
            time.sleep(2)
            self.click_element(next_button)
            time.sleep(2)
            self.input_password(pw_field, sso_password)
            self.click_element(next_button)
            time.sleep(2)
            self.click_element(next_button)
            self._handle_alert_message('checking alert after dut login')
        except Exception:
            pass

    def _do_duo_login_to_dut(self, sso_username=None, sso_password=None):
        DAG_LOGIN_BUTTON = '//*[@id="login-button"]'
        username_field = 'username'
        pw_field = 'password'
        try:
            self._handle_alert_message('alert not present already user authenticated')
            self._wait_until_element_is_present(DAG_LOGIN_BUTTON, 15)
            if 'duo access gateway' not in self.get_title().lower():
                raise guiexceptions.GuiError('DUO ACCESS Gateway page is not loaded')
            else:
                self._info("Redirected to DUO Access Gateway")
            self.input_text(username_field, sso_username)
            self.input_password(pw_field, sso_password)
            self.click_button(DAG_LOGIN_BUTTON)
            self._handle_alert_message('checking alert after dag login')
        except Exception:
            pass

    def _handle_alert_message(self, msg=''):
        try:
            alert_msg = self.get_alert_message(dismiss=False)
            self._info("alert msg:%s" % alert_msg)
            self.alert_should_be_present()
            self._info(msg)
        except Exception as error:
            self._info("alert not present: %s" % error)

    def _check_azure_login_error(self):
        SSO_LOGIN_ERROR = "//div[@id='idTD_Error']"
        try:
            self._wait_until_element_is_present(SSO_LOGIN_ERROR, 15)
            if self._is_element_present(SSO_LOGIN_ERROR):
                error_message = self._get_text(SSO_LOGIN_ERROR)
                test_time = time.strftime('%b%d-%H%M%S', time.gmtime())
                self.capture_page_screenshot('screenshot-duoerror%s.png' % test_time)
                self.go_to('https://%s' % self.dut)
                raise guiexceptions.GuiError('Duo Login Failed:%s' % (error_message))
        except guiexceptions.TimeoutError:
            self._info("SSO login timeout error occurred in 15s")

    def _check_duo_login_error(self):
        SSO_LOGIN_ERROR = "//span[contains(@class, 'message-text')]"
        try:
            self._wait_until_element_is_present(SSO_LOGIN_ERROR, 15)
            if self._is_element_present(SSO_LOGIN_ERROR):
                error_message = self._get_text(SSO_LOGIN_ERROR)
                test_time = time.strftime('%b%d-%H%M%S', time.gmtime())
                self.capture_screenshot('screenshot-duoerror%s.png' % test_time)
                self.go_to('https://%s' % self.dut)
                raise guiexceptions.GuiError('Duo Login Failed:%s' % (error_message))
        except guiexceptions.TimeoutError:
            self._info("SSO login timeout error occurred in 15s")

    def _handle_whatfix_popup(self):
        """Check if WhatFix popup appears after login. If YES then click on the
        ## Got It" button to proceed with automation."""
        try:
            popup_count = 0
            max_popup_count = 2
            timeout = 30
            timeout_start = time.time()
            popup_list = ['wfx-frame-smartPopup', 'wfx-frame-popup']
            while time.time() < timeout_start + timeout:
                for eachpopup in popup_list:
                    if self._is_element_present(eachpopup):
                        self._debug('WhatFix popup window is present')
                        self._selenium.switch_to.frame(eachpopup)
                        self._debug('Selected WhatFix iframe')
                        element = self._selenium.find_element_by_xpath('//button[contains(text(), "Got It")]')
                        self._selenium.execute_script("arguments[0].click();", element)
                        self._selenium.switch_to.default_content()
                        popup_count += 1
                        self._debug('Clicked "Got It" button in WhatFix popup window:popup count%s' % popup_count)
                        time.sleep(1)
                        if popup_count >= max_popup_count:
                            break
        except Exception as error:
            self._info("ERROR in WHATFIX Try LOGIN ::: %s" % error)
        except TimeoutError:
            self._info('Whatfix Popup is not present within 45 seconds')
        # wait for page fully loaded..
        time.sleep(3)

    def close_demo_cert_popup(self, **kwargs):
        """
                Checks if demo cert popup occurs and return warning message
                for ESA appliance.

                Parameter:
                - `disable_demo_certificate_popup`: True if no further demo certificate should be displayed, else False
                Usage : Checks if demo popup occurs and if YES, Click OK
                """
        timeout = 15
        timeout_start = time.time()
        warning_content = None
        disable_demo_certificate_popup = False
        while time.time() < timeout_start + timeout:
            try:
                if self._is_element_present("democert_dialog_c"):
                    self._debug('SMA Demo license popup window is present')
                    self.click_element('democert_dialog_c')
                    self._debug('Selected SMA demo license frame')
                    self._info("Demo certificate warning message is displayed")
                    self.click_element('//*[@type="button" and contains(text(), "OK")]')
                elif self._is_element_present("confirmation_dialog_c"):
                    self._debug('ESA Demo license popup window is present')
                    self.click_element('confirmation_dialog_c')
                    self._debug('Selected ESA demo license frame')
                    self._info("Demo certificate warning message is displayed")
                    warning_content = self._get_text("confirmation_dialog")
                    if kwargs.has_key('disable_demo_certificate_popup'):
                        disable_demo_certificate_popup = kwargs['disable_demo_certificate_popup']
                    if disable_demo_certificate_popup:
                        self.click_element('//input[@id="to_not_remind_later"]')
                    self.click_element('//*[@type="button" and contains(text(), "OK")]')
                else:
                    self._warn("Demo certificate warning message is not displayed")
                    time.sleep(1)
            except Exception as error:
                self._info("ERROR in Demo Try LOGIN ::: %s" % error)

            return warning_content

    def close_demo_cert_popup_sma(self):
        timeout = 15
        timeout_start = time.time()
        flag = 0
        while time.time() < timeout_start + timeout:
            if self._is_element_present("democert_dialog_c"):
                print "Yes element is present"
                flag = 1
                break
            else:
                time.sleep(1)
        if flag:
            try:
                self._debug('Demo license popup window is present')
                self.click_element('democert_dialog_c')
                self._debug('Selected demo license frame')
                self.click_element('//*[@type="button" and contains(text(), "OK")]')
            except Exception as error:
                self._info("ERROR in Demo Try LOGIN ::: %s" % error)

    def verify_demo_certificate_popup_after_login(self, warning_pattern, user=None, password=None, passcode=None):
        """Performs logging into DUT using specified user and password
           credential and returns True is demo certificate pop up is displayed
           and warning message pattern matches else False

        Parameters:
           - `user`: name of authorized user.  Defaulted to 'admin'.
           - `password`: password of authorized user.  Defaulted to 'ironport'.
           - `passcode`: passcode if 2FA is enabled.
           - `warning_pattern` : pattern of warning message.
        """
        if not (user and password):
            variables = common.Variables.get_variables()
            user = 'admin'
            if "${DUT_ADMIN}" in variables:
            # if variables.has_key("${DUT_ADMIN}"):
                user = variables["${DUT_ADMIN}"]
            password = Misc(None, None).get_admin_password(self.dut)

        warning_message = self._log_into_dut_int(user, password, passcode)

        if warning_message:
            if warning_pattern in warning_message:
                self._info("Demo certificate popup is present and warning message "
                           "is displayed as expected")
                return True
            else:
                self._warn("Demo certificate is displayed but warning message "
                           "on pop up is different than expected")
                return False
        else:
            self._warn("Demo certificate is not displayed or warning message "
                       "on pop up is not displayed")
            return False

    def log_out_of_dut(self):
        """Performs logging out of DUT.
        """
        try:
            self._wait_until_element_is_present("//a[contains(text(),'Options')]")
            self.mouse_over("//a[contains(text(),'Options')]")
            self.click_link("//a[contains(text(),'Log Out')]")
        except Exception as error:
            raise Exception("Page fully not loaded. Unable to log out\n:%s" % error)

        msg = 'Uncommitted Changes'
        if self._is_text_present(msg):
            err_msg = 'Uncommitted changes left'
            raise Exception(err_msg)

        # Check if we've logged out successfully.
        msg = 'You have been logged out.'
        if not self._is_text_present(msg):
            err_msg = 'Failed to logout'
            raise Exception(err_msg)

    def _get_default_dut_port(self, protocol='https'):
        wsa_ports = {'http': 8080, 'https': 8443}
        esa_sma_ports = {'http': 80, 'https': 443}
        if self.dut_version.startswith('coeus'):
            return wsa_ports[protocol]
        else:
            return esa_sma_ports[protocol]

    def drag_and_drop_to_object(self, from_loc, to_loc):
        """ Expose selenium's method for usage as a ROBOT keyword
        """
        self._info('Drag and Drop {from_loc} to {to_loc}'.format( \
            from_loc=from_loc, to_loc=to_loc))
        self._drag_and_drop_to_object(from_loc, to_loc)

    def handle_gui_failure(self):
        """
        A list of actions to be taken when failure in any GUI library occurs.
        """
        # turn off run_on_failure decorator to avoid recursion calls when
        # exception is raised inside this method
        on_failure_keyword = self._get_run_on_failure_name()
        self._set_run_on_failure('Capture Screenshot')

        # get test case id
        test_id_var = '${TEST_ID}-'
        try:
            test_id = BuiltIn().replace_variables(test_id_var)
        except:
            test_id = ''

        # get time string
        test_time = time.strftime('%b%d-%H%M%S', time.gmtime())

        # try to put window on foreground before making screen shot
        try:
            self._window_focus()
            # wait until window become in focus
            time.sleep(3)
        except Exception as e:
            self._debug('Got exception "%s"' % (e,))
            pass

        try:
            self.capture_screenshot(test_id + 'screenshot' + '-' + test_time + '.png')
        except Exception as e:
            self._debug('Got exception "%s"' % (e,))
            self._info("Could not capture screenshot of the page")

        try:
            self.capture_source(test_id + 'source' + '-' + test_time + '.html')
        except Exception as e:
            self._debug('Got exception "%s"' % (e,))
            self._info("Could not log HTML source of the page")

        try:
            self.handle_application_error()
        except Exception as e:
            self._warn("Error while recovering: exception %s" % (e,))

        # turn on run_on_failure decorator
        self._set_run_on_failure(on_failure_keyword)

    def handle_application_error(self):
        """
        Close browser and re-login for Application error
        """
        error_messages = [
            'An application error has occurred',
            'Application Error',
        ]
        error_present = False

        for msg in error_messages:
            if self._is_text_present(msg):
                error_present = True
                break
        try:
            robot_vars = common.Variables.get_variables()
            if robot_vars:
                if robot_vars.has_key('${TEST_ID}'):
                    test_id = robot_vars['${TEST_ID}']
                    self._info("TEST_ID- %s" % (test_id))
                    if test_id == 'Tvh929137c':
                        self._info("Debug- selvans- test ID matched")
                        return
        except:
            # Default ${TEST_ID} to 'Unknown' for stand alone usage.
            pass

        if error_present:
            self._debug('Recovering from application error')
            self._debug('Recovering: close browser')
            self.close_browser()
            self._debug('Recovering: launch dut browser')
            self.launch_dut_browser()
            self._debug('Recovering: log into dut')
            self.log_into_dut()
            self._debug('Recovering: done')

    def _save_source(self, data, filename):
        path, link = self._get_screenshot_paths(filename)
        outfile = codecs.open(path, encoding='utf-8', mode='w')
        outfile.write(data)
        outfile.close()
        # add link to html file into log
        self._html('<a href="%s">Entire HTML Source of the page</a>' % (link,))

    # # overwritten SeleniumLibrary method
    # def click_button(self, locator, dont_wait=''):
    #     """Adjustment to the locators are made before locators are passed to the
    #     SeleniumLibrary's method.
    #
    #     * prefixes 'id=' and 'name=' are removed,
    #     * 'xpath=' prefix is added to the locators with initial '//'.
    #     """
    #     #old_locator = locator
    #     #self.click_button(self._modify_locator(locator), dont_wait)
    #     super(ExtendedSeleniumLibrary, self).click_button(self._modify_locator(locator), dont_wait)

    def _modify_locator(self, locator):
        # self._debug('Locator: %s' % locator)
        if re.search(r'^xpath', locator):
            temp = locator.split('xpath=')
            index = 1 if len(temp) > 1 else 0
            locator = temp[index]
        if re.search(r'/$', locator):
            locator = locator.rstrip('/')
        return locator

    def _set_key_is_encrypted(self, key_is_encrypted):
        CHECK_BOX = '//input [@id="encrypted_key" and @type="checkbox"]'
        if key_is_encrypted != None:
            self._set_checkbox(key_is_encrypted, CHECK_BOX)

    def _set_key_password(self, key_password):
        ENTRY_FIELD = \
            '//input[@type = "password" and @name="encrypted_key_password"]'
        if key_password != None:
            self.input_password(ENTRY_FIELD, key_password)

    def _click_next_button(self):
        next_button = "action:Next"
        self.click_button(next_button)

    def _show_advanced(self):
        ARROW = "//div[contains(@id,'arrow_closed')]"
        if self._is_visible(ARROW):
            self.click_element(ARROW, "don't wait")
        else:
            self._info('advanced link is not visible.skipping to click...')

    def _click_continue_button(self, text="Continue"):
        legacy_continue_button = "//button[@type='button']"
        continue_button = "//button[contains(text(),'%s')]" % \
                          text
        try:  # verify that confirmation dialog appeared
            try:  # that's the right new way to click Continue button
                self.click_button(continue_button)
                self._info('Clicked %s button' % text)
            except:  # for backward compatibility in case of "the right new way" fails
                self.click_button(legacy_continue_button)
                self._warn('Clicked Continue button in legacy format')
        except:
            self._warn('Continue button did not appear')
        return self._check_action_result()

    def _click_radio_button(self, element):
        element = self._modify_locator(element)
        self.click_element(element, 'dont_wait')

    def _set_checkbox(self, state, element):
        element = self._modify_locator(element)
        if state:
            self._select_checkbox(element)
        elif state is not None:
            self._unselect_checkbox(element)

    def _select_checkbox(self, element):
        element = self._modify_locator(element)
        if not self._is_checked(element):
            self._debug('_select_checkbox clicking %s' % element)
            self.click_element(element, 'dont_wait')
        else:
            self._debug('_select_checkbox already checked %s' % element)

    def _unselect_checkbox(self, element):
        element = self._modify_locator(element)
        if self._is_checked(element):
            self._debug('_unselect_checkbox clicking %s' % element)
            self.click_element(element)
        else:
            self._debug('_unselect_checkbox already unchecked %s' % element)

    def _navigate_to(self, tab, menu, submenu=None):
        try:
            self._debug("CURRENT URL:%s" % self.get_location())
            self._debug('TAB:%s MENU:%s SUBMENU:%s'%(tab, menu, submenu))
            self._internal_navigate_to(tab, menu, submenu)
        except Exception as error:
            self._warn('"Navigate To" failed, retrying: %s' %error)
            self.go_to('https://%s' % self.dut)
            self._internal_navigate_to(tab, menu, submenu)

    def _internal_navigate_to(self, tab, menu, submenu=None):
        sma_tabs = {'Management': 'tab_management',
                    'Management Appliance': 'tab_management',
                    'Email': 'tab_email',
                    'Web': 'tab_web',
                    }
        sidebar_links = ['My Favorites', 'Options', 'Help and Support']
        self._info("TAB: %s menu :%s submenu:%s" %(tab, menu, submenu))
        self.mouse_over('//img[@class="logo"]')
        if submenu is None and tab not in sidebar_links:
            element_to_point = "//a[contains(text(),'%s') " % tab + \
                               "and contains(@class, 'yuimenubaritemlabel-hassubmenu')]"

            menu_path = "//a[text()='%s']"%tab
            self._info("element_to_point:%s :%s" % (element_to_point, self._is_element_present(element_to_point)))
            self._info("Menu:%s :%s  "%(menu_path, self._is_element_present(menu_path)))

            if self._is_element_present(element_to_point):
                self.mouse_over(element_to_point)
            else:
                try:
                    self._wait_until_element_is_present(menu_path, timeout=10)
                except Exception:
                    print "After wait also menu is not loaded."
                self.click_element(menu_path)
                self.mouse_over(menu_path)
            time.sleep(3)
            try:
                self._click_menu_link(menu)
            except Exception as error:
                print "CLICK LINK failed",error
                self.click_link(menu)
        else:
            if tab in sidebar_links:
                # Navigation through sidebar links
                submenu = menu
                menu = tab
                tab = None
            # Do SMA or sidebar navigation
            menu_locator = "//a[contains(text(),'%s') " % menu + \
                           "and contains(@class, 'yuimenubaritemlabel-hassubmenu')]"
            if tab is not None:
                _tab_loc = "//a[@id='%s']" % (sma_tabs[tab],)
                # Skip clicking the tab if it is open
                # (to avoid reloading default page of the tab.)
                _tab_selected = int(self.get_matching_xpath_count(
                    _tab_loc + "/parent::li[contains(@class, 'selected')]"))
                if _tab_selected == 0:
                    self.click_link("xpath=%s" % (_tab_loc,))

            if self._is_element_present(menu_locator):
                try:
                    self.mouse_over(menu_locator)
                except:
                    # Workaround due to bug CSCvk24126
                    menu1_locator = "//div[@id='yui-navbar']/ul/li[1]/a/img"
                    if self._is_visible(menu1_locator):
                        self.mouse_over(menu1_locator)
                    time.sleep(1)
                    self.mouse_over(menu_locator)
            else:
                self.mouse_over("link=%s" % menu)
            time.sleep(1)
            try:
                self._click_menu_link(submenu)
            except:
                try:
                    self._wait_until_element_is_present(submenu)
                except Exception as error:
                    print "ERROR SUB menu is not vis", error
                self.click_link(submenu)

        # [TODO] The JavaScript Externalization has caused a lot of test failures and this happens mostly on page load.
        # Keeping a common sleep here on the navigate to could help code change across other files.
        time.sleep(3)

    def _click_menu_link(self, item):
        GENERIC_LOCATOR = "//a[starts-with(@href, 'http') and " \
                          "contains(text(), '%s')]" % (item,)
        LOCATOR = lambda n: 'xpath=(' + GENERIC_LOCATOR + ')[%s]' % (n + 1,)
        link_count = int(self.get_matching_xpath_count(GENERIC_LOCATOR))
        assert link_count > 0, "menu link not found"
        if link_count == 1:
            link = GENERIC_LOCATOR
            if self._is_visible(link):
                try:
                    self._click(link)
                except AttributeError:
                    self.click_link(link)
            else:
                scroll = '//div[contains(@class, "scrollbar") and' + \
                         ' not(contains(@class, "scrollbar_disabled"))]'
                self.mouse_over(scroll)
                timeout = 10
                Wait(
                    lambda: self._is_visible(link),
                    timeout=timeout,
                    msg='Link {locator} has not become visible after {timeout}'.format( \
                        locator=link, timeout=timeout)
                ).wait()
                self.click_link(link)
            return

        self._info("Generic locator matched more then one link")
        self._debug('links matched: %s' % (link_count,))

        # Now checking visibility
        visible_links = filter(lambda x: self._is_visible(LOCATOR(x)),
                               xrange(link_count))
        visible_count = len(visible_links)

        if visible_count == 0:
            self._warn("No links are visible. Giving up and clicking on first invisible.")
            self.click_link(LOCATOR(0))
        else:
            if visible_count > 1:
                for i in visible_links:
                    self._debug('link is visible: %s' % (LOCATOR(visible_links[i]),))

            # if side-bar menu is opened its link will be first in list, if not then only main menu link is visible
            # note - this can become incorrect after page layout changes !
            self.click_link(LOCATOR(visible_links[0]))

    def _click_edit_settings_button(self):
        edit_button = "//input[@value='Edit Settings...']"
        self.click_button(edit_button)

    def _click_submit_button(self, wait=True, accept_confirm_dialog=None,
                             accept_EULA=None, skip_wait_for_title=False, check_result=True):
        """
        Click Submit button and verify the result
        Parameter skip_wait_for_title controls whether we need to wait after
        submit when MSG_TITLE appears. In most cases (and by default) we need,
        but after submitting Time Range - no and the parameter should be set to
        True
        """
        submit_button = "//input[@value='Submit']"
        CONFIRM_DLG = '//div[@id="confirmation_dialog"]'
        MSG_TITLE = '//span[@id="action-results-title"]'
        CONFIRM_BTN = lambda confirm: '%s//button[text()="%s"]' % \
                                      (CONFIRM_DLG, {True: 'Continue',
                                                     False: 'Cancel',
                                                     'Import': 'Import'}[confirm])
        ACCEPT_EULA = lambda confirm: 'action:%sLicense' % \
                                      {True: 'Accept', False: 'Decline'}[confirm]

        self._wait_until_element_is_present(submit_button)
        ERROR_LOCATOR = lambda i: 'xpath=(' + generic_error_locator + ')[%s]' % i
        submit_button = self._get_visible_elements(submit_button)[0]
        if wait:
            self.click_button(submit_button)
        else:
            self.click_button(submit_button, "don't wait")

        # If confirmation dialog is expected.
        if accept_confirm_dialog is not None:
            # Elements may not be available
            try:
                # confirmation dialog
                time.sleep(5)  # to avoid time races
                self.click_button(CONFIRM_BTN(accept_confirm_dialog), None)
                self._info('Clicked "Continue" on confirmation popup dialog')
            except:
                self._info('Confirmation popup dialog did not appear')

        if not skip_wait_for_title:
            tmr = CountDownTimer(60).start()
            while tmr.is_active():
                # wait for a second before checking element.
                time.sleep(1)
                # Element may not be available on page reload
                try:
                    if self._is_visible(MSG_TITLE):
                        # Errors are displayed
                        break
                    # if License Agreement is expected
                    if accept_EULA is not None:
                        if self._is_text_present('License Agreement'):
                            # Accept or decline EULA
                            self.click_button(ACCEPT_EULA(accept_EULA))
                except:
                    pass

        # delay 3 seconds to account for latency with submit action before
        # checking for action result
        if check_result:
            time.sleep(3)
            return self._check_action_result()

    # User keywords
    def navigate_to(self, tab, menu, submenu=None):
        """Navigate to a page by menu.

           Parameters:
            - `tab`: first-level item of navigation
            (SMA: name of a tab, or "Options", "Help and Support";
             WSA: name of a menu, or "Options", "Support and Help").
            - `menu`: second-level item of navigation
            (SMA: name of a menu in selected tab, or menu item in "Options", "Help and Support",
             WSA: name of a menu item in selected menu, or menu item in "Options", "Support and Help").
            - `submenu`: third-level item of navigation
            (SMA: name of a menu item in selected menu,
             WSA: not used).

           Examples:
           | # SMA examples: |
           | Navigate To | Management Appliance | Centralized Services | System Status |
           | Navigate To | Options | Active Sessions |
           | # WSA examples: |
           | Navigate To | System Administration | Next Steps |
           | Navigate To | Support and Help | Remote Access |
        """
        self._navigate_to(tab, menu, submenu)

    def capture_source(self, filename):
        """
        Save the entire html source of the current page or frame into file.
        """
        data = self.get_source()
        self._save_source(data, filename)

    def commit_changes(self, comment=None):
        """commit appliance configuration changes.

        :Parameters:
            - `comment`: Comment for commit changes.

        Examples:
        | Commit Changes |
        | Commit Changes | comment=Configured SMTP Routes |
        """

        comment_field = 'comment'
        commit_changes_button = "//*[@type='button' and contains(@value, 'Commit Changes')]"
        final_commit_changes_button = "xpath=//input[@value='Commit Changes']"
        msg1 = 'Your changes have been committed'
        msg2 = 'The system is rebooting'
        msg3 = 'Migration of Policy, Virus and Outbreak Quarantines finished'
        msg4 = 'The changes in the settings of the SSL Configuration can cause all related services to restart'
        msg5 = 'You are currently using a demonstration certificate (Cisco Secure Email Certificate) which is not secure and is not recommended for general use'

        if not self._wait_until_element_is_present(commit_changes_button, timeout=5, raise_exception=False):
            self._debug('COMMIT CHANGES BUTTON NOT PRESENT')
            return
        self.click_button(commit_changes_button)

        if comment:
            self.input_text(comment_field, comment)

        dut_reboot_required=False
        if self._is_text_present(msg4):
            self._debug("Warning: Changes in SSL Configuration can cause all related services to restart")
            dut_reboot_required=True

        try:
            self.click_button(final_commit_changes_button)
        except Exception as e:
            if str(e).startswith('Timed out after'):
                self._debug("Got timeout exception from selenium server. " \
                            "Verifying success message")
            if not (self._is_text_present(msg1) or self._is_text_present(msg2) or self._is_text_present(msg3)):
                raise Exception('Failed to commit changes.')

        if not dut_reboot_required:
            if not(self._is_text_present(msg1) or self._is_text_present(msg2) or self._is_text_present(msg3) or self._is_text_present(msg5)):
                raise Exception('Failed to commit changes.')
            if self._is_text_present(msg2):
                dut_reboot_required=True

        if dut_reboot_required:
            SysTools(self.dut, self.dut_version).wait_until_dut_reboots(timeout=900)
        else:
            Misc(self.dut, self.dut_version).wait_until_ready()

    def abandon_changes(self):
        """Clears appliance configuration changes. """

        commit_changes_button = "//*[@type='button' and contains(@value, 'Commit Changes')]"
        abandon_changes_button = "//input[@value='Abandon Changes']"

        if not self._wait_until_element_is_present(commit_changes_button, timeout=5, raise_exception=False):
            self._debug('COMMIT CHANGES BUTTON NOT PRESENT')
            return

        self.click_button(commit_changes_button)
        self.click_button(abandon_changes_button)
        msg = 'Your changes have been abandoned.'
        if not self._is_text_present(msg):
            raise Exception('Failed to abandon changes.')

    def cancel_changes(self):
        """Cancels commit of appliance configuration changes. """
        commit_changes_button = u"xpath=//input[@value='Commit Changes »']"
        cancel_changes_button = "//input[@value='Cancel']"

        self.click_button(commit_changes_button)
        self.click_button(cancel_changes_button)
        if not self._is_element_present(commit_changes_button):
            raise Exception('Failed to cancel changes.')

    def _get_policies(self):
        """
        Returns list of policies as a dictionary
        """
        result = {}
        TABLE = "//table[@class = 'cols']/tbody"
        rows = int(self.get_matching_xpath_count(TABLE + "/tr"))
        columns = int(self.get_matching_xpath_count(TABLE + "/tr[2]/td"))
        for row in range(2, rows + 1):
            a_policy = {}
            a_policy['state'] = 'enabled'
            policy = TABLE + "/tr[%s]" % row
            lines = str(self._get_text(policy + '/td[2]')).splitlines()
            if self._get_text(TABLE + "/tr[1]/th[1]") == 'Order':
                a_policy["order"] = \
                    self._get_text(policy + "/td[1]")
                order = 2
            else:
                order = 1
            # Policy
            policy_column = policy + "/td[%s]" % order
            if self._is_element_present(policy_column + "//strong"):
                policy_name = self._get_text(policy_column + "//strong")
            elif self._is_element_present(policy_column + "//a"):
                policy_name = self._get_text(policy_column + "//a")
            else:
                policy_name = self._get_text(policy_column)
            items = int(self.get_matching_xpath_count(policy_column + \
                                                      "/table/tbody/tr"))
            if items == 0:
                for line in lines[1:]:
                    ind = line.find(':')
                    if ind > -1:
                        a_policy[line[:ind].strip().lower().replace(' ', '_')] = \
                            line[(ind + 1):].strip()
                    else:
                        if line.find('(disabled)') > -1:
                            a_policy['state'] = 'disabled'

            for item in range(1, items + 1):
                property = policy_column + "/table/tbody/tr[%s]" % item
                if self._is_element_present(property + "/td[2]"):
                    a_policy[self._get_text(property + "/td[1]")[:-1]. \
                        lower(). \
                        replace(' ', '_')] = \
                        self._get_text(property + "/td[2]")

            for column in range((order + 1), columns):
                a_policy[self._get_text(TABLE + "/tr[1]/th[%s]" % column). \
                    lower(). \
                    replace(' ', '_'). \
                    replace('\n', '_'). \
                    replace('__', '_')] = \
                    self._get_text(policy + "/td[%s]" % column)
            result[policy_name] = a_policy
        return result

    def _grep_error_messages(self):
        """Grep error messages from page. """
        err_msgs_list = []
        generic_error_locator = '//*[@class="error"]'
        ERROR_LOCATOR = lambda i: 'xpath=(' + generic_error_locator + ')[%s]' % i
        count = int(self.get_matching_xpath_count(generic_error_locator))
        for i in xrange(1, count + 1):
            if self._is_visible(ERROR_LOCATOR(i)):
                err_msgs_list.append(self._get_text(ERROR_LOCATOR(i)))
        return err_msgs_list

    def _get_visible_elements(self, locator):
        locator = self._modify_locator(locator)
        count = int(self.get_matching_xpath_count(locator))
        if count == 0:
            self._warn('Locator "%s" was not found')
            return []
        if count == 1:
            return [locator]
        locators = []
        for i in xrange(1, count + 1):
            current_locator = 'xpath=(' + locator + ')[%s]' % i
            if self._is_visible(current_locator):
                locators.append(current_locator)
        return locators

    def check_for_warning(self):
        """ If warning is detected on the page, log it and return else return None """
        WARNING = "//* [@class = 'action-results-warn']"
        WARNING_MESSAGE = WARNING + "/../../td[last()]"
        result = None
        if self._is_visible(WARNING_MESSAGE):
            result = self._get_text(WARNING_MESSAGE)
            self._warn(result)
        return result

    def _check_action_result(self):
        """ Checks the action result on the page
        There is 3 types of results:
            - Success - action succeeded
            - Warning - action succeeded with some issues
            - Error - action failed
        Currently Warning is treated as succeeded
        TODO: special treatment for Warning action result
        :Return:
            None
        :Exceptions:
            - WuiValueError - one or more values did not meet validator's
            requirements """

        time.sleep(1)
        try:
            RESULT_TITLE = "//*[@id='action-results-title']"
            RESULT_MSG = "//*[@id='action-results-message']"
            self._wait_until_element_is_present(RESULT_TITLE)
            self._wait_until_element_is_present(RESULT_MSG)
            result = self._get_text(RESULT_TITLE)
            msg = self._get_text(RESULT_MSG)
        except:  # If there are none Errors check passes
            test_time = time.strftime('%b%d-%H%M%S', time.gmtime())
            self.capture_page_screenshot('check-action-screenshot' + '-' + test_time
                                    + '.png')
            import traceback
            self._debug(traceback.print_exc())
            result = ''
            msg = ''

        self._info("after clicking Submit the result is '%s'" % result)

        if result == "Error":
            error_messages = self._grep_error_messages()
            e = guiexceptions.GuiValueError(msg, error_messages)
            raise e
        return result, msg

    def _click_done_button(self, wait=True):
        done_button = "//input[@value='Done']"
        if wait:
            self.click_button(done_button)
        else:
            self.click_button(done_button, "don't wait")

    def _check_feature_status(self, feature):
        """Check if feature is enabled.
        :Parameter:
          - `feature`: feature name
        :Return:
            True if feature is enabled. False if not
            Generate exception for invalid feature name """
        text_info_dict = \
            {'acceptable_use_control': 'The Acceptable Use Controls ' \
                                       'feature is currently disabled.',
             'ironport_url_filters': 'The IronPort URL Filters feature ' \
                                     'is currently disabled.',
             'webroot': 'Webroot is currently disabled globally.',
             'mcafee': 'McAfee is currently disabled globally.',
             'sophos': 'Sophos is currently disabled globally.',
             'saas_id_provider': 'WSA has not been configured as identity '
                                 'provider for SaaS.',
             'https_proxy': 'The HTTPS Proxy is currently disabled',
             'ocsp': 'Enable Online Certificate Status Protocol (OCSP) to configure additional options for certificate checking',
             'upstream_proxy': 'No upstream proxies are defined',
             'ocsp_optional': 'Optional settings for OCSP timeouts and upstream proxy use',
             'data_transfer_filters': 'The Cisco Data Security ' \
                                      'Filters feature is currently disabled.',
             'l4tm': 'The L4 Traffic Monitor is currently disabled.',
             'pac_file_hosting': 'Proxy Auto-Configuration File ' \
                                 'Hosting is currently disabled.',
             'proxy_settings': 'The Web Proxy is currently disabled',
             'ftp_proxy': 'The FTP Proxy is currently disabled.',
             'socks_proxy': 'The SOCKS Proxy is currently disabled.',
             'senderbase': 'SenderBase network participation is currently disabled.',
             'sensorbase': 'SensorBase network participation is ' \
                           'currently disabled.',
             'wbrs': 'The Web Reputation Filters feature is currently disabled.',
             'mus': 'Mobile Security Service is disabled.',
             'ise': 'The Identity Service Engine is currently disabled.',
             'machine_id': 'The Machine Identification service is currently disabled',
             'acsm': 'AnyConnect Secure Mobility is disabled.'}

        if feature.lower() in text_info_dict.keys():
            if self._is_text_present(text_info_dict[feature.lower()]):
                self._info('Returning false.Text present-{txt_prsnt}'.format( \
                    txt_prsnt=text_info_dict[feature.lower()]))
                return False
            else:
                return True
        else:
            raise ValueError('Feature name \'%s\' is incorrect or undefined ' \
                             'in guicommon' % (feature,))

    def _is_proxy_configured(self):
        """Check if Proxy is configured.

        :Return:
            True if Proxy is configured. Generate exception if not

        """
        if self._is_text_present('The Web Proxy is not configured'):
            raise guiexceptions.GuiProxyNotConfiguredError \
                ('Web Proxy is not configured, need to run SSW')
        else:
            return True

    def _validate_presence(self, locator):
        """Validate if element locator is present on current page.

        :Parameters:
            - `locator`: element-locator
        """
        locator = self._modify_locator(locator)
        if not self._is_element_present(locator):
            err_msg = 'Element-locator \'%s\' is not present on page %s. ' \
                      'It is possibly removed or renamed.' % \
                      (locator, self.get_location())

            raise Exception(err_msg)

    def _wait_until_element_is_present(self, locator, timeout=5, raise_exception=True):
        """
        Wait until the specified element is present or timeout is expired
        """
        locator = self._modify_locator(locator)
        return Wait(
            lambda: self._is_visible(locator),
            timeout=timeout,
            raise_exception=raise_exception,
            msg='Element "{locator}" is not present after {timeout} seconds'.format( \
                locator=locator, timeout=timeout)
        ).wait()

    def _wait_until_text_is_present(self, text, timeout=5):
        """
        Wait until the specified text is present or timeout is expired
        """
        Wait(
            lambda: self._is_text_present(text),
            timeout=timeout,
            msg='Text "{text}" is not present after {timeout} seconds'.format( \
                text=text, timeout=timeout)
        ).wait()

    def _wait_for_text(self, locator, expected_text, timeout=60):
        """Wait for the text of the element to appear on the page.

        :Parameters:
            - `locator`: element locator.
            - `expected_text`: expected text of the element.
            - `timeout`: timeout to wait for the text to appear.

        :Exceptions:
            - `TimeoutError`: in case of failure to retrieve expected text in
                              `timeout` seconds.
        """
        locator = self._modify_locator(locator)
        self._validate_presence(locator)

        patt = re.compile(expected_text)

        wait = Wait(msg="Failed to retrieve '%s' text from '%s' element" % \
                        (expected_text, locator), timeout=timeout, \
                    until=lambda: self._is_element_present(locator) and \
                                  patt.search(self._get_text(locator).strip()))
        wait.wait()

    def _wait_to_click_button(self, locator, button_name, timeout=260,
                              raise_exception=True):
        """click the button, when appear on the page

        Parameters:
            - `locator`: element locator for a button.
            - `button_name`: Name of the button
            - `timeout`: timeout to wait for the text to appear.
            - `raise_exception`: raise exception if button does not appear

        Exceptions:
            - `guiexceptions.TimeoutError`: in case of failure to click the button in
                              `timeout` seconds.
        """
        locator = self._modify_locator(locator)
        wait = Wait(
            msg='Failed to click \'%s\' button' % button_name,
            timeout=timeout,
            until=lambda: self._is_element_present(locator),
            raise_exception=raise_exception
        )
        if wait.wait():
            self.click_button(locator)
            self._info("Clicked '%s' button" % button_name)
        else:
            self._info("Button '%s' did not appear" % button_name)

    def _create_prefs_js_pac(self, pacurl):
        # Generate Firefox's prefs.js for autoconfig pac url
        self.prefs_js_path = os.path.join(self._ff_profile.directory, 'prefs.js')
        prefs_js = open(self.prefs_js_path, 'a+')
        prefs_js.write('# Mozilla User Preferences\n')
        prefs_js.write('user_pref("network.proxy.type", 2);\n')
        prefs_js.write('user_pref("network.proxy.autoconfig_url", "%s");\n' % (pacurl))
        prefs_js.close()

    def _create_prefs_js(self, proxy_conf):
        valid_protocols = ('http', 'ssl', 'ftp')
        self.prefs_js_path = os.path.join(self._ff_profile.directory, 'prefs.js')
        prefs_js = open(self.prefs_js_path, 'a+')

        # Generate Firefox's prefs.js.
        prefs_js.write('# Mozilla User Preferences\n')
        prefs_js.write('user_pref("network.proxy.type", 1);\n')

        try:
            for conf in proxy_conf:
                conf = conf.split(':')
                proto = conf[0]
                ip = ":".join(conf[1:-1])
                port = conf[-1]
                if proto not in valid_protocols:
                    raise ValueError('Invalid protocol.  Valid are: %s'
                                     % (valid_protocols,))
                # Add proxy configuration.
                prefs_js.write('user_pref("network.proxy.%s", "%s");\n' % \
                               (proto, ip))
                prefs_js.write('user_pref("network.proxy.%s_port", %s);\n' % \
                               (proto, port))
        finally:
            prefs_js.close()

    def _accept_license(self):
        ACCEPT_LICENSE_BUTTON = "//input[@value='Accept']"
        if self._is_element_present(ACCEPT_LICENSE_BUTTON):
            self.click_button(ACCEPT_LICENSE_BUTTON)
        return self._check_action_result()

    def _input_text_if_not_none(self, locator, text):
        if text is not None:
            locator = self._modify_locator(locator)
            self.input_text(locator, text)

    def _handle_submit(self, submit):
        if submit:
            self._click_submit_button()

    def _get_available_options_from_select(self, locator):
        """
        Gets list of available options from select menu.
        Parameters:
        - `locator`: Select list.

        Return:
        List
        """
        try:
            locator = self._modify_locator(locator)
            OPTIONS_NUM = \
                int(self.get_matching_xpath_count("%s/option" % locator))
            OPTIONS = \
                [self.get_text("%s/option[%s]" % (locator, i)) \
                 for i in range(1, OPTIONS_NUM + 1)]
            return OPTIONS
        except guiexceptions.SeleniumClientException:
            self._warn("Failed to get available options from %s" % locator)
            return []

    def _regex_option(self,
                      option,
                      starts_with=True,
                      ends_with=False,
                      contains=False,
                      custom=False):
        # all regex expressions use re.I - ignore case
        # if none of named args are passed then return option as is
        # also it is possible to use regexp at the rf txt tests level
        # by passing the arg as 'regexp:some_value'
        if not any([starts_with, ends_with, contains, custom]):
            return option
        if starts_with:
            return 'regexpi:^%s.*' % option
        if ends_with:
            return 'regexpi:.*%s$' % option
        if contains:
            return 'regexpi:.*%s.*' % option
        if custom:
            return 'regexpi:%s' % custom

    def _select_from_list_use_regex(self, locator, option, **kwargs):
        # allow to leave selected value as is
        # pass 'starts_with' or 'ends_with' or 'contains' or 'custom' in kwargs
        if option is not None:
            try:
                locator = self._modify_locator(locator)
                self.select_from_list \
                    (locator, self._regex_option(option, **kwargs))
            except Exception as error:
                self._info('Error%s' % error)
                opts = self._get_available_options_from_select(locator)
                raise ValueError \
                    ("Invalid option '%s' for '%s'. Select one from: %s" % \
                     (option, locator, ', '.join(opts)))

    def _select_unselect_checkbox(self, locator, param):
        """
        If param is None - do nothing
        If Param is 'n' or 'no' any case or False , uncheck
        else - check
        """
        # In may testcases param is used as Boolean, True or False
        if type(param) == bool:
            if param == True:
                param = "yes"
            elif param == False:
                param = "no"
        locator = self._modify_locator(locator)
        self._debug('_select_unselect_checkbox %s %s' % (locator, param))
        if param is not None:
            if param.lower() in ['n', 'no']:
                self._unselect_checkbox(locator)
            else:
                self._select_checkbox(locator)

    def _get_element_index_by_name(self,
                                   locator,
                                   element_name,
                                   column=None,
                                   start_count=None,
                                   dont_count_last_nrows=None,
                                   strict_match=True,
                                   only_clickable=True):
        """
        Get index of element by its name.

        Parameters:
        - `locator`: Locator of container. Mandatory.
        Typically it is table, /table[@class='pairs'] or /table[@class='cols']
        - `element_name`: name of the element as it is seen in the wui. Mandatory.
        - `column`: Number of column to look for the name. Optional.
        Typically it is first column.
        It is clickable(link). Typically it is first column(td) of the row.
        - `start_count`: The index value to start rows count from. Optional.
        In most cases it is equal to '2'.
        - `dont_count_last_nrows`: The number to subtract from total rows. optional.
        Table may contain some footer or toolbar without data.
        - `strict_match`: Use regex or not. Boolean. Useful for cases like:
        'Spam Quarantine (IP Interface not configured) **' or 'Outbreak *'
        - `only_clickable`: Some elements may be configured(present in the table), but inactive and
        can't be accessed (no link, disabled). Example: Monitor > Quarantines page on ESA.

        Return: Tuple. (row_idx, col_idx) - coordinates in table where given name was found.

        Exceptions: ValueError - if could not find element with given name.
        """
        _names = []
        _index = None
        locator = self._modify_locator(locator)
        _rows = int(self.get_matching_xpath_count('%s//tr' % locator))
        if dont_count_last_nrows:
            rows = _rows - dont_count_last_nrows
        else:
            rows = _rows
        rowno = start_count or 2
        colno = column or 1
        if only_clickable:
            text = \
                lambda row: self.get_text('%s//tr[%s]/td[%s]/a' % \
                                          (locator, row, colno)).strip() \
                    if self._is_element_present('%s//tr[%s]/td[%s]/a' % \
                                                (locator, row, colno)) else None
        else:
            text = \
                lambda row: self.get_text('%s//tr[%s]/td[%s]' % \
                                          (locator, row, colno)).strip() \
                    if self._is_element_present('%s//tr[%s]/td[%s]' % \
                                                (locator, row, colno)) else None
        try:
            while rowno <= rows:
                _found = text(rowno)
                if _found:
                    _names.append(_found)
                if not strict_match:
                    mo = re.search('^%s.*' % element_name, _found, re.IGNORECASE)
                    if mo:
                        _index = rowno
                        break
                if _found == element_name:
                    _index = rowno
                    break
                rowno += 1
            if not _index:
                raise ValueError \
                    ("No such element: '%s'. Table has these elements: %s" % \
                     (element_name, ','.join(_names)))
            return _index, colno
        except guiexceptions.SeleniumClientException as ex:
            self._warn(ex)

    def _get_element_link(self,
                          locator,
                          element_name,
                          column=None,
                          start_count=None,
                          dont_count_last_nrows=None,
                          strict_match=True,
                          only_clickable=True):
        """
        Get element's link to click on.

        Parameters:
        - `locator`: Locator of container. Mandatory.
        Typically it is table, /table[@class='pairs'] or /table[@class='cols']
        - `element_name`: name of the element as it is seen in the wui. Mandatory.
        - `column`: Number of column to look for the name. Optional.
        Typically it is first column.
        It is clickable(link). Typically it is first column(td) of the row.
        - `start_count`: The index value to start rows count from. Optional.
        In most cases it is equal to '2'.
        - `dont_count_last_nrows`: The number to subtract from total rows. optional.
        Table may contain some footer or toolbar without data.
        - `strict_match`: Use regex or not. Boolean. Useful for cases like:
        'Spam Quarantine (IP Interface not configured) **' or 'Outbreak *'
        - `only_clickable`: Some elements may be configured(present in the table), but inactive and
        can't be accessed (no link, disabled). Example: Monitor > Quarantines page on ESA.

        Return: String. Link to click on.
        """
        locator = self._modify_locator(locator)
        row_idx, col_idx = self._get_element_index_by_name(locator,
                                                           element_name,
                                                           column=column,
                                                           start_count=start_count,
                                                           dont_count_last_nrows=dont_count_last_nrows,
                                                           strict_match=strict_match,
                                                           only_clickable=only_clickable)
        link = '%s//tr[%s]/td[%s]/a' % (locator, row_idx, col_idx)
        return link

    def _get_element_delete_link(self,
                                 locator,
                                 element_name,
                                 column=None,
                                 start_count=None,
                                 dont_count_last_nrows=None,
                                 del_column=None,
                                 strict_match=True,
                                 only_clickable=True):
        """
        Get element's link to delete element.

        Parameters:
        - `locator`: Locator of container. Mandatory.
        Typically it is table, /table[@class='pairs'] or /table[@class='cols']
        - `element_name`: name of the element as it is seeen in the wui. Mandatory.
        - `column`: Number of column to look for the name. Optional.
        Typically it is first column.
        It is clickable(link). Typically it is first column(td) of the row.
        - `start_count`: The indexs value to start rows count from. Optional.
        In most cases it is equal to '2'.
        - `dont_count_last_nrows`: The number to subtract from total rows. optional.
        Table may contain some footer or toolbar without data.
        - `del_column`: Number of column where delete link(icon) is present. Optional.
        Typically it is last column of the table.
        - `strict_match`: Use regex or not. Boolean. Useful for cases like:
        'Spam Quarantine (IP Interface not configured) **' or 'Outbreak *'
        - `only_clickable`: Some elements may be configured(present in the table), but inactive and
        can't be accessed (no link, disabled). Example: Monitor > Quarantines page on ESA.

        Return: String. 'Delete link' to click on.
        """
        locator = self._modify_locator(locator)
        row_idx, col_idx = self._get_element_index_by_name(locator,
                                                           element_name,
                                                           column=column,
                                                           start_count=start_count,
                                                           dont_count_last_nrows=dont_count_last_nrows,
                                                           strict_match=strict_match,
                                                           only_clickable=only_clickable)
        del_col_idx = \
            del_column or \
            int(self.get_matching_xpath_count('%s//tr[%s]/td' % (locator, row_idx)))
        link = '%s//tr[%s]/td[%s]/img' % (locator, row_idx, del_col_idx)
        return link

    def _get_element_list(self,
                          locator,
                          column=None,
                          start_count=None,
                          dont_count_last_nrows=None,
                          only_clickable=True):
        """
        Get list of elements in the container(table).

        Parameters:
        - `locator`: Locator of container. Mandatory.
        Typically it is table, /table[@class='pairs'] or /table[@class='cols']
        - `column`: Number of column to look for the name. Optional.
        It is clickable(link). Typically it is first column(td[1]) of the row.
        - `start_count`: The indexs value to start rows count from. Optional.
        In most cases it is equal to '2'.
        - `dont_count_last_nrows`: The number to subtract from total rows. Optional.
        Table may contain some footer or toolbar without data.
        - `only_clickable`: Some elements may be configured but inactive - present in the table,
        but can't be accessed (no link, disabled). Example: Monitor > Quarantines page on ESA.

        Return: List.
        """
        _names = []
        locator = self._modify_locator(locator)
        _rows = int(self.get_matching_xpath_count('%s//tr' % locator))
        if dont_count_last_nrows:
            rows = _rows - dont_count_last_nrows
        else:
            rows = _rows
        rowno = start_count or 2
        col = column or 1
        if only_clickable:
            text = \
                lambda row: self.get_text('%s//tr[%s]/td[%s]/a' % \
                                          (locator, row, col)) \
                    if self._is_element_present('%s//tr[%s]/td[%s]/a' % \
                                                (locator, row, col)) else None
        else:
            text = \
                lambda row: self.get_text('%s//tr[%s]/td[%s]' % \
                                          (locator, row, col)) \
                    if self._is_element_present('%s//tr[%s]/td[%s]' % \
                                                (locator, row, col)) else None
        try:
            while rowno <= rows:
                _found = text(rowno)
                if _found:
                    _names.append(_found)
                rowno += 1
            if not any(_names):
                self._info('No elements: %s' % _names)
                return []
            self._info('List of elements: %s' % _names)
            return _names
        except guiexceptions.SeleniumClientException as ex:
            self._warn(ex)

    def _set_input_value_with_javascript(self, input_id, value):
        """
        Sets the value of input. Should be used to work with hidden inputs
        since input_text method in selenium2Library does not allow to work
        with invisible elements

        Parameters:
        - `input_id`: Locator of input. Mandatory.
        - `value`: Value to set. Mandatory.

        """
        self._info(
            'Performing little hack: setting value "%s" in input with id="%s"' % \
            (value, input_id))

        self.execute_javascript(
            'window.document.getElementById("%s").value = "%s"' % \
            (input_id, value))

    def setup_selenium_environment(self):
        """Generates a Firefox profile directory for the DUT and starts
           Selenium RC using this profile directory.
        """
        if self._server_host == 'localhost':
            self._debug('_ff_profile is %s' % (self._ff_profile,))
            if self._ff_profile is None:
                # generate Firefox profile
                self._ff_profile = FirefoxProfile()
                self._ff_profile.generate()
                # self.start_selenium_server('-firefoxProfileTemplate',
                #        self._ff_profile.directory)
        else:
            # nothing to do with remote servers
            pass

    def teardown_selenium_environment(self):
        """Removes Firefox profile directory and stops Selenium RC.
        """
        # stop local selenium server, nothing to do with remote ones
        if self._server_host == 'localhost':
            self.close_all_browsers()
            if self._ff_profile is not None:
                self._ff_profile.remove()
            # destroying FirefoxProfile object
            self._ff_profile = None

    def launch_dut_browser(self, url=None, dut_browser=None, dut_version=None, protocol='https', autodownload=None, download_folder=None):
        """Launches Firefox browser directed at DUT's url, sets up Selenium
           RC speed, and maximize browser window.
        """
        # default delay for selenium operations
        delay = self._DEFAULT_SELENIUM_DELAY
        # by default HTTPS protocol is going to be used with local Selenium RC

        if protocol == 'http':
            UnsetHttps(self.dut, self.dut_version).unset_https()
        if url:
            # check if only port is given
            if isinstance(url, int) or re.match(r'\d+', url):
                hostname = self.dut
                port = int(url)
            else:
                # full url is given
                # Pattern groups: # 1: protocol - (https?|ftp) # 2: hostname - ([a-zA-Z0-9.]+)
                # 3: optional colon if port is given - (:)?  # 4: port or '' if not given - ((?(3))\d*)
                url_pattern = r'(https?|ftp)://([a-zA-Z0-9.-]+)(:)?((?(3))\d*)'
                url_matched = re.match(url_pattern, url)
                if url_matched:
                    protocol, hostname, port = url_matched.group(1, 2, 4)
                    if port == '':
                        port = self._get_default_dut_port(protocol.lower())
                    else:
                        port = int(port)
                    self.dut_url = url
                else:
                    raise ValueError('%s is not a correct URL!' % (url,))
        else:
            # no url is given, use defaults
            hostname = self.dut
            port = self._get_default_dut_port(protocol)

        # add certificate exception if HTTPS is used
        dut_version = dut_version or self.dut_version
        if protocol.lower() == 'https':
            try:
                # self._ff_profile.add_certificate(hostname, dut_version, port)
                pass
            except RuntimeError:
                # certificate can't be retrieved from the appliance try to use HTTP instead
                protocol = 'http'
                # if custom port is specified use it for HTTP, connection instead of default port
                if port == self._get_default_dut_port('https'):
                    # default port was used for HTTPS, use default for HTTP
                    port = self._get_default_dut_port(protocol)

        # construct DUT URL
        self.dut_url = '%s://%s:%s' % (protocol, hostname, port)

        # get robot variables
        try:
            robot_vars = common.Variables.get_variables()
            # update default values
            if robot_vars:
                if robot_vars.has_key('${DELAY}'):
                    delay = robot_vars['${DELAY}']
                if robot_vars.has_key('${DUT URL}'):
                    self.dut_url = robot_vars['${DUT URL}']
        except:
            # robot variables are not accessible when WsaGuiLibrary is used in #standalone mode.
            # Default values for delay and dut_url is used
            pass
        self._retry_dut_login(self.dut_url, dut_browser, delay, autodownload, download_folder)

    def get_firefox_profile_directory(self):
        """Returns current firefox profile directory location"""
        return self._ff_profile.directory

    def log_into_dut(self, user=None, password=None, passcode=None, **kwargs):
        """Performs logging into DUT using specified user and password
           credential and disable certificate pop up from displaying
           it in future logins.

        Parameters:
           - `user`: name of authorized user
           - `password`: password of authorized user
           - `passcode`: passcode if 2FA is enabled
           - `disable_demo_certificate_popup`: True if no further demo certificate should be displayed, else False

        If user and password are not set
            and if Login as admin/ironport fails
        Then Login as ${DUT_ADMIN}/${DUT_ADMIN_SSW_PASSWORD}
        """
        if user and password:
            if passcode:
                self._log_into_dut_int(user, password, passcode, **kwargs)
            else:
                self._log_into_dut_int(user, password, **kwargs)
            return

        variables = common.Variables.get_variables()

        user = 'admin'
        if "${DUT_ADMIN}" in variables:
            password = variables["${DUT_ADMIN}"]

        password = Misc(None, None).get_admin_password(self.dut)
        self._log_into_dut_int(user, password, **kwargs)

    def reset_passphrase_expiry_reminder_from_gui(self):
        """
        Resets expired passphrase from gui

        Parameters: None
        Usage : Reset Passphrase Expiry Reminder From Gui
        """

        change_passphrase_text = "Change Passphrase"
        old_password_element_locator = "//input[@name='old_pwd']"
        new_password_element_locator = "//input[@id='passwdv']"
        retype_password_element_locator = "//input[@name='repasswd']"
        change_password_locator = "//div[@id='banner_alert']/div/a"
        submit_button = "//*[@value='Submit']"
        banner_msg_locator = "//div[@id='banner_alert']"
        banner_msg_text = "Your local password will expire on"
        self._wait_until_text_is_present(banner_msg_text, timeout=30)
        banner_msg = self._get_text(banner_msg_locator)
        self._info("Banner message seen: %s" % banner_msg)

        banner_alert = 'Your local password will expire on'
        if self._is_text_present(banner_alert):
            self._info("Inside Change Passphrase")
            self.click_element(change_password_locator)
            # Wait for text Change passphrase appears
            self._wait_until_text_is_present(change_passphrase_text, timeout=30)
            # Get the old password set using get_admin_password
            old_password = Misc(None, None).get_admin_password(self.dut)
            # Set new password as old password itself
            new_password = old_password
            # Set the old and new password to respective fields
            self.input_text(old_password_element_locator, text=old_password)
            self.input_text(new_password_element_locator, text=new_password)
            self.input_text(retype_password_element_locator, text=new_password)
            # Click submit button after making the changes
            self.click_button(submit_button)

    def reset_expired_passphrase_from_gui(self):
        """ Resets expired passphrase from gui
        Parameters: None
        Usage : Reset Expired Passphrase From Gui  """

        change_passphrase_text = "Change Passphrase"
        old_password_element_locator = "//input[@name='old_pwd']"
        new_password_element_locator = "//input[@id='passwdv']"
        retype_password_element_locator = "//input[@name='repasswd']"

        self.log_into_dut()
        self._wait_until_text_is_present(change_passphrase_text, timeout=30)
        old_password = Misc(None, None).get_admin_password(self.dut)
        new_password = old_password
        self.input_text(old_password_element_locator, text=old_password)
        self.input_text(new_password_element_locator, text=new_password)
        self.input_text(retype_password_element_locator, text=new_password)
        self._click_submit_button()

    def configure_pac_for_browser(self, pacurl):
        """Configures browser for auto proxy via a pacurl
           followings:
              - stop all current running web browser.
              - create a prefs.js file in existing Firefox profile directory.
              - updated Firefox profile will be used when new browser starts.

        Parameters:
            - `pacurl`: a string with the URL of the form:
                      http://wsa216-p1.wga:9001/new.pac
                      http://ipv6_address_of_p1_interface/new.pac

           Example:
           | Configure Pac For Browser | http://ipv6_address_of_p1_interface/new.pac |
        """
        self.close_browser()
        self._info('Delaying 5 seconds to allow Selenium RC to shutdown')
        time.sleep(5)
        try:
            os.remove(self.prefs_js_path)  # just in case
        except:
            pass  # not a problem if no prefs previously in effect
        self._create_prefs_js_pac(pacurl)
        self._info('Delaying 5 seconds to allow Selenium RC to come up')
        # prove pref.js changed based on debug
        self._debug(open(self.prefs_js_path).read())
        time.sleep(5)

    def configure_proxy_for_browser(self, conf):
        """Configures browser to proxy request through DUT by doing the
           followings:
              - stop all current running web browser.
              - create a prefs.js file in existing Firefox profile directory.
              - updated Firefox profile will be used when new browser starts.

        Parameters:
            - `conf`: proxy configuration which is either a string of comma
                      separated or a list of the following item:

                         'protocol:dut_name:port'

                      where:

                      'protocol': either 'http', 'ssl', or 'ftp'.
                      'dut_name': name of DUT.
                      'port': port

           Example:
           | Configure Proxy For Browser | http:mywsa.wga:80, ssl:mywsa.wga:80, ftp:mywsa.wga:80 |
        """
        self.close_browser()
        self._info('Delaying 5 seconds to allow Selenium RC to shutdown')
        time.sleep(5)
        conf = ArgumentParser()._convert_to_tuple(conf)
        self._create_prefs_js(conf)
        self._info('Delaying 5 seconds to allow Selenium RC to come up')
        time.sleep(5)

    def remove_proxy_from_browser(self):
        """Removes proxy configuration from browser by doing the
           followings:
              - stop all current running web browser.
              - delete prefs.js file from existing Firefox profile directory.
              - no need to restart Selenium RC again, updated Firefox profile
                will be used when new browser starts.

           Example:
           | Remove Proxy From Browser |
        """
        self.close_browser()
        self._info('Delaying 5 seconds to allow Selenium RC to shutdown')
        time.sleep(1)
        try:
            os.remove(self.prefs_js_path)
        except:
            self._info(str(sys.exc_info()))
        self._info('Delaying 5 seconds to allow Selenium RC to come up')
        time.sleep(1)

    def is_editable(self, locator):
        locator = self._modify_locator(locator)
        return self._is_editable(locator)

    def is_checked(self, locator):
        locator = self._modify_locator(locator)
        return self._is_checked(locator)
