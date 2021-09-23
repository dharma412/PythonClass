from common.cli.clicommon import CliKeywordBase


class CesSetHostName(CliKeywordBase):
    """Set the name of the machine."""

    def get_keyword_names(self):
        return ['ces_set_host_name',]

    def ces_set_host_name(self, name):
        self._cli.sethostname(name)
        return [line for line in self._cli._sess.getbuf().split("\n")]