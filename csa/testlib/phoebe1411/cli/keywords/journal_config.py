
from common.cli.clicommon import CliKeywordBase
from common.cli.cliexceptions import ConfigError

class JournalConfig(CliKeywordBase):
    """
    Keywords for journalconfig
    """
    def get_keyword_names(self):
        return ['journal_config_enable',
                'journal_config_disable',
                'journal_config_is_enabled',
                'journal_config_get_status']

    def journal_config_enable(self, **kwargs):
        """
        Enable easypov mode

        Parameters:
        `mailbox`: Journal mailbox. It can be either Office365 or gsuite
        `journal-mail-to`: Journal recipient email id
        `routing-mode`: Journal routing_mode, by default is Journaling
        `non_journal_action`: non_journal_action by default is drop

        Return:
            Command output as string

        Example:
        | Journal Config Enable | routing-mode=Journalling| mailbox=Office365 |
        | ... |journal-mail-to=journalrecipient@mar-esa.com | non-journal-action=drop|
        """

        if 'mailbox' not in kwargs:
            raise ConfigError('Mailbox option is required not provided')
        if 'journal-mail-to' not in kwargs:
            raise ConfigError('journal-mail-to is required not provided')
        mailbox = kwargs['mailbox']
        journal_mailto = kwargs['journal-mail-to']
        non_journal_action = kwargs.get('non-journal-action', 'drop')
        routing_mode = kwargs.get('routing-mode', 'Journaling')

        return self._cli.journalconfig.enable(routing_mode, mailbox, journal_mailto, non_journal_action)

    def journal_config_disable(self):
        """
        Disable easypov mode

        Parameters:
            None

        Return:
            Command output as string

        Example:
        | Journal Config Disable |
        """

        return self._cli.journalconfig.disable()

    def journal_config_is_enabled(self):
        """
        Check easypov mode

        Parameters:
            None

        Return:
            A boolean

        Example:
        | Journal Config Is Enabled |
        """

        return self._cli.journalconfig.is_enabled()

    def journal_config_get_status(self):
        """
        journal config command output

        Parameters:
            None

        Return:
             Command output as string

        Example:
        | Journal Config |
        """

        return self._cli.journalconfig.journaloutput() 
