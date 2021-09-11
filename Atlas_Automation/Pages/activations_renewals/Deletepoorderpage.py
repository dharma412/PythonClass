from selenium.webdriver.common.by import By

from SeleniumHelper import SeleniumHelper

class Deletepoorderpage:
    def __init__(self):
        self.btn_continue = By.NAME,'continue'

    def click_continue_to_delete_po(self):
        SeleniumHelper.click_element(self.btn_continue)
