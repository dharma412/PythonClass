import time

from selenium.webdriver.common.by import By
from robot.api import logger

from SeleniumHelper import SeleniumHelper
from pages.activations_renewals.Deletepoorderpage import Deletepoorderpage

class Approvalpage:
    ''' Page object model for altas Approval page i.e atlas/approval_page/'''
    def __init__(self):
        self.btn_add_new_order = By.NAME,'neworder'

    def click_on_new_order(self):
        SeleniumHelper.click_element(self.btn_add_new_order)
