#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/showconfig.py#1 $

"""
IAF 2 CLI command: showconfig
"""

import clictorbase

from sal.containers.yesnodefault import YES, NO

class showconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self, mask_pw=NO):
        import re

        self.clearbuf()
        self._writeln('showconfig')
        self._query_response(mask_pw)
        xml = self._wait_for_prompt_line()
        start_xml_pos = xml.find("xml version=")
        if start_xml_pos:
            xml = xml[start_xml_pos - 3:].strip()
            # work around for long line be wrapped around
            patt = 'message\r\ns>'
            xml = re.sub(patt, 'messages>', xml)

        # strip prompt line out of xml
        # and fix line endings before returning
        xml_arr = xml.split("\r\n")
        xml_arr.pop()
        xml = "\n".join(xml_arr)
        return xml

if __name__ == '__main__':
    from sal.containers.yesnodefault import NO
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    scfg = showconfig(cli_sess)

    print 'showconfig with pwd'
    out = scfg()
    print out
    print 'showconfig do NOT include pwd'
    out = scfg(include_pwd=NO)
    print out

