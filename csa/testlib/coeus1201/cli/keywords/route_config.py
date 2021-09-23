#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/route_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class RouteConfig(CliKeywordBase):
    """The routeconfig command controls the IP routing tables."""

    def get_keyword_names(self):

        return [
            'route_config_new',
            'route_config_edit',
            'route_config_delete',
        ]

    def route_config_new(self,
                         name=None,
                         destination=DEFAULT,
                         gateway=DEFAULT,
                         table=DEFAULT,
                         protocol=DEFAULT
                         ):
        """Create a new route.

        routeconfig > new

        Parameters:
        - `protocol`: choose ip protocol. Either 'IPv4' or 'IPv6'. None to use default value.
        - `table`: choose a routing table. Either 'Management' or 'Data'.
        - `name`: name of the route.
        - `destination`: IP or CIDR address to match for
            outgoing IP traffic. The destination cannot already
            be defined by another route.
        - `gateway`: IP address to send this traffic to.

        Examples:
        | Route Config New | table=Management | name=test1 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        | Route Config New | protocol=IPv4 | table=Data | name=test2 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        | Route Config New | protocol=IPv6 | table=Management | name=test3 | destination=fc22::/20 | gateway=fc02::5 |
        """

        if name is None:
            raise ValueError('Name is mandatory parameter.')

        kwargs = {'name': name,
                  'dest': destination,
                  'gateway': gateway}

        if protocol == DEFAULT or protocol.lower() == 'ipv4':
            cli_state = self._cli.routeconfig().ipv4()
        elif protocol.lower() == 'ipv6':
            cli_state = self._cli.routeconfig().ipv6()
        else:
            raise ValueError('Protocol must be IPv4 or IPv6')

        if table.lower() == 'management':
            cli_state = cli_state.management()
        elif table.lower() == 'data':
            cli_state = cli_state.data()
        else:
            raise ValueError('Routing table must be Management or Data')

        cli_state.new(**kwargs)

    def route_config_edit(self,
                          name=None,
                          new_name=DEFAULT,
                          destination=DEFAULT,
                          gateway=DEFAULT,
                          table=None,
                          protocol=DEFAULT):
        """Modify a route.

        routeconfig > edit

        Parameters:
        - `protocol`: choose ip protocol. Either 'IPv4' or 'IPv6'.
        - `table`: choose a routing table. Either 'Management' or 'Data'.
        - `name`: name of the route.
        - `new_name`: new name for the route.
        - `destination`: IP or CIDR address to match for
            outgoing IP traffic. The destination cannot already
            be defined by another route.
        - `gateway`: IP address to send this traffic to.

        Examples:
        | Route Config Edit | table=Management | name=test1 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        | Route Config Edit | protocol=IPv4 | table=Data | name=test2 | destination=192.168.42.0/24 | gateway=10.7.8.1 |
        | Route Config Edit | protocol=IPv6 | table=Data | name=test3 | destination=fc22::/24 | gateway=fc02::1 |
        | Route Config Edit | protocol=IPv6 | table=Data | name=test3 | new_name=myroute | destination=fc22::/14 | gateway=fc02::8 |
        """

        if name is None:
            raise ValueError('Name is mandatory parameter.')

        kwargs = {'new_name' : new_name,
                  'dest': destination,
                  'gateway': gateway,
                  'route_to_edit': str(name)}
        if protocol == DEFAULT or protocol.lower() == 'ipv4':
            cli_state = self._cli.routeconfig().ipv4()
        elif protocol.lower() == 'ipv6':
            cli_state = self._cli.routeconfig().ipv6()
        else:
            raise ValueError('Protocol must be IPv4 or IPv6')

        if table.lower() == 'management':
            cli_state = cli_state.management()
        elif table.lower() == 'data':
            cli_state = cli_state.data()
        else:
            raise ValueError('Routing table must be Management or Data')

        cli_state.edit(**kwargs)

    def route_config_delete(self,
                            name=None,
                            table=None,
                            protocol=DEFAULT):
        """Remove a route.

        routeconfig > delete

        Parameters:
        - `protocol`: choose ip protocol. Either 'IPv4' or 'IPv6'.
        - `table`: choose a routing table. Either 'Management' or 'Data'.
        - `name`: name of the route. Specify 'delete_all' to
            clear all routes.

        Examples:
        | Route Config Delete | name=test1 |
        | Route Config Delete | protocol=IPv4 | table=Data | name=delete_all | #to delete all IPv4 routes |
        | Route Config Delete | protocol=IPv6 | table=Data | name=test3 |
        """

        if name is None:
            raise ValueError('Name is mandatory parameter.')

        kwargs = {'route_to_delete': str(name)}
        if protocol == DEFAULT or protocol.lower() == 'ipv4':
            cli_state = self._cli.routeconfig().ipv4()
        elif protocol.lower() == 'ipv6':
            cli_state = self._cli.routeconfig().ipv6()
        else:
            raise ValueError('Protocol must be IPv4 or IPv6')

        if table.lower() == 'management':
            cli_state = cli_state.management()
        elif table.lower() == 'data':
            cli_state = cli_state.data()
        else:
            raise ValueError('Routing table must be Management or Data')

        if name.strip().lower() == 'delete_all':
            cli_state.clear()
        else:
            cli_state.delete(**kwargs)
