from selenium.webdriver.common.by import By
from SeleniumHelper import SeleniumHelper

class Activationsrenewalspage:
    ''' Page object model for altas Activations and renewal page atlas/customer_list'''
    def __init__(self):
        self.btn_add_new_order = By.XPATH,'//*[@id="container_content"]/div/form[1]/span/input'
        self.txt_search_string = By.ID, 'search_string'
        self.link_allocation_name= By.XPATH,'//*[@id="section_configurations"]/dd/div[2]/table/tbody/tr/td[1]/a'
        self.btn_search = By.XPATH, '//*[@id="container_content"]/div/form[2]/table/tbody/tr/td/div/input[2]'
        self.link_customer_name_search_result = By.XPATH, '//tr[@class="yui-dt-odd"]//a'

    def input_customer(self, customer):
        SeleniumHelper.send_keys(self.txt_search_string,customer)

    def click_on_customer_search(self):
        SeleniumHelper.click_element(self.btn_search)

    def click_on_customer_name(self, customername):
        SeleniumHelper.click_element((By.LINK_TEXT, customername))

    def click_on_allocation_name(self):
        SeleniumHelper.click_element(self.link_allocation_name)

    def get_allocation_name(self):
        return SeleniumHelper.get_text(self.link_allocation_name)

    def get_customer_name_from_search_result(self):
        """
         Purpose:Method to get customer name from search result

         Args:
           None
         Returns:
           customer name as text
        """
        return SeleniumHelper.get_text(self.link_customer_name_search_result)
