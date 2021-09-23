#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/interfaces.py#1 $

from common.gui.guicommon import GuiCommon

intf_index_dict = {'m1': '0', 'p1': '1', 'p2': '2'}
wiring_dict = {
    'duplex': "tm_mode_Tap1",
    'simplex': "tm_mode_Tap2" }

class Interfaces(GuiCommon):
    """Keywords for interaction with 'Network -> Interfaces' GUI page."""

    def get_keyword_names(self):
        return ['ip_interfaces_add',
                'ip_interfaces_edit',
                'ip_interfaces_delete',
                'ip_interfaces_edit_settings'
                ]

    def _fill_in_interface_config(self,
                                  intf,
                                  ip4_address_mask,
                                  hostname,
                                  ip6_address_mask
                                  ):

        ip4_address_mask_field = "interfaces[%s][ip]"
        ip6_address_mask_field = "interfaces[%s][ipv6]"
        hostname_field = "interfaces[%s][hostname]"

        if ip4_address_mask:
            self.input_text(ip4_address_mask_field %
                            intf_index_dict[intf.lower()],
                            ip4_address_mask)
        if ip6_address_mask:
            self.input_text(ip6_address_mask_field %
                            intf_index_dict[intf.lower()],
                            ip6_address_mask)
        self.input_text(hostname_field % intf_index_dict[intf.lower()],
                        hostname)

    def _clear_interface_config(self, intf):

        ip4_address_mask_field = "interfaces[%s][ip]"
        ip6_address_mask_field = "interfaces[%s][ipv6]"
        hostname_field = "interfaces[%s][hostname]"

        self.input_text(ip4_address_mask_field % intf_index_dict[intf.lower()],
                        '')
        self.input_text(ip6_address_mask_field % intf_index_dict[intf.lower()],
                        '')
        self.input_text(hostname_field % intf_index_dict[intf.lower()], '')

    def _configure_m1_restrict(self, restrict_m1):

        restrict_m1_checkbox = "dont_use_mgmt_for_proxy"

        if restrict_m1 is not None:
            if restrict_m1:
                self.select_checkbox(restrict_m1_checkbox)
            else:
                self.unselect_checkbox(restrict_m1_checkbox)

     #Adding FTP configuration as part of defect CSCuu28829
    def _configure_ftp(self, ftp_enable, ftp_port):

        ftp_checkbox = "ftpd"
        ftp_port_field = "ftpd_port"

        if ftp_enable:
           if not self._is_checked(ftp_checkbox):
                self.click_button(ftp_checkbox,"don't wait")
           if ftp_port:
                self.input_text(ftp_port_field, ftp_port)
        else:
            self.unselect_checkbox(ftp_checkbox)


    def _configure_http(self, http_enable, http_port):

        http_checkbox = "httpd"
        http_port_field = "httpd_port"

        if http_enable is not None:
            if http_enable:
                if not self._is_checked(http_checkbox):
                    self.select_checkbox(http_checkbox)
                if http_port:
                    self.input_text(http_port_field, http_port)
            else:
                self.unselect_checkbox(http_checkbox)

    def _configure_https(self, https_enable, https_port):

        https_checkbox = "httpsd"
        https_port_field = "httpsd_port"

        if https_enable is not None:
            if https_enable:
                if not self._is_checked(https_checkbox):
                    self.select_checkbox(https_checkbox)
                if https_port:
                    self.input_text(https_port_field, https_port)
            else:
                self.unselect_checkbox(https_checkbox)

    def _configure_https_redirect(self, redirect_http):

        redirect_https_checkbox = "https_redirect"

        if redirect_http is not None:
            if redirect_http:
                self.select_checkbox(redirect_https_checkbox)
            else:
                self.unselect_checkbox(redirect_https_checkbox)

    def _configure_wiring(self, wiring):

        if wiring:
            self._click_radio_button(wiring_dict[wiring.lower()])

    def _intf_already_configured(self, intf):

        ip_address_field = "interfaces[%s][ip]"

        # if 'IP Address' field is defined, the specified interface
        # is already configured.
        if self.get_value(ip_address_field % intf_index_dict[intf]):
            return True
        else:
            return False

    def _check_if_valid_intf_name(self, intf):
        intf_name_tuple = ('m1', 'p1', 'p2')

        if intf not in intf_name_tuple:
            raise ValueError ('ethernet port should either be "m1", "p1",'\
                              ' or "p2"')

    def _open_interfaces_page(self):
        """Go to 'Network -> Interfaces' configuration page."""

        self._navigate_to("Network", "Interfaces")

    def ip_interfaces_add(self,
                          ethernet_port,
                          ip4_address_mask,
                          hostname,
                          ip6_address_mask=None
                          ):
        """Adds new interface.

        Parameters:
        - `ethernet_port`: indicates the ethernet port to be added. Either
                           'm1', 'p1' or 'p2'.
        - `ip4_address_mask`: ipv4 address and mask`.
        - `hostname`: hostname of port specified in `ethernet_port`.
        - `ip6_address_mask`: ipv6 address and mask`.

        Example:
        | Ip Interfaces Add | P2 | 10.8.11.50/24 | wsaXX.wga |
        """

        self._check_if_valid_intf_name(ethernet_port.lower())
        self._open_interfaces_page()
        self._click_edit_settings_button()
        if self._intf_already_configured(ethernet_port.lower()):
            raise ValueError ('%s ethernet port is already configured' \
                              % ethernet_port.upper())
        self._fill_in_interface_config(ethernet_port.lower(), ip4_address_mask,
                                       hostname, ip6_address_mask)
        self._click_submit_button()

    def ip_interfaces_edit(self,
                           ethernet_port,
                           ip4_address_mask,
                           hostname,
                           ip6_address_mask
                           ):
        """Edits existing interface.

        Parameters:
        - `ethernet_port`: indicates the ethernet port to be edited.
                           Either 'm1', 'p1' or 'p2'.
        - `ip4_address_mask`: ipv4 address and mask`.
        - `hostname`: hostname of port specified in `ethernet_port`.
        - `ip6_address_mask`: ipv6 address and mask`.

        Example:
        | Ip Interfaces Edit | P2 | 10.9.11.48/24 | wsaXX.wga |
        """

        self._check_if_valid_intf_name(ethernet_port.lower())
        self._open_interfaces_page()
        self._click_edit_settings_button()
        if not self._intf_already_configured(ethernet_port.lower()):
            raise ValueError ("Can't edit %s ethernet port since it has not "\
                              "been configured yet" % ethernet_port.upper())
        self._fill_in_interface_config(ethernet_port.lower(), ip4_address_mask,
                                       hostname, ip6_address_mask)
        self._click_submit_button()

    def ip_interfaces_delete(self, ethernet_port):
        """Deletes existing interface.

        Parameters:
        - `ethernet_port`: indicates the ethernet port to be deleted.
                           Deletion of 'm1' is not allowed.  Either 'p1'
                           or 'p2'.

        Example:
        | Ip Interfaces Delete | P1 |
        """

        self._check_if_valid_intf_name(ethernet_port.lower())
        if ethernet_port.lower() == 'm1':
            raise ValueError ('Deleting %s ethernet port is not allowed' \
                              % ethernet_port.upper())
        self._open_interfaces_page()
        self._click_edit_settings_button()
        if not self._intf_already_configured(ethernet_port.lower()):
            raise ValueError ("Can't delete %s ethernet port since it has " \
                       "not been configured yet" % ethernet_port.upper())
        self._clear_interface_config(ethernet_port.lower())
        self._click_submit_button()

    def ip_interfaces_edit_settings(self,
                                    restrict_m1=None,
                                    ftp_enable=None,
                                    ftp_port=None,
                                    http_enable=None,
                                    http_port=None,
                                    https_enable=None,
                                    https_port=None,
                                    redirect_http=None,
                                    l4_wiring=None):
        """Edits additional configuration of interfaces.

        Parameters:
        - `restrict_m1`: restrict M1 port to appliance management services
                         only. True/False.
        - `http_enable`: to enable or disable HTTP service. True/False.
        - `http_port`: HTTP port if HTTP is to be enabled.
        - `https_enable`: to enable or disable HTTPS service. True/False.
        - `https_port`: HTTPS port if HTTPS is to be enabled.
        - `redirect_http`: to redirect or not redirect HTTP requests to
                           HTTPS. True/False.
        - `l4_wiring`: wiring configuration for L4 traffic monitor. Either
                       'duplex' or 'simplex'.

        Examples:
        | Ip Interfaces Edit Settings | http_enable=${True} | http_port=8080 | https_enable=${True} | https_port=8443 | ftp_enable=${True} | ftp_port=21
        | Ip Interfaces Edit Settings | l4_wiring=duplex |
        """

        self._open_interfaces_page()
        self._click_edit_settings_button()
        self._configure_m1_restrict(restrict_m1)

        #Adding FTP configuration as part of defect CSCuu28829  
        self._configure_ftp(ftp_enable, ftp_port)

        self._configure_http(http_enable, http_port)
        self._configure_https(https_enable, https_port)
        self._configure_https_redirect(redirect_http)
        self._configure_wiring(l4_wiring)
        self._click_submit_button()
