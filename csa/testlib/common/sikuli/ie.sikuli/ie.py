# $Id: //prod/main/sarf_centos/testlib/common/sikuli/ie.sikuli/ie.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $
import os
import sys
import sikulilog as log
from sikuli.Sikuli import *

iescriptPath = "ie.sikuli"
addImagePath(iescriptPath)
setAutoWaitTimeout(10)


class Ie(object):

    def openIe(self):
        mark = log.get_length()
        App.open("iexplore")
        wait(2)
        click("1356051789586.png")
        wait(5)
        log.process(mark)

    def _openProxy(self):
        type("t", KEY_ALT)
        for i in range(0, 17):
            type(Key.DOWN)
            wait(2)
        type(Key.ENTER)
        wait("Connections.png")
        click("Connections.png")
        wait("SafariLANsettin.png")
        click("SafariLANsettin.png")
        click("Useaproxyser.png")

    def _closeIe(self):
        click("x7.png")
        wait(2)

    def setupProxyIe(self, proxyhost=None, port="3128"):
        mark = log.get_length()
        self._openProxy()
        type(Key.TAB)
        type(proxyhost)
        type(Key.TAB)
        type(port)
        wait(2)
        type(Key.ENTER)
        wait(2)
        type(Key.TAB)
        type(Key.ENTER)
        wait(2)
        self._closeIe()
        log.process(mark)

    def acceptUntrustedCertificateIe(self):
        mark = log.get_length()
        App.focus("iexplore")
        wait(2)
        wait("Continuetoth-1.png")
        click("Continuetoth-1.png")
        wait("1363677504975.png")
        click("1363677504975.png")
        click("ViewCertificates-1.png")
        click("ilnstallCert.png")
        click("Next.png")
        click("Next.png")
        click("Finish.png")
        click("OK-2.png")
        click("1364251966795.png")
        log.process(mark)

    def authenticateIe(self, domain="wga", username="admin",
                       password="ironport", url="http://mail.google.com"):
        mark = log.get_length()
        App.open("iexplore")
        wait(5)
        type("t", KEY_CTRL)
        type(url)
        type(Key.ENTER)
        wait("SETHBHTE.png", 120)
        type("SETHBHTE.png", "%s\\%s" % (domain, username))
        type(Key.TAB)
        type(password)
        click("OK.png")
        wait(2)
        log.process(mark)

    def cleanupIe(self):
        mark = log.get_length()
        self._openProxy()
        type(Key.ENTER)
        wait(2)
        type(Key.TAB)
        wait(2)
        type(Key.ENTER)
        wait(2)
        self._closeIe()
        log.process(mark)


if __name__ == "__main__":
    ie = Ie()
    ie.openIe()
    ie.setupProxyIe()
    ie.authenticateIe()
    ie.cleanupIe()
