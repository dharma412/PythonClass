#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/dns_client.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.util.utilcommon import UtilCommon
import sal.servers.bind as bind
from common.util.connectioncache import ConnectionCache

import shlex
import atexit


class DnsClient(UtilCommon):
    """
    Keywords for creating dns records and zone.
    """

    _cache = ConnectionCache(no_current_msg="No connected DNS clients")

    def get_keyword_names(self):
        return [
            'dns_client_connect',
            'dns_client_preserve_config',
            'dns_client_restore_config',
            'dns_client_create_zone',
            'dns_client_update_record',
            'dns_client_remove_record',
            'dns_client_switch',
            'dns_client_build_zones',
            'dns_client_update_zones',
            'dns_client_is_valid_named',
            'dns_client_is_valid_named_with_zones',
            'dns_client_is_valid_zone',
            'dns_client_disconnect'
        ]

    def dns_client_connect(self, hostname, alias=None, should_preserve_server_config=True):
        """ Make connection to Bind Server

        *Parameters*
        - `hostname`: host to which you want to connect. String.
        - `alias`: identificator of this connection.
        - `should_preserve_server_config`: whether to preserve existing Bind
        on connect and restore it on disconnect. ${True} by default

        *Return*
            Index of connection

        *Examples*
        | Dns Client Connect | qa42.qa | qa42.qa

        """
        return self._cache.register(bind.BindServerManager(hostname, should_preserve_server_config), alias)

    def dns_client_preserve_config(self):
        """ The current state of named.conf file is preserved
        sudo rm /tmp/named.conf.original
        sudo cp /etc/namedb/named.conf /tmp/named.conf.original

        *Parameters*
         None

        *Examples*
        | Dns Client Preserve Config |
        """
        self._cache.current.preserve_config()

    def dns_client_restore_config(self):
        """ Restores named.conf file which was preserved using
            dns client preserve config keyword
        sudo cp /tmp/named.conf.original /etc/namedb/named.conf

        *Parameters*
         None

        *Examples*
        | Dns Client Restore Config |
        """
        self._cache.current.restore_config()

    def dns_client_create_zone(self, domain):
        """ Creates a zone and returns zone object

        *Parameters*
        - `domain` : Name of the domain/zone. String


        *Examples*
        | Dns Client Create Zone | somedomain.com |

         """
        return self._cache.current.create_zone(domain)

    def dns_client_switch(self, alias):
        """
        Switch current connection.

        *Parameters*
         - `alias`: string wich will indicate this connection. String.

        *Exceptions*
         - ValueError: if provided alias wich doesn't excist.

        *Example*
        | DNS Client Switch | client1 |
        | ${index} | DNS CLient connect | qa42.qa |
        | DNS Client Switch | ${index} |
        """

        self._cache.switch(alias)

    def dns_client_disconnect(self):
        """
        Disconnect from DNS server
        After this opperation current active
        session will be changed to the previous connected. It is strongly
        recomend switch session manualy after running this keyword.

        *Parameters*
            None

        *Example*
        | DNS Client Disconnect |
        """
        return self._cache.current.disconnect()

    def dns_client_update_record(self, zone=None, *args):
        """
        Updates  a record to a Zone.
        Modifies if the record already exists


        *Parameters*
         - `zone`: Zone object returned by `Dns Client Create Zone` keyword . Mandatory
         - `recordname`:  name of the record. Mandatory
         - `recordtype`: Type of the record. Possible Values 'SOA', 'A', 'NS', 'CNAME', 'MX', 'TXT'
                         SOA - start of zone authority
                         NS - an authoritative name server
                         A -  a host address
                         AAAA - IPV6 host address
                         CNAME - the canonical name for an alias
                         MX -  mail exchanger


         if recordtype is 'SOA'
         - `mname` : the SOA MNAME (master name) field . Mandatory
         - `rname` : the SOA RNAME (responsible name) field . Mandatory
         - `serial` : The zone's serial number . Default 100
         - `refresh` : The zone's refresh value (in seconds)  . Default 200
         - `retry` : The zone's retry value (in seconds)  . Default 300
         - `expire` : The zone's expiration value (in seconds)  . Default 400
         - `minimum` : The zone's negative caching time (in seconds) . Default 500

         if recordtype is 'A'
         - `address` : an IPv4 address . Mandatory

         if recordtype is 'AAAA'
         - `address` : an IPv6 address . Mandatory

         if recordtype is 'NS'
         - `target` : the target name of the rdata Mandatory. Example = ns1 or ns1.somedomain.com

         if recordtype is 'CNAME'
         - `target` : the target name of the rdata Mandatory. Example = ns1 or ns1.somedomain.com

         if recordtype is 'MX'
         - `preference` : the preference value . Default is 1
         - `exchange` : the exchange name  . Mandatory

         if recordtype is 'TXT'
         Either
         - `strings` : the text strings. Mandatory
         or
         - `txtobject` :  string record returned from dnstxt command


        *Example*
        | dns client update record  | ${zone1} | recordname=@ |  recordtype=SOA |   mname=ns1.pl.sma | rname=admin.pl.sma |
        | dns client update record  | ${zone1} | recordname=ns |  recordtype=A  |  address=10.92.153.33 |
        | dns client update record  | ${zone1} |  recordname=@ | recordtype=NS | target=ns |
        | dns client update record  | ${zone1} | recordname=@  | recordtype=MX | preference=2 | exchange=mail |
        | dns client update record  | ${zone1} | recordname=mail | recordtype=A | address=3.3.3.3 |
        | dns client update record  | ${zone1} | txtobject=default._domainkey.pl.sma. IN TXT "v=DKIM1; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDKLq0ndYkZu41jL8lpurvnqgnxYL5A9P+WdhdvMiayN0Usg//Y/AzLcLcK70jpHvrs6NE3w+hXX5llaUXy/sbmwQ4GbNFb9GgKnBvg5MMGQ2NZPyqEaxWPULEcZDkW9OFU0vTkYnppItSmoZ7clv7SzQJP6QtwSDZk7shTMtESxQIDAQAB;" |
        | dns client update record  | ${zone1} | recordname=www |  recordtype=CNAME  | target=@ |

        """
        kwargs = self._parse_args(args)

        if kwargs.has_key('preference'):
            kwargs['preference'] = int(kwargs.pop('preference'))

        if kwargs.has_key('txtobject'):
            txtobj = kwargs.pop('txtobject')
            txtobjlist = shlex.split(txtobj)
            kwargs['recordname'] = txtobjlist[0].rstrip('.')
            kwargs['recordtype'] = 'TXT'
            kwargs['strings'] = txtobjlist[3]
        self._cache.current.update_record(zone, **kwargs)

    def dns_client_remove_record(self, zone=None, *args):
        """
        Remove a record from the zone
        An A record or address record.

        *Parameters*
         - `zone`: Zone object returned by `Dns Client Create Zone` keyword . Mandatory
         - `recordname`:  name of the record. Mandatory
         - `recordtype`: Type of the record. Possible Values 'SOA', 'A', 'AAAA', 'NS', 'CNAME', 'MX', 'TXT'

        *Example*
         | dns client remove record |  ${zone1} |  recordname=mail | recordtype=A |
        """
        kwargs = self._parse_args(args)

        self._cache.current.remove_record(zone, **kwargs)

    def dns_client_build_zones(self, *args):
        """
        Writes the zone object to a file . /tmp/'zonename'.db

        *Parameters*
         - Zone objects returned by `dns client create zone` keyword
         multiple zone objects can be passed

        *Example*
         | dns client build zones | ${zone1} | ${zone2} |
        """

        for zone in args:
            self._cache.current.build_zones(zone)

    def dns_client_update_zones(self, should_preserve_zones=True, *args):
        """
        Update the zone to the bind config.
        Adds the zone entry in named.conf
        Copies the zone file to the /etc/namedb/master/*.db location

        *Parameters*
         - First argument is should_preserve_zones . Takes ${True} or ${False}
           When set to True will preserve previosly updates zones in the same connection
           else it will erase those zones
         - Zone objects returned by `dns client create zone` keyword
         multiple zone objects can be passed

        *Return*
         None

        *Example*
         | dns client update zones | ${True} | ${zone1} | ${zone2} |
         """

        for zone in args:
            self._cache.current.build_zones(zone)
        self._cache.current.update_zones(should_preserve_zones, *args)

    def dns_client_is_valid_named(self):
        """
        named-checkconf - named configuration file syntax checking tool
        checks the syntax, but not the semantics, of a named configuration file
        Runs
        'sudo named-checkconf '
        and returns output

        *Parameters*
         None

        *Exceptions*
         - `SyntaxError` - It means the named.conf file validity check failed and
                       output of the named-checkconf is logged for reference

        *Example*
         | dns client is valid named |
        """
        return self._cache.current.is_valid_named()

    def dns_client_is_valid_named_with_zones(self):
        """
        named-checkconf - named configuration file syntax checking tool
        Runs
        'sudo named-checkconf -z'
        and returns output
        Performs a check and loads the master zone files found in the named.conf file

        *Parameters*
         None

        *Return*
         True or False indicating Success or Failure

        *Exceptions*
         - `SyntaxError` - It means the named.conf file validity check failed and
                       output of the named-checkconf -z is logged for reference

        *Example*
         | dns client is valid named with zones|
        """
        return self._cache.current.is_valid_named_with_zones()

    def dns_client_is_valid_zone(self, zonename, filename):
        """
        zone file validity checking or converting tool

        Runs 'sudo named-checkzone zonename filename'
        command and returns output

        *Parameters*
        - `zonename` : name of the zone . String . Mandatory
        - `filename` : name of the file - Sting. Mandatory

        *Return*
        True or False indicating Success or Failure

        *Exceptions*
         - `SyntaxError` - It means the named.conf file validity check failed and
                       output of the named-checkzone is logged for reference

        *Example*
         | dns client is valid zone | pl.sma | /etc/namedb/master/pl.sma.db

        """
        return self._cache.current.is_valid_zone(zonename, filename)


def close_pending_connections():
    all_connections = DnsClient._cache.get_all_current()
    connections_to_close = filter(lambda x: x.is_connected, all_connections)
    map(lambda x: x.disconnect(), connections_to_close)


atexit.register(close_pending_connections)
