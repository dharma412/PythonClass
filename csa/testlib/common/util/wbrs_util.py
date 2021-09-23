#! /usr/bin/env python

import os
import re

import sal.net.sshlib
from common.util.utilcommon import UtilCommon

backup_dir = '/data/pub/wbrs_tmp/orig'


class WbrsUtil(UtilCommon):
    """
    That utility interacts with WBRS database
    """

    def get_keyword_names(self):
        return [
            'wbrs_util_save_db_files',
            'wbrs_util_restore_db_files',
            'wbrs_util_restart_wbrsd',
            'wbrs_util_translate_score',
        ]

    def wbrs_util_save_db_files(self, dir=backup_dir):
        """Save wbrs db files in a backup folder

        Parameters:

        - `dir`: directory of backed-up files. Optional parameter.
           Default value is /data/pub/wbrs_tmp/orig

        Examples:
        The following examples produce the same result.
        | WBRS Util Save DB Files |
        | WBRS Util Save DB Files | dir=/data/pub/wbrs_tmp/orig |
        | WBRS Util Save DB Files | /data/pub/wbrs_tmp/orig     |
        """
        self._info("Saving files in " + dir)
        self._shell.send_cmd('mkdir -p %s' % (dir))
        self._shell.send_cmd('cp /data/db/wbrs/current/db/* %s/' % (dir))

    def wbrs_util_restore_db_files(self, dir=backup_dir):
        """Restore wbrs db files from a backup folder

        Parameters:

        - `dir`: directory of backed-up files. Optional parameter.
           Default value is /data/pub/wbrs_tmp/orig

        Examples:
        The following examples produce the same result.
        | WBRS Util Restore DB Files |
        | WBRS Util Restore DB Files | dir=/data/pub/wbrs_tmp/orig |
        | WBRS Util Restore DB Files | /data/pub/wbrs_tmp/orig     |
        """
        restore_code_list = (
            "import wbrsd",
            """db = wbrsd.update.test_signal_db_switch('%s/restore/', \
                ('ip', 'prefixcat', 'rule', 'categories'))""" % (dir),
            ""
        )

        backdoors = self._shell.send_cmd('ls /tmp/*.bd')
        reqscand = re.findall('(reqscand.+)\.bd', backdoors)
        for r in reqscand:
            self._debug("cmd=" + 'mkdir -p %s/restore' % (dir))
            self._shell.send_cmd('mkdir -p %s/restore' % (dir))
            self._shell.send_cmd('cp %s/* %s/restore/' % (dir, dir))

            self._info(self._shell.backdoor.run(r, restore_code_list))
            self._shell.send_cmd('rm -rf %s/restore' % (dir))

    def wbrs_util_translate_score(self, score):
        """Translates WBRS score into ACL reputation code

        Parameters:

        - `score`: wbrs score

        Examples:
        | ${acl_score}= | WBRS Util Translate Score | -1   |
        | ${acl_score}= | WBRS Util Translate Score | 0    |
        | ${acl_score}= | WBRS Util Translate Score | -2.3 |
        """
        return int(float(score) * 10 + 100)

    def wbrs_util_restart_wbrsd(self):
        """Restart wbrs db

        Parameters: None

        Examples:
        | WBRS Util Restart wbrsd |
        """
        self._shell.heimdall.restart('wbrsd')
