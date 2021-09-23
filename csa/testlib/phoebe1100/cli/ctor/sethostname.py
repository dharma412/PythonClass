#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/sethostname.py#1 $

"""
IAF 2 CLI command: sethostname
"""
import clictorbase
from clictorbase import REQUIRED


class sethostname(clictorbase.IafCliConfiguratorBase):

    def __call__(self, name=REQUIRED):
        self._writeln('sethostname')
        self._query_response(name)
        self._wait_for_prompt()


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    shn = sethostname(cli_sess)
    shn('vitalik.qa')
    # Requires commit to save changes

    # Bad host names
    hostnames = ('bad', '1.1.1.1', 'bad*.com.too')

    for hostname in hostnames:
        try:
            shn(hostname)
        except clictorbase.IafIpHostnameError:
            print '%s failed, as expected' % hostname
        except:
            raise clictorbase.IafCliError

# EOF
