# Light smtp client to send emails
# * send unencrypted mails
# * send smtp with ssl
# * smtp with tls
# Developed By Beno K Immanuel

import argparse
import mailbox
import mimetypes
import os
import re
import smtpclientlib
import socket
import threading
import time
import telnetlib
import math
import itertools
import Queue
import random
import string

from email.utils import formatdate, make_msgid
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import stderr, getsizeof
from sal.net.iputils import IPs

__version_info__ = ('1','0','013')
__version__ = '.'.join(__version_info__)
__author__ = 'Beno K Immanuel'

class FatalOption:
    pass


class FatalError(Exception):
    def __init__(self, msg):
        stderr.write(msg)


class SSLCLient(smtpclientlib.SMTP_SSL):
    def __init__(self, server, port, certfile=None, keyfile=None):
        self.serverchannel = True
        self.server = server
        self.port = port
        self.keyfile = certfile
        self.certfile = keyfile
        try:
            smtpclientlib.SMTP_SSL.__init__(self, self.server, self.port, \
                                            keyfile=self.keyfile, certfile=self.certfile)
        except (socket.error, smtpclientlib.SMTPException) as error:
            # print "Failed to connect to SMTP SERVER SSL :%s :%s \r :%s \r" % (self.server, \
            # self.port, error)
            stderr.write('*')
            self.serverchannel = False
        self.set_debuglevel(True)


class SmtpClient(smtpclientlib.SMTP):

    def __init__(self, server, port, bind_ip=None, debug=False, timeout=None):
        self.serverchannel = True
        self.server = server
        self.port = port
        self.bind_ip = bind_ip
        self.debug = debug
        self.sock = None
        try:
            smtpclientlib.SMTP.__init__(self, self.server, \
                                        self.port, source_address=self.bind_ip, timeout=timeout)
            self.set_debuglevel(debug)
        except (socket.error, smtpclientlib.SMTPException) as error:
            self.serverchannel = False
            if self.debug:
                print "Connect SMTP SERVER:BASIC:%s :%s :%s" % (self.server, self.port, error)
                raise FatalError("Failed to connect to SMTP SERVER:%s :%s :%s, bind ip: %s " % (self.server, \
                                                                                                self.port, error,
                                                                                                self.bind_ip))
            stderr.write('*')
            self.close()

    def connect(self, host='localhost', port=0, source_address=None, timeout=10):
        """Connect to a host on a given port.
        If the hostname ends with a colon (`:') followed by a number, and
        there is no port specified, that suffix will be stripped off and the
        number interpreted as the port number to use.
        Note: This method is automatically invoked by __init__, if a host is
        specified during instantiation.
        """
        self.timeout = timeout
        code = 421
        msg = 'The mail service is unavailable Try again later'
        if not port and (host.find(':') == host.rfind(':')):
            i = host.rfind(':')
            if i >= 0:
                host, port = host[:i], host[i + 1:]
                try:
                    port = int(port)
                except ValueError:
                    raise socket.error, "nonnumeric port"
        if not port:
            port = self.default_port
        # if self.debuglevel > 0:
        #    print>>stderr, 'Socket connect:', (host, port)
        try:
            if source_address:
                self.sock = self._get_socket(host, port, self.timeout, \
                                             source_address=source_address)
            else:
                self.sock = self._get_socket(host, port, self.timeout)
            (code, msg) = self.getreply()
            if self.debuglevel > 0:
                print>> stderr, "connect:", msg
        except socket.error as error:
            if self.debuglevel > 0:
                print "ERROR:", error
            stderr.write('*')
            print "ERROR:", error, code, msg
        return (code, msg)

    def _get_socket(self, host, port, timeout, source_address=None):
        # This makes it simpler for SMTP_SSL to use the SMTP connect code
        # and just alter the socket connection bit.
        if self.debuglevel > 0:
            print>> stderr, '_get_socket connect:SmtpClient', (host, port, source_address)
        if source_address:
            conn_socket = socket.create_connection((host, port), timeout, \
                                                   source_address=source_address)
        else:
            conn_socket = socket.create_connection((host, port), timeout)
        return conn_socket


class TlsSmtpClient(SmtpClient):

    def __init__(self, server, port, bind_ip=None, debug=False, certfile=None, keyfile=None, timeout=None):
        self.serverchannel = True
        self.server = server
        self.port = port
        self.bind_ip = bind_ip
        self.debug = debug
        self.keyfile = keyfile
        self.certfile = certfile
        self.sock = None
        try:
            SmtpClient.__init__(self, self.server, \
                                self.port, bind_ip=self.bind_ip, timeout=timeout, debug=debug)
            self.set_debuglevel(debug)
            self.enable_tls()
        except (socket.error, smtpclientlib.SMTPException) as error:
            if self.debug:
                raise FatalError("Failed to connect to SMTP SERVER:TLS :%s :%s :%s" % (self.server, \
                                                                                       self.port, error))
            # print "Connect SMTP SERVER:TLS :%s :%s :%s" % (self.server,self.port, error)
            stderr.write('*')
            self.serverchannel = False

    def enable_tls(self):
        if self.serverchannel:
            self.ehlo()
            self.starttls(keyfile=self.keyfile, certfile=self.certfile)


class LightSmtpClient(SmtpClient, SSLCLient, TlsSmtpClient):

    def __init__(self, server, port, servertype=None, bind_ip=None, debug=False, certfile=None, keyfile=None,
                 timeout=10):
        self.serverchannel = True
        self.server = server
        self.port = port
        self.bind_ip = bind_ip
        self.servertype = servertype
        self.debug = debug
        self.client = None
        self.sock = None
        self.bind_ip_port = None
        if self.bind_ip:
            self.bind_ip_port = (self.bind_ip, 0)
        if servertype == 'basic':
            self.client = SmtpClient(self.server, self.port, bind_ip=self.bind_ip_port, debug=debug, timeout=timeout)
        if servertype == 'ssl':
            self.client = SSLCLient(self.server, self.port, bind_ip=self.bind_ip_port, debug=debug, timeout=timeout)
            self.local_hostname = self.client.local_hostname
        if servertype == 'tls':
            self.client = TlsSmtpClient(self.server, self.port, bind_ip=self.bind_ip_port, \
                                        debug=debug, certfile=certfile, keyfile=keyfile, timeout=timeout)
        self.serverchannel = self.client.serverchannel

    def user_login(self, username, password, authmethod=None):
        auth_state = None
        if self.serverchannel:
            try:
                self.client.login(username, password, authmethod=authmethod)
                auth_state = 'success'
            except (smtpclientlib.SMTPException, smtpclientlib.SMTPAuthenticationError) as error:
                if self.debug:
                    print "ERROR::ERROR LOGIN:%s" % error
        return auth_state

    def send_mail(self, sender, to, msg, printchar, count=1, dot=1):
        if self.serverchannel:
            for i in range(0, count):
                try:
                    self.client.sendmail(sender, to, msg)
                    stderr.write(printchar * dot)
                except (smtpclientlib.SMTPServerDisconnected, \
                        smtpclientlib.SMTPRecipientsRefused, \
                        smtpclientlib.SMTPSenderRefused, \
                        smtpclientlib.SMTPDataError, \
                        smtpclientlib.SMTPHeloError) as error:
                    stderr.write('x' * dot)
                    print "error", error
                    if self.debug:
                        print "\nERROR::ERROR to send mail:%s" % error

    def disconnect(self):
        try:
            if self.serverchannel:
                self.client.quit()
        except smtpclientlib.SMTPServerDisconnected as error:
            print "ERROR in disconnect:%s" % error


class LightWeightSpam():

    def __init__(self):
        self.bind_ip = None
        self.bind_ips = None
        self.tls_cert_file = None
        self.tls_key_file = None
        self.login_enable = None
        self.username = None
        self.password = None
        self.auth_method = None
        self.inject_host = None
        self.inject_port = None
        self.debug = False
        self.addr_per_msg = 1
        self.dotcount = 1
        self.duration = None
        self.socket_timeout = 30
        self.message_count = 1
        self.max_msg_per_connection = 1
        self.repeat_count = 1
        self.total_connection_count = 0
        self.total_message_count = 0
        self.address_list = []
        self.address_list_file = None
        self.address_list_input = None
        self.rcpt_append_str = None
        self.mail_from_list = []
        self.recp_host_list = []
        self.message_list = []
        self.mbox_header_dict = {}
        self.servertype = 'basic'
        self.msg_body = True
        self.attachment_file = False
        self.msg_file = False
        self.mbox_file = False
        self.repeat_address_list = False
        self.delay = 0
        self.tls_max_connection = 0.0
        self.cache_mbox = 1
        self.mbox_message = []
        self.tls_msg_count = 0
        self.message_count = 1
        self.msg_size = 512
        self.msg_subject = 'Test Mail lightsmtp client'

    def get_eml_data(self, filename=None):
        fileexists = os.path.isfile(filename)
        if fileexists:
            with open(filename) as emlfile:
                emlmsg = emlfile.readlines()
                return "".join(emlmsg)
        else:
            print "File not found", filename

    def get_mbox_messages(self, filename=None):
        mbox_messages = []
        fileexists = os.path.isfile(filename)
        if fileexists:
            for msg in mailbox.mbox(filename):
                if self.mbox_header_dict:
                    msg = self.change_headers(msg)
                mbox_messages.append(msg.as_string())
                return mbox_messages
        else:
            print "File not found", filename

    def process_mbox_header(self, modify_header):
        for eachHeader in modify_header:
            try:
                header, header_value_file = eachHeader.split(':')
            except ValueError:
                print >> sys.stderr, "mbox-header argument must be a header:filename pair"
                raise FatalOption
            self.mbox_header_dict[header] = header_value_file

    def change_headers(self, msg):
        if self.mbox_header_dict:
            for header in self.mbox_header_dict.keys():
                if header in msg.keys():
                    msg.replace_header(header, self.mbox_header_dict[header])
        return msg

    def _get_message_for_msg_size(self, msg_size):
        current_size = 0
        message = ''
        while (current_size < msg_size):
            seed = random.randint(0, 25)
            if msg_size - current_size < 26:
                message += string.ascii_uppercase[seed]
            else:
                message += string.ascii_uppercase[seed::]
            current_size = getsizeof(message)
        return message

    def _get_plain_message(self, args):

        self.msg_type = 'plain'
        message = ''
        if args.msg_body:
            msg_body = args.msg_body
        msg_body = self._get_message_for_msg_size(self.msg_size)
        message += '\r\n%s\r\n' % (msg_body)
        return message

    def get_message(self, args):
        messagelist = []

        if args.mbox_file and self.cache_mbox:
            self.check_option(args.mbox_file, "Mbox file: %s does not exist." % args.mbox_file)
            messagelist = self.get_mbox_messages(args.mbox_file)
            self.mbox_file = True
            return messagelist

        if not self.cache_mbox:
            self.mbox = mailbox.mbox(args.mbox_file)
            self.mbox_len = len(self.mbox)
            self.mbox_message = itertools.cycle(self.mbox)

        if args.msg_body or self.msg_body:
            message = MIMEText(args.msg_body, 'plain')
            # self.msg_body = True
        if args.attachment_file or args.msg_file or args.mbox_file:
            message = MIMEMultipart('alternative')
        if args.msg_subject:
            message['Subject'] = args.msg_subject
        else:
            message['Subject'] = 'Test Mail lightsmtp client'
        message["Date"] = formatdate(localtime=True)
        if args.custom_header:
            for header_value_pair in args.custom_header.split(','):
                header, value = header_value_pair.split(':', 1)
                message[header] = value

        if not args.attachment_file and not args.msg_file and not args.mbox_file and not args.msg_body:
            message = self.build_mime_msg(subject=message['Subject'], attach_file_list=args.attachment_file,
                                          msg_body=self._get_plain_message(args)).as_string()

        elif args.attachment_file:
            message = self.build_mime_msg(subject=message['Subject'], attach_file_list=args.attachment_file,
                                          msg_body=args.msg_body).as_string()
            self.attachment_file = True
        else:
            message = message.as_string()

        if args.msg_file:
            for emlfile in args.msg_file.split(','):
                self.check_option(emlfile, "eml file: %s does not exist." % emlfile)
                message += self.get_eml_data(filename=args.msg_file)
            self.msg_file = True
        messagelist.append(message)
        return messagelist

    def build_mime_msg(self, mail_from=None, mail_to=None, subject=None, attach_file_list=None, msg_body=None):
        """Build a MIME message
        :Parameters:
            - `msg_body`: Message body to use.
        build_mime_msg
        :Returns:
            - A MIME message as a string
        """
        mime_message = MIMEMultipart()
        # mime_message['From'] = mail_from
        # mime_message['To'] = mail_to
        mime_message['Message-Id'] = make_msgid()
        mime_message['Subject'] = subject

        mime_message.attach(MIMEText(msg_body or 'Test message.'))
        if attach_file_list:
            for filename in attach_file_list.split(','):
                ctype, encoding = mimetypes.guess_type(filename)
                if ctype is None or encoding is not None:
                    # No guess could be made, or the file is encoded (compressed), so
                    # use a generic bag-of-bits type.
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)

                # Mapping of filetype -> MIME function
                mime_func = {'text': MIMEText,
                             'image': MIMEImage,
                             'audio': MIMEAudio,
                             'application': MIMEApplication,
                             'message': MIMEText,
                             }
                with open(filename, 'r') as attached_data:
                    msg = mime_func[maintype](attached_data.read(), _subtype=subtype)
                msg.add_header('Content-Disposition', 'attachment',
                               filename=os.path.basename(filename))
                mime_message.attach(msg)
        return mime_message

    def smtp_send_message(self, sender, recipient, sendmsg, servertype=None, printchar='.'):
        if not servertype:
            servertype = self.servertype
        client = LightSmtpClient(self.inject_host, self.inject_port, servertype=servertype, \
                                 bind_ip=self.bind_ip, debug=self.debug, \
                                 certfile=self.tls_cert_file, keyfile=self.tls_key_file, timeout=self.socket_timeout)
        if self.login_enable:
            status = client.user_login(self.username, self.password, authmethod=self.auth_method)
        client.send_mail(sender, recipient, sendmsg, printchar, count=self.max_msg_per_connection, dot=self.dotcount)
        client.disconnect()
        self.total_message_count += self.max_msg_per_connection
        if self.delay:
            time.sleep(self.delay)
        return

    def execute_on_duration(self, queue_enabled=0):
        execute_status = 0
        if self.duration:
            starttime = time.time()
            while ((time.time() - starttime) < self.duration):
                if self.address_list_input:
                    for host_addr in self.address_list_input:
                        if self.rcpt_append_str:
                            host_addr = host_addr.strip() + self.rcpt_append_str
                        if self.mbox_message:
                            execute_status = self.execute(duration=self.duration, start=starttime, \
                                                          queue_enabled=queue_enabled, host_addr=host_addr,
                                                          sendmsg=str(self.mbox_message.next()))
                        else:
                            if not self.message_list:
                                break
                            for sendmsg in self.message_list:
                                execute_status = self.execute(duration=self.duration, start=starttime, \
                                                              queue_enabled=queue_enabled, host_addr=host_addr,
                                                              sendmsg=sendmsg)
                        if execute_status:
                            break
                else:
                    self.execute(duration=self.duration, start=starttime, queue_enabled=queue_enabled)
                if execute_status:
                    break
                # if self.repeat_address_list:
                #    self.repeat_count += 1
                #    self.address_list = self.address_list * self.repeat_count
        return

    def execute(self, duration=0, start=0, queue_enabled=0, host_addr=None, sendmsg=None):
        servertype = 'basic'
        printchar = '.'
        if self.bind_ips:
            self.bind_ip = self.bind_ips.next_ip()
        if self.msg_body or self.attachment_file or self.msg_file or self.mbox_file:
            if host_addr:
                for sender in self.mail_from_list:
                    sender_host_addrlist = host_addr.split(',')
                    if len(sender_host_addrlist) > 1:
                        sender = sender_host_addrlist[0]
                        host_addr = sender_host_addrlist[1:]
                    if (time.time() - start) > int(duration):
                        return 1
                    if queue_enabled:
                        while DURATION_QUEUE.full():
                            time.sleep(0.5)
                        if not DURATION_QUEUE.full():
                            if self.tls_max_connection > 0 and self.tls_max_connection <= 100.0:
                                if (math.floor(float(self.message_count) % (100 / self.tls_max_connection))) == 0.0:
                                    servertype = 'tls'
                                    printchar = '~'
                                    self.tls_msg_count += 1
                                else:
                                    servertype = 'basic'
                                    printchar = '.'
                            DURATION_QUEUE.put([sender, host_addr, sendmsg, servertype, printchar])
                            self.message_count += 1
                    else:
                        self.smtp_send_message(sender, host_addr, sendmsg)
            else:
                for sender in self.mail_from_list:
                    for sendmsg in self.message_list:
                        self.smtp_send_message(sender, self.recp_host_list, sendmsg)

    def get_address_per_msg(self, address, count):
        per_value = 0
        address_list = []
        for eachvalue in range(len(address) / count):
            per_value += count
            address_list.append(address[eachvalue * count:per_value])
        return address_list

    def process_option(self, args):

        if args.inject_host:
            self.inject_host = args.inject_host

        if args.inject_port:
            self.inject_port = args.inject_port

        if args.mbox_header:
            self.process_mbox_header(args.mbox_header)

        if args.tls_enable:
            self.servertype = 'tls'

        if args.tls_cert_file and args.tls_key_file:
            self.servertype = 'tls'
            self.tls_cert_file = args.tls_cert_file
            self.tls_key_file = args.tls_key_file
            
        if args.cache_mbox:
            self.cache_mbox = 0

        self.message_list = self.get_message(args)

        if args.delay:
            self.delay = float(args.delay)
        if args.repeat_address_list:
            self.repeat_address_list = True

        if args.auth_user and args.auth_password:
            self.servertype = 'tls'
            self.login_enable = True
            self.username = args.auth_user
            self.password = args.auth_password

        if args.socket_timeout:
            self.socket_timeout = int(args.socket_timeout)

        if args.auth_method:
            self.auth_method = args.auth_method
        if args.debug:
            self.debug = args.debug

        if args.dot_count:
            self.dotcount = int(args.dot_count)

        if args.duration:
            self.duration = float(args.duration)

        if args.num_msgs:
            self.message_count, self.max_msg_per_connection = int(args.num_msgs), int(args.num_msgs)

        if args.bind_ips:
            self.bind_ips = IPs(args.bind_ips)

        if args.max_msg_per_connection:
            self.max_msg_per_connection = int(args.max_msg_per_connection)
            if self.max_msg_per_connection == 1 and self.message_count > 0:
                self.max_msg_per_connection = self.message_count

        if args.mail_from:
            if args.mail_from_in_list:
                self.mail_from_list.append('%s%s' % (args.mail_from, re.sub('@', '', args.mail_from_in_list)))
            else:
                self.mail_from_list.append(args.mail_from)

        if args.num_senders:
            num_senders = int(args.num_senders)
            format_re = re.compile('%d')
            if num_senders != -1 and len(format_re.findall(args.mail_from)) != 1:
                print 'The --mail-from option must contain a %d when used in conjunction\nwith the --num_senders option'
                parser.print_help()
                return
            else:
                # handling mail from list based on num senders
                self.mail_from_list = [args.mail_from % address for address in range(0, num_senders)]

        # adding support for mail_from is not given to add random testuser
        if not args.mail_from:
            self.mail_from_list.append('testuser@%s' % (socket.gethostname()))

        if args.address_list:
            addr_file, rcpt_append_str = args.address_list, ''
            if args.address_list.find(':') != -1:
                addr_file, rcpt_append_str = args.address_list.split(':')
                self.check_option(addr_file, 'address list file: %s does not exist.' % addr_file)
                self.address_list_file = addr_file
                file_input = open(addr_file, 'r')
                self.address_list_input = file_input.readlines()
                file_input.close()
                self.rcpt_append_str = rcpt_append_str
            else:
                self.check_option(addr_file, 'address list file: %s does not exist.' % addr_file)
                self.address_list_file = addr_file
                file_input = open(addr_file, 'r')
                self.address_list_input = file_input.readlines()
                file_input.close()
                self.rcpt_append_str = rcpt_append_str

        if args.rcpt_host_list:
            recp_list = args.rcpt_host_list.split(',')
            for eachrcpt in recp_list:
                if self.verify_mail_address(eachrcpt):
                    self.recp_host_list.append(eachrcpt)
                else:
                    self.recp_host_list.append(eachrcpt)
                    # To handle auto generate user for the domain name
                    if '.' in eachrcpt and '@' not in eachrcpt:
                        self.recp_host_list = ['user%d@%s' % (x, eachrcpt) for x in range(1, 2)]

        if args.addr_per_msg:
            addr_per_msg = int(args.addr_per_msg)
            if not args.address_list and not args.rcpt_host_list:
                print 'The --addr-per-msg option must be used in conjunction\nwith the --address-list/--rcpt-host-list option'
                return
            if args.address_list:
                self.address_list = self.get_address_per_msg(self.address_list, addr_per_msg)
                print "Address list based on addr_per_msg", self.address_list
            else:
                print "addr_per_msg, recp_host_list", addr_per_msg, len(self.recp_host_list)
                if addr_per_msg <= len(self.recp_host_list):
                    self.recp_host_list = self.get_address_per_msg(self.recp_host_list, addr_per_msg)
                else:
                    print "addr_per_msg is needs to less than equal to recp_host_list/ address list entries"
                    return

        if args.tls_max_connection:
            if not args.duration:
                print "tls_max_connection can be used along with duration"
                raise FatalOption
            self.tls_max_connection = float(args.tls_max_connection)

    def check_option(self, argument, err_text):
        if not os.path.exists(argument):
            print >> stderr, err_text
            raise FatalOption

    def verify_mail_address(self, mailaddress):
        if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', mailaddress):
            return False
        else:
            return True


def process_queue_message(starttime, duration):
    while ((time.time() - starttime) < duration):
        if not MAIL_QUEUE.empty():
            sender, recipient, send_msg, server_type, printchar = MAIL_QUEUE.get()
            # print ">>> ",sender, recipient,server_type, printchar
            spam.smtp_send_message(sender, recipient, send_msg, server_type, printchar)
    spam.message_list = []
    return


def execute_parallel(queue_enabled=0, starttime=0, duration=0):
    process_queue_message(starttime, duration)
    return


def get_queue_size1(output, destqueue, queue_csv):
    '''get_queue_size(s)
    Return the average queue size (per second) represented in the string s.
    '''
    lines = output.splitlines()
    size, tot_in, tot_out = (-1, 0, 0)
    last_size = 0
    time_array = []
    for line in lines:
        try:
            time_str, size, _in, out = line.split()
            if queue_csv:
                with open(queue_csv, 'a+') as data_csv:
                    data_csv.write("%s,%s,%s,%s\n" % (time_str, size, _in, out))
            time_array.append(time.strptime(time_str, '%H:%M:%S'))
            tot_in += int(_in)
            tot_out += int(out)
        except IndexError:
            return (-1, -1, -1)
        except ValueError:
            continue
        last_size = int(size)

    sent = tot_in
    recv = tot_out
    if destqueue == 'work':
        # For work queue, _in is Recv and out is Processed
        sent = tot_out
        recv = tot_in
    return (last_size, sent, recv)


def get_queue_size(output, destqueue, queue_csv):
    lines = output.splitlines()
    size, inp, out = (0, 0, 0)
    time_array = []
    for line in lines:
        try:
            time_str, size, inp, out = line.split()
            size, inp, out = int(size), int(inp), int(out)
            if queue_csv:
                with open(queue_csv, 'a+') as data_csv:
                    data_csv.write("%s,%s,%s,%s\n" % (time_str, size, inp, out))
            # time_array.append(time.strptime(time_str, '%H:%M:%S'))
        except IndexError:
            return (-1, -1, -1)
        except ValueError:
            continue
    return (size, inp, out)


def initialize_work_queue(starttime, duration, dut, queue_target, username='admin', password='ironport', prompt='> ',
                          queue_csv=None):
    status, session = start_telnet_session(dut, username, password, prompt)
    if status:
        configure_workqueue_rate(1, session)
        monitor_work_queue(starttime, duration, session, queue_target, queue_csv)
        return
    else:
        queue.put(-1)


def configure_workqueue_rate(rate, session):
    session.write('workqueue rate %d\n' % rate)
    return True


def monitor_work_queue(starttime, duration, session, queue_target, queue_csv):
    interval = 1
    size = 0
    prev_size, prev_sent, prev_recieved = 0, 0, 0
    while ((time.time() - starttime) < duration):
        time.sleep(interval)
        queue_output = session.read_very_eager()
        # try:
        size, sent, received = get_queue_size(queue_output, 'work', queue_csv)
        if size == 0:
            size, sent, received = prev_size, prev_sent, prev_recieved
        msgcount = (size - queue_target)
        prev_size, prev_sent, prev_recieved = size, sent, received

        high_level = queue_target + (queue_target * 7.5 / 100.0)
        print "msgcount abscount", msgcount, abs(msgcount) * 100 / 500
        if msgcount > 0:
            if msgcount / float(high_level) > 1:
                msgcount = int(msgcount)
            else:
                msgcount = int(msgcount + (queue_target * 5 / 100.0))
        if msgcount < 0 and (abs(msgcount) * 100 / 500) <= 25:
            msgcount = int(msgcount - (queue_target * 50 / 100.0))
        if msgcount < 0 and (abs(msgcount) * 100 / 500) <= 20:
            msgcount = int(msgcount - (queue_target * 25 / 100.0))
        if msgcount < 0 and (abs(msgcount) * 100 / 500) <= 15:
            msgcount = int(msgcount - (queue_target * 20 / 100.0))
        if msgcount < 0 and (abs(msgcount) * 100 / 500) <= 10:
            msgcount = int(msgcount - (queue_target * 15 / 100.0))
        if msgcount < 0 and (abs(msgcount) * 100 / 500) <= 5:
            msgcount = int(msgcount - (queue_target * 10 / 100.0))

        if size > high_level:
            print "High level ", size, high_level
            continue
        elif (size - high_level) > 0:
            print "Diff High level ", size, high_level
            continue
        elif (size + MAIL_QUEUE.qsize()) > high_level:
            print "Above MAIL QUEUE SIZE", size, high_level, \
                MAIL_QUEUE.qsize(), size + MAIL_QUEUE.qsize()
            continue
        else:
            # print "\nmsgcount , size, high diff  : size+ q ", msgcount, size,  size - high_level , size + MAIL_QUEUE.qsize()
            # print "DUR Q ", DURATION_QUEUE.qsize() , MAIL_QUEUE.qsize()
            for count in range(abs(msgcount)):
                if not DURATION_QUEUE.empty() and not MAIL_QUEUE.full():
                    MAIL_QUEUE.put(DURATION_QUEUE.get())
    DURATION_QUEUE.queue.clear()
    MAIL_QUEUE.queue.clear()
    return


def start_telnet_session(dut, username, password, prompt):
    try:
        telnet_session = telnetlib.Telnet(dut)
        telnet_session.read_until('login: ')
        telnet_session.write('%s\n' % username)
        # telnet_session.read_until('%s@%s\'s password: ' % (username, dut))
        telnet_session.read_until('Password:')
        telnet_session.write('%s\n' % password)
        telnet_session.read_until(prompt)
        print "Telnet connection with the: %s was successful\n" % dut
        return (True, telnet_session)
    except Exception, error:
        print "Telnet connection with the: %s was not successful\n " % dut
        print "ERROR::", error
        return (False, error)


def execute_concurrent_workqueue(options, duration, debug=False):
    threads = []
    concurrent_threads = []
    starttime = time.time()
    queue_thread = threading.Thread(target=initialize_work_queue, kwargs=dict(starttime=starttime, \
                                                                              duration=duration, \
                                                                              dut=options.dut, \
                                                                              queue_target=int(options.queue_target), \
                                                                              queue_csv=options.queue_data_csv))
    print "Concurrent Connections::", options.concurrent, duration
    execution_thread = threading.Thread(target=spam.execute_on_duration, kwargs=dict(queue_enabled=1))
    concurrent_threads.append(queue_thread)
    concurrent_threads.append(execution_thread)
    for connection in range(int(options.concurrent)):
        if debug:
            print "INFO::started connection:", connection
        t = threading.Thread(target=execute_parallel,
                             kwargs=dict(queue_enabled=1, starttime=starttime, duration=duration))
        threads.append(t)
    for t in concurrent_threads:
        t.start()
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in concurrent_threads:
        t.join()  # block until all threads finished
    print "\nExecution of concurrent connections finished.."
    return

def process_duration_queue(starttime, duration):
    while ((time.time() - starttime) <= duration):
        if not DURATION_QUEUE.empty():
            sender, recipient, send_msg, server_type, printchar = DURATION_QUEUE.get()
            spam.smtp_send_message(sender, recipient, send_msg, server_type, printchar)
    spam.message_list = []
    exit()
    return

def execute_concurrent_options(options, duration, debug=False):
    threads = []
    concurrent_threads = []
    starttime = time.time()
    if debug:
        print "Concurrent Connections::", options.concurrent, duration
    execution_thread = threading.Thread(target=spam.execute_on_duration, kwargs=dict(queue_enabled=1))
    concurrent_threads.append(execution_thread)
    for connection in range(int(options.concurrent)):
        if debug:
            print "INFO::started connection:", connection
        t = threading.Thread(target=process_duration_queue,
                             kwargs=dict(starttime=starttime, duration=duration))
        threads.append(t)
    for t in concurrent_threads:
        t.start()
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in concurrent_threads:
        t.join()  # block until all threads finished
    print "\nExecution of concurrent connections finished.."
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Light smtp client for spamming email / inject: Threaded\n')

    parser.add_argument('--mail-from', dest='mail_from', \
                        help='Hostname to insert into the mail from field of each message')

    parser.add_argument('--mail-from-in-list', dest='mail_from_in_list', \
                        help='Hostname to insert into the mail from field of each message')

    parser.add_argument('--num-senders=', dest='num_senders', \
                        help='In order to cycle through many mail froms, each number needs to be inserted \
                              into the --mail-from option. If --mail-from=user@domain.com and \
                          --num-senders=5, smtp_spam will cycle through the addresses \
                          user0@domain.com to user4@domain.com.')

    parser.add_argument('--rcpt-host-list=', dest='rcpt_host_list', \
                        help='List of hosts (separated by comma) to address mail to\
                              example : testuser@domain.com,testuser2@domain.com')

    parser.add_argument('--num-msgs=', dest='num_msgs', \
                        help='Number of messages to send. This overrides any other option. \
                         (Setting this to 0 will function like the option was not passed). \
                          default:1')

    parser.add_argument('--msg-filename=', dest='msg_file', \
                        help='Filename(s) of message bodies to use')

    parser.add_argument('--mbox-filename=', dest='mbox_file', help='mbox-format mailbox to use for message bodies.')

    parser.add_argument('--attach-filename=', dest='attachment_file', \
                        help='Filename(s) of attachments to use (All the files\
                         specified will be attached to all messages sent.)')

    parser.add_argument('--msg-body=', dest='msg_body', \
                        help='String to use as message body')

    parser.add_argument('--mbox-header=', dest='mbox_header', action='append', \
                        help='Use with mbox-filename: Replace the <header_name> header in each message with a \
                          line from the file <file_name>. If <file_name> runs out of lines, it is reopened \
                          and used again. This option can be used more than once for different headers.')

    parser.add_argument('--custom-header=', dest='custom_header', \
                        help='Custom header:value pairs to be added in the message.')

    parser.add_argument('--subject=', dest='msg_subject', \
                        help='A custom Subject string')

    parser.add_argument('--duration=', dest='duration', \
                        help='Number of seconds to run the test (Default 30)')

    parser.add_argument('--address-list=', dest='address_list', \
                        help='<file_name>[:suffix] \n File to get addresses from. Test runs until the addresses\
                         are exhausted. Append a suffix to all addresses by appending\
                         a string to the filename with a colon.')

    parser.add_argument('--delay=', dest='delay', help='Delay in seconds. for each connections on messages sent.')

    parser.add_argument('--addr-per-msg=', dest='addr_per_msg', \
                        help='Number of recipients per message. (Default 1)  can be used with address list/rcpt-host-list')

    parser.add_argument('--dot=', dest='dot_count', \
                        help='Messages per dot')

    parser.add_argument('--repeat-address-list=', dest='repeat_address_list', \
                        help='Run through the address list until duration.')

    # Need to handle True/False accept only boolean
    parser.add_argument('--debug=', dest='debug', default=False, help='To enable the debugging log message ')

    parser.add_argument('--port=', dest='inject_port', default='25',
                        help='Port to inject to.  (Default 25)')

    parser.add_argument('--inject-host=', dest='inject_host', required=True, \
                        help='Host to inject to.')

    parser.add_argument('--max-msgs-per-conn=', dest='max_msg_per_connection', \
                        help='Maximum number of messages to send over each \
                                    connection. (Default 0 - Infinite)')

    parser.add_argument('--bind-ips=', dest='bind_ips', \
                        help='Bind to a local IP or IP range. (Ex. 1.2-3.4.5-6 yields\
                        1.2.4.5, 1.2.4.6, 1.3.4.5, 1.3.4.6)')

    parser.add_argument('--tls', dest='tls_enable', help='Send with TLS enabled')

    parser.add_argument('--tls-cert-file', dest='tls_cert_file', \
                        help='Path to client certificate.  If not specified demo\
                             certificate will be used.  If \'-\' specified instead\
                             of a file no certificate will be used.\
                             Should be used with --tls.\
                             supported format for cert file are .pem /.crt')

    parser.add_argument('--tls-key-file', dest='tls_key_file', \
                        help='Path to private key that corresponds to a certificate \
                             specified by --tls-cert-file.  Should be used with --tls-cert-file. \
                             supported format for key file are .pem / .key')

    parser.add_argument('--auth-method=', dest='auth_method', \
                        help='--auth-method==<type> Use SMTP Auth with method <type> where <type> can \
                         be PLAIN or LOGIN or CRAM-MD5')

    parser.add_argument('--user=', dest='auth_user', \
                        help='When using SMTP Auth, this is the user to be authenticated.')

    parser.add_argument('--passwd=', dest='auth_password', \
                        help='The password associated with the given user')

    # parser.add_argument('--smtpauth-file=', dest='smtp_auth_file', \
    #                    help='Location of file containing a list of SMTP Auth methods,\
    #                      users and passwords where each line looks like: \
    #                      <auth-method> <user> <password>\
    #                      For each new connection made by smtp_spam, a new method/user/pass \
    #                      combo will be used from the list. smtp_spam will also repeat \
    #                      the list as needed.')

    parser.add_argument('--timeout=', dest='socket_timeout', \
                        help='Number of seconds to wait for socket I/O \
                         (Default 300)')

    parser.add_argument('--concurrency=', dest='concurrent', \
                        help='Number of connections (Default 10)')

    parser.add_argument('--cache-mbox=', dest='cache_mbox', \
                        help='0 if you don\'t want to cache mbox messages in memory (Default is 1)')

    # parser.add_argument('--msg-size=', dest='msg_size', \
    #                     help='Size of each message (Default 1024). Message size\
    #                      range of (N, M) is only supported with --randomize.')

    # parser.add_argument('--randomize=', dest='randomize', \
    #                    help='Randomize message size and delay. S is the \
    #                    optional seed. Set it to repeat the random sequence.')
    #
    # parser.add_argument('--bandwidth-cap=', dest='bandwidth_cap', \
    #                    help='Simulate limiting bandwith to N bytes per second aggregate')

    # parser.add_argument('--connection-bandwidth-cap=', dest='connection_bandwidth_cap', \
    #                    help='Simulate limiting bandwith to N bytes per second per connection')

    # parser.add_argument('--preferred-proto-version=', dest='preferred_proto_version', \
    #                    help='Prefer specified IP protocol version to connect to \
    #                      inject host. <protocol_version> could be 4 or 6. \
    #                      Overrides any previos preferred-proto-version and \
    #                      required-proto-version options.')
    #
    # parser.add_argument('--required-proto-version==', dest='req_proto_version', \
    #                    help='Require specified IP protocol version to connect to \
    #                      inject host. <protocol_version> could be 4 or 6. \
    #                      Overrides any previos preferred-proto-version and \
    #                      required-proto-version options.')
    #
    # parser.add_argument('--v6-connections-ratio=', dest='ipv6_conn_ratio', \
    #                    help='Each message will be sent through IPv4 or IPv6 chosen \
    #                      by random.  Ratio defines aproximate relation between\
    #                      number of messages sent through IPv6 to messages sent\
    #                      through IPv4.  Ratio should be integer from 0-100\
    #                      range.  Overrides preferred-proto-version')
    #
    # parser.add_argument('--verbose=', dest='verbose', \
    #                    help='Turn on verbose error output. (Default off)')

    #  parser.add_argument('--merge-xmrg=', dest='merge_xmrg', \
    #                    help='Use XMRG mail merge protocol')

    # parser.add_argument('--merge-parts=', dest='merge_parts', \
    #                    help='Number of XPRT parts per message')

    # parser.add_argument('--merge-defs=', dest='merge_defs', \
    #                    help='Number of XDFN keys/replacements per message')

    # parser.add_argument('--tls-key-pass=', dest='tls_key_password', \
    #                    help='Password to decrypt private key specified by\
    #                      --tls-key-file.  Ignored when key is not password protected.')

    parser.add_argument('--DUT=', dest='dut', \
                        help='The DUT in which to collect queue data from. example: C100V')

    parser.add_argument('--queue-target=', dest='queue_target', \
                        help='The target number of messages that smtp_spam should keep in the specified queue. example : 500')

    # parser.add_argument('--queue-verbose=', dest='queue_verbose', \
    #                    help='Print out the current queue size (of the targeted queue)\
    #                    and the current message delay per connection into the C60.')

    parser.add_argument('--queue-data-csv=', dest='queue_data_csv', \
                        help='write the queue data in the csv file')

    parser.add_argument('--tls-connection-max=', dest='tls_max_connection', \
                        help='Maximum tls connection is allowed during duration.. \
                        usage : for 30 percent value needs to be 30.0')
    parser.add_argument('--version', action='version', version='smtp_spam Lightsmtp:%s' % (__version__), help='SMTP SPAM Lightsmtp active version')

    args = parser.parse_args()
    starttime = time.time()
    if args.queue_target:
        queue_target = int(args.queue_target)
        BUFFER_SIZE = int(queue_target + (queue_target * 10 / 100))
        MAIL_QUEUE = Queue.Queue(BUFFER_SIZE)
        DURATION_QUEUE = Queue.Queue(2 * BUFFER_SIZE)
        if not args.dut:
            raise FatalError('--dut option needs to specify for --queue-target')
        if args.concurrent:
            # To handle when lot of concurrent connections
            if not args.duration:
                print "duration needs to specify for concurrent"
                exit(1)
            args.socket_timeout = 180
            spam = LightWeightSpam()
            spam.process_option(args)
            execute_concurrent_workqueue(args, int(args.duration), args.debug)
            print "Total Message Count:", spam.message_count
            print "TLS message Count :", spam.tls_msg_count
        else:
            spam = LightWeightSpam()
            spam.process_option(args)
            if args.duration:
                spam.execute_on_duration()
            else:
                spam.execute()
    else:
        spam = LightWeightSpam()
        spam.process_option(args)
        if args.concurrent:
            args.socket_timeout = 180
            DURATION_QUEUE = Queue.Queue(100 * int(args.concurrent))
            execute_concurrent_options(args, int(args.duration), args.debug)
        else:
            if args.duration:
                spam.execute_on_duration()
            else:
                spam.execute()
    print "Time taken:%0.3f" % (time.time() - starttime)
    exit(0)