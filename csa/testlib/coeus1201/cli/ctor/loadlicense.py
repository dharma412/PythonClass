#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/loadlicense.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
cli -> loadlicense

"""
from clictorbase import IafCliConfiguratorBase
import re

class loadlicense(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._restart()
        self.isLicensed = self._is_licensed()
        return self

    def _is_licensed(self):
        self._writeln('showlicense')
        license_status = self._wait_for_prompt()
        if re.search('No License Installed', license_status):
            self._writeln('loadlicense')
            return False
        else:
            self._writeln('loadlicense')
            self._query_response('Y')
            return True

    def _load_license_from_file(self, filename):
        self._query_select_list_item('Load from file')
        self._query_response(filename)
        try:
            #It can be EULA or not
            eula_text = self._wait_for_prompt()
        except:
            # If it is an EULA agreement
            self._writeln('Y')
            eula_text = self._wait_for_prompt()
        return eula_text


    def _load_license_from_cli(self, paste_conf):
        self._query_select_list_item('Paste via CLI')
        self._sess.writeln(paste_conf)
        self._sess.writeln(' ')
        self._sess.write("\x04")
        try:
            #It can be EULA or not
            eula_text = self._wait_for_prompt()
        except:
            # If it is an EULA agreement
            self._writeln('Y')
            eula_text = self._wait_for_prompt()
        return eula_text