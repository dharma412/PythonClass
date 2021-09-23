from common.cli.clicommon import CliKeywordBase

class EsaApiConfig(CliKeywordBase):

    def get_keyword_names(self):
        return ['esaapiconfig_validate']

    def esaapiconfig_validate(self, validate_certificate=None):
        """
        :param args: validate_certificate(Y|N)
        :return:
        Keyword usage:
        This keyword is used for esa api config validate certificate
        esaapiconfig_validate       validate_certificate=Y
        esaapiconfig_validate       validate_certificate=N
        """
        kwargs = {}
        if validate_certificate:
            kwargs['validate_certificate']= validate_certificate
        self._cli.esaapiconfig('VALIDATE_CERTIFICATE').validate(**kwargs)