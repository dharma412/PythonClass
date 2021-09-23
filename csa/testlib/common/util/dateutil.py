# $Id: //prod/main/sarf_centos/testlib/common/util/dateutil.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import time
from datetime import datetime, timedelta
from common.util.utilcommon import UtilCommon


class DateUtil(UtilCommon):
    """
    Keywords for date processing
    """

    def get_keyword_names(self):
        return [
            'get_datetime_delta',
            'get_current_time',
            'add_time_to_current_time',
        ]

    def get_datetime_delta(self, date1, format1, date2, format2):
        """
        Description:
                Returns number of seconds between dates date1 and date2. If date1 is before date1 negative value will be returned.
        Arguments:
                date1 - (mandatory) string value of datetime. F. e. Thu Feb 7 15:49:43 UTC 2013
                date2 - (mandatory) string value of datetime
                format1 - (mandatory) format of the first date. F. e. %a %b %d %H:%M:%S %Z %Y
                format2 - (mandatory) format of the second date
        Returns:
                Returns number of seconds between dates date1 and date2.
        """
        try:

            t_tuple1 = time.strptime(date1.strip(), format1)
            t1 = datetime.datetime(*t_tuple1[:6])
            t_tuple2 = time.strptime(date2.strip(), format2)
            t2 = datetime.datetime(*t_tuple2[:6])
            delta = t1 - t2
        except ValueError, v:
            print 'Value error occured. Please check the data and format parameters:'
            print 'date1 = %s format1 = %s' % (str(date1), format1)
            print 'date2 = %s format2 = %s' % (str(date2), format2)
            raise
        return delta.days * 86400 + delta.seconds

    def get_current_time(self):
        """
            Returns current time

                  *Parameters*   - None

                  *Return*:  Returns current time
                  Usage:
                  ${current_time}=  Get current time"""
        return datetime.now()

    def add_time_to_current_time(self,hours=None,minutes=None,seconds=None):
        """
           Returns time with time delta added
           *Parameters*:  - Time to be added
                        -Hours -(optional) - Value in integer to be added to Hours
                        -Minutes -(optional) - Value in integer to be added to Minutes
                        -Seconds -(optional) - Value in integer to be added to Seconds
                        If no value given as arguments, zero will be added to the hours,minutes and seconds.
            *Return*:   Returns time plus value to be added to hours,minutes and seconds
            Usage-
            ${formatted_time}=  Add time to current time  hours=1  minutes=30  seconds=60
            """

        if hours is None:
            hours= 0
        if minutes is None:
            minutes=0
        if seconds is None:
            seconds=0

        formatted_time=datetime.now()+timedelta(hours=int(hours),minutes=int(minutes),seconds=int(seconds))
        return formatted_time

