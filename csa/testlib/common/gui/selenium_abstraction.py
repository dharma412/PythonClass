#!/usr/bin/env python

# $Id: //prod/main/sarf_centos/testlib/common/gui/selenium_abstraction.py#2 $
# $DateTime: 2019/06/11 06:52:26 $
# $Author: revlaksh $

"""
The script provides a wrapper for different versions of Selenium Libraries:
    SeleniumLibrary and Selenium2Library
Name of the wrapper class:WrappedSeleniumLibrary

WrappedSeleniumLibrary is designed to inherit identical methods from different
versions of Selenium Libraries and provide wrappers for methods that do not
exist in some or all versions.

Example1. method _is_element_present exists in Selenium2Library, but does not
exist in SeleniumLibrary. It's added to WrappedSelenium1Library class


Example2. method _set_run_on_failure exists in SeleniumLibrary, but does not
exist in Selenium2Library. It's added to WrappedSelenium2Library class

Example3. method _is_editable does not exist in Selenium2Library and
SeleniumLibrary. It's added to both WrappedSelenium1Library and
WrappedSelenium21Library
"""
import re
import time

from common.logging import Logger

try:
    from SeleniumLibrary import SeleniumLibrary, __version__

    print "SeleniumLibrary version:", __version__
    if __version__[0] == '3':
        SELENIUM_LIBRARY_VERSION = '3'
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys
        from selenium.common.exceptions import NoSuchElementException
        from selenium.webdriver.support.ui import Select
        from selenium.webdriver import ChromeOptions

        # from SeleniumLibrary import SeleniumLibrary
        # RunOnFailure = SeleniumLibrary.failure_occurred
except ImportError:
    from Selenium2Library import Selenium2Library as SeleniumLibrary

    SELENIUM_LIBRARY_VERSION = '2'
    from Selenium2Library.keywords.keywordgroup import KeywordGroup as RunOnFailure
    from selenium.webdriver.support.ui import Select
    from selenium.common.exceptions import NoSuchElementException

class WrappedSelenium1Library(SeleniumLibrary):
    """ Wrapper for SeleniumLibrary
    """

    _DEFAULT_SELENIUM_DELAY = 1

    # NOT sure is these definitions are really required
    # need to check !

    def _is_element_present(self, locator):
        return self._selenium.is_element_present(locator)

    def _is_checked(self, locator):
        return self._selenium.is_checked(locator)

    def _is_visible(self, locator):
        if self._is_element_present(locator):
            return self._selenium.is_visible(locator)
        else:
            return False

    def _is_text_present(self, text):
        return self._selenium.is_text_present(text)

    def _click_button(self, locator, dont_wait=''):
        return super(WrappedSelenium1Library, self).click_button(locator, dont_wait=dont_wait)

    def _get_text(self, locator):
        """
        returns clipped text of a specified locator
        """
        return str(self._selenium.get_text(locator).encode('utf-8')).strip()

    def _drag_and_drop_to_object(self, source_locator, destination_locator):
        """Wrapper of Selenium method drag_and_drop_to_object.
        Drags and drops one element onto another one

        Parameters:
         - source_locator: locator of an element to be dragged
         - destination_locator: locator of an element on which the source element
        will be dropped
        """
        self._selenium.drag_and_drop_to_object(source_locator, destination_locator)

    def assign_id_to_element(self, locator, id):
        """Assigns a temporary identifier to element specified by `locator`.

        This is mainly useful if the locator is complicated/slow XPath expression.
        Identifier expires when the page is reloaded.

        New in SeleniumLibrary 2.7.

        Example:
        | Assign ID to Element | xpath=//div[@id="first_div"] | my id |
        | Page Should Contain Element | my id |
        """
        self._info("Assigning temporary id '%s' to element '%s'" % (id, locator))
        self._selenium.assign_id(self._parse_locator(locator), id)

    def _window_focus(self):
        self._selenium.window_focus()

    def _get_all_fields(self):
        return self._selenium.get_all_fields()

    def _get_table_cell(self, tableCellAddress):
        return self._selenium.get_table(tableCellAddress)

    def _is_editable(self, locator):
        return self._selenium.is_editable(locator)

    def _get_selected_label(self, selectLocator):
        """
        Gets option label(visible text) for selected option
        in the specified select element.

        Parameters:
        - `selectLocator` - an element locator identifying a drop-down menu.

        Return:
        Text of currently selected drop-down option. String.
        """
        return self._selenium.get_string("getSelectedLabel",
                                         [selectLocator, ])

    def _get_attribute(self, attributeLocator):
        return self.get_attribute(attributeLocator)

    def open_window(self, url, windowID):
        """
        Opens a popup window (if a window with that ID isn't already open).
        After opening the window, you'll need to select it using the Select Window
        command.
        """
        self._selenium.open_window(url, windowID)

    def _get_select_options(self, selectLocator):
        return self.get_select_options(selectLocator)

    def get_select_values(self, locator):
        """Returns the text value of elements identified by `locator`.
        See `introduction` for details about locating elements.
        """
        return self._get_all_texts(locator)

    def _get_all_texts(self, locator):
        elements = self._element_find(locator, False, True)
        texts = []
        for element in elements:
            txt = element.text
            if element is not None:
                texts.append(txt.rstrip())
        self._info(texts)
        return texts[0] if texts else None

    def _find_elements(self, locator):
        try:
            elements = self._element_find(locator, False, True)
            return elements
        except:
            return None

    def _get_element_id(self, locator):
        element = self._element_find(locator, True, True)
        return element.get_attribute('id') if element is not None else None

    def _get_element_value(self, locator):
        element = self._element_find(locator, True, True)
        return element.get_attribute('value') if element is not None else None


class WrappedSelenium2Library(SeleniumLibrary):
    """ Wrapper for Selenium2Library
    """

    _DEFAULT_SELENIUM_DELAY = 0.5

    def __init__(self, timeout, server_host, run_on_failure):

        super(WrappedSelenium2Library, self).__init__(timeout=timeout, run_on_failure=run_on_failure)

        self._server_host = server_host or 'localhost'
        # self._server_port = int(server_port or 4444)
        # self._jar_path = jar_path
        self._ff_profile = None

    def _set_run_on_failure(self, run_on_failure):
        self.register_keyword_to_run_on_failure(run_on_failure)

    def _get_run_on_failure_name(self):
        if not self._run_on_failure_keyword:
            return 'No keyword'
        return self._run_on_failure_keyword.replace('_', ' ').title()

    def start_selenium_server(self, *params):
        pass

    def stop_selenium_server(self):
        self.close_all_browsers

    def open_browser(self, url, browser='firefox', alias=None, remote_url=False,
                     desired_capabilities=None, ff_profile_dir=None):

        # ff_profile_dir = ff_profile_dir or self._ff_profile.directory
        super(WrappedSelenium2Library, self).open_browser(url,
                                                          browser=browser,
                                                          alias=alias,
                                                          remote_url=remote_url,
                                                          desired_capabilities=desired_capabilities,
                                                          ff_profile_dir=ff_profile_dir
                                                          )

    @property
    def _selenium(self):
        return self._cache.current

    def _click_button(self, locator, dont_wait=''):
        try:
            element = self._element_find(locator, True, True)
            self._debug('Element %s Found [%s]' % (element, locator))
            element_type = element.get_attribute("type")
            self._debug('Element Type: %s' % element_type)
            element_tag_name = element.tag_name
            self._debug('Element Tag Name: %s' % element_tag_name)
            if self._is_visible(locator):
                if element.is_displayed():
                    if element.is_enabled():
                        if element_type == "button" or element_type == "submit":
                            super(WrappedSelenium2Library, self).click_button(locator)
                        else:
                            if element_tag_name == "a":
                                self.click_link(locator)
                            else:
                                self.click_element(locator)
                    else:
                        self._warn('Element %s is NOT enabled' % locator)
                else:
                    self._warn('Element %s is NOT displayed' % locator)
            else:
                self._warn('Element %s is NOT visible' % locator)
        except:
            raise

    def _is_checked(self, locator):
        return self._element_find(locator, True, True).is_selected()

    def click_element(self, locator, dont_wait=''):
        super(WrappedSelenium2Library, self).click_element(locator)

    def click_link(self, locator, dont_wait=''):
        super(WrappedSelenium2Library, self).click_link(locator)

    def select_from_list(self, locator, *values):
        locator = self._modify_locator(locator)
        values_list = []
        WARNING_MSG = 'Method select_from_list was modified in Selenium2Library\n' + \
                      'Please consider updating your code\n'
        for value in values:
            new_value = value
            if value.startswith('label='):
                if value.startswith('label=glob:'):
                    new_value = value[11:]
                    new_value = value[11:].rstrip('*')
                else:
                    new_value = value[6:]

            if value.startswith('value='):
                new_value = value[6:]

            if new_value != value:
                self._warn(WARNING_MSG + 'value was modified from "%s" to "%s"' %
                           (value, new_value))

            values_list.append(new_value)

        super(WrappedSelenium2Library, self).select_from_list(locator, *values_list)

    def go_to(self, url):
        if url.startswith('/'):
            # process relative path
            current_url = self.get_location()

            url_pattern = r'(https?|ftp)://([^/]+)/(.*)'
            matched = re.match(url_pattern, current_url)
            if not matched:
                raise ValueError('Failed to parse current url')

            protocol, hostname, path = matched.group(1, 2, 3)
            new_url = '%s://%s/%s' % (protocol, hostname, url[1:])
            self._info('URL was modified from "%s" to "%s"' % (url, new_url))
            url = new_url

        super(WrappedSelenium2Library, self).go_to(url)

    def wait_until_page_loaded(self, timeout=None):
        pass

    def _drag_and_drop_to_object(self, source_locator, destination_locator):
        """Drags and drops one element onto another one

        Parameters:
         - source_locator: locator of an element to be dragged
         - destination_locator: locator of an element on which the source element
        will be dropped
        """

        self.drag_and_drop(source_locator, destination_locator)

    def _window_focus(self):
        pass

    def capture_screenshot(self, filename='selenium-screenshot-{index}.png'):
        super(WrappedSelenium2Library, self).capture_page_screenshot(filename=filename)

    def _get_all_fields(self):
        """Returns a list containing ids of all inputs found in current page.
        If a input has no id, an empty string will be in the list instead.
        """
        fields = []
        for anchor in self._element_find("tag=input", False, False, 'input'):
            fields.append(anchor.get_attribute('id'))
        return fields

    def _get_table_cell(self, table_cell_address):
        self._info('_get_table_cell is deprecated, use get_table_cell instead' + \
                   ' but notice that rows and columns starts from 1 in get_table_cell' + \
                   ' and before numeration was from 0')
        self._debug('table_cell_address is "%s"' % (table_cell_address,))

        # in selenium get_table rows and columns starts at 0
        # same in SARF _get_table_cell
        # in get_table_cell rows and columns starts at 1

        addr = table_cell_address.split('.')
        locator = '.'.join(addr[:-2])
        row = int(''.join(addr[-2:-1])) + 1
        col = int(''.join(addr[-1:])) + 1
        self._debug('running get_table_cell("%s", %s, %s)' % (locator, row, col))

        return self.get_table_cell(locator, row, col)

    def _is_editable(self, locator):
        locator = self._modify_locator(locator)
        return self._is_enabled(locator)

    def _get_selected_label(self, selectLocator):
        selectLocator = self._modify_locator(selectLocator)
        return self.get_selected_list_label(selectLocator)

    def _get_attribute(self, attributeLocator):
        attributeLocator = self._modify_locator(attributeLocator)
        return super(WrappedSelenium2Library, self). \
            get_element_attribute(attributeLocator)

    def _get_select_options(self, selectLocator):
        selectLocator = self._modify_locator(selectLocator)
        return super(WrappedSelenium2Library, self). \
            _get_select_list_options(selectLocator)

    def open_window(self, url, windowID):
        """
        Opens a popup window (if a window with that ID isn't already open).
        After opening the window, you'll need to select it using the Select Window
        command.
        """

        self.execute_javascript(
            'window.open("%s", "%s");' % \
            (url, windowID))

    def get_select_values(self, locator):
        """Returns the text value of elements identified by `locator`.
        See `introduction` for details about locating elements.
        """
        return self._get_all_texts(locator)

    def _get_all_texts(self, locator):
        locator = self._modify_locator(locator)
        elements = self._element_find(locator, False, True)
        texts = []
        for element in elements:
            txt = element.text
            if element is not None:
                texts.append(txt.rstrip())
        self._info(texts)
        return texts[0] if texts else None

    def _find_elements(self, locator):
        try:
            locator = self._modify_locator(locator)
            elements = self._element_find(locator, False, True)
            return elements
        except:
            return None

    def _get_element_id(self, locator):
        locator = self._modify_locator(locator)
        element = self._element_find(locator, True, True)
        return element.get_attribute('id') if element is not None else None

    def _get_element_value(self, locator):
        locator = self._modify_locator(locator)
        element = self._element_find(locator, True, True)
        return element.get_attribute('value') if element is not None else None

    def _modify_locator(self, locator):
        self._debug('Locator: %s' % locator)
        if re.search(r'^xpath', locator):
            temp = locator.split('xpath=')
            index = 1 if len(temp) > 1 else 0
            locator = temp[index]
        if re.search(r'/$', locator):
            locator = locator.rstrip('/')
        self._debug('Modified Locator: %s' % locator)
        return locator

    def select_from_dropdown_list(self, locator, value):
        if value is not None:
            try:
                if self._is_visible(locator):
                    if self._is_editable(locator):
                        select = Select(
                            self._selenium.find_element_by_xpath(locator))
                        if select:
                            try:
                                select.select_by_visible_text(value)
                            except NoSuchElementException as e:
                                self._warn(
                                    'Element with value [%s] not found' % value)
                                raise e
                        else:
                            self._warn('No elements found with Xpath %s' % locator)
                    else:
                        self._warn(
                            'Element with Xpath %s is not editable' % locator)
                else:
                    self._warn('Element with Xpath %s is not visible' % locator)
            except NoSuchElementException as e:
                self._warn('Wrong Xpath [%s] provided' % locator)
                raise e
        else:
            self._warn('EMPTY value provided for XPATH %s' % locator)


class WrappedSelenium3Library(SeleniumLibrary, Logger):
    _DEFAULT_SELENIUM_DELAY = 1

    def __init__(self, timeout, server_host, run_on_failure):
        # Need to add screenshot_root_directory
        super(WrappedSelenium3Library, self).__init__(timeout=timeout, run_on_failure=run_on_failure)
        self._server_host = server_host or 'localhost'
        self._ff_profile = None
        self.session_name = None

    def _set_current_session(self):
        print "sess curent", self._cache.current
        resolve_index = 0
        try:
            resolve_index = self._cache._resolve_alias(self.session_name)
        except Exception:
            pass

        if self.session_name:
            if int(self._cache.current_index) != int(resolve_index):
                try:
                    self._cache.switch(self.session_name)
                except RuntimeError as error:
                    raise (error)
            else:
                print "Session exists"

    @property
    def _selenium(self):
        return self._cache.current

    @property
    def _s2l(self):
        try:
            return self
        except AttributeError:
            raise

    def _open_browser(self, dut_url, browser, alias,autodownload=None,download_folder=None):
        desired_capabilities = {}
        disable_insecure_cert = ['chrome', 'opera']
        
        if browser in disable_insecure_cert:
            desired_capabilities = {"acceptInsecureCerts": True, 'acceptSslCerts':True}   
            if autodownload and browser.lower() == 'chrome':
                chrome_options = {}
                options = ChromeOptions()
                self._info('Setting Auto download options for Chrome browser')
                prefs = self._set_chrome_pref(download_folder)
                options.add_experimental_option('prefs', prefs)
                chrome_options = options.to_capabilities()
                desired_capabilities.update(chrome_options)
        self.open_browser(dut_url, browser=browser, alias=alias, desired_capabilities=desired_capabilities)
        self._set_current_session()
    
    def _set_chrome_pref(self, download_folder):
            return {"download.default_directory": download_folder,
                     "profile.default_content_setting_values.automatic_downloads": 2,
                     "plugins.always_open_pdf_externally": True,
                     "plugins.plugins_disabled": ["Chrome PDF Viewer"],
                     "download.prompt_for_download": False,
                     "download.directory_upgrade": True,
                     "safebrowsing.enabled": False,
                     "safebrowsing.disable_download_protection": True,
                     "profile.default_content_setting_values.automatic_downloads": 1,
                     "download.extensions_to_open": "text/csv,application/pdf,application/xml,text/xml"}
        
    def _click_button(self, locator, dont_wait=''):
        # need to handle dont wait
        self.click_button(locator)

    def get_current_session(self):
        return self.session_name

    def switch_session(self, session_name):
        pass

    def _is_visible(self, locator):
        return self._is_element_present(locator)

    def _is_element_present(self, locator):
        try:
            self.element_should_be_visible(locator)
            return True
        except Exception:
            return False

    def _is_text_present(self, text):
        try:
            status = self.page_should_contain(text)
            return True
        except Exception:
            return False

    def _get_text(self, locator):
        """
        returns clipped text of a specified locator
        """
        return str(self.get_text(locator).encode('utf-8')).strip()

    def _is_checked(self, locator):
        return self.find_element(locator).is_selected()

    def parse_modifier(self, modifier):
        modifier = modifier.upper()
        modifiers = modifier.split('+')
        keys = []
        for item in modifiers:
            item = item.strip()
            item = self._parse_aliases(item)
            if hasattr(Keys, item):
                keys.append(getattr(Keys, item))
            else:
                raise ValueError("'%s' modifier does not match to Selenium Keys"
                                 % item)
        return keys

    def _parse_aliases(self, key):
        if key == 'CTRL':
            return 'CONTROL'
        if key == 'ESC':
            return 'ESCAPE'
        return key

    def _click_with_modifier(self, locator, tag, modifier):
        self._info("Clicking %s '%s' with %s." % (tag if tag[0] else 'element', locator, modifier))
        modifier = self.parse_modifier(modifier)
        action = ActionChains(self.driver)
        for item in modifier:
            action.key_down(item)
        element = self.find_element(locator, tag=tag[0], required=False)
        if not element:
            element = self.find_element(locator, tag=tag[1])
        action.click(element)
        for item in modifier:
            action.key_up(item)
        action.perform()

    def capture_screenshot(self, filename='selenium-screenshot-{index}.png'):
        super(WrappedSelenium3Library, self).capture_page_screenshot(filename=filename)

    def click_element(self, locator, dont_wait='', modifier=False, wait_timeout=5):
        if dont_wait and dont_wait != "don't wait":
            time.sleep(wait_timeout)
        if modifier:
            self._click_with_modifier(locator, [None, None], modifier)
            return
        self._info("Clicking element '%s'." % locator)
        self.find_element(locator).click()

    def click_button(self, locator, dont_wait=''):
        try:
            element = self.find_element(locator)
            self._debug('Element %s Found [%s]' % (element, locator))
            element_type = element.get_attribute("type")
            self._debug('Element Type: %s' % element_type)
            element_tag_name = element.tag_name
            self._debug('Element Tag Name: %s' % element_tag_name)
            if self._is_visible(locator):
                if element.is_displayed():
                    if element.is_enabled():
                        if element_type == "button" or element_type == "submit":
                            self.find_element(locator).click()
                        else:
                            if element_tag_name == "a":
                                self.click_link(locator)
                            else:
                                self.click_element(locator)
                    else:
                         self._warn('Element %s is NOT enabled' % locator)
                else:
                    self._warn('Element %s is NOT displayed' % locator)
            else:
                self._warn('Element %s is NOT visible' % locator)
        except:
            raise

    def select_from_dropdown_list(self, locator, value):
        if value is not None:
            try:
                if self._is_visible(locator):
                    if self._is_editable(locator):
                        select = Select(
                            self._selenium.find_element_by_xpath(locator))
                        if select:
                            try:
                                select.select_by_visible_text(value)
                            except NoSuchElementException as e:
                                self._warn(
                                    'Element with value [%s] not found' % value)
                                raise e
                        else:
                            self._warn('No elements found with Xpath %s' % locator)
                    else:
                        self._warn(
                            'Element with Xpath %s is not editable' % locator)
                else:
                    self._warn('Element with Xpath %s is not visible' % locator)
            except NoSuchElementException as e:
                self._warn('Wrong Xpath [%s] provided:%s' % (locator, e))
                raise e
        else:
            self._warn('EMPTY value provided for XPATH %s' % locator)

    def _get_table_cell(self, table_cell_address):
        self._info('_get_table_cell is deprecated, use get_table_cell instead' + \
                   ' but notice that rows and columns starts from 1 in get_table_cell' + \
                   ' and before numeration was from 0')
        self._debug('table_cell_address is "%s"' % (table_cell_address,))
        # in selenium get_table rows and columns starts at 0
        # same in SARF _get_table_cell
        # in get_table_cell rows and columns starts at 1
        addr = table_cell_address.split('.')
        locator = '.'.join(addr[:-2])
        row = int(''.join(addr[-2:-1])) + 1
        col = int(''.join(addr[-1:])) + 1
        self._debug('running get_table_cell("%s", %s, %s)' % (locator, row, col))
        return self.get_table_cell(locator, row, col)

    def _get_selected_label(self, selectLocator):
        selectLocator = self._modify_locator(selectLocator)
        return self.get_selected_list_label(selectLocator)

    def wait_until_page_loaded(self, timeout=None):
        pass

    def _is_checked(self, locator):
        return self.find_element(locator).is_selected()

    def _is_editable(self, locator):
        locator = self._modify_locator(locator)
        try:
            self.element_should_be_enabled(locator)
            return True
        except Exception as error:
            return False

    def _get_all_fields(self):
        """Returns a list containing ids of all inputs found in current page.
        If a input has no id, an empty string will be in the list instead.
         """
        fields = []
        for anchor in self.find_elements("//input"):
            fields.append(anchor.get_attribute('id'))
        return fields

    def capture_screenshot(self, filename='selenium-screenshot-{index}.png'):
        super(WrappedSelenium3Library, self).capture_page_screenshot(filename=filename)
        
    def _drag_and_drop_to_object(self, element, target):
        """Drags and drops one element onto another one

        Parameters:
         - source_locator: locator of an element to be dragged
         - destination_locator: locator of an element on which the source element
        will be dropped
        """

        action = ActionChains(self.driver)
        source_locator = self.find_element(element)
        destination_locator = self.find_element(target)
        action.move_to_element(source_locator).pause(1).click_and_hold(source_locator).pause(1).move_by_offset(1,0).move_to_element(destination_locator).move_by_offset(1,0).pause(1).release(destination_locator).perform()

if SELENIUM_LIBRARY_VERSION == '3':
    WrappedSeleniumLibrary = WrappedSelenium3Library
elif SELENIUM_LIBRARY_VERSION == '2':
    WrappedSeleniumLibrary = WrappedSelenium2Library
else:
    WrappedSeleniumLibrary = WrappedSelenium1Library
