#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/network/routing.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.gui.guicommon import GuiCommon

ADD_ROUTE_BUTTON = 'xpath=//input[@value="Add Route..."]'
DELETE_ALL_ROUTES_BUTTON = 'xpath=//input[@value="Delete All"]'
NAME_TEXTBOX = 'name=new_id'
DESTINATION_TEXTBOX = 'name=destination'
GATEWAY_TEXTBOX = 'name=gateway'
EDIT_ROUTE_LINK = lambda route: 'xpath=//a[contains(@href, "&id=%s")]' % (route,)
TABLE_LOCATOR = '//dl[@class="box"]//table'
DELETE_ROUTE_LINK = lambda row: '%s//tr[%s]/td[4]/img' % (TABLE_LOCATOR, row)
TABLE_ROW = '%s//tr' % (TABLE_LOCATOR,)
ROUTE_CELL_TEXT = lambda row: '%s//tr[%s]/td[1]' % (TABLE_LOCATOR, row)
PAGE_SIZE_LIST = 'id=pageSize'
SHOW_ALL_PAGES = 'All'
LIST_LABEL = lambda label: 'label=%s' % (label,)


class Routing(GuiCommon):
    """
    Keyword library for WebUI page Management Appliance -> Network -> Routing
    """

    def get_keyword_names(self):
        return ['routing_add_route',
                'routing_edit_route',
                'routing_delete_routes',
                'routing_set_default_gateway',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'Network', 'Routing')

    def _click_add_route_button(self):
        self.click_button(ADD_ROUTE_BUTTON)
        self._info('Clicked "Add Route..." button.')

    def _fill_table_row(self, name, destination, gateway):
        if name is not None:
            self._fill_name_textbox(name)

        if destination is not None:
            self._fill_destination_textbox(destination)

        if gateway is not None:
            self._fill_gateway_textbox(gateway)

    def _fill_name_textbox(self, name):
        self.input_text(NAME_TEXTBOX, name)
        self._info('Set name to "%s".' % (name,))

    def _fill_destination_textbox(self, destination):
        self.input_text(DESTINATION_TEXTBOX, destination)
        self._info('Set destination network to "%s".' % (destination,))

    def _fill_gateway_textbox(self, gateway):
        self.input_text(GATEWAY_TEXTBOX, gateway)
        self._info('Set gateway to "%s".' % (gateway,))

    def _show_all_routes(self):
        if self._is_element_present(PAGE_SIZE_LIST) and \
                self.get_value(PAGE_SIZE_LIST) != SHOW_ALL_PAGES:
            self.select_from_list(PAGE_SIZE_LIST,
                                  LIST_LABEL(SHOW_ALL_PAGES), SHOW_ALL_PAGES)
            self._info('Selected to show all routes on current page.')

    def _click_edit_route_link(self, name):
        self._show_all_routes()
        route_locator = EDIT_ROUTE_LINK(name)
        if self._is_element_present(route_locator):
            self.click_button(route_locator, "don't wait")
            self._info('Clicked edit "%s" route link.' % (name,))
        else:
            raise ValueError('"%s" route does not exist' % (name,))

    def _get_route_row_index(self, route):
        table_rows = int(self.get_matching_xpath_count(TABLE_ROW))
        for row in xrange(2, table_rows):
            if route == self.get_text('xpath=' + ROUTE_CELL_TEXT(row)):
                return row
        return None

    def _click_delete_route_link(self, route):
        self._show_all_routes()
        row_index = self._get_route_row_index(route)
        if row_index is None:
            raise ValueError('"%s" route does not exist' % (route,))

        self.click_button(DELETE_ROUTE_LINK(row_index), "don't wait")
        self._click_continue_button()
        self._info('Deleted "%s" route.' % (route,))

    def _click_delete_all_routes_button(self):
        if self._is_element_present(DELETE_ALL_ROUTES_BUTTON):
            self.click_button(DELETE_ALL_ROUTES_BUTTON, "don't wait")
            self._info('Clicked "Delete All" button.')
            self._click_continue_button()
        else:
            raise ValueError('There  are no configured routes.')

    def routing_add_route(self, name, destination, gateway):
        """Add new route to the routing table.

        *Parameters*
            - `name`: name for the route. String.
            - `destination`: destination network for the route. String.
            - `gateway`: gateway for the route. String.

        *Return*
            None.

        *Exceptions*
            None.

        *Examples*
            | Routing Add Route | to_branch | 192.168.0.0 | 10.0.0.1 |
            | Routing Add Route | to_branch1 | 192.168.20.0/24 | 10.0.0.2 |
        """
        self._info('Adding "%s" route.' % (name,))

        self._open_page()

        self._click_add_route_button()

        self._fill_table_row(name, destination, gateway)

        self._click_submit_button()

        self._info('Added "%s" route.' % (name,))

    def routing_edit_route(self, name, new_name=None, destination=None, gateway=None):
        """Edit route configuration.

        *Parameters*
            - `name`: name of the route to edit.
            - `new_name`: new name for the route. If ${None}, value will be left
                 unchanged.
            - `destination`: destination network for the route. If ${None}, value
                 will be left unchanged.
            - `gateway`: gateway for the route. If ${None}, value will be left
                 unchanged.

        *Return*
            None.

        *Exceptions*
             - `ValueError`: in case of invalid route name.

        *Examples*
            | Routing Edit Route | branch1 | gateway=10.0.0.1 |
            | Routing Edit Route | branch1 | 192.168.0.0/24 | 10.0.0.1 |
        """
        self._info('Editing "%s" route.' % (name,))

        self._open_page()

        self._click_edit_route_link(name)

        self._fill_table_row(new_name, destination, gateway)

        self._click_submit_button(False)

        self._info('Edited "%s" route.' % (name,))

    def routing_delete_routes(self, routes):
        """Delete route(s) from routing table.

        *Parameters*
            - `routes`: a comma-separated string of the routes name to delete.
                 If 'All', all configured routes will be deleted.

        *Return*
            None.

        *Exceptions*
            - `ValueError`: in case of invalid route name.

        *Examples*
            | Routing Delete Routes | branch1, branch2 |
            | Routing Delete Routes | all |
        """
        self._info('Removing "%s" route(s).' % (routes,))

        self._open_page()

        if routes.lower() == 'all':
            self._click_delete_all_routes_button()
        else:
            list_of_routes = self._convert_to_tuple(routes)
            for route in list_of_routes:
                self._click_delete_route_link(route)

        self._info('Removed "%s" route(s).' % (routes,))

    def routing_set_default_gateway(self, gateway):
        """Edit default gateway for the routing table.

        *Parameters*
            - `gateway`: default gateway to use for the routing table. String.

        *Return*
            None.

        *Exception*
            | Routing Set Default Gateway | 192.168.0.1 |
            | Routing Set Default Gateway | 10.10.0.1 |
        """
        self._info('Setting new default gateway.')

        self._open_page()

        self._click_edit_route_link('ALL')

        self._fill_table_row(None, None, gateway)

        self._click_submit_button()

        self._info('Set "%s" default gateway.' % (gateway,))
