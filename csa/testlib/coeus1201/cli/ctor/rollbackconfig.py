#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/rollbackconfig.py#1 $

import clictorbase

class rollbackconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self, desc, save_for_rollback='Y'):
        self.clearbuf()
        self._writeln('rollbackconfig')
        self._expect('Choose the operation you want to perform:')
        self._writeln('ROLLBACK')
        out = self._read_until('Enter the number of the config to revert to.')
        l = out.split('\r')
        for i in range(10, len(l)-1):
            if desc in l[i]:
                config = l[i].split('\n')[1].split('.')[0]
                print 'Config file number is:', config
            else:
                continue
        self._writeln(config)
        self.clearbuf()
        print self._wait_for_prompt()
        self._writeln('Y')
        print self._wait_for_prompt()
        self._writeln('\n')
        print self._wait_for_prompt()
        self._writeln('\n')
        print self._wait_for_prompt()

    def get_rollback_status(self):
        self._writeln('rollbackconfig')
        raw = self._read_until('>')
        self._info(raw)
        self._writeln('SETUP')
        rollback_status = self._read_until('>')
        self._info(rollback_status)

        if 'Rollback Configuration: Disabled' in rollback_status and '- ROLLBACK' not in rollback_status:
            return 'disabled'
        else:
            return 'enabled'

    def set_rollback_status(self, status='enabled', desc=''):
        self.clearbuf()
        self._writeln('rollbackconfig')
        raw = self._read_until('>')
        self._info(raw)
        self._writeln('SETUP')
        rollback_status = self._read_until('>')
        self._info(rollback_status)
        if status == 'disabled' and 'Rollback Configuration: Disabled' in rollback_status:
           print 'Rollback option is disabled'
        elif status == 'enabled' and 'Rollback Configuration: Enabled' in rollback_status:
           print 'Rollback option is enabled'
        elif 'Rollback Configuration: Disabled' in rollback_status and status == 'enabled' or 'Rollback Configuration: Enabled' in rollback_status and status == 'disabled':
            self._writeln('Y\n')
            self._writeln('\n')
            raw = self._read_until('>')
            self._info(raw)

if __name__ == '__main__':
    sess = clictorbase.get_sess()
    rollback = rollbackconfig(sess)
    rollback(configfile, desc)

