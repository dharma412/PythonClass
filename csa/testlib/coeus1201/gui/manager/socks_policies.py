#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/socks_policies.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from policybase import PolicyBase

class SOCKSPolicies(GuiCommon, PolicyBase):

    """GUI configurator for 'Web Security Manager -> SOCKS Policies' page.
    """

    policy_name_column = 2
    destination_ports_column = 3
    destination_urls_column = 4
    delete_column = 5

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return [
            'socks_policies_add',
            'socks_policies_delete',
            'socks_policies_edit',
            'socks_policies_edit_destination_ports',
            'socks_policies_edit_destination_urls',
                ]

    def _open_page(self):
        locator = 'xpath=//div[@class="text-info"]'
        self._navigate_to('Web Security Manager', 'SOCKS Policies')
        if self._is_element_present(locator):
            txt = self.get_text(locator)
            if 'SOCKS Policies are currently disabled' in txt:
                raise guiexceptions.GuiFeatureDisabledError(txt)

    def socks_policies_add(self,
        name,
        description=None,
        order=None,
        identities=None,
        proxy_ports=None,
        subnets=None,
        time_range=None,
        match_time_range=True,
        ):
        """Adds new socks policy.

        Parameters:
        - `name`: name of socks policy.
        - `description`: description for socks policy.
        - `order`: order of socks policy.
        - `identities`: a string of comma separated values of identity groups to
        apply to this policy, where each identity is presented in the following
        format (see identities specification document.)
        - `proxy_ports`: membership is defined by proxy ports. String of comma
        separated values of proxy ports.
        - `subnets`: string of comma separated values of one or more subnet
        where policy is a member.
        - `time_range`: time range where policy is a member.
        - `match_time_range`: specify whether a policy group should apply to the
                              times inside or outside the selected time range.
                              Defaulted to True. Otherwise False.

        Examples:
        - | SOCKS Policies Add | myDefaultDecrPol | description=This policy uses Global Identification Profile | identities=Global Identification Profile |
        - | SOCKS Policies Add | myOtherDecrPol | description=This policy uses specified identity | identities=myID:authenticated |
        - | SOCKS Policies Add | myOtherDecrPol | description=This policy uses specified identity | identities=myID:selected:jsmith |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        """

        self._open_page()
        if self._is_element_present('xpath=//table[@class="cols"]/tbody'
            '/tr/td/a[substring-after(@href, "%s")="%s"]' % \
            (name, name)):
            raise guiexceptions.ConfigError('SOCKS group with the '
                                            'name %s already exists.' % name)
        self._click_add_policy_button()
        self._fill_policy_page(name, description, order)

        if identities:
            self._edit_identity_membership(identities)
        self._edit_advanced_settings(
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_range=match_time_range,
            )

        self._click_submit_button()

    def socks_policies_delete(self, name):
        """Deletes specified socks policy.

        Parameters:
        - `name`: name of socks policy to be deleted.

        Example:
        - | SOCKS Policies Delete | myDecrPol |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        """

        self._open_page()
        self._delete_policy(name, self.delete_column)

    def socks_policies_edit(self,
        name,
        new_name=None,
        description=None,
        order=None,
        identities=None,
        proxy_ports=None,
        subnets=None,
        time_range=None,
        match_time_range=True,
        ):
        """Edits socks policy.

        Parameters:
        - `name`: name of socks policy group to edit.
        - `new_name`: new name for socks policy.
        - `description`: description for socks policy.
        - `order`: order of socks policy.
        - `identities`: string of comma separated values of identity groups to
        apply to this policy, where each identity is presented in the following
        format (see identities specification document.)
        - `proxy_ports`: membership is defined by proxy ports. string of comma
        separated values of proxy ports.
        - `subnets`: string of comma separated values of one or more subnet
        where policy is a member.
        - `time_range`: time range where policy is a member.
        - `match_time_range`: specify whether a policy group should apply to the
                              times inside or outside the selected time range.
                              Defaulted to True. Otherwise False.

        Examples:
        - | SOCKS Policies Edit | myDecrPol | identities=All Identities:selected:joe.smith |
        - | SOCKS Policies Edit | myDecrPol | identities=All Identities:all | time_range=myTime | proxy_ports=3128 |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        """

        self._open_page()
        self._click_edit_policy_link(name, self.policy_name_column)
        if any((new_name, description, order)):
            self._fill_policy_page(new_name, description, order)
        if identities:
            self._edit_identity_membership(identities)

        self._edit_advanced_settings(
            proxy_ports=proxy_ports,
            subnets=subnets,
            time_range=time_range,
            match_range=match_time_range,
            )
        self._click_submit_button(wait=False)

    def socks_policies_edit_destination_ports(self,
        name,
        ports_settings=None,
        tcp_ports=None,
        udp_ports=None,
        ):
        """Edits SOCKS connections to destination ports.
        Specifies lists of outbound port numbers or ranges

        Parameters:
        - `ports_settings`: type of settings; accepted values: global and custom
        - `tcp_ports`: list of outbound port numbers or ranges separated
        by comma(s). A port must be a number from 1 to 65535.
        - `udp_ports`: list of outbound port numbers or ranges separated
        by comma(s). A port must be a number from 1 to 65535.

        Examples:
        - | ${id1} | Set Variable | myPolicy |

        - | SOCKS Policies Edit Destination Ports | ${id1} |
        - | ... | ports_settings=custom |
        - | ... | tcp_ports=1000, 1001, 1002-1005 |
        - | ... | udp_ports=2000-3000, 2 |

        - | SOCKS Policies Edit Destination Ports | ${id1} |
        - | ... | ports_settings=global |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        - ValueError: ports_settings should be 'global' or 'custom'
        """

        self._open_page()

        self._click_edit_policy_link(name, self.destination_ports_column)

        if ports_settings is not None:
            self._set_ports_settings(ports_settings)

        if tcp_ports is not None:
            self._set_tcp_ports(tcp_ports)

        if udp_ports is not None:
            self._set_udp_ports(udp_ports)

        self._click_submit_button()

    def  _set_ports_settings(self, value):
        SELECT = "xpath=//select[@name='settings_type']"
        map = {"global": "use_global",
               "custom": "custom",
               }
        if not value in map.keys():
            raise ValueError("ports_settings should be 'global' or 'custom'")
        self.select_from_list(SELECT, map[value])

    def  _set_tcp_ports(self, value):
        FIELD = "xpath=//input[@name='tcp_ports']"
        self.input_text(FIELD, value)

    def  _set_udp_ports(self, value):
        FIELD = "xpath=//input[@name='udp_ports']"
        self.input_text(FIELD, value)

    def socks_policies_edit_destination_urls(self,
        name,
        setting_type=None,
        specified_url_categories=None,
        ):
        """Edits Destination URLs / IP Addresses for socks policy.

        Parameters:
        - `name`: name of socks policy group to edit.
        - `setting_type`:
        .    'global' - Use Destinations Global Policy Settings
        .    'block_all' - Do not allow SOCKS connections to any URL or IP Address
        .    'allow_all' - Allow SOCKS connections to any URL or IP Address
        .    'allow_specified' - Allow SOCKS connections only to specified list of
        specified URL categories
        - `specified_url_categories`: 'all' or - comma-separated list of specified
         URL categories

        Examples:
        - | SOCKS Policies Edit Destination Urls | ${ID1} | setting_type=global |
        - | SOCKS Policies Edit Destination Urls | ${ID1} | setting_type=block_all |
        - | SOCKS Policies Edit Destination Urls | ${ID1} | setting_type=allow_all |
        - | SOCKS Policies Edit Destination Urls | ${ID1} | setting_type=allow_specified | specified_url_categories=all |
        - | SOCKS Policies Edit Destination Urls | ${ID1} | setting_type=allow_specified | specified_url_categories=cats, dogs |

        Exceptions:
        - GuiFeatureDisabledError:SOCKS Policies are currently disabled
        - ConfigError:Setting type 'XXX' should be in
        ['global','block_all',allow_all','allow_specified']
        """

        self._open_page()

        self._click_edit_policy_link(name, self.destination_urls_column)

        if setting_type is not None:
            self._select_url_setting_type(setting_type)

        if specified_url_categories is not None:
            self._set_specified_urls(
                self._convert_to_tuple(specified_url_categories))

        self._click_submit_button()

    def _select_url_setting_type(self, option):
        setting_types = {
            'global' : '',
            'block_all' : 'xpath=//input[@id="scan_enabled_none"]',
            'allow_all' : 'xpath=//input[@id="scan_enabled_all"]',
            'allow_specified' : 'xpath=//input[@id="scan_enabled_specified"]',
            }

        global_settings = "Use Destinations Global Policy Settings"
        specified_settings = "Define Destinations Custom Settings"
        list = "xpath=//select[@id='settings_type']"

        if not option in setting_types.keys():
            raise guiexceptions.ConfigError(
                "Setting type '%s' should be in " % option \
                + str(setting_types.keys()))

        if option == 'global':
            self.select_from_list(list, global_settings)
        else:
            self.select_from_list(list, specified_settings)
            self._click_radio_button (setting_types[option])

    def _set_specified_urls(self, list):
        edit_list = 'xpath=//a[@id="edit_custom_categories_list"]'
        select_all = 'xpath=//a[ contains( @onclick, "select_all_checkboxes")]'
        checked_box = 'xpath=//img [contains(@src, "check.gif")]'
        box = lambda name: \
        'xpath=//td[ contains(text() , "%s")]/../td[last()]/div/img' % name

        self.click_link(edit_list)

        if 'all' in list:
            self.click_link(select_all, "don't wait")
        else:
            # uncheck all checked boxes
            while self._is_element_present(checked_box):
                self.click_element(checked_box, "don't wait")
            # check all specified in the list
            for item in list:
                self.click_element(box(item), "don't wait")

        self._click_done_button()

