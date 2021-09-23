from common.cli.clicommon import CliKeywordBase

class Version(CliKeywordBase):
    """
    Returns output of cli/version
    """
    def get_keyword_names(self):
        return [
            'version',
        ]

    def version(self):
        """
        Returns the output of cli command 'version'

        Parameters:
        None

        Example:
        | ${build}= | SetVariable | 7.5.0-268 |
        | ${log}=   | Version |
        | ShouldContain  |  ${log}  |  Version: ${build} | msg=Unexpected build |
        | RunKeywordAndExpectError | * | ShouldContain | ${log} | Version: 7.5.1 | msg=Unexpected build |
        | ShouldNotContain | ${log} | Version: 7.5.1 | msg=Unexpected build |
        | ShouldMatchRegexp | ${log} | .*Webroot Anti-Malware Engine: [0-9\\.]+ \\(Never Updated\\).* |
        """
        return str(self._cli.version())
