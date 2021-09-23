#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/sethostname.py#1 $

"""
IAF 2 CLI command: sethostname
"""

__revision = '$Revision:'

from clictorbase import IafCliConfiguratorBase, get_sess, \
                        REQUIRED, IafIpHostnameError, IafCliError


class sethostname(IafCliConfiguratorBase):
    def __call__(self, name=REQUIRED):
        self._writeln('sethostname')
        self._query_response(name)
        self._wait_for_prompt()


if __name__ == '__main__':
    sess = get_sess()
    shn = sethostname(sess)
    shn('vitalik.qa')
    # Requires commit to save changes

    # Bad host names
    hostnames = ('bad', '1.1.1.1', 'bad*.com.too')
    
    for hostname in hostnames:
        try:
            shn(hostname)
        except IafIpHostnameError:
            pass
        except:
            raise IafCliError

# EOF 
