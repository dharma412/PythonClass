# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/web/utilities/configuration_masters.py#3 $ $DateTime: 2020/05/25 10:52:22 $ $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from sal.exceptions import ConfigError
from zeus1380.gui.management.services.security_appliances import SecurityAppliances
import re

from sma.constants import (sma_config_masters, sma_config_source)

masters_map = {
        sma_config_masters.CM85: 'coeus_8_5',
        sma_config_masters.CM91: 'coeus_8_5',
        sma_config_masters.CM105: 'coeus_10_5',
        sma_config_masters.CM110: 'coeus_10_0',
        sma_config_masters.CM115: 'coeus_10_0',
        sma_config_masters.CM117: 'coeus_11_7',
        sma_config_masters.CM118: 'coeus_11_8',
        sma_config_masters.CM120: 'coeus_12_0',
        sma_config_masters.CM125: 'coeus_12_5',
        sma_config_masters.CM140: 'coeus_14_0'

    }

INITIALIZE_LINK = lambda version: 'xpath=//a[@onclick="doFormInitializeConfig(\'%s\');"]' % (version,)
EDIT_LINK = lambda master, version: 'xpath=//a[@onclick="doFormLoadConfiguration(\'%s\',\'%s\');"]' % (master,version,)
DEFAULT_INITIALIZATION_RADIOBUTTON = 'id=initialize_source_default'
COPY_INITIALIZATION_RADIOBUTTON = 'id=initialize_source_cm'
DISABLED_COPY_INITIALIZATION_RADIOBUTTON =\
    'xpath=//input[@id="initialize_source_cm" and @disabled="True"]'
COPY_CUSTOM_ROLES_CHECKBOX = 'id=use_custom_roles_box'
INITIALIZE_BUTTON = 'xpath=//input[@value="Initialize"]'
IMPORT_LINK = lambda version:\
    'xpath=//a[@onclick="doFormImportConfiguration(\'%s\');"]' % (version,)
CONFIG_SOURCE_LIST = 'id=config_source'
CONFIG_FILE_TEXTBOX =  'id=config_file'
LIST_LABEL = lambda label: 'label=%s' % (label,)
IMPORT_BUTTON = 'xpath=//input[@value="Import"]'
EDIT_ASSIGNMENT_BUTTON = 'xpath=//input[@value="Security Appliances"]'
DISABLED_EDIT_ASSIGNMENT_BUTTON = 'xpath=//input[@value="Security Appliances" '\
                                  'and @disabled="disabled"]'
ASSIGNMENT_TABLE = "//tbody[@class=\"yui-dt-data\"]"
APP_NAME_CELL = lambda row: 'xpath=%s//tr[%s]/td[1]' % (ASSIGNMENT_TABLE, row)
CONFIG_MASTER_ROW = lambda row, column: '%s//tr[%s]/td[%s]' %\
                    (ASSIGNMENT_TABLE, row, column)
CONFIG_MASTERS_HEADER = 'xpath=//tr[@class="yui-dt-last"]'
DISABLED_ASSIGN_CHECKBOX = lambda locator:\
    '%s[contains(@class, "checkbox-disabled")]' % (locator,)
NEW_BUTTON = 'xpath=//input[@value="New"]'
PROXY_INFO_TABLE = '//dl[@class="box"][last()-1]'
PROXY_LIST_TABLE = '%s//table[@class="cols"]' %  (PROXY_INFO_TABLE,)
CONFIG_MASTER_TABLE = lambda row: '%s//tr[%s]/td[1]' % (PROXY_LIST_TABLE, row)
CONFIG_MASTER_VALUE = lambda row, column: "xpath=//table[@class='cols']/tbody/tr[%s]/td[%s]" %\
                              (row, column)
CONFIG_MASTER_LIST = 'id=config_masters'
CONFIG_MASTER_NAME = "xpath=//input[@name='config_master_label_name']"

class ConfigurationMasters(SecurityAppliances):

    def get_keyword_names(self):
        return ['configuration_masters_initialize',
                'configuration_masters_import_config',
                'configuration_masters_edit_assignment',
                'select_new_config_master',
                'edit_config_master',
                'delete_config_master',
                'get_wsa_appliance_list']

    def _open_page(self):
        self._navigate_to('Web', 'Utilities', 'Configuration Masters')

        err_msg = 'Centralized Configuration Manager is currently disabled'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeatureDisabledError(err_msg)

    def _click_initialize_master_link(self, config_master):
        if config_master not in masters_map:
            raise ValueError('Invalid config master name - "%s"' %\
                             (config_master,))

        init_button = INITIALIZE_LINK(masters_map[config_master])
        if self._is_element_present(init_button):
            self.click_element(init_button)
        else:
            raise ConfigError('"%s" config master is already initialized' %\
                              (config_master,))

    def _edit_initialization_settings(self, default_settings, copy_roles):
        if default_settings:
            self._click_radio_button(DEFAULT_INITIALIZATION_RADIOBUTTON)
        elif self._is_element_present(DISABLED_COPY_INITIALIZATION_RADIOBUTTON):
            raise guiexceptions.GuiFeatureDisabledError(
                'Previous version of Config Master is not available.')
        else:
            self._click_radio_button(COPY_INITIALIZATION_RADIOBUTTON)
            self._check_copy_custom_roles_checkbox(copy_roles)

    def _check_copy_custom_roles_checkbox(self, copy_roles):
        if copy_roles is not None:
            if copy_roles:
                self.select_checkbox(COPY_CUSTOM_ROLES_CHECKBOX)
            else:
                self.unselect_checkbox(COPY_CUSTOM_ROLES_CHECKBOX)

    def _click_initialize_button(self):
        self.click_button(INITIALIZE_BUTTON)

    def _click_import_link(self, config_master):
        if config_master not in masters_map:
            raise ValueError('%s master in not available' % (config_master,))

        import_link = IMPORT_LINK(masters_map[config_master])
        if self._is_element_present(import_link):
            self.click_element(import_link)
        else:
            raise ValueError('Import for "%s" is not available' % (config_master,))

    def _set_config_source(self, source, filepath, copy_roles):
        sources = self.get_list_items(CONFIG_SOURCE_LIST)
        if source in sources:
            self.select_from_list(CONFIG_SOURCE_LIST, LIST_LABEL(source))

            if sma_config_source.CONFIG_FILE == source:
                self._fill_config_file_textbox(filepath)
            else:
                self._check_copy_custom_roles_checkbox(copy_roles)
        else:
            raise ValueError('%s source is not available' % (source,))

    def _fill_config_file_textbox(self, config_file):
        if config_file is None:
            raise ConfigError('The path to configuration file should be provided.')
        self.choose_file(CONFIG_FILE_TEXTBOX, config_file)

    def _click_import_button(self):
        self.click_button(IMPORT_BUTTON, "don't wait")

    def _click_edit_assignment_button(self):
        if self._is_element_present(DISABLED_EDIT_ASSIGNMENT_BUTTON):
            raise guiexceptions.GuiFeatureDisabledError(
                'Appliance assignment is not available')

        self.click_button(EDIT_ASSIGNMENT_BUTTON)

    def _click_new_button(self):
        self.click_button(NEW_BUTTON)

    def _assign_appliances(self, appliance, cm):
        err_msg = 'No appliances have been added'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeatureDisabledError(err_msg)

        assignment_map = self._build_config_masters_links()

        #for appliance, cm in assignment.iteritems():
        if appliance not in assignment_map:
            raise ValueError('"%s" appliance name does not exist' %\
                    (appliance,))

        if cm not in assignment_map[appliance]:
            raise ValueError('"%s" config master does no exist' %\
                    (cm,))

        assign_checkbox = assignment_map[appliance][cm]
        if  "assign_checkbox[contains (@class , 'checkbox-checked')]":
            return True

        #self._select_checkbox(assign_checkbox)

    def _build_config_masters_links(self):
        apps_map = {}
        start_column = 4
        rows = self._get_num_of_rows()
        colums = self._get_num_of_columns()
        config_masters = self._get_available_config_masters()

        for i in xrange(1, rows+1):
            name = self.get_text(APP_NAME_CELL(i))
            config_masters_map = {None: CONFIG_MASTER_ROW(i, start_column)}
            for index, master_name in enumerate(config_masters):
                config_masters_map[master_name] =\
                    CONFIG_MASTER_ROW(i, start_column+index+1)
            apps_map[name] = config_masters_map

        return apps_map

    def _get_available_config_masters(self):
        normalized_masters = []
        masters = self.get_text(CONFIG_MASTERS_HEADER)
        for master in masters.split('\n'):
            normalized_masters.append('Configuration Master %s' %\
                master.strip())
        return normalized_masters

    def _get_num_of_rows(self):
        return int(self.get_matching_xpath_count(ASSIGNMENT_TABLE + '//tr'))

    def _get_num_of_columns(self):
        return int(self.get_matching_xpath_count(ASSIGNMENT_TABLE + '//tr/td'))

    def configuration_masters_initialize(self, config_master, default_settings=None,
                   copy_roles=None):
        """Initialize Configuration Master.

        Parameters:
            - `config_master`: name of the configuration master to initialize.
              Can be one of sma_config_masters constant values:
                    - 'Configuration Master 8.0'
                    - 'Configuration Master 7.7'
                    - 'Configuration Master 7.5'
            - `default_settings`: use default settings for initialization.
              Boolean. False to copy initialization settings from previous
              version.
            - `copy_roles`: copy custom roles. Boolean. Applies only if
              `default_settings` is False.

        Exceptions:
            - `ValueError`: in case of invalid value of `config_master`.
            - `ConfigError`: in case if Configuration Master is already
              initialized.
            - `GuiFeatureDisabledError`: in case if Centralized Configuration
              Manager is disabled or there is no ability to copy initialization
              settings from previous version.

        Examples:
            | Configuration Masters Initialize | ${sma_config_masters.CM80} | {True} |
            | Configuration Masters Initialize | ${sma_config_masters.CM75} | {False} |
        """
        self._open_page()
        try: # that's the right new way to click Continue button
            self.click_button(continue_button)
            self._click_initialize_master_link(config_master)
        except:
            self._click_initialize_master_link(config_master)

        if default_settings is not None:
            self._edit_initialization_settings(default_settings, copy_roles)

        self._click_initialize_button()

        ready_msg = 'successfully initialized'
        self.wait_until_page_contains(ready_msg, 30)
        self._debug('successfully initialized')

    def select_new_config_master(self,config_master,name,source=None,filepath=None,copy_roles=None):
        """
           Select New Config Master | ${sma_config_masters.CM80} | ${sma_config_source.CONFIG_FILE} | filepath=i${PATH}
        """
        self._open_page()
        ENTRY_ENTITIES = lambda row, col:\
                       '//table[@class=\'cols\']/tbody/tr[%s]/td[%d]' % (str(row), col)
        rows = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*', 1))) + 2
        for i in range(2,rows+2):
            if self._is_element_present(CONFIG_MASTER_VALUE(i, 1)):
                if self.get_text(CONFIG_MASTER_VALUE(i,1)) == config_master:
                    config_status = self.get_text(CONFIG_MASTER_VALUE(i,4))
                    break
        if 'Initialized' in config_status:
            self._click_new_button()
            self.input_text(CONFIG_MASTER_NAME,name)
            self.select_from_list(CONFIG_MASTER_LIST, LIST_LABEL(config_master[0:4]))
            try:
               self._set_config_source(source,filepath,copy_roles)
            finally:
               self._click_submit_button()

    def edit_config_master(self,config_master):
        self._open_page()
        ENTRY_ENTITIES = lambda row, col:\
                       '//table[@class=\'cols\']/tbody/tr[%s]/td[%d]' % (str(row), col)
        rows = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*', 1))) + 2
        edit_button = ""
        for i in range(2,rows+3):
            if self._is_element_present(CONFIG_MASTER_VALUE(i, 1)):
                 if self.get_text(CONFIG_MASTER_VALUE(i,1)) == config_master:
                     edit_button = CONFIG_MASTER_VALUE(i,2)
                     break
        edit_button = edit_button + "/a"
        if self._is_element_present(edit_button):
            self.click_element(edit_button)
            self._click_continue_button(text="Ok")
            return  self.get_text(CONFIG_MASTER_VALUE(i,2))
        else:
            raise ConfigError('"%s" config master is editing' %\
                             (config_master,))

    def delete_config_master(self,config_master):
        self._open_page()
        ENTRY_ENTITIES = lambda row, col:\
                        '//table[@class=\'cols\']/tbody/tr[%s]/td[%d]' % (str(row), col)
        rows = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*', 1))) + 2
        delete_button = ""
        for i in range(2,rows+3):
            if self._is_element_present(CONFIG_MASTER_VALUE(i, 1)):
                 if self.get_text(CONFIG_MASTER_VALUE(i,1)) == config_master:
                     delete_button = CONFIG_MASTER_VALUE(i,5)
                     break
        delete_button = delete_button + "/img"
        if self._is_element_present(delete_button):
            self.click_element(delete_button)
            self._click_continue_button(text="Delete")
        else:
            raise ConfigError('"%s" config master cannot be deleted' %\
                             (config_master,))

    def get_wsa_appliance_list(self):
        self._open_page()
        appliance_list={}
        ENTRY_ENTITIES = lambda row, col:\
                  '//table[@class=\'cols\']/tbody/tr[%s]/td[%d]' % (str(row), col)
        rows = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*', 1))) + 2
        for i in range(2,rows+3):
            if self._is_element_present(CONFIG_MASTER_VALUE(i, 1)):
                config_master= self.get_text(CONFIG_MASTER_VALUE(i,1))
                appliance_list[config_master]=  self.get_text(CONFIG_MASTER_VALUE(i,3))
        return appliance_list

    def configuration_masters_import_config(self, config_master, source, filepath=None,
                      copy_roles=None):
        """Import web configuration for Configuration Master.

        Parameters:
            - `config_master`: name of the Configuration Master to import
              configuration for. Can be one of sma_config_masters constant
              values:
                    - 'Configuration Master 8.0'
                    - 'Configuration Master 7.7'
                    - 'Configuration Master 7.5'
            - `source`: source of configuration to import. Can be Web
              Configuration File or one of sma_config_masters constant values.
              If 'source' is not Web Configuration File, than it could be
              only one of previous older versions of configuration masters for
              specified 'config_master'.
            - `filepath`: full path to configuration file. Applies only if
              'source' is 'Web Configuration File'.
            - `copy_roles`: copy custom roles. Applies only if `source` is
              'Configuration Master'. Boolean.

        Exceptions:
            - `ValueError`: in case of invalid value for `config_master`,
              `source` or `filepath`.
            - `ConfigError`: in case if no `filepath` was provided when `source`
              is 'Web Configuration File'.
            - `GuiFeatureDisabledError`: in case if Centralized Configuration
              Manager is disabled, Configuration Master is not initialized or
              configuration source is not available.

        Examples:
            | Configuration Masters Import Config | ${sma_config_masters.CM80} | ${sma_config_source.CONFIG_FILE} | filepath=i${PATH} |
            | Configuration Masters Import Config | ${sma_config_masters.CM80} | ${sma_config_masters.CM63} | copy_roles=${True} |

            """
        self._open_page()

        #self._click_import_link(config_master)
        ENTRY_ENTITIES = lambda row, col:\
                         '//table[@class=\'cols\']/tbody/tr[%s]/td[%d]' % (str(row), col)
        rows = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*', 1))) + 2
        import_button = ""
        config_master = re.sub('Configuration Master ','', config_master)
        for i in range(2,rows+3):
            if self._is_element_present(CONFIG_MASTER_VALUE(i, 1)):
                 if self.get_text(CONFIG_MASTER_VALUE(i,1)) == config_master:
                     import_button = CONFIG_MASTER_VALUE(i,4)
                     break
        import_button = import_button + "/a"
        if self._is_element_present(import_button):
            self.click_element(import_button)
            self._set_config_source(source, filepath, copy_roles)
            self._click_import_button()
            if source == sma_config_source.CONFIG_FILE:
                self._click_continue_button()
        else:
            raise ConfigError('"%s" config master import is disabled' %\
                                          (config_master,))

    def configuration_masters_edit_assignment(self, appliance_name, appliance_assignment):
        """Edit appliance assignment list.

        Parameters:
            - `appliance_name`: appliance that will be assigned to
              Configuration Master.
            - `appliance_assignment`: appliance assignment can be one of
              sma_config_masters constant values:
                    - 'Configuration Master 8.0'
                    - 'Configuration Master 7.7'
                    - 'Configuration Master 7.5'
              or None to not assign appliance to any of the Configuration
              Masters.

        Exceptions:
            - `ValueError`: in case of invalid value for appliance name or
              appliance assignment.
            - `ConfigError`: in case if checkbox to assign appliance to
              Configuration Master is disabled.
            - `GuiFeatureDisabledError`: in case of inability to assign
              appliance, Configuration Master is not initialized of Centralized
              Configuration Manager is disabled.

        Examples:
            | Configuration Masters Edit Assignment | wsa103.wga | ${sma_config_masters.CM80} |
            | Configuration Masters Edit Assignment | wsa104.wga | ${sma_config_masters.CM75} |
        """
        self._open_page()

        self._click_edit_assignment_button()

        self.security_appliances_edit_web_appliance\
                (name=appliance_name, config_master=appliance_assignment, config_master_edit=True)
        #return self._assign_appliances(appliance_name, appliance_assignment)

        #self._click_submit_button()
