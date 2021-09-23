#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/passwd.py#1 $

"""
    IAF 2 CLI ctor - passwd
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliError, REQUIRED
from sal.deprecated.expect import EXACT
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap

DEBUG = True


class passwd(clictorbase.IafCliConfiguratorBase):
    class OldPwdWrongError(IafCliError):
        pass

    newlines = 1

    def __init__(self, sess):

        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Old passphrase did not match', EXACT): self.OldPwdWrongError,
        })

    def __call__(self, input_dict=None, **kwargs):
        self._writeln('passwd')
        param_map = IafCliParamMap(end_of_command=self._get_prompt())

        param_map['cluster_mode'] = ['switch to "cluster" mode', DEFAULT]
        param_map['old_pwd'] = ['Old passphrase', REQUIRED]
        param_map['sys_gen_pass'] = ['get a system generated passphrase', DEFAULT]
        param_map['new_pwd'] = ['New Passphrase: []', REQUIRED]
        param_map['confirm_new_pwd'] = ['new passphrase again', REQUIRED]

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    pw = passwd(cli_sess)
    print pw(old_pwd='Cisco123$', new_pwd='Ironport@123')
    print pw(old_pwd='Cisco123$', new_pwd='Ironport@123', abbrev=False)
