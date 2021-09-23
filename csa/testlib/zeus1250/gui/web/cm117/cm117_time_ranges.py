# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm117/cm117_time_ranges.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm117/cm117_time_ranges.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from coeus1170.gui.manager.time_ranges import TimeRanges

class Cm110TimeRanges(TimeRanges):

    """
    Keywords for Web -> Configuration Master 11.7 -> Defined Time Ranges
    """

    def _open_define_timerange_and_quota_page(self):
        self._navigate_to('Web', 'Configuration Master 11.7', 'Defined Time Ranges')

    def get_keyword_names(self):
        return [
             'cm117_time_ranges_add',
             'cm117_time_ranges_edit',
             'cm117_time_ranges_delete',
             'cm117_time_ranges_get_list',
             ]

    def cm117_time_ranges_get_list(self):
        """
        Returns: dictionary of time ranges. Keys are names of time ranges.
        Each time range is a dictionary with following keys:
        - `time_zone`
        - `time_settings`

        Examples:

        | ${policies}= | CM117 Time Ranges Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | ${policies}['CustomPolicy']['time_zone'] == 'Etc/GMT' |
        """
        self._open_define_timerange_and_quota_page()
        return self._get_policies()

    def cm117_time_ranges_add(self,
             name,
             week_days,
             region=None,
             country=None,
             time_zone=None,
             time_of_day='all day'):
        """Adds new custom time range from Configuration Master 11.7

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
        | CM117 Time Ranges Add | myTime | Monday,Thursday |
        | CM117 Time Ranges Add | myTime | Monday,Thursday | time_of_day=09:00,111.00 |
        | CM117 Time Ranges Add | myTime | Monday,Thursday | region=Europe |
        | ... | country=Latvia | time_zone=Riga | time_of_day=09:00,111.00 |
        """
        self._open_define_timerange_and_quota_page()
        self.time_ranges_add(
             name,
             week_days,
             region=region,
             country=country,
             time_zone=time_zone,
             time_of_day=time_of_day)

    def cm117_time_ranges_edit(self,
             name,
             week_days,
             row=0,
             region=None,
             country=None,
             time_zone=None,
             time_of_day='all day'):
        """Edits the custom time range from Configuration Master 11.7

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
        | CM117 Time Ranges Edit | myTime | Monday,Sunday | region=Pacific |
        | ... | country=Fiji | time_zone= Fiji | time_of_day=09:00,19:00 |
        | CM117 Time Ranges Edit | myTime | Monday,Wednesday | row=1 |
        | ... | region=Pacific | country=Fiji | time_zone= Fiji |
        | ... | time_of_day=09:00,19:00 |
        """
        self._open_define_timerange_and_quota_page()
        self.time_ranges_edit(
             name,
             week_days,
             row=row,
             region=region,
             country=country,
             time_zone=time_zone,
             time_of_day=time_of_day)

    def cm117_time_ranges_delete(self, name):
        """Deletes the custom time range from Configuration Master 11.7

        *Parameters*
        - `name`: name of time range to be deleted.

        *Exceptions*
        - GuiControlNotFoundError:"xxx" Time Range is not present

        *Example*
        | CM117 Time Ranges Delete | myTimeRange |
        """
        self._open_define_timerange_and_quota_page()
        self.time_ranges_delete(name)
