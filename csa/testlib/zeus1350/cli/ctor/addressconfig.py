#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/addressconfig.py#1 $
"""
IAF2 CLI command addressconfig
"""

from sal.containers.yesnodefault import YES, NO
import clictorbase

DEFAULT = clictorbase.DEFAULT


class addressconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def _addressconfig_edit(self, oper, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['display_name'] = ['enter the display name portion',
                                     DEFAULT]
        param_map['user_name'] = ['enter the user name portion', DEFAULT]
        param_map['use_hostname'] = \
            ['use the system hostname for the domain portion?',
             DEFAULT]
        param_map['domain_name'] = \
            ['enter the domain name portion of the', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response(oper)
        return self._process_input(param_map)

    # TODO: After update to python 2.4+ make use of real decorators
    def bouncefrom(self, input_dict=None, **kwargs):
        self._addressconfig_edit(oper='BOUNCEFROM', input_dict=None, **kwargs)

    def reportsfrom(self, input_dict=None, **kwargs):
        self._addressconfig_edit(oper='REPORTSFROM', input_dict=None, **kwargs)

    def otherfrom(self, input_dict=None, **kwargs):
        self._addressconfig_edit(oper='OTHERFROM', input_dict=None, **kwargs)


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ac = addressconfig(cli_sess)

    ac().bouncefrom(display_name='disp name', user_name='username',
                    use_hostname=NO, domain_name='somedomain.com')
    ac().reportsfrom(display_name='disp name', user_name='username',
                     use_hostname=NO, domain_name='somedomain.com')
    ac().otherfrom(display_name='disp name', user_name='username',
                   use_hostname=NO, domain_name='somedomain.com')
