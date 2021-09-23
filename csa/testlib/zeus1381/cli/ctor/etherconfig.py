#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/etherconfig.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

"""
CLI command: etherconfig
"""

import clictorbase as ccb
from sal.exceptions import ConfigError
from sal.deprecated.expect import EXACT, REGEX
REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
DEBUG = True

class InterfaceStatusError(ccb.IafCliError): pass
class VlanConfigError(ccb.IafCliError): pass

class etherconfig(ccb.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('etherconfig')
        return self

    def media(self):
        self._query_response('MEDIA')
        return etherconfigMedia(self._get_sess())

    def vlan(self):
        self._query_response('VLAN')
        return etherconfigVlan(self._get_sess())

    def loopback(self):
        self._query_response('LOOPBACK')
        return etherconfigLoopback(self._get_sess())

    def mtu(self):
        self._query_response('MTU')
        return etherconfigMtu(self._get_sess())

class etherconfigLoopback(ccb.IafCliConfiguratorBase):
    """etherconfig -> Loopback"""
    newlines = 2

    def enable(self):
        self._query_response('ENABLE')
        self._to_the_top(self.newlines)

    def disable(self, sure=DEFAULT):
        self._query_response('DISABLE')
        self._query_response(sure)
        self._to_the_top(self.newlines)

class etherconfigMedia(ccb.IafCliConfiguratorBase):
    """etherconfig -> Media"""
    def edit(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['interface_name']     = \
                                 ['interface you wish to edit', REQUIRED]
        param_map['media_option']       = \
                                 ['Ethernet media options', DEFAULT, True]
        param_map['confirmation']       = \
                                 ['sure you want to change it', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('EDIT')
        return self._process_input(param_map)

class etherconfigMtu(ccb.IafCliConfiguratorBase):
    """etherconfig -> MTU"""
    level=2

    def edit(self, interface_name=REQUIRED, mtu_value=DEFAULT):
        self._query_response('EDIT')
        self._query_response(interface_name)
        self._query_response(mtu_value)
        self._to_the_top(self.level)

class etherconfigVlan(ccb.IafCliConfiguratorBase):
    """etherconfig -> Vlan"""
    newlines = 2

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
                ('\S+ already configured', REGEX) : VlanConfigError
                })

    def new(self, vlan_tag_id=REQUIRED, interface_to_bind=DEFAULT):
        self._query_response('NEW')
        self._query_response(vlan_tag_id)
        self._query_select_list_item(interface_to_bind)
        self._to_the_top(self.newlines)

    def edit(self, interface_name=REQUIRED, vlan_tag_id=DEFAULT,
        interface_to_bind=DEFAULT):
        self._query_response('EDIT')
        self._query_response(interface_name)
        self._query_response(vlan_tag_id)
        self._query_response(interface_to_bind)
        self._to_the_top(self.newlines)

    def delete(self, vlan_name):
        self._query_response('DELETE')
        self._query_response(vlan_name)
        self._to_the_top(self.newlines)


if __name__ == '__main__':
    dev_mode = False
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
        dev_mode = True
    except NameError:
        cli_sess = ccb.get_sess()
    ethc = etherconfig(cli_sess)

    ethc().media().edit(interface_name='2', media_option='10baseT/UTP full')
    ethc().media().edit(interface_name='2', media_option='Auto')

    ethc().vlan().new(vlan_tag_id='14')
    ethc().vlan().edit(interface_name='1', vlan_tag_id='2',
                       interface_to_bind='2')
    ethc().vlan().delete(interface_name='1')

    ethc().loopback().enable()
    ethc().loopback().disable(loopback_status='NO')
    ethc().loopback().disable(loopback_status='YES')

    ethc().mtu().edit(interface_name='Management',mtu_value='500')
