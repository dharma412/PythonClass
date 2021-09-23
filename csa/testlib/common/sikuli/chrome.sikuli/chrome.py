# $Id: //prod/main/sarf_centos/testlib/common/sikuli/chrome.sikuli/chrome.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $
import os
import sys
import sikulilog as log
from sikuli.Sikuli import *

chromescriptPath = "chrome.sikuli"
addImagePath(chromescriptPath)


class Chrome(object):

    def openChrome(self):
        mark = log.get_length()
        App.open("Chrome")
        wait(2)
        App.focus("Chrome")
        wait(2)
        log.process(mark)

    def setupProxyChrome(self, proxyhost=None, port="3128"):
        mark = log.get_length()
        type("t", KEY_CTRL)
        type("f", KEY_ALT)
        type("s", KEY_SHIFT)
        wait(2)
        type(Key.PAGE_DOWN + Key.PAGE_DOWN)
        wait(2)
        click("Shawadvanced.png")
        wait(2)
        type(Key.PAGE_DOWN + Key.PAGE_DOWN)
        wait(2)
        click("Changeproxys.png")
        wait(4)
        click("LANsettings.png")
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
        App.close("Chrome")
        wait(2)
        log.process(mark)

    def authenticateChrome(self, domain="wga", username="admin",
                           password="ironport"):
        mark = log.get_length()
        App.open("Chrome")
        wait(5)
        type("t", KEY_CTRL)
        type("http://www.google.com")
        type(Key.ENTER)
        wait(2)
        type("ChromeUserName.png", "%s\\%s" % (domain, username))
        type(Key.TAB)
        type(password)
        click("LoqIn.png")
        wait(2)
        log.process(mark)

    def cleanupChrome(self):
        mark = log.get_length()
        type("t", KEY_CTRL)
        type("f", KEY_ALT)
        type("s", KEY_SHIFT)
        wait(2)
        type(Key.PAGE_DOWN + Key.PAGE_DOWN)
        wait(2)
        click("Shawadvanced.png")
        wait(2)
        type(Key.PAGE_DOWN + Key.PAGE_DOWN)
        wait(2)
        click("Changeproxys.png")
        wait(4)
        click("LANsettings.png")
        click("Useaproxyser.png")
        type(Key.ENTER)
        wait(2)
        type(Key.TAB)
        wait(2)
        type(Key.ENTER)
        wait(2)
        App.close("Chrome")
        wait(2)
        log.process(mark)


if __name__ == "__main__":
    chrome = Chrome()
    chrome.openChrome()
    chrome.setupProxyChrome()
    chrome.authenticateChrome()
    chrome.cleanupChrome()
