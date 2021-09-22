import time
from selenium.common.exceptions import *
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from framework.utils import mulligans


class CommonFunctions(object):

    @mulligans(3)
    def select_option_from_dropdown_by_text(driver, locator_type, locator_string, option_text):
        result = False

        #wait = WebDriverWait(driver, 10)

        if locator_type == 'xpath':
            time.sleep(2)
            # with Utilities.wait_for_page_load(driver,timeout=5):
            '''
            while True:
                dropdown_element = wait.until(EC.visibility_of_element_located((By.XPATH, locator_string)))
                ele_select = Select(dropdown_element)
            '''

            ele_select = driver.find_element_by_xpath(locator_string)
            # Utilities.wait_for_displayed(ele_select)

        for ele_option in ele_select.find_elements_by_tag_name('option'):
            if ele_option.text == option_text:
                # Utilities.wait_for_then_click(ele_option,base=driver)
                ele_option.click()
                result = True
                break

        time.sleep(2)
        # Utilities.wait_for_page_load(driver,timeout=10)

        return result
