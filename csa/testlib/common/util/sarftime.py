#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/common/util/sarftime.py#1 $

"""Time related functions used by SARF tests.
    MutableTime class
    CountDownTimer class
"""
#: Reference Symbols: iaftime

from __future__ import absolute_import

import time


class MutableTime(object):
    """A mutable version of Python's time.struct_time.  In addition to
    mirroring the functionality of time.struct_time, it add logical
    time functionality.

    Detail:
       # Python time tuple:
       # Index   Attribute   Values
       # 0 tm_year (for example, 1993)
       # 1 tm_mon range [1,12]
       # 2 tm_mday range [1,31]
       # 3 tm_hour range [0,23]
       # 4 tm_min range [0,59]
       # 5 tm_sec range [0,61]; see (1) in strftime() description
       # 6 tm_wday range [0,6], Monday is 0
       # 7 tm_yday range [1,366]
       # 8 tm_isdst 0, 1 or -1; see below
    """

    INDEXMAP = {"tm_year": 0, "tm_mon": 1, "tm_mday": 2, "tm_hour": 3, "tm_min": 4,
                "tm_sec": 5, "tm_wday": 6, "tm_yday": 7, "tm_isdst": 8}
    SETTIME_FORMAT = "%a %b %d %H:%M:%S %Y %Z"

    def __init__(self, init=None, fmt=None):
        if init is None:
            self._tm = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            self._tm = list(init)
            assert len(self._tm) == 9
        self._fmt = fmt or "%a %b %d %H:%M:%S %Y"

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self._tm)

    def __str__(self):
        return time.strftime(self._fmt, self._tm)

    def __iter__(self):
        return iter(self._tm)

    def __float__(self):
        return time.mktime(self._tm)

    def __int__(self):
        return int(self.__float__())

    def __coerce__(self, other):
        try:
            return time.mktime(self._tm), float(other)
        except:
            return None

    def __len__(self):
        return len(self._tm)

    def __eq__(self, other):
        return list(self) == list(other)

    def __getitem__(self, idx):
        return self._tm[idx]

    def __setitem__(self, idx, val):
        self._tm[idx] = int(val)

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            try:
                return self._tm[self.INDEXMAP[key]]
            except KeyError:
                raise AttributeError, "no attribute '%s' found." % (key,)

    def __setattr__(self, name, val):
        idx = self.INDEXMAP.get(name, None)
        if idx is None:
            object.__setattr__(self, name, val)
        else:
            self._tm[idx] = int(val)

    def __sub__(self, other):
        return time.mktime(self._tm) - time.mktime(tuple(other))

    def __add__(self, secs):
        new = self.__class__(self._tm[:], self._fmt)
        new.add_seconds(secs)
        return new

    def __mul__(self, other):
        return time.mktime(self._tm) * float(other)

    def __div__(self, other):
        return time.mktime(self._tm) / float(other)

    def __iadd__(self, secs):
        csec = time.mktime(self._tm)
        csec += secs
        self._tm = list(time.localtime(csec))
        return self

    def __isub__(self, secs):
        csec = time.mktime(self._tm)
        csec -= secs
        self._tm = list(time.localtime(csec))
        return self

    def localtime(self, secs=None):
        if secs:  # must do it this way because these functions check arg length, not value.
            self._tm = list(time.localtime(secs))
        else:
            self._tm = list(time.localtime())
        return self

    def gmtime(self, secs=None):
        if secs:
            self._tm = list(time.gmtime(secs))
        else:
            self._tm = list(time.gmtime())
        return self

    def strftime(self, fmt=None):
        return time.strftime(fmt or self._fmt, self._tm)

    def strptime(self, val, fmt=None):
        ttl = list(time.strptime(val, fmt or self._fmt))
        # If 'fmt' contains %Z, timezone may be set properly
        # and ttl[-1] is != -1. In this case don't overwrite it.
        if ttl[-1] == -1:
            ttl[-1] = time.localtime()[-1]  # preserve dstflag - bug workaround
        self._tm = ttl
        return self

    def set_format(self, fmt):
        self._fmt = str(fmt)

    def get_mutable(self, timestring):
        """ returns a MutableTime object converted from a string
            specified by SETTIME_FORMAT above """

        if timestring[-3:] in ('PDT', 'PST', 'GMT'):
            tv = MutableTime(fmt=self.SETTIME_FORMAT)
        else:
            # Non PST/PDT or GMT time zones are not understood by
            # strptime so remove them.
            timestring = timestring[0:-4]
            timefmt = self.SETTIME_FORMAT.replace(" %Z", "")
            tv = MutableTime(fmt=timefmt)
        tv.strptime(timestring)
        return tv

    def add_seconds(self, secs):
        self.__iadd__(secs)

    def add_minutes(self, mins):
        self.add_seconds(mins * 60)

    def add_hours(self, hours):
        self.add_seconds(hours * 3600)

    def add(self, minutes=0, hours=0, days=0, weeks=0):
        self.add_seconds(seconds(minutes, hours, days, weeks))

    def add_time(self, timediff):
        """add_time(timediff) Adds specificed amount of time to the current
        time held in this object. The format of difftime is a string,
        "HH:MM:SS"."""
        [h, m, s] = map(int, timediff.split(":"))
        self.add_seconds(h * 3600 + m * 60 + s)

    def update_fields(self):
        """call this function to ensure that fields such as tm_wday are updated"""
        self._tm = list(time.localtime(time.mktime(self._tm)))


def localtime_mutable(secs=None):
    """ time module equivalent that returns MutableTime object. """
    mt = MutableTime()
    mt.localtime(secs)
    return mt


def gmtime_mutable(secs=None):
    """ time module equivalent that returns MutableTime object. """
    mt = MutableTime()
    mt.gmtime(secs)
    return mt


def strptime_mutable(string, fmt=None):
    """ time module equivalent that returns MutableTime object. """
    mt = MutableTime(fmt=fmt)
    mt.strptime(string)
    return mt


def weekof(secs=None):
    """Returns a date that is the Monday of the current week."""
    if secs:  # must do it this way because these functions check arg length, not value.
        tm = time.localtime(secs)
    else:
        tm = time.localtime()
    y, m, d, H, M, S, wday, jday, dst = tm
    d -= wday
    wday = 0
    return time.struct_time((y, m, d, 0, 0, 0, wday, jday, dst))


def seconds(minutes=0, hours=0, days=0, weeks=0):
    """Returns a value in seconds given some minutes, hours, days, or weeks.

    >>> seconds(17, 0, 0, 0 )
    1020
    """
    return minutes * 60 + hours * 3600 + days * 86400 + weeks * 604800


def secs_to_wdhms(seconds):
    """Converts a number of seconds into weeks, days, hours, minutes
       and seconds. Returns the values in the same order with seconds as whole
       number.

       >>> secs_to_wdhms(1020)
       (0, 0, 0, 17, 0)
       """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    w, d = divmod(d, 7)
    s, tmp = divmod(s, 1)  # reduce to whole seconds
    return (w, d, h, m, s)


def timestamp(fmt="%a, %d %b %Y %H:%M:%S +0000"):
    """Return string with current time, according to given
format. Default is rfc822 compliant date value.

    >>> sal.time.timestamp()    #doctest: +SKIP
    'Thu, 16 Jul 2009 19:42:49 +0000'

    aliases:
        gmtimestamp
        rfc822timestamp
"""
    return time.strftime(fmt, time.gmtime())


gmtimestamp = timestamp
rfc822timestamp = timestamp


def localtimestamp(fmt="%a, %d %b %Y %H:%M:%S"):
    """Return string with current time, according to given
format. Default is rfc822 compliant date value.

    >>> localtimestamp()    #doctest: +SKIP
    'Thu, 16 Jul 2009 12:27:54'
"""
    return time.strftime(fmt, time.localtime())


SEC_IN_MIN = 60
SEC_IN_HOUR = SEC_IN_MIN * 60
SEC_IN_DAY = SEC_IN_HOUR * 24
SEC_IN_WEEK = SEC_IN_DAY * 7


def TimeDurationToString(sec):
    """ TimeDurationToString(sec) --> String that represents number
                                      of weeks, days, hours, and seconds
                                      that are in 'sec' seconds
    """
    res = ''
    if sec >= SEC_IN_WEEK:
        week, sec = divmod(sec, SEC_IN_WEEK)
        res = '%s%dw' % (res, week)
    if sec >= SEC_IN_DAY:
        day, sec = divmod(sec, SEC_IN_DAY)
        res = '%s%dd' % (res, day)
    if sec >= SEC_IN_HOUR:
        hour, sec = divmod(sec, SEC_IN_HOUR)
        res = '%s%dh' % (res, hour)
    if sec >= SEC_IN_MIN:
        min, sec = divmod(sec, SEC_IN_MIN)
        res = '%s%dm' % (res, min)
    if sec > 0:
        res = '%s%ds' % (res, sec)
    return res


class CountDownTimer:
    """A countdown timer.  Does NOT signal when it has expired; you
    will need to check it via is_expired to see if the designated time
    has passed.

    >>> tmr = CountDownTimer(15)                      #doctest: +SKIP
    >>> tmr.start()                                   #doctest: +SKIP
    <sal.time.CountDownTimer instance at 0x14e5710>
    >>> tmr.is_active()                               #doctest: +SKIP
    True
    >>> tmr.time_elapsed()                            #doctest: +SKIP
    21.305315017700195
    >>> tmr.is_expired()                              #doctest: +SKIP
    True
    """

    def __init__(self, timeout=15.0):
        """The timer will expire in 'timeout' seconds"""
        self._timeout = float(timeout)
        self._start_time = None
        self._is_started = False

    def __str__(self):
        s = []
        s += ['CountDownTimer']
        s += ['--------------']
        s += ['timeout   :%s' % self._timeout]
        s += ['start_time:%s' % self._start_time]
        s += ['is_started:%s' % self._is_started]
        return '\n'.join(s)

    def start(self):
        """Start the timer countdown"""
        self._start_time = time.time()
        self._is_started = True
        return self

    def restart(self):
        """Restart the timer countdown.
        Note: restart & start behave the same."""
        return self.start()

    def is_expired(self):
        """Check if the timer has expired"""
        assert self._is_started, 'must start the timer first'
        return bool((time.time() - self._start_time) >= self._timeout)

    def is_active(self):
        return not self.is_expired()

    def time_elapsed(self):
        if self._is_started:
            return time.time() - self._start_time
        else:
            return 0.0
