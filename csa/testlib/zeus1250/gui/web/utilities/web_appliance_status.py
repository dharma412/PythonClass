#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/utilities/web_appliance_status.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.gui.guicommon import GuiCommon
from sal.containers import cfgholder
import common.gui.guiexceptions as guiexceptions

VIEW_APPLIANCE_LINK = lambda name: 'link=%s' % (name,)
SYSTEM_TABLE = '//dl[@class="box"][1]'
SYSTEM_INFO_NUMBER = '%s//tr[*]' % (SYSTEM_TABLE,)
SYSTEM_INFO_ROW = lambda row: '%s//tr[%s]/td' % (SYSTEM_TABLE, row)
SYSTEM_INFO_ATTR_NAME_ROW = lambda row: '%s//tr[%s]/th' % (SYSTEM_TABLE, row)
ICCM_HIST_ROW = lambda row, column:\
    '%s//tr[11]//tr[%s]/td[%s]' % (SYSTEM_TABLE, row, column)
SERVICE_INFO_TABLE = '//dl[@class="box"][2]'
SERVICE_COL_NUMBER = lambda row: '%s/dd/table/tbody/tr[%s]//th' %(SERVICE_INFO_TABLE,row)
SERVICE_INFO_ROW  = lambda row, column:\
'//dl[@class="box"][2]//tr[%s]/td[%s]' % (row, column)
PROXY_INFO_TABLE = '//dl[@class="box"][last()-1]'
PROXY_LIST_TABLE = '%s//table[@class="cols"]' %  (PROXY_INFO_TABLE,)
ROW_NUMBER = lambda table: '%s/dd/table/tbody/tr' % (table)
PROXY_GROUP_NAME = lambda row: '%s//tr[%s]/td[1]' % (PROXY_LIST_TABLE, row)
PROXY_HOSTS = lambda row: '%s//tr[%s]/td[2]' % (PROXY_LIST_TABLE, row)
PROXY_PORTS_INFO = '%s//tr[2]/td[@class="pair-cell"]' % (PROXY_INFO_TABLE,)
AUTH_INFO_TABLE = '//dl[@class="box"][last()]'
AUTH_TABLE = '//dl[@class="box"][last()]//table[@class="pair-base"]'
AUTH_REALM_INFO = lambda row, column: '%s//tr[1]//tr[%s]/td[%s]' %\
                   (AUTH_TABLE, row, column)
AUTH_SEQ_INFO = lambda row, column: '%s//tr[2]//tr[%s]/td[%s]' %\
                    (AUTH_TABLE, row, column)
AUTH_UNREACH_ACTION = '%s/tbody/tr[last()]/td' % (AUTH_TABLE,)

class WebApplianceStatus(GuiCommon):

    """
    Keyword library for WebUI page Web -> Utilities -> Web Appliance Status
    """

    def get_keyword_names(self):
        return ['web_appliance_status_get_proxy',
                'web_appliance_status_get_basic',
                'web_appliance_status_get_authentication',
                'web_appliance_status_get_updates',
                'web_appliance_status_get_services',
                'web_appliance_status_get_appliances_list'
                ]

    def _open_page(self):
        self._navigate_to('Web', 'Utilities', 'Web Appliance Status')

        err_msgs = (('Centralized Configuration Manager is currently disabled',
                    guiexceptions.GuiFeatureDisabledError),
                    ('No Web Appliances are connected', guiexceptions.ConfigError))

        for err_msg, exception in err_msgs:
            if self._is_text_present(err_msg):
                  raise exception(err_msg)

    def _click_view_appliance_link(self, name):
         view_link = VIEW_APPLIANCE_LINK(name)

         if not self._is_element_present(view_link):
            raise ValueError('%s appliance is not on the list' % (name,))

         self.click_link(name)


    def _get_basic_info(self):
        result = cfgholder.CfgHolder()
        start_row = 2
        num_of_rows = int(self.get_matching_xpath_count(ROW_NUMBER(SYSTEM_TABLE)))

        for row in xrange(start_row, num_of_rows+1):

           if self._is_element_present(SYSTEM_INFO_ATTR_NAME_ROW(row)\
                   + '[@class="group top"]') or\
                   not(self._is_element_present(SYSTEM_INFO_ATTR_NAME_ROW(row))):
                continue

           result[self.get_text('xpath='\
                   + SYSTEM_INFO_ATTR_NAME_ROW(row)).rstrip(':').lower()] = \
                   self.get_text('xpath='+SYSTEM_INFO_ROW(row))

        return result

    def _get_publish_history(self):
        start_row = 2
        result = []
        num_of_rows = int(self.get_matching_xpath_count(ICCM_HIST_ROW('*', 1)))

        for row in xrange(start_row, num_of_rows + 1):
            row_info = []

            for column in xrange(1, 6):
                row_info.append(self.get_text('xpath='+ICCM_HIST_ROW(row, column)))
            result.append(row_info)

        return result

    def _get_services_info(self):
        start_row = 3
        start_col = 2
        temp = []
        result = cfgholder.CfgHolder()

        if self._is_text_present('One or more of the services '\
            'on the Web Appliance does not match'):
            start_row = 4

        num_of_rows = int(self.get_matching_xpath_count(\
                ROW_NUMBER(SERVICE_INFO_TABLE)+'[*]/td[1]'))
        num_of_col = int(self.get_matching_xpath_count(\
                SERVICE_COL_NUMBER(start_row-1)))

        for row in xrange(start_row, num_of_rows+start_row):
            # After AUCEU is data for getting which we use another keyword
            if self.get_text('xpath=' + ROW_NUMBER(SERVICE_INFO_TABLE)+'[%s]'\
                    % (row,)) == "Acceptable Use Controls Engine Updates":
                break
            try:
               key = (self.get_text('xpath=' + ROW_NUMBER(SERVICE_INFO_TABLE)\
                    +'[%s]/td[1]' % (row,))).lower()
            except:
               key = (self.get_text('xpath=' + ROW_NUMBER(SERVICE_INFO_TABLE)\
                    +'[%s]/td[1]' % (row+1,))).lower()
            for column in xrange(start_col, num_of_col+start_col):
                try:
                    value = self.get_text('xpath=' + SERVICE_INFO_ROW(row, column))
                except:
                    value = self.get_text('xpath=' + SERVICE_INFO_ROW(row+1, column))
                temp.append(value if value else None)
            result[key] = list()
            result[key] = temp[:]
            temp[:] = []
        return result

    def _get_proxy_ports(self):
        if self._is_text_present('HTTP Proxy is not configured.'):
            return None

        ports = self.get_text('xpath=' + PROXY_PORTS_INFO)
        return list(map( lambda item: item.strip(), ports.split(',')))

    def _get_proxies_list(self):
        if self._is_text_present('No upstream proxies configured'):
            return None

        proxies = []
        start_row = 2
        rows = int(self.get_matching_xpath_count(PROXY_GROUP_NAME('*')))

        for row in xrange(start_row, rows + start_row):
            group_name = self.get_text('xpath=' + PROXY_GROUP_NAME(row))
            hosts = self.get_text('xpath=' + PROXY_HOSTS(row))
            proxies.extend([group_name, hosts])

        return proxies

    def _get_proxy_info(self):
        result = cfgholder.CfgHolder()
        start_row = 1
        attributes = []
        num_of_rows = int(self.get_matching_xpath_count(ROW_NUMBER(PROXY_INFO_TABLE)))

        for row in xrange(start_row, num_of_rows + 1):
            attributes.append(self.get_text('xpath='\
                        +ROW_NUMBER(PROXY_INFO_TABLE)+'[%s]/th' % (row,)))

        methods = (self._get_proxies_list, self._get_proxy_ports)
        for key, method in zip(attributes, methods):
            result[key.rstrip(':').lower()] = method()

        return result

    def _get_auth_table_values(self, cell_locator, columns_num):
        num_of_rows = int(self.get_matching_xpath_count(cell_locator('*', 1)))
        start_row = 2
        result = []

        for row in xrange(start_row, num_of_rows + start_row):
            info_row = []
            for column in xrange(1, columns_num):
                info_row.append(self.get_text('xpath='+cell_locator(row, column)))
            result.extend(info_row)

        return result

    def _get_auth_realms(self):
        if self._is_text_present('No authentication realms configured.'):
            return None

        return self._get_auth_table_values(AUTH_REALM_INFO, 6)

    def _get_auth_seq(self):
        if self._is_text_present('No authentication sequences configured'):
            return None

        return self._get_auth_table_values(AUTH_SEQ_INFO, 3)

    def _get_auth_unreach_action(self):
        result = list()
        result.append(self.get_text('xpath=' + AUTH_UNREACH_ACTION))
        return result

    def _get_auth_info(self):
        start_row = 1
        attributes = []
        num_of_rows = int(self.get_matching_xpath_count(ROW_NUMBER(AUTH_INFO_TABLE)))

        for row in xrange(start_row, num_of_rows + 1):
            attributes.append(self.get_text('xpath='\
                        + ROW_NUMBER(AUTH_INFO_TABLE)+'[%s]/th' % (row,)))

        methods = (self._get_auth_realms, self._get_auth_seq,
                   self._get_auth_unreach_action)
        result = cfgholder.CfgHolder()

        for key, method in zip(attributes, methods):
            result[key.rstrip(':').lower()] = method()

        return result

    def _get_updates_info(self):
        start_row = 3
        start_col = 1
        temp = []
        result = cfgholder.CfgHolder()
        after = 0

        num_of_rows = int(self.get_matching_xpath_count(\
                ROW_NUMBER(SERVICE_INFO_TABLE) + '[*]'))

        for row in xrange(start_row, num_of_rows + 1):
            # Find out after which row update date is located
            if self.get_text('xpath=' + ROW_NUMBER(SERVICE_INFO_TABLE) + '[%s]'\
                    % (row,)) == "Acceptable Use Controls Engine Updates":
                after = 1
                num_of_col = int(self.get_matching_xpath_count(\
                        SERVICE_COL_NUMBER(row + 1)))
                continue

                # Is this element after AUCEU and after table columns header?
            if after and self._is_element_present('xpath='\
                    + ROW_NUMBER(SERVICE_INFO_TABLE) + '[%s]/td[1]' % (row,)):
                 # num_of_col+start_col-1 because last column doesn't contain
                 # anything
                 for column in xrange(start_col + 1, num_of_col+start_col - 1):
                    value = self.get_text('xpath=' + SERVICE_INFO_ROW(row, column))
                    temp.append(value if value else None)
                    key = self.get_text('xpath='\
                        + ROW_NUMBER(SERVICE_INFO_TABLE) + '[%s]/td[1]' % (row,))
                 key = key.rstrip(':').lower()
                 result[key] = list()
                 result[key] = temp[:]
                 temp[:] = []
        if after:
            return result
        else :
            return None

    def web_appliance_status_get_updates(self, app_name='', item=None):
        """Get "Acceptable Use Controls Engine Update versions" info from
        "Appliance status" table

        *Parameters*
            - `app_name`: name of the Web appliance to get status for.
            - `item` : name of row in table. If
              argument is None, keyword will
              return all data in the table as dictionary. If
              string is provided, keyword will return list of values in all
              cells' of this row except firs, which is name of this row.
              Default value is None.

        *Return*
            A dictionary object if table "Acceptable Use Controls Engine Update versions"
            exists or None if not.\n
            Keys for dictionary is text from first column of table.
            The value of keys is list of data from next two columns.
            First value in list represent "Web Appliance Version" column and
            second "Management Appliance Version"
            Example of return value :\n
            {'Application Visibility and Control Data': ['1303408490', 'N/A'],
            'Web Categorization Categories List': ['1304226000', 'N/A']}\n
            Also keyword can return a list if argument `item` is not None.
            Example of return value with item = Web Categorization Categories
            List :\n
            [ '1304226000', 'N/A']

        *Exceptions*
            - `ValueError`: in case of invalid name for Web appliance or invalid
              item argument.
            - `ConfigError`: in case no web appliances are connected.
            - `GuiFeatureDisabledError`: in case Centralized Configuration
                                          Manager is disabled.

        *Examples*
            | Web Appliance Status Get Updates | app_name=wsa104.wga |
            | ... | item=Web Categorization Categories List |
            | Web Appliance Status Get Updates | wsa103.wga |

        """
        self._open_page()

        self._click_view_appliance_link(app_name)

        result = self._get_updates_info()

        if  item != None and result != None:
            if item.lower() in result.keys():
                return result[item.lower()]
            else:
                raise ValueError("Key %s doesn't exists in the dictionary with\
                         result." % (item,))
        else:
            return result

    def web_appliance_status_get_services(self, app_name='',\
            service=None):
        """Get services info from "Security Services" table

        *Parameters*
            - `app_name`: name of the Web appliance to get status for.
            - `service`: name of service which status you want to get.
              If argument is None (which is default value) then status of all
              services will be provided. If you use this argument then keyword
              return a list.

        *Return*
            A dictionary object or list if argument `service` is provided.\n
            Keys for dictionary is lower case text from first column of table.
            The value of keys is list of data from other columns.
            List items is : "Web Appliance Service", "Is Service Displayed?",
            "Status", "Time Remaining", "Expiration Date"
            Keyword is robust to changing of number of columns, their sequences
            and names so it is recomended to look into what data represent each
            value in list.
            Example of return value :\n
            {'proxy mode': ['Transparent', 'N/A', None, None, None],
             'external dlp servers': ['Not Configured', 'N/A', None, None,
             None]}\n
            Also keyword can return a list if argument `service` is provided.
            Default value is None.
            Example of return value with service = proxy mode :\n
            ['Transparent', 'N/A', None, None, None]

        *Exceptions*
            - `ValueError`: in case of invalid name for Web appliance.
            - `ConfigError`: in case no web appliances are connected.
            - `GuiFeatureDisabledError`: in case Centralized Configuration
               Manager is disabled.

        *Examples*
            | Web Appliance Status Get Services | wsa104.wga |
            | ... | FTP Proxy, Webroot Anti-Malware |
            | Web Appliance Status Get Services | app_name=wsa103.wga |
            | ... | service=proxy mode |
            | Web Appliance Status Get Services | wsa103.wga | Sophos AntiVirus |
        """
        self._open_page()

        self._click_view_appliance_link(app_name)

        result = self._get_services_info()

        if service != None:
            if service.lower() in result.keys():
                return result[service.lower()]
            else:
                raise ValueError("Key %s doesn't exists in the dictionary with\
                        result." %(service,) )
        else:
            return result

    def web_appliance_status_get_basic(self, app_name='', item=None):
        """Get info from "Appliance status" table

        *Parameters*
            - `app_name`: name of the Web appliance to get status for.
            - `item`: name of row in table. If argument is None, keyword will
              return all data in the table as dictionary. If
              string is provided, keyword will return string value of cell of
              this row. Default value is None.

        *Return*
            A dictionary object.\n
            Keys for dictionary is text from first column of table.
            The value of keys is data from second columns.
            If row dosn't contain two columns it will be ommited.
            So if feacture "Centralized Configuration Manager" is disabled returned
            dictionary won't contain any information about it.
            Example of return value :\n
            {'Status': 'Waiting for data',
            'AsyncOS Install Date/Time': '2012-01-16 10:40:32',
            'Build Date': '2011-10-18',
            'Uptime': '4 days, 7 mins, 40 secs Up since: 16 Jan 2012 10:34
            (GMT)',
            'Serial Number': '0022190A87A1-4W7VHH1',
            'Last Data Transfer Attempt': 'N/A',
            'AsyncOS Version': '7.5.0-517 for Web',
            'Model': 'S660',
            'Host Name': 'wsa104.wga',
            'Configured Time Zone': 'Etc/GMT'}\n
            Also keyword can return a string if argument `item` is not None.
            Example of return value with item = Model :
             'S660'

        *Exceptions*
            - `ValueError`: in case of invalid name for Web appliance or invalid
              `item` argument.
            - `ConfigError`: in case no web appliances are connected.
            - `GuiFeatureDisabledError`: in case Centralized Configuration
               Manager is disabled.

        *Examples*
            | Web Appliance Status Get Basic | wsa104.wga |
            | Web Appliance Status Get Basic | app_name=wsa103.wga |
            | ... | item=Model |
        """
        self._open_page()

        self._click_view_appliance_link(app_name)

        result = self._get_basic_info()

        if  item != None:
            if item.lower() in result.keys():
                return result[item.lower()]
            else:
                raise ValueError("Key %s doesn't exists in the dictionary with\
                       result." %(item,) )
        else:
            return result

    def web_appliance_status_get_authentication(self,\
            app_name='', item=None):
        """Get info from "Authentication Service" table

        *Parameters*
            - `app_name`: name of the Web appliance to get status for.
            - `item` : name of row in table. If argument is None, keyword will
              return all data in the table as dictionary. If
              string is provided, keyword will return list of values in all
              cells' of this row except firs, which is name of this row.
              If row is empty or contain grey text, then return value will be
              None. Default value is None.

        *Return*
            A dictionary object.\n
            Keys for dictionary is text from first column of table.
            The value of keys is list of data from other columns or None if
            authentication service isn't configured.
            Each row has different number of colums. List items for first row represent values  "Name", "Protocol",
            "Servers", "Support Transparent User Identification"
            List items for second row represent values "Name" and "Order of Realms"
            List items for third row conatin single value
            Keyword is robust to changing of number of columns, their sequences
            and names so it is recomended to look into what data represent each
            value in list.
            Example of return value :\n
            {'Authentication Realms': ['LDAP', 'LDAP',
            'qa19.qa.sbr.ironport.com:389', 'No'],
             'Authentication Sequences': ['All Realms', 'Basic: LDAP'],
             'Unreachable Authentication Service Action': ['Block all traffic if
             authentication fails']\n
            Also keyword can return a list if argument `item` is not None.
            If row is empty or contain grey text, then return value will be
            None.
            Example of return value with item = Authentication Realms :\n
            ['LDAP', 'LDAP', 'qa19.qa.sbr.ironport.com:389', 'No']

        *Exceptions*
            - `ValueError`: in case of invalid name for Web appliance or invalid
              `item` argument.
            - `ConfigError`: in case no web appliances are connected.
            - `GuiFeatureDisabledError`: in case Centralized Configuration
               Manager is disabled.

        *Examples*
            | Web Appliance Status Get Authentication | wsa104.wga |
            | Web Appliance Status Get Authentication | app_name=wsa103.wga |
            | ... | item=Authentication Realms |
         """
        self._open_page()

        self._click_view_appliance_link(app_name)

        result = self._get_auth_info()

        if  item != None:
            if item.lower() in result.keys():
                return result[item.lower()]
            else:
                raise ValueError("Key %s doesn't exists in the dictionary with\
                        result." %(item,) )
        else:
            return result

    def web_appliance_status_get_proxy(self, app_name='', item=None):
        """Get info  from "Proxy Settings" table

        *Parameters*
            - `app_name`: name of the Web appliance to get status for.
            - `item` : name of row in table. If
              argument is None, keyword will return all data in the table as
              dictionary. If string is provided, keyword will return list of
              values in all cells' of this row except firs, which is name of
              this row. If row doesn't contain data or contain grey text, None
              will be returned. Default value is None.

        *Return*
            A dictionary object.\n
            Keys for dictionary is text from first column of table.
            The value of keys is list or None if proxy isn't configured.
            List items for first row represent values  "Group" and "Proxies"
            Each list items for second row contains separated port number.
            Example of return value :\n
            {'HTTP Ports to Proxy': ['80', '3128'],
             'Upstream Proxies': ['upqproxygroup', '10.92.147.36:3128']}\n
            Also keyword can return a list if argument `item` is not None.
            If row is empty or contain grey text, then return None.
            Example of return value with item = HTTP Ports to Proxy :\n
            ['80', '3128']

        *Exceptions*
            - `ValueError`: in case of invalid name for Web appliance or invalid
             `item` argument.
            - `ConfigError`: in case no web appliances are connected.
            - `GuiFeatureDisabledError`: in case Centralized Configuration
             Manager is disabled.

        *Examples*
            | Web Appliance Status Get Proxy | wsa104.wga |
            | Web Appliance Status Get Proxy | app_name=wsa103.wga |
            | ... | item=Upstream Proxies |
        """
        self._open_page()

        self._click_view_appliance_link(app_name)

        result = self._get_proxy_info()

        if  item != None:
            if item.lower() in result.keys():
                return result[item.lower()]
            else:
                raise ValueError("Key %s doesn't exists in the dictionary with\
                         result." %(item,) )
        else:
            return result

    def web_appliance_status_get_appliances_list(self):
        """Get info  from Web->Web Appliance Status page

        *Parameters*
            None.

        *Return*
            A dictionary object.\n
            Keys for dictionary is apliances name.
            The value of keys is list data from corresponding  row in the table.

        *Exceptions*
            None.

        *Examples*
            | ${app_status} | Web Appliance Status Get Appliances List |
        """
        self._open_page()
        ENTRY_ENTITIES = lambda row, col:\
               '//table[@class=\'cols\']/tbody/tr[%s]/td[%d]' % (str(row), col)
        entries = {}
        num_of_entries =\
           int(self.get_matching_xpath_count(ENTRY_ENTITIES('*', 1))) + 3
        for row in xrange(3, num_of_entries):
            name = self.get_text(ENTRY_ENTITIES(row,1))
            ip = self.get_text(ENTRY_ENTITIES(row, 2))
            os_version = self.get_text(ENTRY_ENTITIES(row, 3))
            if self._is_element_present(ENTRY_ENTITIES(row, 8)):
                user = self.get_text(ENTRY_ENTITIES(row, 4))
                job_name = self.get_text(ENTRY_ENTITIES(row, 5))
                configuration = self.get_text(ENTRY_ENTITIES(row, 6))
                service_enabled = self.get_text(ENTRY_ENTITIES(row, 7))
                service_disabled = self.get_text (ENTRY_ENTITIES(row, 8))
                entries[name] = [ip, os_version, user, job_name, configuration,\
                        service_enabled, service_disabled]
            else:
                service_enabled = self.get_text(ENTRY_ENTITIES(row, 5))
                service_disabled = self.get_text(ENTRY_ENTITIES(row, 6))
                entries[name] = [ip, os_version, service_enabled, service_disabled]
        return entries
