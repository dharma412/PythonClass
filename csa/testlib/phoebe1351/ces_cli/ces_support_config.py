from common.cli.clicommon import CliKeywordBase


class CesSupportConfig(CliKeywordBase):

    def get_keyword_names(self):
        return ['ces_support_config',]

    def ces_support_config(self):
        self._cli._sess.writeln(
            'supportconfig --supportrequest=abc@cisco.com')
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]
