# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/ecconfig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

import clictorbase as ccb
from sal.containers.yesnodefault import YES, NO

DEFAULT = ccb.DEFAULT


class ecconfig(ccb.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('ecconfig')
        self.clearbuf()
        self._expect(['requires activation', 'Choose the operation'])
        lines = self.getbuf()
        if self._expectindex == 0:
            self._wait_for_prompt()
            return -1
        if self._expectindex == 1:
            return ecconfigsetup(self._get_sess())


class ecconfigsetup(ccb.IafCliConfiguratorBase):
    def setup(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_enrollment_server'] = ['Do you want to use non-default Enrollment server', YES]
        param_map['new_enrollment_server'] = ['Enter a new Enrollment server:', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        return self._process_input(param_map)


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    asc = ecconfig(cli_sess)
    asc().setup()
