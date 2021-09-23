#-------------------------------------------------------------------------------
# Name:        clean_apache_logs.py
# Purpose:     This modules connects to the http server provided as command arg
#              and cleans httpd logs and then restarts apachectl
#
# Author:      sremanda
#
# Created:     27/04/2015
# Copyright:   (c) Cisco systems
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import sys
import paramiko
import re

cmd_args = sys.argv
http_server = None
httpd_aclog = r"/var/log/httpd-access.log"
httpd_errlog = r"/var/log/httpd-error.log"
httpd_logs = r"/var/log/httpd-*.log"
server_user = r"rtestuser"
server_pswd = r"ironport"

def connect_to_server():
    """ The function is to open a SSH client to a HTTP server and perform
    actions specifed"""

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(http_server, username=server_user, password=server_pswd)
    return ssh

def run_command(ssh, cmd=None):
    """ This function is to run commands specified on the SSH session opened"""

    stdin,stdout,stderr = ssh.exec_command(cmd)
    stdin.close()
    out = stdout.readlines()
    for msg in out:
	print msg.rstrip()

def get_http_server(cmd_args):
    """ This function parses HTTP_SERVER from jenkins additional parameters"""

    print "Parsing HTTP Server from additional arguments passed in Jenkins"
    try:
        if cmd_args:
            for cmd_arg in cmd_args:
                temp = re.search("HTTP_SERVER:(.*)", cmd_arg.rstrip(),)
                if temp:
                    return temp.group(1)
                else:
                    next
    except Exception as exp:
        print "Exception encountered :" + str(exp)
        sys.exit()

try:
    #Parse cmd args to extract HTTP_SERVER
    http_server = get_http_server(cmd_args)

    if http_server:
        print "Connecting to HTTP server : " + http_server
        ssh = connect_to_server()

        print "Clearing apache logs..."
        run_command(ssh, "cat /dev/null > " + httpd_aclog)
        run_command(ssh, "cat /dev/null > " + httpd_errlog)

        print "Restarting apache..."
        run_command(ssh, "apachectl restart")
    else:
        print "Cloud not clean http server logs, No HTTP_SERVER variable passed in Jenkins as additional arguments"
except Exception as exp:
        print "Exception encountered :" + str(exp)
        sys.exit()
