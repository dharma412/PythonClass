#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/route_config.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class RouteConfig(CliKeywordBase):
    """The routeconfig command controls the IP routing tables."""

    def get_keyword_names(self):

        return ['route_config_new',
                'route_config_edit',
                'route_config_delete',
                'route_config_clear',
                'route_config_print_routes'
                ]

    def route_config_new(self,
                         name=None,
                         destination=DEFAULT,
                         gateway=DEFAULT):
        """Create a new route.

        routeconfig > new

        Parameters:
        - `name`: name of the route.
        - `destination`: IP or CIDR address to match for
            outgoing IP traffic. The destination cannot already
            be defined by another route.
        - `gateway`: IP address to send this traffic to.

        Examples:
        | Route Config New | name=test1 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        | Route Config New | name=test2 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        """
        if name is not None:
            kwargs = {'name': name,
                      'dest': destination,
                      'gateway': gateway}

            self._cli.routeconfig().new(**kwargs)
        else: raise ValueError('Name is mandatory parameter.')

    def route_config_edit(self,
                          name=None,
                          destination=DEFAULT,
                          gateway=DEFAULT):
        """Modify a route.

        routeconfig > edit

        Parameters:
        - `name`: name of the route.
        - `destination`: IP or CIDR address to match for
            outgoing IP traffic. The destination cannot already
            be defined by another route.
        - `gateway`: IP address to send this traffic to.

        Examples:
        | Route Config Edit | name=test1 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        | Route Config Edit | name=test2 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        """
        if name is not None:
            kwargs = {'name': name,
                      'dest': destination,
                      'gateway': gateway,
                      'route_to_edit': str(name)}

            self._cli.routeconfig().edit(**kwargs)
        else: raise ValueError('Name is mandatory parameter.')

    def route_config_delete(self,
                            name=None):
        """Remove a route.

        routeconfig > delete

        Parameters:
        - `name`: name of the route. Specify 'delete_all' to
            clear all routes.

        Examples:
        | Route Config Edit | name=test1 |
        | Route Config Edit | name=test2 |
        """
        if name is not None:
            kwargs = {'route_to_delete': str(name)}
            self._cli.routeconfig().delete(**kwargs)
        else:
            raise ValueError('Name is mandatory parameter.')

    def route_config_clear(self):
        """Remove a route.

        routeconfig > clear

        Examples:
        | Route Config Clear |
        """

        self._cli.routeconfig().clear()

    def route_config_print_routes(self):
        """Print route configuration.

        routeconfig > print

        Return:
            Return currently configured routes.

        Examples:
        | ${out}= | Route Config Print Routes |
        """

        output = self._cli.routeconfig().print_routes()
        return output
