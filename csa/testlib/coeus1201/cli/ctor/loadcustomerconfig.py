#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/loadcustomerconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
cli -> loadcustomerconfig

"""
from clictorbase import IafCliConfiguratorBase, IafCliError

class loadcustomerconfig(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._restart()
        self._writeln('loadcustomerconfig')
        return self

    def _load_choice(self, choice):
        self._query_select_list_item(choice)
        return self

    def _load_customerconfig_from_file(self, conf_file):
        self._query_response(conf_file)
        return self

    def _load_customerconfig_from_cli(self, paste_conf):
        self._sess.writeln(paste_conf)
        self._sess.writeln(' ')
        self._sess.write("\x04")
        return self

    def _enter(self, answer):
        self._query_response(answer, timeout=120)
        return self
