#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/etherconfig.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
SARF CLI command: etherconfig
"""

import clictorbase as ccb
from sal.exceptions import ConfigError
from sal.deprecated.expect import EXACT, REGEX
REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
from sal.containers.yesnodefault import YES, is_yes
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

    def pairing(self):
        self._query_response('PAIRING')
        return etherconfigPairing(self._get_sess())

    def media_output(self):
        self.clearbuf()
        self._query_response('MEDIA')
        self._to_the_top(2)
        output= self.getbuf()
        return output

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

class etherconfigPairing(ccb.IafCliConfiguratorBase):
    """etherconfig -> pairing"""
    newlines = 2

    def new(self, input_dict=None, **kwargs):
        """
        Create a new pairing.
        """
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['pair_name'] =  ['enter a name for this pair', REQUIRED]
        param_map['interface_to_bind'] = ['interface you wish bind to', REQUIRED]
        param_map['interface_to_pair'] = ['interface you wish to pair', REQUIRED]
        param_map['confirm'] = ['Do you want to continue', DEFAULT]
        param_map['action'] = ['What would you like to do', DEFAULT, 1]
        param_map['choose_interface'] = ['choose a new interface for listener', DEFAULT, 1]
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        return self._process_input(param_map)

    def delete(self):
        """
        Delete a pairing.
        """
        self._query_response('DELETE')
        self._to_the_top(self.newlines)

    def failover(self):
        """
        Manually failover to other port.
        """
        self._query_response('FAILOVER')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.newlines)
        return raw

    def status(self, as_dictionary=YES):
        """
        Refresh status.
        """
        self._query_response('STATUS')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.newlines)
        if is_yes(as_dictionary):
            import re
            primary = re.search('Primary \((?P<interface>.*)\) (?P<state>.*)\, (?P<link_state>.*)', raw)
            backup = re.search('Backup \((?P<interface>.*)\) (?P<state>.*)\, (?P<link_state>.*)', raw)
            return {'primary':primary.groupdict(), 'backup':backup.groupdict()}
        return raw
