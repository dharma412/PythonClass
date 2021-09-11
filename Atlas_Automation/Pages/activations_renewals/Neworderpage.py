import time

from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from robot.api import logger

from AtlasTestConstants import ATLAS_CUSTOMER_DATA
from SeleniumHelper import SeleniumHelper

class Neworderpage:
    ''' Page object model for altas Neworder page i.e atlas/neworder_page/'''
    def __init__(self):
        self.txt_customer = By.ID,'cst_name'
        self.txt_contract_number = By.ID,'contract_num'
        self.txt_quantity = By.ID,'id_qty'
        self.txt_purchase_order = By.ID,'pur_order'
        self.txt_sales_order = By.ID,'sales_order'
        self.txt_deal_id= By.ID,'deal_id'
        self.drp_customer_type = By.ID,'customer_type'
        self.drp_dc_sub_type= By.ID,'dc_type'
        self.txt_customer_email_address = By.ID,'cust_email'
        self.txt_partner_name = By.ID,'partner_name'
        self.txt_partner_email=By.ID,'partner_email'
        self.txt_se_name = By.ID,'se_name'
        self.txt_se_email = By.ID,'se_email'
        self.txt_acc_manager_name = By.ID,'am_name'
        self.txt_acc_manager_email = By.ID,'am_email'
        self.txt_bill_name = By.ID,'bill_name'
        self.txt_bill_addr = By.ID,'bill_addr'
        self.txt_bill_email = By.ID,'bill_email'
        self.txt_ship_addr = By.ID,'ship_addr'
        self.txt_alerts_notification=By.ID,'alert_email'
        self.txt_start_date = By.ID,'start_date'
        self.txt_end_date = By.ID,'end_date'
        self.drp_feature_type = By.XPATH,'//*[@id="feature_type"]'
        self.btn_save= By.ID,'save'
        self.table_po_report=By.XPATH,'//*[@id="po_report"]/dl/dd/div[2]/table/tbody/tr'
        self.btn_po_order=By.NAME,'poorder'
        self.drp_add_on_feature_type=By.XPATH,'//*[@id="add_on_feat"]'
        self.txt_add_on_start_date = By.ID, 'add_on_start_date'
        self.txt_add_on_end_date = By.ID, 'add_on_end_date'

    def input_customer(self, customername):
        """
        Purpose: sends the input customer to customer name text box

        Args:
            customername  : name of customer to be created
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_customer,customername)

    def input_contract_number(self, contractnumber):
        """
        Purpose: sends the input contractnumber  to contract number text box

        Args:
            contractnumber  : input contract number
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_contract_number,contractnumber)

    def input_quantity(self, quantity):
        """
        Purpose: sends the input quantity  to quantity text box

        Args:
            quantity  : inputs quantity
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_quantity,quantity)

    def input_purchase_order(self, purchaseorder):
        """
        Purpose: sends the input purchase order name to purchase order text box

        Args:
            purchaseorder  : input  purchase order 
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_purchase_order,purchaseorder)

    def input_sales_order(self, salesorder):
        """
        Purpose: sends the input sales order name to sales order text box

        Args:
            salesorder  : inputs sales order
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_sales_order,salesorder)

    def input_deal_id(self, dealid):
        """
        Purpose: sends the input deal id to deal id text box

        Args:
            dealid   : inputs deal id in to deal id text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_deal_id,dealid)

    def select_dc_customer_type_by_index(self, index):
        """
        Purpose: selects the customer type using index

        Args:
            index   : index of the customer type in drop down
        Returns:
            None
        """
        SeleniumHelper.select_by_index_from_dropdown(self.drp_customer_type,index)

    def select_dc_sub_type_by_index(self, index):
        """
        Purpose: selects the datacenter sub type using index

        Args:
            index   : index of the datacenter sub type in drop down
        Returns:
            None
        """
        SeleniumHelper.select_by_index_from_dropdown(self.drp_dc_sub_type,index)

    def input_customer_email_address(self, emailaddress):
        """
        Purpose: sets customers email address

        Args:
            emailaddress  : inputs email address in to email address text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_customer_email_address,emailaddress)

    def input_partner_name(self, partnername):
        """
        Purpose: sets patners name

        Args:
            partnername  : inputs partner name in to partner name text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_partner_name,partnername)

    def input_partner_email(self, email):
        """
        Purpose: sets partner email address

        Args:
            email  : inputs partner email address in to partner email address text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_partner_email,email)

    def input_se_name(self,sename):
        """
        Purpose: sets sales engineer name

        Args:
            sename  : inputs sales engineer name in to SE Name text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_se_name,sename)

    def input_se_email(self,seemail):
        """
        Purpose: sets sales engineer email address

        Args:
            seemail  : inputs se email address in to SE email address text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_se_email,seemail)

    def input_acc_manager_name(self, accmanagername):
        """
        Purpose: sets account manager name

        Args:
            accmanagername  : inputs account manager name in to Account manager Name text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_acc_manager_name,accmanagername)

    def input_acc_manager_email(self,accmanageremail):
        """
        Purpose: sets account manager email

        Args:
            accmanageremail  : inputs account manager email in to Account manager email text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_acc_manager_email,accmanageremail)

    def input_bill_name(self, bill_name):
        """
        Purpose: sets bill to name

        Args:
            bill_name  : inputs bill to name  in to Bill to Name text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_bill_name,bill_name)

    def input_bill_email(self,billemail):
        """
        Purpose: sets bill to email

        Args:
            billemail  : inputs bill to email  in to Bill to Email text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_bill_email,billemail)

    def input_bill_address(self,billaddress):
        """
        Purpose: sets bill address

        Args:
            billaddress  : inputs bill to address  in to Bill to Address text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_bill_addr,billaddress)

    def input_alerts_notification(self,alterNotification):
        """
        Purpose: sets bill address

        Args:
            alterNotification  : inputs bill to address  in to Bill to Address text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_alerts_notification,alterNotification)

    def input_ship_addr(self,shipaddress):
        """
        Purpose: sets ship to address field

        Args:
            shipaddress  : inputs ship address  in to ship to Address text box
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_ship_addr,shipaddress)

    def input_bundle_start_date(self, bundlestartdate):
        """
        Purpose: sets bundle start date 

        Args:
            bundlestartdate  : inputs bundle start date
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_start_date,bundlestartdate)

    def input_bundle_add_on_start_date(self, bundlestartdate):
        """
        Purpose: sets add on bundle start date

        Args:
            bundlestartdate  : inputs add on bundle start date
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_start_date,bundlestartdate)

    def input_bundle_end_date(self, bundleenddate):
        """
        Purpose: sets bundle end date

        Args:
            bundleenddate  : inputs bundle end date
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_end_date,bundleenddate)

    def input_bundle_add_on_end_date(self, bundleenddate):
        """
        Purpose: sets bundle end date

        Args:
            bundleenddate  : inputs bundle end date
        Returns:
            None
        """
        SeleniumHelper.send_keys(self.txt_end_date,bundleenddate)

    def select_bundle_index(self,bundleidx):
        """
        Purpose: sets bundle index

        Args:
            bundleidx  : index of  bundle in drop down
        Returns:
            None
        """
        SeleniumHelper.select_by_index_from_dropdown(self.drp_feature_type,bundleidx)

    def select_addon_bundle_index(self,bundleidx):
        """
        Purpose: sets bundle index

        Args:
            bundleidx  : index of  bundle in drop down
        Returns:
            None
        """
        SeleniumHelper.select_by_index_from_dropdown(self.drp_add_on_feature_type,bundleidx)

    def save_new_order(self):
        """
        Purpose: saves the order

        Args:
            None
        Returns:
            None
        """
        SeleniumHelper.click_element(self.btn_save)
  
    def create_default_customer(self,feature=None):
        """
        Purpose: creates the customer from customer json

        Args:
            None
        Returns:
            None
        """
        self.input_customer(ATLAS_CUSTOMER_DATA.customer_name)
        self.input_contract_number(ATLAS_CUSTOMER_DATA.contract_number)
        self.input_quantity(ATLAS_CUSTOMER_DATA.quantity)
        self.input_purchase_order(ATLAS_CUSTOMER_DATA.purchase_order)
        self.input_sales_order(ATLAS_CUSTOMER_DATA.sales_order)
        self.input_deal_id(ATLAS_CUSTOMER_DATA.deal_id)
        self.select_dc_customer_type_by_index(ATLAS_CUSTOMER_DATA.customer_type)
        self.select_dc_sub_type_by_index(ATLAS_CUSTOMER_DATA.customer_subtype)
        self.input_customer_email_address(ATLAS_CUSTOMER_DATA.customer_email)
        self.input_partner_name(ATLAS_CUSTOMER_DATA.partner_name)
        self.input_partner_email(ATLAS_CUSTOMER_DATA.partner_email)
        self.input_se_name(ATLAS_CUSTOMER_DATA.se_name)
        self.input_se_email(ATLAS_CUSTOMER_DATA.se_email)
        self.input_acc_manager_name(ATLAS_CUSTOMER_DATA.account_manager_name)
        self.input_acc_manager_email(ATLAS_CUSTOMER_DATA.account_manager_email)
        self.input_bill_name(ATLAS_CUSTOMER_DATA.bill_to_name)
        self.input_bill_email(ATLAS_CUSTOMER_DATA.bill_to_email)
        self.input_bill_address(ATLAS_CUSTOMER_DATA.bill_to_address)
        self.input_alerts_notification(ATLAS_CUSTOMER_DATA.alerts_notifications)
        self.input_ship_addr(ATLAS_CUSTOMER_DATA.ship_to_address)
        self.input_bundle_start_date(datetime.today().strftime("%m/%d/%Y"))
        self.input_bundle_end_date((datetime.today()+timedelta(days=90)).strftime("%m/%d/%Y"))
        if feature==None:
            self.select_bundle_index("3")
        else:
            self.select_bundle_index(feature)
        self.save_new_order()

    def verify_future_order(self,typeBundle=None):
        rows_customer_po_report = len(SeleniumHelper.get_web_elements(self.table_po_report))
        return rows_customer_po_report



    def addnewpo_feature(self,purchaseorder,salesorder,feature):
        """
            Purpose: Add new PO with feature bundle

            Args:
                None
            Returns:
                None
        """
        SeleniumHelper.click_element(self.btn_po_order)
        self.input_purchase_order(purchaseorder)
        self.input_sales_order(salesorder)
        self.input_bundle_start_date((datetime.today() + timedelta(days=2)).strftime("%m/%d/%Y"))
        self.input_bundle_end_date((datetime.today() + timedelta(days=90)).strftime("%m/%d/%Y"))
        self.select_bundle_index(feature)
        self.save_new_order()

    def addnewpo_addon_feature(self,purchaseorder,salesorder,feature):
        """
            Purpose: Add new PO with add on feature bundle

            Args:
                None
            Returns:
                None
        """
        SeleniumHelper.click_element(self.btn_po_order)
        self.input_purchase_order(purchaseorder)
        self.input_sales_order(salesorder)
        self.select_bundle_index(feature)
        self.input_bundle_add_on_start_date((datetime.today() + timedelta(days=2)).strftime("%m/%d/%Y"))
        self.input_bundle_add_on_end_date((datetime.today() + timedelta(days=90)).strftime("%m/%d/%Y"))
        self.save_new_order()



