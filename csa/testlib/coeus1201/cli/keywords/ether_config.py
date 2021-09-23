#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/ether_config.py#1 $

from common.cli.clicommon import CliKeywordBase

class EtherConfig(CliKeywordBase):
    """Configure Ethernet settings."""

    def get_keyword_names(self):
        return [
            'ether_config_media_edit',
            'ether_config_vlan_new',
            'ether_config_vlan_edit',
            'ether_config_vlan_delete',
            'ether_config_mtu_edit',
        ]

    def ether_config_media_edit(self,
                                interface_name,
                                media_option=''):
        """Edit ethernet media settings.

        etherconfig > media > edit

        Parameters:
        - `interface_name`: name or number of the ethernet interface you wish to
        edit. Available interfaces:
        | 1 | M2 |
        | 2 | Management |
        | 3 | P1 |
        | 4 | P2 |
        | 5 | T1 |
        | 6 | T2 |
        - `media_option`: number of Ethernet media option for the interface.
        Available options:
        | 1 | Autoselect |
        | 2 | 10baseT/UTP half-duplex |
        | 3 | 10baseT/UTP full-duplex |
        | 4 | 100baseTX half-duplex |
        | 5 | 100baseTX full-duplex |
        | 6 | 1000baseTX half-duplex |
        | 7 | 1000baseTX full-duplex |
        Default value 1.

        Example:
        | Ether Config Media Edit | 1 | media_option=1 |

        | Ether Config Media Edit | 2 |
        """

        kwargs = {'interface_name':interface_name,
                  }
        if media_option:
            kwargs['media_option'] = media_option

        output = self._cli.etherconfig().media().edit(**kwargs)
        return(output)

    def ether_config_vlan_new(self, vlan_tag_id, interface_to_bind=''):
        """Create a new VLAN.

        etherconfig > vlan > new

        Parameters:
        - `vlan_tag_id`: VLAN tag ID for the interface. Number from 1 to 4094.
        - `interface_to_bind`: name or number of the ethernet interface you wish
        bind to. Available interfaces:
        | 1 | M2 |
        | 2 | Management |
        | 3 | P1 |
        | 4 | P2 |
        | 5 | T1 |
        | 6 | T2 |
        Default value 1.

        Examples:
        | Ether Config Vlan New | 555 | interface_to_bind=1 |

        | Ether Config Vlan New | 333 |
        """

        self._cli.etherconfig().vlan().new(vlan_tag_id, interface_to_bind)

    def ether_config_vlan_edit(self,
                               interface_name,
                               vlan_tag_id='',
                               interface_to_bind=''):
        """Create a new VLAN.

        etherconfig > vlan > edit

        Parameters:
        - `interface_name`: interface you wish to edit.
        - `vlan_tag_id`: new VLAN tag ID for the interface. Optional.
        - `interface_to_bind`: name or number of the ethernet interface you wish
        bind to. Available interfaces:
        | 1 | M2 |
        | 2 | Management |
        | 3 | P1 |
        | 4 | P2 |
        | 5 | T1 |
        | 6 | T2 |
        Default value 1.

        Examples:
        | Ether Config Vlan Edit | 555 | vlan_tag_id=33 | interface_to_bind=1 |

        | Ether Config Vlan Edit | 33 | interface_to_bind=5 |
        """

        self._cli.etherconfig().vlan().edit(interface_name,
                                            vlan_tag_id,
                                            interface_to_bind)

    def ether_config_vlan_delete(self, interface_name):
        """Create a new VLAN.

        etherconfig > vlan > delete

        Parameters:
        - `interface_name`: VLAN tag ID for the interface you wish to delete.

        Example:
        | Ether Config Vlan Delete | 555 |
        """

        kwargs = {'interface_name':interface_name}
        self._cli.etherconfig().vlan().delete(**kwargs)

    def ether_config_mtu_edit(self, interface_name, mtu_value=''):
        """Configure MTU for ethernet interfaces.

        etherconfig > mtu > edit

        Parameters:
        - `interface_name`: the name or number of the ethernet interface you
        wish to edit. Available interfaces:
        | 1 | M2 |
        | 2 | Management |
        | 3 | P1 |
        | 4 | P2 |
        | 5 | T1 |
        | 6 | T2 |
        - `mtu_value`: MTU value for selected interface. Number from 72 to 1500.
        Example:
        | Ether Config MTU Edit | 1 | mtu_value=500 |

        | Ether Config MTU Edit | 1 |
        """

        self._cli.etherconfig().mtu().edit(interface_name, mtu_value)
