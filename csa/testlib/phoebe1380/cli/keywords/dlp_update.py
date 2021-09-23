#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/dlp_update.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class DLPUpdate(CliKeywordBase):
    """
    cli -> dlpupdate
    """

    def get_keyword_names(self):
        return ['dlp_update',
                'dlp_update_setup',
                'dlp_update_is_enabled',]

    def dlp_update(self, force=False):
        """
        CLI command: dlpupdate

        *Parameters*:
        - `force`: Force update or not.

        *Examples*:
        | ${res}= | Dlp Update |
        | Log | ${res} |

        *Return*:
        CLI response. String.
        """
        return self._cli.dlpupdate(force=force)

    def dlp_update_setup(self, enable_auto_update=None):
        """
        CLI command: dlpupdate > setup

        *Parameters*:
        - `enable_auto_update`: Enable update. YES or NO. Use keyword `Dlp Update Is Enabled` to get current status.

        *Examples*:
        | Dlp Update Setup | enable_auto_update=yes |

        *Return*:
        CLI response. String.
        """
        return self._cli.dlpupdate(self_hook=True).setup(enable_auto_update=enable_auto_update)

    def dlp_update_is_enabled(self):
        """
        CLI command: dlpupdate

        *Examples*:
        | ${res}= | Dlp Update Is Enabled |
        | Run Keyword If | not ${res} |
        | ... | Dlp Update Setup | enable_auto_update=yes |

        *Return*:
        Boolean. True if automatic update is enabled, False otherwise.
        """
        return self._cli.dlpupdate(self_hook=True).is_enabled()
