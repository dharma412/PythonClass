#!/usr/bin/env python
# $Repository: $
# $DateTime: 2020/02/04 22:25:40 $
# $Author: rajaks $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
import time


class DomainMap(GuiCommon):
    """Domain Map Settings page interaction class.
    'Web Security Manager -> Domain Map' section.
    """

    name_column = 2
    delete_column = 3

    table_id = "//table[@class='cols']"

    def get_keyword_names(self):
        return ['domain_map_add',
                'domain_map_delete',
                'domain_map_edit',
                'domain_map_get_list',
                ]

    def domain_map_get_list(self):
        """
        Returns: list of domain_map

        Examples:

        domains = domain_map_get_list()
        Should Be True/False for len(domains) == 2
        Should Be True/False for 'domain1' in domains
        """
        self._open_page()
        return self._get_policies().keys()

    def domain_map_add(self,
                       name,
                       ip_addresses,
                       order=1):
        """Adds the domain map

        Parameters:
        - `name`: domain name of the domain map. Mandatory.
        - `order`: processing order. Optional, '1' by default.
        - `ip_addresses`: IP addresses for the domain and IP mapping

        Return:

        Example:
        domain_map_add(nameOfDomain,'1.1.1.1/24,2.2.2.2/27',order=1)
        domain_map_add(nameOfDomain,'1.1.1.1,2.2.2.2/27',order=1)

        """

        self._open_page()
        self._click_add_domain_button()

        self._fill_name(name)
        self._fill_order(int(order))
        self._fill_ips(ip_addresses)

        # Click the submit button
        self._click_submit_button()

    def domain_map_edit(self,
                        name,
                        ip_addresses,
                        order=None,
                        regexes=None):

        """Updates the domain map

        Parameters:
        - `name`: domain name of the domain map. Mandatory.
        - `order`: processing order. Optional, '1' by default.
        - `ip_addresses`: IP addresses for the domain and IP mapping


        Return:

        Example:
        domain_map_edit(nameOfDomain,'1.1.1.1/24,2.2.2.2/27'order=1)
        domain_map_edit(nameOfDomain,'1.1.1.1,2.2.2.2/27',order=1)

        """

        self._open_page()
        self._click_edit_link(name)

        if order is not None:
            self._fill_order(str(order))
        if ip_addresses is not None:
            self._fill_ips(ip_addresses)

        self._click_submit_button(wait=False)

    def domain_map_delete(self, name):
        """Deletes the domain map

        Parameters:
        - `name`: The name of the domain to be deleted.

        Example:
        domain_map_delete(nameOfDomain)
        domain_map_delete(name=nameOfDomain)
        """

        self._open_page()
        self._click_delete_link(name)

    def _click_add_domain_button(self):
        """Click 'Add Domain...' button"""
        button = "xpath=//input[@title='Add Domain...']"
        self._wait_until_element_is_present(button)
        self.click_button(button)

    def _get_table_row_index(self, name):
        table_rows = self.get_matching_xpath_count('%s//tr' % \
                                                   (self.table_id,))
        for i in xrange(2, int(table_rows) + 1):
            policy_name = self.get_text('%s//tr[%s]//td[%s]' % \
                                        (self.table_id, i, self.name_column)).split(' \n')[0]
            if policy_name == name:
                return i
        return None

    def _click_edit_link(self, name):

        row = self._get_table_row_index(name)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(name,
                                                        'Domain Map')
        cell_id = 'xpath=%s//tr[%s]//td[%s]/a' % \
                  (self.table_id, row, self.name_column)

        self.click_element(cell_id)

    def _click_delete_link(self, name):

        start_time = time.time()
        while time.time() - start_time < 60:  # max possible timeout for worst scenario
            policy_row = self._get_table_row_index(name)
            if not policy_row is None:
                break
        else:
            raise guiexception.GuiControlNotFoundError('Domain Map: \
                   "%s" missing' % (name,))
        row = self._get_table_row_index(name)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(
                'Domain Map "%s" missing' % (name,),
                'Domain Maps')
        cell_id = 'xpath=%s//tr[%s]//td[%s]//img' % \
                  (self.table_id, row, self.delete_column)
        self.click_element(cell_id, "don't wait")
        self.click_button("xpath=//button[text()='Delete']")

    def _fill_name(self, name):

        self.input_text("//input[@id='domain_name']", name)

    def _fill_order(self, order):

        self.input_text("//input[@id='order']", order)

    def _fill_ips(self, sites):

        self.input_text("//textarea[@id='server_list']",
                        ', '.join(self._convert_to_tuple(sites)))

    def _open_page(self):
        """Open 'Domain Map' page """
        self._navigate_to('Web Security Manager', 'Domain Map')