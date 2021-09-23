#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/guiexceptions.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $
""" Customized exceptions."""
from __future__ import absolute_import


class GuiError(Exception): pass  # Page is available


class DutError(Exception): pass  # Page is missing


class TimeoutError(Exception): pass


class ConfigError(Exception): pass


class SeleniumClientException(Exception): pass


class GuiProxyNotConfiguredError(GuiError): pass


class GuiFeatureDisabledError(GuiError): pass


class GuiFeaturekeyMissingError(GuiFeatureDisabledError): pass


class DutGuiError(DutError): pass


class GuiTimeoutError(DutGuiError): pass


class GuiPageNotFoundError(DutGuiError): pass


class GuiAppFault(DutGuiError): pass


class GuiTracebackError(GuiAppFault): pass


class GuiApplicationError(GuiAppFault): pass


class GuiAuthorizationRequiredError(DutGuiError): pass


class GuiLoginFailureError(Exception): pass


class GuiValueError(GuiError):
    """ Incorrect values were entered to the page """

    # The special exception the product page validator
    def __init__(self, msg, page_errors=None):
        self.msg = msg
        if page_errors:
            self.page_errors = page_errors
        else:
            self.page_errors = list()

    def __str__(self):
        return str(self.msg) + ':\n\n' + '\n'.join(map(str, self.page_errors))

    # used by Robot Framework to print message to console and log
    def __unicode__(self):
        return unicode(self.__str__())


class GuiControlNotFoundError(GuiError):
    """ Alerts that searched control is not available on the page
    """

    def __init__(self, control, page):
        self.page = page
        self.control = control

    def __str__(self):
        return 'Control "%s" is not found/available on the page "%s"' % (self.control, self.page)


class TestError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'Test completed: %s' % (self.msg,)


class AsaTestError(TestError): pass


class AuthTestError(TestError): pass


class ExternalDLPTestError(TestError): pass


class InvalidUrlPathError(Exception): pass
