from common.cli.clicommon import CliKeywordBase, DEFAULT


class CesSetGateway(CliKeywordBase):

    def get_keyword_names(self):
        return ['ces_set_gateway']

    def ces_set_gateway(self, ip, ip_version=DEFAULT):
        self._cli.setgateway(ip_version, ip)
        return [line for line in self._cli._sess.getbuf().split("\n")]
