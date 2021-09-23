#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/save_config.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class SaveConfig(CliKeywordBase):
    """Saves the current configuration to disk.

    Please be aware that a configuration with a masked password can not be
    reloaded with loadconfig command.
    """

    def get_keyword_names(self):
        return ['save_config',
                ]

    def save_config(self,
                    mask_pw='no',
                    ):
        """Saves the current configuration to disk.

        Parameters:
        - `mask_pw`: Either 'yes' or 'no'. Indicates whether password should
        be masked. Files with masked passwords cannot be loaded using
        loadconfig command

        Examples:
        | ${result}= | Save Config |
        | Log | ${result} |

        | ${result}= | Save Config | no |
        | Log | ${result} |

        Returns:
        - name of the saved configuration file
        """

        mask_pw = self._process_yes_no(mask_pw)

        output = self._cli.saveconfig(mask_pw)
        return output
