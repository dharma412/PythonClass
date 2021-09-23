# $Id: //prod/main/sarf_centos/testlib/BrowserUtilities.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import inspect
import sys
import time
import types

from common.TestLibrary import TestLibrary
from selenium import selenium


class BrowserUtilities(TestLibrary):
    """ Common Browser Utilities Library

    """
    keywords = {}
    sessions = {}

    def get_keyword_names(self):
        keywords = []

        method = inspect.getmembers(BrowserUtilities,
                                    predicate=inspect.ismethod)
        for key, value in BrowserUtilities.__dict__.items():
            if (type(value) == types.FunctionType and
                    not key.startswith('_') and
                    key != 'get_keyword_names'):
                keywords.append(key)

        return keywords

    """
    Go to a specified client and open the desired browser at the given url.
    """

    def open_browser_on_client_at_url(self, sess_id, client='localhost',
                                      port=5555, browser='*firefox',
                                      url='http://www.google.com/'):
        sess_id = int(sess_id)
        port = int(port)
        print 'Opening "{0}" in browser {1} on {2}:{3}'.format(url, browser,
                                                               client, port)
        self.sessions[sess_id] = selenium(client, port, browser, url)
        self.sessions[sess_id].start()

    """
    Go to a specified client and move the desired browser to the given url.
    """

    def move_client_browser_to_url(self, sess_id, url='http://www.google.com/',
                                   timeout='30000', sleep=5):
        sess_id = int(sess_id)
        timeout = str(timeout)
        sleep = int(sleep)
        print url, timeout, sleep
        try:
            self.sessions[sess_id].set_timeout(timeout)
            self.sessions[sess_id].open(url)
            self.sessions[sess_id].window_maximize()
            self.sessions[sess_id].wait_for_page_to_load(timeout)
            time.sleep(sleep)
        except Exception, e:
            print e

    def close_client_browser_session(self, sess_id):
        sess_id = int(sess_id)
        self.sessions[sess_id].stop()
        del self.sessions[sess_id]
