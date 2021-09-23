#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/sal/net/services/netinstallpage.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $
""" Client module for Ironport phoebeinstall.cgi interface.  """

import urllib
import re
from cStringIO import StringIO
import getpass
from sal.containers import cfgholder
from sal.net import ifc

subnet_list = ifc._InterfaceInfo.subnets.keys()

cfg = cfgholder.CfgHolder()
cfg.datalisturl = {}
cfg.updateurl = {}
for subnet in subnet_list:
    cfg.datalisturl[subnet] = 'http://install.' + subnet + \
                              '/netinstall.cgi?render=text&format=machine%20user%20until'
    cfg.updateurl[subnet] = 'http://install.' + subnet + '/netinstall.cgi'


class TextGetter(object):
    def __init__(self, url=None):
        self._fo = None
        if url:
            self.get(url)

    def close(self):
        if self._fo:
            self._fo.close()
            self._fo = None

    def get(self, url):
        s = []
        fo = urllib.urlopen(url)
        data = fo.read(16384)
        while data:
            s.append(data)
            data = fo.read(16384)
        fo.close()
        self._fo = StringIO("".join(s))
        self._fo.seek(0, 0)

    def readline(self):
        return self._fo.readline()

    def getvalue(self):
        return self._fo.getvalue()

    def readlines(self):
        line = self._fo.readline()
        while line:
            yield line.strip()
            line = self._fo.readline()

    def __str__(self):
        if self._fo:
            return self._fo.getvalue()
        else:
            return "<empty>"


class PhoebeInstall(object):
    """Interface to the Ironport phoebeinstall.cgi web interface.
    NOTE: script name has changed to netinstall.cgi.
    """

    def __init__(self, phoebeinstall=None):
        self.reset()
        self._config = phoebeinstall or cfg

    def reset(self):
        """reset() - clears the cached values."""
        self._result = None
        self.buildlist = []
        self.gatewaylist = []
        self.test_machinelist = []
        self._tagmap = {"build": self.buildlist,
                        "messaging_gateway": self.gatewaylist,
                        "test_machine": self.test_machinelist, }

    def close(self):
        self.reset()
        self._config = None

    def update(self, target_network=None):
        """update - updates this object with the latest lists. It populates
        'buildlist', 'gatewaylist', and 'test_machinelist'."""
        self.reset()
        for network, domain_url in self._config.datalisturl.items():
            if target_network and target_network != network:
                continue  # optimization (skip to specified target_network)
            try:
                tg = TextGetter()
                try:
                    tg.get(domain_url)
                except:
                    raise EnvironmentError('Can not get ' + domain_url)
                for line in tg.readlines():
                    array = line.split("\t")
                    # tag is: test_machine, build, or messaging_gateway
                    # value is: hostname or build_id
                    if len(array) > 1:
                        tag = array[0]
                        value = array[1]
                        if tag in self._tagmap.keys():
                            if value not in self._tagmap[tag]:
                                self._tagmap[tag].append(value)
            finally:
                tg.close()
        self.buildlist.sort()
        self.gatewaylist.sort()
        self.test_machinelist.sort()

    def get_build_list(self, build_regex=None, network=None):
        if not self.buildlist:
            self.update(target_network=network)

        if not build_regex:
            return self.buildlist

        return self.get_matching_builds(build_regex)  # returns a build list

    def get_matching_builds(self, regexp):
        """Return a sub-set of the build list that matches a regular
        expression."""
        if not self.buildlist:
            self.update()
        matcher = re.compile(regexp)
        return filter(matcher.search, self.buildlist)

    def change(self, dut, build, model, preconfigure):
        """change(dut_name, build_id)
        Forces a change of build version that the DUT will reload with."""
        dut = str(dut)  # coerce to string, in case it is a device object
        if not self.buildlist:
            self.update()
        if build in self.buildlist:
            form = self._get_form(dut, build, model, preconfigure)
            self._send_form(form, dut)
        else:
            raise ValueError, "Build <%s> not in the build list!" % build

    def _get_form(self, dut, build, model, preconfigure):
        form = []
        form.append(("render", "text"))
        form.append(("format", "machine"))
        if model != 'NONE':
            form.append(("%s_model" % dut, model))
        form.append(("%s_build" % dut, build))
        form.append(("%s_preconfigure" % dut, preconfigure))
        form.append(("Change", "Change"))
        return form

    def _send_form(self, formdata, dut):
        """_send_form(form) - sends a form in the form of a dictionary or list
        of tuples to the server."""
        # NOTE: Regardless of subdomains like mlab1.qa, we still want to access
        #       the main "install.qa", not "install.mlab1.qa"
        form = urllib.urlencode(formdata)
        domain = dut.split(".")[-1]
        fo = urllib.urlopen(self._config.updateurl[domain], form)
        self._result = fo.read()
        fo.close()


def build2version(build_id):
    """Converts a build_id to match the format of the CLI version string."""
    [ph, major, minor, subminor, build] = build_id.split("-")
    return "%s.%s.%s-%s" % (major, minor, subminor, build)


# sample
"""
POST /phoebeinstall.cgi HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 258

melissa.qa_build=phoebe-3-0-0-011&melissa.qa_model=A50&melissa.qa_platform=DELL+2550&melissa.qa_raid=RAID10&melissa.qa_drivesize=&melissa.qa_preconfigure=Testing&melissa.qa_comment=test+development&melissa.qa_user=Keith&melissa.qa_until=forever&Change=Change
"""

if __name__ == "__main__":
    import pprint

    pi = PhoebeInstall()
    pi.update()
    pprint.pprint(pi.buildlist)
