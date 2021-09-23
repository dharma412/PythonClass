#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/feature_key.py#1 $

from common.cli.clicommon import CliKeywordBase

class FeatureKey(CliKeywordBase):
    """The featurekey command is an administrative tool to provide specific
       functionality on your system
    """

    def get_keyword_names(self):
        return [
                'feature_key_activate',
                'feature_key_checknow',
                'feature_key_list',
               ]

    def feature_key_activate(self, key):
        """activates given feature key

        featurekey > activate

        Parameters:
        - `key`: the key to activate

        Example:
        | Feature key Activate | PJUA6-GxXVn-ZLWBH-kshuk-qYgy5-dM8cs-77Jg=-= |

        """
        self._cli.featurekey().activate(key)

    def feature_key_checknow(self):
        """check now for new feature keys and returns dictionary of new
           feature keys

        featurekey > checknow

        Example:
        | Feature key Checknow |

        """
        output = self._cli.featurekey().checknow()
        self._info(output)
        return output

    def feature_key_list(self):
        """all feature keys list

        featurekey > list

        Example:
        | Feature key list |

        """
        output = self._cli.featurekey().list()
        self._info(output)
        return output
