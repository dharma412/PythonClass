#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/vrrp.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.gui.guicommon import GuiCommon

class VRRP(GuiCommon):
    """Keywords for interaction with "Network > High Availability" GUI page."""

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return [
                'vrrp_edit_settings',
                'vrrp_add_failover_group',
                'vrrp_edit_failover_group',
                'vrrp_delete_failover_group',
                'vrrp_refresh_status',
                ]

    def _open_page(self):
        self._navigate_to('Network', 'High Availability')

    def vrrp_edit_settings(self, failover_handling_preemptive):
        """Add new route to the routing table.

        Parameters:
        - `failover_handling_preemptive`: either 'yes' or 'no'
         If preemptive failover is selected, the highest priority server will
         assume control when online. If non-preemptive failover is selected,
         the server in control will remain in control, even if a higher priority
         server comes online.

        Examples:
        VRRP Edit Settings yes
        VRRP Edit Settings no

        Exceptions:
        - ValueError: Invalid failover_handling_preemptive '{value}'
         Should be in ['yes', 'no']

        """
        failover_map = {
            'yes':'Preemptive',
            'no':'Non-preemptive',
        }
        EDIT_SETTINGS_BUTTON = "//input [@value='Edit Settings']"
        FAILOVER_HANDLING_LIST = "//select [@id='failover_handling']"
        INVALID_HANDLING_VALUE = \
            "Invalid failover_handling_preemptive parameter." + \
            "'{value}'. Should be in {values}".format(
            value = failover_handling_preemptive,
            values = failover_map.keys())

        self._info('Edit High Availability Global Settings')
        if not failover_handling_preemptive in failover_map.keys():
            raise ValueError(INVALID_HANDLING_VALUE)
        self._open_page()
        self.click_button(EDIT_SETTINGS_BUTTON)
        self.select_from_list(FAILOVER_HANDLING_LIST,
            failover_map[failover_handling_preemptive])
        self._click_submit_button(skip_wait_for_title=True)

    def vrrp_add_failover_group(self,
        group_id,
        enable_group=None,
        description=None,
        hostname=None,
        addr_mask=None,
        interface=None,
        master_priority=None,
        backup_priority=None,
        enable_security=None,
        secret=None,
        secret_retype=None,
        interval=None,
    ):
        """Add a failover group

        Parameters:
        - `group_id`: Group ID (range 1 through 255)
        - `enable_group`: yes or no
        - `description`: Description
        - `hostname`: Hostname
        - `addr_mask`: Virtual IP Address and Netmask
         i.e., 10.0.0.3/24 or 2001:420:80:1::5/32
        - `interface`: Interface. If the option Select Interface Automatically
         is chosen, the interface (ethernet port) will be selected based on
         the entered IP address. If a specific interface selected, the Virtual
         IP address must be in the same subnet as the IP address associated
         with that interface (see Network > Interfaces).
        - `master_priority`: if set, Master Priority (255)
        - `backup_priority`: (range 1 through 254)
        - `enable_security`: Enable Security for Service: yes or no
        - `secret`: Shared Secret
        - `secret_retype`: Retype Shared Secret
        - `interval`: Advertisement Interval sec (range 1 through 255)

        Examples:
        VRRP Add Failover Group
        ...    1
        ...    enable_group=yes
        ...    description=Description
        ...    hostname=a.host.name
        ...    addr_mask=2001:420:80:1::5/32
        ...    interface=Management
        ...    master_priority=yes
        ...    enable_security=yes
        ...    secret=ironport
        ...    secret_retype=ironport
        ...    interval=35
        VRRP Add Failover Group
        ...    11
        ...    enable_group=no
        ...    description=Description
        ...    hostname=a.host.name
        ...    addr_mask=2001:420:80:1::5/32
        ...    interface=Management
        ...    backup_priority=35
        ...    enable_security=no
        ...    interval=35
        """
        self._info('Adding failover group "%s"' % group_id)
        self._open_page()
        self._click_add_group()
        self._enable_group(enable_group)
        self._input_group_id(group_id)
        self._input_description(description)
        self._input_hostname(hostname)
        self._input_addr_mask(addr_mask)
        self._select_interface(interface)
        self._set_master_priority(master_priority)
        self._set_backup_priority(backup_priority)
        self._enable_security(enable_security)
        self._input_secret(secret)
        self._input_secret_retype(secret_retype)
        self._input_interval(interval)
        self._click_submit_button(skip_wait_for_title=True)

    def vrrp_edit_failover_group(self,
        group_id,
        group_id_new=None,
        enable_group=None,
        description=None,
        hostname=None,
        addr_mask=None,
        interface=None,
        master_priority=None,
        backup_priority=None,
        enable_security=None,
        secret=None,
        secret_retype=None,
        interval=None,
    ):
        """Edit a failover group

        Parameters:
        - `group_id`: Group ID
        - `group_id_new`: Updated Group ID (range 1 through 255)
        - `enable_group`: yes or no
        - `description`: Description
        - `hostname`: Hostname
        - `addr_mask`: Virtual IP Address and Netmask
         i.e., 10.0.0.3/24 or 2001:420:80:1::5/32
        - `interface`: Interface. If the option Select Interface Automatically
         is chosen, the interface (ethernet port) will be selected based on
         the entered IP address. If a specific interface selected, the Virtual
         IP address must be in the same subnet as the IP address associated
         with that interface (see Network > Interfaces).
        - `master_priority`: if set, Master Priority (255)
        - `backup_priority`: (range 1 through 254)
        - `enable_security`: Enable Security for Service: yes or no
        - `secret`: Shared Secret
        - `secret_retype`: Retype Shared Secret
        - `interval`: Advertisement Interval sec (range 1 through 255)

        Examples:
        VRRP Edit Failover Group
        ...    1
        ...    group_id_new=111
        ...    enable_group=yes
        ...    description=Description
        ...    hostname=a.host.name
        ...    addr_mask=2001:420:80:1::5/32
        ...    interface=Management
        ...    master_priority=yes
        ...    enable_security=yes
        ...    secret=ironport
        ...    secret_retype=ironport
        ...    interval=35
        """
        self._info('Editing failover group "%s"' % group_id)
        self._open_page()
        self._click_edit_link(group_id)
        self._enable_group(enable_group)
        self._input_group_id(group_id_new)
        self._input_description(description)
        self._input_hostname(hostname)
        self._input_addr_mask(addr_mask)
        self._select_interface(interface)
        self._set_master_priority(master_priority)
        self._set_backup_priority(backup_priority)
        self._enable_security(enable_security)
        self._input_secret(secret)
        self._input_secret_retype(secret_retype)
        self._input_interval(interval)
        self._click_submit_button(skip_wait_for_title=True)

    def vrrp_delete_failover_group(self, group_id):
        """Deletes specified failover policy.

        Parameters:
        - `group_id`: Group ID

        Example:
        | VRRP Delete Failover Group | 45 |
        """
        self._info('Adding failover group "%s"' % group_id)
        self._open_page()
        self._click_delete_link(group_id)

    def vrrp_refresh_status(self):
        """Click Refresh Status on VRRP page

        Parameters:

        Examples:
        VRRP Refresh Status

        """
        BUTTON = "//input [@value='Refresh Status']"
        self.click_button(BUTTON)

##### Internal methods ###
    def _click_add_group(self):
        BUTTON = "//input [contains(@value, 'Add Failover Group')]"
        self.click_button(BUTTON)

    def _enable_group(self, param):
        CHECKBOX = "//input [@id='enabled']"
        if param == 'yes':
            self.select_checkbox(CHECKBOX)
        elif param == 'no':
            self.unselect_checkbox(CHECKBOX)

    def _input_group_id(self, param):
        TEXTFIELD = "//input[@id='id']"
        self._input_text_if_not_none(TEXTFIELD, param)

    def _input_description(self, param):
        TEXTFIELD = "//textarea[@id='descr']"
        self._input_text_if_not_none(TEXTFIELD, param)

    def _input_hostname(self, param):
        TEXTFIELD = "//input[@id='hostname']"
        self._input_text_if_not_none(TEXTFIELD, param)

    def _input_addr_mask(self, param):
        TEXTFIELD = "//input[@id='virtualip']"
        self._input_text_if_not_none(TEXTFIELD, param)

    def _select_interface(self, param):
        LIST = "//select [@id='failover_handling']"
        if param:
            self.select_from_list(LIST, param)

    def _set_master_priority(self, param):
        RADIOBUTTON = "//input[@id='master']"
        if param:
            self.click_element(RADIOBUTTON, "don't wait")

    def _set_backup_priority(self, param):
        RADIOBUTTON = "//input[@id='backup']"
        TEXTFIELD = "//input[@id='priority_value']"
        if param:
            self.click_element(RADIOBUTTON, "don't wait")
            self.input_text(TEXTFIELD, param)

    def _enable_security(self, param):
        CHECKBOX = "//input[@id='enable_security']"
        self._select_unselect_checkbox(CHECKBOX, param)

    def _input_secret(self, param):
        TEXTFIELD = "//input[@id='secret']"
        self._input_text_if_not_none(TEXTFIELD, param)

    def _input_secret_retype(self, param):
        TEXTFIELD = "//input[@id='secret_retype']"
        self._input_text_if_not_none(TEXTFIELD, param)

    def _input_interval(self, param):
        TEXTFIELD = "//input[@id='interval']"
        self._input_text_if_not_none(TEXTFIELD, param)

    def _click_edit_link(self, id_group):
        LINK = "//a [text()='Failover Group {id}']".format(id=id_group)
        self.click_element(LINK)

    def _click_delete_link(self, id_group):
        DELETE_IMG = "//a [text()='Failover Group {id}']".format(id=id_group)\
            + "/../../..//img[contains(@title, 'Delete')]"
        DELETE_BUTTON = "//div [@id='confirmation_dialog']//button[text()='Delete']"
        self.click_element(DELETE_IMG, "don't wait")
        self.click_button(DELETE_BUTTON)
