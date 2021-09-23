#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/smtp_relay.py#1 $

import re
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ADD_ROW_BUTTON = \
    "xpath=//input[@id='relay_hosts_domtable_AddRow' and @class='button-secondary']"
DELETE_ROW_LINK = lambda index:\
            'xpath=//tr[@id="relay_hosts_row%s"]/td[3]/img' % (index,)
RELAYS_TBODY_ROW = '//tbody[@id="relay_hosts_rowContainer"]/tr'
SMTP_RELAY_TEXTBOX = lambda index, info_type: 'id=relay_hosts[%s][%s]' %\
                                              (index, info_type)
ROUTING_TABLE_LIST = 'name=routing_table'
ROUTING_TABLE_ITEM = lambda table_name: 'label=%s' % (table_name,)

DEFAULT_PORT = u'25'

class SmtpRelay(GuiCommon):
    """Internal SMTP Relay settings page interaction class."""

    def get_keyword_names(self):
        return ['smtp_relay_edit']

    def _open_page(self):
        self._navigate_to('Network', 'Internal SMTP Relay')

    def _get_table_rows_ids(self):
        ids = []
        row_pattern = re.compile('relay_hosts\[(\d+)\]\[host\]')
        text_fields = self._get_all_fields()
        for field in text_fields:
            result = row_pattern.search(field)
            if result:
                ids.append(result.group(1))
        return ids

    def _add_table_rows(self, rows_num):
        for i in xrange(rows_num):
            self.click_button(ADD_ROW_BUTTON, "don't wait")

    def _delete_table_rows(self, rows_num):
        rows_ids = self._get_table_rows_ids()
        for i in xrange(rows_num):
            self.click_element(DELETE_ROW_LINK(rows_ids[i]), "don't wait")

    def _set_smtp_relays_table(self, rows_num):
        num_of_entries = int(self.get_matching_xpath_count(RELAYS_TBODY_ROW))
        rows_diff = rows_num - num_of_entries
        if rows_diff < 0:
            self._delete_table_rows(abs(rows_diff))
        elif rows_diff > 0:
            self._add_table_rows(rows_diff)

    def _fill_smtp_relay_row(self, relay, index):
        if len(relay) is 1:
            port = DEFAULT_PORT
        else:
            port = relay[1]
        for entry, link in zip((relay[0], port), ('host', 'port')):
            self.input_text(SMTP_RELAY_TEXTBOX(index, link), entry)

    def _fill_smtp_relays_table(self, relays):
        if relays is not None:
            self._set_smtp_relays_table(len(relays))
            row_ids = self._get_table_rows_ids()

            for relay, index in zip(relays, row_ids):
                self._fill_smtp_relay_row(relay, index)

    def _select_routing_table(self, table):
        if table is not None:
            if self._is_visible(ROUTING_TABLE_LIST) and\
                table in self.get_list_items(ROUTING_TABLE_LIST):
                self.select_from_list(ROUTING_TABLE_LIST,
                                       ROUTING_TABLE_ITEM(table))
            else:
                raise guiexceptions.ConfigError(
                                '"%s" table is not configured.' % (table,))

    def smtp_relay_edit(self, smtp_relays=None, routing_table=None):
        """Edit internal SMTP relay settings.

        Parameters:
        - `smtp_relays`: a comma separated list of strings 'host:port'.
                    String 'clear' to clear the table. Default port is 25.
                    If None, value will be left unchanged.
        - `routing_table`: routing table to use for SMTP. Either 'Data' or
                        'Management'. If none, value will be left unchanged.

        Example:
        | Smtp Relay Edit | smtp_relays=mail.qa:25, services.wga:25, test.com |
        | Smtp Relay Edit | smtp_relays=clear | routing_table=Data |
        | Smtp Relay Edit | routing_table=Data |
        """
        if smtp_relays is not None:
            if smtp_relays.lower().strip() == 'clear':
                smtp_relays = tuple()
            else:
                smtp_relays = tuple([tuple(item.split(':')) for item\
                                in self._convert_to_tuple(smtp_relays)])
        self._open_page()
        self._click_edit_settings_button()
        self._fill_smtp_relays_table(smtp_relays)
        self._select_routing_table(routing_table)
        self._click_submit_button(wait=False)
