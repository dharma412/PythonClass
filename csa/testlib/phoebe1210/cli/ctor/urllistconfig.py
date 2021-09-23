#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/urllistconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import clictorbase
import shlex
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap
from sal.deprecated.expect import REGEX

from sal.containers.yesnodefault import YES, NO


class urllistconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('urllistconfig')
        return self

    def newwithoutimport(self, urllist_name, urldomain_name):
        domain = shlex.split(urldomain_name)
        self._query_response('NEW')
        self._query_response('\n')
        self._query_response(urllist_name)
        for list in domain:
            self._writeln(list)
        self._query_response('.' + '\n')
        self._query_response('\n')

        return self

    def newwithimport(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        self._query_response('NEW')
        param_map['import_urllist'] = ['Do you want to import a URL list', REQUIRED]
        param_map['assign_newname'] = ['Assign new name to list', DEFAULT]
        param_map['urllist_newname'] = ['Enter name of URL list', REQUIRED]
        param_map['urllist_imported'] = ['Enter the name of the file on machine', REQUIRED]

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def edit(self, urllist_to_edit='1', input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='- EDIT -')

        self._query_response('EDIT')
        param_map['option'] = ['Choose the operation you want to perform:', REQUIRED]
        param_map['urllist_rename'] = ['Enter the number of URL list to rename', REQUIRED]
        param_map['urllist_name'] = ['Enter new name for the URL list', REQUIRED]
        param_map['assign_newname'] = ['Assign new name to list', DEFAULT]
        param_map['urllist_newname'] = ['Enter name of URL list', REQUIRED]
        param_map['urllist_imported'] = ['Enter the name of the file on machine', REQUIRED]
        param_map['urllist_number'] = ['Enter the number of URL list to export', REQUIRED]
        param_map['urllist_exported'] = ['Enter a name for the exported file:', REQUIRED]

        param_map.update(input_dict or kwargs)
        result = self._process_input(param_map, do_restart=False)
        self._to_the_top(1)
        return result

    def delete(self, urllist_to_delete='1'):
        self._query_response('DELETE')
        self._query_response(urllist_to_delete)
        self._to_the_top(1)
