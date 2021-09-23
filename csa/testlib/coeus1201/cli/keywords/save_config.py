#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/save_config.py#1 $

from common.cli.clicommon import CliKeywordBase

class SaveConfig(CliKeywordBase):
    """Saves the current configuration to disk.

    Please be aware that a configuration without passwords will fail when
    reloaded with loadconfig.
    """

    def get_keyword_names(self):
        return ['save_config',
                ]

    def save_config(self,
                    save_pw='no',
                    name=None):
        """Saves the current configuration to disk.

        Parameters:
        - `save_pw`: Either 'yes' or 'no'.Indicates whether passwords should be
        included as plain password/ mask password/ in the configuration file.
        - `name`: name to be given for the generated configuration file. ".xml"
        will be appended to the specified filename automatically if the filename
        does not contain a file extension. If no filename is provided, the
        system will automatically generate the filename.

        NOTE: The configuration filename must start with a letter, number, or
        underscore, followed by letters, numbers, underscores, or hyphens, and
        can have a maximum of 251 characters. Spaces are not permitted within
        the filename. The filename should not have any extensions.

        Examples:
        | ${result}= | Save Config |
        | Log | ${result} |

        | ${result}= | Save Config | save_pw=no | name=test |
        | Log | ${result} |
        """

        password_option_dict = {
            'y':          '1',      #yes
            'n':           '2',     #no
        }
        save_pw = save_pw.strip().lower()[0]
        if save_pw.lower() not in password_option_dict.keys():
            raise "Save Password option 'save_pw' should be one of the following:\n['yes' >'mask password' | [default] 'no' > 'plain password']"
        save_pw = password_option_dict[save_pw.lower()]
        if name is not None and name.strip():
            system_generates_name = self._process_yes_no('no')
            name = name.strip()
        else:
            system_generates_name = self._process_yes_no('yes')
            name = None

        output = self._cli.saveconfig(save_pw, system_generates_name, name)
        return output
