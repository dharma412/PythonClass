import time
import re
from datetime import datetime
from datetime import timedelta

from selenium.webdriver.common.by import By
from robot.api import logger

from SeleniumHelper import SeleniumHelper
from pages.activations_renewals.Deletepoorderpage import Deletepoorderpage
import CreateCustomer

class Customerpage:
    ''' Page object model for altas Customer page'''

    def __init__(self):
        self.btn_add_new_order = By.NAME,'poorder'
        self.status_message = By.XPATH,'//*[@id="container_content"]/table[2]/tbody/tr/td'
        self.po_report = By.XPATH,'//*[@id="po_report"]/dl/dd/div[2]/table/tbody/tr'
        self.btn_continue = By.NAME,"continue"
        self.txt_features= By.XPATH,'//*[@id="features_div"]/dl/dd[1]/div[2]/table/tbody/tr'
        self.mx_records= '//div[@id="mail_xdiv"]//child::tbody[1]//child::tr//td'

    def click_add_po_order(self):
        """
        Purpose: Clicks on the add purchase order button

        Args:
            None
        Returns:
            None

        """
        SeleniumHelper.click_element(self.btn_add_new_order)

    def delete_specific_purchase_orders(self,name):
        """
        Purpose: deletes the purchase order based on sales order name from caller

        Args:
            name : sales order name to be deleted
        Returns:
            None

        """
        text = "No PO available."
        elements = SeleniumHelper.get_driver().find_elements(By.XPATH,"//*[contains(text(),'" + text + "')]")
        if not elements:
            webelements = SeleniumHelper.get_web_elements(self.po_report)
            i = 1
            while i <=len(webelements):
                text = SeleniumHelper.get_text((By.XPATH,'//*[@id="po_report"]/dl/dd/div[2]/table/tbody/tr['+ str(i) +']/td[1]'))
                if text == name:
                    SeleniumHelper.click_element((By.XPATH,'//*[@id="po_report"]/dl/dd/div[2]/table/tbody/tr['+ str(i) +']/td[12]'))
                    SeleniumHelper.click_element(self.btn_continue)
                    break
                i = i+1

    def delete_existing_purchase_orders(self):
        """
        Purpose: Clears all purchase order for the customer

        Args:
            None
        Returns:
            None

        """
        text = "No PO available."
        elements = SeleniumHelper.get_driver().find_elements(By.XPATH,"//*[contains(text(),'" + text + "')]")
        if len(elements)==0:
            webelements = SeleniumHelper.get_web_elements(self.po_report)
            i = 1
            result = []
            while i <=len(webelements):
                result.append(SeleniumHelper.get_text((By.XPATH,'//*[@id="po_report"]/dl/dd/div[2]/table/tbody/tr['+ str(i) +']/td[1]')))
                i = i+1
            for order in result:
                self.delete_specific_purchase_orders(order)

    def get_activation_status_of_sales_order(self,so_name):
        """
        Purpose: gets the status of input sales order

        Args:
            so_name   : Sales order name whose status is to be fetched
        Returns:
            str : status of the specified sales order

        """
        text = "No PO available."
        status = None
        elements = SeleniumHelper.get_driver().find_elements(By.XPATH,"//*[contains(text(),'" + text + "')]")
        if len(elements)==0:
            webelements = SeleniumHelper.get_web_elements(self.po_report)
            i = 1
            while i <=len(webelements):
                text = SeleniumHelper.get_text((By.XPATH,'//*[@id="po_report"]/dl/dd/div[2]/table/tbody/tr['+ str(i) +']/td[2]'))
                if text == so_name:
                    status = SeleniumHelper.get_text((By.XPATH,'//*[@id="po_report"]/dl/dd/div[2]/table/tbody/tr['+ str(i) +']/td[11]'))
                    break
                i = i + 1
        return status

    def get_features_for_customer(self):
        """
        Purpose: Fetches all the features from features section in the atlas UI

        Args:
            None
        Returns:
           returns features information like name,quantity and end dates 

        """
        SeleniumHelper.click_element((By.ID,"img_features"))
        i  =  len(SeleniumHelper.get_web_elements(self.txt_features))
        features = []
        for j in range(1,i+1):
            feature_name = SeleniumHelper.get_text((By.XPATH,'//*[@id="features_div"]/dl/dd[1]/div[2]/table/tbody/tr['+str(j)+']/td[1]'))
            feature_end_date = SeleniumHelper.get_text((By.XPATH,'//*[@id="features_div"]/dl/dd[1]/div[2]/table/tbody/tr['+str(j)+']/td[3]'))
            feature_end_date = "".join(feature_end_date.split(',')[0:2])
            feature_qty = SeleniumHelper.get_text((By.XPATH,'//*[@id="features_div"]/dl/dd[1]/div[2]/table/tbody/tr['+str(j)+']/td[5]'))
            if('.' in feature_end_date):
                if('Sept.' in feature_end_date):
                    feature_end_date = feature_end_date.replace('Sept.','Sep.')
                end_date_format = str(datetime.strptime(feature_end_date, '%b. %d %Y')).split()[0]
            else:
                end_date_format = str(datetime.strptime(feature_end_date, '%B %d %Y')).split()[0]
            end_date_format = datetime.strptime(end_date_format, '%Y-%m-%d')
            end_date_format = datetime.strftime(end_date_format, '%m/%d/%Y')
            features.append({'feature_name':feature_name, 'end_date':end_date_format,'Quantity':feature_qty})
        return features
   
    def verify_feature_activated(self,actual_features,activated_feature_name,end_date):
        """
        Purpose: Asserts features are activated correctly

        Args:
            actual_features        : Output of features in UI
            activated_feature_name : Feature or add on name
            end_date               : No. dates the feature/addon will be active
        Returns:
            Returns True if actual and expected output matches else fails

        """
        master_feature_list = {'L-CES-ESI-LIC':['IPAS', 'SO', 'VOF'],
                               'L-CES-ESP-LIC':['IPAS','SO', 'VOF', 'DLP', 'PXE'],
                               'L-CES-ESO-LIC':['DLP', 'PXE'],
                               'L-CES-O365I-LIC':['IPAS','VOF'],
                               'L-CES-O365P-LIC':['IPAS', 'VOF', 'DLP', 'PXE'],
                               'L-CES-AMP-LIC':['ESFR', 'ESFA'],
                               'L-CES-GSU-LIC': ['GSU'],
                               'L-CES-ENC-LIC-K9':['PXE'],
                               'L-CES-DLP-LIC':['DLP'],
                               'L-CES-MFE-LIC':['MC'],
                               'L-CES-IA-LIC':['IIA'],
                               'L-CES-IMS-LIC':['IMS'],
                               }
        expected_keys = master_feature_list.get(activated_feature_name)
        logger.info("Actual feature - {}".format(actual_features))
        logger.info("Expected feature - {}".format(expected_keys))
        logger.info("End Date {}".format(end_date))
        actual_result=[]
        for e in actual_features:
            for f in expected_keys:
                if e.get('feature_name').strip() == f.strip() and e.get('end_date').strip()== end_date.strip():
                    actual_result.append(f)
        if sorted(expected_keys) == sorted(actual_result):
            return True
        else:
            return False

    def refresh_customer_purchase_order_page(self):
        """
        Purpose: Refreshes the customer purchase order page

        Args:
          None
        Returns:
          None
        """
        SeleniumHelper.refresh_browser()

    def get_allocation_page_title(self):
        """
        Purpose:To get title of the page

        Args:
          None
        Returns:
          Page title
        """
        return SeleniumHelper.get_page_title()

    def mx_records_generate(self,allocation_name):
        """
        Purpose: To validate the MX records when

        Args:

        Returns:

        """
        elements = SeleniumHelper.get_driver().find_elements(By.XPATH,self.mx_records)
        i = 1
        count=1
        pattern = "(mx|obj)[1-2]\." + allocation_name
        while i <= len(elements):
            text = SeleniumHelper.get_text(
                (By.XPATH, '//div[@id="mail_xdiv"]//child::tbody[1]//child::tr['+str(i)+']//td'))
            result=re.search(pattern,text)
            if result:
                count=count+1
            i = i + 1
        return str(count)
