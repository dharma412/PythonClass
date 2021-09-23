# $Id: //prod/main/sarf_centos/variables/error_log_branches/coeus77.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $
""" Patterns for determining errors in logs
This is a default set of patterns.
If you need to use a different one, create a corresponding file
and provide its name as a parameter while starting robot as
--variablesfile <file_name>
"""

LOG_ERROR_PATTERNS = [
    '-E "'\
    '(Error'\
    '|Critical'\
    '|Exception'\
    '|appfault'\
    '|application.fault'\
    '|failed consistency check'\
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
    '-v -E "updater\.exceptions\.HealthError.*app_thread\.py _monitor_health"',

    # skip until #87101 is fixed
    '-v -E "Exception AssertionError in .webroot.WebrootEngine object at .* ignored"',
    '-v -E "merlin traceback: .*class .updater.exceptions.HealthError"',
    '-v "Exception: Failed to load Webroot definition"',

    # skip until #92142 is fixed
    '-v "Cannot contact any KDC for requested realm"',

    # skip until #91704 is fixed CSCzv91787 CSCzv52581
    '-v -E "wbrsd_rpc.ParallelApplyError.*fast_rpc.RPC_Server_Unreachable"',

    # skip until #82543 CSCuf76816 is fixed
    '-v "coro.TimeoutError"',

    # skip until #91213 (CSCzv40367) is fixed
    '-v "db/database_manager.py"',

    # skip until #90848 (CSCzv24588) is fixed
    '-v "updater/app_thread.py"',

    # skip until #CSCuf31169 is fixed
#    '-v "ads_connect: No logon servers"',

    # skip until #CSCuf93890 is fixed
    '-v "No module named oserrors"',

    # skip until #CSCuf93897 is fixed
    '-v "Error opening certificate"',

    # skip until product bug: CSCug66702 is fixed
    '-v -E "Critical.*PROXY.*Couldn.t open configuration file /usr/local/prox/etc/prox.conf"',

    # CSCug62449
    '-v -E "Critical: An application fault occurred: .*aggregator/master_aggregator.py"',

    # skip until bug CSCzv24448 is fixed
    '-v "Critical: firestone Could not instantiate Categorizer"',
    '-v "RuntimeError: Error opening database file"',
    '-v -E "ERROR +firestone Could not load data for .* language: Error opening database file .* language will be disabled"',

    # skip until bug CSCuf35558 is fixed
    '-v "Critical: HTTPS : - : Error opening certificate"',
    '-v "Critical: HTTPS : - : Error opening private key"',
    # skip in coeus77 only because of bug CSCzv44441; it should be fixed in coeus80
    '-v "wbnp query reporting failed"',

    # per request CSCzv47551
    '-v -E "Errno 2.*No such file or directory.*/data/tmp/.*_rpc.sock""',
]

def get_patterns():
    return LOG_ERROR_PATTERNS
