#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/email/reporting/outbreak_table.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

import details_table
import report_table

# Outbreak table attributes dictionary.
# Item format is:
# '<table_name_in_gui>': ((<tuple_with_tab_names_to_be_passed_to_navigate_to_method>),
# (<tuple_with_table_coordinates_in_gui_taken_from_"id=ss_0_%d_%d"_parameter>))
TABLE_NAMES = {'Past Year Virus Outbreaks': (('Email', 'Reporting', 'Outbreak Filters'),
                                             (3, 0))}


COUNT_ITEMS_DISPLAY_COMBO = '//select[@id=\'rows_ss_0_3_0\' and @name=\'rows_ss_0_3_0\']'
LOCAL_GLOBAL_DISPLAY_COMBO = '//select[@id=\'filter_ss_0_3_0\' and @name=\'filter_ss_0_3_0\']'

class OutbreakTableParameters(report_table.TableParameters):
    """Represents additional parameters for Past Year Virus Outbreaks table"""

    def __init__(self,
                 wui,
                 count_items_displayed=None,
                 items_displayed=None):
        """
        Parameters:
         - count_items_displayed: count of items to display on the
        'Past Year Virus Outbreaks' table
        Possible values are: '10', '20', '50', '100', 'All'
         - items_displayed: type of items to be displayed
        ('Global Outbreaks' or 'Local Outbreaks')
        """
        super(OutbreakTableParameters, self).__init__(wui,
                                        count_items_displayed=count_items_displayed,
                                        items_displayed=items_displayed)

    def set_count_items_displayed(self, new_value):
        self._wui.select_from_list(COUNT_ITEMS_DISPLAY_COMBO,
                                   new_value)

    def set_items_displayed(self, new_value):
        self._wui.select_from_list(LOCAL_GLOBAL_DISPLAY_COMBO,
                                   new_value)


class OutbreakTable(details_table.DetailsTable):
    """This class represents the details table on Email->Outbreak Filters Page
    """

    def _get_table_parameters(self, kwargs={}):
        return OutbreakTableParameters(self._wui, **kwargs)

    def _get_table_attributes_dict(self):
        return TABLE_NAMES
