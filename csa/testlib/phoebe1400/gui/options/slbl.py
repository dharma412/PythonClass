#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/options/slbl.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $


from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

ENTRY_LINK = lambda row: '//tbody[@class="yui-dt-data"]/tr[%s]/td[1]' % (row,)
ENTRY_LINK2 = lambda row: 'xpath=//tbody[@class="yui-dt-data"]/tr[%s]/td[1]' % (row,)
DELETE_LINK = lambda row: 'xpath=//tbody[@class="yui-dt-data"]/tr[%s]/td[2]/div/img' % (row,)

TABLE_HEADER = lambda table_name: 'xpath=//table/tbody/tr/td[1]/dl/dt[contains(text(),"%s")]' % (table_name,)
BUTTON_ADD_TO_LIST = 'name=add_to_list'
INPUTH_LINE_FOR_ENTRY = 'id=list_entry'

error_message_slbl_isnt_available =  'SLBL is not enabled'

class SLBLBasePage(GuiCommon):

    def _navigate(self, list_name):
        self._info('Navigating to "Options" -> "%s"' % (list_name,))
        self._info('Navigating to "Options" -> "%s"' % (self.dut,))
        if list_name.lower() == 'safelist':
            control_text = 'SafeList'
        else:
            control_text = list_name

        if not self._is_element_present(TABLE_HEADER(control_text)):
            try:
                self._navigate_to('Options', list_name)
            except:
                raise guiexceptions.GuiApplicationError(
                          error_message_slbl_isnt_available)

    def _get_item_list(self, list_name):
        self._info('Get entries from %s' % (list_name,))
        self._navigate(list_name)
        entries = []
        start_row = 1
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_LINK('*')))

        for row in xrange(start_row, num_of_entries + 1):
            text = self.get_text(ENTRY_LINK2(row))
            entries.append(text)

        return entries

    def _add_entries(self, list_name, new_entries):
        self._info('Add entries to %s' % (list_name,))
        self._navigate(list_name)
        new_entries = self._convert_to_tuple(new_entries)

        for entry in new_entries:
            self.input_text(INPUTH_LINE_FOR_ENTRY, entry)
            self.click_button(BUTTON_ADD_TO_LIST, "don't wait")
            self._check_action_result()

    def _delete_entries(self, list_name, deleting_entries):
        self._info('Delete entries from %s' % (list_name,))
        self._navigate(list_name)
        deleting_entries = self._convert_to_tuple(deleting_entries)

        for entry in deleting_entries:
            available_entries = self._get_item_list(list_name)
            if entry in available_entries:
                self.click_element(DELETE_LINK(available_entries.index(entry) + 1))
            else:
                raise ValueError('(%s) entry does not exists' % (entry,))

class Safelist(SLBLBasePage):
    """Keyword library for menu Options -> Safelist"""

    def get_keyword_names(self):
        return ['safelist_get',
                'safelist_delete',
                'safelist_add',
               ]

    def safelist_get(self):
        """Get entries of the safe list

        *Parameters:*
        None

        *Return:*
         - list of safe list entries.

        *Exceptions:*
         - `ValueError`: in case of safelist functionality is disabled

        *Examples:*
        | @{safelist_entries} | SAFELIST GET |
        """
        return self._get_item_list('Safelist')

    def safelist_delete(self, safelist_entries=None):
        """Delete entries from the safe list

        *Parameters:*
         - `safelist_entries`: string of comma separated safelist entries

        *Return:*
         - None

        *Exceptions:*
         - `ValueError`: in case of
        | safelist entries do not  exist |
        | safelist functionality is disabled |

        *Examples:*
        | SAFELIST DELETE | domain.org, user@domain.com, fun.domain.com |
        | SAFELIST DELETE | domain.net |
        """
        self._delete_entries('Safelist', safelist_entries)

    def safelist_add(self, safelist_entries=None):
        """Add entries to the safe list

        *Parameters:*
         - `safelist_entries`: string of comma separated safelist entries

        *Return:*
         - None

        *Exceptions:*
         - `ValueError`: in case of
        | safelist entries exist |
        | list maximum is reached |
        | not allowed format of entry |
        | safelist functionality is disabled |

        Examples
        | SAFELIST ADD | domain.org, user@domain.com, fun.domain.com |
        | SAFELIST ADD | domain.net |
        """
        self._add_entries('Safelist', safelist_entries)

class Blocklist(SLBLBasePage):
    """Keyword library for menu Options -> Blocklist"""

    def get_keyword_names(self):
        return ['blocklist_get',
                'blocklist_delete',
                'blocklist_add',
               ]

    def blocklist_get(self):
        """Get entries of the block list

        *Parameters:*
         - None

        *Return:*
         - list of block list entries.

        *Exceptions:*
         - `ValueError`: in case of blocklist functionality is disabled.

        *Examples*
        | @{blocklist_entries} | BLOCKLIST GET |
        """
        return self._get_item_list('Blocklist')

    def blocklist_delete(self, blocklist_entries=None):
        """Delete entries from the block list

        *Parameters:*
         - `blocklist_entries`: string of comma separated blocklist entries

        *Return:*
         - None

        *Exceptions:*
         - `ValueError`: in case of
         | blocklist entries do not exist |
         | blocklist functionality is disabled |

        *Examples*
        | BLOCKLIST DELETE | domain.org, user@domain.com, fun.domain.com |
        | BLOCKLIST DELETE | domain.net |
        """
        self._delete_entries('Blocklist', blocklist_entries)

    def blocklist_add(self, blocklist_entries=None):
        """Add entries to the block list

        *Parameters:*
         - `blocklist_entries`: string of comma separated blocklist entries

        *Return:*
         - None

        *Exceptions:*
         - `ValueError`: in case of
        | blocklist entries exist |
        | list maximum is reached |
        | not allowed format of entry |
        | blocklist functionality is disabled |

        Examples
        | BLOCKLIST ADD | domain.org, user@domain.com, fun.domain.com |
        | BLOCKLIST ADD | domain.net |
        """
        self._add_entries('Blocklist', blocklist_entries)