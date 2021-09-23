#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/incomingrelayconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class incomingrelayconfig(CliKeywordBase):
    """
    cli -> incomingrelayconfig

    Configure incoming relays.
    """

    def get_keyword_names(self):
        return ['incoming_relay_config_setup',
                'incoming_relay_config_relay_list_new',
                'incoming_relay_config_relay_list_delete',
                'incoming_relay_config_relay_list_print',
                'incoming_relay_config_relay_list_edit_name',
                'incoming_relay_config_relay_list_edit_host',
                'incoming_relay_config_relay_list_edit_type',
                'incoming_relay_config_relay_list_edit_match',
                'incoming_relay_config_relay_list_edit_position',
                'incoming_relay_config_relay_list_edit_header']

    def incoming_relay_config_setup(self, enable_relays='No'):
        """Enable/disable incoming relays

        incomingrelayconfig -> setup

        *Parameters:*
        - `enable_relays`: enable and define incoming relays, yes or no

        *Examples:*
        | Relay Config Setup | enable_relays=Yes |
        """
        self._cli.incomingrelayconfig().setup(enable_relays)

    def incoming_relay_config_relay_list_new(self, relay_name, *args):
        """Create new incoming relay

        incomingrelayconfig -> relaylist -> new

        *Parameters:*
        - `relay_name`: a name for incoming relay
        - `address`: the IP address of the incoming relay. IPv4 and IPv6
        addresses are supported. For IPv4, CIDR format subnets such as 10.1.1.0/24,
        IP address ranges such as 10.1.1.10-20, and subnets such as 10.2.3. are allowed.
        For IPv6, CIDR format subnets such as 2001:db8::/32 and IP address ranges such
        as 2001:db8::1-2001:db8::11 are allowed.
        Hostnames such as crm.example.com and partial hostnames such as .example.com
        are allowed.
        This parameter is mandatory.
        - `header_type`: whether to use the "Received:" header or a custom header to
        determine the originating IP address:
        | 1 | Use "Received:" header |
        | 2 | Use a custom header |
        - `custom_header_name`: the custom header name that contains the originating
        IP address
        - `special_character: within the "Received:" header, the special character or
        string after which to begin parsing for the originating IP address, 'from'
        by default
        - `received_header_position`: within the headers, the position of the
        "Received:" header that contains the originating IP address, 1 by default

        *Return:*
        Raw output

        *Examples:*
        | Relay Config Relay List New | first-hop | address=1.1.1.1 |
        | ... | header_type=Use a custom header | custom_header_name=X-Custom |
        | Relay Config Relay List New | second-hop | address=2.2.2.2 |
        | ... | header_type=Use "Received:" header |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.incomingrelayconfig().relaylist().new(relay_name=relay_name,
                                                               **kwargs)

    def incoming_relay_config_relay_list_delete(self, relay_name_or_number):
        """Delete existing incoming relay

        incomingrelayconfig -> relaylist -> delete

        *Parameters:*
        - `relay_name_or_number`: a name or number (got from PRINT command)
        of incoming relay to be deleted

        *Examples:*
        | Relay Config Relay List Delete | first-hop |
        """
        self._cli.incomingrelayconfig().relaylist().delete(relay_name_or_number)

    def incoming_relay_config_relay_list_print(self):
        """Print the incoming relays list

        incomingrelayconfig -> relaylist -> print

        *Return:*
        Raw output

        *Examples:*
        | ${all_relays}= | Relay Config Relay List Print |
        | Log | ${all_relays} |
        """
        return self._cli.incomingrelayconfig().relaylist().print_table()

    def incoming_relay_config_relay_list_edit_name(self, relay_name_or_number, new_name=''):
        """Edit the name of particular relay list entry

        incomingrelayconfig -> relaylist -> edit -> name

        *Parameters:*
        - `relay_name_or_number`: a name or number (got from PRINT command)
        of incoming relay to be deleted.
        - `new_name`: new name for an incoming relay. Leaving it blank will not
        change an old name

        *Examples:*
        | Relay Config Relay List Edit Name | first-hop | very-first-hop |
        """
        self._cli.incomingrelayconfig().relaylist().edit(entry=relay_name_or_number). \
            name(new_name)

    def incoming_relay_config_relay_list_edit_host(self, relay_name_or_number, new_host=''):
        """Edit the host of particular relay list entry

        incomingrelayconfig -> relaylist -> edit -> host

        *Parameters:*
        - `relay_name_or_number`: a name or number (got from PRINT command)
        of incoming relay to be deleted.
        - `new_host`: new host name for an incoming relay. Leaving it blank will not
        change an old host

        *Examples:*
        | Relay Config Relay List Edit Host | first-hop | pentagon.mil |
        """
        self._cli.incomingrelayconfig().relaylist().edit(entry=relay_name_or_number). \
            host(new_host)

    def incoming_relay_config_relay_list_edit_type(self, relay_name_or_number, *args):
        """Edit the type of particular relay list entry

        incomingrelayconfig -> relaylist -> edit -> host

        *Parameters:*
        - `relay_name_or_number`: a name or number (got from PRINT command)
        of incoming relay to be deleted.
        - `header_type`: whether to use the "Received:" header or a custom header to
        determine the originating IP address:
        | 1 | Use "Received:" header |
        | 2 | Use a custom header |
        Leaving it blank will not change an old type
        - `custom_header_name`: the custom header name that contains the originating
        IP address
        - `special_character: within the "Received:" header, the special character or
        string after which to begin parsing for the originating IP address, 'from'
        by default
        - `received_header_position`: within the headers, the position of the
        "Received:" header that contains the originating IP address, 1 by default

        *Return:*
        Raw output

        *Examples:*
        | Relay Config Relay List Edit Type | first-hop | header_type=Use a custom header |
        | ... | custom_header_name=My custom header |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.incomingrelayconfig().relaylist().edit(entry=relay_name_or_number). \
            type(**kwargs)

    def incoming_relay_config_relay_list_edit_match(self, relay_name_or_number,
                                                    special_character=''):
        """Edit the special character of particular relay list entry
        having type "Use a custom header"

        incomingrelayconfig -> relaylist -> edit -> match

        *Parameters:*
        - `relay_name_or_number`: a name or number (got from PRINT command)
        of incoming relay to be deleted.
        - `special_character: within the "Received:" header, the special character or
        string after which to begin parsing for the originating IP address.
        Leaving it blank will not change an old value

        *Examples:*
        | Relay Config Relay List Edit Match | first-hop | to |
        """
        self._cli.incomingrelayconfig().relaylist().edit(entry=relay_name_or_number). \
            match(special_character)

    def incoming_relay_config_relay_list_edit_position(self, relay_name_or_number,
                                                       received_header_position=''):
        """Edit the received header position of particular relay list entry
        having type "Use a custom header"

        incomingrelayconfig -> relaylist -> edit -> position

        *Parameters*
        - `relay_name_or_number`: a name or number (got from PRINT command)
        of incoming relay to be deleted.
        - `received_header_position`: within the headers, the position of the
        "Received:" header that contains the originating IP address.
        Leaving it blank will not change an old value

        *Examples*
        | Relay Config Relay List Edit Position | first-hop | 2 |
        """
        self._cli.incomingrelayconfig().relaylist().edit(entry=relay_name_or_number). \
            position(received_header_position)

    def incoming_relay_config_relay_list_edit_header(self, relay_name_or_number,
                                                     custom_header_name=''):
        """Edit the custom header name that contains the originating
        IP address of particular relay list entry having type
        'Use "Received:" header'

        incomingrelayconfig -> relaylist -> edit -> header

        *Parameters:*
        - `relay_name_or_number`: a name or number (got from PRINT command)
        of incoming relay to be deleted.
        - `custom_header_name`: the custom header name that contains the originating
        IP address
        Leaving it blank will not change an old value

        *Examples:*
        | Relay Config Relay List Edit Header | first-hop | 2 |
        """
        self._cli.incomingrelayconfig().relaylist().edit(entry=relay_name_or_number). \
            header(custom_header_name)
