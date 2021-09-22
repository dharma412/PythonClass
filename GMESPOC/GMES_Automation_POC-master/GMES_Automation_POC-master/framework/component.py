'''
Created on Mar 10, 2019

@author: 29265
'''
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import json
import logging
import os
import shutil
import subprocess
import pandas as pd
import pyodbc
import random
import autoit

import requests
from xml.dom import minidom
from lxml import etree

from framework.utils import Utilities as util
from framework.common_functions import CommonFunctions as common_functions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

IMPLICIT_WAIT_DEFAULT = 10

logging.basicConfig()
log = logging.getLogger("LOG")

class GMESComp:
    IMPLICIT_WAIT_DEFAULT = 10

    def sum(self,b):
        #self.a=a
        self.b=b
        c=b+1
        return c


    def ValidateConfiguration(self,json_string):
        result = True

        json_data = json.loads(json_string)
        tc_id=json_data['tc_id']

        global details_dict
        ROOT_DIR = util.get_root_dir()
        config_file_path = ROOT_DIR + '\\config.properties'
        #print(config_file_path)
        config = util.loadConfigFile(config_file_path)
        details_dict = dict(config.items('Env Details'))

        UIPATH_ROOT_DIR_NAME = details_dict['configcheckrootdirname']
        UIPATH_ROOT_DIR = ROOT_DIR + '\\..\\' + UIPATH_ROOT_DIR_NAME
        if json_data['execute_uipath'] == 'True':
            uipath_xaml_file = json_data['uipath_xaml_file']
            uipath_batch_file = UIPATH_ROOT_DIR + "\\" + details_dict['configcheckexecutable']
            uipath_xaml_file_path = UIPATH_ROOT_DIR + "\\" + uipath_xaml_file
            #local_cmd = "cmd /c " + invoke_message_processor_path + " " + local_inbound_file
            local_cmd = uipath_batch_file + " " + uipath_xaml_file_path
            return_code = util.run_win_cmd(local_cmd)

            if return_code is None:
                util.html_print("Successfully executed config check")
            else:
                util.html_print("Failed to execute config check")
                return False

        configCheckWorkBook = details_dict['configcheckworkbook']
        configCheckResultSheetName = details_dict['configcheckresultsheetname']

        configTestResult = pd.read_excel(UIPATH_ROOT_DIR + '\\' + configCheckWorkBook,
                           sheet_name=configCheckResultSheetName)
        configTestResult = configTestResult.dropna(subset=['TC_ID'])

        util.html_print("Configuration Check Validation results:")
        for index, row in configTestResult.iterrows():
            # print(row)
            #print(row['TC_ID'], row['Status'])
            test_result_tc_id = row['TC_ID'].split('_')[0]
            #print(test_result_tc_id, test_result_status)
            if tc_id == test_result_tc_id:
                test_result_status = row['Status']
                test_result_description = row['Test Case Name']
                if 'PASS' == test_result_status:
                    util.html_print(test_result_description + ": PASS")
                else:
                    util.html_print(test_result_description + ": FAIL")
                    result = False

        if result is False:
            util.html_print("Configuration Check Validation Failed!")

        return result


    def wait_for_async_processing(self):
        #util.wait_for_not_displayed("//img[@id='DisableForm' and contains(@style,'visibility: visible')]", driver)
        #util.wait_for_not_displayed("//div[@class='LoadingOverlay' and contains(@style,'display: block')]", driver)
        util.wait_for_ajax(driver)


    def fetch_db_data(self,query, key=None, var_list=None):
        cnxn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};Server=10.6.14.138;UID=FlxAdmin;PWD=FlxAdmin;Database=TaOFlexNet_BR4.18;")
        df = pd.read_sql_query(query, cnxn, params=var_list)

        result_set = []
        for index, row in df.iterrows():
            result_set.append(row[key])

        return result_set


    def OpenBrowser(self,json_string):
        result = True
        json_data = json.loads(json_string)

        time.sleep(5)
        local_cmd = "taskkill /f /im iexplore.exe & taskkill /f /im IEDriverServer.exe"
        #util.run_win_cmd(local_cmd)
        time.sleep(5)

        global driver
        #global ROOT_DIR
        cap = DesiredCapabilities().INTERNETEXPLORER
        cap['platform'] = "windows"
        cap['version'] = "11"
        cap['browserName'] = "internet explorer"
        cap['ignoreProtectedModeSettings'] = True
        cap['IntroduceInstabilityByIgnoringProtectedModeSettings'] = True
        cap['nativeEvents'] = True
        cap['ignoreZoomSetting'] = True
        cap['requireWindowFocus'] = True
        cap['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
        #ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ROOT_DIR = util.get_root_dir()
        DRIVER_PATH = ROOT_DIR + "\\Resources\\Drivers\\IEDriverServer.exe"
        #driver = webdriver.Ie(desired_capabilities=cap, executable_path="D:\\workspace\\GMES-master\\Resources\\Drivers\\IEDriverServer.exe")

        driver = webdriver.Ie(desired_capabilities=cap,
                              executable_path=DRIVER_PATH)

        #time.sleep(5)
        driver.maximize_window()
        driver.execute_script("document.body.style.zoom='100%'")
        driver.implicitly_wait(self.IMPLICIT_WAIT_DEFAULT)
        #pyHandle = driver.window_handles[0]
        #driver.switch_to.window(pyHandle)
        #driver.switch_to_window(driver.current_window_handle)
        # driver=webdriver.Chrome("D:\\IEDriverServer.exe")

        #try:
            #time.sleep(5)
        #    autoit.opt("WinTitleMatchMode", 2)
        #    autoit.win_wait_active("Internet Explorer",5)
        #except:
        #    autoit.win_activate("Internet Explorer")

        return result


    def Login(self, json_string):
        result = True
        json_data = json.loads(json_string)

        driver.get("http://192.168.240.213/Apriso/Portal/Kiosk/Login.aspx")

        elem = driver.find_element_by_xpath("(//*[@class='PopupInput input'])[1]")
        #time.sleep(5)
        elem.send_keys(json_data['username'])
        elem = driver.find_element_by_xpath("(//*[@class='PopupInput input'])[2]")
        elem.send_keys(json_data['password'])
        driver.find_element_by_xpath("//*[@value='Log In']").click()
        #time.sleep(5)
        #driver.quit()
        self.wait_for_async_processing()

        return result


    def SelectMenu(self,json_string):
        result = True
        json_data = json.loads(json_string)

        menu_path = json_data['menu_path']
        menu_list = menu_path.split(" => ")

        for menu_item in menu_list:
            menu_item = menu_item.strip()
            if menu_item != "":
                ele_menu_item = driver.find_element_by_link_text(menu_item)
                driver.execute_script('arguments[0].scrollIntoView(true);', ele_menu_item)
                ele_menu_item.click()
                util.html_print("Clicked on menu item: " + menu_item)

        time.sleep(5)
        return result


    def PMCreation(self,json_string):
        result=True
        json_data = json.loads(json_string)
        util.html_print(json_data['workcenter'])

        driver.find_element_by_xpath("//a[contains(@title, 'BAT Operations')]").click()
        driver.find_element_by_xpath("(//a[contains(@title, 'UIUX Operations')])[1]").click()
        driver.find_element_by_xpath("//a[contains(@id, 'TC_Operator Portal UIUXLink')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'GeExternaltInputs_WorkCenter')]").send_keys(json_data['workcenter'])
        driver.find_element_by_xpath("//span[text() = 'OK']").click()
        driver.find_element_by_xpath("//button[@value='IWS']").click()
        time.sleep(4)
        driver.find_element_by_xpath("//*[@class='ToolButton CREATE']").click()

        util.html_print(json_string)
        log.info(json_data)

        xpath_failure_type = "//*[text()='" + json_data['failure_type'] + "']"

        driver.find_element_by_xpath(xpath_failure_type).click()
        #ele_temp = driver.find_element_by_xpath(xpath_failure_type)
        #driver.execute_script("arguments[0].click", ele_temp)

        time.sleep(2)
        common_functions.select_option_from_dropdown_by_text(driver, 'xpath',
                                                 "//*[contains(@id,'PMCardPage1Parameters_FunctionalLocNo')]",
                                                 json_data['functional_location_number'])

        time.sleep(2)
        common_functions.select_option_from_dropdown_by_text(driver, 'xpath',
                                                 "//*[contains(@id,'PMCardPage1Parameters_EquipmentNo')]",
                                                 json_data['equipment_number'])

        time.sleep(2)
        common_functions.select_option_from_dropdown_by_text(driver, 'xpath',
                                                 "//*[contains(@id,'PMCardPage1Parameters_Component')]",
                                                 json_data['component'])

        time.sleep(2)
        driver.find_element_by_xpath("//*[@type='text' and contains(@id,'PMCardPage1Parameters_DownTimeEnd')]").click()

        time.sleep(2)
        driver.find_element_by_xpath("//*[@type='text' and contains(@id,'PMCardPage1Parameters_RepairTimeEnd')]").click()

        time.sleep(2)
        driver.find_element_by_xpath("//*[contains(@id,'PMCardPage1Parameters_WorkOrderNo')]").send_keys(
            json_data['work_order_number'])

        time.sleep(2)
        driver.find_element_by_xpath("//*[contains(@id,'PMCardPage1Parameters_WhatHappened1')]").send_keys(
            json_data['what_happened_headline'])

        time.sleep(2)
        driver.find_element_by_xpath("//*[contains(@id,'PMCardPage1Parameters_WhatHappened2')]").send_keys(
            json_data['what_happened_note'])

        time.sleep(2)
        driver.find_element_by_xpath("//*[contains(@id,'PMCardPage1Parameters_HowRepaired')]").send_keys(
            json_data['how_repaired'])

        time.sleep(2)
        driver.find_element_by_xpath("//*[contains(@id,'PMCardPage1Parameters_ItemsChecked')]").send_keys(
            json_data['items_checked'])

        time.sleep(2)
        driver.find_element_by_xpath("//*[contains(@id,'PMCardPage1Parameters_Results')]").send_keys(
            json_data['results'])

        time.sleep(2)
        common_functions.select_option_from_dropdown_by_text(driver, 'xpath',
                                                 "//*[contains(@id,'PMCardPage1Parameters_ObjectPart')]",
                                                 json_data['object_part'])

        time.sleep(2)
        common_functions.select_option_from_dropdown_by_text(driver, 'xpath',
                                                 "//*[contains(@id,'PMCardPage1Parameters_DamageCode')]",
                                                 json_data['damage_code'])

        time.sleep(2)
        common_functions.select_option_from_dropdown_by_text(driver, 'xpath',
                                                 "//*[contains(@id,'PMCardPage1Parameters_ActivityPM')]",
                                                 json_data['activity_pm'])

        time.sleep(2)
        common_functions.select_option_from_dropdown_by_text(driver, 'xpath',
                                                 "//*[contains(@id,'PMCardPage1Parameters_CauseCode')]",
                                                 json_data['cause_code'])

        time.sleep(2)
        driver.find_element_by_xpath("//*[text()='Save and Close']").click()

        time.sleep(10)
        #self.OP_Home()
        #self.OP_Exit()

        #self.Logout()
        return result


    def PMCardOnOperatorPortal(self,data):
        result=True
        time.sleep(5)
        global pmno

        pmno=driver.find_element_by_xpath("(//table//tr//span)[7]").text

        if len(pmno)<=0:
            result=False
        else:
            util.html_print("PM Card No. has been validated: " + pmno)
        return result
        #time.sleep(5)


    def editPmCard(self,data):
        result=True
        driver.find_element_by_xpath("(//table//tr//span)[7]").click()
        time.sleep(2)
        driver.find_element_by_xpath("// span[text() = 'Edit PM Card']").click()
        time.sleep(5)
        driver.find_element_by_xpath("//*[contains(@id,'PMCardPage1Parameters_WhatHappened1')]").send_keys('_Test')
        time.sleep(2)
        result=driver.find_element_by_xpath("//*[text() = 'Print']").is_displayed()
        time.sleep(3)
        driver.find_element_by_xpath("//*[text()='Save and Close']").click()

        time.sleep(10)

        return result


    def BDALogValidation(self,data):
        result=True
        driver.find_element_by_xpath("// *[text() = 'Home']").click()
        time.sleep(2)
        driver.find_element_by_xpath("// *[text() = 'Exit']").click()
        time.sleep(2)
      #  driver.find_element_by_xpath("//a[contains(@id, 'TC_Operator Portal UIUXLink')]").click()
       # time.sleep(3)
        driver.find_element_by_xpath("// a[@title= 'Navigate up one level']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[text()='BDELOG']").click()
        time.sleep(6)

        driver.find_element_by_xpath("//input[@data-field='bdnumber']").send_keys(pmno)
        time.sleep(2)
        driver.find_element_by_xpath("//input[@data-field='bdnumber']").send_keys(u'\ue007')
        time.sleep(2)

        result=driver.find_element_by_xpath("// *[text() = '"+pmno+"']").is_displayed()

        if result == True:
            util.html_print("PM Card No.: " + pmno + " is validated in the BDE Log with status as Open")

        time.sleep(2)
        return result


    def Copy_Latest_Outbound_File(self, outbound_type):
        latest_file_folder = "\\\\192.168.240.213\\Output\\" + outbound_type
        latest_file = util.newest(latest_file_folder)
        if (latest_file != None):
            util.html_print("Found latest file: " + latest_file)
        else:
            util.html_print("Could not find a latest file")
            result = False

        ROOT_DIR = util.get_root_dir()
        local_outbound_file = ROOT_DIR + "\\user_files\\outbound\\" + os.path.basename(latest_file)
        shutil.copy(latest_file, local_outbound_file)

        return local_outbound_file


    def Get_Latest_Local_Outbound_File(self):
        ROOT_DIR = util.get_root_dir()
        latest_file_folder = ROOT_DIR + "\\user_files\\outbound\\"
        latest_file = util.newest(latest_file_folder)
        if (latest_file != None):
            util.html_print("Found latest file: " + latest_file)
        else:
            util.html_print("Could not find a latest file")
            result = False

        local_outbound_file = ROOT_DIR + "\\user_files\\outbound\\" + os.path.basename(latest_file)

        return local_outbound_file


    def PM_Card_Outbound_Validation(self,json_string):
        result=True
        json_data = json.loads(json_string)
        latest_file = util.newest('\\\\192.168.240.213\\Output\\PlantNotification')
        if(latest_file!=None):
            util.html_print("Found latest file: " + latest_file)
        else:
            util.html_print("Could not find a latest file")
            result=False

        ROOT_DIR = util.get_root_dir()
        local_outbound_file = ROOT_DIR + "\\user_files\\outbound\\" + os.path.basename(latest_file)
        shutil.copy(latest_file, local_outbound_file)

        xml_message = self.get_outbound_message_data('PlantNotification', pmno)
        if 'xmlFile not found' not in xml_message:
            print("Found Outbound PlantNotification xml for " + pmno)
        else:
            print("Could not find Outbound PlantNotification xml for " + pmno)
            return False

        #pmno="PM1001107"
        outbound_pm_no = util.get_xml_tag_data_from_string(xml_message, json_data['GMESDowntimeMessageNumber'])
        if outbound_pm_no == pmno:
            util.html_print("Expected Outbound PM Card No.: " + pmno + "; Actual PM Card No.: " + outbound_pm_no)
            util.html_print("Validated outbound PM Card No in xml successfully!")
        else:
            util.html_print("Expected Outbound PM Card No.: " + pmno + "; Actual PM Card No.: " + outbound_pm_no)
            util.html_print("Failed to validate Outbound PM Card No in xml")
            result=False


        #open(latest_file)

        return result


    def PM_Card_Publish_Notification_Confirmation(self,json_string):
        result=True
        json_data = json.loads(json_string)

        #pmno="PM1001107"
        ROOT_DIR = util.get_root_dir()
        local_inbound_file = ROOT_DIR + "\\user_files\\inbound\\" + json_data['inbound_file']

        util.set_xml_tag_text(local_inbound_file,json_data['tag_name'],pmno)

        invoke_message_processor_path = ROOT_DIR + "\\Resources\\Utilities\\InvokeMessageProcesserUtility.exe"
        #local_cmd = "cmd /c " + invoke_message_processor_path + " " + local_inbound_file
        local_cmd = invoke_message_processor_path + " " + local_inbound_file
        return_code = util.run_win_cmd(local_cmd)

        if(return_code is None):
            util.html_print("Successfully published PM Card Notification Confirmation for PM Card No.: " + pmno)
        else:
            util.html_print("Failed to publish PM Card Notification Confirmation for PM Card No.: " + pmno)
            result=False

        return result


    def PM_Card_Validate_Notification_Confirmation(self, json_string):
        result=True
        json_data = json.loads(json_string)

        driver.find_element_by_xpath("//a[@id='ctl04_TC_FlexNet.Portal.BackLink']").click()

        driver.find_element_by_xpath("//*[text()='BDELOG']").click()
        time.sleep(6)

        driver.find_element_by_xpath("//input[@data-field='bdnumber']").send_keys(pmno)
        time.sleep(3)
        driver.find_element_by_xpath("//input[@data-field='bdnumber']").send_keys(u'\ue007')
        time.sleep(3)

        notification_no = driver.find_element_by_xpath(
            "//*[@data-field='notificationno']//span").text

        #pmno="PM100107"
        util.html_print("Expected Notification No.: " + json_data[
            'master_notification_no'] + "; Actual Notification No.: " + notification_no)
        if notification_no == json_data['master_notification_no']:
            util.html_print("Successfully validated notification no.: " + notification_no + " for PM Card No.: " + pmno)
        else:
            util.html_print("Failed to validate notification no.: " + notification_no + " for PM Card No.: " + pmno)
            result = False

        time.sleep(5)
        return result


    def Navigate_to_Operator_Portal(self):
        self.wait_for_async_processing()
        driver.find_element_by_xpath("//a[contains(@title, 'BAT Operations')]").click()
        self.wait_for_async_processing()
        driver.find_element_by_xpath("(//a[contains(@title, 'UIUX Operations')])[1]").click()
        self.wait_for_async_processing()
        driver.find_element_by_xpath("//a[contains(@id, 'TC_Operator Portal UIUXLink')]").click()
        self.wait_for_async_processing()


    def Navigate_to_Work_Center(self,workcenter):
        self.Navigate_to_Operator_Portal()
        driver.find_element_by_xpath("//input[contains(@id, 'GeExternaltInputs_WorkCenter')]").send_keys(workcenter)
        driver.find_element_by_xpath("//span[text() = 'OK']").click()
        self.wait_for_async_processing()


    def Navigate_to_OP_Tab(self,op_tab):
        result = False
        #op_tab_xpath = "//button[@value='" + op_tab + "']//span[not(@class='oppActiveTab')]"

        self.wait_for_async_processing()
        op_tab_xpath = "//button[@value='" + op_tab + "']"
        ele_list_opp_tab = driver.find_elements_by_xpath(op_tab_xpath)
        if len(ele_list_opp_tab) > 0:
            ele_list_opp_tab[0].click()
            self.wait_for_async_processing()
            result = True
        else:
            op_tab_xpath = "//button[@value='" + op_tab + "']//span[@class='oppActiveTab']"
            ele_list_opp_tab = driver.find_elements_by_xpath(op_tab_xpath)
            if len(ele_list_opp_tab) > 0:
                result = True

        return result


    def Navigate_to_Maker_Packer(self,maker_packer):
        maker_packer_tab_xpath = "//span[text()='" + maker_packer + "']"
        found = False
        tab_counter = 1
        while not found:
            ele_list_maker_packer_tab = driver.find_elements_by_xpath(maker_packer_tab_xpath)
            if len(ele_list_maker_packer_tab) > 0:
                found = True
            else:
                if tab_counter < 3:
                    driver.find_element_by_xpath("//a[contains(@class,'maker_packer_btn_left')]").click()
                    tab_counter = tab_counter + 1
                    self.wait_for_async_processing()
                else:
                    break

        return found


    def Select_PO(self,po_number):
        selected = False
        found_index = -1

        self.wait_for_async_processing()
        current_product_number_xpath = "//div[@data-portal-view='SF_ProductionHeaderUI_SingleData']//td[@data-field='productno']//span"
        ele_current_product_number = driver.find_element_by_xpath(current_product_number_xpath)
        po_number_xpath = "//tr[contains(@class,'OprStatus')]//td[@data-field='wipordernolistdisp']//span[text()='" + po_number + "']"
        po_number_xpath_already_selected = "//tr[contains(@class,'selected')]//td[@data-field='wipordernolistdisp']//span[text()='" + po_number + "']"
        product_number_relative_xpath = "./ancestor::td/following-sibling::td[@data-field='productnolist']//span"

        while not selected:
            ele_list_po_number = driver.find_elements_by_xpath(po_number_xpath)
            if len(ele_list_po_number) > 0:
                ele_product_number = ele_list_po_number[0].find_element_by_xpath(product_number_relative_xpath)
                if ele_product_number.text != ele_current_product_number.text:
                    ele_list_po_number_already_selected = driver.find_elements_by_xpath(po_number_xpath_already_selected)
                    if len(ele_list_po_number_already_selected) == 0:
                        ele_list_po_number[0].click()
                    selected = True
                    util.html_print("Selected PO: " + po_number)
                else:
                    util.html_print(
                        "Cannot proceed! PO to be selected has the same product number as that of current PO")
            else:
                ele_list_page_next = driver.find_elements_by_xpath("//button[contains(@class,'action_page_next') and not(@disabled)]")
                if len(ele_list_page_next) > 0:
                    ele_list_page_next[0].click()
                else:
                    break

        return selected


    def get_po_no_from_loipro(self,loipro_file_name):
        ROOT_DIR = util.get_root_dir()
        loipro_file = ROOT_DIR + "\\user_files\\" + loipro_file_name
        fetched_po_number = util.get_xml_tag_data(loipro_file,'AUFNR') or util.get_xml_tag_data(loipro_file, 'OrderNumber')
        return fetched_po_number








    def get_outbound_message_data(self, msg_type, uid):
        server_name = "192.168.240.213"
        mock_automation_service_port = "8383"
        url = "http://" + server_name + ":" + mock_automation_service_port + "/AutomationTest/services/AutomationServiceImpl"
        # headers = {'content-type': 'application/soap+xml'}
        headers = {'Accept': 'text/xml', 'content-type': 'text/xml',
                   'SoapAction': 'http://tempuri.org/IFlexNetMessageProcessor/ProcessMessage'}
        body = ('<?xml version="1.0" encoding="UTF-8"?>'
                '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://webservices.automation.com">'
                '<soapenv:Header/>'
                '<soapenv:Body>'
                '<web:getRequestIdentifier>'
                '<web:messageType>' + msg_type + '</web:messageType>'
                                                 '<web:uniqueIdentifiers>' + uid + '</web:uniqueIdentifiers>'
                                                                                   '</web:getRequestIdentifier>'
                                                                                   '</soapenv:Body>'
                                                                                   '</soapenv:Envelope>')

        response = requests.post(url, data=body, headers=headers)

        doc = minidom.parseString(response.content)
        xmlMessage = util.strip_all_namespaces_from_xml(doc.getElementsByTagName("xmlMessage")[0].firstChild.nodeValue)

        return xmlMessage


    def invoke_process_inbound_message(self, local_inbound_file, inbound_message_type):
        result = True
        server_name = "192.168.240.213"
        url = "http://" + server_name + "/Apriso/MessageProcessor/FlexNetMessageProcessor.svc"
        # headers = {'content-type': 'application/soap+xml'}
        headers = {'Accept': 'text/xml', 'content-type': 'text/xml; charset=utf-8',
                   'SoapAction': 'http://tempuri.org/IFlexNetMessageProcessor/ProcessMessage'}

        xml_message_string = util.get_xml_string_from_file(local_inbound_file)
        body = ('<?xml version="1.0" encoding="UTF-8"?>'
                '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">'
                '<soapenv:Header/>'
                '<soapenv:Body>'
                '<tem:ProcessMessage>'
                '<tem:xmlMessage><![CDATA[' + xml_message_string + ']]></tem:xmlMessage>'
                                                                   '<tem:applicationName>' + server_name + '</tem:applicationName>'
                                                                                                           '</tem:ProcessMessage>'
                                                                                                           '</soapenv:Body>'
                                                                                                           '</soapenv:Envelope>')

        response = requests.post(url, data=body, headers=headers)

        xml_response = util.strip_all_namespaces_from_xml(
            etree.tostring(etree.fromstring(response.content), encoding='utf-8', method='xml', xml_declaration=True,
                           pretty_print=True).decode('utf-8'))
        process_result = util.get_xml_data_by_xpath_from_string(xml_response, "//ProcessMessageResult")
        error_message = util.get_xml_data_by_xpath_from_string(xml_response, "//errorMessage")
        # process_result = get_xml_tag_data_from_string(xml_response,"ProcessMessageResult")
        # error_message = get_xml_tag_data_from_string(xml_response, "errorMessage")

        if process_result == 'true':
            util.html_print("GMES processed Inbound message successfully for: " + inbound_message_type + " xml")
        else:
            util.html_print("GMES Failed to process Inbound message for: " + inbound_message_type + " xml")
            result = False

        if error_message == None:
            util.html_print("No error message")
        else:
            util.html_print("Error message: " + error_message)
            result = False

        return result


    def generate_plant_notification_response(self, xml_message, pm_no, notification_number):
        return True


    def validate_treq_message(self, xml_message, treq_master_data):
        result = True
        try:
            treq_info = {"treq_movement_type":util.get_xml_tag_data_from_string(xml_message, 'MovementType')}
            treq_info.update({"treq_storage_type":util.get_xml_tag_data_from_string(xml_message, 'StorageType')})
            treq_info.update({"treq_storage_bin":util.get_xml_tag_data_from_string(xml_message, 'StorageBin')})
            treq_info.update({"treq_destination_storage_type": util.get_xml_tag_data_from_string(xml_message, 'DestinationStorageType')})
            treq_info.update({"treq_destination_storage_bin": util.get_xml_tag_data_from_string(xml_message, 'DestinationStorageBin')})
            treq_info.update({"treq_warehouse_number": util.get_xml_tag_data_from_string(xml_message, 'WarehouseNumber')})
            treq_info.update({"treq_requirement_number": util.get_xml_tag_data_from_string(xml_message, 'RequirementNumber')})
            treq_info.update({"treq_material_number": util.get_xml_tag_data_from_string(xml_message, 'MaterialNumber')})
            treq_info.update({"treq_plant": util.get_xml_tag_data_from_string(xml_message, 'Plant')})
            treq_info.update({"treq_stock_category": util.get_xml_tag_data_from_string(xml_message, 'StockCategory')})
            treq_info.update({"treq_batch_number": util.get_xml_tag_data_from_string(xml_message, 'BatchNumber')})
            treq_info.update({"treq_quantity": util.get_xml_tag_data_from_string(xml_message, 'QuantityInSKU')})

            for key, value in treq_info.items():
                if value is None:
                    value = ''
                if treq_master_data[key] == '__NOT_EMPTY__':
                    if value != '':
                        util.html_print("Validated " + key + " is not empty and has value: " + value)
                    else:
                        util.html_print("Failed validation: " + key + " is empty or not present")
                        result = False
                else:
                    if treq_master_data[key] == value:
                        util.html_print("Validated " + key + " value: " + value)
                    else:
                        util.html_print("Failed validation of " + key)
                        util.html_print("Expected value: " + treq_master_data[key] + "; Actual value: " + value)
                        result = False
        except Exception as e:
            util.html_print("Exception: " + str(e))
            return False

        return result


    def generate_tord_xml(self, xml_message, orderno, local_inbound_file):
        result = True

        try:
            root = etree.Element('WMTOID02')  # The root element

            IDOC = etree.SubElement(root, "IDOC")
            IDOC.set("BEGIN", "1")
            EDI_DC40 = etree.SubElement(IDOC, "EDI_DC40")
            EDI_DC40.set("SEGMENT", "1")
            TABNAM = etree.SubElement(EDI_DC40, "TABNAM")
            TABNAM.text = "EDI_DC40"
            MANDT = etree.SubElement(EDI_DC40, "MANDT")
            MANDT.text = "170"
            DOCNUM = etree.SubElement(EDI_DC40, "DOCNUM")
            DOCNUM.text = "0000000476939692"
            DOCREL = etree.SubElement(EDI_DC40, "DOCREL")
            DOCREL.text = "731"
            STATUS = etree.SubElement(EDI_DC40, "STATUS")
            STATUS.text = "30"
            DIRECT = etree.SubElement(EDI_DC40, "DIRECT")
            DIRECT.text = "1"
            OUTMOD = etree.SubElement(EDI_DC40, "OUTMOD")
            OUTMOD.text = "4"
            IDOCTYP = etree.SubElement(EDI_DC40, "IDOCTYP")
            IDOCTYP.text = "WMTOID02"
            MESTYP = etree.SubElement(EDI_DC40, "MESTYP")
            MESTYP.text = "WMTORD"
            SNDPOR = etree.SubElement(EDI_DC40, "SNDPOR")
            SNDPOR.text = "SAPT03"
            SNDPRT = etree.SubElement(EDI_DC40, "SNDPRT")
            SNDPRT.text = "LS"
            SNDPRN = etree.SubElement(EDI_DC40, "SNDPRN")
            SNDPRN.text = "T03CLNT170"
            RCVPOR = etree.SubElement(EDI_DC40, "RCVPOR")
            RCVPOR.text = "T21CLNT910"
            RCVPRN = etree.SubElement(EDI_DC40, "RCVPRN")
            RCVPRN.text = "GMES_UBR"

            E1LTORH = etree.SubElement(IDOC, "E1LTORH")
            E1LTORH.set("SEGMENT", "1")
            LGNUM = etree.SubElement(E1LTORH, "LGNUM")
            LGNUM.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                           "//Message/TransferRequirementHeader/WarehouseNumber")
            TANUM = etree.SubElement(E1LTORH, "TANUM")
            TANUM.text = str(random.randint(100000000, 999999999))
            BWLVS = etree.SubElement(E1LTORH, "BWLVS")
            BWLVS.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                           "//Message/TransferRequirementHeader/MovementType")
            BENUM = etree.SubElement(E1LTORH, "BENUM")
            BENUM.text = orderno

            treq_count = int(util.get_xml_nodes_count_by_xpath_from_string(xml_message, "//TransferRequirementItem"))
            for treq_index in range(1, treq_count + 1):
                E1LTORI = etree.SubElement(E1LTORH, "E1LTORI")
                E1LTORI.set("SEGMENT", "1")
                TAPOS = etree.SubElement(E1LTORI, "TAPOS")
                TAPOS.text = "00" + str(treq_index)
                MATNR = etree.SubElement(E1LTORI, "MATNR")
                MATNR.text = "0000000000" + util.get_xml_data_by_xpath_from_string(xml_message,
                                                                              "//Message//TransferRequirementItem[" + str(
                                                                                  treq_index) + "]/MaterialNumber")
                WERKS = etree.SubElement(E1LTORI, "WERKS")
                WERKS.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                               "//Message//TransferRequirementItem[" + str(
                                                                   treq_index) + "]/Plant")
                CHARG = etree.SubElement(E1LTORI, "CHARG")
                CHARG.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                               "//Message//TransferRequirementItem[" + str(
                                                                   treq_index) + "]/BatchNumber")
                BESTQ = etree.SubElement(E1LTORI, "BESTQ")
                BESTQ.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                               "//Message//TransferRequirementItem[" + str(
                                                                   treq_index) + "]/StockCategory")
                SOBKZ = etree.SubElement(E1LTORI, "SOBKZ")
                SOBKZ.text = ""
                MEINS = etree.SubElement(E1LTORI, "MEINS")
                MEINS.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                               "//Message//TransferRequirementItem[" + str(
                                                                   treq_index) + "]/UnitOfMeasure")
                ABLAD = etree.SubElement(E1LTORI, "ABLAD")
                if BWLVS.text == "932":
                    ABLAD.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                                   "//Message//DestinationStorageBin")
                else:
                    ABLAD.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                                   "//Message//TransferRequirementItem[" + str(
                                                                       treq_index) + "]/UnloadingPoint")
                VLTYP = etree.SubElement(E1LTORI, "VLTYP")
                VLTYP.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                               "//Message//StorageType")
                VLPLA = etree.SubElement(E1LTORI, "VLPLA")
                VLPLA.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                               "//Message//StorageBin")
                NLTYP = etree.SubElement(E1LTORI, "NLTYP")
                NLTYP.text = "100"
                NLPLA = etree.SubElement(E1LTORI, "NLPLA")
                NLPLA.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                               "//Message//DestinationStorageBin")
                NSOLM = etree.SubElement(E1LTORI, "NSOLM")
                NSOLM.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                               "//Message//TransferRequirementItem[" + str(
                                                                   treq_index) + "]/QuantityInSKU")
                VLENR = etree.SubElement(E1LTORI, "VLENR")
                VLENR.text = "L3Test" + str(random.randint(1000, 9999))

                global container
                container = VLENR.text
                LGORT = etree.SubElement(E1LTORI, "LGORT")
                LGORT.text = util.get_xml_data_by_xpath_from_string(xml_message,
                                                               "//Message//TransferRequirementItem[" + str(
                                                                   treq_index) + "]/StorageLocation")

            etree.ElementTree(root).write(local_inbound_file, encoding='utf-8', xml_declaration=True, pretty_print=True)

        except Exception as e:
            util.html_print("Exception: " + str(e))
            util.html_print("Failed to generate TORD xml for TREQ order number: " + orderno)
            result = False

        return result


    def gmes_message_processing(self, msg_type, uid, publish_inbound_file=False, local_inbound_file=None,
                                inbound_message_type=None, var_list_dict=None):
        result = True
        xml_message = self.get_outbound_message_data(msg_type, uid)
        if 'xmlFile not found' not in xml_message:
            util.html_print("Found Outbound " + msg_type + " xml for " + uid)
        else:
            util.html_print("Could not find Outbound " + msg_type + " xml for " + uid)
            return False

        if msg_type == 'PlantNotification':
            result = self.generate_plant_notification_response(xml_message, uid, var_list_dict['notification_number'])
            pass
        elif msg_type == 'ProductionOrderData':
            pod_event = util.get_xml_tag_attribute_value_from_string(xml_message, 'ProductionOrderData', 'Event')
            util.html_print("Expected ProductionOrderData event: " + var_list_dict[
                'pod_event'] + "; Actual ProductionOrderData event: " + pod_event)
            if pod_event == var_list_dict['pod_event']:
                util.html_print("Validated outbound ProductionOrderData event")
            else:
                util.html_print("Failed to validate outbound ProductionOrderData event")
                return False
        elif msg_type == 'TransferRequirement':
            if var_list_dict['treq_requirement_number'] == '__DYNAMIC__':
                var_list_dict['treq_requirement_number'] = uid
            result = self.validate_treq_message(xml_message, var_list_dict)
            if result is True:
                util.html_print("Validated TransferRequirement")
            else:
                util.html_print("Failed to validate TransferRequirement")
            result = self.generate_tord_xml(xml_message, uid, local_inbound_file)

        if publish_inbound_file is True:
            if result is True:
                result = self.invoke_process_inbound_message(local_inbound_file, inbound_message_type)
            else:
                util.html_print("Failed to generate " + inbound_message_type + " xml")

        return result





    def SMD_POD_10_OP_Prepare_PO_for_maker(self, json_string):
        result=True

        json_data = json.loads(json_string)
        util.html_print(json_data['workcenter'])

        self.Navigate_to_Work_Center(json_data['workcenter'])

        #driver.find_element_by_xpath("//button[@value='PRODUCTION']").click()
        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        global po_number
        #po_number = "2019443"

        #loipro1_file_name = details_dict['loipro1_file_name']
        #ROOT_DIR = util.get_root_dir()
        #loipro1_file = ROOT_DIR + "\\user_files\\" + loipro1_file_name

        #po_number = util.get_xml_tag_data(loipro1_file,'AUFNR')
        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//button[contains(@class,'PREPARE')]").click()

        ele_list_confirm_button = driver.find_elements_by_xpath("//a[contains(@class,'Button')]//span[text()='Confirm']")
        if len(ele_list_confirm_button) > 0:
            ele_list_confirm_button[0].click()

        self.wait_for_async_processing()
        driver.find_element_by_xpath("//button[@value='BACK']").click()

        driver.find_element_by_xpath("//a[contains(@class,'Button')]//span[text()='Confirm']").click()

        self.wait_for_async_processing()
        po_number_prepared_xpath = "//tr[@data-class='OprStatus100']//td[@data-field='wipordernolistdisp']//span[text()='" + po_number + "']"
        ele_list_po_number_prepared = driver.find_elements_by_xpath(po_number_prepared_xpath)
        if len(ele_list_po_number_prepared) > 0:
            util.html_print("Validated initially prepared PO is displayed with yellow status")
        else:
            util.html_print("Initially prepared PO is not displayed with yellow status")
            return False

        return result


    def ADM_JobHistory_MM_Check_Change_PO_Status_message(self,json_string):
        result = True
        json_data = json.loads(json_string)

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        result = self.gmes_message_processing("ProductionOrderData", po_number, publish_inbound_file=False,
                                         var_list_dict=json_data)

        return result


    def MFG_POD_32_OP_Select_materials_for_preparation_before_brand_change(self, json_string):
        result=True
        #po_number = "2019443"
        json_data = json.loads(json_string)
        #util.html_print(json_data['workcenter'])

        #self.Navigate_to_Work_Center(json_data['workcenter'])

        #driver.find_element_by_xpath("//button[@value='PRODUCTION']").click()
        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//button[contains(@class,'PREPARE')]").click()

        ele_list_confirm_button = driver.find_elements_by_xpath(
            "//a[contains(@class,'Button')]//span[text()='Confirm']")
        if len(ele_list_confirm_button) > 0:
            ele_list_confirm_button[0].click()

        self.wait_for_async_processing()
        ele_list_quantity_input = driver.find_elements_by_xpath("//tbody//tr[not(contains(@class,'Dummy'))]//td[@data-field='quantity']//input")
        if len(ele_list_quantity_input) > 0:
            for index in range(0,len(ele_list_quantity_input)):
                driver.execute_script('arguments[0].scrollIntoView(true);', ele_list_quantity_input[index])
                ele_list_quantity_input[index].clear()
                ele_list_quantity_input[index].send_keys('20')

        ele_replenish_button = driver.find_element_by_xpath("//a[@data-value='REPLENISH']")
        driver.execute_script('arguments[0].scrollIntoView(true);', ele_replenish_button)
        ele_replenish_button.click()
        #driver.find_element_by_xpath("//a[@data-value='REPLENISH']//span").click()

        time.sleep(5)

        return result


    def ADM_JobHistory_MM_Check_trolley_preparation_request_message(self,json_string):
        result = True
        json_data = json.loads(json_string)

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])
        query = "select distinct od.orderno from ORDER_DETAIL od join warehouse_location wl on od.towarehouselocationid=wl.id where od.parentorderno=? and wl.warehouselocationtype=10"
        db_result_set = util.fetch_db_data(query, key='orderno', var_list=[po_number])
        orderno = None
        if json_data['maker_or_packer'] == 'Maker / 0010':
            orderno = db_result_set[0]
        elif json_data['maker_or_packer'] == 'Packer / 0020':
            orderno = db_result_set[1]

        ROOT_DIR = util.get_root_dir()
        local_inbound_file = ROOT_DIR + "\\user_files\\inbound\\response_output.xml"

        result = self.gmes_message_processing('TransferRequirement', orderno, publish_inbound_file=True, local_inbound_file=local_inbound_file, inbound_message_type='TORD', var_list_dict=json_data)
        return result


    def verify_element_present_by(self, ele_locator_type, ele_locator, base=None):
        present = False

        if ele_locator_type == 'xpath':
            if base.find_element_by_xpath(ele_locator).is_displayed():
                present = True

        return present


    def SMD_POD_21_OP_Compare_visual_standards_between_POs_for_maker(self,json_string):
        result = True
        json_data = json.loads(json_string)

        #self.Navigate_to_Work_Center(json_data['workcenter'])

        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//*[@data-key='BRANDCOMPARE']").click()
        self.wait_for_async_processing()
        #ele_current_screen = driver.find_element_by_xpath("//label[contains(text(),'POD-20')]")
        if self.verify_element_present_by("xpath","//label[contains(text(),'POD-20')]",driver):
            util.html_print("Verified POD-20 screen")
        else:
            util.html_print("Could not verify POD-20 screen")
            result = False

        ele_list_showall_button = driver.find_elements_by_xpath("//span[contains(text(),'Show All')]/ancestor::a[1]")
        if len(ele_list_showall_button) > 0:
            driver.execute_script('arguments[0].scrollIntoView(true);', ele_list_showall_button[0])
            ele_list_showall_button[0].click()
        #driver.find_element_by_xpath("//button[@value='BACK']//span").click()
        #self.Navigate_to_OP_Tab("PRODUCTION")

        self.wait_for_async_processing()
        driver.find_element_by_xpath("//*[@value='CHARACTERISTICCOMPARE']").click()
        self.wait_for_async_processing()
        if self.verify_element_present_by("xpath","//label[contains(text(),'POD-21')]",driver):
            util.html_print("Verified POD-21 screen")
        else:
            util.html_print("Could not verify POD-21 screen")
            result = False

        self.Navigate_to_OP_Tab("PRODUCTION")

        driver.find_element_by_xpath("//*[@data-key='SPECIFICATIONCURRENTPO']").click()
        self.wait_for_async_processing()
        if self.verify_element_present_by("xpath","//label[contains(text(),'VSP-10')]",driver):
            util.html_print("Verified VSP-10 screen")
        else:
            util.html_print("Could not verify VSP-10 screen")
            result = False

        self.Navigate_to_OP_Tab("PRODUCTION")

        self.Select_PO(po_number)

        driver.find_element_by_xpath("//*[@data-key='SPECIFICATIONSELECTEDPO']").click()
        self.wait_for_async_processing()
        if self.verify_element_present_by("xpath","//label[contains(text(),'VSP-10')]",driver):
            util.html_print("Verified VSP-10 screen")
        else:
            util.html_print("Could not verify VSP-10 screen")
            result = False

        return result


    def SMD_POD_30_OP_Stop_Production_Order_for_maker(self, json_string):
        result = True
        json_data = json.loads(json_string)

        self.Navigate_to_OP_Tab("PRODUCTION")

        self.Select_PO(po_number)

        driver.find_element_by_xpath("//*[@data-key='BRANDCHANGE']").click()

        self.wait_for_async_processing()
        ele_list_stop_current_green = driver.find_elements_by_xpath("//a[@data-value='STOP' and contains(@class,'green')]")
        if len(ele_list_stop_current_green) > 0:
            ele_list_stop_current_green[0].click()
            util.html_print("Validated Stop button is green")
        else:
            util.html_print("Stop button is not green")
            return False

        ele_list_ok_button = driver.find_elements_by_xpath("//a[@data-value='OK']")
        if len(ele_list_ok_button) > 0:
            if self.verify_element_present_by("xpath", "//span[contains(text(),'ACK-10')]",driver):
                util.html_print("Verified ACK-10 dialog")
            else:
                util.html_print("Could not verify ACK-10 dialog")
                result = False
            ele_list_ok_button[0].click()

            driver.find_element_by_xpath("//input[contains(@name,'Username')]").send_keys(json_data['username'])
            driver.find_element_by_xpath("//input[contains(@name,'Password')]").send_keys(json_data['password'])
            driver.find_element_by_xpath("//a[@data-value='OK']").click()

        ele_operation_status_description = driver.find_element_by_xpath("//tr[2]//td[@data-field='operationstatusdescription']//span")
        if ele_operation_status_description.text == 'Completed':
            util.html_print("Validated Complete status of current PO")
        else:
            util.html_print("Failed validation of Complete status of current PO")
            result = False

        return result


    def MFG_POD_30_OP_Brand_Change_Initiate(self,json_string):
        result = True
        json_data = json.loads(json_string)

        self.Navigate_to_Work_Center(json_data['workcenter'])
        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        self.wait_for_async_processing()

        global po_number
        #po_number = "2019443"

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//*[@data-key='BRANDCHANGE']").click()
        self.wait_for_async_processing()
        ele_list_brand_change_button = driver.find_elements_by_xpath("//a[@data-value='BRANDCHANGE']")
        if len(ele_list_brand_change_button) > 0:
            ele_list_brand_change_green_button = driver.find_elements_by_xpath("//a[@data-value='BRANDCHANGE' and contains(@class,'green')]//span")
            if len(ele_list_brand_change_green_button) > 0:
                util.html_print("Validated Brand Change button is green")
            else:
                util.html_print("Brand Change button is not green")
                return False
        else:
            util.html_print("Brand Change button is not found")
            return False

        ele_list_showall_button = driver.find_elements_by_xpath("//span[contains(text(),'Show All')]/ancestor::a[1]")
        if len(ele_list_showall_button) > 0:
            driver.execute_script('arguments[0].scrollIntoView(true);', ele_list_showall_button[0])
            ele_list_showall_button[0].click()

        self.wait_for_async_processing()
        ele_list_grid_title = driver.find_elements_by_xpath("//div[contains(@class,'POD-20_MaterialComparisonGrid')]//div[@class='Title']")
        if len(ele_list_grid_title) > 0:
            grid_title = ele_list_grid_title[0].text
            if grid_title == json_data['grid_title']:
                util.html_print('Validated Material Comparison grid title')
            else:
                util.html_print('Failed to validate Material Comparison grid title')
                result = False
            util.html_print('Expected value: ' + json_data['grid_title'] + "; Actual value: " + grid_title)
        else:
            util.html_print("Could not find Material Comparison grid title")
            return False

        ele_list_grid_rows = driver.find_elements_by_xpath(
            "//div[contains(@class,'POD-20_MaterialComparisonGrid')]//tbody//tr")
        if len(ele_list_grid_rows) > 1:
            util.html_print('Validated Material Comparison grid is not empty')
        else:
            util.html_print("Material Comparison grid is empty")
            return False

        return result


    def validate_brand_change_checklist(self,operator_or_technician):
        result = True

        self.wait_for_async_processing()
        ele_list_operator_or_technician_tab = driver.find_elements_by_xpath("//span[text()='" + operator_or_technician + "']/parent::a")
        if len(ele_list_operator_or_technician_tab) > 0:
            if(ele_list_operator_or_technician_tab[0].is_displayed()):
                ele_list_operator_or_technician_tab[0].click()
                self.wait_for_async_processing()
                page_count = int(driver.find_element_by_xpath("//span[@class='pgTotal']").text)
                for page_index in range(1,page_count+1):
                    tr_count = len(driver.find_elements_by_xpath("//div[contains(@class,'ChecklistContainer')]//div[contains(@class,'vpBody')]//tr"))
                    for tr_index in range(1,tr_count+1):
                        class_value = driver.find_element_by_xpath(
                            "//div[contains(@class,'ChecklistContainer')]//div[contains(@class,'vpBody')]//tr[" + str(tr_index) + "]").get_attribute('class')
                        if class_value == "unchecked":
                            driver.find_element_by_xpath(
                                "//div[contains(@class,'ChecklistContainer')]//div[contains(@class,'vpBody')]//tr[" + str(tr_index) + "]//td[@data-field='checked']//button").click()
                            #time.sleep(2)
                            self.wait_for_async_processing()
                            class_value_new = driver.find_element_by_xpath(
                                "//div[contains(@class,'ChecklistContainer')]//div[contains(@class,'vpBody')]//tr[" + str(tr_index) + "]").get_attribute('class')
                            if class_value_new != 'checked':
                                util.html_print("Checklist button is not in Checked state")
                                result = False
                    if result:
                        util.html_print("Checklisted items for " + operator_or_technician)
                    else:
                        util.html_print("Unable to checklist items for " + operator_or_technician)
                    ele_list_page_next = driver.find_elements_by_xpath(
                        "//button[contains(@class,'action_page_next') and not(@disabled)]")
                    if len(ele_list_page_next) > 0:
                        ele_list_page_next[0].click()
            else:
                util.html_print(operator_or_technician + " checklist is not displayed")
        else:
            util.html_print(operator_or_technician + " checklist is not present")

        return result


    def MFG_POD_31_OP_Confirm_check_list_for_operator(self,json_string):
        result = True
        json_data = json.loads(json_string)

        driver.find_element_by_xpath("//a[@data-value='BRANDCHANGE']").click()
        util.html_print("Clicked on Brand Change button")
        self.wait_for_async_processing()

        ele_list_confirm_button = driver.find_elements_by_xpath("//div[@class='DialogButtonsContainer']//span[contains(text(),'Confirm')]")
        if len(ele_list_confirm_button) > 0:
            ele_list_confirm_button[0].click()
            util.html_print("Clicked on Confirm button")
        else:
            util.html_print("Note that Confirm button was not displayed")

        result = self.validate_brand_change_checklist("Operator")

        return result


    def MFG_POD_31_OP_Confirm_check_list_for_technician_or_supervisor(self,json_string):
        result = True
        json_data = json.loads(json_string)

        #driver.find_element_by_xpath("//a[@data-value='BRANDCHANGE']").click()

        #driver.find_element_by_xpath("//div[@class='DialogButtonsContainer']//span[contains(text(),'Confirm')]").click()

        result = self.validate_brand_change_checklist("Technician")

        result = self.validate_brand_change_checklist("Team Leader")

        return result


    def MFG_POD_31_OP_Brand_Change_Complete(self,json_string):
        result = True
        json_data = json.loads(json_string)

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        time.sleep(5)

        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        self.wait_for_async_processing()

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//*[@data-key='BRANDCHANGE']").click()
        self.wait_for_async_processing()

        ele_list_brand_change_button = driver.find_elements_by_xpath("//a[@data-value='BRANDCHANGE']")
        if len(ele_list_brand_change_button) > 0:
            ele_list_brand_change_green_button = driver.find_elements_by_xpath("//a[@data-value='BRANDCHANGE' and contains(@class,'green')]")
            if len(ele_list_brand_change_green_button) > 0:
                util.html_print("Validated Brand Change button is green")
                ele_list_brand_change_green_button[0].click()
                util.html_print("Clicked on Brand Change button")
                self.wait_for_async_processing()
            else:
                util.html_print("Brand Change button is not green")
                return False
                ele_list_brand_change_button[0].click()
                util.html_print("Clicked on Brand Change button")
                self.wait_for_async_processing()
        else:
            util.html_print("Brand Change button is not found")
            return False

        current_po_status = driver.find_element_by_xpath(
            "//tr[2]/td[@data-field='operationstatusdescription']//span").text
        brand_change_po_status = driver.find_element_by_xpath(
            "//tr[3]/td[@data-field='operationstatusdescription']//span").text

        if current_po_status == 'Completed':
            util.html_print("Validated current PO status as Completed")
        else:
            util.html_print("Failed validation of current PO status as Completed")
            util.html_print("Expected: Completed; Actual: " + current_po_status)

        if brand_change_po_status == 'Brand Change':
            util.html_print("Validated brand change PO status as Brand Change")
        else:
            util.html_print("Failed validation of brand change PO status as Brand Change")
            util.html_print("Expected: Brand Change; Actual: " + brand_change_po_status)

        ele_list_checklist_operator_tab = driver.find_elements_by_xpath("//span[text()='Operator']/parent::a")
        if len(ele_list_checklist_operator_tab) > 0:
            checklist_tab_count = len(driver.find_elements_by_xpath("//div[contains(@class,'TabsMaterialsToStage')]//span/a"))
            for tab_index in range(1,checklist_tab_count+1):
                tab_text = driver.find_element_by_xpath(
                    "//div[contains(@class,'TabsMaterialsToStage')]//span/a[" + str(tab_index) + "]/span").text
                util.html_print("Validating Checklist for: " + tab_text)
                self.validate_brand_change_checklist(tab_text)

        ele_list_confirm_button = driver.find_elements_by_xpath("//span[contains(text(),'Confirm Brand Change')]")
        if len(ele_list_confirm_button) > 0:
            ele_list_confirm_button = driver.find_elements_by_xpath("//a[contains(@class,'green')]//span[contains(text(),'Confirm Brand Change')]")
            if len(ele_list_confirm_button) > 0:
                util.html_print("Validated status of Confirm button is green")
                driver.execute_script('arguments[0].scrollIntoView(true);', ele_list_confirm_button[0])
                ele_list_confirm_button[0].click()
                util.html_print("Clicked on Confirm button")
            else:
                util.html_print("Confirm button is not green")
                return False
        else:
            util.html_print("Confirm button is not present")
            return False

        driver.find_element_by_xpath("//input[contains(@id,'RenderInputs_Username')]").send_keys(json_data['username'])
        driver.find_element_by_xpath("//input[contains(@id,'RenderInputs_Password')]").send_keys(json_data['password'])
        driver.find_element_by_xpath("//*[@data-value='OK']").click()

        self.wait_for_async_processing()

        return result


    def MFG_CPV_HH_Validate_wrapping_material_GS1_code_success(self,json_string):
        result = True
        json_data = json.loads(json_string)

        ROOT_DIR = util.get_root_dir()
        loipro1_file = ROOT_DIR + "\\user_files\\" + details_dict['loipro1_file_name']

        if json_data['maker_or_packer'] == 'Maker / 0010':
            machine = util.get_xml_data_by_xpath(loipro1_file,
                "//VORNR[text()='0010']/ancestor::E1AFVOL[1]//ARBPL") or util.get_xml_data_by_xpath(
                loipro1_file, "//ActivityNumber[text()='0010']/ancestor::ProductionOrderProcesses[1]//WorkCenter")
            machine = machine.replace('SP', 'SM')
        elif json_data['maker_or_packer'] == 'Packer / 0020':
            machine = util.get_xml_data_by_xpath(loipro1_file,
                "//VORNR[text()='0020']/ancestor::E1AFVOL[1]//ARBPL") or util.get_xml_data_by_xpath(
                loipro1_file, "//ActivityNumber[text()='0020']/ancestor::ProductionOrderProcesses[1]//WorkCenter")
            if machine is None:
                machine = util.get_xml_data_by_xpath(loipro1_file,
                    "//VORNR[text()='0010']/ancestor::E1AFVOL[1]//ARBPL") or util.get_xml_data_by_xpath(
                    loipro1_file, "//ActivityNumber[text()='0010']/ancestor::ProductionOrderProcesses[1]//WorkCenter")
            machine = machine.replace('SM', 'SP')

        driver.find_element_by_xpath("//span[contains(text(),'Machine :')]/parent::div/following-sibling::div//input").send_keys(machine)

        driver.find_element_by_xpath("//*[@data-value='CONTINUE']").click()
        self.wait_for_async_processing()

        driver.find_element_by_xpath("//*[@data-value='SHOWALL']").click()
        self.wait_for_async_processing()

        grid_rows_xpath = "//*[@class='TabularGridLayout MobileDataGrid']//table/tbody/tr[@class='GridBody']"

        aicode = json_data['aicode']
        for row_index in range(1,3):
            product_number = driver.find_element_by_xpath(grid_rows_xpath + "[" + str(row_index) + "]/td/span").text
            before_validated_count = driver.find_element_by_xpath("//span[text()='" + product_number + "']/parent::td/following-sibling::td/span").text
            driver.find_element_by_xpath(
                "//span[contains(text(),'LABEL:')]/ancestor::div/following-sibling::div//input").send_keys(aicode + product_number)
            driver.find_element_by_xpath("//*[@data-value='CONTINUE']").click()
            self.wait_for_async_processing()
            ele_list_component_validated_message = driver.find_elements_by_xpath("//span[contains(text(),'Component Validated Successfully')]")
            if len(ele_list_component_validated_message) > 0:
                util.html_print("Validated success message")
            else:
                util.html_print("Failed validation of success message")
                result = False
            after_validated_count = driver.find_element_by_xpath("//span[text()='" + product_number + "']/parent::td/following-sibling::td/span").text
            before_validated_count = int(before_validated_count)
            after_validated_count = int(after_validated_count)
            if after_validated_count == before_validated_count + 1:
                util.html_print("Validated product number: " + product_number)
            else:
                util.html_print("Failed validation count of product number: " + product_number)
                util.html_print("Expected: " + str(before_validated_count + 1) + " ; Actual: " + str(after_validated_count))
                result = False

        time.sleep(2)
        return result


    def MFG_CPV_HH_Validate_wrapping_material_SSCC_code_success(self,json_string):
        result = True
        json_data = json.loads(json_string)

        container = 'L3Test8134'

        ROOT_DIR = util.get_root_dir()
        loipro1_file = ROOT_DIR + "\\user_files\\" + details_dict['loipro1_file_name']
        if json_data['maker_or_packer'] == 'Maker / 0010':
            machine = util.get_xml_data_by_xpath(loipro1_file,
                "//VORNR[text()='0010']/ancestor::E1AFVOL[1]//ARBPL") or util.get_xml_data_by_xpath(
                loipro1_file, "//ActivityNumber[text()='0010']/ancestor::ProductionOrderProcesses[1]//WorkCenter")
            machine = machine.replace('SP', 'SM')
        elif json_data['maker_or_packer'] == 'Packer / 0020':
            machine = util.get_xml_data_by_xpath(loipro1_file,
                "//VORNR[text()='0020']/ancestor::E1AFVOL[1]//ARBPL") or util.get_xml_data_by_xpath(
                loipro1_file, "//ActivityNumber[text()='0020']/ancestor::ProductionOrderProcesses[1]//WorkCenter")
            if machine is None:
                machine = util.get_xml_data_by_xpath(loipro1_file,
                    "//VORNR[text()='0010']/ancestor::E1AFVOL[1]//ARBPL") or util.get_xml_data_by_xpath(
                    loipro1_file, "//ActivityNumber[text()='0010']/ancestor::ProductionOrderProcesses[1]//WorkCenter")
            machine = machine.replace('SM', 'SP')

        driver.find_element_by_xpath("//span[contains(text(),'Machine :')]/parent::div/following-sibling::div//input").send_keys(machine)

        driver.find_element_by_xpath("//*[@data-value='CONTINUE']").click()
        self.wait_for_async_processing()

        driver.find_element_by_xpath(
            "//span[contains(text(),'LABEL:')]/ancestor::div/following-sibling::div//input").send_keys(
            container)
        driver.find_element_by_xpath("//*[@data-value='CONTINUE']").click()
        self.wait_for_async_processing()
        ele_list_component_validated_message = driver.find_elements_by_xpath(
            "//span[contains(text(),'Component Validated Successfully')]")
        if len(ele_list_component_validated_message) > 0:
            util.html_print("Validated success message")
        else:
            util.html_print("Failed validation of success message")
            #result = False

        time.sleep(2)
        return result


    def MFG_POD_31_OP_View_material_validation_status(self, json_string):
        result = True
        json_data = json.loads(json_string)

        self.Navigate_to_Work_Center(json_data['workcenter'])
        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        self.wait_for_async_processing()

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//*[@data-key='BRANDCHANGE']").click()
        self.wait_for_async_processing()

        ele_list_brand_change_button = driver.find_elements_by_xpath("//a[@data-value='BRANDCHANGE']")
        if len(ele_list_brand_change_button) > 0:
            ele_list_brand_change_button[0].click()
            util.html_print("Clicked on Brand Change button")
            self.wait_for_async_processing()
        else:
            util.html_print("Brand Change button is not found")
            return False

        ele_list_dialog_buttons_container = driver.find_elements_by_xpath("//div[@class='DialogButtonsContainer']//a[2]")
        if len(ele_list_dialog_buttons_container) > 0:
            if ele_list_dialog_buttons_container[0].is_displayed():
                ele_list_dialog_buttons_container[0].click()

        self.wait_for_async_processing()

        grid_xpath = "(//div[contains(@class,'ConnectionInfoGrid')])[1]"
        rows_count = len(driver.find_elements_by_xpath(grid_xpath + "//table//tr[(contains(@class,'GridBody'))]"))

        if rows_count > 1:
            for row_index in range(1,rows_count+1):
                active_material = driver.find_element_by_xpath(grid_xpath
                                                                   + "//tr[contains(@class,'GridBody')]["
                                                                   + str(row_index) + "]//td[1]").text
                required_material = driver.find_element_by_xpath(grid_xpath
                                                                     + "//tr[contains(@class,'GridBody')]["
                                                                     + str(row_index) + "]//td[2]/span").text
                if active_material == required_material:
                    util.html_print("Active material and required material are both same")
                else:
                    util.html_print("Active material and required material are not same")
                ele_list_grid_row_yellow = driver.find_elements_by_xpath(
                    grid_xpath+ "//tr[contains(@class,'GridBody yellow')]["+ str(row_index) + "]")
                if len(ele_list_grid_row_yellow) > 0:
                    util.html_print("Pipe connection is in deactive state")
                ele_list_grid_row_yellow = driver.find_elements_by_xpath(
                    grid_xpath + "//tr[contains(@class,'GridBody green')][" + str(row_index) + "]")
                if len(ele_list_grid_row_yellow) > 0:
                    util.html_print("Pipe connection is in active state")

        util.html_print("Validated material status for Brand Change")

        return result


    def MFG_POD_30_OP_Skip_material_validation(self, json_string):
        result = True
        json_data = json.loads(json_string)

        self.wait_for_async_processing()
        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        self.wait_for_async_processing()

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//*[@data-key='BRANDCHANGE']").click()
        self.wait_for_async_processing()

        ele_list_showall_button = driver.find_elements_by_xpath("//span[contains(text(),'Show All')]/ancestor::a[1]")
        if len(ele_list_showall_button) > 0:
            driver.execute_script('arguments[0].scrollIntoView(true);', ele_list_showall_button[0])
            ele_list_showall_button[0].click()

        ele_temp = driver.find_element_by_xpath("//span[contains(text(),'DMS File')]")
        driver.execute_script('arguments[0].scrollIntoView(true);', ele_temp)
        ele_temp.click()
        ele_temp = driver.find_element_by_xpath("//*[@data-key='SkipValidation']")
        driver.execute_script('arguments[0].scrollIntoView(true);', ele_temp)
        ele_temp.click()

        self.wait_for_async_processing()
        driver.find_element_by_xpath("//input[contains(@name,'Username')]").send_keys(json_data['username'])
        driver.find_element_by_xpath("//input[contains(@name,'Password')]").send_keys(json_data['password'])
        driver.find_element_by_xpath("//a[@data-value='OK']").click()

        self.wait_for_async_processing()
        driver.find_element_by_xpath("//textarea[contains(@name,'AddComment')]").send_keys("Skipping validation for Brand Change")
        driver.find_element_by_xpath("//span[text()='Save']").click()

        self.wait_for_async_processing()
        util.html_print("Validated Skip material validation")
        time.sleep(5)
        return result


    def SMD_POD_31_OP_View_brand_change_data(self, json_string):
        result = True
        json_data = json.loads(json_string)

        self.wait_for_async_processing()
        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        self.wait_for_async_processing()

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//*[@data-key='BRANDCHANGE']").click()
        self.wait_for_async_processing()

        ele_list_brand_change_button = driver.find_elements_by_xpath("//a[@data-value='BRANDCHANGE']")
        if len(ele_list_brand_change_button) > 0:
            ele_list_brand_change_button[0].click()
            util.html_print("Clicked on Brand Change button")
            self.wait_for_async_processing()
        else:
            util.html_print("Brand Change button is not found")
            return False

        current_po_status = driver.find_element_by_xpath(
            "//tr[2]/td[@data-field='operationstatusdescription']//span").text
        brand_change_po_status = driver.find_element_by_xpath(
            "//tr[3]/td[@data-field='operationstatusdescription']//span").text

        if current_po_status == 'Completed':
            util.html_print("Validated current PO status as Completed")
        else:
            util.html_print("Failed validation of current PO status as Completed")
            util.html_print("Expected: Completed; Actual: " + current_po_status)

        if brand_change_po_status == 'Brand Change':
            util.html_print("Validated brand change PO status as Brand Change")
        else:
            util.html_print("Failed validation of brand change PO status as Brand Change")
            util.html_print("Expected: Brand Change; Actual: " + brand_change_po_status)

        ele_list_checklist_operator_tab = driver.find_elements_by_xpath("//span[text()='Operator']/parent::a")
        if len(ele_list_checklist_operator_tab) > 0:
            checklist_tab_count = len(driver.find_elements_by_xpath("//div[contains(@class,'TabsMaterialsToStage')]//span/a"))
            for tab_index in range(1,checklist_tab_count+1):
                tab_text = driver.find_element_by_xpath(
                    "//div[contains(@class,'TabsMaterialsToStage')]//span/a[" + str(tab_index) + "]/span").text
                util.html_print("Validating Checklist for: " + tab_text)
                self.validate_brand_change_checklist(tab_text)

        return result


    def MFG_POD_30_OP_Compare_materials_between_PO(self,json_string):
        result = True
        json_data = json.loads(json_string)

        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//*[@data-key='BRANDCOMPARE']").click()
        self.wait_for_async_processing()
        #ele_current_screen = driver.find_element_by_xpath("//label[contains(text(),'POD-20')]")
        if self.verify_element_present_by("xpath","//label[contains(text(),'POD-20')]",driver):
            util.html_print("Verified POD-20 screen")
        else:
            util.html_print("Could not verify POD-20 screen")
            result = False

        return result


    def MFG_POD_21_OP_Compare_charcteristics_between_PO(self,json_string):
        result = True
        json_data = json.loads(json_string)

        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//*[@data-key='BRANDCOMPARE']").click()
        self.wait_for_async_processing()
        #ele_current_screen = driver.find_element_by_xpath("//label[contains(text(),'POD-20')]")
        if self.verify_element_present_by("xpath","//label[contains(text(),'POD-20')]",driver):
            util.html_print("Verified POD-20 screen")
        else:
            util.html_print("Could not verify POD-20 screen")
            result = False

        driver.find_element_by_xpath("//*[@value='CHARACTERISTICCOMPARE']").click()
        self.wait_for_async_processing()
        if self.verify_element_present_by("xpath","//label[contains(text(),'POD-21')]",driver):
            util.html_print("Verified POD-21 screen")
        else:
            util.html_print("Could not verify POD-21 screen")
            result = False

        return result


    def ADM_JobHistory_MM_Check_trolley_staging_request_message(self,json_string):
        result = True
        json_data = json.loads(json_string)

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])
        query = "select distinct od.orderno from ORDER_DETAIL od join warehouse_location wl on od.towarehouselocationid=wl.id where od.parentorderno=? and wl.warehouselocationtype=10"
        db_result_set = util.fetch_db_data(query, key='orderno', var_list=[po_number])
        orderno = None
        if json_data['maker_or_packer'] == 'Maker / 0010':
            orderno = db_result_set[0]
        elif json_data['maker_or_packer'] == 'Packer / 0020':
            orderno = db_result_set[1]

        ROOT_DIR = util.get_root_dir()
        local_inbound_file = ROOT_DIR + "\\user_files\\inbound\\response_output.xml"

        result = self.gmes_message_processing('TransferRequirement', orderno, publish_inbound_file=True, local_inbound_file=local_inbound_file, inbound_message_type='TORD', var_list_dict=json_data)
        return result


    def SMD_VSP_10_OP_View_production_order_specification_maker(self,json_string):
        result = True
        json_data = json.loads(json_string)

        self.Navigate_to_Work_Center(json_data['workcenter'])
        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        ele_temp = driver.find_element_by_xpath("//*[@data-key='SPECIFICATIONCURRENTPO']")
        driver.execute_script('arguments[0].scrollIntoView(true);', ele_temp)
        ele_temp.click()
        self.wait_for_async_processing()
        if self.verify_element_present_by("xpath","//label[contains(text(),'VSP-10')]",driver):
            util.html_print("Verified VSP-10 screen")
        else:
            util.html_print("Could not verify VSP-10 screen")
            result = False

        self.Navigate_to_OP_Tab("PRODUCTION")

        self.Select_PO(po_number)

        ele_temp = driver.find_element_by_xpath("//*[@data-key='SPECIFICATIONSELECTEDPO']")
        driver.execute_script('arguments[0].scrollIntoView(true);', ele_temp)
        ele_temp.click()
        self.wait_for_async_processing()
        if self.verify_element_present_by("xpath","//label[contains(text(),'VSP-10')]",driver):
            util.html_print("Verified VSP-10 screen")
        else:
            util.html_print("Could not verify VSP-10 screen")
            result = False

        return result


    def SMD_POD_30_OP_Start_Production_Order_for_maker(self,json_string):
        result = True
        json_data = json.loads(json_string)

        self.wait_for_async_processing()
        self.Navigate_to_OP_Tab("PRODUCTION")

        if not self.Navigate_to_Maker_Packer(json_data['maker_or_packer']):
            util.html_print("Could not navigate to Maker tab")
            return False

        self.wait_for_async_processing()

        po_number = self.get_po_no_from_loipro(details_dict['loipro1_file_name'])

        if not self.Select_PO(po_number):
            util.html_print("Could not find PO for selection")
            return False

        driver.find_element_by_xpath("//*[@data-key='BRANDCHANGE']").click()
        self.wait_for_async_processing()

        driver.find_element_by_xpath("//a[contains(@class,'Button green')]//span[text()='Start']").click()
        self.wait_for_async_processing()

        ele_list_confirm = driver.find_elements_by_xpath("//a[contains(@class,'Button')]//span[text()='Confirm']")
        if len(ele_list_confirm) > 0:
            ele_list_confirm[0].click()
            self.wait_for_async_processing()

        ele_list_authenticate = driver.find_elements_by_xpath("//span[contains(text(),'Authenticate')]")
        if len(ele_list_authenticate) > 0:
            ele_list_authenticate[0].click()
            self.wait_for_async_processing()
            driver.find_element_by_xpath("//input[contains(@name,'Username')]").send_keys(json_data['username'])
            driver.find_element_by_xpath("//input[contains(@name,'Password')]").send_keys(json_data['password'])
            driver.find_element_by_xpath("//a[@data-value='OK']").click()
            self.wait_for_async_processing()

        if result is True:
            util.html_print("Validated PO is Started")

        time.sleep(5)
        return result





    def OP_Home(self):
        driver.find_element_by_xpath("//button[@value='HOME']").click()
        time.sleep(5)

    def OP_Exit(self):
        driver.find_element_by_xpath("//button[@value='EXIT']").click()
        time.sleep(5)

    def Logout(self,data=True):
        driver.find_element_by_xpath("//a[@title='Click to go Logout']").click()
        time.sleep(5)
        return data


    def teardown(self):
        driver.quit()
        pass


    def Testing_1(self,json_string):
        result = True
        json_data = json.loads(json_string)

        json_data['']
        return result

