#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/CssmGuiLibrary.py#1 $

import re
import time

from common.gui.guicommon import GuiCommon
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

# XpathS and variables

virtual_account = ""
tab_name = ""

CSSM_LOGIN_TEXT = ".//*[contains(text(),'Log in')]"
CSSM_CLOUD_URL = "http://slexta.cloudapps.cisco.com/#/"
CSSM_LOGIN_BUTTON = "//input[@id='login-button']"
CSSM_USERNAMEFIELD = "//input[@id='userInput']"
CSSM_PASSWORDFIELD = "//input[@id='passwordInput']"
CSSM_ADD_LICENSE_BTN = "//button[contains(text(),'Add License')]"
CSSM_LICENSE_SEARCH_FIELD = "//input[@placeholder='Search Licenses']"
CSSM_LICENSE_TAGS = "//tr[contains(@ng-repeat,'licenseCollection')]/td[1]/"
REGISTER_TOKEN_WINDOW = "//h3[text()='Create Registration Token']"
NEW_VIRTUAL_ACCOUNT = "//a[@id='new-virtual-account-action']"

VIRTUAL_ACCOUNTS_TABS = "//div[@class='pool-name' and contains(text(),'" + virtual_account + "')]"
NEW_VIRTUAL_ACCOUNT_HEADER = "//h3[text()='New Virtual Account']"
LICENSE_TRANSFER_QUANTITY_FIELD = "//input[contains(@id,'mult-license-transfer-input')]"
LICENSE_TRANSFER_ALERT_POPUP = "//form[@id='lic-transfer-form']//div[contains(@id,'quantity-error')]"
EXPORT_CONTROL_AGREEMENT = "//input[@id='export-control-agreement-accept']"
NEW_LICENSE_TAG_FIELD = "//tr[contains(@ng-repeat,'new_license')]/td[1]//input"
NEW_LICENSE_QUANTITY_FIELD = "//tr[contains(@ng-repeat,'new_license')]/td[2]//input"
NEW_LICENSE_EXPIRY_FIELD = "//tr[contains(@ng-repeat,'new_license')]/td[3]//input"
EVENTLOG_TAB_ROWS = "//tbody[@id='eventlog-table-body']/tr"
GENERAL_TAB_ROWS = "//tbody[@id='prod_tokens_table']/tr"
PRODUCT_INSTANCES_TAB_ROWS = "//tbody[@id='product-table-body']/tr"
LICENSES_TAB_ROWS = "//tbody[@id='license-table-body']/tr"
PRODUCT_OVERVIEW_ROWS = "//table[@class='info-table']//tr"

EDIT_LINK = "//a[text()='Edit']"
EDIT_VIRTUAL_ACCOUNT_HEADER = "//h3[text()='Edit Virtual Account Settings']"
TRANSFER_PRODUCT_HEADER = "//h3[text()='Transfer Product Instance']"
ALERT_POPUP = "//div[contains(@class,'alert-modal-text')]"
TOASTER_POPUP = "//div[@class='toaster-icon-success']/../div[@class='toaster-text']"
POPOVER_CLOSE_BTN = "//a[@class='close-popover-btn']"
POPOVER_TRANSFER_BTN = "//a[@id='product-details-transfer-btn']"
POPOVER_REMOVE_BTN = "//a[@id='product-details-remove-btn']"
LICENSE_DELETE = "//div[text()='Licenses deleted successfully']"
PRODUCT_TRANSFER_OK_BTN = "//a[@id='product-transfer-ok-btn']"
PRODUCT_OVERVIEW_EVENTLOG_ROWS = "//table[contains(@class,'license-details-table')]/tbody/tr"


class CssmGuiLibrary(GuiCommon):
    """Keywords for interaction with "cssm GUi"."""

    def get_keyword_names(self):
        return ['cssm_launch',
                'cssm_close',
                'cssm_login',
                'navigate_to_alpha_account_page',
                'cssm_add_license',
                'cssm_delete_license',
                'cssm_generate_new_token',
                'cssm_create_virtual_account',
                'cssm_copy_token',
                'cssm_transfer_license',
                'cssm_get_table_entries',
                'cssm_get_product_overview_details',
                'cssm_get_product_overview_event_logs',
                'cssm_delete_virtual_account',
                'cssm_edit_virtual_account',
                'cssm_product_transfer']

    def cssm_launch(self):
        """
        This function would launch the cssm GUI browser. And
        checks for the login page should be displayed
        """

        try:
            self.browser = webdriver.Firefox()
            self.browser.get(CSSM_CLOUD_URL)
            self.browser.implicitly_wait(30)
            self.browser.maximize_window()
            loginpage, loginxpath = self.get_visible_element(CSSM_LOGIN_TEXT)
            if (loginpage):
                print("The CSSSM: {} has been sucessfully launched".format(CSSM_CLOUD_URL))
            else:
                raise NoSuchElementException("Failed to launch CSSSM")
        except Exception as e:
            self.cssm_close()
            raise e

    def cssm_login(self, cssm_username, cssm_password):
        """
        This Function would logs into the CSSM Browser
        provide the parameters cssm username and cssm
        password

        Parameters:
         - 'cssm_username': Cisco user id should be given
         - 'cssm_password': Cisco password ,Cisco credentials should be given
        """

        try:
            username_field = self.browser.find_element_by_xpath(CSSM_USERNAMEFIELD)
            password_field = self.browser.find_element_by_xpath(CSSM_PASSWORDFIELD)
            if (username_field):
                username_field.clear()
                time.sleep(3)
                username_field.send_keys(cssm_username)
                print("Entered username: {} on Login page".format(cssm_username))
            else:
                raise NoSuchElementException('Username field on cssm login page not displayed')
            if (password_field):
                password_field.clear()
                time.sleep(3)
                password_field.send_keys(cssm_password)
                print("Entered the password: on Login page")
            else:
                raise NoSuchElementException('password field on cssm login page not displayed')
            self.browser.find_element_by_id('login-button').click()
            print("Successfully logged into CSSM")
            self.wait_till_UI_loads("//*[text()='My Alpha Accounts']")

            # For handling multiple windows:
            self.main_window = self.browser.current_window_handle
        except Exception as e:
            print "Failed to login CSSM"
            raise e

    def navigate_to_alpha_account_page(self, alpha_account_name):
        """
        This function would navigate to the alpha account Page. Unsupported
        browser error detected which popsup only when Firefox version is below 30.
        which is handled in code in the below try catch block.

        Parameters:
         - 'alpha_account_name': ESA|WSA alpha account name should be given.which is present in alpha account
        """
        product, productxpath = self.get_visible_element("//a[text()='" + alpha_account_name + "']")
        if (product):
            print("The product is " + alpha_account_name + " is visible.Clicking on the product page")
            product.click()
            time.sleep(5)

            self.windows = self.browser.window_handles
            self.browser.switch_to_window(self.windows[1])
            time.sleep(5)
        else:
            raise NoSuchElementException("Failed to click the product link " + alpha_account_name)

        try:
            continuebutton, continuexpath = self.get_visible_element("//*[@id='continue']")
            if (continuebutton):
                print("Unsupported browser error is displayed. Clicking on continue")
                continuebutton.click()
                time.sleep(3)
        except:
            print "The browser version is supported"

    def cssm_create_virtual_account(self, virtual_account, virtualacc_desc=None):
        """
        This function would create a virtual account

        Parameters:
        - 'virtual_account': virtual account name to be created
        - 'virtualacc_desc': virtual account description
        """
        try:
            self.browser.switch_to_window(self.windows[1])
            virtual_account_add, virtual_account_xpath = self.get_visible_element(NEW_VIRTUAL_ACCOUNT)
            if (virtual_account_add):
                virtual_account_add.click()
                self.wait_till_UI_loads(NEW_VIRTUAL_ACCOUNT_HEADER)
                self._input_textfield("Name:", virtual_account)
                print ("entered the virtual account name {}".format(virtual_account))
                if virtualacc_desc is not None:
                    self._input_textfield("Description:", virtualacc_desc)
                    print ("entered the virtual account description {}".format(virtualacc_desc))
                self._click_button("Save")
                self.wait_till_UI_loads(VIRTUAL_ACCOUNTS_TABS)
                print ("Successfully created the virtual account ".format(virtual_account))
        except Exception as e:
            print ("failed to create virtual account".format(virtual_account))
            raise e

    def cssm_transfer_license(self, virtual_account, license_name, transfer_type, transfer_account, quantity):
        """
        This function would transfer the license between the virtual accounts
        Parameters:
        - 'virtual_account': virtual account name to be created
        - 'license_name': name of the license under the above virtual account
           which required to be transfer
        - 'transfer_type' : Mention the transfer type option -To|From
        - 'transfer_account' : Mention the account to which license has to be transfered to
        """
        try:
            tab_name = "Licenses"
            self.browser.switch_to_window(self.windows[1])
            time.sleep(2)
            print("Clicking on Virtual account {}".format(virtual_account))
            self._select_virtual_account(virtual_account)
            time.sleep(2)
            self.wait_till_UI_loads("//div[@id='pool-name-str' and text()='" + virtual_account + "']")
            self._click_subtabs(tab_name)
            time.sleep(2)
            license_xpath = "//a[text()='" + license_name + "']/../..//td[6]/a[text()='Transfer...']"
            self.browser.find_element_by_xpath(license_xpath).click()
            self.wait_till_UI_loads("//h3[text()='Transfer Licenses']")
            select_pooltype = Select(self.browser.find_element_by_id('license-transfer-pool-type'))
            select_pooltype.select_by_visible_text(transfer_type)
            select_poolname = Select(self.browser.find_element_by_id('license-transfer-pool-name'))
            select_poolname.select_by_visible_text(transfer_account)
            self.wait_till_UI_loads(LICENSE_TRANSFER_QUANTITY_FIELD)
            transfer_quantity_field = self.browser.find_element_by_xpath(LICENSE_TRANSFER_QUANTITY_FIELD)
            transfer_quantity_field.send_keys(quantity)
            self._click_button("OK")
            print("Successfully transfered the license from {} to {} virtual account".format(virtual_account,
                                                                                             transfer_account))
        except NoSuchElementException:
            if (self.browser.find_element_by_xpath(LICENSE_TRANSFER_ALERT_POPUP).is_displayed()):
                raise ValueError("Specified more licenses than the available.!! ")
            raise Exception("failed to transfer the license from {} to {} virtual account".format(virtual_account,
                                                                                                  transfer_account))

    def cssm_generate_new_token(self, virtual_account, description=None, expire_after=None, allow_export_ctrl=False):
        """
        This function would create a new token.
        Parameters:
        - 'virtual_account': virtual account under which new token has to be generated
        - 'description' - Description for the virtual_account mention None if not required
        - 'expire_after' - Mention number of days after which license has to get expired
        - 'allow_export_ctrl' - Mention True if export control functionality needs to be enabled
        """
        try:
            self.browser.switch_to_window(self.windows[1])
            self._select_virtual_account(virtual_account)
            time.sleep(2)
            self._click_button("New Token...")
            self.wait_till_UI_loads(REGISTER_TOKEN_WINDOW)
            if description is not None:
                self._input_textfield("Description:", description)
                print("Entered the description {} Successfully".format(description))
            if expire_after is not None:
                self._input_textfield("Expire After:", expire_after)
                print("Entered the expire after {} Successfully".format(expire_after))
            if (allow_export_ctrl):
                time.sleep(3)
                self.browser.find_element_by_xpath(EXPORT_CONTROL_AGREEMENT).click()

            self._click_button("Create Token")
            self._verify_toaster_popup()
            print "Sucessfully created the token"
        except Exception as e:
            print("Failed to generate token for virtual account {}".format(virtual_account))
            raise e

    def cssm_copy_token(self, virtual_account, created_by, description=None):
        """
        This function copies the token and returns the token value.
        if description provided it copies based on the description and virtual account
        Parameters:
        - 'virtual_account': virtual account from which token needs to be copied
        - 'created_by' - owner id who created the token
        - 'description' - provide description for copying the token[optional]
        """
        try:
            token_text = ""
            self.browser.switch_to_window(self.windows[1])
            self._select_virtual_account(virtual_account)
            time.sleep(2)
            COPYTEXT_DESCRIPRION = "//td[3][contains(text(),'" + description + "')]/../td[5][contains(text(),'" + created_by + "')]/../td[1]"
            COPYTEXT = "//td[5][contains(text(),'" + created_by + "')]/../td[1]"
            if description is not None:
                token = self.browser.find_element_by_xpath(COPYTEXT_DESCRIPRION)
            else:
                token = self.browser.find_element_by_xpath(COPYTEXT)
            time.sleep(2)
            # Since the token fetched would be unicode
            token_val = token.get_attribute('title').strip()
            print("The token {} copied successfuly ".format(token_val))
            token_text = token_val.encode('ascii', 'ignore')
            return token_text
        except Exception as e:
            print "Failed to copy token"
            raise e

    def cssm_add_license(self, productname, licensename, quantity, expirydate):
        """
        This Function would add the licenses to the product. If the license is already added
        it handles the alert popupi for the same

        Parameters:
        - 'licensename':Provide the license name which you wanted to add
        - 'quantity':Mention the quantity for the license specified
        - 'expirydate':Mention the date of expiry for the license with proper format i.e,yy-mm-dd format
        """
        try:
            self.browser.switch_to_window(self.main_window)
            time.sleep(2)
            expand_product = self.browser.find_element_by_xpath("//span[contains(text(),'" + productname + "')]/..\
            /a/span[contains(@ng-class,'show_licenses')]")

            print ("Expanding the product {} link for adding license".format(expand_product))
            if (expand_product):
                expand_product.click()
                self.wait_till_UI_loads(CSSM_ADD_LICENSE_BTN)
                add_license_button = self.browser.find_element_by_xpath(CSSM_ADD_LICENSE_BTN)
                add_license_button.click()
                time.sleep(3)
                tag_field = self.browser.find_element_by_xpath(NEW_LICENSE_TAG_FIELD)
                quantity_field = self.browser.find_element_by_xpath(NEW_LICENSE_QUANTITY_FIELD)
                expiry_field = self.browser.find_element_by_xpath(NEW_LICENSE_EXPIRY_FIELD)
                print ("Entering the value {} to Tag field".format(licensename))
                tag_field.send_keys(licensename)
                quantity_field.send_keys(quantity)
                print ("Entering the value {} to quantity field".format(quantity))
                expiry_field.send_keys(expirydate)
                print ("Entering the value {} to expirydate field".format(expirydate))

                # Click on save button provided button is enabled
                self._click_button("Save")
                time.sleep(4)
                try:
                    alert_popup = ""
                    alert_popup = self._get_alert_message()
                    if (alert_popup == "A license with the tag " + licensename + " already exists for this account"):
                        self._click_button("OK")
                        time.sleep(3)
                        print ("License already exists alert popup:{}".format(alert_popup))
                        self.browser.switch_to_window(self.main_window)
                        self._click_button("Cancel")
                except:
                    print ("Successfully added the license {}".format(licensename))
        except Exception as e:
            print("Failed to add license {}".format(licensename))
            raise e

    def cssm_delete_license(self, license_name, product_name):
        """
        This function would delete the license.

        Parameters:
        - 'license_name':Specify the license name which has to be deleted

        """

        delete_xpath = "//span[text()='" + license_name + "']/../..//td[4]/span[@tooltip='Delete License']"
        self.browser.switch_to_window(self.main_window)
        time.sleep(2)
        try:
            try:
                expand_product, expand_xpath = self.get_visible_element(CSSM_ADD_LICENSE_BTN)
                if (expand_product):
                    print("Product is already expanded proceed to delete operatoin")
                    time.sleep(3)
            except:
                already_expanded = "//span[contains(text(),'" + product_name + "')]/../a/span[contains(@ng-class,'show_licenses')]"
                productexp, productexp_xpath = self.get_visible_element(already_expanded)
                if (productexp):
                    print("Product link needs to be expanded to proceed with the delete operation")
                    productexp.click()
                    time.sleep(3)

            # type in search field for filtering license
            license_field = self.browser.find_element_by_xpath(CSSM_LICENSE_SEARCH_FIELD)
            license_field.send_keys(license_name)
            license_field.send_keys(Keys.ENTER)
            time.sleep(3)
            delobj, delxpath = self.get_visible_element(delete_xpath)
            if (delobj):
                delobj.click()
                self.wait_till_UI_loads(LICENSE_DELETE)
                print("Deleted the license {} successfully".format(license_name))
        except Exception as e:
            print("Unabe to delete the license {}".format(license_name))
            raise e

    def cssm_get_table_entries(self, virtual_account, subtab_name):
        """
        This would fetch the details of message column
        Parameters:
        - 'virtual_account':Specify the virtual_account name
        - 'subtab_name' : Mention the subtab_name under the above virtual account to get the table details
        Example:
        cssm_get_table_entries  "Default" "sample1"  "Product Instances"

        """
        try:
            table_entries = []
            self.browser.switch_to_window(self.windows[1])
            time.sleep(2)
            self._select_virtual_account(virtual_account)
            self._click_subtabs(subtab_name)
            if (subtab_name == "Event Log"):
                event_row_xpath = self.browser.find_elements_by_xpath(EVENTLOG_TAB_ROWS)
            elif (subtab_name == "General"):
                event_row_xpath = self.browser.find_elements_by_xpath(GENERAL_TAB_ROWS)
            elif (subtab_name == "Product Instances"):
                event_row_xpath = self.browser.find_elements_by_xpath(PRODUCT_INSTANCES_TAB_ROWS)
            elif (subtab_name == "Licenses"):
                event_row_xpath = self.browser.find_elements_by_xpath(LICENSES_TAB_ROWS)

            print("The table entried for the {} are :\n".format(subtab_name))
            for event_row in event_row_xpath:
                columns = event_row.find_elements_by_tag_name('td')
                for column in columns:
                    column_val = column.text
                    column_val_encoded = column_val.encode('ascii', 'ignore')
                    table_entries.append(column_val_encoded)
                    print(column_val_encoded + "\n")
            return table_entries
        except Exception as e:
            print("Failed to fetch the table entries from virtual account {} for tab {}".format(virtual_account,
                                                                                                subtab_name))
            raise e

    def cssm_get_product_overview_details(self, virtual_account, product_name):
        """
        This function would fetch the input values in terms of list and output would be
        returned as list
        Parameters:
        - virtual_account : Provide virtual account name
        - product_name : Provide product name

        """
        try:
            overview_general_lists = []
            product_xpath = "//a[(@class='table-product-entry') and contains(text(),'" + product_name + "')]"
            self.browser.switch_to_window(self.windows[1])
            time.sleep(2)
            self._select_virtual_account(virtual_account)
            self._click_subtabs('Product Instances')
            time.sleep(2)
            self.browser.find_element_by_xpath(product_xpath).click()
            self.wait_till_UI_loads("//legend[text()='General']")

            print("The Registered product overview details are as :\n")
            product_row_xpath = self.browser.find_elements_by_xpath(PRODUCT_OVERVIEW_ROWS)
            for product_row in product_row_xpath:
                columns = product_row.find_elements_by_tag_name('td')
                for column in columns:
                    column_val = column.text
                    column_val_encoded = column_val.encode('ascii', 'ignore')
                    overview_general_lists.append(column_val_encoded)
                    print(column_val_encoded + "\n")
            return overview_general_lists
        except Exception as e:
            print("Failed to fetch the details in product overview window")
            raise e

    def cssm_product_transfer(self, virtual_account, device_name, transfer_to_account):
        """
        This function would transfer the product between the virtual accounts
        Parameters:
        - 'virtual_account' : Transfer the product from this virtual account
        - 'device_name' : Mention the device name which is registered to cloud
        - 'transfer_to_account' : Mention the virtual account to which the device needs to be transfered
        """
        try:
            self.browser.switch_to_window(self.windows[1])
            time.sleep(2)
            self._select_virtual_account(virtual_account)
            self._click_subtabs('Product Instances')
            time.sleep(2)
            self._click_product_link(device_name)
            self._popover_window_actions("transfer")
            transfer_to = Select(self.browser.find_element_by_id('product-transfer-dest-pool'))
            transfer_to.select_by_visible_text(transfer_to_account)
            ok_button, ok_button_xpath = self.get_visible_element(PRODUCT_TRANSFER_OK_BTN)
            if (ok_button.is_enabled()):
                ok_button.click()
                time.sleep(2)
            print("Successfully transfered the product from virtual account{0} to virtual account{1} ".format(
                virtual_account, transfer_to_account))
        except Exception as e:
            print("Not able to transfer the product {} ".format(device_name))
            raise e

    def cssm_get_product_overview_event_logs(self, virtual_account, product_name):
        """
        This function would fetch all the details of event logs under product instances tab
        overiview window and returns the list
        Parameters:
        - 'virtual_account' : Mention virtual account
        - 'product_name' : Mention the esa|wsa device which is registered

        """
        try:
            event_logs = []
            self.browser.switch_to_window(self.windows[1])
            time.sleep(2)
            self._select_virtual_account(virtual_account)
            self._click_subtabs('Product Instances')
            self._click_product_link(product_name)
            self._click_subtabs('Event Log', True)

            print("The Registered product event log details are :\n")
            event_row_xpath = self.browser.find_elements_by_xpath(PRODUCT_OVERVIEW_EVENTLOG_ROWS)
            for event_row in event_row_xpath:
                columns = event_row.find_elements_by_tag_name('td')
                for column in columns:
                    column_val = column.text
                    column_val_encoded = column_val.encode('ascii', 'ignore')
                    event_logs.append(column_val_encoded)
                    print(column_val_encoded + "\n")
            return event_logs
        except Exception as e:
            print("Not able to get the product {} event log details ".format(product_name))
            raise e

    def cssm_delete_virtual_account(self, virtual_account):
        """
        This function would delete the virtual account
        Parameters:
        - 'virtual_account' : Mention virtual account which needs to be deleted
        """
        try:
            self.browser.switch_to_window(self.windows[1])
            self._select_virtual_account(virtual_account)
            self._click_subtabs('General')
            self.browser.find_element_by_xpath(EDIT_LINK).click()
            print("Clicked on edit link")
            self.wait_till_UI_loads(EDIT_VIRTUAL_ACCOUNT_HEADER)
            self.browser.find_element_by_xpath("//a[text()='Delete Virtual Account']").click()
            time.sleep(2)
            self.wait_till_UI_loads("//h3[text()='Confirm Delete Virtual Account']")
            self._click_button("Delete Virtual Account")
            print("Successfully deleted the virtual account {}".format(virtual_account))
        except Exception as e:
            print("Not able to delete virtual account {} ".format(virtual_account))
            raise e

    def cssm_edit_virtual_account(self, virtual_account, description=None, default=False):
        """
        This function would edit the name decription or make the account as default virtual account

        Parameters:
        - 'virtual_account' : Mention virtual account which requires to be modified
        - 'description' : provide the decription if the description needs to be modified
        - 'default' : If Default= True whenever new licenses are added to the cloud it would
           by default gets added under this account
        """
        try:
            self.browser.switch_to_window(self.windows[1])
            self._select_virtual_account(virtual_account)
            self._click_subtabs('General')
            self.browser.find_element_by_xpath(EDIT_LINK).click()
            print("Clicked on edit link")
            self.wait_till_UI_loads(EDIT_VIRTUAL_ACCOUNT_HEADER)
            self._input_textfield('Name', virtual_account)
            if description is not None:
                self._input_textfield('Description', description)
            if (default):
                self.browser.find_element_by_xpath("//input[@type='checkbox']").click()
                print ("clicked on Make this the default destination for new licenses checkbox")
                time.sleep(2)
            self._click_button('Save')
            print("Successfully done changes for virtual account {} ".format(virtual_account))
        except Exception as e:
            print("Failed to edit changes to virtual account {} ".format(virtual_account))
            raise e

    def cssm_close(self):
        """
        This would close the cssm browser which was opened[main and childwindows].

        """
        try:
            browser_windows = self.browser.window_handles
            for handle in browser_windows:
                self.browser.switch_to_window(handle)
                self.browser.close()
        except Exception as e:
            print("Not able to close the CSSM browsers")
            raise e

    # Some additional functions required for browser stability
    def wait_till_UI_loads(self, elementxpath):
        """
        This function would wait for the application to load till the specified
        element exists on the page. Provide the desired element xpath As parameter
        The function fails if it fails to locate the elemenT mentioned within 30s
        as given below
        """

        delay = 30  # seconds
        try:
            element_present = EC.presence_of_element_located((By.XPATH, elementxpath))
            WebDriverWait(self.browser, delay).until(element_present)
            print("Application has loaded successfully along with the GUI object {}!".format(elementxpath))
        except TimeoutException:
            print("Loading of Application for GUI object {} took too much time!".format(elementxpath))

    def get_visible_element(self, xpath):
        """
        It will provide the list of matching elements from the page

        Parameter:
         - 'xpath' - xpath of the element which you want to access

        Return:
           returns two values element,xpath

        """

        element = ''
        match_elements = self.browser.find_elements_by_xpath(xpath)
        if (match_elements):
            for elements in match_elements:
                if (elements.is_displayed()):
                    element = elements
                    break
                else:
                    pass
        if (not element):
            raise NoSuchElementException("Web Element {} Not Found".format(element))
        return element, xpath

    def _click_button(self, button_name):
        btnxpath = "//button[text()='" + button_name + "']"
        try:
            webobj, objpath = self.get_visible_element(btnxpath)
            if (webobj):
                if (webobj.is_enabled()):
                    webobj.click()
                    time.sleep(3)
                    print("Successfully clicked of {} button".format(button_name))
                else:
                    raise NoSuchElementException("Button {} Not Enabled ".format(button_name))
        except NoSuchElementException as e:
            raise NoSuchElementException("Button {} not found".format(button_name))
        except Exception as e:
            raise e

    def _input_textfield(self, inputfield_label, value):
        try:
            inputfield_xpath = "//label[contains(text(),'" + inputfield_label + "')]/../../td[2]/input"
            inputobj, inputxpath = self.get_visible_element(inputfield_xpath)
            inputobj.clear()
            inputobj.click()
            print("Enetering value {} to textfield {} ".format(inputfield_label, value))
            inputobj.send_keys(value)
            time.sleep(3)
        except NoSuchElementException as e:
            raise NoSuchElementException("Input text field {} not found".format(inputfield_label))

    def _get_alert_message(self):
        return_val = ""
        alertobj, alert_msg = self.get_visible_element(ALERT_POPUP)
        if (alertobj):
            return_val = str(alertobj.text.strip())
        return return_val

    def _verify_toaster_popup(self):
        toaster_popup_xpath = "//div[@class='toaster-icon-success']/../div[@class='toaster-text']"
        self.wait_till_UI_loads(TOASTER_POPUP)

    def _click_subtabs(self, tab_name, popover=False):
        subtab_xpath = "//li/a[text()='" + tab_name + "']"
        subtab_xpath1 = "//div[contains(@class,'popover')]//li/a[text()='" + tab_name + "']"
        if (popover):
            if (self.browser.find_element_by_xpath(subtab_xpath1).is_displayed()):
                self.browser.find_element_by_xpath(subtab_xpath1).click()
                print("Clicked on Sub Tab {} Successfully".format(tab_name))
        elif (self.browser.find_element_by_xpath(subtab_xpath).is_displayed()):
            self.browser.find_element_by_xpath(subtab_xpath).click()
            time.sleep(4)
        else:
            raise Exception("Not able to click on virtual account sub Tab {}".format(tab_name))

    def _select_virtual_account(self, virtual_account_tab):
        virtual_tab_name = "//div[@class='pool-name' and contains(text(),'" + virtual_account_tab + "')]"
        try:
            self.browser.find_element_by_xpath(virtual_tab_name).click()
            print("Clicked on Virtual account Tab {} Successfully".format(virtual_account))
            time.sleep(4)
        except NoSuchElementException:
            raise Exception("Not able to click on virtual account Tab {}".format(virtual_account))

    def _click_product_link(self, product_name):
        product_xpath = "//a[(@class='table-product-entry') and contains(text(),'" + product_name + "')]"
        try:
            self.browser.find_element_by_xpath(product_xpath).click()
            print("Clicked on product link {} ".format(product_name))
            time.sleep(2)
        except NoSuchElementException:
            raise Exception("product {} not found".format(product_name))

    def _popover_window_actions(self, perform_action):
        """
        This function would basically perform the popover window actions
        such as clicking on close,remove,transfer               ,
        This window would appear when you click on the product link under
        product instances TAB
        """
        try:
            if (perform_action.lower() == "close"):
                self.browser.find_element_by_xpath(POPOVER_CLOSE_BTN).click()
            elif (perform_action.lower() == "transfer"):
                self.browser.find_element_by_xpath(POPOVER_TRANSFER_BTN).click()
                self.wait_till_UI_loads(TRANSFER_PRODUCT_HEADER)
            elif (perform_action.lower() == "remove"):
                self.browser.find_element_by_xpath(POPOVER_REMOVE_BTN).click()
                time.sleep(2)
        except NoSuchElementException:
            raise Exception("Not able to click on {}".format(perform_action.lower()))
