# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.gui.reports_base import ReportsBase


class Report(ReportsBase):
    """Keywords for Web Security Manager -> L4 Traffic Monitor
    """

    def get_keyword_names(self):
        return [
            "report_check_table_content",
            "report_add_to_my_reports",
        ]

    def report_check_table_content(self,
                                   super_tab=None,
                                   report=None,
                                   time_range=None,
                                   tab=None,
                                   table=None,
                                   filter=None,
                                   checks=None,
                                   ):
        """
        Checks whether specified values are present in reports

        Parameters:
        - `super_tab`: super_tab of Reporting:
         'Email' or 'Web' for SMA
          None for WSA
        - `report`: full or partial name of Report
        - `time_range`: if specified, change time range;
          examples: day, week, month
          See more details about setting time range in reports_base
        - `tab`: full or partial name of TAB within report;
          None if TAB should not be selected
        - `table`: full or partial name of a table to search
        - `filter`: if filter is specified, enter it to a text field
         and click corresponding filtering button like
         'Find User ID or Client IP' before performing checks
        - `checks`: one or several checks in the table separated by #

        Examples:
        Report Check Table Content
        ...    report=Users
        ...    table=Users
        ...    filter=10.4.1.100
        ...    checks=10.4.1.100

        Report Check Table Content
        ...    report=Reports by User Location
        ...    tab=Users
        ...    table=Remote Users
        ...    checks=10.4.6.132#yahoo

        Report Check Table Content
        ...    report=Reports by User Location
        ...    tab=Domains
        ...    table=Domains Matched by Remote Users
        ...    checks=yahoo.com
        ...    time_range=week

        Exceptions:
        - RuntimeError: Report "{report}" does not have TAB "{tab}"
        - RuntimeError: Could not find Filter Field
        - RuntimeError: Could not find Find... button
        - RuntimeError: "{check}" in table "{table}" was not detected
        """
        TAB = "xpath=//div [@class='subtitle']/" + \
              "a[contains(text(), '{tab}')]".format(tab=tab)
        CONTAINER = '*[contains(@class, "widget-content")]'
        TABLE = "xpath=//" + CONTAINER + "//*[contains(text(), '{table}')]" \
            .format(table=table) + "/ancestor::" + CONTAINER
        VERIFICATION = lambda check: TABLE + "//dl[@class='header']" \
                                     + "//* [contains(text(), '{check}')]" \
                                         .format(check=check)
        FILTER_FIELD = TABLE + 'xpath=//input[contains(@id,"search_field")]'
        SEARCH_BUTTON = TABLE + "//input[contains(@id,'-search-button')]"

        if super_tab:
            self._navigate_to(super_tab, "Reporting", report)
        else:
            self._navigate_to("Reporting", report)
        if tab:
            try:  # select TAB
                self.click_button(TAB, "don't wait")
            except:
                raise RuntimeError(
                    'Report "{report}" does not have TAB "{tab}".\n'.format \
                        (report=report, tab=tab) + TAB)
        if time_range:
            self._select_time_range(time_range)
        if filter:
            try:
                self._wait_until_element_is_present(FILTER_FIELD)
                if not self._is_visible(FILTER_FIELD):
                    raise RuntimeError('FilterField')
                self.input_text(FILTER_FIELD, filter)
                try:
                    if not self._is_visible(SEARCH_BUTTON):
                        raise RuntimeError('SEARCH_BUTTON')
                    self.click_button(SEARCH_BUTTON, "don't wait")
                except:
                    raise RuntimeError('Could not find Find... button ' +
                                       SEARCH_BUTTON)
            except:
                raise RuntimeError('Could not find Filter Field ' +
                                   FILTER_FIELD)
        if checks:
            try:
                for check in checks.split('#'):
                    self._wait_until_element_is_present(VERIFICATION(check))
                    self._info('"{check}" in table "{table}" was detected'.format \
                                   (check=check, table=table))
            except:
                raise RuntimeError(
                    '"{check}" in table "{table}" was not detected.\n'.format \
                        (check=check, table=table) + VERIFICATION(check))

    def report_add_to_my_reports(self,
                                 super_tab=None,
                                 report=None,
                                 tab=None,
                                 table=None,
                                 name=None,
                                 action='OK',
                                 ):
        """
        Checks whether specified values are present in reports

        Parameters:
        - `super_tab`: super_tab of Reporting:
         'Email' or 'Web' for SMA
          None for WSA
        - `report`: full or partial name of Report
        - `tab`: full or partial name of TAB within report;
          None if TAB should not be selected
        - `table`: full or partial name of a table to search
        - `name`: non-default name to be assigned to report
        - `action`: "OK" to add and close this window;
          "Go to My Reports" to add and view My Reports page

        Examples:
        Report Add To My Reports
        ...    report=Reports by User Location
        ...    tab=Users
        ...    table=Remote Users
        ...    name=Custom name for Users report
        ...    action=Go to My Reports

        Report Add To My Reports
        ...    report=Reports by User Location
        ...    tab=Domains
        ...    table=Domains Matched by Remote Users

        Exceptions:
        - RuntimeError: Report "{report}" does not have TAB "{tab}"
        """
        TAB = "xpath=//div [@class='subtitle']/" + \
              "a[contains(text(), '{tab}')]".format(tab=tab)
        CONTAINER = "dl[@class='header']"
        TABLE = "xpath=//" + CONTAINER + "//*[contains(text(), '{table}')]" \
            .format(table=table) + "/ancestor::" + CONTAINER
        ADD_BUTTON = TABLE + "//div [@class='add-button']"
        NAME_FIELD = 'xpath=//input[@name="display_name"]'
        ACTION_BUTTON = 'xpath=//button[contains(text(), "{action}")]'.format \
            (action=action)

        if super_tab:
            self._navigate_to(super_tab, "Reporting", report)
        else:
            self._navigate_to("Reporting", report)
        if tab:
            try:  # select TAB
                self.click_button(TAB, "don't wait")
            except:
                raise RuntimeError(
                    'Report "{report}" does not have TAB "{tab}".\n'.format \
                        (report=report, tab=tab) + TAB)
        self.click_button(ADD_BUTTON, "don't wait")
        self._input_text_if_not_none(NAME_FIELD, name)
        self.click_button(ACTION_BUTTON, "don't wait")
