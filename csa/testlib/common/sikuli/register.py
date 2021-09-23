# $Id: //prod/main/sarf_centos/testlib/common/sikuli/register.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import imp
import sys
from robotremoteserver import RobotRemoteServer

firefox = imp.load_source('firefox.sikuli', 'firefox.sikuli//firefox.py')
chrome = imp.load_source('chrome.sikuli', 'chrome.sikuli//chrome.py')
safari = imp.load_source('safari.sikuli', 'safari.sikuli//safari.py')
ie = imp.load_source('ie.sikuli', 'ie.sikuli//ie.py')


class Register(firefox.Firefox, chrome.Chrome, safari.Safari, ie.Ie):
    """
    Library for invoking sikuli scripts remotely
    """


if __name__ == '__main__':
    RobotRemoteServer(Register(), *sys.argv[1:])
