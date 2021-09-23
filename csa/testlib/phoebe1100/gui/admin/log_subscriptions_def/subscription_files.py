#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/admin/log_subscriptions_def/subscription_files.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $


FILES_TABLE = "//table[@class='cols']"
LOG_ROWS = "%s/tbody/tr" % (FILES_TABLE,)
COLUMN_DATA = lambda row_index, col_index: "%s[%d]/td[%d]" % \
                                           (LOG_ROWS, row_index, col_index)
ENTRY_MAP = {'File Name': 1,
             'Date': 2,
             'Size': 3}
DELETE_FILE_CHECKBOX = lambda name: "%s//td[normalize-space()='%s']" \
                                    "/following-sibling::td[3]/input" % \
                                    (FILES_TABLE, name)
FILES_DELETE_ALL_CHECKBOX = "//input[@id='delete']"


class SubscriptionFiles(object):
    def __init__(self, gui_common):
        self.gui = gui_common

    def get_details(self):
        details = []
        files_count = int(self.gui.get_matching_xpath_count(LOG_ROWS))
        for row_index in xrange(2, files_count + 1):
            entry_info = {}
            for entry_name, col_index in ENTRY_MAP.iteritems():
                entry_info[entry_name] = self.gui.get_text(COLUMN_DATA(row_index,
                                                                       col_index))
            details.append(entry_info)
        return details

    def delete(self, names):
        if not names:
            raise ValueError('There should be at least one log file name')

        if isinstance(names, basestring) and names.upper() == 'ALL':
            self.gui._select_checkbox(FILES_DELETE_ALL_CHECKBOX)
        else:
            if isinstance(names, basestring):
                names = (names,)
            for file_name in names:
                if self.gui._is_element_present(DELETE_FILE_CHECKBOX(file_name)):
                    self.gui._select_checkbox(DELETE_FILE_CHECKBOX(file_name))
                else:
                    raise ValueError('There is no log file named "%s" ' \
                                     ' or it is N/A for removal' % (file_name,))
