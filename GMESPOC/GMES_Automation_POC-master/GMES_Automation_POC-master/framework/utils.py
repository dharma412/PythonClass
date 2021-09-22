import time
import datetime
import os
import subprocess

from io import StringIO
import configparser
from xml.dom import minidom
import xml.etree.ElementTree as ET
from lxml import etree
import pandas as pd
import pyodbc
import random
import subprocess

from selenium.common.exceptions import *
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class Utilities:

    @contextmanager
    def wait_for_page_load(driver, timeout=180):
        old_page = driver.find_element_by_tag_name('html')
        yield
        try:
            WebDriverWait(driver, timeout).until(
                staleness_of(old_page)
            )
        except:
            pass

    @staticmethod
    def loadConfigFile(path):
        config = configparser.RawConfigParser()
        config.read(path)
        return config


    @staticmethod
    def html_print(message):
        print(str(datetime.datetime.now().replace(microsecond=0).isoformat(' ')) + ": " + message)
        print("<br />")


    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        return max(paths, key=os.path.getctime)


    @staticmethod
    def get_xml_tag_data(xml_file, tag_name):
        doc = minidom.parse(xml_file)
        # doc.getElementsByTagName returns NodeList
        name_list = doc.getElementsByTagName(tag_name)
        if name_list is not None and len(name_list) > 0:
            name = name_list[0]
            if name is not None:
                if name.firstChild:
                    return name.firstChild.data
                else:
                    return None
            else:
                return None
        else:
            return None


    @staticmethod
    def get_xml_tag_data_from_string(xml_string, tag_name):
        doc = minidom.parseString(xml_string)
        # doc.getElementsByTagName returns NodeList
        name_list = doc.getElementsByTagName(tag_name)
        if name_list is not None and len(name_list) > 0:
            name = name_list[0]
            if name is not None:
                if name.firstChild:
                    return name.firstChild.data
                else:
                    return None
            else:
                return None
        else:
            return None


    @staticmethod
    def get_xml_data_by_xpath(xml_file, xpath_string):
        root = etree.parse(xml_file)
        find_text = etree.XPath(xpath_string)
        if find_text(root) is not None and len(find_text(root)) > 0:
            return find_text(root)[0].text
        else:
            return None


    @staticmethod
    def get_xml_data_by_xpath_from_string(xml_string, xpath_string):
        xml_data = xml_string.encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(xml_data, parser=parser)
        find_text = etree.XPath(xpath_string)
        if find_text(root) is not None and len(find_text(root)) > 0:
            return find_text(root)[0].text
        else:
            return None


    @staticmethod
    def get_xml_data_by_xpath_from_file(xml_file, xpath_string):
        root = etree.parse(xml_file)
        find_text = etree.XPath(xpath_string)
        if find_text(root) is not None and len(find_text(root)) > 0:
            return find_text(root)[0].text
        else:
            return None


    @staticmethod
    def get_xml_string_from_file(xml_file):
        xml_tree = etree.parse(xml_file)
        return etree.tostring(xml_tree, encoding='utf-8', method='xml', xml_declaration=True, pretty_print=True).decode(
            'utf-8')


    @staticmethod
    def get_xml_nodes_count_by_xpath_from_string(xml_string, xpath_string):
        xml_data = xml_string.encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(xml_data, parser=parser)
        count = len(root.xpath("." + xpath_string))
        return count


    @staticmethod
    def get_xml_nodes_count_by_xpath_from_file(xml_file, xpath_string):
        doc = etree.parse(xml_file)
        root = doc.getroot()
        count = len(root.xpath("." + xpath_string))
        return count


    @staticmethod
    def get_xml_tag_attribute_value(xml_file, tag_name, attribute_name):
        doc = minidom.parse(xml_file)
        name_list = doc.getElementsByTagName(tag_name)
        if name_list is not None and len(name_list) > 0:
            name = name_list[0]
            if name is not None:
                return name.getAttribute(attribute_name)
            else:
                return None
        else:
            return None


    @staticmethod
    def get_xml_tag_attribute_value_from_string(xml_string, tag_name, attribute_name):
        doc = minidom.parseString(xml_string)
        name_list = doc.getElementsByTagName(tag_name)
        if name_list is not None and len(name_list) > 0:
            name = name_list[0]
            if name is not None:
                return name.getAttribute(attribute_name)
            else:
                return None
        else:
            return None


    @staticmethod
    def set_xml_tag_text(xml_file, tag_name, text):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # changing a field text
        for elem in root.iter(tag_name):
            elem.text = text

        tree.write(xml_file, encoding="UTF-8")


    @staticmethod
    def strip_all_namespaces_from_xml(xml_string):
        it = ET.iterparse(StringIO(xml_string))
        for _, el in it:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
        root = it.root
        xml_modified_string = ET.tostring(root).decode('utf-8')
        return xml_modified_string


    @staticmethod
    def fetch_db_data(query, key=None, var_list=None):
        db_server = "10.6.14.138"
        db_user = "FlxAdmin"
        db_pwd = "FlxAdmin"
        db_database = "TaOFlexNet_BR4.18"
        db_connect_string = "Driver={SQL Server Native Client 11.0};Server=" + db_server + ";UID=" + db_user + ";PWD=" + db_pwd + ";Database=" + db_database + ";"
        cnxn = pyodbc.connect(db_connect_string)
        df = pd.read_sql_query(query, cnxn, params=var_list)

        result_set = []
        for index, row in df.iterrows():
            result_set.append(row[key])

        return result_set


    @staticmethod
    def run_win_cmd(cmd):
        result = []
        process = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        for line in process.stdout:
            result.append(line)
        errcode = process.returncode
        for line in result:
            print(line)
        if errcode is not None:
            raise Exception('cmd %s failed, see above for details', cmd)

        return errcode


    @staticmethod
    def get_root_dir():
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    @staticmethod
    def wait_for_ajax(driver, max_timeout=10):
        wait = WebDriverWait(driver, max_timeout)
        try:
            wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            pass


    @staticmethod
    def wait_for_then_click(element, base=None, interval=.5, maxWait=5):
        ticker = 0
        myElement = None
        if base:
            elementAvailable = False
            while ((ticker * interval) < maxWait):
                try:
                    for elementCheck in base.find_elements_by_xpath(element):
                        if elementCheck.is_displayed() and elementCheck.is_enabled():
                            myElement = elementCheck
                            elementAvailable = True
                            break
                except:
                    pass
                if elementAvailable:
                    break
                else:
                    ticker += interval
                    time.sleep(interval)
        else:
            print("returning none")
            return base
        print("\tWAITED %s seconds for element %s" % ((ticker * interval), element))
        if myElement is not None:
            myElement.click()
            return myElement
        else:
            raise NoSuchElementException("wait for expired on {}".format(element))


    @staticmethod
    def wait_for_displayed(element, base=None, interval=.5, maxWait=5):
        ticker = 0
        myElement = None
        if base:
            elementAvailable = False
            while ((ticker * interval) < maxWait):
                print("*")
                print(base.title)
                try:
                    for elementCheck in base.find_elements_by_xpath(element):
                        if elementCheck.is_displayed():
                            myElement = elementCheck
                            elementAvailable = True
                            break
                except:
                    pass
                if elementAvailable:
                    break
                else:
                    ticker += interval
                    time.sleep(interval)
        else:
            return base
        print("\tWAITED %s seconds for element %s" % ((ticker * interval), element))
        if myElement is not None:
            return myElement
        else:
            raise NoSuchElementException("wait for expired on {}".format(element))


    @staticmethod
    def wait_for_not_displayed(element, base=None, interval=.5, maxWait=10):
        ticker = 0
        myElement = None
        if base:
            base.implicitly_wait(1)
            elementNotAvailable = False
            #time.sleep(1)
            while (ticker < maxWait):
                try:
                    myElement = None
                    for elementCheck in base.find_elements_by_xpath(element):
                        if elementCheck.is_displayed():
                            print("#")
                            myElement = elementCheck
                            break
                    if myElement is None:
                        elementNotAvailable = True
                except (StaleElementReferenceException, NoSuchElementException, InvalidElementStateException) as err:
                    elementNotAvailable = True
                if elementNotAvailable:
                    break
                else:
                    ticker += interval
                    time.sleep(interval)
        else:
            return base
        #print("\tWAITED %s seconds for element %s" % ((ticker + 1), element))
        # time.sleep(1)
        if hasattr(base.__class__, 'portalbase'):
            base.implicitly_wait(base.__class__.portalbase.IMPLICIT_WAIT_DEFAULT)
        else:
            base.implicitly_wait(10)
        if myElement is None:
            return True
        else:
            raise TimeoutException("wait for not displayed expired on {}".format(element))


    @staticmethod
    def wait_for_not_enabled(element, base=None, interval=.5, maxWait=10):
        ticker = 0
        myElement = None
        if base:
            base.implicitly_wait(2)
            elementNotAvailable = False
            time.sleep(1)
            while (ticker < maxWait):
                try:
                    myElement = None
                    for elementCheck in base.find_elements_by_xpath(element):
                        if elementCheck.is_enabled():
                            print("#")
                            myElement = elementCheck
                            break
                    if myElement is None:
                        elementNotAvailable = True
                except (StaleElementReferenceException, NoSuchElementException, InvalidElementStateException) as err:
                    elementNotAvailable = True
                if elementNotAvailable:
                    break
                else:
                    ticker += interval
                    time.sleep(interval)
        else:
            return base
        print("\tWAITED %s seconds for element %s" % ((ticker + 1), element))
        # time.sleep(1)
        if hasattr(base.__class__, 'portalbase'):
            base.implicitly_wait(base.__class__.portalbase.IMPLICIT_WAIT_DEFAULT)
        else:
            base.implicitly_wait(10)
        if myElement is None:
            return True
        else:
            raise TimeoutException("wait for not enabled expired on {}".format(element))


def mulligans(tries):
    def setupSwings(f):
        def startSwinging(*p):
            output = None
            for swing in range(tries):
                try:
                    output = f(*p)
                    return output
                except StaleElementReferenceException:
                    time.sleep(.5)
                    print("got stale element exception")
                    pass
                except WebDriverException:
                    time.sleep(.5)
                    pass
                except Exception as e:
                    raise e
            raise NoSuchElementException("{} could not resolve {} after {} tries !".format(f, p[1::], tries))

        return startSwinging

    return setupSwings


class tableProcessor(object):
    #  should be passed the table elemnt from something like
    #  webdriver.find_element_by_xpath('//div[@id="contentList"]/div/table[@id="contTbl"]/tbody')
    def __init__(self, tableElement):
        self._tableElement = tableElement
        self._rows = tableElement.find_elements_by_tag_name('tr')
        self._columns = [c.find_elements_by_tag_name('td') for c in self._rows]

    @property
    def rows(self):
        return len(self._rows)

    @property
    def columns(self):
        return len(self._columns[0])

    def getRowAsDict(self, rowindex):
        if rowindex < len(self._rows):
            rad = {}
            for c in range(len(self._columns[rowindex])):
                columntag = "column{}".format(c)
                mydivs = None
                myanchors = None
                myspans = None
                rad[columntag] = {
                    "anchor": None,
                    "text": None,
                    "div": None,
                    "element": self._columns[rowindex][c]}
                ctext = self._columns[rowindex][c].get_attribute('innerHTML')
                if '<div ' in ctext:
                    mydivs = self._columns[rowindex][c].find_elements_by_tag_name('div')
                elif '<a ' in ctext:
                    myanchors = self._columns[rowindex][c].find_elements_by_tag_name('a')
                    if '<span ' in ctext:
                        myspans = self._columns[rowindex][c].find_elements_by_tag_name('span')
                elif '<span ' in ctext:
                    myspans = self._columns[rowindex][c].find_elements_by_tag_name('span')
                else:
                    pass
                if mydivs:
                    if len(mydivs) == 1:
                        rad[columntag]['div'] = mydivs[0]
                    else:
                        rad[columntag]['div'] = mydivs
                    continue
                else:
                    if myanchors:
                        if len(myanchors) == 1:
                            rad[columntag]['anchor'] = myanchors[0]
                        else:
                            rad[columntag]['anchor'] = myanchors
                        if myspans:
                            if len(myspans) == 1:
                                # rad[columntag]['text'] = myspans[0].text
                                rad[columntag]['text'] = myspans[0].get_attribute('title') or myspans[0].text
                            else:
                                # rad[columntag]['text'] = [s.text for s in myspans if s.text]
                                rad[columntag]['text'] = [s.get_attribute('title') or s.text for s in myspans]
                        continue
                    if myspans:
                        if len(myspans) == 1:
                            rad[columntag]['text'] = myspans[0].get_attribute('title') or myspans[0].text
                        else:
                            rad[columntag]['text'] = [s.get_attribute('title') or s.text for s in myspans]
                        continue
                    if self._columns[rowindex][c].text:
                        rad[columntag]['text'] = self._columns[rowindex][c].text
            return rad
        else:
            raise ValueError('index {} > available {}'.format(rowindex, len(self._rows)))

    def getTableAsDict(self):
        tad = {}
        for row in range(len(self._rows)):
            tad['row{}'.format(row)] = self.getRowAsDict(row)
        return tad
