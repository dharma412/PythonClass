#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/feature_key.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class FeatureKey(CliKeywordBase):

    """The featurekey command is an administrative tool to provide specific
       functionality on your system
    """

    def get_keyword_names(self):
        return [
                'feature_key_activate',
                'feature_key_checknow',
                'feature_key_list'
               ]

    def feature_key_activate(self, key):
        """Activate given feature key.

        featurekey > activate

        Parameters:
        - `key`: the key to activate

        Example:
        | Feature Key Activate | PJUA6-GxXVn-ZLWBH-kshuk-qYgy5-dM8cs-77Jg=-= |
        """
        self._cli.featurekey().activate(key)

    def feature_key_checknow(self):
        """Check now for new feature keys.

        featurekey > checknow

        Return:
        A string of comma-separated values of new keys in 'keyname:fkey_string'
        format.

        Example:
        | Feature Key Checknow |
        """
        output = self._cli.featurekey().checknow()
        result = ','.join(':'.join(entry) for entry in output.iteritems())
        self._info(result)
        return result

    def feature_key_list(self):
        """List all feature keys.

        Return:
        An output of 'featurekey list' CLI batch command.

        Example:
        | Feature Key List |
        """
        output = self._cli.featurekey(batch_cmd='list')
        self._info(output)
        return output
