import json
import os

from robot.api import logger
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains


from Logger import exec_log

driver = None
driver_wait = None
action_driver=None
@exec_log
def get_web_driver_details():
    """
    Purpose: Initializes the driver and driver wait, returns reference to these objects

    Args:
	None

    Returns:
        Returns reference to webdriver and webdriver wait
    """

    global driver
    global driver_wait
    global action_driver
    if driver == None:
        base_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','config','jenkins_config.json'))
        with open(base_path, "r") as read_file:
            data = json.load(read_file)
        if data['browser'] ==  "firefox":
            firefox_capabilities = webdriver.FirefoxProfile()
            firefox_capabilities.accept_untrusted_certs = True
            driver = webdriver.Firefox(firefox_profile=firefox_capabilities,executable_path=data['browser_path'])
            driver_wait = WebDriverWait(driver, data['explicit_wait'])
            action_driver = ActionChains(driver)
        elif data['browser'] == "chrome":
            chrome_options = Options()
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-useAutomationExtension")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--start-maximized")
            driver  = webdriver.Chrome(executable_path=data['browser_path'])
            driver_wait = WebDriverWait(driver, data['explicit_wait'])
            action_driver=ActionChains(driver)
        elif data['browser'] == "ie":
            driver  = webdriver.Ie(executable_path=data['browser_path'])
            driver_wait = WebDriverWait(driver, data['explicit_wait'])
            action_driver = ActionChains(driver)
    return driver,driver_wait,action_driver

@exec_log
def get_web_driver_wait():
    """
    Purpose: Returns the reference to  driver wait object

    Args:
      None

    Returns:
        Returns the reference to  web driver wait object

    """
    global driver_wait
    return driver_wait


