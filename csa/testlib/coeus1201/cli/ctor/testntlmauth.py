#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/testntlmauth.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
    IAF 2 CLI ctor - testntlmauth
"""

import clictorbase

class testntlmauth(clictorbase.IafCliConfiguratorBase):

    def __call__(self, msg_1, msg_2, msg_3):
        self._sess.writeln('testntlmauth')
        self._query_response('1')
        self._query_response(msg_1)
        self._query_response(msg_2)
        self._query_response(msg_3)
        return self._wait_for_prompt()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ntlmtest = testntlmauth(cli_sess)
    msg_1 = 'TlRMTVNTUAABAAAABoIIAAAAAAAAAAAAAAAAAAAAAAA='
    msg_2 = 'TlRMTVNTUAACAAAADAAMADAAAAAGgokAYpHp/DrASScAAAAAAAAAAE4ATgA8AAAA'\
            'SUFGLVcySzMtQUQxAgAYAEkAQQBGAC0AVwAyAEsAMwAtAEEARAAxAAEACgBXAFMA'\
            'QQA0ADkABAAGAHcAZwBhAAMAEgB3AHMAYQA0ADkALgB3AGcAYQAAAAAA'
    msg_3 = 'TlRMTVNTUAADAAAAGAAYAEAAAAAYABgAWAAAABAAEABwAAAABwAHAIAAAAAPAA8A'\
            'hwAAAAAAAAAAAAAABoKJAJSx+5yC4dFjAAAAAAAAAAAAAAAAAAAAAPO75kquEsDE'\
            'RaurKyYQHXwapodEh4HZe0lBRi1XMkszLUFEMS5XR0FpYWZ1c2Vydm13MDcyLWNs'\
            'aWVudDEy'
    ntlmtest(msg_1, msg_2, msg_3)


