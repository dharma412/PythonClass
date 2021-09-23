#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/clients/cres.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import os
import socket

try:
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver import Firefox, FirefoxProfile
except ImportError:
    class Firefox(object):
        pass


    print ('Please update your Python Selenium library in order ' \
          'to use CRES Client keywords')

from cres_def.login_form import LoginForm
from cres_def.provisioning_form import ProvisioningForm

LOGIN_BUTTON = "//input[@name='continuebtn']"
MENU_ITEM = lambda name: "//a[normalize-space()='%s']" % (name,)
CREATE_ACCOUNT_BUTTON = "//input[@value='Create Account']"
ERR_MSG_CELL = "//td[@class='errorMessageCell']"


class FirefoxWebdriverWrapper(Firefox):
    def __init__(self):
        super(FirefoxWebdriverWrapper, self).__init__(self._get_configured_ff_profile())
        self.implicitly_wait(10)
        self.maximize_window()

    def _get_configured_ff_profile(self):
        customized_profile = FirefoxProfile()
        ext_path = os.path.join(os.getenv('SARF_HOME'),
                                'tests/testdata/xpi',
                                'mitm_me_cert_error_bypass-2.1.110513-fx.xpi')
        customized_profile.add_extension(ext_path)
        customized_profile.accept_untrusted_certs = True
        customized_profile.assume_untrusted_cert_issuer = True
        return customized_profile

    def input_text(self, locator, value):
        elem = self.find_element_by_xpath(locator)
        elem.send_keys(value)

    def click(self, locator):
        elem = self.find_element_by_xpath(locator)
        elem.click()

    def get_text(self, locator):
        elem = self.find_element_by_xpath(locator)
        return elem.text

    def get_value(self, locator):
        elem = self.find_element_by_xpath(locator)
        return elem.value_of_css_property('value')


class CRESGUIClient(object):
    def __init__(self, host, username, password):
        self._host = host
        self._username = username
        self._password = password

        self._gui = FirefoxWebdriverWrapper()
        self._login()

    @property
    def login_url(self):
        return 'https://%s/websafe/login.action' % \
               (socket.gethostbyname(self._host),)

    @property
    def host(self):
        return self._host

    def _is_logged_in(self):
        return (len(self._gui.title) > 0) and (self._gui.title != 'Login')

    def _get_login_form_controller(self):
        if not hasattr(self, '_login_form_controller'):
            self._login_form_controller = LoginForm(self._gui)
        return self._login_form_controller

    def _get_provisioning_form_controller(self):
        if not hasattr(self, '_provisioning_form_controller'):
            self._provisioning_form_controller = ProvisioningForm(self._gui)
        return self._provisioning_form_controller

    def _login(self):
        if self._is_logged_in():
            return
        self._gui.get(self.login_url)
        controller = self._get_login_form_controller()
        for _ in range(3):
            controller.set({'Name': self._username,
                            'Password': self._password})
            self._gui.click(LOGIN_BUTTON)
            if self._is_logged_in():
                break
        if not self._is_logged_in():
            raise ValueError('Failed to log in to CRES server %s with ' \
                             'given username and password' % (self._host,))

    def _verify_provisioning_result(self, should_raise_if_acc_exists):
        try:
            err_cell = self._gui.find_element_by_xpath(ERR_MSG_CELL)
        except NoSuchElementException:
            return
        if err_cell:
            action_result = err_cell.text
            acceptable_descriptions = ('exists already', 'Provisioning Failed')
            if any(map(lambda x: action_result.find(x) >= 0, acceptable_descriptions)) and \
                    not should_raise_if_acc_exists:
                return
            else:
                raise AssertionError(action_result)

    def provision_account(self, info, should_raise_if_acc_exists=False):
        self._login()

        self._gui.click(MENU_ITEM('Provision Account'))
        controller = self._get_provisioning_form_controller()
        info.update({'Administrator Username': self._username})
        controller.set(info)
        self._gui.click(CREATE_ACCOUNT_BUTTON)
        self._verify_provisioning_result(should_raise_if_acc_exists)

    def close(self):
        self._gui.close()
        self._gui.quit()
