#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/feature_key_config.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class FeatureKeyConfig(CliKeywordBase):
    """Keywords for featurekeyconfig CLI command"""

    def get_keyword_names(self):
        return ['feature_key_config_setup']

    def feature_key_config_setup(self, autoactivate=None, autocheck=None):
        """Configure feature key settings.

        Parameters:
        - `autoactivate`: set automatic activation of downloaded keys to either
           'yes', 'no', or 'default'
        - `autocheck`: automatic checking for new feature keys to either
           'yes', 'no', or 'default'

        Examples:
        | FeatureKeyConfig Setup | autoactivate=yes  |
        | FeatureKeyConfig Setup | autoactivate=no |
        | FeatureKeyConfig Setup | autoactivate=default |
        | FeatureKeyConfig Setup | autocheck=yes  |
        | FeatureKeyConfig Setup | autocheck=no |
        | FeatureKeyConfig Setup | autocheck=default |
        | FeatureKeyConfig Setup | autoactivate=yes  | autocheck=yes  |
        | FeatureKeyConfig Setup | autoactivate=no | autocheck=yes  |
        | FeatureKeyConfig Setup | autoactivate=yes  | autocheck=no |
        | FeatureKeyConfig Setup | autoactivate=no | autocheck=no |
        """
        if autoactivate is not None:
            self._info("Setting AUTOACTIVATE to '" + str(autoactivate) + "'")
            self._cli.featurekeyconfig().setup().autoactivate \
                (self._process_yes_no(autoactivate))

        if autocheck is not None:
            self._info("Setting AUTOCHECK to '" + str(autocheck) + "'")
            self._cli.featurekeyconfig().setup().autocheck \
                (self._process_yes_no(autocheck))
