from common.cli.clicommon import CliKeywordBase


class NotificationsUpdate(CliKeywordBase):
    """Update Notifications Component via CLI."""

    def get_keyword_names(self):
        return ['notifications_update']

    def notifications_update(self, force=False):
        """
        CLI > notificationsupdate

        Use this keyword to perform updating of Notifications Component via CLI.

        *Parameters:*
        - `force`: Force update. Boolean. False by default.

        *Example:*
        | Notifications Update |
        | Notifications Update | force |
        """

        return self._cli.notificationsupdate(force=force)