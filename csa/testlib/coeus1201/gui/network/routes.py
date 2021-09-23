#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/routes.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.gui.guicommon import GuiCommon
import os.path

DEFAULT_PROTOCOL = 'IPv4'
DEFAULT_INTERFACE = 'M1'

class Routes(GuiCommon):
    """Keywords for interaction with "Network > Routes" GUI page."""

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return [
                'routes_add',
                'routes_edit',
                'routes_delete',
                'routes_setgateway',
                'routes_load',
                ]

    def _open_page(self):
        self._navigate_to('Network', 'Routes')

    def _click_add_route_button(self, table):
        BUTTON = "//input[@value='Add Route...']"
        self.click_button(table + BUTTON)
        self._info('Clicked "Add Route..." button.')

    def _fill_table_row(self, name, destination, gateway):
        if name is not None:
            self._fill_name_textbox(name)

        if destination is not None:
            self._fill_destination_textbox(destination)

        if gateway is not None:
            self._fill_gateway_textbox(gateway)

    def _fill_name_textbox(self, name):
        TEXTBOX = 'id=name_id'
        self.input_text(TEXTBOX, name)
        self._info('Set name to "%s".' % (name,))

    def _fill_destination_textbox(self, destination):
        TEXTBOX = 'id=network_id'
        self.input_text(TEXTBOX, destination)
        self._info('Set destination network to "%s".' % (destination,))

    def _fill_gateway_textbox(self, gateway):
        TEXTBOX = 'id=gateway_id'
        self.input_text(TEXTBOX, gateway)
        self._info('Set gateway to "%s".' % (gateway,))

    def _fill_default_gateway_textbox(self, gateway):
        TEXTBOX = 'id=gateway_address_id'
        self._wait_until_element_is_present(TEXTBOX)
        self.input_text(TEXTBOX, gateway)
        self._info('Set default gateway to "%s".' % (gateway,))

    def _click_edit_route_link(self, name, table):
        LINK = "//a[text()='{name}']".format(name=name)

        self.click_element(table + LINK)
        self._info('Clicked edit "%s" route link.' % (name,))

    def _get_table_locator(self, protocol, interface):
        """
        return xpath of routing table
        Parameters:
            protocol - IPv4 or IPv6
            interface - Data, Management, M1, P1, or P2
        """
        LOW  = 'qwertyuiopasdfghjklzxcvbnm'
        HIGH = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        TEXT = "translate(text(), '{high}', '{low}')".format \
            (high=HIGH, low=LOW)

        table_locator = ("//dl/dt " + \
            "[contains({text}, '{protocol}')]" + \
            "[contains({text}, '{interface}')]/..").format ( \
            protocol=protocol.lower(), interface=interface.lower(), text=TEXT)
        self._wait_until_element_is_present(table_locator)

        return table_locator

    def _click_delete_route_checkbox(self, route, table):
        CHECKBOX = "//a[text() = '{name}']".format(name=route) + \
             "/ancestor::tr[1]//input[contains(@id, 'delete_checkbox')]"

        self.click_element(table + CHECKBOX, "don't wait")
        self._info('Selected "%s" route to delete.' % (route,))

    def _click_delete_all_routes_checkbox(self, table):
        CHECKBOX = "//input[contains(@id, 'selectAll_')]"
        self.click_button(table + CHECKBOX, "don't wait")
        self._info('Selected all routes to delete.')

    def _click_delete_button(self, table):
        BUTTON = "//input[@value = 'Delete']"
        self.click_button(table + BUTTON, "don't wait")
        self._info('Clicked "Delete" button.')

        CONFIRM_DLG = "//div[@id='confirmation_dialog']"
        try:
            self._wait_until_element_is_present(CONFIRM_DLG)
        except:
            self._info('Confirmation dialog did not appear')
        if self._is_element_present(CONFIRM_DLG):
            CONFIRM_DELETE_BUTTON = CONFIRM_DLG + "//button[text()='Delete']"
            self.click_button(CONFIRM_DELETE_BUTTON, "don't wait")
            self._info('Clicked "Delete" button in confirmation dialog.')

    def _click_load_table_button(self, table):
        BUTTON = "//input[@value='Load Route Table...']"
        self.click_button(table + BUTTON)
        self._info('Click "Load Table" button.')

    def _fill_filepath_textbox(self, filepath):
        TEXTBOX = 'id=file'
        self.choose_file(TEXTBOX, filepath)
        self._info('Set "%s" file to load table from.' % (filepath,))

    def routes_add(self, name, destination, gateway,
        table=DEFAULT_INTERFACE, protocol=DEFAULT_PROTOCOL):
        """Add new route to the routing table.

        Parameters:
            - `name`: name for the route.
            - `destination`: destination network for the route.
            - `gateway`: gateway for the route.
            - `table`: Data, or Management, or P1, or P2
            - `protocol`: choose ip protocol. Either 'IPv4' or 'IPv6'.
                Default to 'IPv4'

        Examples:
        | Routes Add | testroute | 10.10.1.0/24 | 10.7.10.1 | |
        | Routes Add | myroute | destination=10.10.1.0/24 | gateway=10.7.10.1 |
        | ... | table=Data |
        | Routes Add | myroutev6 | destination=fc03::1/64 | gateway=fc01::1 |
        | ... | protocol=IPv6 |
        """
        self._info('Adding "%s" route.' % (name,))
        self._open_page()
        table_loc = self._get_table_locator(protocol, table)
        self._click_add_route_button(table_loc)
        self._fill_table_row(name, destination, gateway)
        self._click_submit_button()

    def routes_edit(self, name, new_name=None, destination=None, gateway=None,
        table=DEFAULT_INTERFACE, protocol=DEFAULT_PROTOCOL):
        """Edit route configuration.

        Parameters:
            - `name`: name of the route to edit.
            - `new_name`: new name for the route. By default value will be left
                unchanged.
            - `destination`: destination network for the route. By default
                value will be left unchanged.
            - `gateway`: gateway for the route. By default value will be left
                unchanged.
            - `table`: Data, or Management, or P1, or P2
            - `protocol`: choose ip protocol. Either 'IPv4' or 'IPv6'.
                Default to 'IPv4'

        Examples:
        | Routes Edit | testroute | destination=10.5.1.0/24 |
        | Routes Edit | testroute | new_name=updatedroute |
        | ... | destination=10.6.1.0/24 | gateway=10.7.10.1 |
        | Routes Edit | myroutev6 | new_name=newv6route |
        | ... | destination=fc05::1/64 | gateway=fc01::5 | protocol=IPv6 |

        """
        self._info('Editing "%s" route.' % (name,))
        self._open_page()
        table_loc = self._get_table_locator(protocol, table)
        self._click_edit_route_link(name, table_loc)
        self._fill_table_row(new_name, destination, gateway)
        self._click_submit_button()

    def routes_delete(self, routes,
        table=DEFAULT_INTERFACE, protocol=DEFAULT_PROTOCOL):
        """Delete route(s) from routing table.

        Parameters:
            - `routes`: a coma separated list of names of the routes to delete.
                If 'All', all configured routes will be deleted.
            - `table`: Data, or Management, or P1, or P2
            - `protocol`: choose ip protocol. Either 'IPv4' or 'IPv6'.
                Default to 'IPv4'

        Examples:
        | Routes Delete | testroute |
        | Routes Delete | myroute1, myroute2 | protocol=IPv4 |
        | Routes Delete | myroutev6 | protocol=IPv6 |
        | Routes Delete | All | protocol=IPv6 |
        """
        self._info('Removing "%s" route(s).' % (routes,))
        self._open_page()
        table_loc = self._get_table_locator(protocol, table)
        if isinstance(routes, basestring) and routes.lower() == 'all':
            self._click_delete_all_routes_checkbox(table_loc)
        else:
            routes = self._convert_to_tuple(routes)
            for route in routes:
                self._click_delete_route_checkbox(route, table_loc)

        self._click_delete_button(table_loc)


    def routes_setgateway(self, gateway,
        table=DEFAULT_INTERFACE, protocol=DEFAULT_PROTOCOL):
        """Edit default gateway for the routing table.

        Parameters:
            - `gateway`: default gateway to use for the routing table.
            - `table`: Data, or Management, or P1, or P2
            - `protocol`: choose ip protocol. Either 'IPv4' or 'IPv6'.
                Default to 'IPv4'

        Examples:
        | Routes Set Gateway | 10.1.10.1 |
        | Routes Set Gateway | fc01::1 | protocol=IPv6 |
        """
        self._info('Setting default gateway for "%s" table.' % (table,))
        self._open_page()
        table_loc = self._get_table_locator(protocol, table)
        self._click_edit_route_link('Default Route', table_loc)
        self._fill_default_gateway_textbox(gateway)
        self._click_submit_button()
        self._info('Set "%s" default gateway for "%s" table.' %\
                        (gateway, protocol))

    def routes_load(self, filepath,
        table=DEFAULT_INTERFACE, protocol=DEFAULT_PROTOCOL):
        """Load IP routing table into WSA from local machine.

        Parameters:
            - `filepath`: path to routing table configuration file on local
                machine.
            - `protocol`: choose ip protocol. Either 'IPv4' or 'IPv6'.
                Default to 'IPv4'

        Examples:
        | Routes Load | /home/mymoroz/routes_table |
        | Routes Load | /home/mymoroz/routes_table | protocol=IPv6 |
        """
        if not os.path.isfile(filepath):
            raise ValueError('"%s" file does not exist' % (filepath,))

        self._info('Loading IP routing configuration from "%s".' %\
                         (filepath,))

        self._open_page()
        table_loc = self._get_table_locator(protocol, table)
        self._click_load_table_button(table_loc)
        self._fill_filepath_textbox(filepath)
        self._click_submit_button(False, accept_confirm_dialog='Import')
        self._info('Loaded IP routing configuration for "%s" table.' %\
                        (protocol,))
