#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/avcresetconfig.py#1 $

"""
    IAF 2 CLI ctor - avcresetconfig
"""

import clictorbase

class avcresetconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('avcresetconfig')
        self._wait_for_prompt()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    avcresetcfg = avcresetconfig(cli_sess)
    avcresetcfg()
