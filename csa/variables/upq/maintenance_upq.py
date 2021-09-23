# $Id: //prod/main/sarf_centos/variables/upq/maintenance_upq.py#1 $

""" Variables for Maintenance UPQ configuration """

import os
import socket

# test lab variables for upload/download files over HTTP/S
UPQ_SERVER_HOSTNAME = 'vm10bsd0150.wga'
UPQ_HTTP_SERVER = 'http://' + UPQ_SERVER_HOSTNAME
UPQ_HTTPS_SERVER = 'https://' + UPQ_SERVER_HOSTNAME
UPLOAD_PAGE = '/upload'
DOWNLOAD_PAGE = '/uploads/'

# test lab variables for uload/download files over FTP
UPQ_FTP_SERVER = UPQ_SERVER_HOSTNAME
RTESTUSER = 'rtestuser'
TESTUSER_PASSWORD = 'ironport'

# test files variables
TESTDATA_DIR = os.environ['SARF_HOME'] + '/tests/testdata/'
UPLOAD_FILES_DIR = TESTDATA_DIR + 'upq/files_to_upload/'
FILE_TO_UPLOAD = 'testfile.txt'

# UPQ configuration variables
UPQ_IDENTITY = 'upgrade identity'
UPQ_USER_AGENT = 'Firefox'
UPQ_URL_CATEGORY = 'upgrade cust cat'
UPQ_ACCESS_POLICY = 'upgrade policy'
UPQ_DECRYPTION_POLICY = 'upgrade decryption policy'
UPQ_NTLM_REALM = 'NTLM Realm'

# for configuration file
CLIENT_NETWORK = socket.gethostname().split('.')[-1].upper()

ERRORS_TO_IGNORE = [
        "<type 'exceptions\.IOError'>=\[Errno 32\] Broken pipe",
        "Failed to tell heimdall we're ready",
        'AVC_Engine failed to connect to \/tmp\/avc_fastrpc\.sock',
        'SSL error with client',
        'Watchdog timed out',
        '\[cli\/cli\.py _reboot_or_shutdown\|19622\] \[command_manager\/command_client.py call\|238\]',
        'featurekey adjustment failed',
        'mcafee: Watchdog detected an error',
        'wbrs\/update\.py __rollback_engine\|268\] \[heimdall\/svc\.py send_command\|183\] \[socket\.pyx coro\._coro\.sock\.connect \(coro\/_coro\.c\:22756\)\|1016',
        'wbrsd: Watchdog detected an error',
        ]
