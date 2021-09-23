# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/version.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase
class Version(CliKeywordBase):
    """
    Returns some version data of DUT
    """
    def get_keyword_names(self):
        return ['version' ]

    def version(self):
        """
        Returns the following attributes of the version:
        - Model
        - Version
        - Build Date
        - Install Date
        - Serial #
        - BIOS
        - RAID
        - RAID Status
        - RAID Type
        - BMC

        Parameters:
        None

        Example:
        | ${build}= | SetVariable | 7.8.0-470 |
        | ${log}=   | Version |
        | ShouldContain  |  ${log}  |  Version: ${build} | msg=Unexpected build |
        | RunKeywordAndExpectError | * | ShouldContain | ${log} | Version: 7.5.1 | msg=Unexpected build |
        | ShouldNotContain | ${log} | Version: 7.5.1 | msg=Unexpected build |
        """

        return str(self._cli.version())

