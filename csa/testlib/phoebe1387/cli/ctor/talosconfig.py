#!/usr/bin/env python
import clictorbase as ccb
from curses.ascii import ctrl
import re

class talosconfig(ccb.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self,server):
        self._query_response('setup')
        self._query_select_list_item(server)
        self._to_the_top(1)

    def customserver(self, url):
        self._query_response('customserver')
        self._query_response(url)
        self._to_the_top(1)

    def status(self):
        self.clearbuf()
        self._query_response('setup')
        self._query_response()
        self._sess.write(ctrl('c'))
        self._to_the_top(1)
        talosconfig_output = self.getbuf()
        self._debug(talosconfig_output)
        production_server = re.search('Configured server is: production_server', \
        talosconfig_output)
        if production_server :
            return 'production_server'
        else:
            return 'stage_server'

        self._to_the_top(1)
        return server
