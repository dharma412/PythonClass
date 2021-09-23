#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/l4tm.py#1 $

from common.gui.guicommon import GuiCommon

class L4TM(GuiCommon):
    """Keywords for Web Security Manager -> L4 Traffic Monitor
    """

    def get_keyword_names(self):
        return [
                "l4tm_edit",
               ]

    def _open_page(self):
        """
        Navigate to L4 Traffic Monitor configuration page.
        """
        self._navigate_to("Web Security Manager", "L4 Traffic Monitor")


    def l4tm_edit(self,
        malware_action=None,
        allow_list=None,
        block_ambigous=None,
        suspected=None
        ):
        """ Edits L4 Traffic monitor policy

        Parameters:
        - `malware_action`: 'monitor' or 'block'
           These actions will be applied to the list of suspect malware
           addresses provided by the L4 Anti-Malware Rules, and to any
           additional suspect malware addresses listed below.

        - `allow_list`: string of comma separated values
           All destinations and clients in this list will be allowed.
           The destinations will not be checked against the L4 Anti-Malware
           Rules or the additional suspected malware addresses
           (examples: 10.0.0.1, 10.0.0.0/24, host.example.com, example.com)

        - `block_ambiguous`: "True" or "False"
           That options is in effect only when malware_action is 'block'
           An IP address is "ambiguous" if it is referenced by more than one
           hostname, one of which is a known malware site and another an
           unlisted (potentially legitimate) site.
           Use caution when selecting the option to include ambiguous addresses
           when blocking, since it may result in blocking legitimate sites.

        - 'suspected' Additional Suspected Malware Addresses (optional)
           Entries in this list are classified as suspected malware by the L4
           Traffic Monitor, and will be monitored or blocked based on the
           selected Actions for Suspected Malware Addresses.
           If entries in this list are found to be ambiguous, they will not be
           blocked unless the option to include ambiguous addresses when
           blocking is selected.

        Separate multiple entries with whitespace or commas. Valid formats:
        * an IP address
        * a CIDR address such as 10.1.1.0/24
        * a domain name such as example.com (see note below)
        * a hostname such as crm.example.com

        Note: Entering a domain name such as example.com will also match
        www.example.com and hostname.example.com.

        Examples:
        | L4TM Edit |
        | | malware_action=monitor |

        | L4TM Edit |
        | | malware_action=block |
        | | allow_list=10.0.0.1, 10.0.0.0/24, host.example.com, example.com |
        | | block_ambigous=${True} |
        | | suspected=101.11.11.0/24, host2.example2.com |

        | L4TM Edit |
        | | allow_list=10.0.0.1, 10.0.0.0/24, host.example.com, example.com |

        | L4TM Edit |
        | | malware_action=block |
        | | block_ambigous=${True} |
        | | suspected=121.21.12.24, host3.example3.com |

        Exceptions:
        - `Value Error`:Invalid malware_action; should be 'block' or 'monitor'
        """

        self._open_page()

        self._click_edit_settings_button()
        if malware_action is not None:
            self._select_malware_action(malware_action)
        if block_ambigous is not None:
            self._block_ambigous(block_ambigous)
        if allow_list is not None:
            self._fill_allow_list(allow_list)
        if suspected is not None:
            self._fill_suspected(suspected)

        self._click_submit_button()

    def _fill_allow_list(self, allow_list):
        """ Fills in Allow List textbox"""
        if allow_list is None: return

        ALLOW = "id=whitelist_id"

        if isinstance(allow_list, str):
            allow_list = (allow_list,)

        text = ', '.join(self._convert_to_tuple(allow_list))

        self.input_text(ALLOW, text)

        self._info("Allow List filled in with %s" % text)

    def _select_malware_action(self, malware_action):
        """ Selects malware action """
        MONITOR_RADIO_LOC = "id=tm_action_monitor_id"
        BLOCK_RADIO_LOC = "id=tm_action_block_id"

        self._info("Malware action is '%s'" % malware_action)

        if malware_action == "monitor":
            self.click_element(MONITOR_RADIO_LOC, "don't wait")
        elif malware_action == "block":
            self.click_element(BLOCK_RADIO_LOC, "don't wait")
        else:
            raise ValueError, \
            "Invalid malware_action; should be 'block' or 'monitor'"

    def _block_ambigous(self, block_ambigous):
        """ Blocks-unblocks ambigous """
        AMBIGOUS = "id=tm_force_greylist_black"

        self._info("block_ambigous = " + str(block_ambigous))
        if block_ambigous:
            self.select_checkbox(AMBIGOUS)
        else:
            self.unselect_checkbox(AMBIGOUS)

    def _fill_suspected(self, suspected):
        """ Fills in Additional Suspected Malware Addresses textbox"""
        if suspected is None: return

        SUSPECTED = "id=blacklist_id"

        text = ", ".join(self._convert_to_tuple(suspected))

        self.input_text(SUSPECTED, text)

        self._info("Additional Suspected Malware Addresses filled with %s"  \
            % text)

