#!/usr/bin/env python
import pexpect
import datetime
import os
import time
import json
import argparse
import sys
from pathlib import Path

DEFAULT_PROMPTS = {
       'ROOT_PROMPT':'\]#',
       'ESA_SMA_PROMPT':'>',
       'USER_PROMPT':'\$'
     }

class CliUtils:

    def __init__(self):
        self.session = None
        self.isconnected = False


    def ssh_login(self, host, user, password,log_filename):
        self.log = open(log_filename,'wb')
        print(log_filename)
        ssh_command =  'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no  {0}@{1}'.format(user,host)
        print(ssh_command)
        self.session =  pexpect.spawn(ssh_command,logfile=self.log)
        if self.session:
            self.isconnected = True
        self.session.expect('password:',timeout=20)
        self.session.sendline(password)
        self.session.expect(DEFAULT_PROMPTS['USER_PROMPT'],timeout=20)
        return self.session.before.decode("us-ascii") + self.session.after.decode("us-ascii")

   
    def execute_command(self, command, prompt=DEFAULT_PROMPTS['ROOT_PROMPT'], wait_time=120):
        try:
            self.session.sendline(command)
            self.session.expect(prompt,timeout=wait_time)
            cmd_output = self.session.before.decode("us-ascii") + self.session.after.decode("us-ascii")
            return cmd_output
        except pexpect.TIMEOUT:
            raise  Exception("{0} - command did not execute in the given time {1} seconds ".format(command,wait_time))
            return False

    def close_session(self):
        if self.isconnected:
            print("Closing the session")
            self.session.close()




# Create the parser
arg_parser = argparse.ArgumentParser(description='Updates Atlas')

# Add the arguments
arg_parser.add_argument('--version',
                       type=str,
                       help='Version of atlas')

arg_parser.add_argument('--atlasip',
                       type=str,
                       help='IP address of atlas')

arg_parser.add_argument('--atlasuser',
                       type=str,
                       help='atlas user name')

arg_parser.add_argument('--atlaspassword',
                        metavar="password",
                       help='atlas user password')

# Execute the parse_args() method
args = arg_parser.parse_args()

atlas_version = args.version
atlas_label = atlas_version[12:]
print('Build label Passed from Jenkins: {}'.format(atlas_version))
atlas_version = atlas_version[:6] + atlas_version[6:].replace('-' , '.' , 2) + '.noarch'
atlas_ip = args.atlasip
atlas_username = args.atlasuser
atlas_password = args.atlaspassword
cli = CliUtils()
path = path = Path(__file__).parent.absolute()
logs_path = os.path.join(path,"atlas-upgrader.log")


cli.ssh_login(atlas_ip,atlas_username,atlas_password,logs_path)
print('Atlas login is completed')
cli.execute_command('sudo bash')
current_version = cli.execute_command("rpm -qa | grep atlas")
current_version = current_version.split('\n')[1]
current_label = current_version[29:32]

#current_version is the image present on Atlas and atlas_version is from version passed from jenkins 
print(" Image to be Upgraded on Atlas: {} ,  Current Image on Atlas: {}".format(atlas_version,current_version))

cmd = ""
if "5.0.1" in atlas_version and "5.0.0" in current_version:
    cmd = "yum install "
if "5.0.0" in atlas_version and "5.0.1" in current_version:
    cmd = "yum downgrade "
if "5.0.1" in atlas_version and "5.0.1" in current_version:
    if (atlas_label > current_label):
        cmd = "yum upgrade "
    elif (atlas_label < current_label):
        cmd = "yum downgrade "
if "5.0.0" in atlas_version and "5.0.0" in current_version:
    if (atlas_version in current_version):
        cmd = "yum reinstall"  
    else:
        cmd = "yum upgrade"
        

print('Allow the Image to be Synced from Spacewalk Server')
time.sleep(210)
cli.execute_command("yum search --showduplicates atlas | grep {}  > checkversion".format(atlas_version))
spacewalkcheck = cli.execute_command("awk '{print $1}' checkversion")
spacewalkcheck = spacewalkcheck.split('\n')[1]
if(atlas_version in spacewalkcheck):
    print('Package is present and  can be pushed to Altas')
    cli.execute_command('systemctl stop httpd','\]\#')
    cli.execute_command('systemctl stop celery','\]\#')
    time.sleep(5)
    print('Command to be executed on Atlas: {} -y {} --nogpgcheck'.format(cmd,atlas_version))
    actual_output = cli.execute_command('{} -y {} --nogpgcheck'.format(cmd,atlas_version))
    print(actual_output)
    cli.execute_command('sudo /usr/local/ironport/atlas/bin/atlas-configure.sh -s /usr/local/ironport/.configbuilder/ -v3')
    print('Restarting httpd and celery ')
    cli.execute_command('systemctl start httpd','\]\#')
    cli.execute_command('systemctl start celery','\]\#')
    print('Httpd and Celery Restarted')
    cli.close_session()
else:
    cli.close_session()
    expected_output = "No package" 
    raise Exception("Update Failed due to {}".format(expected_output))
