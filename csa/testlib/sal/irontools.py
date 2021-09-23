#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/sal/irontools.py#1 $

"""
Library of objects that are directly related to interfacing to Ironport
tools and products.

"""
#: Reference Symbols: irontools

from __future__ import absolute_import

import email
import ftplib
import mailbox
import os
import re
import smtplib
import socket
import telnetlib
import time

import sal.net.socket
import sal.net.sshlib
import sal.time

from sal.deprecated import expect
from sal.exceptions import TimeoutError

NULL = lambda: None


#################################################
#### TODO: Move to iaf.net.socket :TODO
#### Socket Helper Functions
#################################################
def port_in_use(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('mail.qa', 25))
    ip, unused = s.getsockname()
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((ip, port))
    except socket.error, e:
        return True
    else:
        s.close()
        return False


#################################################
#### Random Helper Functions / Classes
#################################################
def wait_for_phoebe(testobj, timeout=600):
    host = testobj
    do_reset = False

    # - If testobj is a DUT object, then extract
    # its hostname into 'host', and set the do_reset
    # flag to reset all connections to the DUT.
    #
    # - If testobj is a string, then it is already
    # the DUT's hostname
    if type(testobj) != type(''):
        host = testobj.cfg.dut.hostname
        do_reset = True

    print 'Wait for ssh to come up...'
    sal.net.socket.wait_for_port(host, 22, timeout=timeout)

    if do_reset:
        print 'Resetting the DUT...'
        testobj.cfg.dut.reset()


### TODO: Move to method of DUT object :TODO ###
def save_and_load(test_obj):
    xml_save_file = test_obj.cfg.dut.cli.saveconfig()
    print('saving configuration out to file: %s' % xml_save_file)
    print('going offline and resetting config')
    test_obj.cfg.dut.cli.offline()
    test_obj.cfg.dut.cli.resetconfig()
    print('loading configuration back in')
    test_obj.cfg.dut.cli.loadconfig(filename=xml_save_file)
    test_obj.cfg.dut.cli.commit()
    print('wait 90s for config to finish initializing')
    time.sleep(90)


def gen_addresses(N, host, basename="user"):
    """Generate a list of N unique addresses destined for 'host'. A user
prefix may be supplied. It defaults to "user".  """
    return ["%s%d@%s" % (basename, n, host) for n in xrange(1, N + 1)]


# Results analysis
def exit_status(results):
    """ exit_status(results) --> int

        Find the IAF exit status to return to the Shell that ran the test.
    """
    # find the lowest value
    min_val = min(results)

    # LOGIC
    # IAF     What it means      Return value
    # -2       FAIL and ABORT         2
    # -1       ABORT                  2
    # 0        FAILED                 1
    # 1        PASSED                 0

    if min_val < 0:
        return 2
    elif min_val == 0:
        return 1
    else:
        return 0


#################################################
#### User / R-User Methods
#################################################

def getuser():
    """Get the username from the environment or password database."""
    for name in ('USER', 'LOGNAME', 'LNAME', 'USERNAME'):
        user = os.environ.get(name, None)
        if user:
            return user
    import pwd
    return pwd.getpwuid(os.getuid())[0]


def get_ruser():
    """return the root-user name per the Ironport convention."""
    return "rtestuser"


def get_ruser_prompt():
    """return the prompt for the root-user name"""
    return "#"


def get_sh_root_prompt():
    """return the prompt for the sh root"""
    return "RootPrompt> "


def get_root_prompt():
    """return the prompt template (no hostname) for root"""
    return "%s#"


def get_ruser_password():
    """return the password for the root-user name.
        Return None if ssh login is unchallenged
    """
    return None


def get_ruser_ssh(host, logfile=None):
    """ get_ruser_ssh(host) --> ssh session

        Return an ssh session to the current user's r-account.
    """
    user = get_ruser()
    password = get_ruser_password()
    prompt = get_ruser_prompt()
    sess = sal.net.sshlib.get_ssh_unsafe(host, user, password,
                                         prompt=prompt, logfile=logfile)
    return sess


def remote_command(host, command, user=None, password=None, prompt=None,
                   logfile=None, wait=True):
    """run_command(host, command, [password], [logfileobject])
Invoke the commandobject on the specified host, using a remote shell via SSH."""
    command = str(command)  # in case it is a Program object.
    prompt = prompt
    if user == None:
        user = getuser()
    if wait:  # return a string
        return sal.net.sshlib.ssh_command(host, user, password, prompt=prompt,
                                          command=command, logfile=logfile)
    else:  # return SshExpect object
        return sal.net.sshlib.get_ssh(host, user, password, prompt=prompt,
                                      cmd=command, logfile=logfile)


def remote_command_ruser(host, command, logfile=None, wait=True):
    """run_command(host, command, [password], [logfileobject])
    Invoke the commandobject on the specified host, using a remote shell
    via SSH.  through the backdoor with ruser"""
    dev_auto = os.getenv('DEV_FOR_AUTOMATION')
    if dev_auto:
        user = "ftpuser"
        password = "ironport"
        prompt = "$"
    else:
        user = get_ruser()
        password = None
        prompt = get_ruser_prompt()
    if wait:  # return a string
        return sal.net.sshlib.ssh_command(host, user, password, prompt=prompt,
                                          command=command, logfile=logfile)
    else:  # return SshExpect object
        return sal.net.sshlib.get_ssh(host, user, password, prompt=prompt,
                                      cmd=command, logfile=logfile)


def scp_ruser(host, src, dst, dstremote=True, logfile=None):
    """Invoke the commandobject on the specified host, using a remote shell
    via SSH.  through the backdoor with ruser"""
    user = password = None
    dev_auto = os.getenv('DEV_FOR_AUTOMATION')
    if dev_auto:
        user = "ftpuser"
        password = "ironport"
    else:
        user = get_ruser()
        password = get_ruser_password()

    if dstremote:
        dst = '%s@%s:%s' % (user, host, dst)
    else:
        src = '%s@%s:%s' % (user, host, src)

    return sal.net.sshlib.scp(src, dst, password=password, logfile=logfile)


def start_command(host, command, user=None, password=None, logfile=None):
    """ Start a command on a remote host using SSH. Return the
    SSH process object.  """
    ssh = sal.net.sshlib.get_ssh(host, user, password, prompt=None,
                                 cmd=command, logfile=logfile)
    return ssh


def ssh_drainhost(config, user=None, password=None):
    """ssh_drainhost(config, user=None, password=None)
Return an SSH session connected to your configured drain host."""
    host = config.drainhost
    ssh = sal.net.sshlib.get_ssh(host, user=user, password=password,
                                 prompt=host.prompt, logfile=config.logfile)
    return ssh


def ssh_injectorhost(config, user=None, password=None):
    """ssh_injectorhost(config, user=None, password=None)
Return an SSH session connected to your configured injector host."""
    host = config.injectorhost
    ssh = sal.net.sshlib.get_ssh_unsafe(host, user=user, password=password,
                                        prompt=host.prompt, logfile=config.logfile)
    return ssh


#################################################
#### TODO: Move to product code :TODO
#### C60 Error Checking Functions
#################################################

def dev_check_errors(host, logfile=None):
    """ dev_check_errors(host, logfile) --> string

        If any errors are lurking in the log files on a C60, this method
        will weed them out. This method should be run after *every* IAF
        test to make sure there were no application faults, etc.
    """

    # common base directory
    LOG_DIR = "/var/log/godspeed"

    # do not grep libexec and bin directories since some of the code has
    # OSError, application.fault, IOError and message in the code.

    cmd = "grep -r -s application.fault %s/* | grep -v /libexec | grep -v /bin" % LOG_DIR
    grep_results = remote_command_ruser(host, cmd, logfile).strip()

    cmd = "grep -r -s exceptions.IOError %s/* | grep -v /libexec | grep -v /bin" % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    cmd = "grep -r -s Queue\: %s/mail_logs/*" % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    # TODO: A check is needed to if the latency is longer than 1.0s
    #       Only then is the latency an error. These two lines will
    #       yield false positives if uncommented without this check.
    # cmd = "grep -r -s work_queue_thread /var/log/godspeed/*"
    # grep_results += remote_command_ruser(host, cmd, logfile).strip()

    cmd = "grep -r -s queue.is.corrupt %s/*" % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()
    cmd = "grep -r -s OSError %s/* | grep -v stdout_thirdparty | \
            grep -v stdout_hermes | grep -v /libexec | grep -v /bin | \
            grep -v euqgui_fastrpc" % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    cmd = "find %s/ -name '\*core' | grep -v unicore | \
            grep -v third_party/splunk/* " % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    cmd = "grep -r -s Critical\: %s/* | grep -v system_logs" % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    # Check if error logs are greater than zero which means th
    # removed this test since negative testing (bad args) produce errors
    # in these logs.
    # cmd =  "find %s/error_logs/* -size +1c -print" % LOG_DIR
    # grep_results += remote_command_ruser(host, cmd, logfile).strip()
    return grep_results


def check_errors(host, logfile=None):
    """ See: dev_check_errors """
    # XXX - if it's development then route this to the dev_check_errors
    # since development log directories will not have the same list of
    # files, we will just use generic '*'
    # As always, this should be triggered only if an dev-env-var is set
    if os.getenv('DEV_FOR_AUTOMATION'):
        return dev_check_errors(host, logfile)
    grep_results = ""

    # common base directory
    LOG_DIR = "/var/log/godspeed"

    cmd = "find %s/ -name '\*core' | grep -v unicore | \
            grep -v third_party/splunk/* " % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    cmd = "grep -I -r -s application.fault %s/* | grep -v /libexec | \
           grep -v /bin | grep -Ev \"Info:.MID.[0-9]+.Subject\"" % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    cmd = "grep -I -r -s exceptions.IOError %s/*  | grep -v /libexec | \
           grep -v /bin | grep -Ev \"Info:.MID.[0-9]+.Subject\"" % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    # cmd = "grep -I -r -s Queue\: %s/mail_logs/*" % LOG_DIR
    # grep_results += remote_command_ruser(host, cmd, logfile).strip()

    # TODO: A check is needed to if the latency is longer than 1.0s
    #       Only then is the latency an error. These two lines will
    #       yield false positives if uncommented without this check.
    # cmd = "grep -r -s work_queue_thread /var/log/godspeed/*"
    # grep_results += remote_command_ruser(host, cmd, logfile).strip()
    cmd = "grep -I -r -s queue.is.corrupt %s/* | \
           grep -Ev \"Info:.MID.[0-9]+.Subject\"" % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    cmd = 'grep -I -r -s OSError %s/* | grep -v stdout_thirdparty | \
           grep -v stdout_hermes  | grep -v /libexec | grep -v /bin | \
           grep -v stdout_euq_server  | grep -v stdout_euq_webui | \
           grep -v Info | grep -v Debug | grep -v "RPC:.OSError" | \
           grep -v third_party/splunk/ | grep -v euqgui_fastrpc | \
           grep -v external_auth/ | \
           grep -v hermes_euq ' % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    cmd = 'grep -I -r -s Critical\: %s/* | grep -v system_logs | \
          grep -v "Push.error" | grep -v "Harvest.Attack" | \
          grep -Ev "Info:.MID.[0-9]+.Subject" | \
          grep -v "page.not.found"' % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    # Any file with the string "exception" is an error.
    # Ignore the following:
    # cli_logs directory.  config.dtd file. Binary files.
    # Files in third_party/case/libexec and third_party/case/tmp directory.
    # Files in third_party/mcafee/bin directory.
    #
    # TODO: Following 2 commands should be joined into one,
    # but "\|" seems not work
    cmd = 'grep -I -r -s -i "exception" %s/* | grep -v cli_logs | ' \
          'grep -v config.dtd | grep -v ^Binary | ' \
          'grep -v "third_party/" | ' \
          'grep -v "httpd/" | ' \
          'grep -v stdout_upgrade.log | grep -v "configuration/" | ' \
          'grep -vi smart.exceptions | ' \
          'grep -Ev "Info:.MID.[0-9]+.Subject"' % LOG_DIR

    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    cmd = 'grep -I -r -s -i "Traceback" %s/* | grep -v cli_logs | ' \
          'grep -v config.dtd | grep -v ^Binary | ' \
          'grep -v "third_party/" | ' \
          'grep -v "httpd/" | ' \
          'grep -v stdout_upgrade.log | grep -v "configuration/" | ' \
          'grep -vi smart.exceptions | ' \
          'grep -Ev "Info:.MID.[0-9]+.Subject"' % LOG_DIR

    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    # "spamd: already running on" in stdout_case.log
    # signals serious issues with CASE startup/shutdown/restart
    cmd = 'grep -s spamd\:.already.running.on %s/stdout_case.log' % LOG_DIR
    grep_results += remote_command_ruser(host, cmd, logfile).strip()

    # remove all 'Bogus work queue app fault' errors from the list, we make
    # those ourselves.  Make a copy of grep_results first.
    results = grep_results.splitlines()
    for result_str in grep_results.splitlines():
        # delete our target app faults from the copy, not the original
        # so as not to screw up the loop counter
        if result_str.find('Bogus work queue app fault') > -1:
            results.remove(result_str)
        # except postx traceback
        elif result_str.find('BATSAFE:') > -1:
            results.remove(result_str)
        # except info entries
        elif result_str.find("Info: ") > -1:
            results.remove(result_str)
        # except PthreadException
        elif result_str.find("PthreadException") > -1:
            results.remove(result_str)

    return '\r\n\r\n'.join(results)


def quick_qmqp(host, argv, user=None, password=None, logfile=None):
    if type(argv) is list:
        argv = " ".join(argv)
    cmd = "/usr/godspeed/bin/quick_qmqp %s" % (argv)
    return remote_command(host, cmd, user, password, logfile)


def quick_send(host, argv, user=None, password=None, logfile=None):
    if type(argv) is list:
        argv = " ".join(argv)
    cmd = "/usr/godspeed/bin/quick_send %s" % (argv)
    return remote_command(host, cmd, user, password, logfile)


#################################################
#### TODO: Move to sal.mail.utils :TODO
#### Injector / Drain Backdoor Information Retrieval Methods
#################################################

def reset_drain_counters(host):
    """ Connect to the drain specified in 'host', and send in the
        msgs_reset command, effectively clearing all drain counters.  """

    server = smtplib.SMTP(host)
    server.docmd('msgs_reset')
    server.quit()


class ToolBackdoor(expect.Expect):
    """An interface to the Python interpreter backdoor present on many Ironport
    tools."""

    def msgs_accepted(self):
        """ Return the number of messages the null_smtpd has accepted. """
        self.write('msgs_accepted\r\n')
        return int(self.read_until().strip())

    def tls_msgs_accepted(self):
        """ Return the number of TLS messages the null_smtpd has accepted. """
        self.write('tls_msgs_accepted\r\n')
        return int(self.read_until().strip())

    def msgs_sent(self):
        """ Return the number of messages that smtp_spam has sent. """
        self.write('msgs_sent\r\n')
        return int(self.read_until().strip())

    def rcpts_accepted(self):
        """ Return the number of recipients that null_smtpd has accepted. """
        self.write('rcpts_accepted\r\n')
        return int(self.read_until().strip())

    def interact(self, msg=None, prompt="backdoor> "):
        """ A way to interact with the backdoor of the given IronPort utility.
        I think it's much better to just telnet to the port...  """
        print msg or "entering interactive mode. type '^D' to quit."
        try:
            while 1:
                l = raw_input(prompt)
                l = l.strip()
                if l:
                    self.write("%s\r\n" % (l,))
                    print self.read_until()
        except EOFError:
            pass


def get_toolbackdoor(host, port=8023, logfile=None):
    """ Always use this factory function to get a tool backdoor object. """
    conn = None
    # Try 10 times from port 8023 to port 8032 to get a connection
    for i in range(10):
        try:
            conn = sal.net.socket.connect_tcp(host, port + i)
        except socket.error:
            continue
        else:
            port = port + i
            break

    if conn == None:
        raise AssertionError, "Could not connect to the Hammer Tools backdoor."

    if logfile:
        print >> logfile, "Connection to the null_smtpd backdoor on host: " + \
                          "%s port: %d" % (host, port)
    bd = ToolBackdoor(conn.makefile("w+", 1), ">>> ", logfile=logfile)
    bd.wait_for_prompt()
    return bd


#################################################
#### TODO: Move to sal.mail.utils :TODO
#### Injection / Delivery Counting Helper methods
#################################################
def check_drain(hostname, num_msgs, info_meth, bd_port=8023, stag_callback=None):
    n = 0
    sleep_time = num_msgs / 10000 or 1
    if sleep_time == 0:
        info_meth('For some reason, sleep_time managed to be 0, so let\'s make it 1!')
        sleep_time = 1
    history = [-1] * 15
    info_meth('Sleep time is: %d' % sleep_time)
    for i in range(1000):
        time.sleep(sleep_time)
        try:
            n = get_num_msgs(hostname, port=bd_port)
        except IOError:
            info_meth("A interrupted system call occured, but we don't care")
            continue
        info_meth('checking drain... %d out of %d delivered' % (n, num_msgs))
        if n < num_msgs:
            prepend_chop(history, n)
            # This gives a hook for a function call if the drain is not processing messages.
            if history[:5] == 5 * [history[0]] and stag_callback:
                stag_callback()
            if history == 15 * [history[0]]:
                raise AssertionError, 'Drain did not receive the correct amount of messages'
            continue
        elif n > num_msgs:
            raise AssertionError, 'Drain received TOO MANY messages'
        # else
        return True
    raise AssertionError, 'Drain did not receive the correct amount of messages'


### TODO: Move to product code for ESA :TODO ###
def wait_for_injection(ctor, inj_proc, info_meth, num_msgs, allow_lower=False):
    err_str = ""

    num_attempts, sleep_time = 25, 15
    if num_msgs > 100000:
        num_attempts, sleep_time = 35, 20
    if allow_lower:
        num_attempts, sleep_time = 35, 5

    # If we allow for a smaller amount to be accepted, it must stay at the
    # frozen level for 18*5 == 1.5 minutes.
    history = [-1] * 18
    for i in range(num_attempts):
        st = ctor.status()
        n = st['counters']['injection']['injected_recipients'][0]
        if n < num_msgs:
            prepend_chop(history, n)

            if n == 0 and history[:7] == 7 * [n]:
                info_meth("0 messages were injected when %d were expected" % num_msgs)
                break

            info_meth('checking DUT...%d out of %d injected' % (n, num_msgs))
            time.sleep(sleep_time)
            try:
                inj_proc.read(80, timeout=5)
            except TimeoutError:
                pass

            if allow_lower and history == 18 * [history[0]]:
                info_meth('DUT only processed %d / %d messages, but we expected that' % (n, num_msgs))
                return n
            continue

        elif n > num_msgs:
            info_meth('DUT processed more messages than expected...%d / %d injected' % (n, num_msgs))
            break

        info_meth('DUT processed exactly the number of messages expected...%d / %d injected' % (n, num_msgs))
        return num_msgs

    raise AssertionError, "Injection to the DUT failed!"


#################################################
#### Net Install Methods
#################################################

def get_build_list(cfgobj):
    """Gets the list of build IDs from the DUT in the config."""
    raise NotImplementedError
    return cfgobj.DUT.get_build_list(cfgobj.software_version)


#################################################
#### TODO: Move to sal.clients.ftp? :TODO
#### FTP utilities ###
#################################################

def ftp_download(fname=None,
                 remotedir=".",
                 ftpserver=None,
                 ftpusername=None,
                 ftppass=None,
                 dutusername=None,
                 dutpass=None,
                 proxy=None,
                 passive_mode=1,
                 port=8021):
    """Method gets a file from the FTP server to the client via proxy,
       returns a big string
    :Parameters:
      - `fname` : File to get from the FTP server
      - `remotedir` : remote directory from where to get the file
      - `ftpserver` : FTP server name
      - `ftpusername` : Username for FTP server
      - `ftppass` : Password for the provided username
      - `dutusername` : Username for dut
      - `dutpass` : Password for dut
      - `passive_mode` : To send request in Passive mode or active mode,
                         Default to passive mode request
      - `port` : Port on which proxy will listen, default to 8021
    """

    if not fname:
        raise ValueError, "Provide a file to download"
    if not ftpserver:
        raise ValueError, "Provide FTP server name"
    if not proxy:
        raise ValueError, "Provide a proxy"

    rname = "%s/%s" % (remotedir, os.path.basename(fname))
    ftp = None
    blocks = []
    _cb = lambda d: blocks.append(d)
    try:
        ftp = ftplib.FTP()
        ftp.set_pasv(passive_mode)
        ftp.connect("%s" % (proxy,), port)
        ftp.sendcmd('USER %s@%s@%s' % (ftpusername, dutusername, ftpserver,))
        ftp.sendcmd('PASS %s@%s' % (ftppass, dutpass,))
        ftp.retrbinary('RETR %s' % (rname,), _cb)
        return "".join(blocks)
    finally:
        if ftp:
            ftp.close()


def ftp_upload(fname=None,
               remotedir=".",
               ftpserver=None,
               ftpusername=None,
               ftppass=None,
               dutusername=None,
               dutpass=None,
               proxy=None,
               passive_mode=1,
               port=8021):
    """Method uploads a file to the FTP server via proxy
    :Parameters:
      - `fname` : File to upload
      - `remotedir` : remote directory to upload the file
      - `ftpserver` : FTP server name
      - `ftpusername` : Username for FTP server
      - `ftppass` : Password for the provided username
      - `dutusername` : Username for dut
      - `dutpass` : Password for dut
      - `passive_mode` : To send request in Passive mode or active mode,
                         Default to passive mode request
      - `port` : Port on which proxy will listen, default to 8021
    """

    if not fname:
        raise ValueError, "Provide a file to upload"
    if not ftpserver:
        raise ValueError, "Provide FTP server name"
    if not proxy:
        raise ValueError, "Provide a proxy"

    rname = "%s/%s" % (remotedir, os.path.basename(fname))
    fo = ftp = None
    try:
        fo = file(fname)
        ftp = ftplib.FTP()
        ftp.set_pasv(passive_mode)
        ftp.connect("%s" % (proxy,), port)
        ftp.sendcmd('USER %s@%s@%s' % (ftpusername, dutusername, ftpserver,))
        ftp.sendcmd('PASS %s@%s' % (ftppass, dutpass,))
        ftp.storbinary('STOR %s' % (rname,), fo)
    finally:
        if fo:
            fo.close()
        if ftp:
            ftp.close()


def ftp2dut(DUT, fname, remotedir=".", logfile=None, username=None, passwd=None):
    """ftp2dut(DUT, filename, [remotedir])
Use FTP to copy a local file to a DUT's admin port. Make sure FTP is
enabled on that port.  The DUT parameter is a DUT object, not a string."""

    rname = "%s/%s" % (remotedir, os.path.basename(fname))
    if username == None:
        username = DUT.mga_cfg.cli.user
    if passwd == None:
        passwd = DUT.mga_cfg.cli.password
    acct = "%s@%s" % (username, DUT.hostname)
    fo = ftp = None
    try:
        fo = file(fname)
        ftp = ftplib.FTP(DUT.hostname, username, passwd, acct)
        ftp.set_pasv(1)
        ftp.storbinary("STOR %s" % (rname,), fo)  # the ftp module has the lamest interface
    finally:
        if fo:
            fo.close()
        if ftp:
            ftp.quit()


def ftp_get(DUT, fname, remotedir=".", username=None, password=None):
    """Fetch a file from the DUT via FTP. Return it as a big string."""
    if not username:
        username = DUT.mga_cfg.cli.user
    if not password:
        password = DUT.mga_cfg.cli.password

    rname = "%s/%s" % (remotedir, os.path.basename(fname))
    ftp = None
    blocks = []
    _cb = lambda d: blocks.append(d)
    try:
        ftp = ftplib.FTP(DUT.hostname, username, password)
        ftp.set_pasv(1)
        ftp.retrbinary('RETR %s' % (rname,), _cb)
        return "".join(blocks)
    finally:
        if ftp:
            ftp.quit()


def ftp_dir(DUT, remotedir=".", username=None, password=None):
    """Run 'LIST' on a directory in the DUT via FTP. Return it is a list."""

    if not username:
        username = DUT.mga_cfg.cli.user
    if not password:
        password = DUT.mga_cfg.cli.password
    ftp = None
    ans = []
    _cb = lambda d: ans.append(d)
    try:
        ftp = ftplib.FTP(DUT.hostname, username, password)
        ftp.set_pasv(1)
        ftp.cwd(remotedir)
        ftp.retrlines('LIST', _cb)
        return ans
    finally:
        if ftp:
            ftp.quit()


def check_cli_cmd(sess, cmd_list):
    """Check each step of a CLI command is executed properly.
    We repeat the following:
        1. Wait for prompt (cmd_list[0]).
        2. Send command (or sub-command) via CLI session (cmd_list[1]).
        3. Check result of command (cmd_list[2]).
    """

    last_expected_text = None
    for start_of_cmd, cmd, expected_text in cmd_list:
        # print '[%s][%s][%s]'%(start_of_cmd, cmd, expected_text)
        if start_of_cmd != None:
            output = sess.read_until(start_of_cmd)
            if last_expected_text != None:
                assert re.search(last_expected_text, output)
        if cmd != None:
            sess.writeln(cmd)
            last_expected_text = expected_text


def get_mbox(mbox_filename):
    def msg_factory(fp):
        try:
            return email.message_from_file(fp)
        except email.Errors.MessageParseError:
            return ''

    mbox = mailbox.UnixMailbox(open(mbox_filename), msg_factory)
    return mbox


### TODO: Move to sal.net.ping :TODO ###
def is_port_open(host, port, timeout=5, verbose=False):
    """Return True if connect(host, port) is successfull."""
    tmr = sal.time.CountDownTimer(timeout or 1).start()
    while tmr.is_active():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rv = s.connect((host, port))
        except Exception, e:
            if verbose:
                print 'is_port_open():', e
            del s
        else:
            return True
        time.sleep(1)
    else:
        # timeout. Port is closed
        return False


### TODO: Move to sal.net.ping :TODO ###
def is_port_closed(host, port, timeout=2, verbose=False):
    """Return True if connect(host, port) is successfull."""
    tmr = sal.time.CountDownTimer(timeout or 1).start()
    while tmr.is_active():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rv = s.connect((host, port))
        except Exception, e:
            # port is closed
            return True
        time.sleep(1)
    else:
        # timeout. Port is open
        return False


### TODO: Move to sal.net.telnet? :TODO ###
class TelnetPlus(telnetlib.Telnet):
    """TelnetPlus is identical to telnetlib except it provides a
        bind_ip argument in the constructor and open() call that is
        not available in telnetlib.
    """

    def __init__(self, host=None, port=0, bind_ip=None):
        """Constructor.

        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance; a port
        number is optional.

        """
        telnetlib.Telnet.__init__(self)
        self.debuglevel = telnetlib.DEBUGLEVEL
        self.host = host
        self.port = port
        self.sock = None
        self.rawq = ''
        self.irawq = 0
        self.cookedq = ''
        self.eof = 0
        self.option_callback = None
        if host:
            self.open(host, port, bind_ip)

    def open(self, host, port=0, bind_ip=None):
        """Connect to a host.

        The optional second argument is the port number, which
        defaults to the standard telnet port (23).

        Don't try to reopen an already connected instance.

        """
        self.eof = 0
        if not port:
            port = telnetlib.TELNET_PORT
        self.host = host
        self.port = port
        msg = "getaddrinfo returns an empty list"
        for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                if bind_ip:
                    self.sock.bind((bind_ip, 0))
                self.sock.connect(sa)
            except socket.error, msg:
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error, msg
