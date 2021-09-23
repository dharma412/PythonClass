#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/dns_server.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.util.utilcommon import UtilCommon
import sal.servers.bind as bind


class DnsServer(UtilCommon):
    """
    Keywords for Adding zone files and reload the bind server
    """

    SERVERS_CACHE = {}

    def get_keyword_names(self):
        return [
            'dns_server_start',
            'dns_server_stop',
            'dns_server_restart',
            'dns_server_reload',
        ]

    def _get_server_obj(self, hostname):
        if not self.SERVERS_CACHE.has_key(hostname):
            self.SERVERS_CACHE[hostname] = bind.BindServerManager(hostname)
        return self.SERVERS_CACHE[hostname]

    def dns_server_start(self, hostname):
        """
        if not already started starts server with the command
           sudo /usr/sbin/named -t /var/named -u bind

        created the following dir if not already present
        /etc/namedb/master

        *Parameters*
        - `hostname`: host  on which you want to configure dns. String

        *Example*
        | dns server start |
        """

        self._get_server_obj(hostname).start()

    def dns_server_restart(self, hostname):
        """
        Stops server
        and starts server with the command
           sudo /usr/sbin/named -t /var/named -u bind

        created the following dir if not already present
        /etc/namedb/master

        *Parameters*
        - `hostname`: host  on which you want to configure dns. String

        *Example*
        | dns server restart |
        """
        self._get_server_obj(hostname).restart()

    def dns_server_reload(self, hostname):
        """
        reloads dns if already present
           sudo rndc reload
        if not started starts server with the command
           sudo /usr/sbin/named -t /var/named -u bind

        created the following dir if not already present
        /etc/namedb/master

        *Parameters*
        - `hostname`: host  on which you want to configure dns. String

        *Example*
         | dns server reload |
        """
        self._get_server_obj(hostname).reload()

    def dns_server_stop(self, hostname):
        """
        Stops dns server from running

        *Parameters*
        - `hostname`: host  on which you want to configure dns. String

        *Example*
         | dns server stop |
        """
        self._get_server_obj(hostname).stop()
