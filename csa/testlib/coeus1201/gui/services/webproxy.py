#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/webproxy.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.gui.guicommon import GuiCommon

PROX_MODE = lambda mode: 'id=proxyMode_%s' % (mode.lower(),)
HEADER_ACTION = {'send': 'yes',
                 'do_not_send': 'no'}
IP_SPOOFING_CHECKBOX = 'proxySpoofing'

SETTINGS_VALUE = lambda  row:\
                    '//table[@class=\'pairs\']/tbody/tr[%s]/td[1]' % str(row)

SETTINGS_NAME = lambda  row:\
                    '//table[@class=\'pairs\']/tbody/tr[%s]/th[1]' % str(row)

class WebProxy(GuiCommon):
    """Web Proxy settings page interaction class."""

    def get_keyword_names(self):
        return ['web_proxy_enable',
                'web_proxy_disable',
                'web_proxy_clear_cache',
                'web_proxy_get_settings',
                'web_proxy_edit_settings']

    def _open_page(self):
        """Open 'Web Proxy page' & check if proxy configured"""

        self._navigate_to('Security Services', 'Web Proxy')
        # check if proxy configured or not
        self._is_proxy_configured()

    def web_proxy_enable(self):
        """Enable Proxy.

        Example:
        | Web Proxy Enable |

        """
        enable_proxy_button = "//input[@value='Enable...']"
        self._open_page()
        if self._check_feature_status(feature='proxy_settings'):
            return
        self.click_button(enable_proxy_button)

    def web_proxy_disable(self):
        """Disable Proxy.

        Example:
        | Web Proxy Disable |

        """
        enable_checkbox = 'prox_enabled'
        confirm_disable_button = "//button[text() = 'Disable Proxy']"
        self._open_page()
        #check if proxy already disabled or not
        if not self._check_feature_status(feature='proxy_settings'):
            return
        self._click_edit_settings_button()
        self._unselect_checkbox(enable_checkbox)
        self.click_button(confirm_disable_button, "don't wait")
        self._click_submit_button()

    def web_proxy_get_settings(self):
        """Get Proxy Settings.

        Parameters:
            None.

        Return:
            Dictionary keys of which are names of settings.

        Example:
        | ${result} | Web Proxy Get Settings |
        """
        self._open_page()
        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(\
                SETTINGS_NAME('*'))) + 1
        for row in xrange(2, num_of_entries):
            if not(self._is_element_present(SETTINGS_VALUE(row))):
                continue
            entries[self.get_text(SETTINGS_NAME(row))] = \
                   self.get_text(SETTINGS_VALUE(row))
        return entries

    def _set_http_ports_to_proxy(self, http_ports_to_proxy):

        http_ports_field = 'port'
        if http_ports_to_proxy:
            self.input_text(http_ports_field, http_ports_to_proxy)

    def _manipulate_caching(self, caching):

        caching_checkbox = 'cacheEnabled'
        if caching is not None:
            if caching:
                self.select_checkbox(caching_checkbox)
            else:
                self.unselect_checkbox(caching_checkbox)

    def _set_proxy_mode(self, proxy_mode):

        if proxy_mode is not None:
            self._click_radio_button(PROX_MODE(proxy_mode))

    def _select_ip_spoofing_for(self, spoofing_for):

        spoofing_radio_button = \
                         {'trans' : 'id=transparentSpoofing_trans',
                          'all' : 'id=transparentSpoofing_all'}
        if spoofing_for is not None:
            if not self._is_checked(IP_SPOOFING_CHECKBOX):
                raise ValueError\
                   ('Cannot set \'spoofing_for\', IP spoofing '\
                                                  'is Disabled')
            if spoofing_for.lower() == 'transparent':
                self._click_radio_button(spoofing_radio_button['trans'])
            else:
                self._click_radio_button(spoofing_radio_button['all'])

    def _manipulate_ip_spoofing(self, enable_spoofing):

        if enable_spoofing is not None:
            if enable_spoofing:
                self.select_checkbox(IP_SPOOFING_CHECKBOX)
            else:
                self.unselect_checkbox(IP_SPOOFING_CHECKBOX)

    def _set_persistent_connection_timeout_client(self,
                                                persistent_timeout_client):

        persistent_timeout_client_field = 'maxClientIdleConnTime'
        if persistent_timeout_client is not None:
            self.input_text(persistent_timeout_client_field,
                                   persistent_timeout_client)

    def _set_persistent_connection_timeout_server(self,
                                              persistent_timeout_server):

        persistent_timeout_server_field = 'minActivitySecs'
        if persistent_timeout_server is not None:
            self.input_text(persistent_timeout_server_field,
                                   persistent_timeout_server)

    def _set_in_use_connection_timeout_client(self, in_use_timeout_client):

        in_use_timeout_client_field = 'maxClientPConnTime'
        if in_use_timeout_client is not None:
            self.input_text(in_use_timeout_client_field,
                                   in_use_timeout_client)

    def _set_in_use_connection_timeout_server(self, in_use_timeout_server):

        in_use_timeout_server_field = 'maxServPConnTime'
        if in_use_timeout_server is not None:
            self.input_text(in_use_timeout_server_field,
                                   in_use_timeout_server)

    def _set_simultaneous_persistent_connections(self, simultaneous_conn):

        persistent_conn_max_server_field = 'maxIdleServPConns'
        if simultaneous_conn:
            self.input_text(persistent_conn_max_server_field,
                                   simultaneous_conn)

    def _set_headers_x_fwd_for(self, headers_x):

        if headers_x:
            if not headers_x.lower() in HEADER_ACTION.keys():
                raise ValueError\
                          ('Value for Headers X-Forwarded-For \'%s\' '
                           'is not allowed. Please choose one from '\
                           '%s' % (headers_x, HEADER_ACTION.keys()))
            headers_x_radio_button = 'id=forwardedFor_%s' % \
                        HEADER_ACTION[headers_x.lower()]
            self._click_radio_button(headers_x_radio_button)

    def _set_headers_via_req(self, headers_via_req):

        headers_via_req_radio_button = {'send': 'suppressRequestVia_yes',
                                        'do_not_send': 'suppressRequestVia_no'}
        if headers_via_req is not None:
            if headers_via_req.lower() == 'send':
                self._click_radio_button(headers_via_req_radio_button['send'])
            else: # assuming user will give valid input
                self._click_radio_button\
                                (headers_via_req_radio_button['do_not_send'])

    def _set_headers_via_resp(self, headers_via_resp):

        headers_via_resp_radio_button = {'send': 'suppressResponseVia_yes',
                                         'do_not_send': 'suppressResponseVia_no'}
        if headers_via_resp is not None:
            if headers_via_resp.lower() == 'send':
                self._click_radio_button(headers_via_resp_radio_button['send'])
            else: # assuming user will give valid input
                self._click_radio_button\
                            (headers_via_resp_radio_button['do_not_send'])

    def _set_enable_identification(self, enable_identification):
        CHECKBOX = "//input [@id='use_xff']"

        if enable_identification == None: return

        if enable_identification != self._is_checked(CHECKBOX):
            self.click_element(CHECKBOX, "don't wait")

    def _set_enable_range_request_fwd(self, enable_rr_fwd):
        CHECKBOX = "//input[@id='enable_range_requests']"

        if enable_rr_fwd == None: return

        if enable_rr_fwd != self._is_checked(CHECKBOX):
            self.click_element(CHECKBOX, "don't wait")

    def _set_trusted_proxies(self, trusted_proxies):
        ADD_ROW = "//input [@id='downstream_proxies_domtable_AddRow']"
        ROWS = "//tr[starts-with(@id , 'downstream_proxies_row')]"
        DELETE_ROW =  lambda row: "//tr[@id = 'downstream_proxies_row%s']/td/img" % row
        IP_FIELD = lambda row: "//tr[@id = 'downstream_proxies_row%s']/td/input" % row

        if trusted_proxies == None: return

        # Remove all existing IPs
        count = int(self.get_matching_xpath_count(ROWS))
        for index in range(count):
            self.click_element(DELETE_ROW(index), "don't wait")

        # Enter the specified IPs
        ips = self._convert_to_tuple(trusted_proxies)
        for index in range(ips.__len__()):
            self.input_text(IP_FIELD(count-1+index), ips[index])
            if index < (ips.__len__() -1):
                self.click_button(ADD_ROW, "don't wait")

    def web_proxy_clear_cache(self):
        """Click 'Clear Cache' button

        Example:
        | Web Proxy Clear Cache |

        """
        clear_cache_button = "//input[@value=\'Clear Cache\']"
        confirm_clear_cache_button = "//button[@type=\'button\']"
        self._open_page()
        #check if proxy already disabled or not
        if not self._check_feature_status(feature='proxy_settings'):
            raise ValueError('Proxy is disabled.')
        if not self._is_visible(clear_cache_button):
            raise ValueError('Cannot clear cache, caching is Disabled')
        self.click_button(clear_cache_button, "don't wait")
        self.click_button(confirm_clear_cache_button)
        # Validate errors on the page
        self._check_action_result()

    def web_proxy_edit_settings(self,
                  http_ports_to_proxy=None,
                  caching=None,
                  proxy_mode=None,
                  enable_spoofing=None,
                  spoofing_for=None,
                  persistent_timeout_client=None,
                  persistent_timeout_server=None,
                  in_use_timeout_client=None,
                  in_use_timeout_server=None,
                  simultaneous_conn=None,
                  headers_x=None,
                  headers_via_req=None,
                  headers_via_resp=None,
                  enable_identification=None,
                  trusted_proxies=None,
                  enable_rr_fwd=None,
        ):

        """Edit Proxy Settings.

        :Parameters:
            - `http_ports_to_proxy` : HTTP port numbers.
            - `caching` : Set True to enable, False to disable.
            - `proxy_mode` : Set proxy mode, 'Transparent' or 'Forward'
            - `enable_spoofing` : True to enable 'IP Spoofing', False to disable
            - `spoofing_for` : Enable IP Spoofing for, 'Transparent' -> For Transparent Connections Only, 'All' -> For All Connections
            - `persistent_timeout_client` : Set client side persistent, timeout in seconds
            - `persistent_timeout_server` : Set server side persistent, timeout in seconds
            - `in_use_timeout_client` : Set client side in-use connection, timeout in seconds
            - `in_use_timeout_server` : Set server side in-use connection, timeout in seconds
            - `simultaneous_conn` : Set maximum server, number for simultaneous persistent connections
            - `headers_x` : Set Headers 'X-Forwarded-For' to 'send' or 'do_not_send'
            - `headers_via_req`: Set Headers 'Request Side VIA' to 'send' or 'do_not_send'
            - `headers_via_resp`: Set Headers 'Response Side VIA' to 'send' or 'do_not_send'
            - `enable_identification` - Enable Identification of Client IP Addresses using X-Forwarded-For
               accepted values: True - enable, False - disable, None - do not change
            - `trusted_proxies` -  A string of comma-separated IPs of
               Trusted Downstream Proxies or Load Balancers
            - `enable_rr_fwd` - Enable Range Request Forwarding
               accepted values: True - enable, False - disable, None - do not change

        Example:
        | Web Proxy Edit Settings | http_ports_to_proxy=12, 24 | caching=True | proxy_mode=Forward |
        | Web Proxy Edit Settings | enable_spoofing=True | spoofing_for=All |
        | Web Proxy Edit Settings | persistent_timeout_client=100 | simultaneous_conn=100 |
        | Web Proxy Edit Settings | headers_x=do_not_send | headers_via_req=send |

        """
        self._open_page()
        if not self._check_feature_status(feature='proxy_settings'):
            raise ValueError('Proxy is disabled.')
        self._click_edit_settings_button()
        self._set_http_ports_to_proxy(http_ports_to_proxy)
        self._manipulate_caching(caching)
        self._set_proxy_mode(proxy_mode)
        self._manipulate_ip_spoofing(enable_spoofing)
        self._select_ip_spoofing_for(spoofing_for)
        self._set_persistent_connection_timeout_client(persistent_timeout_client)
        self._set_persistent_connection_timeout_server(persistent_timeout_server)
        self._set_in_use_connection_timeout_client(in_use_timeout_client)
        self._set_in_use_connection_timeout_server(in_use_timeout_server)
        self._set_simultaneous_persistent_connections(simultaneous_conn)
        self._set_headers_x_fwd_for(headers_x)
        self._set_headers_via_req(headers_via_req)
        self._set_headers_via_resp(headers_via_resp)
        self._set_enable_identification(enable_identification)
        self._set_enable_range_request_fwd(enable_rr_fwd)
        self._set_trusted_proxies(trusted_proxies)
        self._click_submit_button()
