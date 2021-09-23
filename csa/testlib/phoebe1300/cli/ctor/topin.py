#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/topin.py#1 $

"""
IAF Command Line Interface (CLI)

command:
    - topin
"""

import re

import clictorbase


class topin(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        self.buf = self._wait_for_prompt()

        patt = re.compile(r'^(\d+) +(\S+) +([\d\.]+) +(.*) +(\d+)\s*$')
        buf_list = self.buf.split('\n')
        self.obj_list = TopInObjList(self.buf)

        for line in buf_list[6:-1]:
            if re.search(r'^\s*$', line):
                continue

            mo = patt.search(line)
            self.obj_list.append(TopInObj(*mo.groups()))

        return self.obj_list


class TopInObjList(list):
    def __init__(self, buf):
        list.__init__(self)
        self.buf = buf

    def __str__(self):
        return self.buf


class TopInObj:
    def __init__(self, rank, remote_host, remote_ip, listener, connections_in):
        self.rank = rank
        self.remote_host = remote_host
        self.remote_ip = remote_ip
        self.listener = listener
        self.connections_in = connections_in


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    # session host defaults to .iafrc.DUT
    cli = topin(cli_sess)
    # test case
    print cli()
