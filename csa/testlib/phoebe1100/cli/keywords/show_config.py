#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/show_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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

                    5. plain_pw : view Config file with plain passwords.

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

        | ${result}= | Show Config | plain_pw |
        | Log | ${result} |

        """

        dict_options = {'yes': 1,
                        'no': 3,
                        'mask_pw': 1,
                        'encrypt_pw': 2,
                        'plain_pw': 3}

        return self._cli.showconfig(option=dict_options[option])
