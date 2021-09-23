#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/routeconfig.py#3 $

"""
IAF 2 CLI command: routeconfig
"""

import clictorbase
from clictorbase import REQUIRED, DEFAULT, IafCliParamMap
from sal.exceptions import ConfigError

class routeconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def __call__(self):
        self._writeln('routeconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['name']      = ['create a name', REQUIRED]
        param_map['dest']      = ['enter the destination IP', REQUIRED]
        param_map['gateway']   = ['enter the gateway IP', REQUIRED]
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):

        # convert route_to_edit argument from a string to a number
        # if necessary as no names are allowed for this question in the CLI
        if kwargs.get('route_to_edit'):
            route_to_edit = kwargs['route_to_edit']
        elif input_dict.get('route_to_edit'):
            route_to_edit = input_dict['route_to_edit']
        else:
            raise ConfigError, "routeconfig->edit: route_to_edit is"\
                               "a required value"

        # if an integer, use route_to_edit as is.
        # otherwise figure out which entry corresponds to the route
        try:
            int(route_to_edit)
        except ValueError:
            pt = self._input_list_obj.parse_text(self.getbuf())
            for kk in pt.keys():
                if pt[kk].find(route_to_edit) > -1:
                    if kwargs:
                        kwargs['route_to_edit'] = kk
                    else:
                        input_dict['route_to_edit'] = kk
                    break
        else:
            pass

        self._query_response('EDIT')

        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['route_to_edit'] = ['number of the route', REQUIRED]
        param_map['name']          = ['name for the route', DEFAULT]
        param_map['dest']          = ['enter the destination IP', DEFAULT]
        param_map['gateway']       = ['enter the gateway IP', DEFAULT]
        param_map.update(input_dict or kwargs)

        return self._process_input(param_map)

    def delete(self, route_to_delete='1'):
        self._query_response('DELETE')
        # no names allowed, select list item based on name if necessary
        idx = self._select_list_item(route_to_delete,
                                     self._sess.getbuf(clear_buf=False))
        self._to_the_top(self.newlines)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.newlines)

    def print_routes(self):
        self._to_the_top(1)
        self._writeln('routeconfig print')
        return self._wait_for_prompt()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    rc = routeconfig(cli_sess)
    rc().new(name='blah', dest='192.168.42.0/24', gateway='192.168.42.1')
    rc().edit(route_to_edit='blah', dest='192.168.43.0/24',
              gateway='192.168.43.1')
    rc().delete(route_to_delete='blah')
    rc().new(name='blah', dest='192.168.42.0/24', gateway='192.168.42.1')
    rc().clear()

