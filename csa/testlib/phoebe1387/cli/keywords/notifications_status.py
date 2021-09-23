from common.cli.clicommon import CliKeywordBase


class NotificationsStatus(CliKeywordBase):
    """ Keyword for dnsstatus CLI command.
    """
    def get_keyword_names(self):
        return ['notifications_status']

    def notifications_status(self):
        """Display notification component status.

        Return:
            A dictionary containing below keys -
            `Component` - String
            `Version` - String
            `Last Updated` - String

        Examples:
        | ${status}= | Notification Status |
        """
        return self._cli.notificationsstatus()
