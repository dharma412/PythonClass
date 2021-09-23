#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/network/smtp_routes.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

import re
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ADD_ROUTE_BUTTON = 'xpath=//input[@value="Add Route..."]'
DELETE_ROUTE_CHECKBOX = lambda route: 'xpath=//input[@value="%s"]' % (route,)
DELETE_ROUTES_BUTTON = 'id=_click'
CLEAR_ROUTES_BUTTON = 'xpath=//input[@value="Clear All Routes"]'
IMPORT_ROUTES_BUTTON = 'xpath=//input[@value="Import Routes..."]'
IMPORT_CONFIRM_BUTTON = '//button[text()="Import"]'
CONFIG_FILES_LIST = 'id=impexpfile'
EXPORT_ROUTES_BUTTON = 'xpath=//input[@value="Export Routes..."]'
EXPORT_FILENAME_TEXTBOX = 'name=file_server'
DOMAIN_CELL_TEXT = lambda row: '//table[@class="cols"]//tr[%s]/td[1]' % (row,)
PAGE_SIZE_LIST = 'id=pageSize'
SHOW_ALL_PAGES = 'All'
LIST_LABEL = lambda label: 'label=%s' % (label,)
RECEIVING_DOMAIN_TEXTBOX = 'name=new_domain'
DESTINATION_HOST_TEXTBOX = lambda row: 'id=dest_hosts[%s][val]' % (row,)
DESTINATION_HOST_ROW = '//tbody[@id="dest_hosts_rowContainer"]/tr'
ADD_ROW_BUTTON = 'id=dest_hosts_domtable_AddRow'
DELETE_ROW_BUTTON = lambda row: '//tr[@id="dest_hosts_row%s"]/td[2]/img' % \
                                (row,)
OVERWRITE_BUTTON = 'xpath=//button[text()="Overwrite"]'
CANCEL_BUTTON = 'xpath=//button[text()="Cancel"]'
SUBMIT_BUTTON = 'xpath=//input[@value="Submit"]'
ALL_OTHER_DOMAINS = '//a[contains(@href,"domain=ALL")]'


class SmtpRoutes(GuiCommon):
    """
    Keyword library for menu Management Appliance -> Network -> SMTP Routes
    """

    def get_keyword_names(self):
        return ['smtp_routes_add',
                'smtp_routes_clear',
                'smtp_routes_delete',
                'smtp_routes_import',
                'smtp_routes_export',
                'smtp_routes_edit',
                'smtp_routes_get_receiving_domain_list',
                'smtp_routes_get_smtp_routes',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'Network', 'SMTP Routes')

    def _click_add_route_button(self):
        self.click_button(ADD_ROUTE_BUTTON, "don't wait")
        self._info('Clicked "Add Route..." button.')

    def _fill_receiving_domain(self, domain):
        self.input_text(RECEIVING_DOMAIN_TEXTBOX, domain)
        self._info('Set receiving domain to "%s".' % (domain,))

    def _fill_destination_hosts_table(self, hosts):
        self._setup_table(len(hosts))
        rows_id = self._get_table_rows_ids()

        for num, host in enumerate(hosts):
            self._fill_destination_host_row(host, rows_id[num])

    def _fill_destination_host_row(self, host, row):
        self.input_text(DESTINATION_HOST_TEXTBOX(row), host)
        self._info('Filled row with "%s" host.' % (host,))

    def _click_edit_route_link(self, domain):
        self._show_all_routes()

        if self._is_element_present('link=' + domain):
            self.click_link(domain)
            self._info('Clicked edit "%s" domain.' % (domain,))
        else:
            raise ValueError('"%s" receiving domain does not exist' % \
                             (domain,))

    def _click_delete_routes_checkboxes(self, domains):
        domains_to_del = domains.split(',')
        self._show_all_routes()

        for domain in domains_to_del:
            delete_link = DELETE_ROUTE_CHECKBOX(domain.strip())

            if self._is_element_present(delete_link):
                self.select_checkbox(delete_link)
                self._info('Checked delete checkbox for "%s" domain.' % \
                           (domain,))
            else:
                raise ValueError('"%s" receiving domain does not exist' % \
                                 (domain,))

    def _get_table_rows_ids(self):
        fields_nums = []
        field_patt = re.compile('dest_hosts\[(\d+)\]')
        text_fields = self._get_all_fields()
        for field in text_fields:
            result = field_patt.search(field)
            if result:
                fields_nums.append(result.group(1))
        return fields_nums

    def _setup_table(self, num_of_rows):
        num_of_entries = int(self.get_matching_xpath_count(DESTINATION_HOST_ROW))
        rows_diff = num_of_rows - num_of_entries
        if rows_diff < 0:
            self._click_delete_row_button(abs(rows_diff))
        elif rows_diff > 0:
            self._click_add_row_button(rows_diff)

    def _click_delete_row_button(self, rows):
        rows_ids = self._get_table_rows_ids()
        for i in xrange(rows):
            self.click_button(DELETE_ROW_BUTTON(rows_ids[i]), "don't wait")
        self._info('Deleted %s row(s).' % (rows,))

    def _click_add_row_button(self, rows):
        for i in xrange(rows):
            self.click_button(ADD_ROW_BUTTON, "don't wait")
        self._info('Clicked "Add row" button %s time(s).' % (rows,))

    def _show_all_routes(self):
        if self._is_element_present(PAGE_SIZE_LIST) and \
                str(self.get_value(PAGE_SIZE_LIST)) != SHOW_ALL_PAGES:
            self.select_from_list(PAGE_SIZE_LIST,
                                  LIST_LABEL(SHOW_ALL_PAGES), SHOW_ALL_PAGES)
            self._info('Selected to show all routes on current page.')

    def _click_delete_button(self):
        self.click_button(DELETE_ROUTES_BUTTON, "don't wait")
        self._info('Clicked "Delete" button.')

    def _click_clear_routes_button(self):
        if self._is_element_present(CLEAR_ROUTES_BUTTON):
            self.click_button(CLEAR_ROUTES_BUTTON, "don't wait")
            self._info('Clicked "Clear All Routes" button.')
        else:
            raise guiexceptions.GuiFeatureDisabledError(
                'There are no configured routes.')

    def _click_import_routes_button(self):
        self.click_button(IMPORT_ROUTES_BUTTON, "don't wait")
        self._info('Clicked "Import Routes..." button.')

    def _select_file_to_import(self, filename):
        config_files = self.get_list_items(CONFIG_FILES_LIST)
        if filename in config_files:
            self.select_from_list(CONFIG_FILES_LIST, LIST_LABEL(filename))
            self._info('Selected "%s" configuration file to import.' % \
                       (filename,))
        else:
            raise ValueError('"%s" configuration file does not exist' % \
                             (filename,))

    def _click_export_routes_button(self):
        if self._is_element_present(EXPORT_ROUTES_BUTTON):
            self.click_button(EXPORT_ROUTES_BUTTON, "don't wait")
            self._info('Clicked "Export Routes..." button.')
        else:
            raise guiexceptions.GuiFeatureDisabledError(
                'Unable to export routes. There are no configured routes.')

    def _fill_config_filename(self, filename):
        self.input_text(EXPORT_FILENAME_TEXTBOX, filename)
        self._info('Exporting to "%s" filename.' % (filename,))

    def _get_destination_hosts(self):
        hosts = []
        rows_ids = self._get_table_rows_ids()
        for index in rows_ids:
            hosts.append(self.get_value(DESTINATION_HOST_TEXTBOX(index)))
        return hosts

    def _get_list_of_domains(self):
        domains = []
        starting_row = 2
        num_of_rows = int(self.get_matching_xpath_count(DOMAIN_CELL_TEXT('*')))
        for row in xrange(starting_row, num_of_rows + starting_row):
            domains.append(self.get_text('xpath=' + DOMAIN_CELL_TEXT(row)))
        return domains

    def smtp_routes_add(self, recv_domain, dest_hosts):
        """Add SMTP route.

        *Parameters*
            - ` recv_domain`: receiving domain to set up route(s) for. String
              of comma-separated values.
              If recv_domain is equal to "All" then this smtp route will be
              provided as default route.
            - `dest_hosts`: destination host(s). If multiple hosts are provided
              they must be comma-separated value. Port number can be specified by
              adding ':<port number>' to the destination host.

        *Return*
            None.

        *Exceptions*
            - `GuiValueError`: in case of malformed `dest_hosts` or
             `recv_damian` value.

        *Example*
            | Smtp Route Add | ironport.com | smtp.cisco.com |
            | Smtp Route Add | anysite.com | smtp.mysite.com:25, spam.com:110 |
            | Smtp Route Add | mysite.org | fbi.gov:25, cia.gov:254, nsa.com:50 |
            | Smtp Route Add | All | smtp.cisco.com |
        """
        self._info('Adding SMTP route(s) for "%s" domain.' % (recv_domain,))

        self._open_page()

        if recv_domain.lower() != "all":
            self._click_add_route_button()
            self._fill_receiving_domain(recv_domain)

        else:
            self.click_button(ALL_OTHER_DOMAINS, "don't wait")

        self._fill_destination_hosts_table(self._convert_to_tuple(dest_hosts))

        self._click_submit_button(False)

        self._info('Added SMTP route(s) for "%s" domain.' % (recv_domain,))

    def smtp_routes_edit(self, recv_domain, dest_hosts=None, new_recv_domain=None):
        """Edit SMTP route.

        *Parameters*
            - `recv_domain`: receiving domain to edit.
                If recv_domain is equal to All then default smtp route will be edited. In
                this case argument `new_recv_domain` will be ignored.
            - `dest_hosts`: destination host(s). If multiple hosts are provided
                they must be comma-separated value. Port number can be specified by
                adding ':<port number>' to the destination host.
            - `new_recv_domain`: new receiving domain to set up route(s) for.
                None to leave configuration unchanged.

        *Return*
            None.

        *Exceptions*
            - `ValueError`: in case `recv_domain` is not present in SMTP routes
                   table or value of `dest_hosts` is malformed.
        *Examples*
            | Smtp Route Edit | ironport.com |
            | ... | new_recv_domain=anysite.com|
            | ... | dest_hosts=smtp.cisco.com |
            | Smtp Route Edit | anysite.com | smtp.mysite.com:25, spam.com:110 |
            | ... | site.com |
            | Smtp Route Edit | mysite.org |
            | ... | dest_hosts=fbi.gov:25, cia.gov:254, nsa.com:50 |
            | Smtp Route Edit | All | dest_hosts=example.com |
        """
        self._info('Editing SMTP route(s) for "%s" domain.' % (recv_domain,))

        self._open_page()

        if recv_domain.lower() != 'all':
            self._click_edit_route_link(recv_domain)
        else:
            self.click_button(ALL_OTHER_DOMAINS, "don't wait")

        if new_recv_domain != None and recv_domain.lower() != 'all':
            self._fill_receiving_domain(new_recv_domain)

        if dest_hosts != None:
            self._fill_destination_hosts_table(self._convert_to_tuple(dest_hosts))

        self._click_submit_button(False)

        self._info('Edited SMTP route(s) for "%s" domain.' % \
                   (recv_domain,))

    def smtp_routes_delete(self, recv_domain):
        """Delete SMTP route(s).

        *Parameters*
            - `recv_domain`: domain(s) for which routes will be deleted.
              Comma-separated string.

        *Return*
            None.

        *Exceptions*
            - `ValueError`: in case any of `recv_domain` is not present in SMTP
                routes table.

        *Examples*
            | Smtp Route Delete | ironport.com |
            | Smtp Route Delete | anysite.com, site.com, smtp.mysite.com |
            | Smtp Route Delete | mysite.org, fbi.gov |
        """
        self._info('Deleting routes for "%s" domain(s).' % (recv_domain,))

        self._open_page()

        self._click_delete_routes_checkboxes(recv_domain)

        self._click_delete_button()

        self._click_continue_button()

        self._info('Deleted routes for "%s" domain(s).' % (recv_domain,))

    def smtp_routes_clear(self):
        """Clear SMTP routes table.

        *Return*
            None.

        *Exceptions*
            - `GuiFeatureDisabledError`: in case there are no configured
                 routes.

        *Examples*
            | Smtp Routes Clear |
        """
        self._info('Clearing SMTP routes table.')

        self._open_page()

        self._click_clear_routes_button()

        self._click_continue_button()

        self._info('Cleared SMTP routes table.')

    def smtp_routes_import(self, filename):
        """Import SMTP routes configuration from file.

        *Parameters*
            - `filename`: name of the file to import configuration from. All
              routes will be rewrited.

        *Return*
            None.

        *Exceptions*
            - `ValueError`: in case `filename` does not exist.

        *Examples*
            | Smtp Routes Import | myroutes.txt |
            | Smtp Routes Import | otherfile.txt |
        """
        self._info('Importing SMTP routes configuration from "%s".' % \
                   (filename,))

        self._open_page()

        self._click_import_routes_button()

        self._select_file_to_import(filename)

        self._click_submit_button(wait=False, skip_wait_for_title=True)

        self.click_button(IMPORT_CONFIRM_BUTTON)

        self._info('Imported SMTP routes configuration from "%s" file.' % \
                   (filename,))

    def smtp_routes_export(self, filename, overwrite=True):
        """Export SMTP routes configuration to file.

        *Parameters*
            - `filename`: name of the file to export configuration to.
            - `overwrite`: overwrite file if it exists. Boolean. If True,
              existing file with the same name will be overwited. If False,
              existing file with the same name wont be overwited. If file with
              the same name exists, keyword will return True. None in other
              case.

        *Return*
            False file with `filename` doesn't exist. True in other case.

        *Exceptions*
            - `GuiFeatureDisabledError`: in case there are no configured
                  routes.

        *Examples*
            | Smtp Routes Export | myroutes.txt | overwrite=${FALSE} |
            | Smtp Routes Import | otherfile.txt |
        """
        self._info('Exporting SMTP routes configuration to "%s".' % \
                   (filename,))

        self._open_page()

        self._click_export_routes_button()

        self._fill_config_filename(filename)

        self.click_button(SUBMIT_BUTTON, "don't wait")

        self._check_action_result()

        if self._is_text_present("already exists"):

            if overwrite:
                self._info("File %s is overwrited" % (filename,))
                self.click_button(OVERWRITE_BUTTON)
                return True
            else:
                self.click_button(CANCEL_BUTTON, "don't wait")

        return False

    def smtp_routes_get_receiving_domain_list(self):
        """Get list of configured receiving domains.

        *Return*
            A list of strings of currently configured receiving domains.
            If no domains was configure, keyword will return empty list.

        *Exceptions*
            None.

        *Examples*
            | Smtp Routes Get Receiving Domain List |
        """
        self._info('Retrieving list of receiving domains.')

        self._open_page()

        return self._get_list_of_domains()

    def smtp_routes_get_smtp_routes(self, recv_domain):
        """Get  list of configured SMTP routes for receiving domain.

        *Return*
            A list of strings of currently configured SMTP routes for
            `recv_domain`.

        *Exceptions*
            - `ValueError`: in case `recv_domain` is not present in SMTP
               routes table.

        *Examples*
            | Smtp Routes Get Smtp Routes | anysite.com |
            | Smtp Routes Get Smtp Routes | site.com |
        """
        self._info('Retrieving SMTP routes for "%s" domain.' % (recv_domain,))

        self._open_page()

        self._click_edit_route_link(recv_domain)

        return self._get_destination_hosts()
