#!/usr/bin/env python -tt
from common.cli.clicommon import CliKeywordBase
import re

class Talosconfig(CliKeywordBase):
    """
    cli -> talosconfig
    Configure talos
    """
    def get_keyword_names(self):
        return ['talosconfig_setup',
                'talosconfig_status',
                'talosconfig_customserver']

    def talosconfig_setup(self,server=None):
        """Setup talosconfig to Production or Stage server
           talosconfig -> setup

        *Parameters:*
        - `server`: Provide the server for streamline service configuration
           wheter you want to point to Stage server or Production Server

        *Examples:*
        | TalosConfig Setup | server=Production Server |
        | TalosConfig Setup | server=Stage server |
        """
        self._cli.talosconfig().setup(server)

    def talosconfig_customserver(self, url=None):
        """Setup talosconfig to customserver
           talosconfig -> customserver -> url
        *Parameters:*
        - `url`: Enter the streamline service configuration URL for beaker
        *Examples:*
        | TalosConfig Customserver | url=url1 |
        """
        self._cli.talosconfig().customserver(url)

    def talosconfig_status(self):
        """This keyword to get the current Configured server for talos
        *Return:*
        Production_server or Stage_server
        *Examples:*
        $status=    |TalosConfig Status|
        """
        return self._cli.talosconfig().status()
