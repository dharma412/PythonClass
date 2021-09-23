from common.cli.clicommon import CliKeywordBase

class TrailBlazerConfig(CliKeywordBase):
    """
    TrailBlazerConfig related keywords
    """
    def get_keyword_names(self):
        return ['trailblazer_config_enable', 'trailblazer_config_disable', 'trailblazer_config_status']

    def trailblazer_config_enable(self,  *args):
        """
        To enable the trailblazer config
        :param args:
        :return: command output
        Usage:
        |Trailblazer Config Enable|
        |Trailblazer Config Enable| port=14000|
        """
        kwargs = self._convert_to_dict(args)
        kwargs.update({'action':'enable'})
        return str(self._cli.trailblazerconfig(**kwargs))

    def trailblazer_config_disable(self):
        """
        To disable the trailblazer config

        :return: command output
        Usage:
        |Trailblazer Config Disable|
        """
        return str(self._cli.trailblazerconfig(**{'action': 'disable'}))

    def trailblazer_config_status(self):
        """
        To get the status of the trailblazer config
        :return: command output
        Usage:
        |${status}=     Trailblazer Config Status|
        |Should Contain    ${status}      trailblazer is running with https|
        """
        return str(self._cli.trailblazerconfig(**{'action': 'status'}))
