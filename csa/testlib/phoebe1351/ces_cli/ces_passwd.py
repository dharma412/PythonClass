from common.cli.clicommon import CliKeywordBase


class CesPasswd(CliKeywordBase):
    """Change your password."""

    def get_keyword_names(self):
        return ['ces_passwd']

    def ces_passwd(self, *args):
        kwargs = self._convert_to_dict(args)
        kwargs['confirm_new_pwd'] = kwargs['new_pwd']
        self._cli.passwd(**kwargs)
        return [line for line in self._cli._sess.getbuf().split("\n")]
