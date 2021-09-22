'''
Created on Mar 10, 2019

@author: 29265
'''

import datetime
import pytest
import allure
import unittest
import HtmlTestRunner

import json
import configparser
import os
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.insert(0, ROOT_DIR)
from framework import component as components_class_instance

class TestsContainer(unittest.TestCase):
    logMessage = True


def loadConfigFile(path):
    config = configparser.RawConfigParser()
    config.read(path)
    return config

#test_controller_main()

def make_test_function(obj, all_actual_components_per_tc, all_actual_components_data, testComponentOffset, testDataOffset):
    def test(self):
        for k in range(0, len(all_actual_components_per_tc)-int(testComponentOffset)):
            # print(allActualComponentsPerTC[k])
            component_test = all_actual_components_per_tc[k+int(testComponentOffset)]
            # print(xx)
            #with pytest.allure.step(component_test):

            print(str(datetime.datetime.now().replace(microsecond=0).isoformat(' ')) + ": STARTED execution of component: " + component_test)
            print("<br/>")
            result = getattr(obj, component_test)(all_actual_components_data[k+int(testDataOffset)])
            print(str(datetime.datetime.now().replace(microsecond=0).isoformat(' ')) + ": FINISHED execution of component: " + component_test)
            print("<br/>")
            if not result:
                break
        obj.teardown()
        assert result
    return test


def create_test_suite():
    components_obj=components_class_instance.GMESComp()

    print(os.getcwd())
    global ROOT_DIR
    ROOT_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file_path=ROOT_DIR+'\\config.properties'
    print(config_file_path)
    config=loadConfigFile(config_file_path)
    details_dict = dict(config.items('Env Details'))
    #to get country
    country=details_dict['countrycode']
    print(country)
    testSuite=details_dict['testsuite']
    tcsheetname=details_dict['tcsheetname']
    testDataSheetName=details_dict['testdatasheetname']
    testComponentOffset = details_dict['testcomponentoffset']
    testDataOffset = details_dict['testdataoffset']
    print(testSuite)
    print(tcsheetname)
    print(testDataSheetName)

    tSuite = pd.read_excel(ROOT_DIR + "\\GMESmarket\\" + country + "\\" + testSuite + ".xlsx",
                           sheet_name=tcsheetname)
    tSuite.fillna('noStep',inplace=True)

    tData = pd.read_excel(ROOT_DIR + "\\GMESmarket\\" + country + "\\" + testSuite + ".xlsx",
                          sheet_name=testDataSheetName)
    tData.fillna('noStep',inplace=True)

    #transpose
    tSuite=tSuite.T
    tData=tData.T

    for i in range(0,len(tSuite.columns)):
        if tSuite.loc['Execute', i] == "YES":
            for j in range(0,len(tData.columns)):
                #TC validation
                if list(tSuite[i])[0]== list(tData[j])[0]:
                    allComponentsPerTC=list(tSuite[i])
                    allComponentsData=list(tData[j])
                    allActualComponentsPerTC = [x for x in allComponentsPerTC if x != 'noStep']
                    allActualComponentsData = [x for x in allComponentsData if x != 'noStep']
                    #both list will be equal size
                    test_func = make_test_function(components_obj, allActualComponentsPerTC, allActualComponentsData, testComponentOffset, testDataOffset)
                    setattr(TestsContainer, 'test_{0}'.format(allActualComponentsPerTC[0]), test_func)


'''
def test_create_suite():
    create_test_suite()
    unittest.main()
'''

if __name__ == '__main__':

    '''
    testsmap = {
        'foo': [1, 1],
        'bar': [1, 2],
        'baz': [5, 5]}

    for name, params in testsmap.items():
        test_func = make_test_function(name, params[0], params[1])
        setattr(TestsContainer, 'test_{0}'.format(name), test_func)
    '''

    #test_create_suite()

    create_test_suite()

    html_report_dir=ROOT_DIR+'\\html_report'
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(output=html_report_dir, report_title='GMES Automation Report',
                                                 open_in_browser=True))
