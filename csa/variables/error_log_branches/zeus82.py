# $Id: //prod/main/sarf_centos/variables/error_log_branches/zeus82.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

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
    '-v "splunkd."',
    '-v -i "Info:"',
    '-v -i "Warning:"',

    # skip
    '-v "Bogus work queue app fault"',
    '-v "PthreadException"',
    '-v "BATSAFE:"',
    '-v "page not found"',
    '-v "relation .* already exists"',
    '-v "system_logs"',
    '-v "RPC: OSError"',
    '-v "a[s|v]archive"',
    '-v "Configuring application"',
    '-v "exit_save_error unknown"',
    '-v "reason other error"',
    '-v "sslv3 alert bad certificate"',
    '-v -E ".tunnels.ironport.com:25: (tunnel only ran|\\[Errno 10\\] No child processes)"',
    '-v "return result, no error"',
    '-v "\\[Errno 54\\] Connection reset by peer"',

    # from IGNORE variables
    '-v "SSL error with client"',
    '-v -E "IOError.*Errno 32.*Broken pipe"',

    # added recently
    '-v "handshake failure"',
    #Critical: SSL error with client 173.37.1.121:52792 - (336150757,
    #'error:140940E5:SSL routines:SSL3_READ_BYTES:ssl handshake failure

    # skip until bug 81706 is fixed
    '-v -E "wbrs traceback.*wbrs_mgmt.py send_to_wbrs_mgmt.*class .wbrs.wbrs_mgmt.WBRSManagementError.*File.*mgmt_server.py.*in __mgmt_server_handler.*No such file or directory"',
    '-v -E "Errno 2.*No such file or directory.*/data/tmp/(reqscand2|wbnpd)_rpc.sock"',
    '-v -E "featurekey adjustment failed.*The daemon is not responding"',
    '-v "coro._coro.TimeoutError"',

    '-v  "\\[Errno 61\\] Connection refused"',
    '-v "failed to connect to host"',

    '-v -E "DNS (Hard Error|Error|Soft Error)"',
    # until bug CSCul10478 is fixed in 8.2.0 version
    '-v -E "Critical.*ISQ"',
    ]

def get_patterns():
    return LOG_ERROR_PATTERNS
