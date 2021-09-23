#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/ether_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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
                'ether_config_mtu_edit',
                'ether_config_pairing_new',
                'ether_config_pairing_delete',
                'ether_config_pairing_status',
                'ether_config_pairing_failover', ]

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

    def ether_config_pairing_new(self, *args):
        """Create a new pairing..

        Parameters:
        - `pair_name`: A name for the pair. Required.
        - `interface_to_bind`: The name or number of the primary ethernet interface to bind to.
        - `confirm`: Confirm if an interface for the NIC Pair is configured with one or more IP addresses. YES or NO.
        - `action`: The action to choose if there is listener configured on interface.
        | 1 | Delete: Remove the listener and all its settings |
        | 2 | Change: Choose a new interface |
        | 3 | Ignore: Leave the listener configured for interface |
        - `choose_interface`: Interface for listener if `action` is _2_.

        Examples:
        | Ether Config Pairing New | pair_name=pair1 | interface_to_bind=data 1 |
        | Ether Config Pairing New | pair_name=pair1 | interface_to_bind=1 | confirm=yes | action=delete |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.etherconfig().pairing().new(**kwargs)

    def ether_config_pairing_delete(self):
        """Delete a pairing.

        Parameters:
        None

        Return:
        None

        Examples:
        | Ether Config Pairing Delete |
        """
        self._cli.etherconfig().pairing().delete()

    def ether_config_pairing_status(self, *args):
        """Refresh pairing status.

        Parameters:
        - `as_dictionary`: Format result as dictionary. YES or NO.

        Return:
        Dictionary or String(raw output).
        Dictionary:
        | Dictionary | Keys |
        | primary | interface |
        |         | state |
        |         | link state |
        | backup  | interface |
        |         | state |
        |         | link state |

        Examples:
        | Ether Config Pairing Status |

        | Ether Config Pairing Status | as_dictionary=no |

        | ${status}= | Ether Config Pairing Status |
        | Log Dictionary | ${status} |
        | ${primary}= | Get From Dictionary | ${status} | primary |
        | ${backup}= | Get From Dictionary | ${status}  backup |
        | Log | ${primary} |
        | Log | ${backup} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.etherconfig().pairing().status(**kwargs)

    def ether_config_pairing_failover(self):
        """Manually failover to other port.

        Parameters:
        None

        Return:
        None

        Examples:
        | Ether Config Pairing Failover |
        """
        self._cli.etherconfig().pairing().failover()
