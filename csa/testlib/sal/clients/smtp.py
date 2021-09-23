#!/usr/bin/env python
"""
    Collection of mail-related utilities.
        1) generate ham, spam or suspect ham msg
        2) inject_raw(): uses smtplib.SMTP
        3) class Spam: use smtplib.SMTP
        4) inject(): uses the Spam class, needs a host passed in now
        5) inject_qmqp()
        6) inject_ipmm()
"""
#: Reference Symbols: mailtools, ironman

from __future__ import absolute_import

import os
import socket
import sal.deprecated.smtptestlib as smtplib
import telnetlib
import time
import types

from sal.exceptions import ConfigError
import sal.clients.smtpspam
import sal.time


def gen_ham_msg(body=None, stress_header=None, header_subject=None,
                header_other=None):
    # stress_header should not contain the "X-Stress: " portion
    from_addr = 'test@%s' % socket.gethostname()
    to_addr = 'test@%s' % socket.gethostname()

    msg = []
    msg.append('From: %s' % from_addr)
    msg.append('To: %s' % to_addr)
    Subject = header_subject or 'ham-test-msg'
    msg.append('Subject: %s' % Subject)
    if header_other:
        msg.append(header_other)
    if stress_header != None:
        msg.append("X-Stress: %s" % stress_header)
    msg.append('')  # separate message header from body
    if body == None:
        msg.append('A simple non-spam message.\nThis is unique ham message' \
                   'Time is now: ' + sal.time.localtimestamp())
    else:
        msg.append(body)
    return '\r\n'.join(msg)


def gen_xad_spam_msg(body=None, msg_id=None):
    from_addr = "test@%s" % socket.gethostname()
    to_addr = "test@%s" % socket.gethostname()

    msg = []
    msg.append("From: %s" % from_addr)
    msg.append("To: %s" % to_addr)
    msg.append("X-Advertisement: spam")
    msg.append("Subject: xad-spam-test-msg")
    if msg_id:
        msg.append("Message-ID: <%s>" % (msg_id,))
    msg.append("")  # separate message header from body
    if body == None:
        msg.append("Because this message contains X-Advertisement set to "
                   "'spam' it will be identified as spam by the phoebe. " \
                   "Time is now:" + sal.time.localtimestamp())
    else:
        msg.append(body)
    return '\r\n'.join(msg)


def gen_xad_suspect_spam_msg(body=None):
    from_addr = "test@%s" % socket.gethostname()
    to_addr = "test@%s" % socket.gethostname()

    msg = []
    msg.append("From: %s" % from_addr)
    msg.append("To: %s" % to_addr)
    msg.append("X-Advertisement: suspectspam")
    msg.append("Subject: %s xad--spam-test-msg")
    msg.append("")  # separate message header from body
    if not body:
        msg.append("Because this message contains X-Advertisement set to "
                   "'suspect spam' it will be identified as "
                   "suspect spam by the phoebe. " \
                   "Time is now:" + sal.time.localtimestamp())
    else:
        msg.append(body)
    return '\r\n'.join(msg)


def inject_raw(msg=None, to_addr=None, from_addr=None, host='localhost'):
    """ Inject mgs via telnet session

        :Parameters:
            - `msg`: message's body in string
            - `to_addrs`: message's recipient
            - `from_addr`: message's sender
            - `host`: if None, default public interface will be used

        :Return:
            return tuple of all reply codes and msgs
    """
    if not from_addr:
        from_addr = 'from@%s' % (socket.gethostname(),)

    if not to_addr:
        to_addr = 'to@%s' % (socket.gethostname(),)

    if not msg:
        msg = gen_ham_msg()

    telnet_session = []
    connect = smtplib.SMTP(host=host)
    cmds = ('helo %s' % (socket.gethostname(),),
            'mail from: %s' % (from_addr,),
            'rcpt to: %s' % (to_addr,),
            'data',
            '%s\r\n.\r\n' % (msg,),
            )
    for cmd in cmds:
        connect.putcmd(cmd)
        reply = connect.getreply()
        telnet_session.append(reply)
    connect.quit()

    return telnet_session


class Spam:
    def __init__(self, hostname=None):
        self.hostname = hostname

        fqdn = socket.gethostname()
        self.from_addr = 'mail_from_test@' + fqdn
        self.to_addr = 'mail_to_test@' + fqdn
        self.payload = "Subject: This is a test\r\n\r\nThis is a test\r\n"

    def connect(self, hostname=None):
        ## NOTE: hangs if no route to host
        hostname = hostname or self.hostname
        if not hostname:
            raise ConfigError("Spam hostname not set.")
        self.server = smtplib.SMTP(hostname, 25)

    def disconnect(self):
        self.server.quit()

    def set_debuglevel(self, level=1):
        self.server.set_debuglevel(level)

    def send_raw_message(self, payload=None, from_addr=None, to_addr=None,
                         qty=1, mail_iter=None):
        if mail_iter:  # send varying messages using iterator
            for mi in mail_iter:
                self.server.sendmail(*mi)
            return

        # send same message repeatedly
        payload = payload or self.payload
        from_addr = from_addr or self.from_addr
        to_addr = to_addr or self.to_addr
        if isinstance(to_addr, str):
            to_addr = to_addr.split(',')
        for i in range(qty):
            self.server.sendmail(from_addr, to_addr, payload)

    sendmail = send_raw_message  # alias


def inject(host, msg=None, to_addr=None, from_addr=None):
    """ Injects given string(should be email's body)

    Uses sal.clients.smtp.Spam() class

        :Parameters:
            - `msg`: message's body in string
            - `to_addr`: message's recipient
            - `from_addr`: message's sender
            - `host`: if None, default public interface will be used
    """
    if not from_addr:
        from_addr = 'from@%s' % (socket.gethostname(),)

    if not to_addr:
        to_addr = 'to@%s' % (socket.gethostname(),)

    spammer = Spam()
    spammer.connect(hostname=host)
    spammer.send_raw_message(payload=msg, to_addr=to_addr, from_addr=from_addr)
    spammer.disconnect()
    time.sleep(5)


def inject_qmqp(host, mail_from, rcpt_to=None, headers=None, body='',
                data_rsp_code='K', port=628):
    """Inject message to a QMQP server.

        :Parameters:
            - `host`: host to inject message to.
            - `mail_from`: message's sender.
            - `rcpt_to`: string of comma separated list of recipients.
            - `headers`: dictionary of message headers.
            - `body`: message's body.
            - `data_rsp_code`: QMQP response code.
            - `port`: host's port to connect to.
    """

    def netstring(s):
        assert isinstance(s, types.StringType)
        return '%d:%s,' % (len(s), s)

    # message header
    header_string = ''
    if isinstance(headers, types.DictType):
        if headers.has_key('From'):
            header_string += 'From: ' + headers['From'] + '\r\n'
        if headers.has_key('to'):
            header_string += 'To: ' + ', '.join(headers['to']) + '\r\n'
        if headers.has_key('cc'):
            header_string += 'CC: ' + ', '.join(headers['cc']) + '\r\n'
        if headers.has_key('subject'):
            header_string += 'Subject: ' + headers['subject'] + '\r\n'
    if header_string: header_string += '\r\n'

    # default body
    if not body:
        body = 'text message body'

    # entire message
    msg = header_string + body

    print 'qmqp_inject:host=%s, mail_from:%s,rcpt_to:%s, ' \
          'data_rsp_code=%s' % (host, mail_from, rcpt_to, data_rsp_code)

    rcpt_list = ''
    if rcpt_to != None:
        for rcpt in rcpt_to.split(','):
            rcpt_list += netstring(rcpt.strip())

    qmqp_msg = netstring(
        netstring(msg)
        + netstring(mail_from)
        + rcpt_list
    )

    t = telnetlib.Telnet(host, port=port)
    try:
        t.write(qmqp_msg)
    except socket.error, e:
        if e[0] == 32:  # 'connection broke'
            # Sometimes we write much more than max_messag_size bytes
            # which causes the phoebe to break the tcp connection.
            # The script receives and ignores 'connection broke'(errno32)
            # error;  but prior to errno32 the response may have already
            # been written to the socket so we will attempt to
            # read it from the socket.
            pass
        else:
            raise socket.error, e

    real_resp = t.read_some()
    if real_resp.find(':' + data_rsp_code) == -1:
        raise AssertionError, 'Sent cmd: Expected resp: %s, Got resp: %s' \
                              % (data_rsp_code, real_resp)
    t.close()
    del t


def inject_ipmm(inj_host, to_addr=None, from_addr=None, msg='', port=25):
    """ Inject a IPMM message.

        :Parameters:
            - `inj_host`: host to inject message to
            - `to_addr`: message's recipient
            - `from_addr`: message's sender
            - `msg`: message's body
            - `port`: host's port to connect to

        :Return:
            a list of tuples (response code, response line)
    """

    hostname = socket.gethostname()

    if not to_addr:
        to_addr = 'to@' % (hostname,)

    if not from_addr:
        from_addr = 'from@' % (hostname,)

    replies = []
    cmds = ('EHLO %s' % (hostname,),
            'XLSMTP-ACKRCPT OFF',
            'XMRG FROM:<%s> VERSION=1' % (from_addr,),
            'RCPT TO:<%s>\r\nXPRT 1 LAST' % (to_addr,),
            '%s\r\n.\r\n' % (msg,))

    try:
        conn = smtplib.SMTP(inj_host, port)
        for cmd in cmds:
            reply = conn.putcmd(cmd)
            replies.append(reply)
    finally:
        conn.quit()

    return replies
