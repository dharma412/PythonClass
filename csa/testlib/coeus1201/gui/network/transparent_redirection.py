#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/transparent_redirection.py#1 $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon


TABLE_ID = "//table[@class=\'cols\']"
TABLE_ITEM = lambda table_name, index, table_column: ('%s//tr[%s]//td[%d]' % \
                                           (table_name, index, table_column,))
CELL_ID = lambda table_name, index, table_column, element: \
          '%s//tr[%s]//td[%s]/%s' % (table_name, index, table_column, element)


class TransparentRedirection(GuiCommon):
    """Transparent Redirection Settings page interaction class.

    This class designed to interact with GUI elements of 'Network' ->
    'Transparent Redirection' page.

    Before configuring Transparent Redirections settings make sure that web
    proxy was configured correctly.
    """

    def get_keyword_names(self):
        return ['transparent_redirection_add_service',
                'transparent_redirection_edit_service',
                'transparent_redirection_delete_service',
                'transparent_redirection_edit_device',
               ]

    def _open_page(self):
        """Open 'Transparent Redirection' page """

        self._navigate_to('Network', 'Transparent Redirection')

    def _check_service_status(self, check_service_defined=False):
        """Check if WCCP v2 Services is available

        :Return:
            True if WCCP v2 Services is available and/or any service defined,
            Generate exception otherwise
        """

        if not self._is_text_present('WCCP v2 Services'):
            raise guiexceptions.GuiFeatureDisabledError\
             ('WCCP v2 Services is not available, select type - '\
                      'WCCP v2 Router to add/delete/edit service')
        if check_service_defined:
            if self._is_text_present('No WCCP services are defined.'):
                raise guiexceptions.GuiFeatureDisabledError\
                ('Cannot perform delete/edit as no WCCP services defined.')
        return True

    def _click_edit_device_button(self):
        """Click 'Edit Device...' button"""

        edit_device_button = 'xpath=//input[@value=\'Edit Device...\']'
        self.click_button(edit_device_button)

    def _click_add_service_button(self):
        """Click 'Add Service...' button"""

        add_service_button = "xpath=//input[@title='Add Service...']"
        self.click_button(add_service_button)

    def _select_type(self, device_type=None):

        type_option = {'wccp': 'label=WCCP v2 Router',
                       'l4': 'label=Layer 4 Switch or No Device'}
        type_select = 'routing_device'
        if device_type is not None:
            if device_type.lower() not in type_option.keys():
                raise guiexceptions.CinfigError('Value for device type \'%s\' '
                                 'is not allowed. Please choose one from '\
                                 '%s' % (device_type, type_option.keys()))
            self.select_from_list(type_select, type_option[device_type.lower()])

    def _set_service_profile_name(self, name=None):

        service_name_field = 'name'
        if name is not None:
            self.input_text(service_name_field, name)

    def _select_standard_service(self):

        std_service_radio_button = "//input[@name='isWebCache' and (@value='true' or @value='1')]"
        if self._is_text_present('Not available, already defined'):
            raise guiexceptions.GuiFeatureDisabledError\
                   ('Standard Service is not available, already defined')
        self._click_radio_button(std_service_radio_button)

    def _select_dynamic_service(self, dynamic_dict):

        serv_dict = \
         {'type': "//input[@name='isWebCache' and (@value='false' or @value='0')]",
          'id': 'id',
          'port': 'ports',
          'redirect': ("direction",
          "//input[@id='direction' and @name='direction' and @value='1']"),
          'load_balance': ("use_client_addr",
          "//input[@id='use_client_addr' and @name='use_client_addr'" + \
          " and @value='1']")
         }

        for serv_field, value in dynamic_dict.iteritems():
            if value is None:
                continue
            if serv_field.lower() not in serv_dict.keys():
                raise guiexceptions.ConfigError\
                      ('Invalid Key \'%s\' to set service info. '\
                       'Here are the valid fields '\
                       '%s' % (serv_field, serv_dict.keys()))
            if serv_field.lower() == 'type':
                self._click_radio_button(serv_dict['type'])

            if serv_field.lower() == 'id':
                self.input_text(serv_dict['id'], value)

            if serv_field.lower() == 'port':
                value = self._convert_to_tuple(value)
                port_text = ",".join([str(p) for p in value])
                self.input_text(serv_dict['port'], port_text)

            if serv_field.lower() == 'redirect':
                if value.lower() not in ('destination', 'source'):
                    raise guiexceptions.ConfigError(
                        'Invalid redirect value \'%s\'. Should be ' + \
                        'either \'destination\' or \'source\'.')
                if value.lower() == 'destination':
                    self._click_radio_button(serv_dict['redirect'][0])
                else:
                    self._click_radio_button(serv_dict['redirect'][1])

            if serv_field.lower() == 'load_balance':
                if value.lower() not in ('server', 'client'):
                    raise guiexceptions.ConfigError(
                        'Invalid redirect value \'%s\'. Should be ' + \
                        'either \'destination\' or \'source\'.')
                if value.lower() == 'server':
                    self._click_radio_button(serv_dict['load_balance'][0])
                else:
                    self._click_radio_button(serv_dict['load_balance'][1])

    def _set_service_info(self, service_type=None, id=None, ports=None,
                          redirect_type=None, load_balance=None):

        if service_type is None:
            return

        if service_type.lower() not in ['dynamic', 'standard']:
            raise guiexceptions.ConfigError('Invalid service type %s.' % \
                                                            (service_type,))

        if service_type.lower() == 'dynamic':
            if id is not None and \
                ports is not None:
                    dynamic_dict = {'type': service_type,
                                    'id': id,
                                    'port': ports,
                                    'redirect': redirect_type,
                                    'load_balance': load_balance}
            else:
                raise guiexceptions.ConfigError('Please specify ' + \
                    'dynamic service ID and ports for dynamic ' + \
                    'service type.')
            self._select_dynamic_service(dynamic_dict)
        else:
            self._select_standard_service()

    def _set_ip(self, ip=None):

        ip_field = "xpath=//textarea[@id='routers']"
        if ip is not None:
            self.input_text(ip_field, ip)

    def _manipulate_enable_security(self, security):

        security_checkbox = 'enable_security'
        if security is not None:
            if security.lower() != 'off':
                if not self._is_checked(security_checkbox):
                    self.click_element(security_checkbox, "don't wait")
                self._set_password(security)
            else:
                if self._is_checked(security_checkbox):
                    self.click_element(security_checkbox, "don't wait")

    def _set_password(self, password):

        pass_field = "xpath=//input[@name='router_password']"
        confirm_pass_field = "xpath=//input[@name='confirm_router_password']"
        if password is not None:
            self.input_text(pass_field, password)
            self.input_text(confirm_pass_field, password)

    def _select_advance_option(self,
                               load_balancing,
                               forward_method,
                               return_method):

        advanced_load_bal = {'hash and mask': 'label=Allow Hash or Mask',
                             'hash': 'label=Allow Hash Only',
                             'mask': 'label=Allow Mask Only'
                             }

        advanced_other = {'gre and l2': 'label=Allow GRE or L2',
                          'l2': 'label=Allow L2 only',
                          'gre': 'label=Allow GRE only'
                          }

        option_link = 'optionsLinkOpen'
        self.click_element(option_link, "don't wait")

        if load_balancing is not None:
            if load_balancing.lower() not in advanced_load_bal.keys():
                raise guiexceptions.ConfigError(
                    'Specified load-balancing method \'%s\' is invalid' % \
                    (load_balancing,))
            self.select_from_list('id=load_balancing',
                                  advanced_load_bal[load_balancing.lower()])

        if forward_method is not None:
            if forward_method.lower() not in advanced_other.keys():
                raise guiexceptions.ConfigError(
                    'Specified forwarding method method \'%s\' is invalid' % \
                    (forward_method,))
            self.select_from_list('id=forwarding_method',
                                  advanced_other[forward_method.lower()])

        if return_method is not None:
            if return_method.lower() not in advanced_other.keys():
                raise guiexceptions.ConfigError(
                    'Specified return method method \'%s\' is invalid' % \
                    (return_method,))
            self.select_from_list('id=return_method',
                                  advanced_other[return_method.lower()])

    def _assign_wccp_weight(self, name=None):

        weight_assign_field = 'assignment_weight'
        if name is not None:
            self.input_text(weight_assign_field, name)

    def _get_service_profile_name_row_index(self, name):

        table_column = 1
        table_rows = int(self.get_matching_xpath_count('%s//tr' % (TABLE_ID,)))
        for i in xrange(2, table_rows + 1):
            service_name = self.get_text\
               (TABLE_ITEM(TABLE_ID, i, table_column)).split(' \n')[0]
            if name in service_name:
                return i
        return None

    def _click_service_profile_link(self, name, table_column=1, element='a'):

        service_row = self._get_service_profile_name_row_index(name)
        if service_row is None:
            raise guiexceptions.GuiControlNotFoundError(\
              'Service Profile Name "%s"' % (name,), 'Transparent Redirection')
        self.click_element(
            CELL_ID(TABLE_ID, service_row, table_column, element), "don't wait")

    def transparent_redirection_delete_service(self,
                                               name):

        """Delete WCCP v2 Service.

        Parameters:
         - `name`: Service Profile Name. String. Mandatory.

        Example:
        | Transparent Redirection Delete Service | myServiceName |
        """
        confirm_delete_button = '//button[@type=\'button\']'
        self._open_page()
        # check if proxy configured
        self._is_proxy_configured()
        # check if WCCP v2 Service is available
        self._check_service_status(check_service_defined=True)
        self._click_service_profile_link(name, table_column=5, element='img')
        self.click_button(confirm_delete_button)

    def transparent_redirection_edit_service(self,
                                             name,
                                             new_name=None,
                                             ip=None,
                                             service=None,
                                             id=None,
                                             ports=None,
                                             redirection=None,
                                             load_balance=None,
                                             password=None,
                                             load_balancing_method=None,
                                             assign_weight=None,
                                             forwarding_method=None,
                                             return_method=None):

        """Edit WCCP v2 Service.

        Parameters:
        - `name`: Service Profile Name. String Mandatory.
        - `new_name`: New name for the Service Profile Name. String.
        - `ip`: String of comma separated values that represents IP addresses.
        - `service`: String. Type of service, 'dynamic' or 'standard'.
        - `id`: Dynamic service ID. Used only if type of service is 'dynamic'.
        - `ports`: String with comma separated values that represents dynamic
        port numbers. Used only if type of service is 'dynamic'.
        - `redirection`: String with value that indicate redirect based on
        'destination' or 'source' port.
        - `load_balance`: String with value that indicate load balance based on
        'server' or 'client' address.
        - `password`: String. 'off' to disable service security or string with
        security password to enable Router Security and set or change password.
        - `load_balancing_method`: Load-Balancing Method, Either: 'hash_mask'
        (to allow Hash or Mask), 'hash' (to allow Hash only) or 'mask' (to
        allow Mask only).
        - `assign_weight`: Weight Assignment should be between 0 and 255.
        - `forwarding method`: Forwarding Method. One of values: 'gre and l2'
        (to allow GRE or L2), 'l2' (to allow L2 only) or 'gre' (to allow GRE
        only).
        - `return_method`: Return Method, possible values are same as in
        `forwarding_method`.

        Example:
        | ${name} | Set Variable | Test |

        | Transparent Redirection Edit Service |  |
        | ... | ${name} |
        | ... | new_name=New |
        | ... | ip=1.1.1.1 |
        | ... | service=standard |
        | ... | password=qwerty |
        | ... | load_balancing_method=hash and mask |
        | ... | forwarding_method=l2 |
        | ... | return_method=gre and l2 |
        """

        self._open_page()
        # check if proxy configured
        self._is_proxy_configured()
        # check if WCCP v2 Service is available
        self._check_service_status(check_service_defined=True)
        self._click_service_profile_link(name)
        self._set_service_profile_name(new_name)
        self._set_service_info(service, id, ports, redirection, load_balance)
        self._set_ip(ip)
        self._manipulate_enable_security(password)
        self._select_advance_option(load_balancing_method, forwarding_method,
                                    return_method)
        self._assign_wccp_weight(assign_weight)
        self._click_submit_button()

    def transparent_redirection_add_service(self,
                                            name,
                                            ip,
                                            service=None,
                                            id=None,
                                            ports=None,
                                            redirection=None,
                                            load_balance=None,
                                            password=None,
                                            load_balancing_method=None,
                                            assign_weight=None,
                                            forwarding_method=None,
                                            return_method=None):

        """Add WCCP v2 Service.

        Parameters:
        - `name`: Service Profile Name. String Mandatory.
        - `ip`: String with comma separated values that represents IP addresses.
        Mandatory.
        - `service`: String. Type of service, 'dynamic' or 'standard'.
        - `id`: Dynamic service ID. Used only if type of service is 'dynamic'.
        - `ports`: String with comma separated values that represents dynamic
        port numbers. Used only if type of service is 'dynamic'.
        - `redirection`: String with value that indicate redirect based on
        'destination' or 'source' port.
        - `load_balance`: String with value that indicate load balance based on
        'server' or 'client' address.
        - `password`: String. 'off' to disable service security or string with
        security password to enable Router Security and set or change password.
        - `load_balancing_method`: Load-Balancing Method, Either: 'hash_mask'
        (to allow Hash or Mask), 'hash' (to allow Hash only) or 'mask' (to
        allow Mask only).
        - `assign_weight`: Weight Assignment should be between 0 and 255.
        - `forwarding method`: Forwarding Method. One of values: 'gre and l2'
        (to allow GRE or L2), 'l2' (to allow L2 only) or 'gre' (to allow GRE
        only).
        - `return_method`: Return Method, possible values are same as in
        `forwarding_method`.

        Example:
        | ${name} | Set Variable | Test |
        | ${ips} | Set Variable | 10.1.1.1, 192.168.1.1 |

        | Transparent Redirection Add Service |  |
        | ... | ${name} |
        | ... | ${ips} |
        | ... | service=dynamic |
        | ... | id=111 |
        | ... | ports=80, 110, 3128 |
        | ... | redirection=destination |
        | ... | load_balance=server |
        | ... | password=qwerty |
        | ... | load_balancing_method=mask |
        | ... | assign_weight=1 |
        | ... | forwarding_method=gre and l2 |
        | ... | return_method=gre |
        """

        self._open_page()
        # check if proxy configured
        self._is_proxy_configured()
        # check if WCCP v2 Service is available
        self._check_service_status()
        self._click_add_service_button()
        self._set_service_profile_name(name)
        self._set_service_info(service, id, ports, redirection, load_balance)
        self._set_ip(ip)
        self._manipulate_enable_security(password)
        self._select_advance_option(load_balancing_method, forwarding_method,
                                    return_method)
        self._assign_wccp_weight(assign_weight)
        self._click_submit_button()

    def transparent_redirection_edit_device(self, device_type):
        """Edit Transparent Redirection Device type.

        Parameters:
        - `device_type`: String. Represents Transparent Redirection device type
        'wccp' -> For 'WCCP v2 Router',
        'l4'   -> For 'Layer 4 Switch or No Device'

        Example:
        | Transparent Redirection Edit Device | l4 |

        | Transparent Redirection Edit Device | wccp |
        """

        self._open_page()
        # check if proxy configured
        self._is_proxy_configured()
        self._click_edit_device_button()
        self._select_type(device_type)
        self._click_submit_button()
