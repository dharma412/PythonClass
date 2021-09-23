#!/usr/bin/env python
#$Id: //prod/main/sarf_centos/testlib/zeus1380/gui/csdl/xpath_update.py#1 $

import re
import time

from common.gui.guicommon import GuiCommon
from credentials import DUT_ADMIN, DUT_ADMIN_PASSWORD, DUT_ADMIN_SSW_PASSWORD
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from sal.clients.crawler import ApplianceCrawler
from bs4 import BeautifulSoup
import requests

#XpathS and variables

LOGIN_URL= lambda protocol, hostname: '%s://%s/login   ' % (protocol, hostname)
DEFAULT_PATH = lambda protocol, hostname: '%s://%s' % (protocol, hostname)
LOGIN_XPATH = "//input[@value='Login']"
NEWLOGIN_XPATH = "//input[@value='NewLogin']"
DEMO_OK = '//*[@type="button" and contains(text(), "OK")]'
TAB_XPATH = lambda tab: "//a[contains(text(),'%s') "\
             "and contains(@class, 'yuimenubaritemlabel-hassubmenu')]" % (tab)
LINK_XPATH = lambda tab_link:"//a[starts-with(@href, 'http') and "\
              "contains(text(), '%s')]" % (tab_link)
INTERFACE_LINK = "//table[@class='cols']//tr[2]/td[1]/a"
SUBMIT_BTN = "//input[@value='Submit']"
ERR_XPATH = "//*[contains(text(),'Error')]"
HOME_LOCATOR = "//div[@id='yui-navbar']/ul/li[1]/a/img"
CONFIGURATION_MENU = "//*[@id='yui-navbar']/ul/li[4]/div/div[2]/ul[3]/li[5]"
SAVE_OPERATION = "//input[@id='save_operation_id']"
SUCCESS_XPATH = "//*[contains(text(),'Success')]"

class XpathUpdate(GuiCommon):
    """Keywords for interaction with "cssm GUi"."""

    def get_keyword_names(self):
        return ['change_name_for_login_button',
                'change_id_for_login_button',
                'modify_cookies_for_dut_url',
                'remove_element_in_login_page',
                'add_element_in_login_page',
                'update_netmask_name_in_ip_interface',
                'modify_title_and_groupindex_in_configuration_file']

    def _get_protocol(self):
        if self.selenium_server_host == 'localhost':
            protocol = 'https'
        else:
            protocol = 'http'
        return protocol

    def _launch_login_page(self):
        self.browser=webdriver.Firefox()
        protocol = self._get_protocol()
        self.browser.get(LOGIN_URL(protocol, self.dut))
        self.browser.implicitly_wait(30)
        self.browser.maximize_window()

    def _click_to_login(self, btn):
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        username.send_keys(DUT_ADMIN)
        password.send_keys(DUT_ADMIN_SSW_PASSWORD)
        btn.click()

    def change_name_for_login_button(self):
        self._launch_login_page()
        submit_value = self.browser.find_element_by_xpath(LOGIN_XPATH)
        self._info("Value before update :%s" % submit_value)
        self.browser.execute_script("arguments[0].value = 'NewLogin'", submit_value)
        submit_value1 = self.browser.find_element_by_xpath(NEWLOGIN_XPATH)
        self._info("Value after update :%s" % submit_value1)
        self._click_to_login(submit_value1)
        time.sleep(5)
        try:
            self.browser.find_element_by_xpath(NEWLOGIN_XPATH)
        except:
            self.browser.close()
            return True

    def change_id_for_login_button(self):
        self._launch_login_page()
        element=self.browser.find_element_by_id("_login")
        self.browser.execute_script("arguments[0].setAttribute('id','_newlogin')", element)
        id1 = self.browser.find_element_by_id("_newlogin")
        self._info("Value after update :%s" % id1)
        self._click_to_login(id1)
        time.sleep(5)
        try:
            self.browser.find_element_by_id("_newlogin")
        except:
            self.browser.close()
            return True

    def modify_cookies_for_dut_url(self):
        s = requests.Session()
        protocol = self._get_protocol()
        url = DEFAULT_PATH(protocol, self.dut)
        r = s.get(url, verify=False)
        cookievalue = []
        a_dict = s.cookies.get_dict()
        for key, value in a_dict.items():
            s.cookies.set(key, None)
            s.cookies.set(key, 'foobar', domain=self.dut, path='/')
            cookievalue.append(value)
        r = s.get(url, verify=False)
        new_dict = s.cookies.get_dict()
        for key, value in new_dict.items():
            if value == 'foobar':
                return False
        return True

    def remove_element_in_login_page(self, elmt):
        self._launch_login_page()
        element=self.browser.find_element_by_class_name(elmt)
        self.browser.execute_script("arguments[0].remove()", element)
        id1 = self.browser.find_element_by_id("_login")
        self._click_to_login(id1)
        try:
            self.browser.find_element_by_id(elmt)
            self.browser.find_element_by_name('username')
        except:
            self.browser.close()
            return True

    def add_element_in_login_page(self, elmt):
        self._launch_login_page()
        element=self.browser.find_element_by_class_name(elmt)
        self.browser.execute_script("arguments[0].innerHTML='My Text';", element)
        id1 = self.browser.find_element_by_id("_login")
        self._click_to_login(id1)
        try:
            self.browser.find_element_by_id(elmt)
        except:
            self.browser.close()
            return True

    def _close_democert_dialog(self, navmenu):
        self._launch_login_page()
        submit_value = self.browser.find_element_by_xpath(LOGIN_XPATH)
        self._info("Value after update :%s" % submit_value)
        self._click_to_login(submit_value)
        time.sleep(3)
        try:
            demo_cert = self.browser.find_element_by_id('democert_dialog_c')
            demo_cert.click()
            demo_ok = self.browser.find_element_by_xpath(DEMO_OK)
            demo_ok.click()
        except:
            self._info("Demo_ok not found")
        tab = self.browser.find_element_by_xpath(TAB_XPATH(navmenu))
        tab.click()

    def update_netmask_name_in_ip_interface(self):
        self._close_democert_dialog('Network')
        menu =  self.browser.find_element_by_xpath(LINK_XPATH('IP Interfaces'))
        menu.click()
        time.sleep(2)
        interf = self.browser.find_element_by_xpath(INTERFACE_LINK)
        interf.click()
        time.sleep(2)
        netmask = self.browser.find_element_by_name('netmask')
        self.browser.execute_script("arguments[0].setAttribute('name','netmask1')", netmask)
        submit_btn = self.browser.find_element_by_xpath(SUBMIT_BTN)
        submit_btn.click()
        time.sleep(4)
        try:
            element = self.browser.find_element_by_xpath(ERR_XPATH)
        except:
            raise AssertionError, "Could not find the element."
        finally:
            self.browser.close()

    def modify_title_and_groupindex_in_configuration_file(self):
        navmenu='System Administration'
        self._close_democert_dialog(navmenu)
        menu1_locator = self.browser.find_element_by_xpath(HOME_LOCATOR)
        ActionChains(self.browser).move_to_element(menu1_locator).perform()
        tab = self.browser.find_element_by_xpath(TAB_XPATH(navmenu))
        tab.click()
        time.sleep(1)
        menu =  self.browser.find_element_by_xpath(LINK_XPATH('Configuration File'))
        menu.click()
        tab = self.browser.find_element_by_xpath(TAB_XPATH(navmenu))
        tab.click()
        time.sleep(2)
        grpindex_tab = self.browser.find_element_by_xpath(CONFIGURATION_MENU)
        grpindex1 = grpindex_tab.get_attribute("groupindex")
        self.browser.execute_script("arguments[0].setAttribute('groupindex','1')", grpindex_tab)
        grpindex2 = grpindex_tab.get_attribute("groupindex")
        if grpindex1 == grpindex2:
            raise AssertionError, "groupindex not updated"
        time.sleep(2)
        title = self.browser.find_element_by_tag_name("title")
        self.browser.execute_script("arguments[0].innerHTML='New Text'", title)
        time.sleep(7)
        if 'Text' not in self.browser.title:
            raise AssertionError, "Title not updated"
        radio_button = self.browser.find_element_by_xpath(SAVE_OPERATION)
        ActionChains(self.browser).move_to_element(radio_button).perform()
        try:
             radio_button.click()
        except:
             self.browser.execute_script("arguments[0].click()", radio_button)
             self._info("Radio button click with exception")
        time.sleep(1)
        submit_btn = self.browser.find_element_by_xpath(SUBMIT_BTN)
        submit_btn.click()
        time.sleep(1)
        try:
            element = self.browser.find_element_by_xpath(SUCCESS_XPATH)
            tab = self.browser.find_element_by_xpath(TAB_XPATH(navmenu))
            tab.click()
            grpindex_tab = self.browser.find_element_by_xpath(CONFIGURATION_MENU)
            grpindex3 = grpindex_tab.get_attribute("groupindex")
            if grpindex3 != grpindex1:
                raise AssertionError, "groupindex not restored"
        except:
            raise AssertionError, "Could not find the element."
        finally:
            self.browser.close()
