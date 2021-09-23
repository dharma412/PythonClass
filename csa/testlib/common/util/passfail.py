#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/passfail.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from robot.libraries.BuiltIn import BuiltIn

from common.util.filter import Filter
from common.util.misc import Misc
from common.util.systools import SysTools
from common.util.utilcommon import UtilCommon
from common.cli.clicommon import CliKeywordBase
from sal.time import CountDownTimer
from UtilsLibrary import UtilsLibrary
import common.Variables


class CommonPassFailError(AssertionError):

    def __unicode__(self):
        return unicode(self.__str__())


class CommonPassFail(UtilCommon):
    """Common pass fail criteria check that can be configured to perform the
       followings after every test:

          - check for memory and connection leak.
          - check for core dump.
          - check for exceeded open connections.
    """

    def __init__(self, *args, **kwargs):
        UtilCommon.__init__(self, *args, **kwargs)
        self.prox_track_log = '/data/pub/track_stats/prox_track.log'
        self.cli_kw_obj = CliKeywordBase(self.dut, self.dut_version)
        self.log_filter_obj = Filter(self.dut, self.dut_version)
        self.systools_obj = SysTools(self.dut, self.dut_version)
        self.misc_dut_obj = Misc(self.dut, self.dut_version)

    def _reset_objs(self):
        self.start_shell_session()
        self.cli_kw_obj.start_cli_session()

    def get_keyword_names(self):
        return [
            'common_pass_fail_check',
            'common_pass_fail_get_current_chunk_purposes',
        ]

    def common_pass_fail_get_current_chunk_purposes(self):
        """Gets the current chunk purposes value in proxy track log.

        Example:
        | ${chunk}= | Get Current Chunk Purposes |
        """
        return self._get_current_chunk_purposes()

    def common_pass_fail_check(self, chunk_before):
        """Performs check for:

              - memory and connection leak.

              - core dump.

              - exceeded open connections.

       Parameters:
           - `chunk_before`: chunk value before calling this test.

        Example:
        | Common Pass Fail Check | chunk_before=61234 |
        """
        self._memory_leak_check(chunk_before)
        self._connection_leak_check()
        self._core_dump_check()
        self._opened_connection_check()

    def _get_current_chunk_purposes(self):
        """Gets the current chunk purposes value in proxy track log.
        """
        base_line = self.log_filter_obj.filter_log_create_baseline(
            self.prox_track_log)
        out, count = self.log_filter_obj.filter_log(self.prox_track_log,
                                                    baseline=base_line, match_patterns="'chunk purposes:'",
                                                    timeout=15)
        self._debug('Out: %s' % (out,))
        return out.split(',')[0].split()[3]

    def _memory_leak_check(self, chunk_before):
        """Checks for memory leak by comparing 'chunk purposes:' before and
           after test in /data/pub/track_stats/prox_track.log.

           Note: Per Parag, here is the process:
             - monitor 'chunk purposes:' for 30 - 40 seconds after
               test/transaction completed.  It should finally match with
               that before test.  If it doesn't, there is a leak.

           If memory leaks, performs the followings:
           - stop test and mark it as a failure.
           - reboot appliance.
        """
        self._info('Checking for memory leak...')
        mem_leak = False
        timer = CountDownTimer(40)
        timer.start()
        while timer.is_active():
            chunk_after = self._get_current_chunk_purposes()
            self._debug("Chunk before: %s; Chunk after: %s" %
                        (chunk_before, chunk_after))
            if int(chunk_after) == int(chunk_before):
                break
            mem_leak = True
        if mem_leak:
            self._info("Memory is leaking.  Chunk after did not return to"
                       "same level as chunk before")
            self.systools_obj.reboot_and_wait()
            self._reset_objs()
            raise CommonPassFailError, 'Memory leak occurred'
        else:
            self._info('No memory leak found')

    def _connection_leak_check(self):
        """Checks 'AuthClientInfo', 'ClientInfo', and 'ServerInfo' in
           /data/pub/track_stats/prox_track.log after completion of transaction.
           Value of first column, in each field, should be 0.

           AuthClientInfo   0   96  96   0   0   8   8
               ClientInfo   0   96  96   0   0   12  12
               ServerInfo   0   12  12   0   0    2   2

           If not, performs the followings:

           - stop test and mark it as a failure.
           - reboot appliance.
        """
        self._info('Checking for connection leak...')
        fields = ('AuthClientInfo', 'ClientInfo', 'ServerInfo')
        conn_leak = False
        pre_msg = []
        connection_dict = {}
        base_line = self.log_filter_obj.filter_log_create_baseline(
            self.prox_track_log)
        output, count = self.log_filter_obj.filter_log(self.prox_track_log,
                                                       baseline=base_line, match_patterns="-e "
                                                                                          "'ClientInfo' -e 'ServerInfo'",
                                                       timeout=15)
        output = output.strip().split('\n')
        self._debug('Output: %s' % (output,))
        for line in output:
            line = line.split()
            connection_dict[line[0]] = line[1]
        self._debug('Connection dictionary: %s' % (connection_dict,))
        for field in fields:
            if int(connection_dict[field]) > 0:
                conn_leak = True
                pre_msg.append(field)
        if conn_leak:
            self._info("%s show(s) connection is leaking." %
                       (' and '.join(pre_msg),))
            self.systools_obj.reboot_and_wait()
            self._reset_objs()
            raise CommonPassFailError, 'Connection leak occurred'
        else:
            self._info('No connection leak found')

    def _core_dump_check(self):
        """Check for core dump in /data/cores.  If found, performs the
           followings:

           - stop test and mark it as a failure.
           - copy out all core file to a designated server for future
             analysis. Then clear all core files in /data/cores in preparation
             for next test.
           - zip all files in /data/pub and /data/log directories and name them
             with testcase id. Then, copy them out to a designated server for
             future analysis.
           - reboot appliance.
        """

        app_bin_dict = {
            'prox': '/usr/local/prox/libexec/prox',
            'sophos': '/usr/local/bin/sophos',
        }
        self._info('Checking for core file...')
        core_dir = '/data/cores/'
        data_pub_dir = '/data/pub/'
        data_log_dir = '/data/log/'
        cmd = "find %s -name '*.core'" % core_dir
        core_files = self._shell.send_cmd("find %s -name '*.core'" %
                                          (core_dir,)).strip()
        self._debug(core_files)
        if core_files:
            self._info("Core file found.  Performing the followings:")
            core_files = core_files.split('\r\n')
            cmd = '%s -batch -x %s %s %s > %s'
            gdb_bin = '/usr/bin/gdb'
            core_bt_file = '/tmp/core_gdb.bt'
            app_bin = app_bin_dict['prox']
            remote_server = 'explore02.qa'
            gdb_batch_cmd_file = '/tmp/gdb.cmd'
            if not self._shell.send_cmd("find /tmp -name gdb.cmd").strip():
                self._info("Creating gdb commands file for batch run")
                self._shell.send_cmd('echo bt > %s' % (gdb_batch_cmd_file,))
                self._shell.send_cmd('echo quit >> %s' % (gdb_batch_cmd_file,))
            for file in core_files:
                self._info('Generate gdb backtrace for %s' % (file,))
                if 'sophos' in file:
                    app_bin = app_bin_dict['sophos']
                self._shell.send_cmd(cmd % (gdb_bin, gdb_batch_cmd_file,
                                            app_bin, file, core_bt_file))
                self._info(self._shell.send_cmd('cat %s' % (core_bt_file,)))

            self._info("Tar all core files and relevant logs")
            curr_time = BuiltIn().get_time()
            test_id = 'Unknown'
            try:
                robot_vars = common.Variables.get_variables()
                if robot_vars:
                    if robot_vars.has_key('${TEST_ID}'):
                        test_id = robot_vars['${TEST_ID}']
            except:
                # Default ${TEST_ID} to 'Unknown' for stand alone usage.
                pass
            tar_file = '%s_%s.tgz' % (test_id, curr_time.replace(' ', '_'))
            self._shell.send_cmd('tar cvzf %s%s %s*.core %s* %s*' %
                                 (core_dir, tar_file, core_dir, data_pub_dir, data_log_dir),
                                 timeout=45)
            self._info("Copy tar file, %s, out to %s" % (tar_file,
                                                         remote_server,))
            self.misc_dut_obj.copy_file_from_dut_to_remote_machine(
                remote_host=remote_server, from_loc='%s%s' % (core_dir,
                                                              tar_file), to_loc='')
            self._info("Remove all core file from  %s" % (core_dir,))
            self._shell.send_cmd('rm %s*' % (core_dir,), timeout=20)
            self.systools_obj.reboot_and_wait()
            self._reset_objs()
            raise CommonPassFailError, 'Core file found'
        else:
            self._info('No core file found')

    def _opened_connection_check(self):
        """Checks for opened connection by running 'status detail'.

           Connections:
             Idle client connections                    0
             Idle server connections                    0
             Total client connections                   0
             Total server connections                   0

           For both 'Total client connections' and 'Total server connections',
           each should not exceed 10. If any of them does or both do, perform
           the followings:

           - stop test and mark it as a failure.
           - reboot appliance.

        """
        self._info('Checking for opened connection...')
        status = self.cli_kw_obj._cli.status()
        self._info("Connection Status: %s" % status.connections)
        if int(status.connections['total_client'][0]) > 10 or \
                int(status.connections['total_server'][0]) > 10:
            self._debug("More than 10 connection opened")
            self._info("Opened connection exceeded threshold.  Reboot"
                       " machine")
            self.systools_obj.reboot_and_wait()
            self._reset_objs()
            raise CommonPassFailError, ('Opened connections exceed allowed '
                                        'threshold of 10')
        else:
            self._info('Opened connection does not exceed threshold')
