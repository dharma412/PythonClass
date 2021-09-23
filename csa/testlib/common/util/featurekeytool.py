#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/common/util/featurekeytool.py#2 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import commands
import urllib
import re
import time
import os
from sal.containers.yesnodefault import YES, NO, DEFAULT
from sal.exceptions import ConfigError

from WsaCliLibrary import WsaCliLibrary
from common.util.utilcommon import UtilCommon

gen_fkey = os.environ['SARF_HOME'] + '/bin/genfkey.py'


class GenericFeatureKey:
    """Serves as a base class for the various FeatureKey interface classes,
    such as WebrootFeatureKey, L4TrafficMonitorFeatureKey,
    URLFilteringFeatureKey etc."""
    forever = 'forever'
    perpetual = 'Perpetual'
    dormant = 'Dormant'
    expired = 'expired'
    notinstalled = 'notinstalled'

    def __init__(self, dut, cli, shell):
        # by default use backdoor since only the backdoor output
        # provides per second granularity.
        self.checkmethod = 'backdoor'
        self.dut = dut
        self._cli = cli
        self._shell = shell
        self.available_methods = ('showconfig', 'featurekey', 'backdoor')
        self.component = None
        self.keystr_showconfig = None
        self.keystr_featurekey = None

    def get_ctor(self):
        return self._cli

    def get_shell(self):
        return self._shell

    def get_serial(self):
        out = self.get_ctor().version()
        lines = out.split('\n')
        for line in lines:
            if line.startswith('Serial'):
                return line.split(":", 1)[1].strip()

    def is_forever_key(self, key_time=None):
        key_time = key_time or self.get_key_time()
        assert key_time, 'key_time is None.'
        key_time = str(key_time)
        return bool(key_time.lower().find(self.forever.lower()) >= 0)

    def is_dormant_key(self, key_time=None):
        key_time = key_time or self.get_key_time()
        assert key_time, 'key_time is None.'
        return bool(key_time == 30 * 24 * 60 * 60)  # 30 days

    def is_expired_key(self, key_time=None):
        key_time = key_time or self.get_key_time()
        assert key_time, 'key_time is None.'
        key_time = str(key_time)
        return bool(key_time.lower().find(self.expired.lower()) >= 0)

    def expire_key(self):
        """Expire the feature key. Assert the key has been expired."""
        self.set_key(keytime=5, reset=YES)
        time.sleep(5)
        assert self.is_expired_key(), 'key has not expired!'

    def convert_key_time_seconds(self, key_time, return_string_bool=True):
        """ key_time can be "\d+ mins", "\d+ min", "\d+ secs",
            or "\d+ mins \d+ secs", "expired", "Dormant/Perpetual"
        Return converted time in seconds, 'expired', or 'forever'."""

        # handle case when key_time is: expired, Dormant, forever
        special_key_times = {
            True: {'expired': self.expired,
                   'forever': self.forever},
            False: {'expired': 0,
                    'forever': None},
        }
        if self.is_expired_key(key_time):
            return special_key_times[return_string_bool]['expired']
        if self.is_dormant_key(key_time) or self.is_forever_key(key_time):
            return special_key_times[return_string_bool]['forever']

        # convert time component to seconds
        sec_per_day = 24 * 60 * 60
        conversion_dict = {
            "(\d+) years?": 365 * sec_per_day,
            # note: no "months"
            "(\d+) weeks?": 7 * sec_per_day,
            "(\d+) days?": 1 * sec_per_day,
            "(\d+) hours?": 3600,
            "(\d+) mins?": 60,
            "(\d+) secs?": 1,
        }
        seconds = 0
        for patt, conversion_factor in conversion_dict.items():
            m = re.search(patt, key_time)
            if m:
                seconds += int(m.group(1)) * conversion_factor
        return seconds

    def create_key_via_backdoor(self, duration, clear,
                                duration_additive):
        opts_dict = {'component': self.component, 'quantity': 1}
        if clear != NO:
            clear = 1
        else:
            clear = None
        opts_dict['clear'] = clear
        if duration_additive:
            opts_dict['duration_additive'] = 1
        if duration:
            expiry = int(time.time()) + duration
            opts_dict['expiry'] = expiry
            opts_dict['duration'] = duration
        else:
            opts_dict['deadline'] = None
        print "Key options: %s" % (opts_dict,)

        code_list = (
            "import features.utils",
            "import tags",
            "start = '<START_MARKER>'",
            "end = '<END_MARKER>'",
            "key = features.utils._encode_key(%s)" % (opts_dict),
            "key = features.utils._encrypt_string(key, \
                tags.hardware_address())",
            "key = features.utils._denormalize_key(key)",
            "print start, key, end",
            "")
        out = self.get_shell().backdoor.run('hermes', code_list)

        matches = re.search('<START_MARKER>\s([A-Za-z0-9/+=-]+)\s<END_MARKER>',
                            out)
        assert matches, "backdoor string((%s))" % out

        return matches.group(1)

    def create_key_via_genfkey(self, duration, quantity, serial, clear,
                               duration_additive):
        global gen_fkey

        print("Eval key request for serial# %s" % serial)
        cmd = gen_fkey + \
              " --component=%s" \
              " --duration=%s" \
              " --hardware_address=%s" \
              " --quantity=%s" \
              % (self.component, duration, serial, quantity)

        # If there are clear and duration_additive options in the same time,
        # each is ignored by genfkey.py. So if there are they both,
        # duration_additive is used.

        if duration_additive != None:
            cmd += " --duration_additive=%s" % (duration_additive,)
        else:
            cmd += " --clear=%s" % (clear or 'No')

        print("featurekey command:" + cmd)
        key = commands.getoutput(cmd).strip()

        key = key.split('\n')[-1]
        print("Auto-Generated Feature Key:%s" % key)
        return key

    def create_key(self, duration=None, quantity=None, serial=None, clear=None,
                   duration_additive=None, method='backdoor', clobber=0):
        """Obtains a feature key of the specified duration and quantity.
        (quantity is the number of items granted by this key. Defaults to 1)
        Return feature key string.
        """
        assert method in ('genfkey', 'backdoor'), \
            "No such method of getting key information: %s" % method

        serial = serial or self.get_serial()
        quantity = quantity or 1

        if (not duration) or self.is_forever_key(duration):
            duration = 0

        if method == 'backdoor':
            return self.create_key_via_backdoor(duration, clear,
                                                duration_additive)
        elif method == 'genfkey':
            return self.create_key_via_genfkey(duration, quantity, serial,
                                               clear, duration_additive)

    def get_key_info(self, method=None):
        """Retrieves the key time (seconds, self.forever, self.expired,
        self.notinstalled None) and quantity (int or None) using the
        specified method """
        method = method or self.checkmethod
        assert method in self.available_methods, \
            "No such method of getting key information: %s" % method
        if method == "showconfig":
            qty, key_time = self.get_key_info_from_showconfig(
                self.keystr_showconfig)
        elif method == "featurekey":
            qty, key_time = self.get_key_info_from_featurekey(
                self.keystr_featurekey)
        elif method == "backdoor":
            qty, key_time = self.get_key_info_from_backdoor()
        return qty, key_time

    def get_key_time(self, method=None):
        qty, key_time = self.get_key_info(method)
        return key_time

    def get_key_quantity(self, method=None):
        qty, key_time = self.get_key_info(method)
        return qty

    def get_key_info_from_showconfig(self, keystr):
        """Gets a feature key (duration,quantity) from "showconfig".
        Key string is text following "Feature "

        Return (quantity, feature_key) tuple or None.
        feature_key is  seconds, 'forever' or 'expired' """
        showconfig = self.get_ctor().showconfig()
        rexp = re.compile('^\s+Feature "%s": Quantity = (\d+), ' \
                          'Time Remaining = "([^"]+)"\s*$' % keystr, re.MULTILINE)
        match = rexp.search(showconfig)
        if not match:
            # looks like searched feature key is not installed
            print("Search for <%s> in showconfig returned nothing." % (keystr))
            return (None, self.notinstalled)
        quantity = int(match.group(1))
        keytimetext = match.group(2)
        key_time = self.convert_key_time_seconds(keytimetext)
        return (quantity, key_time)

    def get_key_info_from_featurekey(self, keystr):
        """Gets a feature key (duration,quantity) from "showconfig".
        Key string is text in first column

        Return (quantity, feature_key) tuple or None.
        feature_key is  seconds, 'forever' or 'expired' """
        featurematch = self.get_ctor().featurekey().get_featurekey(
            key_str=keystr)
        if not featurematch:
            # looks like searched feature key is not installed
            print("Search for <%s> in featurekey returned nothing." % (keystr))
            return (None, self.notinstalled)
        quantity = int(featurematch.group(1))
        keytimetext = featurematch.group(2)
        key_time = self.convert_key_time_seconds(keytimetext)
        return (quantity, key_time)

    def get_key_info_from_backdoor(self):
        """Gets a feature key (duration,quantity) from the backdoor.
        This is the only method we have of getting key time in seconds!
        Return (quantity, feature_key) tuple.
        feature_key is  seconds, 'forever' or 'expired' """

        # Execute in the MGA's backdoor:
        #   features.get(keytype).get_remaining_time()
        code_list = (
            """import features.feature""",
            """f = features.feature._all_features['%s']""" % self.component,
            """start='<START_MARKER>'""",
            """end='<END_MARKER>'""",
            """print start, f.get_remaining_time(), end""",
            """print start, f.get_quantity(), end""",
        )

        out = self.get_shell().backdoor.run('hermes', code_list)
        # 'out' format:
        # import features
        # >>> f = features.get('max_interfaces')
        # >>> start='<START_MARKER>'
        # >>> end='<END_MARKER>'
        # >>> print start, f.get_remaining_time(), end
        # <START_MARKER> None <END_MARKER>
        # >>> print start, f.get_quantity(), end
        # <START_MARKER> 4 <END_MARKER>
        # >>>
        matches = re.findall('<START_MARKER>\s(.*)\s<END_MARKER>', out)
        assert matches, "backdoor string((%s))" % out

        if matches[0] == 'None' and matches[1] == 'None':  # not installed
            return (None, self.notinstalled)

        if matches[0] == 'None':  # forever key
            return int(matches[1]), self.forever

        # key_time is in seconds
        key_time, qty = map(int, map(float, matches))

        if key_time <= 0:  # expired key
            key_time = self.expired

        return qty, key_time

    def set_key(self, keytime=None, quantity=None, checksame=NO,
                checkdecrease=NO, reset=NO, forcecountdown=NO, checkmethod=None,
                duration_additive=None):
        """Retrieves and sets a new feature key, and allows for the key to be
        reset with a forever key first, and checked for decreasing or constant
        keytime.  Some keys can also be forced to begin countdown"""
        checkmethod = checkmethod or self.checkmethod

        print "Setting %ss %s" % (keytime, self.__class__.__name__)

        newkey = self.create_key(
            duration=keytime,
            quantity=quantity,
            clear=reset,
            duration_additive=duration_additive,
            method="backdoor"
        )

        # wait a second before setting key. Sometimes if you set the key
        # too fast it doesn't register!?
        time.sleep(5)

        self.get_ctor().feature_key_activate(key=newkey)
        if (forcecountdown == YES):
            self.force_countdown()
        if checksame:
            time.sleep(5)
            result = self.test_key(checkmethod, equalto=keytime)
            if result == NO:
                return None
        if checkdecrease:
            time.sleep(5)
            result = self.test_key(checkmethod, lt=keytime - 4)
            if result == NO:
                return None
        return newkey

    def force_countdown(self):
        """Activate keyed feature (eg. by enabling the feature via CLI) thus
         starting the feature key countdown timer."""
        pass

    def test_key(self, method=None, expired=None, forever=None,
                 blank=None, equalto=None, gt=None, gte=None, lt=None,
                 lte=None, decreasing=None, stayingconstant=None, quantityequal=None):
        """returns the logical AND of all given tests (format: YES or NO)
        """
        method = method or self.checkmethod

        # check quantity
        if quantityequal == None:
            keytime = self.get_key_time(method)
        else:
            print("Checking key quantity==%s" % quantityequal)
            info = self.get_key_info(method)
            if not info:
                print("No quantity info obtained")
                return NO
            if quantityequal != info[0]:
                print("quantity=%s" % info[0])
                return NO
            keytime = info[1]

        # check blank
        if keytime == None:
            if blank == YES:
                return YES
            # no other test can be performed on keytime==None, return
            elif blank == NO:
                return YES
            print("keytime is %s, although a value was expected" % keytime)
            return NO

        # check expired
        if (expired == YES) and (not self.is_expired_key(keytime)):
            return NO
        if (expired == NO) and (self.is_expired_key(keytime)):
            return NO

        # check forever
        if (forever == YES) and (keytime != self.forever):
            return NO
        if (forever == NO) and (keytime == self.forever):
            return NO
        if (keytime == self.forever) or (self.is_expired_key(keytime)):
            if ((equalto != None) or (gt != None) or (gte != None) or (lt != None)
                    or (lte != None) or (decreasing != None) or (stayingconstant != None)):
                print("comparison test illegal with key <%s>" % keytime)
                raise ConfigError, "comparison test illegal with key <%s>" \
                                   % keytime

        # check equalto
        if (equalto != None) and (keytime != equalto):
            print("equalto comparison negative keytime %s != %s" \
                  % (keytime, equalto))
            return NO
        # check greater-than (gt)
        if (gt != None) and (keytime <= gt):
            print("gt comparison negative keytime %s !> %s" % (keytime, gt))
            return NO
        # check less-than (lt)
        if (lt != None) and (keytime >= lt):
            print("lt comparison negative keytime %s !< %s" % (keytime, lt))
            return NO
        # check greater-than-or-equal (gte)
        if (gte != None) and (keytime < gte):
            print("gte comparison negative keytime %s !>= %s" % (keytime, gte))
            return NO
        # check less-than-or-equal (lte)
        if (lte != None) and (keytime > lte):
            print("lte comparison negative keytime %s !<= %s" % (keytime, lte))
            return NO
        # check if key is decreasing
        if (decreasing == YES) or (stayingconstant == NO):
            time.sleep(5)
            keytime2 = self.get_key_time(method)
            if (keytime2 >= keytime):
                return NO
        # check if key is staying constant
        if (decreasing == NO) or (stayingconstant == YES):
            time.sleep(5)
            keytime2 = self.get_key_time(method)
            if (keytime2 != keytime):
                return NO
        return YES

    def update_fkey(self, threshold=86400, keytime=2592000):
        """Set featurekey with duration `keytime` if remaining time is less
        than threshold
        :Parameters:
            - `threshold`: lower remaining time
            - `keytime`: remaining time to be set
        """
        fkey_time_remain = self.get_key_time()
        if fkey_time_remain in (self.notinstalled, self.expired) or \
                fkey_time_remain < threshold:
            print('Installing %ds feature key for component %s...' %
                  (keytime, self.component))
            self.set_key(keytime=keytime, reset=YES, forcecountdown=YES)

    def delete_key(self):
        """
        Delete this key using the hermes backdoor
        """
        code_list = (
            """import features.feature""",
            """f = features.feature._all_features['%s']""" % self.component,
            """start='<START_MARKER>'""",
            """end='<END_MARKER>'""",
            """print start, f.delete_key(), end""",
        )
        out = self.get_shell().backdoor.run('hermes', code_list)
        matches = re.search('<START_MARKER>\s(.*)\s<END_MARKER>',
                            out)
        assert matches, "backdoor string((%s))" % out

        return matches.group(1)


class WebrootFeatureKey(GenericFeatureKey):
    """Feature key enabling Webroot"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = "Webroot"
        self.component = "merlin"

    def force_countdown(self):
        raise NotImplementedError


class L4TrafficMonitorFeatureKey(GenericFeatureKey):
    """Feature key enabling L4 traffic monitor"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = "L4 Traffic Monitor"
        self.component = "trmon"

    def force_countdown(self):
        raise NotImplementedError


class WebReputationFiltersFeatureKey(GenericFeatureKey):
    """Feature key enabling WBRS support"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Web Reputation Filters"
        self.component = "wbrs"

    def force_countdown(self):
        raise NotImplementedError


class URLFilteringFeatureKey(GenericFeatureKey):
    """Feature key enabling URL filtering"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = "URL Filtering"
        self.component = "cato"

    def force_countdown(self):
        raise NotImplementedError


class McAfeeFeatureKey(GenericFeatureKey):
    """Feature key enabling McAfee AV filtering"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = "McAfee"
        self.component = "mcafee"

    def force_countdown(self):
        raise NotImplementedError


class HTTPSFeatureKey(GenericFeatureKey):
    """Feature key enabling HTTPS engine"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = "HTTPS Proxy"
        self.component = "https"

    def force_countdown(self):
        raise NotImplementedError


class MUSFeatureKey(GenericFeatureKey):
    """Feature key enabling Mobile User Security"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = "Mobile User Security"
        self.component = "mus"

    def force_countdown(self):
        raise NotImplementedError


class SophosFeatureKey(GenericFeatureKey):
    """Feature key enabling McAfee AV filtering"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = "Sophos"
        self.component = "sophos"

    def force_countdown(self):
        raise NotImplementedError


class FirestoneFeatureKey(GenericFeatureKey):
    """Feature key enabling Web Usage Controls"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = "Cisco IronPort " \
                                                          "Web Usage Controls"
        self.component = "firestone"

    def force_countdown(self):
        raise NotImplementedError


class ProxyFeatureKey(GenericFeatureKey):
    """Feature key enabling Cisco IronPort Web Proxy & DVS Engine"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Cisco IronPort Web Proxy & DVS Engine"
        self.component = "proxy"

    def force_countdown(self):
        raise NotImplementedError


class CentralizedWebReportingFeatureKey(GenericFeatureKey):
    """Feature key enabling SMA Centralized Web Reporting"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Cisco IronPort Centralized Web Reporting"
        self.component = "c_web_rep_processing"

    def force_countdown(self):
        raise NotImplementedError


class CentralizedEmailReportingFeatureKey(GenericFeatureKey):
    """Feature key enabling SMA Centralized Email Reporting"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Cisco IronPort Centralized Email Reporting"
        self.component = "c_rep_processing"


class CentralizedEmailMessageTrackingFeatureKey(GenericFeatureKey):
    """Feature key enabling SMA Centralized Email Message Tracking"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Cisco IronPort Centralized Email Message Tracking"
        self.component = "c_track_processing"


class CentralizedWebConfigurationFeatureKey(GenericFeatureKey):
    """Feature key enabling SMA Centralized Web Configuration"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Cisco IronPort Centralized Web Configuration Manager"
        self.component = "iccm_processing"

    def force_countdown(self):
        raise NotImplementedError


class SpamQuarantineFeatureKey(GenericFeatureKey):
    """Feature key enabling SMA Spam Quarantine"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Cisco IronPort Spam Quarantine"
        self.component = "master_isq"


class CloudAdminFeatureKey(GenericFeatureKey):
    """Feature key enabling SMA Cloud Administration Mode"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Cloud Administration Mode"
        self.component = "cloud"


class BrightmailFeatureKey(GenericFeatureKey):
    """Feature key enabling ESA brightmail support"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Brightmail"
        self.component = "Brightmail"

    def force_countdown(self):
        raise NotImplementedError


class AntiSpamFeatureKey(GenericFeatureKey):
    """Feature key enabling ESA anti-spam support"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "IronPort Anti-Spam"
        self.component = "case"

    def force_countdown(self):
        raise NotImplementedError


class VirusOutbreakFeatureKey(GenericFeatureKey):
    """Feature key enabling ESA virus outbreak filter support"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Outbreak Filters"
        self.component = "VOF"

    def force_countdown(self):
        raise NotImplementedError


class ClusteringFeatureKey(GenericFeatureKey):
    """Feature key enabling ESA clustering(central mgmnt)support"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Central Mgmt"
        self.component = "clustering"

    def force_countdown(self):
        raise NotImplementedError


class IMSFeatureKey(GenericFeatureKey):
    """Feature key enabling ESA IMS(Ironport Multi-Scan Support"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Intelligent Multi-Scan"
        self.component = "ims"

    def force_countdown(self):
        raise NotImplementedError


class ImageAnalysisFeatureKey(GenericFeatureKey):
    """Feature key enabling ESA IronPort Image Analysis."""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "IronPort Image Analysis"
        self.component = "iia"

    def force_countdown(self):
        raise NotImplementedError


class CloudmarkFeatureKey(GenericFeatureKey):
    """Feature key enabling ESA Cloudmark antispam"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Cloudmark SP"
        self.component = "cloudmark"

    def force_countdown(self):
        raise NotImplementedError


class ReceivingFeatureKey(GenericFeatureKey):
    """Feature key enabling Incoming Mail Handling"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Receiving"
        self.component = "imh"

    def force_countdown(self):
        raise NotImplementedError


class RsaDlpFeatureKey(GenericFeatureKey):
    """Feature key for RSA DLP"""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "RSADLP"
        self.component = "rsadlp"

    def force_countdown(self):
        raise NotImplementedError


class EmailEncryptionFeatureKey(GenericFeatureKey):
    """Feature key enabling IronPort Email Encryption."""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "IronPort Email Encryption"
        self.component = "envelope_encryption"

    def force_countdown(self):
        raise NotImplementedError


class BounceVerificationFeatureKey(GenericFeatureKey):
    """Feature key enabling Bounce Verification."""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Bounce Verification"
        self.component = "bounce_verification"

    def force_countdown(self):
        raise NotImplementedError


class AmpFileReputationFeatureKey(GenericFeatureKey):
    """Feature key enabling AdvancedMalware."""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Amp File Reputation"
        self.component = "amp_file_rep"

    def force_countdown(self):
        raise NotImplementedError


class AmpFileAnalysisFeatureKey(GenericFeatureKey):
    """Feature key enabling AdvancedMalware."""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Amp File Analysis"
        self.component = "amp_file_analysis"

    def force_countdown(self):
        raise NotImplementedError


class GrymailSafeUnsubscribeFeatureKey(GenericFeatureKey):
    """Feature key enabling Graymail Safe Unsubscribe feature."""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "Graymail Safe Unsubscription"
        self.component = "gm_unsubscription"

    def force_countdown(self):
        raise NotImplementedError


class ExternalThreatFeedsFeatureKey(GenericFeatureKey):
    """Feature key enabling External Threat Feeds."""

    def __init__(self, dut, cli, shell):
        GenericFeatureKey.__init__(self, dut, cli, shell)
        self.keystr_showconfig = self.keystr_featurekey = \
            "External Threat Feeds"
        self.component = "ETF"

    def force_countdown(self):
        raise NotImplementedError


class FeaturekeyTool(UtilCommon):
    """Keywords to configure and check status of feature keys."""

    # 1st grouping is for WSA featurekeys
    # 2nd grouping is for SMA featurekeys
    # 3rd grouping is for ESA featurekeys
    valid_fk_dict = {
        'avc': FirestoneFeatureKey,
        'https': HTTPSFeatureKey,
        'l4tm': L4TrafficMonitorFeatureKey,
        'mcafee': McAfeeFeatureKey,
        'mus': MUSFeatureKey,
        'sophos': SophosFeatureKey,
        'wbrs': WebReputationFiltersFeatureKey,
        'webroot': WebrootFeatureKey,
        'cato': URLFilteringFeatureKey,
        'proxy': ProxyFeatureKey,

        'c_web_rep_processing': CentralizedWebReportingFeatureKey,
        'iccm_processing': CentralizedWebConfigurationFeatureKey,
        'master_isq': SpamQuarantineFeatureKey,
        'cloud': CloudAdminFeatureKey,
        'c_rep_processing': CentralizedEmailReportingFeatureKey,
        'c_track_processing': CentralizedEmailMessageTrackingFeatureKey,

        'Brightmail': BrightmailFeatureKey,
        'case': AntiSpamFeatureKey,
        'VOF': VirusOutbreakFeatureKey,
        'clustering': ClusteringFeatureKey,
        'ims': IMSFeatureKey,
        'iia': ImageAnalysisFeatureKey,
        'cloudmark': CloudmarkFeatureKey,
        'imh': ReceivingFeatureKey,
        'rsadlp': RsaDlpFeatureKey,
        'envelope_encryption': EmailEncryptionFeatureKey,
        'boun': BounceVerificationFeatureKey,
        'amp_file_rep': AmpFileReputationFeatureKey,
        'amp_file_analysis': AmpFileAnalysisFeatureKey,
        'gm_unsubscription': GrymailSafeUnsubscribeFeatureKey,
        'ETF': ExternalThreatFeedsFeatureKey
    }

    def __init__(self, *args, **kwargs):
        UtilCommon.__init__(self, *args, **kwargs)
        self._cli = WsaCliLibrary(self.dut, self.dut_version)

    def get_keyword_names(self):
        return [
            'feature_key_set_key',
            'feature_key_generate_key',
            'feature_key_delete_key',
            'feature_key_expire_key',
            'feature_key_get_key_time',
            'feature_key_is_forever_key',
            'feature_key_is_expire_key',
        ]

    def feature_key_generate_key(self, key, duration=None):
        """Generates specified key.

        Parameters:
           - `key`: type of key.  Either:
           | WSA | 'avc'  'https' 'l4tm' 'mcafee' 'mus' 'sophos' 'wbrs' 'webroot' 'proxy' 'cato' |
           | SMA | 'c_web_rep_processing' 'iccm_processing' 'master_isq' 'cloud' 'c_rep_processing' 'c_track_processing' |
           | ESA | 'Brightmail' 'case' 'VOF' 'clustering' 'ims' 'iia' 'cloudmark' 'imh' 'rsadlp' 'envelope_encryption' 'boun' 'amp_file_rep' 'amp_file_analysis' |
           - `duration`: life time of key in second.  Defaulted to forever.

        Examples:
        | Feature Key Generate Key | mcafee | | #forever McAfee key |
        | Feature Key Generate Key | sophos | duration=2592000 | #30-day Sophos key |
        """
        if key not in self.valid_fk_dict:
            raise ValueError, 'Invalid key type - "%s"' % key
        if duration is not None:
            duration = int(duration)
        return self.valid_fk_dict[key](self.dut, self._cli, self._shell). \
            create_key(duration=duration)

    def feature_key_set_key(self, key, duration=None):
        """Generates and installs specified key onto WSA appliance.

        Parameters:
           - `key`: type of key.  Either:
           | WSA | 'avc'  'https' 'l4tm' 'mcafee' 'mus' 'sophos' 'wbrs' 'webroot' 'proxy' 'cato' |
           | SMA | 'c_web_rep_processing' 'iccm_processing' 'master_isq' 'cloud' 'c_rep_processing' 'c_track_processing' |
           | ESA | 'Brightmail' 'case' 'VOF' 'clustering' 'ims' 'iia' 'cloudmark' 'imh' 'rsadlp' 'envelope_encryption' 'boun' 'amp_file_rep' 'amp_file_analysis' |
           - `duration`: life time of key in second.  Defaulted to forever.

        Examples:
        | Feature Key Set Key | mcafee | | #forever McAfee key |
        | Feature Key Set Key | sophos | duration=2592000 | #30-day Sophos key |
        """
        if key not in self.valid_fk_dict:
            raise ValueError, 'Invalid key type - "%s"' % key
        if duration is not None:
            duration = int(duration)
        self.valid_fk_dict[key](self.dut, self._cli, self._shell). \
            set_key(keytime=duration)

    def feature_key_delete_key(self, key):
        """Deletes specified key from appliance

        Parameters:
           - `key`: type of key.  Either:
           | WSA | 'avc'  'https' 'l4tm' 'mcafee' 'mus' 'sophos' 'wbrs' 'webroot' 'proxy' 'cato' |
           | SMA | 'c_web_rep_processing' 'iccm_processing' 'master_isq' 'cloud' 'c_rep_processing' 'c_track_processing' |
           | ESA | 'Brightmail' 'case' 'VOF' 'clustering' 'ims' 'iia' 'cloudmark' 'imh' 'rsadlp' 'envelope_encryption' 'boun' 'amp_file_rep' 'amp_file_analysis' |

        Examples:
        | Feature Key Delete Key | mcafee | | #delete McAfee key |
        """
        if key not in self.valid_fk_dict:
            raise ValueError, 'Invalid key type - "%s"' % key
        return self.valid_fk_dict[key](self.dut, self._cli, self._shell). \
            delete_key()

    def feature_key_expire_key(self, key):
        """Causes specified key to expire immediately.

        *Parameters:*
           - `key`: type of key to expire.  Either:
           | WSA | 'avc'  'https' 'l4tm' 'mcafee' 'mus' 'sophos' 'wbrs' 'webroot' 'proxy' 'cato' |
           | SMA | 'c_web_rep_processing' 'iccm_processing' 'master_isq' 'cloud' 'c_rep_processing' 'c_track_processing' |
           | ESA | 'Brightmail' 'case' 'VOF' 'clustering' 'ims' 'iia' 'cloudmark' 'imh' 'rsadlp' 'envelope_encryption' 'boun' 'amp_file_rep' 'amp_file_analysis' |

        *Examples:*
        | Feature Key Expire Key | mcafee |
        | Feature Key Expire Key | https |
        """
        if key not in self.valid_fk_dict:
            raise ValueError, 'Invalid key type - "%s"' % key
        self.valid_fk_dict[key](self.dut, self._cli, self._shell).expire_key()

    def feature_key_get_key_time(self, key):
        """Gets remaining duration of installed key.

        *Parameters:*
           - `key`: type of key to get duration for.  Either:
           | WSA | 'avc'  'https' 'l4tm' 'mcafee' 'mus' 'sophos' 'wbrs' 'webroot' 'proxy' 'cato' |
           | SMA | 'c_web_rep_processing' 'iccm_processing' 'master_isq' 'cloud' 'c_rep_processing' 'c_track_processing' |
           | ESA | 'Brightmail' 'case' 'VOF' 'clustering' 'ims' 'iia' 'cloudmark' 'imh' 'rsadlp' 'envelope_encryption' 'boun' 'amp_file_rep' 'amp_file_analysis' |

        *Examples:*
        | Feature Key Get Key Time | mcafee |
        | Feature Key Get Key Time | https |
        """
        if key not in self.valid_fk_dict:
            raise ValueError, 'Invalid key type - "%s"' % key
        return self.valid_fk_dict[key](self.dut, self._cli, self._shell). \
            get_key_time()

    def feature_key_is_forever_key(self, key):
        """Checks to see if specified key is a forever key.

        *Parameters:*
           - `key`: type of key to check for.  Either
           | WSA | 'avc'  'https' 'l4tm' 'mcafee' 'mus' 'sophos' 'wbrs' 'webroot' 'proxy' 'cato' |
           | SMA | 'c_web_rep_processing' 'iccm_processing' 'master_isq' 'cloud' 'c_rep_processing' 'c_track_processing' |
           | ESA | 'Brightmail' 'case' 'VOF' 'clustering' 'ims' 'iia' 'cloudmark' 'rsadlp' 'envelope_encryption' 'boun' 'amp_file_rep' 'amp_file_analysis' |

        *Examples:*
        | ${status}= | Feature Key Is Forever Key | mcafee |
        | ${status}= | Feature Key Is Forever Key | mus |
        """
        if key not in self.valid_fk_dict:
            raise ValueError, 'Invalid key type - "%s"' % key
        return self.valid_fk_dict[key](self.dut, self._cli, self._shell). \
            is_forever_key()

    def feature_key_is_expire_key(self, key):
        """Checks to see if specified key has expired.

        *Parameters:*
           - `key`: type of key to check for.  Either
           | WSA | 'avc'  'https' 'l4tm' 'mcafee' 'mus' 'sophos' 'wbrs' 'webroot' 'proxy' 'cato' |
           | SMA | 'c_web_rep_processing' 'iccm_processing' 'master_isq' 'cloud' 'c_rep_processing' 'c_track_processing' |
           | ESA | 'Brightmail' 'case' 'VOF' 'clustering' 'ims' 'iia' 'cloudmark' 'imh' 'rsadlp' 'envelope_encryption' 'boun' 'amp_file_rep' 'amp_file_analysis' |

        *Examples:*
        | ${status}= | Feature Key Is Expire Key | avc |
        | ${status}= | Feature Key Is Expire Key | webroot |
        """
        if key not in self.valid_fk_dict:
            raise ValueError, 'Invalid key type - "%s"' % key
        return self.valid_fk_dict[key](self.dut, self._cli, self._shell). \
            is_expired_key()
