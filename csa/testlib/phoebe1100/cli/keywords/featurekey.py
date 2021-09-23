#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/featurekey.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class FeatureKey(CliKeywordBase):
    """The featurekey command is an administrative tool to provide specific
       functionality on your system
    """

    def get_keyword_names(self):
        return [
            'feature_key_list',
            'feature_key_activate',
            'feature_key_checknow'
        ]

    def feature_key_list(self, key_str):
        """Returns installed featurekey.

        *Parameters*:
        - `key_str`: String to search the key

        *Exceptions*:
            - assert if no keysting given

        *Examples*:

        | Feature key List | Bounce Verification |

        """

        return self._cli.featurekey().get_featurekey(key_str)

    def feature_key_activate(self, key=None, pendingkey=None):
        """activates given feature key

        featurekey > activate

        *Parameters*:
        - `key`: the key to activate
        - `pendingkey`: the pending key to activate, can be int(index) or str(key)

        *Examples*:
        | Feature key Activate | PJUA6-GxXVn-ZLWBH-kshuk-qYgy5-dM8cs-77Jg=-= |

        """

        self._cli.featurekey().activate(key, pendingkey)

    def feature_key_checknow(self):
        """Checks, if there are some pending keys

        featurekey > check for new keys

        Parameter:
        None

        Return:
            Dictionary of pending keys. Dictionary will be empty if there
            are no pending keys

        *Examples*:
        | Feature Key Checknow |  |

        """

        self._cli.featurekey().checknow()
