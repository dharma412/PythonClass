#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/rollovernow.py#1 $

"""
IAF 2 CLI command: rollovernow
"""

import clictorbase

class rollovernow(clictorbase.IafCliConfiguratorBase):
    def __call__(self, logfile='All Logs'):
        self._sess.writeln('rollovernow')
        self._query_select_list_item(logfile)
        self._wait_for_prompt()

if __name__ == '__main__':
    sess = clictorbase.get_sess() 
    rollnow = rollovernow(sess)
    rollnow(logfile=18)
    # note: 'gui_logs' will match 'euqgui_logs' first!
    rollnow(logfile='"gui_logs')
    
