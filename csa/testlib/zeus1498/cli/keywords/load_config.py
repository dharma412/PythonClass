# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/load_config.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

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
            'load_config_from_file',
            'load_config_via_cli',
                ]

    def load_config_from_file(self,
        filename,
        load_network_settings='',
        load_disk_quota_settings='',
    ):

        """Loads XML configuration from a file

        Parameters:
        - `filename` filename must start with a letter, number, or
        underscore, followed by letters, numbers, underscores, or hyphens, and
        can have a maximum of 251 characters. Spaces are not permitted within
        the filename. The filename cannot have any extensions other than ".xml"
        - `load_network_settings=`: answer to question
         'Do you want to load network settings?'
         accepted answers are 'Y' and 'N'
        - `load_disk_quota_settings': answer to question
         'Do you want to load disk quota settings?'
         accepted answers are 'Y' and 'N'

        Return value:
        - True if there are changes to commit
        - False if there are no changes to commit

        Exceptions:
        - ConfigError, "loadconfig: Parse of config file failed"

        Examples:

        | Load configuration from a file |
        | | ${name}= |   Save Config |
        | | ${result}= | Load Config From File |  ${name} |

        | Load Configuration Error "Parse of config file failed" |
        | | ${name}=  |  Save Config  | yes |
        | | Run Keyword And Expect Error |  Parse of config file failed |
        | | ... | Load Config From File | ${name} |

        """

        return self._cli.loadconfig(
            load_method='Load from file',
            filename=filename,
            load_network_settings=load_network_settings,
            load_disk_quota_settings=load_disk_quota_settings,
        )

    def load_config_via_cli(self,
        config_str,
        load_network_settings='',
        load_disk_quota_settings='',
        ):

        """Loads XML configuration via cli

        Parameters:
        - `config_str` configuration string to be entered
        - `load_network_settings=`: answer to question
         'Do you want to load network settings?'
         accepted answers are 'Y' and 'N'
        - `load_disk_quota_settings': answer to question
         'Do you want to load disk quota settings?'
         accepted answers are 'Y' and 'N'
        Exceptions:
        - ConfigError, "loadconfig: Parse of config file failed"

        Return value:
        - True if there are changes to commit
        - False if there are no changes to commit

        Examples:

        | Load configuration from CLI |
        | |   ${result}= | Load Config Via Cli |
        | |   ... |  string |

        """

        return self._cli.loadconfig(
            load_method='Paste via CLI',
            config_str=config_str,
            load_network_settings=load_network_settings,
            load_disk_quota_settings=load_disk_quota_settings,
        )
