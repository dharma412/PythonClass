#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/misc.py#8 $
# $DateTime: 2019/09/30 02:53:55 $
# $Author: amanikaj $

from common.util.utilcommon import UtilCommon
from tempfile import mkstemp
from shutil import move
from os import remove, close
from ipaddr import IPv4Network
import hashlib
import re
import os
import time
import socket
import pexpect
import urllib2
import stat
import ConfigParser
import sys
import SSHLibrary
import common.Variables
import paramiko
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import email
import email.mime.application

import subprocess


class ProcessesAreNotReady(Exception):
    pass


class VerificationFailed(Exception):
    pass


class NoConfigFileError(IOError):
    pass


class Misc(UtilCommon):
    """
    Miscellaneous keywords
    """

    def get_keyword_names(self):
        return [
            'wsa_status',
            'send_mail',
            'get_host_ipv6_by_name',
            'get_config_file',
            'get_file_md5',
            'verify_file_md5',
            'wait_until_ready',
            'scp',
            'run_on_host',
            'run_on_slice_server',
            'run_on_dut',
            'dut_file_exists',
            'copy_file_from_dut_to_remote_machine',
            'copy_file_to_dut',
            'configure_http_server',
            'configure_cntlm_conf',
            'generator_ipv4',
            'get_xml_file_from_jenkins',
            'get_curl_command',
            'get_library_name',
            'get_test_folder',
            'get_admin_password',
            'get_gen_pass',
            'get_cli_pattern_match',
            'get_upq_cust_keyword',
            'get_file_permission',
            'ssh_keyboard_auth_brute_force_vulnerability_check',
        ]

    def send_mail(self,
                  fromaddr='gopselva@cisco.com',
                  toaddr='gopselva@cisco.com',
                  smtpaddr='xch-rtp-007.cisco.com',
                  subject='Soak Monitor',
                  attachfile='test.txt',
                  setup='soak',
                  prox_stat='',
                  no_cores='',
                  app_fault='',
                  ):
        sender = "%s" % fromaddr
        receivers = "%s" % toaddr

        if setup == 'soak':
            body = email.mime.Text.MIMEText("""Hi
================
Number of cores
================
%s

================
Application Fault
================
%s

================
Prox Track Log
================
%s

=====================================================================
Thanks,""" % (no_cores, app_fault, prox_stat))
        elif setup != 'soak':
            body = email.mime.Text.MIMEText("""Hi
================
Number of cores
================
%s

================
Application Fault
================
%s

=====================================================================
Thanks,""" % (no_cores, app_fault))

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receivers

        attachment = MIMEBase('application', "octet-stream")
        attachment.set_payload(open("/home/testuser/work/sarf/%s" % attachfile, "rb").read())
        attachment.add_header('Content-Disposition', 'attachment; filename=%s' % attachfile)

        msg.attach(attachment)
        msg.attach(body)
        try:
            smtpObj = smtplib.SMTP('%s' % smtpaddr)
            smtpObj.sendmail(msg['From'], msg["To"].split(","), msg.as_string())
            print "Successfully sent email"
        except SMTPException:
            print "Error: unable to send email"

    def wsa_status(self,
                   server='wsaxxx.wga',
                   adminpass='Cisco123$',
                   logfile='test.txt',
                   ):

        clilog = ['', '', '', '']
        cmdlog = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        clicount = 0
        cmdcount = 0
        ruser = 'rtestuser'
        rpass = 'ironport'
        adminuser = 'admin'
        fo = open("/home/testuser/work/sarf/%s" % logfile, "w+")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username=ruser, password=rpass)
        ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh1.connect(server, username=adminuser, password=adminpass)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("date")
        dateout = ssh_stdout.read()
        daterep = dateout.replace("  ", " ")
        date = daterep.split(" ")
        thisD = date[2]
        if int(date[2]) < 10:
            thisD = "0" + date[2]
        latency_cmd = "awk -F\" \" -v last=\"\"\"\`date +%s\`\"\"\" -v x=14400 \'{split($1,a,\"\\.\");getline d; z=last-a[1]; if(z<=x && $2 >120000 && (\!match($4,/[A-Z_]+\/5[0-5]+/) && \!match($6,/TCP_CONNECT/) )) print $0 }\'"
        clicmd = """version
status detail"""
        cmd = """top -b all | egrep 'SIZE|snmpd'
ipmitool sel list -30
ls /data/cores/*.core | wc -l
ls -lt /data/cores/*.core
top -m cpu
egrep -i 'out of swap space' /var/log/messages
egrep -i 'started' /data/log/heimdall/heimdall/heimdall.current | grep '%s %s'
egrep -i 'Critical|Warning|Error' /data/log/heimdall/heimdall/* | grep '%s %s'
grep -r 'application fault occurred' /data/pub/*logs/* | egrep -i 'critical\\:|warning\\:|error\\:' | grep '%s %s'
%s /data/pub/accesslogs/aclog\.current
tail -n 2150 /data/pub/track_stats/prox_track.log
tail -n 1000 /data/log/stdout/stdout_upgrade.log""" % (thisD, date[1], thisD, date[1], thisD, date[1], latency_cmd)

        clilist = clicmd.split("\n")
        cmdlist = cmd.split("\n")
        for clicmd in clilist:
            fo.write(
                "*************************************************************************************************************************************\n")
            fo.write(clicmd)
            fo.write("\n---------------------------------------------\n")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh1.exec_command(clicmd)
            clilog[clicount] = ssh_stdout.read()
            fo.write(clilog[clicount])
            clicount = clicount + 1
        for command in cmdlist:
            fo.write(
                "*************************************************************************************************************************************\n")
            fo.write(command)
            fo.write("\n---------------------------------------------\n")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
            cmdlog[cmdcount] = ssh_stdout.read()
            fo.write(cmdlog[cmdcount])
            cmdcount = cmdcount + 1
        fo.write(
            "*************************************************************************************************************************************\n")
        tab = cmdlog[10].split("\n")
        prox_track = ''
        l = [tab.index(i) for i in tab if 'INFO: cache memory blocks; size:used:free:reserved:' in i]
        k = [tab.index(i) for i in tab if 'Total count of stale fd:' in i]
        for i in range(l[0], k[0] + 1):
            print tab[i]
            prox_track = prox_track + tab[i] + "\n"
        ssh.close()
        ssh1.close()
        fo.close()
        return (prox_track, cmdlog[2], cmdlog[8])

    def get_file_permission(self, filepath):
        st = os.stat(filepath)
        print st
        return bool(st.st_mode & stat.S_IWGRP)

    def get_upq_cust_keyword(self, config_filename):

        arr_request = []
        config = ConfigParser.ConfigParser()
        print config_filename
        config.read(config_filename)
        sections_list = config.sections()
        print sections_list
        for section in sections_list:
            section_items = config.items(section)
            section_options = config.options(section)
            if config.get(section, 'type') == 'httpget':
                variable = 'Send HTTP Get Request'
            elif config.get(section, 'type') == 'httppost':
                variable = 'Send HTTP Post Request'
            elif config.get(section, 'type') == 'httpsget':
                variable = 'Send HTTPS Get Request'
            elif config.get(section, 'type') == 'httpspost':
                variable = 'Send HTTPS Post Request'

            for options in section_options:
                if options != 'type':
                    variable = variable + '    ' + config.get(section, options)
                    print variable
            arr_request.append(variable)
        return arr_request

    def get_host_ipv6_by_name(self, host):
        """
        Return IPv6 of the specified host
           or None if IPv6 can not be determined
        Parameters:
        - `host` - name of the host

        Example of Usage:
        ${ipv6}=    Get Host IPv6 By Name    ${DUT}
        """
        try:  # http://stackoverflow.com/questions/16276913/reliably-get-ipv6-address-in-python
            result = socket.getaddrinfo(host, None, socket.AF_INET6)[0][4][0]
            return result
        except Exception as e:
            self._warn(
                '{type}:{message} while getting IPv6 address for {host}'. \
                    format(type=type(e).__name__,
                           message=e.message,
                           host=host, ))
            return None

    def get_library_name(self, dut):
        """
        Connects to specified appliance, gets installed version,
        and returns name of corresponding automation testlib folder
        Parameters:
        - `dut` - appliance under test
        """
        s = self._get_library(dut, 'testlib')
        if s:
            return s[s.rfind(os.path.sep) + 1:]
        else:
            return s

    def get_test_folder(self, dut):
        """
        Connects to specified appliance, gets installed version,
        and returns location of correspondent automation tests folder
        Parameters:
        - `dut` - appliance under test
        """
        return self._get_library(dut, 'tests')

    def _get_library(self, HOST, directory):
        USER = 'rtestuser'
        PWD = 'ironport'
        PROMPT = ']'
        CAT_COMMAND = 'cat /data/VERSION'
        CONNECTION_STRING = \
            'ssh -4 -q -t -o StrictHostKeyChecking=no -o ' + \
            'UserKnownHostsFile=/dev/null {user}@{host}'.format(user=USER, host=HOST)
        try:
            sql_session = pexpect.spawn(CONNECTION_STRING)
            i = sql_session.expect(['Password:', '.*password:', '\?'], timeout=120)
            if i == 2:  # first connection to the box
                self._info('first connection to the box')
                sql_session.sendline('yes')
                sql_session.expect('Password:', timeout=120)
            sql_session.sendline(PWD)
            sql_session.expect(PROMPT)
            sql_session.sendline(CAT_COMMAND)
            sql_session.expect('2]')
            line = sql_session.before.splitlines()[-2].split('-')[0]
        except:
            self._warn('Failure during pexpect ' + sql_session.before)
            return None
        finally:
            sql_session.terminate()
        self._debug("Searching for closest {directory} folder for {name}". \
                    format(directory=directory, name=line))
        name = line.replace(' ', '').replace('.', '')
        if os.environ.has_key('SARF_HOME'):
            full_name = os.path.join(os.environ['SARF_HOME'], directory, name)
        else:
            full_name = os.path.join(directory, name)
        self._debug("Load Library: Level1")
        for i in range(1, 4):
            folder = (full_name + ' ')[:-i]
            self._debug("Checking: %s" % folder)
            if os.path.exists(folder):
                self._debug("Going with {folder} for closest {directory}". \
                            format(folder=folder, directory=directory))
                return folder
        self._debug("Load Library: Level2")
        for i in range(1, 4):
            folder = (full_name + ' ')[:-i] + ('0' * (i - 1))
            self._debug("Checking: %s" % folder)
            if os.path.exists(folder):
                self._debug("Going with {folder} for closest {directory}". \
                            format(folder=folder, directory=directory))
                return folder
        self._warn("Can not find {directory} folder for {name}". \
                   format(directory=directory, name=line))
        return None

    def get_curl_command(self, params):
        """
        creates IP_Protocol specific curl command based on parameter ${IPV_PARAM}
        executing curl with '-4' or '-6' is much faster
        """
        variables = common.Variables.get_variables()
        proto_param = '-4'
        if "${IPV_PARAM}" in variables:
            proto_param = variables["${IPV_PARAM}"]

        return 'curl %s %s' % (proto_param, params)

    def get_admin_password(self, dut):
        """
        Check whether updated(SSW) password is set for the dut
        if none of them can't be used, raises an Exception
        """
        variables = common.Variables.get_variables()
        user = 'admin'
        if "${DUT_ADMIN}" in variables:
            user = variables["${DUT_ADMIN}"]
        password = 'ironport'
        if "${DUT_ADMIN_PASSWORD}" in variables:
            password = variables["${DUT_ADMIN_PASSWORD}"]
        ssw_password = 'Cisco12$'
        if "${DUT_ADMIN_SSW_PASSWORD}" in variables:
            ssw_password = variables["${DUT_ADMIN_SSW_PASSWORD}"]
        tmp_password = 'Cisco21$'
        if "${DUT_ADMIN_TMP_PASSWORD}" in variables:
            tmp_password = variables["${DUT_ADMIN_TMP_PASSWORD}"]

        CONNECTION_COMMAND = \
            'ssh -4 -q -t -o UserKnownHostsFile=/dev/null ' + \
            '-o StrictHostKeyChecking=no {user}@{host}'.format(user=user, host=dut)
        self._info("CONNECTION_COMMAND: '%s'" % CONNECTION_COMMAND)
        try:
            self._info("Trying '{}'".format(password))
            pexpect_session = pexpect.spawn(CONNECTION_COMMAND)
            pexpect_session.expect('assword:', timeout=35)
            pexpect_session.sendline(password)
            index = pexpect_session.expect(['assword:', 'Old Password:', '>', 'change your password now'], timeout=60)
            if index:
                return password
            self._info("Trying '{}'".format(ssw_password))
            pexpect_session.sendline(ssw_password)
            index = pexpect_session.expect(['assword:', 'Old Password:', '>', 'change your password now'], timeout=60)
            print "Index: " + str(index)
            if index:
                return ssw_password
            self._info("Trying '{}'".format(tmp_password))
            pexpect_session.sendline(tmp_password)
            index = pexpect_session.expect(['assword:', 'Old Password:', '>', 'change your password now'], timeout=60)
            if index:
                return tmp_password
            self._warn( \
                'Can not ssh to {dut} as {user}/{pwd} or {user}/{ssw_pwd}'. \
                    format(dut=dut, user=user, pwd=password, ssw_pwd=ssw_password))
            return 'ironport'
        except:
            self._warn('Failure during pexpec, restoring the session SSH')
        finally:
            pexpect_session.terminate()

    def get_xml_file_from_jenkins(self,
                                  link,
                                  from_host="auto01.wga.sbr.ironport.com",
                                  from_user='testuser',
                                  from_password='ironport',
                                  from_prompt='$',
                                  from_location=None,

                                  #      to_parameters
                                  to_host=None,
                                  to_user='testuser',
                                  to_password='ironport',
                                  to_location="output.xml",
                                  ):
        """
        Parses link from format
        http://auto01.wga.sbr.ironport.com/jenkins/job/<Server><ProjectName>/<ID>/robot/report/<OutputFile>.report.html
        i.e http://auto01.wga.sbr.ironport.com/jenkins/job/Coeus-7-5_CLI_Test/289/robot/report/sarfclicheck.report.html
        ProjectName:  Coeus-7-5_CLI_Test
        ID: 289
        OutputFile: sarfcliheck

        and scp file
        /data/jenkins/jobs/< ProjectName>/builds/<ID>/robot-plugin/<OutputFile>.xml
        to client

        Parameters:
        - `link`: link to a file in a directory with xml to copy. That should not be
         necessarily a link to xml file
        - `from_host`: name or IP of Jenkins server
        - `from_user`: username on Jenkins server
        - `from_password`: password on Jenkins server
        - `from_prompt`: prompt on Jenkins server
        - `to_host`: Client
        - `to_user`: username on Client
        - `to_password`: password on Client
        - `to_location`: destination of xml file

        Exceptions:
        - ValueError: Invalid link '<link>'

        Examples:
        | Get Xml File From Jenkins |
        | ... | http://auto01.wga.sbr.ironport.com/jenkins/job/Coeus-7-5_CLI_Test/289/robot/report/sarfclicheck.report.html |
        """
        if not re.match('http://[^/]+/jenkins/.*/[0-9]+/robot/report/.+', link):
            raise ValueError("Invalid link '%s'" % link)
        array = link.split("/")
        for num in range(len(array) - 1, 1, -1):
            if array[num] == "robot":
                break
        else:
            raise ValueError("Invalid link '%s'" % link)
        projectName = array[num - 2]
        id = array[num - 1]
        outputFile = array[-1].split(".")[0]
        if num > 4:
            from_host = array[num - 5]
        from_location = "/data/jenkins/jobs/%s/builds/%s/robot-plugin/%s.xml" % \
                        (projectName, id, outputFile)
        if not to_host:
            to_host = self._get_parameter("${CLIENT_IP}")
        self.scp(
            from_host=from_host,
            from_user=from_user,
            from_password=from_password,
            from_prompt=from_prompt,
            from_location=from_location,
            to_host=to_host,
            to_user=to_user,
            to_password=to_password,
            to_location=to_location,
        )
        self.run_on_host(to_host, to_user, to_password,
                         "chmod 777 %s" % to_location)

    def configure_cntlm_conf(self,
                             cntlm='/etc/cntlm.conf',
                             username='ntlm1',
                             domain='wga',
                             password='ironport',
                             proxy_host=None,
                             proxy_port='3128'
                             ):
        """ Configures cntlm configuration

        Parameters:
        - `username`: - username for ntlm authentication
        - `password`: - password for ntlm authentication
        - `domain` - domain for ntlm authentication
        - `proxy_host`: - if not specified, uses that value for dut
           defaults to ${DUT}
        - `proxy_port`: - port number of the ntlm proxy

        Examples:
        | Configure Cntlm Conf |

        | Configure Cntlm Conf |
        | ... | proxy_host=${DUT} |
        | ... | proxy_port=3128 |
        | ... | username=ntlm1 |
        | ... | password=ironport |
        | ... | domain=wga |
        """
        if proxy_host == None:
            proxy_host = self.dut

        fh, abs_path = mkstemp()
        new_file = open(abs_path, 'w')

        new_file.write("Username          %s\n" % username)
        new_file.write("Domain          %s\n" % domain)
        new_file.write("Password          %s\n" % password)
        new_file.write("Proxy          %s:%s\n" % (proxy_host, proxy_port))
        new_file.write("Listen          3128\n")
        new_file.write("Header User-Agent: Mozilla/5.0")

        # close temp file
        new_file.close()
        close(fh)

        # Remove original file
        remove(cntlm)
        # Move new file
        move(abs_path, cntlm)

    def configure_http_server(self,
                              host=None,
                              httpd='/usr/local/etc/apache22/httpd.conf',
                              httpd_ssl='/usr/local/etc/apache22/extra/httpd-ssl.conf',
                              listen_ports='80, 9009, 3128, 8443, 5050, 443',
                              ssl_listen_ports='443',
                              ssl_protocols=None,
                              ssl_cipher_suite= \
                                      'ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP:+eNULL',
                              ):
        """ Configures http server and restarts it.
        The default settings files are stored in the tests/data.

        Parameters:
        - `host`: - name or IP address of http server;
           defaults to ${SLICE_SERVER}
        - `httpd`: - location of configuration file for http connections
        - `httpd_ssl`: - location of configuration file for https connections
        - `listen_ports`: - list of comma-separated ports for http connections
        - `ssl_listen_ports` - list of comma-separated ports for https
        connections
        - `ssl_protocols` - protocols for ssl connections;
        example: '-All -SSLv2 -SSLv3 +TLSv1'
        - `ssl_cipher_suite`: - setting of SSLCipherSuite

        Examples:
        | Configure Http Server | - restores the defaults

        | Configure Http Server |
        | ... | host=${SLICE_SERVER} |
        | ... | listen_ports=80,234 |
        | ... | ssl_listen_ports=843 |
        | ... | ssl_protocols=-All -SSLv2 -SSLv3 +TLSv1 |
        """
        COMMENT = 'Settings added by configure_http_server'
        VIRTUAL_HOST = '<VirtualHost'
        LISTEN = 'Listen'

        command = "grep -v -E -i '^(%s|SSLProtocol|SSLCipherSuite) .*' %s " % (LISTEN, httpd)
        command += "| grep -v '%s' " % COMMENT
        command += " > %s.new;" % httpd
        command += "echo \\# %s >> %s.new;" \
                   % (COMMENT, httpd)
        if listen_ports:
            for port in listen_ports.split(','):
                if port.strip():
                    command += "echo %s %s >> %s.new;" % (LISTEN, port.strip(), httpd)

        command += \
            "grep -v -E -i '^(%s|SSLProtocol|SSLCipherSuite) .*' %s " \
            % (LISTEN, httpd_ssl)
        command += "| grep -v '%s' " % COMMENT
        command += " > %s.new;" % httpd_ssl
        command += \
            "echo \\# %s >> %s.new;" % (COMMENT, httpd_ssl)
        if ssl_protocols:
            command += "echo SSLProtocol %s >> %s.new;" % \
                       (ssl_protocols.strip(), httpd_ssl)
            command += "echo SSLProtocol %s >> %s.new;" % \
                       (ssl_protocols.strip(), httpd)
        if ssl_cipher_suite:
            command += "echo SSLCipherSuite %s >> %s.new;" % \
                       (ssl_cipher_suite.strip().replace('!', r'\!'), httpd_ssl)
            command += "echo SSLCipherSuite %s >> %s.new;" % \
                       (ssl_cipher_suite.strip().replace('!', r'\!'), httpd)
        command += "mv %s.new %s;" % (httpd, httpd)
        virtual_host_defaults = VIRTUAL_HOST
        if ssl_listen_ports:
            for port in ssl_listen_ports.split(','):
                port = port.strip()
                if port:
                    command += "echo %s %s >> %s.new;" % \
                               (LISTEN, port, httpd_ssl)
                    virtual_host_defaults += (" _default_:" + port)
        virtual_host_defaults += '>'
        command += "sed -e 's/%s .*/%s/g' %s.new > %s;" % \
                   (VIRTUAL_HOST, virtual_host_defaults, httpd_ssl, httpd_ssl)
        command += "apachectl restart"
        self._info("Configuring http_server\n'%s'" % command)
        self.run_on_slice_server(command, host)

    def scp(self,
            recursive='',

            #      from_parameters
            from_host=None,
            from_user='rtestuser',
            from_password='ironport',
            from_prompt='#',
            from_location=None,

            #      to_parameters
            to_host=None,
            to_user='rtestuser',
            to_password='ironport',
            to_location=None,

            timeout=120
            ):
        """ Copy file(s) or folders(s) between remote hosts using scp

        Parameters:
        - `recursive`: recursive copying; accepted values '-r' or empty string
        - `from_host`: name or IP of host with source files
        - `from_user`: username of host with source files
        - `from_password`: password of host with source files
        - `from_prompt`: prompt of host with source files
        - `from_location`: location of source files
        - `to_host`: name or IP of destination host
        - `to_user`: username on destination host
        - `to_password`: password on destination host
        - `to_location`: destination of copying
        - `timeout`: maximum timeout to wait, default is 120s

        Examples:
        | scp | from_host=${CLIENT_IP} | from_location=${EXECDIR}/tests/testdata/*.py |
        | ... | to_host=${DUT} | to_location=/tmp |
        | scp | to_host=${CLIENT_IP} | to_location=/tmp |
        | ... | from_host=${DUT} | from_location=/data/pub |
        | ... | recursive=-r |
        """

        copy_command = "scp -4 -q -o StrictHostKeyChecking=no " + \
                       "-o UserKnownHostsFile=/dev/null -C %s %s %s@%s:" % \
                       (recursive, from_location, to_user, to_host) \
                       + to_location
        self._info("Executing '%s' from %s" % (copy_command, from_host))

        ## Increasing timeout as some scp take more than 60 secs to connect
        timeout = timeout
        _expected_strings = [
            'Are you sure you want to continue connecting (yes/no)?',
            'Enter passphrase for key',
            'assword:',
            'Password for %s@%s:' % (to_user, to_host)
        ]

        if (from_host is None) or (socket.gethostbyname(from_host) == socket.gethostbyname(socket.gethostname())):
            import pexpect
            _expected_strings.extend([pexpect.EOF, pexpect.TIMEOUT])
            child = pexpect.spawn(copy_command)
            _timer_start = time.time()
            while (time.time() - _timer_start) < int(timeout):
                index = child.expect(_expected_strings)
                self._info(child.before + str(_expected_strings[index]))
                if index == 0:
                    child.sendline('yes')
                if index == 1:
                    child.sendline('')
                if index == 2:
                    child.sendline(to_password)
                if index == 3:
                    child.sendline(to_password)
                if index == 4:
                    break
                time.sleep(1)
            child.close()
            return

        ssh = SSHLibrary.SSHLibrary()
        from_host_ip = socket.gethostbyname(from_host)
        try:
            ssh.open_connection(host=from_host_ip, prompt=from_prompt,
                                timeout=timeout)

            ssh.login(username=from_user, password=from_password)
            ssh.write(text=copy_command)

            _timer_start = time.time()
            while (time.time() - _timer_start) < int(timeout):
                _output = ssh.read()
                self._debug('(romete) found output: %s' % _output)
                if _output.find(_expected_strings[0]) > -1:
                    ssh.write(text='yes')
                if _output.find(_expected_strings[1]) > -1:
                    ssh.write(text='')
                if _output.find(_expected_strings[2]) > -1:
                    ssh.write(text=to_password)
                if _output.find(_expected_strings[3]) > -1:
                    ssh.write(text=to_password)
                if _output.find(from_prompt) > -1:
                    break
                time.sleep(1)
        finally:
            ssh.close_connection()

    def wait_until_ready(self, timeout=700):
        """
        Wait until all processes are ready.
        This is required when processes are restarted after SSW or other
        environment changes which take effect after corresponding processes
        are restarted.
        A python script is copied to the appliance and launched.
        The script is located @ tests/testdata/check_processes.py

        After all processes are ready wait another 5 sec
        (DEFAULT_ADDITIONAL_SLEEP) or time specified in optional parameter
        ${ADDITIONAL_SLEEP}

        Parameters:
        - `timeout` - maximum timeout to wait until all processes are ready

        Return:
        - output of check_processes.py

        Exceptions:
        - Exception ProcessesAreNotReady is raised if not all processes are
        ready

        Examples:
        | ${result}= | Wait Until Ready |
        | ${result}= | Wait Until Ready | 120 |
        """
        SOURCE = os.environ["SARF_HOME"] + '/tests/testdata/check_processes.py'
        DESTINATION = '/tmp/check_processes.py'
        DEFAULT_ADDITIONAL_SLEEP = 5
        SSH_RECONNECT_SLEEP = 30

        try:
            static_sleep = float(self._get_parameter("${ADDITIONAL_SLEEP}", \
                                                     DEFAULT_ADDITIONAL_SLEEP))
        except:
            self._info("Invalid value of ADDITIONAL_SLEEP is replaced by '%s'" \
                       % DEFAULT_ADDITIONAL_SLEEP)
            static_sleep = DEFAULT_ADDITIONAL_SLEEP

        result = None
        variables = common.Variables.get_variables()
        if not "${RTESTUSER}" in variables:
            variables["${RTESTUSER}"] = 'rtestuser'
        if not "${RTESTUSER_PASSWORD}" in variables:
            variables["${RTESTUSER_PASSWORD}"] = 'ironport'
        ssh = SSHLibrary.SSHLibrary()
        dut_ip = socket.gethostbyname(self.dut)
        start_time = time.time()
        while start_time + int(timeout) > time.time():
            try:
                print "Inside Try"
                ssh.open_connection(dut_ip, timeout=90)
                print "connection opened"
#                ssh.login(variables["${RTESTUSER}"], variables["${RTESTUSER_PASSWORD}"], )
                ssh.login(variables["${RTESTUSER}"], variables["${RTESTUSER_PASSWORD}"])
                print "Login happen"
                break
            except Exception as e:
                print e
                time.sleep(SSH_RECONNECT_SLEEP)
                ssh.close_connection()
                # ssh.open_connection(dut_ip)
        else:
            raise ProcessesAreNotReady('Can not ssh to dut')

        try:
            file_exists = bool(ssh.execute_command("[ -f %s ] && echo True" % DESTINATION))
            if not file_exists:
                self.copy_file_to_dut(SOURCE, DESTINATION)
            result0 = ssh.execute_command('python %s %s' % (DESTINATION, timeout))
            self._debug("check result0: %s" % result0)
            time.sleep(static_sleep)
            self._info("Sleep %s seconds between checks of all processes are ready" \
                       % static_sleep)

            result = ssh.execute_command('python %s %s' % (DESTINATION, timeout))
            self._debug("check result: %s" % result)
        finally:
            ssh.close_connection()
        if result is not None:
            ready = (result.find('ready now') > -1)
            if not ready:
                self._warn("Not all processes are ready!")
                raise ProcessesAreNotReady(result)
        time.sleep(static_sleep)
        self._info("Sleep %s seconds after all processes are ready" \
                   % static_sleep)
        return result

    def get_config_file(self, filename):
        """ Return path to a config file for actual AsyncOS version if
        it exists otherwise look for config files for previous versions.

        Parameters:
            - `filename`: path to the expected configuration file.
              Either absolute or relative to SARF/tests/testdata paths are
              accepted.

        Examples:
        | ${config} = | Get Config File | upq/config_files/${CLIENT_NETWORK}/7-0-0-819_P1_cleaned.xml |
        | ${config} = | Get Config File | /home/testuser/config_files/coeus-7-0-0-819_P1_cleaned.xml |
        """
        # get absolute filename if relative is given
        filename = self._get_absolute_path(filename)
        # check if file exists
        if os.path.exists(filename):
            return filename
        else:
            # get path to directory and filename
            dirpath, filename = os.path.split(filename)
            # prepare regexp pattern
            patt = re.sub(r'\d', '\d', filename)
            config_files = os.listdir(dirpath)
            matched_files = []
            for config_file in config_files:
                if re.match(patt, config_file) and config_file < filename:
                    matched_files.append(config_file)
            if len(matched_files) > 0:
                matched_files.sort()
                return os.path.join(dirpath, matched_files[-1])
            else:
                raise NoConfigFileError, \
                    "Configuration file for this or previous AsyncOS versions " \
                    "are not found. No files that match pattern: %s and are " \
                    "lower then %s" % (patt, filename)

    def get_file_md5(self, filename):
        """ Returns md5 sum of the file.

        Parameters:
            - `filename`: path to the file to calculate md5 sum.
              Either absolute or relative to SARF/tests/testdata paths are
              accepted.

        Examples:
        | ${sum} = | Get File MD5 | myfile.txt | #file SARF/tests/testdata/myfile.txt |
        | ${sum} = | Get File MD5 | /etc/resolv.conf | # absolute path to file |
        """
        # get absolute filename if relative is given
        filename = self._get_absolute_path(filename)
        # get md5sum
        file = open(filename, 'rb')
        md5 = hashlib.md5()
        buffer = file.read(2 ** 20)
        while buffer:
            md5.update(buffer)
            buffer = file.read(2 ** 20)
        file.close()
        return md5.hexdigest()

    def verify_file_md5(self, filename, md5sum=None, file_to_compare=None):
        """ Verify md5 sum of the given file against expected `md5sum` or the
            md5 sum calculated from another file.

        Parameters:
            - `filename`: path to the file to calculate md5 sum.
              Either absolute or relative to SARF/tests/testdata paths are
              accepted.
            - `md5sum`: expected md5 sum represented as a string of hexadecimal
              digits.
            - `file_to_compare`: etalon file to compare md5 sum. Either absolute
              or relative to SARF/tests/testdata/ paths are accepted.

              Note: If both parameters `md5sum` and `file_to_compare` are given
              then `md5sum` will be used.

        Examples:
        | ${sum} = | Get File MD5 | myfile.txt |
        | Verify File MD5 | myfile2.txt | md5sum=${sum} |
        | Verify File MD5 | myfile2.txt | file_to_compare=myfile.txt |
        """
        # get actual and expected md5 sum
        actual_md5 = self.get_file_md5(filename)
        if md5sum:
            expected_md5 = str(md5sum)
        elif file_to_compare:
            expected_md5 = self.get_file_md5(file_to_compare)
        else:
            raise RuntimeError, 'No expected value of md5 sum. ' \
                                'One of parameters md5sum or file_to_compare should be' \
                                ' specified'

        # compare to the expected md5sum if exists
        if actual_md5 == expected_md5:
            self._info('Actual md5 sum of the file equals to expected')
        else:
            raise VerificationFailed, 'Actual md5 sum: %s differs ' \
                                      'from expected: %s' % (actual_md5, expected_md5)

    def run_on_host(self,
                    host,
                    user,
                    password,
                    command,
                    verbose=None,
                    to_host=None,
                    to_user=None,
                    to_pwd=None,
                    error=False,
                    timeout=180
                    ):
        """
        Execute the specified command on a remote host
        and return the response

        Parameters:
        - `host`: name or IP address of a remote host
        - `user`: username for ssh
        - `password`: password for ssh
        - `command`: command to execute from command-line
        - `verbose`: Flag for verbose eg: ssh -v user@host
        - `to_host`: name or IP of destination host
        - `to_user`: username on destination host
        - `to_pwd`: password on destination host
        - `timeout`: maximum timeout to wait, default is 180s

        Example:
        | *** Settings *** |
        | Library | UtilsLibrary |
        | *** Test Cases *** |
        | Test1 |
        | | ${resp}= | Run On Host | ${SLICE_SERVER} | testuser | ironport |
        | | ... | tail -20 /data/pub/track_stats/prox_track.log |

        Example for verbose:
        | *** Settings *** |
        | Library | UtilsLibrary |
        | *** Test Cases *** |
        | Test1 |
        | | ${resp}= | Run On Host [ ${CLIENT_IP} | ${USERNAME} | ${PASSWORD} |
        | | ... | ssh -m ${MAC_ALG1} -v ${DUT_ADMIN}@${DUT_IP} | True | ${DUT_IP} |
        | | ... | ${DUT_ADMIN} | ${DUT_ADMIN_SSW_PASSWORD} ] |
        """
        self._info("Executing '%s' from %s" % (command, host))
        ssh = SSHLibrary.SSHLibrary()
        ssh.set_default_configuration(timeout=90, loglevel='DEBUG')
        host_ip = socket.gethostbyname(host)
        ssh.open_connection(host=host_ip, timeout=60)
        try:
            ssh.login(username=user, password=password)
            print '>>>> username: password: cmd:%s : %s :%s' % (user, password, command)
            result = ''
            if verbose:
                _expected_strings = ['Are you sure you want to continue connecting (yes/no)?',
                                     'Enter passphrase for key', '[Pp]assword:']
                ssh.write(command)
                _timer_start = time.time()
                while time.time() < _timer_start + timeout:
                    result = ssh.read(delay='45 seconds')
                    if result.find(_expected_strings[0]) > -1:
                        ssh.write('yes')
                        self._debug("Entered 'yes'")
                    if result.find(_expected_strings[1]) > -1:
                        ssh.write('')
                    if re.search(_expected_strings[2], result) is not None:
                        ssh.write(to_pwd)
                        self._debug("Entered '%s'" % (to_pwd))
                        result = ssh.read(delay='45 seconds')
                        break
                    time.sleep(1)
            else:
                result, _error = ssh.execute_command(command, 'both')
                if error:
                    result += _error
            self._info(result)
        finally:
            ssh.close_connection()
        return result

    def run_on_dut(self, command, host=None):
        """
        Execute the specified command on the appliance
        and return the response

        Parameters:
        - `command`: command to execute from command-line
        - `host`: if specified, uses that value for dut

        Example:
        | *** Settings *** |
        | Library | UtilsLibrary |
        | *** Test Cases *** |
        | Test1 |
        | | ${resp}= | Run On DUT | tail -20 /data/pub/track_stats/prox_track.log |
        """

        if host == None:
            host = self.dut
        user = self._get_parameter("${RTESTUSER}", "rtestuser")
        password = self._get_parameter("${RTESTUSER_PASSWORD}", 'ironport')
        return self.run_on_host(host, user, password, command)

    def run_on_slice_server(self, command, host=None):
        """
        Execute the specified command on slice_server
        and return the response

        Parameters:
        - `command`: command to execute from command-line
        - `host`: if specified, uses that value instead of ${SLICE_SERVER}

        Example:
        | *** Settings *** |
        | Library | UtilsLibrary |
        | *** Test Cases *** |
        | Test1 |
        | | ${resp}= | Run On Slice Server | ls -la |

        Exceptions:
        ValueError: SLICE_SERVER is not specified; it should be set either
        as a ${SLICE_SERVER} or in parameter host
        """

        if host == None:
            host = self._get_parameter("SLICE_SERVER")
            if host == None:
                raise ValueError("SLICE_SERVER is not specified")
        user = self._get_parameter("${RTESTUSER}", "rtestuser")
        password = self._get_parameter("${RTESTUSER_PASSWORD}", 'ironport')
        return self.run_on_host(host, user, password, command)

    def _get_parameter(self, parameter, default=None):
        """
        returns value of a parameter or default if parameter is not set
        """
        variables = common.Variables.get_variables()
        if parameter in variables:
            return variables[parameter]
        else:
            return default

    def dut_file_exists(self, name):
        """
        Verifies whether the specified file exists on the appliance
        and returns True or False correspondingly

        Parameters:
        - `name`: name of the file to search on the appliance

        Example:
        | *** Settings *** |
        | Library | UtilsLibrary |
        | *** Test Cases *** |
        | Test1 |
        | | Set Suite Variable | ${FILE} | /tmp/dut_file_exists |
        | | ${resp}= | Run On DUT | rm -rf ${FILE} |
        | | ${out}=  | DUT File Exists | ${FILE} |
        | | Should Not Be True | ${out} |
        | Test2 |
        | | ${resp}= | Run On DUT | touch ${FILE} |
        | | ${out}=  | DUT File Exists | ${FILE} |
        | | Should Be True | ${out} |
        """

        return bool(self.run_on_dut("[ -f %s ] && echo True" % name))

    def copy_file_from_dut_to_remote_machine(self,
                                             remote_host=None,
                                             from_loc=None,
                                             to_loc='/tmp',

                                             recursive='',

                                             #      from_parameters
                                             from_user='rtestuser',
                                             from_password='ironport',
                                             from_prompt=']',

                                             #      to_parameters
                                             to_user='rtestuser',
                                             to_password='ironport',
                                             ):
        """
        Copy file from the appliance to remote machine.

        Parameters:
        - `remote_host`: name of remote machine.
        - `from_loc`: location of file on the appliance to copy from.
        - `to_loc`: target location on remote machine to copy to.

        - `recursive`: recursive copying; accepted values '-r' or empty string
        - `from_user`: username of host with source files
        - `from_password`: password of host with source files
        - `from_prompt`: prompt of host with source files
        - `to_user`: username on destination host
        - `to_password`: password on destination host

        Example:
        - | Copy File From DUT To Remote Machine | from_loc=/data/pub/configuration/testconfig.xml | remote_host=${CLIENT_IP} | to_loc=/tmp |
        - | Copy File From DUT To Remote Machine | from_loc=/data/pub/configuration/ | remote_host=${CLIENT_IP} | to_loc=/tmp | recursive=-r |

        """
        self.scp(
            recursive=recursive,
            #      from_parameters
            from_host=self.dut,
            from_user=from_user,
            from_password=from_password,
            from_prompt=from_prompt,
            from_location=from_loc,

            #      to_parameters
            to_host=remote_host,
            to_user=to_user,
            to_password=to_password,
            to_location=to_loc,
        )

    def copy_file_to_dut(self,
                         source,
                         destination,

                         recursive='',

                         #      from_parameters
                         from_user='rtestuser',
                         from_password='ironport',
                         from_prompt='#',

                         #      to_parameters
                         to_user='rtestuser',
                         to_password='ironport',
                         ):
        """
        Copy file from the appliance to remote machine.

        Parameters:
        - `source`: location of file on client machine.
        - `destination`: directory on DUT to copy file to.

        - `recursive`: recursive copying; accepted values '-r' or empty string
        - `from_user`: username of host with source files
        - `from_password`: password of host with source files
        - `from_prompt`: prompt of host with source files
        - `to_user`: username on destination host
        - `to_password`: password on destination host

        Example:
        - | Copy File To DUT | %{SARF_HOME}/tests/testdata/config_file.xml | /data/pub/configuration/ |

        """
        self.scp(
            recursive=recursive,
            #      from_parameters
            from_host=self._get_parameter("${CLIENT_IP}"),
            from_user=from_user,
            from_password=from_password,
            from_prompt=from_prompt,
            from_location=source,

            #      to_parameters
            to_host=self.dut,
            to_user=to_user,
            to_password=to_password,
            to_location=destination,
        )

    def generator_ipv4(self, ip_addr=None, netmask=None, strict=True):
        """
        Generates IPv4 range list for the given IP address and netmask.

        *Parameters*:
        - `ip_addr`: A string or integer representing the IP.
        - `netmask`: If the mask (portion after the / in the argument) is given in
        dotted quad form, it is treated as a netmask if it starts with a
        non-zero field (e.g. /255.0.0.0 == /8) and as a hostmask if it
        starts with a zero field (e.g. 0.255.255.255 == /8), with the
        single exception of an all-zero mask which is treated as a
        netmask == /0. If no mask is given, a default of /24 is used.
        - `strict`: A boolean. If true, ensure that we have been passed
        a true network address, eg, 192.168.1.0/24 and not an
        IP address on a network, eg, 192.168.1.1/24.

        *Exceptions*:
        - `AddressValueError`: If ipaddr isn't a valid IPv4 address.
        - `NetmaskValueError`: If the netmask isn't valid for an IPv4 address.
        - `ValueError`: If strict was True and a network address was not supplied.

        *Return*:
        Generator object that generates one IP address per iteration.
        """
        if not ip_addr:
            ip_addr = socket.gethostbyname(socket.gethostname())
        netmask = netmask or 24
        return IPv4Network('%s/%s' % (ip_addr, netmask), strict=strict).iterhosts()

    def get_gen_pass(self, host, sshpasswd, esaserial):
        """
        Takes tech support generated password and serial number and
        and returns True or False correspondingly

        Parameters:
        - `host`: Host machine on which the password will be generated
        - 'sshpasswd': Password generated through techsupport command
        - 'esaserial': Serial of the DUT

        Example:
        | *** Settings *** |
        | Library | UtilsLibrary |
        | *** Test Cases *** |
        | Test1 |
        | | ${out}=  | Get Gen Pass | ${HOST} | ${SSHPASSWD} | ${ESASERIAL}
        """

        host = host.strip()
        sshpasswd = sshpasswd.strip()
        esaserial = esaserial.strip()
        url_response = urllib2.urlopen(
            'http://%s/cgi-bin/service_password.py?password=%s&serial=%s' % (host, sshpasswd, esaserial))
        time.sleep(20)
        html_resp = url_response.read()
        output = re.findall('<h3>(.*)</h3>', html_resp)
        return output[1].strip()

    def get_cli_pattern_match(self, input, pattern):
        """
        Returns the pattern match of cli status detail
        Example:
        | Get Cli Pattern Match  input  pattern |
        """
        list1 = input.split('\n')
        pattern_string = ''
        flag = 0
        for line in list1:
            if re.search(pattern, line) is not None:
                flag = 1
                print line
                pattern_string = pattern_string + line
                continue
            if flag == 1:
                if re.search('^[ ][a-zA-Z ]+', line) is not None:
                    print line
                    pattern_string = pattern_string + line
                else:
                    flag = 0
        return pattern_string

    def ssh_keyboard_auth_brute_force_vulnerability_check(self, host, user, password):
        """
        OpenSSH keyboard auth brute force vulnerability CVE-2015-5600 check
        Related to defect CSCvg96138

        Parameters:
        - `host`: name or IP address of a remote host
        - `user`: username for ssh
        - `password`: password for ssh

        Example:
        | ${output} = | Ssh Keyboard Auth Brute Force Vulnerability Check | ${host} | ${user} | ${password} |
        """

        try:
            ssh_session = pexpect.spawn('perl -e \'print "pam," x 10000\'')
            session_read = ssh_session.read()
            print session_read

            CONNECTION_STRING = 'ssh -o KbdInteractiveDevices=' + session_read + ' ' + user + '@' + host
            print "CONNECTION_STRING: ", CONNECTION_STRING

            ssh_session = pexpect.spawn(CONNECTION_STRING)
            index = ssh_session.expect(['Password:', '.*password:', '\?'], timeout=120)
            if index == 2:  # first connection to the box
                self._info('first connection to the box')
                ssh_session.sendline('yes')
                ssh_session.expect('.*password:', timeout=120)
            ssh_session.sendline(password)
            for n in range(1, 4):
                ssh_session.expect('.*password:', timeout=120)
                ssh_session.sendline(password)
            return ssh_session.read()
        except Exception as e:
            return str(e)
        finally:
            ssh_session.terminate()
