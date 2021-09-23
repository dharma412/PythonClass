#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/return_addresses.py#1 $

from common.gui.guicommon import GuiCommon

class ReturnAddresses(GuiCommon):
    """ GUI configurator for 'System Administration -> Return Addresses'
        page.
    """

    def get_keyword_names(self):
        return ['return_addresses_edit']

    def _open_page(self):
        """Go to 'System Administration -> Return Addresses' configuration
           page """

        self._navigate_to("System Administration", "Return Addresses")

    def _fill_display_name(self, name):
        name_loc = 'name=REPORTSFROM_friendlyname'
        self.input_text(name_loc, name)

    def _fill_username(self, name):
        username_loc = 'name=REPORTSFROM_username'
        self.input_text(username_loc, name)

    def _fill_hostname(self, name):
        hostname_loc = 'name=REPORTSFROM_hostname'
        self.input_text(hostname_loc, name)

    def return_addresses_edit(self, displayname=None, username=None,
                              hostname=None):
        """Edit return address for system-generated email for report.

        Parameters:
           - `displayname`: display name for generated email.
           - `username`: username to use in generated email.
           - `hostname`: domain name to use in generated email.

        Example:
        | Return Addresses Edit | displayname=Test User | username=testuser | hostname=mail.qa |
        """
        self._open_page()
        self._click_edit_settings_button()
        if displayname is not None:
            self._fill_display_name(displayname)
        if username is not None:
            self._fill_username(username)
        if hostname is not None:
            self._fill_hostname(hostname)
        self._click_submit_button()
