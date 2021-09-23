# $Id: //prod/main/sarf_centos/variables/error_log_branches/phoebe.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $
""" Patterns for determining errors in logs
This is a default set of patterns.
If you need to use a different one, create a corresponding file
and provide its name as a parameter while starting robot as
--variablesfile <file_name>
"""

LOG_ERROR_PATTERNS = [
    '-E "'\
    '(Error'\
    '|Critical:'\
    '|Exception'\
    '|appfault'\
    '|application.fault'\
    '|failed consistency check'\
    '|No module named)"',


    # skip
    '-v -i "Info:"',
    '-v -i "Warning:"',
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
    '-v -E "Errno 2.*No such file or directory.*/tmp/(mcafee|sophos)_fastrpc.sock"',
    '-v -E "(xfp|db|fp)match - Error parsing configuration info needed for initialization"',
    '-v -E "User \\w+ entered"',
    '-v -E "to [\\w\\.@]+ with subject"',
    '-v "ssl handshake failure"',
    # Antivirus has detected an encrypted message
    '-v "0x80040212"',
    '-v "\\[Errno 32\\] Broken pipe"',
    '-v "\\[Errno 65\\] No route to host interface"',
    '-v -E "DNS (Hard Error|Error)"',
    '-v "\\[Errno 61\\] Connection refused"',
    '-v "EOF interface"',
    '-v "Could not update auto configuration from disk"',
    '-v "failed to connect to host"',
    '-v "sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target"',
    # skip until LS-3014 is fixed
    '-v "phone.base.ManifestError"',
    '-v "updater.exceptions.DownloadError"',
    # sophos error
    '-v ".*Exception in thread Thread.*:\n /data/log/heimdall/sophos"',
    ]

def get_patterns():
    return LOG_ERROR_PATTERNS
