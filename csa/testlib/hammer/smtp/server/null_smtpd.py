import ssl
import time
import datetime
import os
import sys
import signal
import argparse
import commands
import shutil
import logging

from secure_smtpd import SMTPServer, CredentialValidator, LOG_NAME
from sys import stderr

__version_info__ = ('1','0','012')
__version__ = '.'.join(__version_info__)
__author__ = 'Beno K Immanuel'

mbox_enable = 0


class TlsCertificate():
    def __init__(self, certfile, keyfile):
        self.ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_ctx.load_cert_chain(certfile=certfile, keyfile=keyfile)


class FatalOption:
    pass


class FatalError(Exception):
    def __init__(self, msg):
        stderr.write(msg)


class SSLSMTPServer(SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, message_data, data):
        stderr.write('.')
        if self.debug:
            print "*" * 30
            print "INFO::Peer:", peer
            print "INFO::From:", mailfrom
            print "INFO::To:", rcpttos
            print "*" * 30
        if mbox_enable:
            self.add_mbox_data(mailfrom, rcpttos, message_data)

    def add_mbox_data(self, mailfrom, recipient, message_data):
        data_buffer = []
        starttime = time.time()
        current_time = time.strftime('%a %b %d %H:%M:%S %Y', time.localtime(time.time()))
        recipient = ['X-IronPort-RCPT-TO:%s' % recp for recp in recipient]
        data_buffer.extend(["From %s %s" % (mailfrom, current_time), '\n'.join(recipient), message_data])

        with open(args.log_file, 'ab+') as fdata:
            fdata.writelines("%s\n" % line for line in data_buffer)
        if self.debug:
            print "\nINFO::Time taken to mbox write:%0.4f" % (time.time() - starttime)


def smtpd_start(args):
    soft_bounce_perc = 0
    hard_bounce_perc = 0
    smtp_auth_succeed_perc = 1

    debug = False
    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(logging.INFO)

    if args.bind_ip:
        bind_ip = args.bind_ip
    else:
        bind_ip = ''

    if args.bind_port:
        bind_port = int(args.bind_port)

    if args.debug:
        print "INFO::Debug:", args.debug
        debug = True

    if args.concurrency:
        concurrent = int(args.concurrency)
    else:
        concurrent = 10

    if args.soft_bounce:
        soft_bounce_perc = int(args.soft_bounce)

    if args.hard_bounce:
        hard_bounce_perc = int(args.hard_bounce)

    if soft_bounce_perc < 0 or soft_bounce_perc > 100:
        parser.print_help()
        print "ERROR::Soft bounce percentage must between 0 and 100."
        exit(1)

    if hard_bounce_perc < 0 or hard_bounce_perc > 100:
        parser.print_help()
        print "Hard bounce percentage must between 0 and 100."
        exit(1)

    if soft_bounce_perc + hard_bounce_perc > 100:
        parser.print_help()
        print "Soft plus hard bounce percentages must not be more than 100."
        exit(1)

    soft_bounce_perc /= 100.0
    hard_bounce_perc /= 100.0
    if args.smtp_auth_succeed:
        smtp_auth_succeed_perc = int(args.smtp_auth_succeed)/100.0

    if debug:
        print "INFO::Input arguments", args
        print "INFO::bind_ip", bind_ip, bind_port
        if args.log_file:
            print  "INFO::Log file:", args.log_file

        if args.soft_bounce:
            print "INFO::soft_bounce percent:%s" % soft_bounce_perc

        if args.hard_bounce:
            print "INFO::hard_bounce percent:%s" % hard_bounce_perc

    if args.tls:
        if args.tls_certfile and args.tls_keyfile:
            check_option(args.tls_certfile, 'cert file: %s does not exist.' % args.tls_certfile)
            check_option(args.tls_keyfile, 'key file: %s does not exist.' % args.tls_keyfile)
            context = TlsCertificate(args.tls_certfile, args.tls_keyfile).ssl_ctx
        else:
            print "ERROR::--tls-certfile and --tls-keyfile is needed to enable smtpd with tls"
            exit()

        server = SSLSMTPServer(
            (bind_ip, bind_port),
            None,
            require_authentication=False, tls=True,
            credential_validator=CredentialValidator(),
            maximum_execution_time=1.0,
            ssl_ctx=context,
            soft_bounce=soft_bounce_perc,
            hard_bounce=hard_bounce_perc,
            process_count=concurrent,
            smtp_auth_succeed_perc=smtp_auth_succeed_perc,
            debug=debug)
    elif args.ssl:
        if args.tls_certfile and args.tls_keyfile:
            check_option(args.tls_certfile, 'cert file: %s does not exist.' % args.tls_certfile)
            check_option(args.tls_keyfile, 'key file: %s does not exist.' % args.tls_keyfile)
        else:
            print "ERROR::--tls-certfile and --tls-keyfile is needed to enable smtpd with ssl"
            exit()
        server = SSLSMTPServer(
            (bind_ip, bind_port),
            None,
            require_authentication=False,
            ssl=True,
            certfile='sslserver.crt',
            keyfile='sslserver.key',
            credential_validator=CredentialValidator(),
            maximum_execution_time=1.0,
            soft_bounce=soft_bounce_perc,
            hard_bounce=hard_bounce_perc,
            process_count=concurrent,
            debug=debug)
    else:
        server = SSLSMTPServer((bind_ip, bind_port), None,
                               soft_bounce=soft_bounce_perc, \
                               hard_bounce=hard_bounce_perc,
                               process_count=concurrent,
                               maximum_execution_time=60,
                               debug=debug)
    server.run()


def check_option(argument, err_text):
    if not os.path.exists(argument):
        print >> sys.stderr, err_text
        raise FatalOption


def kill_pid(pid):
    os.kill(pid, signal.SIGTERM)


def check_port_available(ip, port):
    # need to handle multiple entries
    cmd = 'sudo netstat -natpl | grep %s:%s' % (ip, port)
    cmdoutput = commands.getoutput(cmd)
    runprogram = cmdoutput.strip().split(' ')
    runprogram = filter(None, runprogram)
    if runprogram:
        if '-' not in runprogram[-1]:
            pid, program = runprogram[-1].split('/')
            print "INFO::PID:", pid
            kill_pid(int(pid))
            # sleep added after killing socket , waits for socket to close connection completely
            time.sleep(60)
            return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Light smtpd server..')

    parser.add_argument('--bind-ip', dest='bind_ip', \
                        help='bind ip to smtpd server to run default:localhost')

    parser.add_argument('--port', dest='bind_port', default=25, \
                        help='bind port to smtpd server to run default:25')

    parser.add_argument('--tls', dest='tls', \
                        help='smtpd serv = er encrypted with tls.')

    parser.add_argument('--ssl', dest='ssl', \
                        help='smtpd server encrypted with ssl.')

    parser.add_argument('--log', dest='log_file', \
                        help='logfile to log/ mbox file ')

    parser.add_argument('--concurrency', dest='concurrency', \
                        help='concurrent server session.')

    parser.add_argument('--tls-certfile', dest='tls_certfile', \
                        help='tls certfile to use smtpd with tls')

    parser.add_argument('--tls-keyfile', dest='tls_keyfile', \
                        help='tls key to use smtpd with tls')

    parser.add_argument('--soft_bounce=N', dest='soft_bounce', \
                        help='Percent (from 0 to 100) of messages to soft bounce.')

    parser.add_argument('--hard_bounce=N', dest='hard_bounce', \
                        help='Percent (from 0 to 100) of messages to hard bounce')
    
    parser.add_argument('--smtpauth-pct-succeed=N', dest='smtp_auth_succeed', \
                        help='Minimum Percent (from 0 to 100) of messages to smtp_auth_succeed')

    parser.add_argument('--debug=', dest='debug', default=False, \
                        help='To enable the debugging log message.')

    parser.add_argument('--version', action='version', version='null_smtpd Lightsmtp:%s' % (__version__), help='Null SMTP Lightsmtp active version')

    args = parser.parse_args()

    if args.log_file:
        fileexists = os.path.isfile(args.log_file)
        if fileexists:
            basename, ext = os.path.splitext(args.log_file)
            timestamp = time.strftime('%d_%H_%M_%S_%Y', time.localtime(time.time()))
            backupfile = "%s_%s%s" % (basename, timestamp, ext)
            shutil.move(args.log_file, backupfile)
        with open(args.log_file, 'ab+') as fdata:
            pass
        mbox_enable = 1

    port = int(args.bind_port)
    if port in range(1, 1025):
        starttime = time.time()
        if args.bind_ip:
            check_port_available(args.bind_ip, port)
        else:
            check_port_available('', port)

    smtpd_start(args)
