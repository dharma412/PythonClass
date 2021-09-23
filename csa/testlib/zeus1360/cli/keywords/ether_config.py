#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/ether_config.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class EtherConfig(CliKeywordBase):

    """Keywords for etherconfig CLI command."""

    def get_keyword_names(self):
        return ['ether_config_media_edit',
                'ether_config_vlan_new',
                'ether_config_vlan_edit',
                'ether_config_vlan_delete',
                'ether_config_loopback_enable',
                'ether_config_loopback_disable',
                'ether_config_mtu_edit']


    def ether_config_media_edit(self, interface_name, media_option=DEFAULT):
        """Edit Ethernet media settings.

        Parameters:
        - `interface_name`: name or number of the Ethernet interface to edit.
        - `media_option`: Ethernet media option for the interface.

        Examples:
        | Ether Config Media Edit | Data 2 | 100baseTX full-duplex |
        | Ether Config Media Edit | 1 | media_option=1 |
        | Ether Config Medit Edit | Management | media_option=1 |
        """
        self._cli.etherconfig().media().edit(
            interface_name=interface_name,
            media_option=media_option)

    def ether_config_vlan_new(self, tag_id, interface_name=DEFAULT):
        """Add a new VLAN.

        Parameters:
        - `tag_id`: VLAN tag ID for the interface.
        - `interface_name`: name or number of the ethernet interface to bind
           to.

        Examples:
        | Ether Config VLAN New | 34 | Management |
        | Ether Config VLAN New | 12 |
        """
        self._cli.etherconfig().vlan().new(tag_id, interface_name)

    def ether_config_vlan_edit(self, vlan_num, tag_id=DEFAULT,
        interface_name=DEFAULT):
        """Edit a VLAN.

        Parameters:
        - `vlan_num`: the number of the VLAN interface to edit.
        - `tag_id`: VLAN tag ID for the interface.
        - `interface_name`: name or number of the ethernet interface to bind
           to.

        Examples:
        | Ether Config VLAN Edit | 1 | 37 | Data 2 |
        | Ether Config VLAN Edit | 1 | interface_name=1 |
        """
        self._cli.etherconfig().vlan().edit(vlan_num, tag_id, interface_name)

    def ether_config_vlan_delete(self, vlan_num):
        """Delete a VLAN.

        Parameters:
        - `vlan_num`: the number of the VLAN interface to delete.

        Examples:
        | Ether Config VLAN Delete | 1 |
        """
        self._cli.etherconfig().vlan().delete(vlan_num)

    def ether_config_loopback_enable(self):
        """Enable loopback interface.

        Examples:
        | Ether Config Loopback Enable |
        """
        self._cli.etherconfig().loopback().enable()

    def ether_config_loopback_disable(self, confirm=DEFAULT):
        """Disable loopback interface.

        Parameters:
        - `confirm`: confirm looback interface deactivation.

        Examples:
        | Ether Config Loopback Disable |
        | Ether Config Loopback Disable | no |
        """
        self._cli.etherconfig().loopback().disable(
            self._process_yes_no(confirm))

    def ether_config_mtu_edit(self, interface_name, mtu=DEFAULT):
        """Configure MTU.

        Parameters:
        - `interface_name`: name of the interface to set MTU for.
        - `mtu`: MTU value for the interface.

        Examples:
        | Ether Config MTU Edit | Data 2 |
        | Ether Config MTU Edit | Management | 1400 |
        """
        self._cli.etherconfig().mtu().edit(interface_name, mtu)


