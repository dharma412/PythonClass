#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/route_config.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

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

    def route_config_new(self, ip_prot='ipv4',
                         name=None,
                         destination=DEFAULT,
                         gateway=DEFAULT):
        """Create a new route.

        routeconfig > new

        Parameters:
        - `ip_prot` : ip protocol ipv4 or ipv6. Default is ipv4
        - `name`: name of the route.
        - `destination`: IP or CIDR address to match for
            outgoing IP traffic. The destination cannot already
            be defined by another route.
        - `gateway`: IP address to send this traffic to.

        Examples:
        | Route Config New | ip_prot=ipv4 | name=test1 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        | Route Config New | name=test2 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        """
        if name is not None:
            kwargs = {'name': name,
                      'dest': destination,
                      'gateway': gateway}

            self._cli.routeconfig(ip_prot).new(**kwargs)
        else:
            raise ValueError('Name is mandatory parameter.')

    def route_config_edit(self, ip_prot='ipv4',
                          name=None,
                          destination=DEFAULT,
                          gateway=DEFAULT):
        """Modify a route.

        routeconfig > edit

        Parameters:
        - `ip_prot` : ip protocol ipv4 or ipv6. Default is ipv4
        - `name`: name of the route.
        - `destination`: IP or CIDR address to match for
            outgoing IP traffic. The destination cannot already
            be defined by another route.
        - `gateway`: IP address to send this traffic to.

        Examples:
        | Route Config Edit | ip_prot=ipv4 | name=test1 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        | Route Config Edit | name=test2 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        """
        if name is not None:
            kwargs = {'name': name,
                      'dest': destination,
                      'gateway': gateway,
                      'route_to_edit': str(name)}

            self._cli.routeconfig(ip_prot).edit(**kwargs)
        else:
            raise ValueError('Name is mandatory parameter.')

    def route_config_delete(self, ip_prot='ipv4',
                            name=None):
        """Remove a route.

        routeconfig > delete

        Parameters:
        - `ip_prot` : ip protocol ipv4 or ipv6. Default is ipv4
        - `name`: name of the route. Specify 'delete_all' to
            clear all routes.

        Examples:
        | Route Config Edit | name=test1 |
        | Route Config Edit | name=test2 |
        """
        if name is not None:
            kwargs = {'route_to_delete': str(name)}
            self._cli.routeconfig(ip_prot).delete(**kwargs)
        else:
            raise ValueError('Name is mandatory parameter.')

    def route_config_clear(self, ip_prot='ipv4'):
        """Remove a route.

        routeconfig > clear

        Parameters:
        - `ip_prot` : ip protocol ipv4 or ipv6. Default is ipv4

        Examples:
        | Route Config Clear |
        """

        self._cli.routeconfig(ip_prot).clear()

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
