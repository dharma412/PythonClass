from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
from robot.api import logger

from Webdrivermanager import get_web_driver_details
from Logger import exec_log


class SeleniumHelper(object):
    ''' Wrapper for interacting with web UI'''
    _driver,_wait,_ac_driver = get_web_driver_details()


    @classmethod
    @exec_log
    def get_web_element(cls,locator):
        """
        Purpose: checks if web element is present with explicitly

        Args:
          locator       : Locator to be found

        Returns:
            Returns webelement if found else raises exception
       """

        try:
            cls._wait.until(EC.element_to_be_clickable(locator))
            logger.info("get_web_element()-  waiting for element ... {0}".format(locator))
            return cls._driver.find_element(locator[0],locator[1])
        except NoSuchElementException as e:
            logger.info("get_web_element()-  waiting for element ...")
            raise NoSuchElementException(locator[1], e)
        except TimeoutException as e:
            logger.info("get_web_element()- waiting for element exceeds timeout ...")
            raise TimeoutException(locator[1], e)

    
    @classmethod
    @exec_log
    def get_text(cls,locator):
        """
        Purpose: returns the text info. in the specified locator

        Args:
            locator       : Locator whose text needs to be retrieved

        Returns:
            Returns text for the given webelement if found else raises exception
        """

        return cls.get_web_element(locator).text
 

    @classmethod
    @exec_log
    def get_web_elements(cls,locator):
        """
        Purpose: checks if web element is present with explicitly and returns list 
                 of web elements if found

        Args:
            locator       : Locator to be identified
        Returns:
            Returns webelements if found else raises exception
        """

        try:
            cls._wait.until(EC.presence_of_element_located(locator))
            logger.info("get_web_elements()-  waiting for element ... {0}".format(locator))
            return SeleniumHelper._driver.find_elements(locator[0],locator[1])
        except NoSuchElementException as e:
            logger.info("get_web_elements()-  waiting for element ...")
            raise NoSuchElementException(locator[1], e)
        except TimeoutException as e:
            logger.info("get_web_elements()- waiting for element exceeds timeout ...")
            raise TimeoutException(locator[1], e)

    @classmethod
    @exec_log
    def select_by_index_from_dropdown(cls,locator,index):
        """
        Purpose: selects the dropdown webelement based on
                 specified locator and index

        Args:
            locator       : Locator to be identified
            index         : index in dropdown
        Returns:
            selects the item from dropdown based on index
        """

        try:
            cls._wait.until(EC.presence_of_all_elements_located(locator))
            select = Select(SeleniumHelper._driver.find_element(locator[0],locator[1]))
            select.select_by_index(index)
        except NoSuchElementException as e:
            raise NoSuchElementException(locator[1], e)

    @classmethod
    @exec_log
    def select_by_visible_text(cls,elem,text):
        """
        Purpose: selects the dropdown webelement based on
                 specified locator and visible text

        Args:
            locator       : Locator to be identified
            text          : visible text name in dropdown
        Returns:
            selects the item from dropdown based on text
        """

        select = Select(cls.get_web_element(elem))
        select.select_by_visible_text(text)

    @classmethod
    @exec_log
    def click_element(cls,element):
        """
        Purpose: clicks on the input webelement 

        Args:
            element       : element to be clicked

        Returns:
           None
        """

        logger.info("click_element() - Clicking on element= {0}...".format(element))
        cls.get_web_element(element).click()

    @classmethod
    @exec_log
    def open(cls, url):
        """
        Purpose: Launches/opens the website for the specified url

        Args:
            url(str)       : url to be opened

        Returns:
           None
        """

        logger.info("open() - Opening the browser - URL = {0}...".format(url))
        cls._driver.get(url)

    @classmethod
    @exec_log
    def get_driver(cls):
        """
        Purpose: returns the reference to selenium web driver 

        Args:
            None
        Returns:
           returns the reference web driver
        """

        logger.info("get_driver() - getting driver...")
        return cls._driver

    @classmethod
    @exec_log
    def send_keys(cls,elem,input):
        """
        Purpose: inputs the specified text for the specified element

        Args:
            elem  : Web element for which the input text has to be sent
            input : input text
        Returns:
            None
        """

        SeleniumHelper.get_web_element(elem).send_keys(input)

    @classmethod
    @exec_log
    def refresh_browser(cls):
        """
        Purpose: refreshes the browser

        Args:
            None
        Returns:
            None
        """
        logger.info("refresh_browser() - refreshing browser...")
        cls._driver.refresh()

    @classmethod
    @exec_log
    def navigate_back_browser(cls):
        """
        Purpose: move back to prior browser page

        Args:
            None
        Returns:
            None
        """
        logger.info("navigate_back_browser() - navigate back browser...")
        cls._driver.back()

    @classmethod
    @exec_log
    def close_all(cls):
        """
        Purpose: closes the browser

        Args:
            None
        Returns:
            None
        """
        logger.info("close_all() - closing driver...")
        cls._driver.quit()

    @classmethod
    @exec_log
    def get_action_driver(cls):
        """
        Purpose: returns the reference to selenium web action driver

        Args:
            None
        Returns:
           returns the reference web action driver
        """

        logger.info("get_driver() - getting driver...")
        return cls._ac_driver

    @classmethod
    @exec_log
    def get_title(cls):
        """
        Purpose: returns the title of the page

        Args:
            None
        Returns:
           returns the title of the page
        """

        logger.info("get_driver() - getting driver...")
        return cls._driver.title
