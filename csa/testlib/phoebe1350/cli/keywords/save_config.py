#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase


class SaveConfig(CliKeywordBase):
    """Saves the current configuration to disk.

    Please be aware that a configuration with a masked password can not be
    reloaded with loadconfig command.
    """

    def get_keyword_names(self):
        return ['save_config',
                ]

    def save_config(self, option='no'):
        """Saves the current configuration to disk.

        Parameters:
        - `option`: Five options are available.

                    1. yes : Config file is generated with masked passwords.

                    2. no : Passwords in the generated config file are not masked.

                    3. mask_pw : Masks the passwords in the generated config file.
                               Files with masked passwords cannot be loaded using
                               loadconfig command.

                    4. encrypt_pw : Encrypts the passwords in the generated config file.

        Examples:
        | ${result}= | Save Config |
        | Log | ${result} |

        | ${result}= | Save Config | no |
        | Log | ${result} |

        | ${result}= | Save Config | yes |
        | Log | ${result} |

        | ${result}= | Save Config | mask_pw |
        | Log | ${result} |

        | ${result}= | Save Config | encrypt_pw |
        | Log | ${result} |


        Returns:
        - name of the saved configuration file
        """

        dict_options = {'yes': 1,
                        'no': 2,
                        'mask_pw': 1,
                        'encrypt_pw': 2,
                       }
        return self._cli.saveconfig(option = dict_options[option])
