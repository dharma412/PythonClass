#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/network_access.py#1 $ $DateTime: 2019/08/14 09:58:47 $ $Author: uvelayut $

from common.gui.guicommon import GuiCommon

class NetworkAccess(GuiCommon):
    """Keywords for System Administration -> Network Access
    """

    def get_keyword_names(self):
        return [
                'network_access_edit',
               ]

    def _open_page(self):
        """
       Navigate to Network Access configuration page.
        """
        # the simple way does not work
        self._navigate_to('System Administration', 'Network Access')
        #self._navigate_to('System Administration',  \
        #  "xpath=//*[contains(@class, 'yuimenuitemlabel') and text()='Network Access']")

    def network_access_edit(self,
        timeout=None,
        access=None,
        custom_connections=None):
        """Edit Network Access settings.

        Parameters:
        - `timeout`: Web UI Inactivity Timeout,
           value between 5 - 1440 Minutes (24 hours)
        - `access`: Control system access; 'any' or 'custom'
        - `custom_connections`: IP address, IP range or CIDR range.
           Separate multiple entries with commas.
           Examples: 10.0.0.1, 10.0.0.1-24, 10.0.0.0/8

        Examples:
        | NetworkAccess Edit | timeout=120 |
        | NetworkAccess Edit | access=any |
        | NetworkAccess Edit | access=custom | custom_connections=10.0.0.1, 10.0.0.1-24, 10.0.0.0/8 |

        """
        self._info('Editing Network Access settings.')
        if timeout is None and \
           access is None and \
           custom_connections is None:
            self._info('Nothing is set to change')
            return
        self._open_page()
        self._click_edit_settings_button()

        if not timeout is None:
            self._set_timeout(timeout)
        if not access is None:
            self._set_access(access)
        if not custom_connections is None:
            self._set_connections(custom_connections)
        self._click_submit_button()

    def _set_timeout(self, timeout):
        timeout_loc = 'name=session_timeout'
        self.input_text(timeout_loc, timeout)

    def _set_access(self, access):
        access_loc = 'id=access_type'
        access_map = {
            'any':'Allow Any Connection',
            'custom':'Only Allow Specific Connections'
            }
        if access_map.has_key(access):
            self.select_from_list(access_loc, access_map[access])
        else:
            raise ValueError, '"%s" is not allowed value' % (access,)

    def _set_connections(self, custom_connections):
        connections_loc = 'id=access_list'
        self.input_text(connections_loc, custom_connections)

