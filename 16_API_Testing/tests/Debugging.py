import json
import os

from robot.api import logger
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
driver=webdriver.Chrome()


def navigate_to_page(PageName):
    Xpath = "//ul[@class='list_navbar_tabs']//a[contains(text(),'" + PageName + "')]"
        # Xpath="//a[contains(text(),'"+PageName+"')]"
    element=driver.find_element_by_xpath(Xpath).click()

navigate_to_page("Atlas")

