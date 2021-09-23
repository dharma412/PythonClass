# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/supportrequest_update.py#1 $
# $ DateTime: $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class SupportRequestUpdate(CliKeywordBase):
    """
    Request an immediate update of Support Request Keywords.

    CLI command: supportrequestupdate
    """

    def get_keyword_names(self):
        return ['supportrequestupdate',]

    def supportrequestupdate(self, *args):
        """Request an immediate update of CASE rules and engine core.

        CLI command: supportrequestupdate

        *Parameters:*
        - `force`: Force updates. ${True} or ${Flase}.

        *Return:*
        Output of the CLI.

        *Examples:*
        | ${result}= | supportrequestupdate |
        | Should Contain | ${result} |
        | ... | Requesting update of Support Request Keywords. |

        | ${result}= | supportrequestupdate | force=${True} |
        | Should Contain | ${result} |
        | ... | Requesting forced update of Support Request Keywords. |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.supportrequestupdate(**kwargs)
