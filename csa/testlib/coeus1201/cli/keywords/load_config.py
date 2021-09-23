#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/load_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase

class LoadConfig(CliKeywordBase):
    """
    cli -> loadconfig

    Loads the XML configuration from a file.  Not available on
    clustered machines.

    Please be aware that a configuration created without passwords will fail
    when trying to reload.
    """

    def get_keyword_names(self):
        return [
            'load_config',
        ]

    def load_config(self, name, clear_net_settings='Y'):
        """Loads XML configuration from a file

        Parameters:
        - `name`: name of the XML configuration file.
        - `clear_net_settings`: - answer to question:
         "Do you want to load network settings?" [N]>
         accepted answers are 'Y' and 'N'

        NOTE: The configuration filename must start with a letter, number, or
        underscore, followed by letters, numbers, underscores, or hyphens, and
        can have a maximum of 251 characters. Spaces are not permitted within
        the filename. The filename cannot have any extensions other than ".xml"

        Return value:
        - True if there are changes to commit
        - False if there are no changes to commit

        Exceptions:
        - ConfigError, "loadconfig: Parse of config file failed.
        - ConfigError, "loadconfig: No configuration data entered.
        - ConfigError, "loadconfig: Config filename does not exist.

        Examples:

        | Save and load configuration with a custom name |
        | | ${name}=   | setVariable | custom_name.xml |
        | | Run Keyword And Ignore Error  | SaveConfig | name=${name} |
        | | ${result}= | LoadConfig | ${name} |
        | | ${result}= | LoadConfig | ${name} | clear_net_settings=Y |
        | | ${result}= | LoadConfig | ${name} | clear_net_settings=N |

        | Save and load configuration with a generated name |
        | | ${name}=   | SaveConfig |
        | | ${result}= | LoadConfig | ${name} |

        | Save and load configuration with a custom name without password.
        Load should fail |
        | | ${name}=  | setVariable | custom_name_no.xml |
        | | Run Keyword And Ignore Error  | SaveConfig | name=${name}| save_pw=no |
        | | Run Keyword And Expect Error | * | LoadConfig | ${name} |

        | Save and load configuration with a generated name without password.
        Load should fail |
        | | ${name}=  | SaveConfig | save_pw=no |
        | | Run Keyword And Expect Error | * | LoadConfig | ${name} |
        """

        return self._cli.loadconfig(filename=name,
            clear_net_settings=clear_net_settings)
