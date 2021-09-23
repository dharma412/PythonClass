# $Id: //prod/main/sarf_centos/testlib/common/sikuli/firefox.sikuli/firefox.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $
import os
import sys
import sikulilog as log
from sikuli.Sikuli import *

firefoxscriptPath = "firefox.sikuli"
addImagePath(firefoxscriptPath)


class Firefox(object):

    def _close(self):
        type("f", KEY_ALT)
        type("x", KEY_CTRL)

    def openFirefox(self):
        mark = log.get_length()
        App.open("Firefox")
        wait(2)
        App.focus("Firefox")
        wait(2)
        log.process(mark)

    def setupProxyFirefox(self, proxyhost=None, port="3128"):
        mark = log.get_length()
        click("Tools.png")
        wait(2)
        type("o", KEY_CTRL)
        click("Advanced.png")
        click("Network.png")
        type("e", KEY_ALT)
        type("m", KEY_ALT)
        type("x", KEY_ALT)
        type(proxyhost)
        type("p", KEY_ALT)
        type(port)
        wait(2)
        click("OK.png")
        wait(2)
        click("OK.png")
        wait(2)
        self._close()
        wait(2)
        log.process(mark)

    def acceptUntrustedCertificateFirefox(self):
        mark = log.get_length()
        App.focus("Firefox")
        wait(2)
        click("IUnderstandt-1.png")
        click("AddException-2.png")
        click("QonfirmSecur.png")
        log.process(mark)

    def authenticateFirefox(self, domain="wga", username="admin",
                            password="ironport"):
        mark = log.get_length()
        App.open("Firefox")
        wait("UserName.png", 5)
        type("UserName.png", "%s\\%s" % (domain, username))
        type(Key.TAB)
        type(password)
        click("OK.png")
        wait(2)
        log.process(mark)

    def cleanupFirefox(self):
        mark = log.get_length()
        click("Tools.png")
        wait(2)
        type("o", KEY_CTRL)
        click("Advanced.png")
        click("Network.png")
        type("e", KEY_ALT)
        type("y", KEY_ALT)
        click("OK.png")
        wait(2)
        click("OK.png")
        wait(2)
        self._close()
        wait(2)
        log.process(mark)


if __name__ == "__main__":
    firefox = Firefox()
    firefox.openFirefox()
    firefox.setupProxyFirefox()
    firefox.authenticateFirefox()
    firefox.cleanupFirefox()
    firefox.acceptUntrustedCertificateFirefox()
