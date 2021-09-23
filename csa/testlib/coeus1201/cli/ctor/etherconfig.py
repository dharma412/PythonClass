#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/etherconfig.py#1 $

"""
IAF 2 CLI command: etherconfig
"""
from sal.exceptions import ConfigError
import clictorbase as ccb
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

    def mtu(self, input_dict=None, **kwargs):
        self._query_response('MTU')
        return etherconfigMtu(self._get_sess())

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

class etherconfigVlan(ccb.IafCliConfiguratorBase):
    """etherconfig -> Vlan"""
    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
                ('\S+ already configured', REGEX) : VlanConfigError
                })

    def new(self, vlan_tag_id=REQUIRED, interface_to_bind=DEFAULT):
        self.level=2
        self._query_response('NEW')
        self._query_response(vlan_tag_id)
        self._query_select_list_item(interface_to_bind)
        self._to_the_top(self.level)

    def edit(self, interface_name=REQUIRED, vlan_tag_id=DEFAULT,
             interface_to_bind=DEFAULT):
        self.level=2
        self._query_response('EDIT')
        self._query_response(interface_name)
        self._query_response(vlan_tag_id)
        self._query_response(interface_to_bind)
        self._to_the_top(self.level)

    def delete(self, input_dict=None, **kwargs):
        if kwargs.has_key('action'):
            kwargs['action'] = 1
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['interface_name']    = \
                                 ['interface you wish to delete', REQUIRED]
        param_map['confirmation']      = \
                                 ['Do you want to continue', DEFAULT]
        param_map['action']            = \
                                 ['What would you like to do', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('DELETE')
        return self._process_input(param_map)

class etherconfigMtu(ccb.IafCliConfiguratorBase):
    """etherconfig -> Mtu"""
    level = 2

    def edit(self, interface_name=DEFAULT, mtu_value=DEFAULT):
        self._query_response('EDIT')
        self._query_response(interface_name)
        self._query_response(mtu_value)
        self._to_the_top(self.level)

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
                       interface_to_bind='1')
    ethc().vlan().delete(interface_name='1')

    ethc().mtu().edit()
    ethc().mtu().edit(interface_name='Management', mtu_value=500)

