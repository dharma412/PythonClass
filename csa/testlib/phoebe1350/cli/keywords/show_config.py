#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/show_config.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class ShowConfig(CliKeywordBase):
    """Shows the current system configuration."""

    def get_keyword_names(self):
        return ['show_config']

    def show_config(self, option='no'):
        """Shows the current system configuration.
        This does not include uncommitted changes.

        showconfig

        Parameters:
        - `option`: Five options are available.

                    1. yes : Show Config file with masked passwords.

                    2. no : Passwords in the config file are not masked.

                    3. mask_pw : view Config file with masked passwords.

                    4. encrypt_pw : view Config file with encrypted passwords.

        Examples:
        | ${result}= | Show Config |
        | Log | ${result} |

        | ${result}= | Show Config | no |
        | Log | ${result} |

        | ${result}= | Show Config | yes |
        | Log | ${result} |

        | ${result}= | Show Config | mask_pw |
        | Log | ${result} |

        | ${result}= | Show Config | encrypt_pw |
        | Log | ${result} |

        """

        dict_options = {'yes': 1,
                        'no': 2,
                        'mask_pw': 1,
                        'encrypt_pw': 2}

        return self._cli.showconfig(option = dict_options[option])
