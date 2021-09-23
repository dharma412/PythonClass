# $Id: //prod/main/sarf_centos/variables/error_log.py#2 $
# $DateTime: 2019/06/03 22:56:07 $
# $Author: revlaksh $
""" Patterns for determining errors in logs
This is a default set of patterns.
If you need to use a different one, create a corresponding file
and provide its name as a parameter while starting robot as
--variablesfile <file_name>
"""
from robot.libraries.BuiltIn import BuiltIn

LOG_ERROR_PATTERNS = [
    '-E "'\
    '(Error'\
    '|Critical'\
    '|Exception'\
    '|appfault'\
    '|application.fault'\
    '|failed consistency check'\
    '|page not found'\
    '|No module named)"',

    # exclude
    '-v "prox_track.log:"',
    '-v "configdefragd."',
    '-v -i "Info:"',
    '-v -i "Warning:"',

    # skip
    '-v "/configuration/"',
    '-v -i -E "(info|warning|debug):"',
    '-v "/tmp/merlin_query.sock"',
    '-v "winbind"',
    '-v "domain list"',
    '-v "fetch our SID"',
    '-v -i -E "error_?page"',
    '-v "ManifestAcquisitionError"',
    '-v "Scanning Error"',
    '-v "ERR_INTERNAL_ERROR"',
    '-v "error 22 in LargeFile_BlockWriteDone"',
    '-v "tunnel error"',
    '-v "waitpid error"',
    '-v "ads_sasl_spnego_krb5_bind failed"',
    '-v -i "error_code"',
    '-v "capacity reporting: exception:"',
    '-v -E "system_health.coro_snmp.(Network|Timeout)Error\'>"',
    '-v "AVC_Engine read_thread: packet: 0 bytes:"',
    '-v "AVC_Engine failed to connect to /tmp/avc_cb_fastrpc.sock"',
    '-v "exceptions.client.xobni.com/exceptions"',
    '-v "SSL3_READ_BYTES:tlsv1"',
    '-v "Test Log Message"',
    '-v "on \'/tmp/webcat_fast_rpc.sock\'"',

    # from IGNORE variables
    '-v "SSL error with client"',
    '-v "Watchdog timed out"',
    '-v -E "(wbrsd|mcafee): Watchdog detected an error"',
    '-v -E "IOError.*Errno 32.*Broken pipe"',
    '-v "AVC_Engine failed to connect to /tmp/avc_fastrpc.sock"',

    # added recently
    '-v "handshake failure"',
    #Critical: SSL error with client 173.37.1.121:52792 - (336150757,
    #'error:140940E5:SSL routines:SSL3_READ_BYTES:ssl handshake failure

    '-v -E "\[Errno 2\] No such file or directory.*/tmp/avc_manager_fastrpc.sock"',

    '-v -E "\[Errno 61\] Connection refused.*/tmp/"',
    # [[Errno 61] Connection refused] on '/tmp/avc_manager_fastrpc.sock'

    # skip until bug 81706 is fixed
    '-v -E "wbrs traceback.*wbrs_mgmt.py send_to_wbrs_mgmt.*class .wbrs.wbrs_mgmt.WBRSManagementError.*File.*mgmt_server.py.*in __mgmt_server_handler.*No such file or directory"',
    '-v -E "Errno 2.*No such file or directory.*/data/tmp/(reqscand2|wbnpd)_rpc.sock"',
    '-v -E "featurekey adjustment failed.*The daemon is not responding"',
    ]
def get_variables(library=""):
    log_patterns = {}
    robot_vars = BuiltIn().get_variables()

    for lib in library.split(','):
        lib_version = lib+'_LIB_VERSION'
        lib_version_var = "${%s_LIB_VERSION}" % (lib,)
        if lib_version_var in robot_vars.keys():
            lib_version = robot_vars[lib_version_var]
            for i in range(len(lib_version), 1, -1):
                try:
                    _name = lib_version[:i]
                    _lib = __import__("error_log_branches." + _name)
                    result = eval("_lib." + _name + ".get_patterns()")
                    break
                except:
                    pass
            else:
                result = LOG_ERROR_PATTERNS
            log_patterns[lib.upper()+'_ERROR_PATTERNS'] = result

    return log_patterns
