from common.cli.clicommon import CliKeywordBase

class smaconfig(CliKeywordBase):
    """
    cli -> smaconfig

    Edit the configuration of Sma.
    """
    def get_keyword_names(self):
        return ['smaconfig_add',
                'smaconfig_delete',
                'smaconfig_print_key']

    def smaconfig_add(self,hostname,ssh_key):
        """
        This will add smaconfig

        cli -> smaconfig -> ADD

        Parameters:
        - `hostname`:  Hostname of the sma to add.
        - `ssh_key':  Ssh key of the sma.

        Examples:
        Add SmaConfig
        | SmaConfig ADD | hostname | ssh_key |
        """

        return self._cli.smaconfig().add(hostname,ssh_key)

    def smaconfig_print_key(self):
        """
        This will print smaconfig

        cli -> smaconfig -> PRINT

        Examples:
        Add SmaConfig
        | SmaConfig PRINT |
        """

        return self._cli.smaconfig().print_key()

    def smaconfig_delete(self,keynumber):
        """
        This will delete smaconfig

        cli -> smaconfig -> DELETE

        Examples:
        Add SmaConfig
        | SmaConfig DELETE | 1 |
        """

        return self._cli.smaconfig().delete(keynumber)
