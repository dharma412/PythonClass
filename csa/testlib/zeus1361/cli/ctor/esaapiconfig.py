
from clictorbase import DEFAULT, REQUIRED, IafCliParamMap, IafCliConfiguratorBase

class esaapiconfig(IafCliConfiguratorBase):

    def __call__(self, operation=None):
        self._writeln('esaapiconfig')
        if operation== 'VALIDATE_CERTIFICATE':
            return ValidateCertificate(self._get_sess())

class ValidateCertificate(esaapiconfig):
    def validate(self,  input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        self.newlines = 1
        param_map['validate_certificate'] = ['Should ESA API server certificates be validated during interaction', REQUIRED]
        param_map.update(input_dict or kwargs)
        self._query_response('VALIDATE_CERTIFICATES')
        self._process_input(param_map)
        self._to_the_top(self.newlines)
