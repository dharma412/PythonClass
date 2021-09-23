# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm91/cm91_time_ranges.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# !/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm91/cm91_time_ranges.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from coeus90.gui.manager.time_ranges import TimeRanges


class Cm91TimeRanges(TimeRanges):
    """
    Keywords for Web -> Configuration Master 9.1 -> Defined Time Ranges
    """

    def _open_defined_timerange_page(self):
        self._navigate_to('Web', 'Configuration Master 9.1', 'Defined Time Ranges')

    def get_keyword_names(self):
        return [
            'cm91_time_ranges_add',
            'cm91_time_ranges_edit',
            'cm91_time_ranges_delete',
            'cm91_time_ranges_get_list',
        ]

    def cm91_time_ranges_get_list(self):
        """
        Returns: dictionary of time ranges. Keys are names of time ranges.
        Each time range is a dictionary with following keys:
        - `time_zone`
        - `time_settings`

        Examples:

        | ${policies}= | CM91 Time Ranges Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['CustomPolicy']['time_zone'] == 'Etc/GMT' |
        """
        self._open_defined_timerange_page()
        return self._get_policies()

    def cm91_time_ranges_add(self,
                             name,
                             week_days,
                             region=None,
                             country=None,
                             time_zone=None,
                             time_of_day='all day'):
        """Adds new custom time range from Configuration Master 9.1

        *Parameters*
        - `name`: name of time range.
        - `week_days`: a comma separated values of days of the week.
        - `region`: name of region.
        - `country`: name of country that belongs the region.
        - `time_zone`: time zone within the country.
        - `time_of_day`: a comma separated values of two numbers in 24 hour
             format.

        *Exceptions*
        - ValueError:Incorrect time range. Must be start time and end time
        - ConfigError:Time range with the name xxx already exists.

        *Examples*
        | CM91 Time Ranges Add | myTime | Monday,Thursday |
        | CM91 Time Ranges Add | myTime | Monday,Thursday | time_of_day=09:00,19.10 |
        | CM91 Time Ranges Add | myTime | Monday,Thursday | region=Europe |
        | ... | country=Latvia | time_zone=Riga | time_of_day=09:00,19.10 |
        """
        self.time_ranges_add(
            name,
            week_days,
            region=region,
            country=country,
            time_zone=time_zone,
            time_of_day=time_of_day)

    def cm91_time_ranges_edit(self,
                              name,
                              week_days,
                              row=0,
                              region=None,
                              country=None,
                              time_zone=None,
                              time_of_day='all day'):
        """Edits the custom time range from Configuration Master 9.1

        *Parameters*
        - `name`: name of the edited time range.
        - `week_days`: a comma separated values of days of the week.
        - `row`: number of time value row to be edited. The default value is 0.
             If row doesn't exist with given number it is created.
        - `region`: name of region.
        - `country`: name of country that belongs the region.
        - `time_zone`: time zone within the country.
        - `time_of_day`: a comma separated values of two numbers in 24 hour
             format.

        *Exceptions*
        - ValueError:Incorrect time range. Must be start time and end time

        *Examples*
        | CM91 Time Ranges Edit | myTime | Monday,Sunday | region=Pacific |
        | ... | country=Fiji | time_zone= Fiji | time_of_day=09:00,19:00 |
        | CM91 Time Ranges Edit | myTime | Monday,Wednesday | row=1 |
        | ... | region=Pacific | country=Fiji | time_zone= Fiji |
        | ... | time_of_day=09:00,19:00 |
        """
        self.time_ranges_edit(
            name,
            week_days,
            row=row,
            region=region,
            country=country,
            time_zone=time_zone,
            time_of_day=time_of_day)

    def cm91_time_ranges_delete(self, name):
        """Deletes the custom time range from Configuration Master 9.1

        *Parameters*
        - `name`: name of time range to be deleted.

        *Exceptions*
        - GuiControlNotFoundError:"xxx" Time Range is not present

        *Example*
        | CM91 Time Ranges Delete | myTimeRange |
        """
        self.time_ranges_delete(name)
