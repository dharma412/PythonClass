#-------------------------------------------------------------------------------
# Name:        copy_tg_apikey.py
# Purpose:     This module is used to backup TG API key from WSA and restore it
#              back to WSA
# Author:      sremanda
# Created:     27/04/2015
# Copyright:   (c) sremanda 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pexpect
import socket
import sys
import os

#Get the WSA version from command line args
wsa = sys.argv[1]
#Get the client hostname
client = socket.gethostname()

#Exit if wsa or client variables not defined
if not wsa or not client:
    sys.exit()

#Get the action type specified either back or restore
action_type = sys.argv[2]

#API Key path on WSA and client
apikey_path = r"/data/fire_amp/db/preserve/analysis.key"
client_backup_path = r"/tmp/tg_apikey"

#WSA/Client credentials
user = r"rtestuser"
pswd = r"ironport"

#Method to handle pexpect responses
def handle_response(resp=3):
    try:
        #Add host to known list
        if resp == 0:
            child.sendline('yes')
        #Send password
        if resp == 1:
            child.sendline (pswd)
        if resp == 3:
            print "Timeout occurred..., Bye!!!"
            sys.exit()
    except Exception as exp:
        print "Exception encountered :" + str(exp)
        child.close()
        sys.exit()

try:
    if wsa:
        """ The function is to open a SSH client to a WSA and perform
        actions specifed"""

        #client the client backup path if doesn't exist
        if not os.path.exists(client_backup_path):
            os.mkdir(client_backup_path)

        wsa_name = wsa.split('.')[0]

        #SSH to WSA
        ssh_command = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ' + user + '@' + wsa
        child = pexpect.spawn(ssh_command)

        ssh_newkey = 'Are you sure you want to continue connecting'
        resp=child.expect([ssh_newkey, '[Pp]assword:', pexpect.EOF, pexpect.TIMEOUT], 90)
        #Handle the pexpect response
        handle_response(resp)

        #Should provide password when host to is added to known list
        if resp == 0:
            child.expect ('Password:')
            child.sendline (pswd)

        #Expect the prompt to be available
        child.expect (wsa_name + ':' + user + ' 1] ')

        #Prepare the SCP command based on the action type
        if action_type == 'backup_apikey':
            scp_cmd = 'scp ' + apikey_path + ' ' + user + '@' + client + \
                    ':' + client_backup_path + "/" + wsa_name + ".key"
            msg = "Backing up TG API Key from " + wsa
        elif action_type == 'restore_apikey':
            if not os.path.exists(client_backup_path + "/" + wsa_name + ".key"):
                print "No TG API Key available to restore on " + wsa
                child.close()
                sys.exit()
            scp_cmd = 'scp ' + user + '@' + client + ':' + client_backup_path + "/" + \
                    wsa_name + ".key " + apikey_path
            msg = "Restoring TG API Key to " + wsa
        else:
            child.close()
            sys.exit()

        print msg

        child.sendline (scp_cmd)
        resp=child.expect([ssh_newkey,
                        'Password for ' + user + '@' + client + ':',
                        'cp: ' + apikey_path + ': No such file or directory',
                        pexpect.EOF,
                        pexpect.TIMEOUT],
                        1)

        handle_response(resp)

        if resp == 0:
            child.expect ('Password for ' + user + '@' + client + ':')
            child.sendline (pswd)

        resp = child.expect ([wsa_name + ':' + user + ' 2] ', apikey_path + ': No such file or directory'], 90)

        if resp == 1:
            print "API Key not available on " + wsa

        child.close()
    else:
        print "No wsa variable passed"
except Exception as exp:
        print "Exception encountered :" + str(exp)
        sys.exit()

