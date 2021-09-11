import time
import string
import random

from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from robot.api import logger

from AtlasTestConstants import ATLAS_CUSTOMER_DATA
from SeleniumHelper import SeleniumHelper
import CreateCustomer
import AtlasDbUtils

class Newpoorderpage:
    ''' Page object model for altas po order'''
    def __init__(self):
        '''  Page repository for interacting with purchase order  '''
        self.txt_cust_name = By.ID,'cust_name'
        self.label_virtual_serial = By.XPATH,'//*[@id="id_form"]/table[1]/tbody/tr[2]/td'
        self.txt_contract_num = By.ID,'contract_num'
        self.txt_id_qty = By.ID,'id_qty'
        self.label_stage = By.XPATH,'//*[@id="id_form"]/table[1]/tbody/tr[5]/td'
        self.txt_pur_order=By.ID,'pur_order'
        self.txt_sales_order = By.ID,'sales_order'
        self.txt_deal_id = By.ID, 'deal_id'
        self.txt_cust_email = By.ID,'cust_email'
        self.txt_partner_name = By.ID,'partner_name'
        self.txt_partner_email = By.ID,'partner_email'
        self.txt_se_name = By.ID,'se_name'
        self.txt_se_email = By.ID,'se_email'
        self.txt_am_name = By.ID,'am_name'
        self.txt_am_email =By.ID,'am_email'
        self.txt_bill_name = By.ID,'bill_name'
        self.txt_bill_addr = By.ID,'bill_addr'
        self.txt_bill_email = By.ID,'bill_email'
        self.txt_ship_addr = By.ID,'ship_addr'
        self.no_po_text = By.XPATH,"//*[contains(text(),'No PO available.')]"
        self.txt_feature_start_date = By.ID, 'start_date'
        self.txt_feature_end_date =   By.ID, 'end_date'
        self.txt_add_on_start_date = By.ID,'add_on_start_date'
        self.txt_add_on_end_date = By.ID,'add_on_end_date'
        self.drp_feature_type = By.ID,'feature_type'
        self.drp_addon_feature = By.ID,'add_on_feat'
        self.btn_save = By.ID,'save'
        self.btn_confirm = By.XPATH,"//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']/span"
        self.txt_warning_dialog_message = By.ID,'ui-id-1'
        self.txt_confirm_dialog_message = By.ID, 'dialog'
        self.btn_confirm_dialog_yes = By.XPATH,'//span[@class="ui-button-text" and contains(text(),"YES")]'
        self.btn_confirm_add_on_dialog_yes = By.XPATH,'//span[@class="ui-button-text" and contains(text(),"Yes")]'
        self.btn_confirm_dialog_no= By.XPATH,'//span[@class="ui-button-text" and contains(text(),"NO")]'
        self.btn_ok_dialog_box = By.XPATH,'//span[@class="ui-button-text" and contains(text(),"Ok")]'
        self.text_confirm_diaglog = By.ID,'id_next'
        self.txt_success_message = By.XPATH,'//td[@class="successmessage"]'
        self.list_of_future_po = By.XPATH,'//table[@class="yui-dt table_section_table_notes"]/tbody/tr/td[contains(text(),"FUTURE")]'
        self.btn_continue = By.NAME, "continue"

    def get_feature(self):
        """
        Purpose: picks and returns atlas supported features dynamically or at runtime

        Args:
            None
        Returns:
            Returns atlas features at run time
        
        O365-LIC will be included  when O365 is in place
        features = ['L-CES-ESO-LIC', 'L-CES-ESI-LIC', 'L-CES-ESP-LIC','L-CES-O365I-LIC','L-CES-O365P-LIC']
        """
        
        features = ['L-CES-ESO-LIC', 'L-CES-ESI-LIC', 'L-CES-ESP-LIC']
        return random.choice(features)

    def get_add_on(self):
        """
        Purpose: picks and returns atlas supported addons dynamically or at runtime

        Args:
            None
        Returns:
            Returns atlas add on at runtime

        """
        add_on = ['L-CES-AMP-LIC', 'L-CES-GSU-LIC','L-CES-DLP-LIC', 'L-CES-MFE-LIC','L-CES-IA-LIC']
        return random.choice(add_on)

    def create_feature_in_purchase_order(self, feature_key, start_days=0,end_days=30):
        """
        Purpose: Creates purchase order with feature bundle name for start/end dates 
                 from atlas time 

        Args:
            feature_key :  Feature key name
            start_days  :  No. of days from today is picked from atlas current date
            end_days    :  No. of days from today is picked from atlas current date

        Returns:
            returns the details of the created purchase order

        """
        allowed_characters =''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase+'$%_!&/-') for _ in range(10))
        allowed_characters = (allowed_characters+str(time.time())).replace('.','')

        # Purchase order and sales order name  with allowed characters
        po_name =  "po-"+allowed_characters
        so_name =  "so-"+allowed_characters
        SeleniumHelper.send_keys(self.txt_pur_order,po_name)
        SeleniumHelper.send_keys(self.txt_sales_order,so_name)

        # Setting activations time and expiry using current date on atlas server 
        start_date = CreateCustomer.get_days_from_now(start_days)
        end_date = CreateCustomer.get_days_from_now(end_days)
        SeleniumHelper.send_keys(self.txt_feature_start_date,start_date)
        SeleniumHelper.send_keys(self.txt_feature_end_date,end_date)
        SeleniumHelper.get_web_element(self.txt_feature_end_date).send_keys(Keys.TAB)
      
        # Picks feature key passed from test case
        SeleniumHelper.select_by_visible_text((By.ID,"feature_type"),feature_key)
        time.sleep(2)
        SeleniumHelper.click_element(self.btn_save)
        time.sleep(2)
      
        # Selects dialog box for proceed or cancel purchase order
        SeleniumHelper.click_element((By.XPATH,"//button/span[@class='ui-button-text' and contains(text(),'YES')]"))
        return {'feature':feature_key,'purchase_order': po_name ,'sales_order': so_name,'start_date':start_date,'end_date':end_date}

    def create_add_on_in_purchase_order(self,add_on, start_days=0,end_days=30):
        """
        Purpose: Creates purchase order with add on name for start/end dates
                 from atlas time

        Args:
            add_on      :  add on name
            start_days  :  No. of days from today is picked from atlas current date
            end_days    :  No. of days from today is picked from atlas current date

        Returns:
            returns the details of the created purchase order

        """
        allowed_characters =''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase+'$%_!&/-') for _ in range(10))
        allowed_characters = (allowed_characters+str(time.time())).replace('.','')

        # Dynamically generating Purchase order and sales order name with allowed characters
        po_name =  "po-"+allowed_characters
        so_name =  "so-"+allowed_characters
        SeleniumHelper.send_keys(self.txt_pur_order,po_name)
        SeleniumHelper.send_keys(self.txt_sales_order,so_name)

        # Picks add on passed from test case with specified start and end dates
        SeleniumHelper.select_by_visible_text(self.drp_addon_feature,add_on)
        start_date = CreateCustomer.get_days_from_now(start_days)
        end_date = CreateCustomer.get_days_from_now(end_days)
        SeleniumHelper.send_keys(self.txt_add_on_start_date,start_date)
        SeleniumHelper.send_keys(self.txt_add_on_end_date,end_date)
        SeleniumHelper.get_driver().find_element(By.ID,'add_on_end_date').send_keys(Keys.TAB)
        SeleniumHelper.click_element((By.ID,'save'))
        time.sleep(4)

        # Selects dialog box for proceed or cancel purchase order
        SeleniumHelper.get_driver().find_element(By.XPATH,"//button/span[@class='ui-button-text' and contains(text(),'Yes')]").click()
        return {'add_on':add_on,'purchase_order': po_name ,'sales_order': so_name,'start_date':start_date,'end_date':end_date}

    def create_feature_and_add_on_in_same_purchase_order(self,feature,add_on,start_days=0,end_days=30):
        """
        Purpose: Creates purchase order with bundle and add on name for start/end dates
                 from atlas time

        Args:
            feature     :  Feature name
            add_on      :  add on name
            start_days  :  No. of days from today is picked from atlas current date
            end_days    :  No. of days from today is picked from atlas current date

        Returns:
            returns the details of the created purchase order

        """
        allowed_characters =''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase+'$%_!&/-') for _ in range(10))
        allowed_characters = (allowed_characters+str(time.time())).replace('.','')
        po_name =  "po-"+allowed_characters
        so_name =  "so-"+allowed_characters

        # Picks feature bundle and add on passed from test case with specified start and end dates
        SeleniumHelper.send_keys(self.txt_pur_order,po_name)
        SeleniumHelper.send_keys(self.txt_sales_order,so_name)
        start_date = CreateCustomer.get_days_from_now(start_days)
        end_date = CreateCustomer.get_days_from_now(end_days)
        SeleniumHelper.send_keys(self.txt_feature_start_date,start_date)
        SeleniumHelper.send_keys(self.txt_feature_end_date,end_date)
        SeleniumHelper.get_web_element(self.txt_feature_end_date).send_keys(Keys.TAB)
        SeleniumHelper.select_by_visible_text((By.ID,"feature_type"),feature.strip())
        add_ons = add_on.split(",")
        for add_on in add_ons:
            SeleniumHelper.select_by_visible_text(self.drp_addon_feature,add_on.strip())
        SeleniumHelper.send_keys(self.txt_add_on_start_date,start_date)
        SeleniumHelper.send_keys(self.txt_add_on_end_date,end_date)
        SeleniumHelper.get_driver().find_element(By.ID,'add_on_end_date').send_keys(Keys.TAB)
        SeleniumHelper.click_element((By.ID,'save'))
        time.sleep(4)

        # Selects dialog box for proceed or cancel purchase order
        SeleniumHelper.click_element((By.XPATH,"//button/span[@class='ui-button-text' and contains(text(),'YES')]"))
        return {'feature':feature,'add_on':add_on,'purchase_order': po_name ,'sales_order': so_name,'start_date':start_date,'end_date':end_date}

    def update_end_dates_to_expire_purchase_order(self,end_days,so_name):
        """
        Purpose: Updates the sales order end date for checking its expiry

        Args:
            end_days    :  No. of days from today is picked from atlas current date
            so_name     :  Sales order name

        Returns:
           None
        """

        CreateCustomer.update_purchase_order_end_dates(end_days,so_name)

    def refresh_purchase_order_page(self):
        """
        Purpose: Refreshes the purchase page

        Args:
          None
        Returns:
          None
        """

        SeleniumHelper.refresh_browser()

    def click_save_po(self):
        """
        Purpose: To click Save PO button

        Args:
          None
        Returns:
          None
        """

        SeleniumHelper.click_element(self.btn_save)

    def get_warning_dialog_text(self):
        """
        Purpose: To return text form warning dialog box

        Args:
            None
        Returns:
            warning text as string
        """
        text = SeleniumHelper.get_text(self.txt_warning_dialog_message)
        return text

    def click_ok_warning_dialog(self):
        """
        Purpose: To click Ok button in warning dialog box

        Args:
            None
        Returns:
            None
        """
        SeleniumHelper.click_element(self.btn_ok_dialog_box)

    def click_no_confirm_dialog(self):
        """
        Purpose: To click No button in confirm dialog box

        Args:
            None
        Returns:
            None
        """
        SeleniumHelper.click_element(self.btn_confirm_dialog_no)

    def click_yes_confirm_dialog(self):
        """
        Purpose: To click Yes button in confirm dialog box

        Args:
            None
        Returns:
            None
        """
        SeleniumHelper.click_element(self.btn_confirm_dialog_yes)

    def get_confirm_dialog_text(self):
        """
        Purpose: To return text from confirm dialog box

        Args:
            None
        Returns:
             Message from Confirmation dialog box
        """
        text = SeleniumHelper.get_text(self.txt_confirm_dialog_message)
        return text

    def input_purchase_order(self, purchase_order):
        """
        Purpose: To input value to Purchase Order text box

        Args:
            purchase_order :value to be entered for purchase order text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_pur_order,purchase_order)

    def input_sales_order(self, sales_order):
        """
        Purpose: To input value to Sales Order text box

        Args:
            sales_order :value to be entered for sales order text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_sales_order,sales_order)

    def select_feature_bundle_by_index(self,bundleidx):
        """
        Purpose: select feature type by index

        Args:
            bundleidx  : index of  feature type to be selected from drop down
        Returns:
            None
        """
        SeleniumHelper.select_by_index_from_dropdown(self.drp_feature_type,bundleidx)

    def input_feature_end_date(self, end_date):
        """
        Purpose: To Input value to feature end date

        Args:
            end_date:feature end date in mm/dd/yyyy
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_feature_end_date,end_date)

    def input_feature_start_date(self, start_date):
        """
        Purpose: To Input value to feature start date

        Args:
            start_date:feature start date in mm/dd/yyyy
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_feature_start_date,start_date)

    def get_date_from_today (self,days_to_be_modified):
        """
         purpose: To Modify date from current day

         Args:
            days_to_be_modified  : days has to be added to current date
         Returns:
            date in mm/dd/yyyy format
         """
        dat = int(days_to_be_modified)
        expected_date = datetime.today() + timedelta(days=dat)
        return expected_date.strftime("%m/%d/%Y")

    def get_status_message(self):
        """
        Purpose: Get status message from UI

        Args:
            None
        Returns:
            Message as String
        """

        return SeleniumHelper.get_text(self.txt_success_message)

    def delete_all_future_po_orders(self):
        """
        Purpose: deletes all the future pos if available

        Args:
            None
        Returns:
            None

        """
        rows = SeleniumHelper.get_driver().find_elements(By.XPATH,
                                                         "//div[@id='po_report']/dl/dd/div/table/tbody/tr")
        future_po = SeleniumHelper.get_driver().find_elements(By.XPATH,"//table[@class='yui-dt table_section_table_notes']/tbody/tr/td[contains(text(),'FUTURE')]")

        name='FUTURE'
        if rows and future_po:
            i = 1
            while i <=len(rows):
                text = SeleniumHelper.get_text((By.XPATH,'//*[@id="po_report"]/dl/dd/div[2]/table/tbody/tr['+ str(i) +']/td[11]'))
                if text == name:
                    SeleniumHelper.click_element((By.XPATH,'//*[@id="po_report"]/dl/dd/div[2]/table/tbody/tr['+ str(i) +']/td[12]'))
                    SeleniumHelper.click_element(self.btn_continue)
                    break
                i = i+1
        else:
            logger.info("There are no Future PO available in the table")