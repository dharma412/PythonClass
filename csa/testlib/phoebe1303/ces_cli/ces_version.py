from common.cli.clicommon import CliKeywordBase


class CesVersion(CliKeywordBase):
    """
    Returns some version data of DUT
    """
    def get_keyword_names(self):
        return ['ces_version' ]

    def ces_version(self):
        self._cli.version()
        return [line for line in self._cli._sess.getbuf().split("\n")]
