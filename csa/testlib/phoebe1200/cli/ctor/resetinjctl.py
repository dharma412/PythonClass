#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/resetinjctl.py#1 $

"""
    IAF 2 CLI ctor - resetinjctl
"""
import clictorbase


class resetinjctl(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        """reset to zero the internal injection counters (hidden command) for
           throttling and such."""
        from sal.containers.yesnodefault import YES

        self._writeln('resetinjctl')
        self._query_response(YES)  # injection control counters
        self._wait_for_prompt()


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    reset_injctl = resetinjctl(cli_sess)
    reset_injctl()
    print 'resetinjctl test DONE!'
