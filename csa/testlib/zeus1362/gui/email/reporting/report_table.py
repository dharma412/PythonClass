# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/email/reporting/report_table.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from inspect import ismethod
import time

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
from common.util.sarftime import CountDownTimer


# Common DOM root for email reporting tables
REPORT_TABLE = '//table[@class=\'report_subsection\']'

# Locators for CommonReportTableParameters properties
PERIOD_COMBO = '//select[@id=\'date_range\' and @name=\'date_range\']'
VIEW_DATA_FOR_COMBO = '//select[@id=\'host_id\' and @name=\'host_id\']'


class TableParameters(object):
    """Abstract holder for email reporting table parameters"""

    def __init__(self, wui, **kwargs):
        self._wui = wui
        self._properties = kwargs

    def apply(self):
        """Calls all parameters setters

        In subclasses all param setters should look like
        def set_<param_name>(self, new_value)

        Raise:
         - NotImplementedError: if there is no setter method
        for particular parameter
        """
        for property_name, property_value in self._properties.items():
            setter_name = 'set_%s' % (property_name,)
            if hasattr(self, setter_name) and \
               ismethod(getattr(self, setter_name)):
                setter_func = getattr(self, setter_name)
                if property_value is not None:
                    setter_func(property_value)
            else:
                raise NotImplementedError('TableParameters object should '\
                                          'contain setter for parameter "%s"!'\
                                          % (property_name,))


class CommonReportTableParameters(TableParameters):
    def __init__(self,
                 wui,
                 period=None,
                 view_data_for=None):
        """Common reports table parameters are:
        - `period`: time period to view data for.
        Possible values are: 'Day', 'Week', '30 days', '90 days', 'Year'
        'Yesterday (00:00 to 23:59)', 'Previous Calendar Month'
        - `view_data_for`: Slave appliance name to view data for.
        Can be 'All appliances' to show summary data for all slave appliances
        """
        super(CommonReportTableParameters, self).__init__(wui,
                                                period=period,
                                                view_data_for=view_data_for)

    def set_period(self, new_value):
        self._wui.select_from_list(PERIOD_COMBO,
                                   new_value)

    def set_view_data_for(self, new_value):
        self._wui.select_from_list(VIEW_DATA_FOR_COMBO,
                                   new_value)


class ReportTableKeywordsContainer(GuiCommon):
    """Keywords are used to do particular manipulation with data/content from Email
    reporting tables.
    """
    def get_keyword_names(self):
        return ['email_report_table_get_data',
                'email_report_table_create_parameters',
                'email_report_table_get_column_index',
                'email_report_table_drag_column',
                'email_report_table_sort_column',
                'email_report_table_show_columns',
                'email_report_get_content_link']

    def __getattr__(self, name):
        list = ['email_report_table_get_data',
                'email_report_table_create_parameters',
                'email_report_table_get_column_index',
                'email_report_table_drag_column',
                'email_report_table_sort_column',
                'email_report_table_show_columns',
                'email_report_get_content_link']
        if name in list:
            return getattr(ReportTable(self), name)
        return super(ReportTableKeywordsContainer, self).__getattr__(name)


class ReportTable(object):
    """Base abstract class designed to interact with email reporting tables on
    Email->Reporting pages.
    """

    def __init__(self, wui):
        self._wui = wui

    def _get_table_by_name(self,
                           table_name):
        """Factory method. Returns corresponding table instance by its name.
        All tables, that are inherited from this class, should be present here

        Parameters:
         - `table_name`: name of the table. Should match exactly to one of
        imported TABLE_NAMES dictionaries keys

        Raise:
         - `ValueError`: if no table is defined with given name
        """
        import details_table
        DETAILS_TABLES = details_table.TABLE_NAMES
        if table_name in DETAILS_TABLES.keys():
            return details_table.DetailsTable(self._wui)

        import summary_table
        SUMMARY_TABLES = summary_table.TABLE_NAMES
        if table_name in SUMMARY_TABLES.keys():
            return summary_table.SummaryTable(self._wui)

        import outbreak_table
        OUTBREAK_TABLES = outbreak_table.TABLE_NAMES
        if table_name in OUTBREAK_TABLES.keys():
            return outbreak_table.OutbreakTable(self._wui)

        # You should return new table object here
        raise ValueError('There is no table found with name "%s"' \
                          % (table_name))

    def email_report_table_drag_column(self,
                                       table_name,
                                       source_column_name,
                                       target_column_name,
                                       table_parameters=None,
                                       should_navigate_to_table=True):
        """Emulates reporting table columns drag and drop

        Parameters:
         - `table_name`: name of the table to which these columns belongs. Should match
         exactly to table caption in WUI, for example:
         User Mail Flow Details,
         Outgoing Destinations Detail,
         Past Year Virus Outbreaks
         - `source_column_name`: name of the source column of the table to drag from,
         for example:
         Virus Detected,
         Spam Detected
         - `target_column_name`: name of the target column of the table to drag to,
         for example:
         Virus Detected,
         Spam Detected
         - `table_parameters`: object that contains additional params
         for the table to be populated and its setters. See keyword
         'Email Report Table Create Parameters'
         for more details
         - `should_navigate_to_table`: signals whether to navigate to this table (if ${True}) or it
         is already loaded  (if ${False})

        Raise:
         - `ValueError`: if column with given name was not found in table
         - `TimeoutError`: if table with given name was not populated within default timeout

        Example:
        | Email Report Table Drag Column | Incoming Mail Details |
        | ... | Virus Detected | Spam Detected |
        """
        target_table = self._get_table_by_name(table_name)
        target_table._drag_column(table_name,
                        source_column_name,
                        target_column_name,
                        table_parameters,
                        should_navigate_to_table)

    def _drag_column(self,
                     table_name,
                     source_column_name,
                     target_column_name,
                     table_parameters=None,
                     should_navigate_to_table=True):
        """Base abstract method for table classes which supports column dragging.

        Parameters:
         - `table_name`: name of the table to which these columns belongs. Should match
         exactly to table caption in WUI.
         - `source_column_name`: name of the source column of the table to drag from
         - `target_column_name`: name of the target column of the table to drag to
         - `table_parameters`: TableParameters descendant, contains additional params
         for the table to be populated and its setters
         - `should_navigate_to_table`: signals whether to navigate to this table (if True) or it
         is already loaded  (if False)

        Raise:
         - `ValueError`: if no column with given name found
         - `TimeoutError`: if table with given name was not populated within default timeout

        Return:
         None
        """
        raise NotImplementedError('The table "%s" does not support '\
                                  'drag_column operation' % (table_name,))

    def email_report_table_sort_column(self,
                                       table_name,
                                       column_name,
                                       table_parameters=None,
                                       should_navigate_to_table=True):
        """Emulates reporting table columns sorting

        Parameters:
         - `table_name`: name of the table to which the column belongs. Should match
         exactly to table caption in WUI, for example:
         User Mail Flow Details,
         Outgoing Destinations Detail,
         Past Year Virus Outbreaks
         - `column_name`: name of the column of the table that should be sorted,
         for example:
         Virus Detected,
         Spam Detected
         - `table_parameters`: object that contains additional params
         for the table to be populated and its setters. See keyword
         'Email Report Table Create Parameters'
         for more details
         - `should_navigate_to_table:` signals whether to navigate to this table (if ${True}) or it
         is already loaded  (if ${False})

        Raise:
         - `ValueError`: if column with given name was not found in table
         - `TimeoutError`: if table with given name was not populated within default timeout

        Example:
        | Email Report Table Sort Column | Incoming Mail Details |
        | ... | Virus Detected |
        """
        target_table = self._get_table_by_name(table_name)
        target_table._sort_column(table_name,
                    column_name,
                    table_parameters,
                    should_navigate_to_table)

    def _sort_column(self,
                     table_name,
                     column_name,
                     table_parameters=None,
                     should_navigate_to_table=True):
        """Base abstract method for table classes which supports column sorting.

        Parameters:
         - `table_name`: name of the table to which these columns belongs. Should match
         exactly to table caption in WUI.
         - `column_name`: name of the column of the table that should be sorted
         - `table_parameters`: TableParameters descendant, contains additional params
         for the table to be populated and its setters
         - `should_navigate_to_table`: signals whether to navigate to this table (if True) or it
         is already loaded  (if False)

        Raise:
         - `ValueError`: if no column with given name found
         - `TimeoutError`: if table with given name was not populated within default timeout

        Return:
         None
        """
        raise NotImplementedError('The table "%s" does not support '\
                                  'sort_column operation' % (table_name,))

    def email_report_table_get_column_index(self,
                                            table_name,
                                            column_name,
                                            table_parameters=None,
                                            should_navigate_to_table=True):
        """Returns an index of particular table column

        Parameters:
         - `table_name`: name of the table to which the column belongs. Should match
         exactly to table caption in WUI, for example:
         User Mail Flow Details,
         Outgoing Destinations Detail,
         Past Year Virus Outbreaks
         - `column_name`: name of the column of the table, for example:
         Virus Detected,
         Spam Detected
         - `table_parameters`: object that contains additional params
         for the table to be populated and its setters. See keyword
         'Email Report Table Create Parameters'
         for more details
         - `should_navigate_to_table`: Whether to navigate to the table or not.
         Set it to ${False} if table is loaded already and you do not want to refresh it.

        Return:
            Index of the particular column in the table

        Raise:
         - `ValueError`: if column with given name was not found in table
         - `TimeoutError`: if table with given name was not populated within default timeout

        Example:
        | ${col_index}= | Email Report Table Get Column Index | Incoming Mail Details |
        | ... | Virus Detected | should_navigate_to_table=${False} |
        """
        target_table = self._get_table_by_name(table_name)
        return target_table._get_column_index(table_name,
                        column_name,
                        table_parameters,
                        should_navigate_to_table)

    def _get_column_index(self,
                          table_name,
                          column_name,
                          table_parameters=None,
                          should_navigate_to_table=True):
        """Base abstract method for table classes which supports getting column indexes.

        Parameters:
         - `table_name`: name of the table to which these columns belongs. Should match
         exactly to table caption in WUI.
         - `column_name`: name of the existing table column
         - `table_parameters`: TableParameters descendant, contains additional params
         for the table to be populated and its setters
         - `should_navigate_to_table`: signals whether to navigate to this table (if True) or it
         is already loaded  (if False)

        Raise:
         - `ValueError`: if no column with given name found
         - `TimeoutError`: if table with given name was not populated within default timeout

        Return:
         int: column index
        """
        raise NotImplementedError('The table "%s" does not support '\
                                  'get_column_index operation' % (table_name,))

    def email_report_table_create_parameters(self, table_name, *args):
        """Returns particular table parameters object

        Parameters:
         - `table_name`: name of the table for which parameters will be created. Should match
         exactly to table caption in WUI, for example:
         User Mail Flow Details,
         Outgoing Destinations Detail,
         Past Year Virus Outbreaks
         - `*args`: parameters, specific for the current table (see corresponding
         properties constructor for this table)

        For details/summary tables:
         - `period`: time period to view data for.
         Possible values are: 'Day', 'Week', '30 days', '90 days', 'Year'
         'Yesterday (00:00 to 23:59)', 'Previous Calendar Month'
         - `view_data_for`: Slave appliance name to view data for.
         Can be 'All appliances' to show summary data for all slave appliances

        For Past Year Virus Outbreaks table:
         - `count_items_displayed`: count of items to display on the 'Past Year Virus Outbreaks' table
         Possible values are: '10', '20', '50', '100', 'All'
         - `items_displayed`: type of items to be displayed ('Global Outbreaks' or 'Local Outbreaks')

        Raise:
         - `ValueError`: if column with given name was not found in table
         - `TimeoutError`: if table with given name was not populated within default timeout

        Examples:
        | ${details_table_params}= | Email Report Table Create Parameters | Incoming Mail Details |
        | ... | period=Day | view_data_for=All appliances |
        | ${summary_table_params}= | Email Report Table Create Parameters | Incoming Mail Summary |
        | ... | period=Week | view_data_for=All appliances |

        | ${outbreak_table_params}= | Email Report Table Create Parameters | Past Year Virus Outbreaks |
        | ... | count_items_displayed=100 | items_displayed=Local Outbreaks |
        """
        kwargs = self._wui._parse_args(args)
        target_table = self._get_table_by_name(table_name)
        return target_table._get_table_parameters(kwargs)

    def _get_table_parameters(self, kwargs={}):
        """In subclasses this method must return TableParameters descendant object
        which corresponds to the particular table class
        """
        raise NotImplementedError('This method should be overriden in subclasses')

    def email_report_table_get_data(self,
                                    table_name,
                                    table_parameters=None,
                                    should_navigate_to_table=True):
        """Extracts report table data as dictionary which keys are column names and
         which values are lists with corresponding column values

        Parameters:
         - `table_name`: name of the table whose data will be got. Should match
         exactly to table caption in WUI, for example:
         User Mail Flow Details,
         Outgoing Destinations Detail,
         Past Year Virus Outbreaks
         Incoming Mail Summary
         - `table_parameters`: object that contains additional params
         for the table to be populated and its setters. See keyword
         'Email Report Table Create Parameters'
         for more details
         - `should_navigate_to_table`: Whether to navigate to the table or not.
         Set it to ${False} if table is loaded already and you do not want to refresh it.

        Return:
            Dictionary with table data

        Raise:
         - `ValueError`: if column with given name was not found in table
         - `TimeoutError`: if table with given name was not populated within default timeout

        Example:
            | ${table_data}= | Email Report Table Get Data | Incoming Mail Details |
            | ... | should_navigate_to_table=${False} |
        """
        target_table = self._get_table_by_name(table_name)
        return target_table._get_data(table_name,
                        table_parameters,
                        should_navigate_to_table)

    def email_report_get_content_link(self,
                                      table_name,
                                      table_parameters=None,
                                      should_navigate_to_table=True):
        target_table = self._get_table_by_name(table_name)
        return target_table._get_report_get_content_link(table_name,
                        table_parameters,
                        should_navigate_to_table)

    def _get_data(self,
                  table_name,
                  table_parameters=None,
                  should_navigate_to_table=True):
        """Base abstract method for table classes which supports getting data.

        Parameters:
         - `table_name`: name of the table to which these columns belongs. Should match
         exactly to table caption in WUI.
         - `table_parameters`: TableParameters descendant, contains additional params
         for the table to be populated and its setters
         - `should_navigate_to_table`: signals whether to navigate to this table (if True) or it
         is already loaded  (if False)

        Raise:
         - `TimeoutError`: if table with given name was not populated within default timeout

        Return:
         dict: keys are column names and values are lists with corresponding column values
        """
        raise NotImplementedError('Implement the method in subclasses')

    def email_report_table_show_columns(self,
                                        table_name,
                                        columns='all',
                                        table_parameters=None,
                                        should_navigate_to_table=True):
        """Extracts report table data as dictionary which keys are column names and
         which values are lists with corresponding column values

        Parameters:
         - `table_name`: name of the table whose data will be got. Should match
         exactly to table caption in WUI, for example:
         User Mail Flow Details,
         Outgoing Destinations Detail,
         Past Year Virus Outbreaks
         - `columns`: list of table column headers that should be shown
         in table. Can be 'all' to show all available columns
         - `table_parameters`: object that contains additional params
         for the table to be populated and its setters. See keyword
         'Email Report Table Create Parameters'
         for more details
         - `should_navigate_to_table`: Whether to navigate to the table or not.
         Set it to ${False} if table is loaded already and you do not want to refresh it.

        Return:
            Dictionary with table data

        Raise:
         - `ValueError`: if column with given name was not found in table
         - `TimeoutError`: if table with given name was not populated within default timeout

        Example:
            | ${cols}= | Create List | Spam Detected | Virus Detected |
            | Email Report Table Show Columns | Incoming Mail Details |
            | columns=${cols} |

            | Email Report Table Show Columns | Incoming Mail Details |
            | columns=all | should_navigate_to_table=${False} |
        """
        target_table = self._get_table_by_name(table_name)
        return target_table._show_columns(table_name,
                        columns,
                        table_parameters,
                        should_navigate_to_table)

    def _show_columns(self,
                      table_name,
                      columns='all',
                      table_parameters=None,
                      should_navigate_to_table=True):
        """Base abstract method for table classes which supports columns selection for show.

        Parameters:
         - `table_name`: name of the table to which these columns belongs. Should match
         exactly to table caption in WUI.
         - `columns`: list of table column headers that should be shown
         in table. Can be 'all' to show all available columns
         - `table_parameters`: TableParameters descendant, contains additional params
         for the table to be populated and its setters
         - `should_navigate_to_table`: signals whether to navigate to this table (if True) or it
         is already loaded  (if False)

        Raise:
         - `TimeoutError`: if table with given name was not populated within default timeout

        Return:
         dict: keys are column names and values are lists with corresponding column values
        """
        raise NotImplementedError('Implement the method in subclasses')

    def _get_table_attributes_dict(self):
        """This method should return dictionary with current
        table names and its attributes for current class.
        Dictionary format is:
        {'<table_name_in_gui>': ((<tuple_with_tab_names_to_be_passed_to_navigate_to_method>),
        (<tuple_with_table_coordinates_in_gui_taken_from_"id=ss_0_%d_%d"_parameter>))}"""
        raise NotImplementedError('Implement the method in subclasses')

    def _is_element_really_present_on_page(self, locator, checks_count=3):
        """Checks whether element with given locator is really present on
        current page by verifying its presence checks_count times

        Parameters:
         - `locator`: element locator
         - `checks_count`: checks count. In case an element was successfully
        detected within all checks this method returns True

        Return:
         - True if element is present or False otherwise
        """
        for check_num in xrange(checks_count):
            if not self._wui._is_element_present(locator):
                return False
            time.sleep(1.0)
        return True

    def _wait_for_table_load(self, locator, max_wait_time=20):
        """waits until element with given locators appears on page
        within given timeout. Use this method to wait until table
        data appears on page.

        Parameters:
         - `locator`: locator of element to be detected
         - `max_wait_time`: max time to wait for an element in seconds.

        Raise:
         - `TimeoutError`: if element was not detected within given timeout
        """
        timer = CountDownTimer(max_wait_time).start()
        while timer.is_active():
            if locator and self._is_element_really_present_on_page(locator):
                return
            time.sleep(1.0)
        raise guiexceptions.TimeoutError('Email report table data has not been populated'\
                                         ' within %d seconds timeout' % (max_wait_time,))

    def _navigate_to_table(self,
                           table_path,
                           table_parameters=None):
        """Navigates to page where table is present and sets
        corresponding table parameters in wui if necessary.

        Parameters:
         - `table_path`: tuple of navigation menu item names. It is used in
        _navigate_to method to go to the necessary page on appliance where
        particular table is located
         - `table_parameters`: TableParameters descendant which stores
        particular table parameter values
        """
        self._wui._navigate_to(*table_path)
        if table_parameters:
            table_parameters.apply()

    def _extract_table_attributes(self, table_name):
        """Extracts table attributes by its name

        Parameters:
         - `table_name`: name of the table for which attributes will be
        extracted

        Return:
         - `tuple`: - first item is tuple and contains navigation menu items path
        where this table is located. Second item is 2-integers tuple with table
        coordinates in DOM taken from id="ss_0_<first_int>_<second_int>"
        """
        table_attributes_dict = self._get_table_attributes_dict()
        if table_name not in table_attributes_dict.keys():
            raise ValueError('Email report table with name "%s" does not exist' \
                             % (table_name,))
        return table_attributes_dict[table_name]
