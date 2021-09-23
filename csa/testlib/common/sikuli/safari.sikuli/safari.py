# $Id: //prod/main/sarf_centos/testlib/common/sikuli/safari.sikuli/safari.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $
import os
import sys
import sikulilog as log
from sikuli.Sikuli import *

safariscriptPath = "safari.sikuli"
addImagePath(safariscriptPath)
setAutoWaitTimeout(10)


class Safari(object):

    def openSafari(self):
        mark = log.get_length()
        App.open("Safari")
        wait(2)
        App.focus("Safari")
        wait(2)
        log.process(mark)

    def setupProxySafari(self, proxyhost=None, port="3128"):
        mark = log.get_length()
        click("1356039750608.png")
        wait(2)
        type(",", KEY_CTRL)
        wait("SafariAdvanced.png")
        click("SafariAdvanced.png")
        wait("SafariChangeSettin.png")
        click("SafariChangeSettin.png")
        wait("SafariLANsettin.png")
        click("SafariLANsettin.png")
        click("Useaproxyser.png")
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
        click("x7.png")
        wait(2)
        type("q", KEY_CTRL)
        type(Key.ENTER)
        wait(2)
        log.process(mark)

    def authenticateSafari(self, domain="wga", username="admin",
                           password="ironport", url="http://www.google.com"):
        mark = log.get_length()
        App.open("Safari")
        wait(5)
        type("t", KEY_CTRL)
        type(url)
        type(Key.ENTER)
        wait("Name.png", 120)
        type("Name.png", "%s\\%s" % (domain, username))
        type(Key.TAB)
        type(password)
        click("LogIn.png")
        wait(2)
        log.process(mark)

    def cleanupSafari(self):
        mark = log.get_length()
        type(",", KEY_CTRL)
        wait(2)
        wait("SafariAdvanced.png")
        click("SafariAdvanced.png")
        wait("SafariChangeSettin.png")
        click("SafariChangeSettin.png")
        wait("SafariLANsettin.png")
        click("SafariLANsettin.png")
        click("Useaproxyser.png")
        type(Key.ENTER)
        wait(2)
        type(Key.TAB)
        wait(2)
        type(Key.ENTER)
        wait(2)
        click("x7.png")
        wait(2)
        type("q", KEY_CTRL)
        type(Key.ENTER)
        wait(2)
        log.process(mark)


if __name__ == "__main__":
    safari = Safari()
    safari.openSafari()
    safari.setupProxySafari()
    safari.authenticateSafari()
    safari.cleanupSafari()
