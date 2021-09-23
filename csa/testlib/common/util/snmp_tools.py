#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/util/snmp_tools.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.util.utilcommon import UtilCommon

from sal.clients.snmp import SNMPToolsClient, SNMP_MIBS_DIR


class SNMPTools(UtilCommon):
    """Keywords for interacting with SNMP tools from
    the net-mgmt/net-snmp FreeBSD port.
    """

    def get_keyword_names(self):
        return ['snmp_walk',
                'snmp_get',
                'snmp_trap_sync',
                'snmp_trap_async',
                'snmp_wait_for_trap',
                'snmp_load_mibs_from_dut',
                'snmp_load_mibs_from_files']

    def _get_client_obj(self):
        if not hasattr(self, '_client'):
            self._client = SNMPToolsClient()
        return self._client

    def snmp_walk(self, *args):
        """Run snmpwalk command and get its output.

        *Important:*
        - Place 10-15 seconds sleep after you commit
        snmpconfig changes on appliance and before this
        keyword invocation. Otherwise you may get "No such
        OID" error in the command output

        *Parameters:*
        - `args`: arguments of snmpwalk command. Read
        http://www.net-snmp.org/docs/man/snmpwalk.html for
        more details

        *Exceptions:*
        - `subprocess.CalledProcessError`: if command has returned
        non zero return code

        *Return:*
        Output of snmpwalk command

        *Examples:*
        | ${result}= | SNMP Walk | -v3 | -c | ${SECRET} | -mALL |
        | ... | -l | authNoPriv | -A | ${SECRET} |
        | ... | -u | v3get | ${DUT} | sysContact |
        | Log | ${result} |
        | Should Contain | ${result} | ${CONTACT} |
        """
        snmp_client = self._get_client_obj()
        return snmp_client.snmpwalk(*args)

    def snmp_get(self, *args):
        """Run snmpget command and get its output

        *Important:*
        - Place 10-15 seconds sleep after you commit
        snmpconfig changes on appliance and before this
        keyword invocation. Otherwise you may get "No such
        OID" error in the command output

        *Parameters:*
        - `args`: arguments of snmpget command. Read
        http://www.net-snmp.org/docs/man/snmpget.html for
        more details

        *Exceptions:*
        - `subprocess.CalledProcessError`: if command has returned
        non zero return code

        *Return:*
        Output of snmpget command

        *Examples:*
        | ${result}= | SNMP Get | -v3 | -c | ${SECRET} | -mALL |
        | ... | -l | authNoPriv | -A | ${SECRET} |
        | ... | -u | v3get | ${DUT} | sysContact |
        """
        snmp_client = self._get_client_obj()
        return snmp_client.snmpget(*args)

    def snmp_trap_sync(self, search_pattern, timeout=180, *args):
        """Run SNMP trap in synchronous mode.
        The snmptrapd will be forcibly restarted if it is already
        running

        *Parameters:*
        - `search_pattern`: regexp string, which should be matched
        in snmptrapd output. Matching is case insensitive

        or

        dictionary whose keys are regexps and values are matches counts
        - `timeout`: number of seconds within the search pattern
        should be detected in snmptrapd output
        - `args`: additional parameters to snmptrapd command.
        Read http://www.net-snmp.org/docs/man/snmptrapd.html for
        more details

        *Exceptions:*
        - `TimeoutError`: if search_pattern has not been found
        in snmptrapd output within given time period

        *Return:*
        Full snmptrapd output

        *Examples:*
        | ${output}= | SNMP Trap Sync | blabla | timeout=30 |
        """
        snmp_client = self._get_client_obj()
        return snmp_client.snmptrapd_sync(search_pattern, int(timeout), *args)

    def snmp_trap_async(self, *args):
        """Run SNMP trap in asynchronous mode. Make sure that
        `SNMP Wait For Trap` keywords was called after this one.
        The snmptrapd will be forcibly restarted if it is already
        running

        *Parameters:*
        - `args`: additional parameters to snmptrapd command.
        Read http://www.net-snmp.org/docs/man/snmptrapd.html for
        more details

        *Return:*
        Reference to process object, which should be passed to
        `SNMP Wait For Trap` keyword

        *Examples:*
        | ${proc_obj}= | SNMP Trap Async |
        | Snmp Config Setup | enable_snmp=yes |
        | ... | snmpv3_passphrase=${SECRET} |
        | ... | snmpv1v2_enabled=yes |
        | ... | snmpv1v2_community=${SECRET} |
        | ... | snmpv1v2_network=${DUT_IP}/21 |
        | ... | trap_target=${CLIENT_IP} |
        | ... | trap_community=${SECRET} |
        | ... | system_location_string=${LOCATION} |
        | ... | system_contact_string=${CONTACT} |
        | Commit |
        | ${output}= | SNMP Wait For Trap | ${proc_obj} |
        | ... | ColdStart | timeout=30 |
        | Log | ${output} |
        """
        snmp_client = self._get_client_obj()
        return snmp_client.snmptrapd_async(*args)

    def snmp_wait_for_trap(self, proc_obj, search_pattern, timeout=180,
                           should_kill_daemon=True):
        """Wait until SNMP trap event is generated

        *Parameters:*
        - `proc_obj`: subprocess.Popen return class instance. Should
        be taken from `SNMP Trap Async` keyword output
        - `search_pattern`: regexp string, which should be matched
        in snmptrapd output. Matching is case insensitive

        or

        dictionary whose keys are regexps and values are matches counts
        - `timeout`: number of seconds within the search pattern
        should be detected in snmptrapd output
        - `should_kill_daemon`: whether to kill snmptrapd process
        after search_pattern regexp condition is met. ${True} by default.
        In case of some exception inside this keyword the daemon process
        will be killed anyway.

        *Exceptions:*
        - `TimeoutError`: if search_pattern has not been found
        in snmptrapd output within given time period

        *Return:*
        Full snmptrapd output since last call of this keyword
        or since it was started by `SNMP Trap Async` keyword

        *Examples:*
        | ${proc_obj}= | SNMP Trap Async |
        | Snmp Config Setup | enable_snmp=yes |
        | ... | snmpv3_passphrase=${SECRET} |
        | ... | snmpv1v2_enabled=yes |
        | ... | snmpv1v2_community=${SECRET} |
        | ... | snmpv1v2_network=${DUT_IP}/21 |
        | ... | trap_target=${CLIENT_IP} |
        | ... | trap_community=${SECRET} |
        | ... | system_location_string=${LOCATION} |
        | ... | system_contact_string=${CONTACT} |
        | Commit |
        | ${output}= | SNMP Wait For Trap | ${proc_obj} |
        | ... | ColdStart | timeout=30 | should_kill_daemon=${False} |
        | Log | ${output} |
        | Run Keyword And Expect Error | *TimeoutError* |
        | ... | SNMP Wait For Trap | ${proc_obj} | ColdStart | timeout=5 |
        """
        snmp_client = self._get_client_obj()
        return snmp_client.wait_for_trap(proc_obj, search_pattern,
                                         int(timeout), should_kill_daemon)

    def snmp_load_mibs_from_dut(self, src_dut=None, dst_dir=SNMP_MIBS_DIR):
        """Load MIB files from appliance to local SNMP MIBs storage. Copy will
        not be performed if the same file already exists locally


        *Parameters:*
        - `src_dut`: source appliance hostname. The corresponding UtilsLibrary
        DUT will be taken by default
        - `dst_dir`: path to local MIBs storage. /usr/local/share/snmp/mibs
        be default

        *Return:*
        List of filenames actually loaded to `dst_dir`


        *Examples:*
        | SNMP Load MIBs From DUT |
        """
        args = []
        if src_dut is None:
            args.append(self.dut)
        else:
            args.append(src_dut)
        args.append(dst_dir)
        snmp_client = self._get_client_obj()
        return snmp_client.load_mibs_from_dut(*args)

    def snmp_load_mibs_from_files(self, dst_dir=SNMP_MIBS_DIR, *src_paths):
        """Load MIB files from local files to SNMP MIBs storage. Copy will
        not be performed if the same file already exists locally

        *Parameters:*
        - `dst_dir`: path to local MIBs storage. /usr/local/share/snmp/mibs
        be default
        - `src_paths`: paths to source MIB files. These files should already exist
        on client BSD

        *Exceptions:*
        - `ValueError:`: if one of given paths is not valid file path

        *Return:*
        List of filenames actually loaded to `dst_dir`

        *Examples:*
        | SNMP Load MIBs From Files | ${SNMP_NET_MIB_DIR} | /tmp/f1.txt |
        | ... | /tmp/f2.txt |
        """
        snmp_client = self._get_client_obj()
        return snmp_client.load_mibs_from_dut(dst_dir, *src_paths)
