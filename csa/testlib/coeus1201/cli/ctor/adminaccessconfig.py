#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/adminaccessconfig.py#1 $

"""
SARF CLI command: adminaccessconfig
"""

import clictorbase
import sal.containers.yesnodefault as yesnodefault
from sal.deprecated.expect import REGEX

class adminaccessconfig(clictorbase.IafCliConfiguratorBase):

    newlines = 1

    class NonExistedFileError(clictorbase.IafCliError):
        pass

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Error: the file ".+?" does not exist.', REGEX): \
             self.NonExistedFileError })

    def __call__(self):
        self._writeln('adminaccessconfig')
        return self

    def banner(self, load_method = 'pasting', banner_str = None,
               filename = None):

        self._query_response('BANNER')
        entry = int(self._query_select_list_item(load_method))
        if entry == 1:      # Paste via CLI
            self._sess.writeln(banner_str)
            self._sess.write("\x04")    # ^D (CTRL-D)
        if entry == 2: # Load from file
            self._query_response(filename)
        self._to_the_top(self.newlines)

    def ipaccess(self):
        self._query_response('IPACCESS')
        return ipaccessAdminaccessconfig(self._get_sess())

    def strictssl(self, implement = clictorbase.DEFAULT):
        self._query_response('STRICTSSL')
        self._query_response(implement)
        self._to_the_top(self.newlines)

    def timeout(self, timeout=30):
        self._query_response('TIMEOUT')
        self._sess.writeln(timeout)
        self._to_the_top(self.newlines)

    def how_tos(self):
        self._query_response('HOW-TOS')
        return HowTosAdminAccessConfig(self._get_sess())


class ipaccessAdminaccessconfig(clictorbase.IafCliConfiguratorBase):

    newlines = 2

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def allowall(self):
        self._query_response('ALLOWALL')
        self._to_the_top(self.newlines)

    def restricted(self):
        self._query_response('RESTRICTED')
        return restrictIpaccessAdminaccessconfig(self._get_sess())

class restrictIpaccessAdminaccessconfig(clictorbase.IafCliConfiguratorBase):

    newlines = 3

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def new(self, ip = clictorbase.REQUIRED):
        self._query_response('NEW')
        self._query_response(ip)
        self._to_the_top(self.newlines)

    def edit(self, old_ip = clictorbase.REQUIRED,
             new_ip = clictorbase.REQUIRED):
        self._query_response('EDIT')
        self._select_list_item(old_ip, self._sess.getbuf(clear_buf = False))
        self._query_response(new_ip)
        self._to_the_top(self.newlines)

    def delete(self, ip = clictorbase.REQUIRED):
        self._query_response('DELETE')
        self._select_list_item(ip, self._sess.getbuf(clear_buf = False))
        self._to_the_top(self.newlines)

    def clear(self, ip = clictorbase.REQUIRED):
        self._query_response('CLEAR')
        self._to_the_top(self.newlines)

class HowTosAdminAccessConfig(clictorbase.IafCliConfiguratorBase):

    newlines =2

    def __init__(self,  sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def enable(self):
        self._query_response('Y')
        self._to_the_top(self.newlines)

    def disable(self):
        self._query_response('N')
        self._to_the_top(self.newlines)

    def status(self):
        self.clearbuf()
        self._query_response('\n')
        self._to_the_top(self.newlines)
        return self._sess.getbuf()
