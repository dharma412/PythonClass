#!/usr/bin/env python -tt

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
import string


EDIT_SETTINGS_BUTTON = "//input[@value='Edit Settings']"
CANCEL_BUTTON = "//input[@value='Cancel']"
HEADER_TABLE = '//table[@class=\'pairs\']/tbody/'
HEADER_ROW = lambda row : '%s/tr[%s]/th[1]' % (HEADER_TABLE, row)
HEADER_DATA = lambda row : '%s/tr[%s]/td/table[@class=\'layout\']/tbody/tr/td[2]' % (HEADER_TABLE, row)


PAGE_PATH = ('Management','System Administration', 'SSL Configuration')

class SSLConfig(GuiCommon):
    def get_keyword_names(self):
        return ['edit_ssl_configuration_settings',
                'get_ssl_configuration_settings']

    @go_to_page(PAGE_PATH)
    def edit_ssl_configuration_settings(self,category,method,enable=None):
        """Edit SSL configuration settings

        *Parameters:*
        category - categrory to modify the ssl configs.
        ...  valid parameters are Appliance Management Web User Interface
        ...  LDAP Services
        ...  EUQ
        ...  Updater Service
        method  - method is modify the ssl types.
        ... valid parameters are
        ...  SSL v3,TLS v1.1,TLS v1.2,TLS v1.0
        mode - mode is enable or disable ssl type
        *Examples:*
        SSL Configuration Settings Edit
        ...  Appliance Management Web User Interface
        ...  SSL v3
        """
        categories_mapping = {'Appliance Management Web User Interface': 'WebUI',
                      'Secure LDAP Services': 'LDAPS',
                      'EUQ': 'EUQ',
                      'Updater Service': 'Updater',
                      'Peer Certificate FQDN Validation': 'peer_cert'}
        methods_mapping = {'TLS v1.0': 'TLSv1.0',
                   'SSL v3': 'SSLv3.0',
                   'TLS v1.1': 'TLSv1.1',
                   'TLS v1.2': 'TLSv1.2',
                   'FQDN': 'fqdn'}
        if category not in categories_mapping.keys():
            raise ValueError\
                   ('Invalid Key \'%s\' for category. '\
                       'Here are the valid category keys'\
                       '%s' % (category, categories_mapping.keys()))
        if method not in methods_mapping.keys():
            raise ValueError\
                   ('Invalid Key \'%s\' for method. '\
                       'Here are the valid method keys'\
                       '%s' % (method,methods_mapping.keys()))
        checkbox_locator = "//input[@id='{0}_{1}']".format(
                categories_mapping[category], methods_mapping[method])
        self.click_button(EDIT_SETTINGS_BUTTON)
        if self._is_element_present(checkbox_locator):
            if enable:
                if self._is_checked(checkbox_locator):
                    return
                self.select_checkbox(checkbox_locator)
            else:
                self._info("inside else loop")
                if self._is_checked(checkbox_locator):
                    self.unselect_checkbox(checkbox_locator)
            self._click_submit_button()
            return True
        return False

    @go_to_page(PAGE_PATH)
    def get_ssl_configuration_settings(self):
        """Get SSL configuration settings

        *Return:*
        - Dictionary. It has same set of items as in the `settings`

        *Examples:*
        | ${changed_settings}= | get_ssl_configuration_settings |
        | Log Dictionary | ${changed_settings} |
        """
        self._info('ssl_configuration_settings_get_all')
        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(HEADER_ROW('*')))
        for row in xrange(1, num_of_entries + 1):
            service_name = self.get_text(HEADER_ROW(row))
            versions = self.get_text(HEADER_DATA(row))
            service_name = string.replace(service_name,':','')
            versions = string.replace(versions,'\n'," ")
            versions = versions.split("  ")
            self._info(service_name)
            self._info(versions)
            entries[service_name] = versions

        return entries
