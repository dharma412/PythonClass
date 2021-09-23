# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/beaker_config.py#1 $
# $DateTime: 2020/01/17 04:04:23 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase

class BeakerConfig(CliKeywordBase):
    """Configure beaker streamline configuration settings"""

    def get_keyword_names(self):
        return ['beaker_config_setup']

    def beaker_config_setup(self, server_type=None):
        """
        Keyword to configure beaker streamline server

        beakerconfig > setup

        Parameters:
        - `server_type`: Provide the server for streamline service configuration
                         "Stage Server" OR "Production Server"

        Examples:
        | Beaker Config Setup | server_type=Stage Server |
        | Beaker Config Setup | server_type=Production Server |
        """
        self._cli.beakerconfig().setup(server_type)
