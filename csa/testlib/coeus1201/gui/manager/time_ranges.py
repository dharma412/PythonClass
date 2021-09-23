#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/time_ranges.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

TABLE_ID = 'xpath=//table[@class="cols"]'
TABLE_CELL_ID = lambda row, col: TABLE_ID + '//tr[%s]//td[%s]' % (row, col)
TABLE = "xpath=//*[@id='form']/dl[2]/dd/table/tbody"
TABLE_CELL = lambda row, col: TABLE + '//tr[%s]//td[%s]' % (row, col)

class TimeRanges(GuiCommon):
    """Adds time range."""

    name_column = 1
    del_column = 4
    delete_quota_column = 5

    def get_keyword_names(self):
        return ['time_ranges_add',
                'time_ranges_edit',
                'time_ranges_delete',
                'time_ranges_get_list',
                'quotas_add',
                'quotas_edit',
                'quotas_delete',
                'quotas_get_list',
		]

    def time_ranges_get_list(self):
        """
        Returns: dictionary of time ranges. Keys are names of time ranges.
        Each time range is a dictionary with following keys:
        - `time_zone`
        - `time_settings`

        Examples:

        | ${policies}= | Time Ranges Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['CustomPolicy']['time_zone'] == 'Etc/GMT' |
        """
        self._open_define_timerange_and_quota_page()
        return self._get_policies()

    def time_ranges_add(self,
                        name,
                        week_days,
                        region=None,
                        country=None,
                        time_zone=None,
                        time_of_day='all day'):
        """Adds new custom time range.

        `name`: name of time range.

        'week_days: a comma separated values of days of the week.

        `region`: name of region.

        `country`: name of country that belongs the region.

        `time_zone`: time zone within the country.

        `time_of_day`: a comma separated values of two numbers in 24 hour
                       format.

        Exceptions:
        - ValueError:Incorrect time range. Must be start time and end time
        - ConfigError:Time range with the name xxx already exists.

        Examples:
        | Time Ranges Add | myTime | Monday,Thursday |
        | Time Ranges Add | myTime | Monday,Thursday | time_of_day=09:00,18:00 |
        | Time Ranges Add | myTime | Monday,Thursday | region=Europe | country=Latvia | time_zone=Riga | time_of_day=09:00,18:00 |
        """

        self._open_define_timerange_and_quota_page()
        if self._is_element_present('xpath=//table[@class="cols"]'
                         '/tbody/tr/td/a[substring-after(@href, "%s") = "%s"]' % \
                         (name, name)):
            raise guiexceptions.ConfigError('Time range with the '
                                            'name %s already exists.' % name)
        self._click_add_timerange_button()
        self._fill_name(name)

        time_zone_dict = {'region':region, 'country':country,
                          'timezone':time_zone}
        if any(time_zone_dict.values()):
            self._select_timezone(time_zone_dict)

        times = self._convert_to_tuple(time_of_day)
        weekdays = self._convert_to_tuple(week_days)
        if len(times) == 2:
            timedefs = {'time':{'from':times[0], 'to':times[1]},
                        'days':weekdays}
        elif times[0] == 'all day':
            timedefs = {'days':weekdays}
        else:
            raise ValueError('Incorrect time range. Must be start time and '
                             'end time')

        row = 0
        self._fill_timedef(row, timedefs)
        self._click_submit_button()

    def time_ranges_edit(self,
                         name,
                         week_days,
                         row=0,
                         region=None,
                         country=None,
                         time_zone=None,
                         time_of_day='all day'):
        """Edits the custom time range.

        `name`: name of the edited time range.

        'week_days: a comma separated values of days of the week.

        `row`: number of time value row to be edited. The default value is 0.
               If row doesn't exist with given number it is created.

        `region`: name of region.

        `country`: name of country that belongs the region.

        `time_zone`: time zone within the country.

        `time_of_day`: a comma separated values of two numbers in 24 hour
                       format.

        Exceptions:
        - ValueError:Incorrect time range. Must be start time and end time

        Examples:
        | Time Ranges Edit | myTime | Monday,Sunday | region=Pacific | country=Fiji | time_zone= Fiji | time_of_day=09:00,19:00 |
        | Time Ranges Edit | myTime | Monday,Wednesday | row=1 | region=Pacific | country=Fiji | time_zone= Fiji | time_of_day=09:00,19:00 |
        """

        self._open_define_timerange_and_quota_page()
        self._click_edit_link(name, self.name_column)

        time_zone_dict = {'region':region, 'country':country,
                          'timezone':time_zone}
        if any(time_zone_dict.values()):
            self._select_timezone(time_zone_dict)

        times = self._convert_to_tuple(time_of_day)
        weekdays = self._convert_to_tuple(week_days)
        if len(times) == 2:
            timedefs = {'time':{'from':times[0], 'to':times[1]},
                        'days':weekdays}
        elif times[0] == 'all day':
            timedefs = {'days':weekdays}
        else:
            raise ValueError('Incorrect time range. Must be start time and '
                             'end time')

        self._edit_timedefs(row, timedefs)
        self._click_submit_button()

    def time_ranges_delete(self, name):
        """Deletes the custom time range.

        `name`: name of time range to be deleted.

        Exceptions:
        - GuiControlNotFoundError:"xxx" Time Range is not present

        Example:
        | Time Ranges Delete | myTimeRange |
        """
        self._open_define_timerange_and_quota_page()
        self._click_delete_link(name, self.del_column)

    def quotas_get_list(self):
        """
        Returns: dictionary of quotas. Keys are names of quotas.
        Each quotas is a dictionary with following keys:
        - `reset_time/time_range`
        - `time_quota`
        - `volume_quota`
        Examples:
        | ${policies}= | quotas Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['CustomPolicy']['time_zone'] == 'Etc/GMT' |
        """
        self._open_define_timerange_and_quota_page()
        return self._get_quota_policies_list()

    def quotas_add(self,
                 name,
                 time_quota=None,
                 volume_quota=None,
                 region=None,
                 country=None,
                 time_zone=None,
                 reset_time='12:00 AM',
                 time_range=None):
        """Adds new custom quotas.

        `name`: name of quotas.

        'time_quota': quota of time have hrs and mins

        'volume_quota': quota of volume.

        `region`: name of region.

        `country`: name of country that belongs the region.

        `time_zone`: time zone within the country.

        'reset_time' : to reset the quota daily/time range defined.

        'time_range' : name of time range which is already defimed.


        Exceptions:
        - ValueError:Incorrect reset time. Must be hours and meridian.
        - ConfigError:quotas with the name xxx already exists.

        Examples:
        | quotas Add | myquotas |
        | quotas Add | myquotas | time_quota=02:30 | volume_quota=500 GB |
	... | reset_time=04:00 PM |
        | quotas Add | myquotas | region=Europe | country=Latvia |
	... | time_zone=Riga | time_quota=02:00 | volume_quota=200 MB |
        """

        self._open_define_timerange_and_quota_page()
        if self._is_element_present('xpath=//table[@class="cols"]'
                         '/tbody/tr/td/a[substring-after(@href, "%s") = "%s"]' % \
                         (name, name)):
            raise guiexceptions.ConfigError('Quota with the '
                                            'name %s already exists.' % name)
        self._click_add_quota_button()
        self._fill_quota_name(name)

        if reset_time:
            r_time=reset_time.split(" ")

        if len(r_time) == 2:
            reset_time_dict = {'hrs':r_time[0], 'AM':r_time[1]}
        elif len(r_time) == 1:
            reset_time_dict = {'hrs':r_time[0], 'AM':'AM'}
        else:
            raise ValueError('Incorrect reset time. Must be hours and '
                             'meridian')

        if time_range is not None:
            self._fill_time_range(time_range)
        elif any(reset_time_dict.values()):
            self._fill_reset_time(reset_time_dict)

        time_zone_dict = {'region':region, 'country':country,
                          'timezone':time_zone}
        if any(time_zone_dict.values()):
            self._unselect_checkbox('tz_appliance')
            self._select_quota_timezone(time_zone_dict)

        if time_quota is not None:
	    self._fill_time_quota(time_quota)
	if volume_quota is not None:
	    self._fill_volume_quota(volume_quota)
        self._click_submit_button()

    def quotas_edit(self,
                    name,
                    time_quota=None,
                    volume_quota=None,
                    row=0,
                    region=None,
                    country=None,
                    time_zone=None,
                    reset_time='12:00 AM',
                    time_range=None):
        """Edits the custom quotas.

        `name`: name of quotas.

        'time_quota': quota of time have hrs and mins

        'volume_quota': quota of volume.

        `region`: name of region.

        `country`: name of country that belongs the region.

        `time_zone`: time zone within the country.

        'reset_time' : to reset the quota daily/time range defined.

        'time_range' : name of time range which is already defimed.

        Exceptions:
        - ValueError:Incorrect reset time. Must be hours and meridian.

        Examples:
        | quotass Edit | myquotas | time_quota=06:40 | volume_quota=100 GB |
	... | reset_time=06:00 PM |
        | quotass Edit | myquotas | region=Europe | country=Latvia |
	... | time_zone=Riga | time_quota=02:00 |
        """

        self._open_define_timerange_and_quota_page()
        self._click_edit_quota_link(name, self.name_column)

        if reset_time:
            r_time=reset_time.split(" ")

        if len(r_time) == 2:
            reset_time_dict = {'hrs':r_time[0], 'AM':r_time[1]}
        elif len(r_time) == 1:
            reset_time_dict = {'hrs':r_time[0], 'AM':'AM'}
        else:
            raise ValueError('Incorrect reset time. Must be hours and '
                             'meridian')

        if time_range is not None:
            self._fill_time_range(time_range)
        elif any(reset_time_dict.values()):
            self._fill_reset_time(reset_time_dict)

        time_zone_dict = {'region':region, 'country':country,
                          'timezone':time_zone}
        if any(time_zone_dict.values()):
            self._unselect_checkbox('tz_appliance')
            self._select_quota_timezone(time_zone_dict)

        self._fill_time_quota(time_quota)
        self._fill_volume_quota(volume_quota)
        self._click_submit_button()

    def quotas_delete(self, name):
        """Deletes the custom quotas.

	`name`: name of quotas to be deleted.

        Exceptions:
        - GuiControlNotFoundError:"xxx" quotas is not present

        Example:
        | quotas Delete | myquotas |
        """
        self._open_define_timerange_and_quota_page()
        self._click_delete_quota_link(name, self.delete_quota_column)

    def _edit_timedefs(self, row, timedefs):
        self._fill_timedef(row, timedefs)

    def _fill_timedef(self, row, timedef):

        if not self._is_element_present('id=timedef_row%s' % row):
            count = self.get_matching_xpath_count(
            '//tbody[@id="timedef_rowContainer"]/tr[contains(@id, "timedef_row")]')
            if abs(int(row) - int(count)) > 1:
                raise guiexceptions.ConfigError("Wrong number of row.")
            self.click_button('timedef_domtable_AddRow', "don't wait")

        self._fill_dow(row, timedef['days'])

        if timedef.get('time'):
            self._fill_tod(row, timedef['time'])

    def _fill_dow(self, row, dow):
        """Selects days of the week."""

        dow_map = {
            'Monday':'M',
            'Tuesday':'T',
            'Wednesday':'W',
            'Thursday':'H',
            'Friday':'F',
            'Saturday':'A',
            'Sunday':'S',
            }
        dow = map(lambda x: x.capitalize(), dow)
        for day, abbr in dow_map.items():
            if day in dow:
                self.select_checkbox('id=timedef[%s][%s]' % (row, abbr))
            else:
                self.unselect_checkbox('id=timedef[%s][%s]' % (row, abbr))

    def _fill_tod(self, row, tod):
        """Sets time of day."""

        self.click_button('f_timedef[%s][ID]' % row, "don't wait")
        time_from = tod.get('from', '')
        time_to = tod.get('to', '')
        self.input_text('from[%s][FROM]' % row, time_from)
        self.input_text('to[%s][TO]' % row, time_to)

    def _click_add_timerange_button(self):
        """Click 'Add Time Range...' button."""

        button = 'xpath=//input[@value="Add Time Range..."]'
        self.click_button(button)

    def _click_add_quota_button(self):
        """Click 'Add quotas...' button."""

        button = 'xpath=//input[@value="Add Quota..."]'
        self.click_button(button)

    def _get_table_row_index(self, name):
        table_rows = self.get_matching_xpath_count('%s//tr' % \
                                                    (TABLE_ID.strip('xpath='),))

        for i in xrange(2, int(table_rows) + 1):
            time_range_name = self._get_text(TABLE_CELL_ID(i,
                                                  self.name_column))\
                                                  .split(' \n')[0]
            if time_range_name == name:
                return i
        return None

    def _get_quota_table_row_index(self, name):
        table_rows = self.get_matching_xpath_count('%s//tr' % \
                                                    (TABLE.strip('xpath='),))

        for i in xrange(2, int(table_rows) + 1):
            quota_name = self._get_text(TABLE_CELL(i,
                                                  self.name_column))\
                                                  .split(' \n')[0]
            if quota_name == name:
                return i
        return None

    def _click_edit_link(self, name, column):
        row = self._get_table_row_index(name)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(
                    '"%s" Time Range is not present' % (name,))

        self.click_element('%s/a' % TABLE_CELL_ID(row, column))

    def _click_edit_quota_link(self, name, column):
        row = self._get_quota_table_row_index(name)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(
                    '"%s" quotas is not present' % (name,))

        self.click_element('%s/a' % TABLE_CELL(row, column))

    def _click_delete_link(self, name, delete_column):

        row = self._get_table_row_index(name)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(
                    '"%s" Time Range is not present' % (name,))

        self.click_element('%s//img' % TABLE_CELL_ID(row, delete_column),
                        "don't wait")
        self.click_button("xpath=//button[text()='Delete']")

    def _click_delete_quota_link(self, name, delete_column):

        row = self._get_quota_table_row_index(name)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(
                    '"%s" quotas is not present' % (name,))

        self.click_element('%s//img' % TABLE_CELL(row, delete_column),
                        "don't wait")
        self.click_button("xpath=//button[text()='Delete']")

    def _fill_name(self, name):
        self.input_text('id=timerange_name', name)

    def _fill_quota_name(self, name):
        self.input_text('id=quota_name', name)

    def _select_timezone(self, time_zone_dict):
        """Specify Time Zone."""

        if not all(time_zone_dict.values()):
            raise ValueError('"Time Settings" should consist of three '
                             'options: Region, Country, Time Zone')

        self.click_button('xpath=id("tz_specified")', "don't wait")
        self.select_from_list('id=continent', time_zone_dict['region'])
        self.select_from_list('id=country', time_zone_dict['country'])
        self.select_from_list('id=time_zone', time_zone_dict['timezone'])

    def _select_quota_timezone(self, time_zone_dict):
        """Specify Time Zone."""

        if not all(time_zone_dict.values()):
            raise ValueError('"Time Settings" should consist of three '
                             'options: Region, Country, Time Zone')

        self._unselect_checkbox('tz_appliance')
        self.select_from_list('id=continent', time_zone_dict['region'])
        self.select_from_list('id=country', time_zone_dict['country'])
        self.select_from_list('id=time_zone', time_zone_dict['timezone'])

    def _fill_time_range(self, time_range):
        self.click_button('xpath=id("pre_time_specified")', "don't wait")
        self.select_from_list('id=pre_time_range', time_range)

    def _fill_time_quota(self, time_quota):
        time=time_quota.split(":")

        if len(time) == 2:
            time_quota_dict = {'hrs':time[0], 'mins':time[1]}

        elif len(time) == 1:
            time_quota_dict = {'hrs':time[0], 'mins':00}
        else:
            raise ValueError('Incorrect time quota. Must be hours and '
                             'minutes')
        self._select_checkbox('qt_check')
        self.select_from_list('id=hr', time_quota_dict['hrs'])
        self.select_from_list('id=min', time_quota_dict['mins'])

    def _fill_volume_quota(self, volume_quota):
        volume=volume_quota.split(" ")

        if len(volume) == 2:
            volume_quota_dict = {'num':volume[0], 'units':volume[1]}
        elif len(volume) == 1:
            volume_quota_dict = {'num':volume[0], 'units':'kb'}
        else:
            raise ValueError('Incorrect volume quota. Must be size and '
                             'units')

        self._select_checkbox('vq_check')
        self.input_text('id=volume_quota', volume_quota_dict['num'])
        self.select_from_list('id=volume_select', volume_quota_dict['units'])

    def _fill_reset_time(self, reset_time_dict):
        self.click_button('xpath=id("rst_radio")', "don't wait")
        self.input_text('id=rst_time', reset_time_dict['hrs'])
        self.select_from_list('id=ap', reset_time_dict['AM'])

    def _get_quota_policies_list(self):
        """
        Returns list of policies as a dictionary
        """
        result = {}
        TABLE = "//*[@id='form']/dl[2]/dd/table/tbody"
        rows = int(self.get_matching_xpath_count(TABLE + "/tr"))
        columns = int(self.get_matching_xpath_count(TABLE + "/tr[2]/td"))
        for row in range(2, rows + 1):
            a_policy = {}
            a_policy['state'] = 'enabled'
            policy = TABLE + "/tr[%s]" % row
            lines = str(self._get_text(policy + '/td[2]')).splitlines()
            # Order
            if self._get_text(TABLE + "/tr[1]/th[1]") == 'Order':
                a_policy["order"] = \
                    self._get_text(policy + "/td[1]")
                order = 2
            else:
                order = 1

            # Policy
            policy_column = policy + "/td[%s]" % order
            if self._is_element_present(policy_column + "//strong"):
                policy_name = self._get_text(policy_column + "//strong")
            elif self._is_element_present(policy_column + "//a"):
                policy_name = self._get_text(policy_column + "//a")
            else:
                policy_name = self._get_text(policy_column)
            items =int(self.get_matching_xpath_count(policy_column + \
                "/table/tbody/tr"))
            if items == 0:
                for line in lines[1:]:
                    ind = line.find(':')
                    if ind > -1:
                        a_policy[line[:ind].strip().lower().replace(' ','_')] =\
                            line[(ind+1):].strip()
                    else:
                        if line.find('(disabled)') > -1:
                            a_policy['state'] = 'disabled'

            for item in range (1, items+1):
                property = policy_column + "/table/tbody/tr[%s]" % item
                if self._is_element_present(property + "/td[2]"):
                    a_policy[self._get_text(property + "/td[1]")[:-1]. \
                             lower().\
                             replace(' ', '_')] = \
                             self._get_text(property + "/td[2]")

            for column in range((order+1), columns):
                a_policy[self._get_text(TABLE + "/tr[1]/th[%s]" % column).\
                         lower().\
                         replace(' ', '_').\
                         replace('\n', '_').\
                         replace('__','_')] = \
                    self._get_text(policy + "/td[%s]" % column)
            result[policy_name] = a_policy
        return result

    def _open_define_timerange_and_quota_page(self):
        """Open 'Defined Time Ranges and Quotas' page."""

        self._navigate_to('Web Security Manager', 'Define Time Ranges and Quotas')
