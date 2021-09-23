import secure_smtpd
import smtpdlib, base64, secure_smtpd, asynchat, logging
import ssl
import time
import random

from asyncore import ExitNow
from smtpdlib import NEWLINE, EMPTYSTRING, DEBUGSTREAM

def decode_b64(data):
    '''Wrapper for b64decode, without having to struggle with bytestrings.'''
    byte_string = data.encode('utf-8')
    decoded = base64.b64decode(byte_string)
    return decoded.decode('utf-8')


def encode_b64(data):
    '''Wrapper for b64encode, without having to struggle with bytestrings.'''
    byte_string = data.encode('utf-8')
    encoded = base64.b64encode(byte_string)
    return encoded.decode('utf-8')


class SMTPChannel(smtpdlib.SMTPChannel):

    def __init__(self, smtp_server, newsocket, fromaddr, \
                 require_authentication=False, credential_validator=None, map=None, smtp_auth_succeed_perc=None, debug=None):
        smtpdlib.SMTPChannel.__init__(self, smtp_server, newsocket, fromaddr)
        asynchat.async_chat.__init__(self, newsocket, map=map)
        self.require_authentication = require_authentication
        self.authenticating = False
        self.authenticated = False
        self.username = None
        self.password = None
        self.credential_validator = credential_validator
        self.logger = logging.getLogger(secure_smtpd.LOG_NAME)
        self.msg_count = 0
        self.grumpy = 0
        self.soft_bounce_percent = 0.0
        self.hard_bounce_percent = 0.0
        self.auth_succeed_pct = smtp_auth_succeed_perc
        self.debug = debug

    def smtp_QUIT(self, arg):
        self.push('221 Bye')
        self.close_when_done()
        raise ExitNow()

    def collect_incoming_data(self, data):

        if not isinstance(data, str):
            # We're on python3, so we have to decode the bytestring
            data = data.decode('utf-8')
        self.__line.append(data)

    def smtp_EHLO(self, arg):
        if not arg:
            self.push('501 Syntax: HELO hostname')
            return
        if self.__greeting:
            self.push('503 Duplicate HELO/EHLO')
        else:
            self.__greeting = arg
            if isinstance(self.__conn, ssl.SSLSocket):
                self.push('250-%s Hello %s' % (self.__fqdn, arg))
                self.push('250-AUTH LOGIN PLAIN')
                self.push('250 EHLO')
            else:
                self.push('250-%s' % self.__fqdn)
                # self.push('250 SIZE 10000')
                self.push('250 STARTTLS')

    def smtp_STARTTLS(self, arg):
        if arg:
            self.push('501 Syntax error (no parameters allowed)')
        elif self.__server.starttls and not isinstance(self.__conn, ssl.SSLSocket):
            self.push('220 Ready to start TLS')
            self.__conn.settimeout(30)
            self.__conn = self.__server.ssl_ctx.wrap_socket(self.__conn, \
                                                            server_side=True)
            self.__conn.settimeout(None)
            # re-init channel
            asynchat.async_chat.__init__(self, self.__conn)
            self.__line = []
            self.__state = self.COMMAND
            self.__greeting = 0
            self.__mailfrom = None
            self.__rcpttos = []
            self.__data = ''
            print >> DEBUGSTREAM, 'Peer: %s - negotiated TLS: %s' \
                                  % (repr(self.__addr), repr(self.__conn.cipher()))
            if self.debug:
                print >> DEBUGSTREAM, 'Peer: %s - negotiated TLS: %s' \
                                      % (repr(self.__addr), repr(self.__conn.cipher()))
        else:
            self.push('454 TLS not available due to temporary reason')
            if self.debug:
                print "454 TLS not available due to temporary reason"

    def smtp_AUTH(self, arg):

        straw = random.random()
        if straw > self.auth_succeed_pct:
            self.push('535 Authentication failed.')
            if self.debug:
                print "AUTH SUCCEED PCT:Authentication Failure"

        if 'PLAIN' in arg:
            split_args = arg.split(' ')
            # second arg is Base64-encoded string of blah\0username\0password
            authbits = decode_b64(split_args[1]).split('\0')
            self.username = authbits[1]
            self.password = authbits[2]
            if self.credential_validator and \
                    self.credential_validator.validate(self.username, self.password):
                self.authenticated = True
                self.push('235 Authentication successful.')
                if self.debug:
                    print "AUTH PLAIN\nOk Authenticated"
            else:
                if self.debug:
                    print "AUTH PLAIN\nAuthentication Failure"
                self.push('454 Temporary authentication failure.')
                raise ExitNow()

        elif 'LOGIN' in arg:
            self.authenticating = True
            split_args = arg.split(' ')
            # Some implmentations of 'LOGIN' seem to provide the username
            # along with the 'LOGIN' stanza, hence both situations are
            # handled.
            if len(split_args) == 2:
                self.username = decode_b64(arg.split(' ')[1])
                self.push(str('334 ' + encode_b64('Username')))
            else:
                self.push(str('334 ' + encode_b64('Username')))
        elif 'CRAM-MD5' in arg:
            self.push('502 Error command AUTH CRAM-MD5 not implemented.')
            raise ExitNow()
        elif not self.username:
            self.username = decode_b64(arg)
            self.push('334 ' + encode_b64('Password'))
        else:
            self.authenticating = False
            self.password = decode_b64(arg)
            if self.credential_validator and \
                    self.credential_validator.validate(self.username, self.password):
                self.authenticated = True
                self.push('235 Authentication successful.')
                if self.debug:
                    print "AUTH LOGIN\nOk Authenticated"
            else:
                self.push('454 Temporary authentication failure.')
                if self.debug:
                    print "AUTH LOGIN\nAuthentication Failure"
                raise ExitNow()

    # This code is taken directly from the underlying smtpd.SMTPChannel
    # support for AUTH is added.
    def found_terminator(self):
        line = EMPTYSTRING.join(self.__line)
        if self.debug:
            self.logger.info('found_terminator(): data: %s' % repr(line))
        self.__line = []
        if self.__state == self.COMMAND:
            if not line:
                self.push('500 Error: bad syntax.')
                return
            method = None
            i = line.find(' ')
            if self.authenticating:
                # If we are in an authenticating state, call the
                # method smtp_AUTH.
                arg = line.strip()
                command = 'AUTH'
            elif i < 0:
                command = line.upper()
                arg = None
            else:
                command = line[:i].upper()
                arg = line[i + 1:].strip()
            # White list of operations that are allowed prior to AUTH.
            if not command in ['AUTH', 'EHLO', 'HELO', 'NOOP', 'RSET', 'QUIT']:
                if self.require_authentication and not self.authenticated:
                    self.push('530 Authentication required')
                    if self.debug:
                        print "530 Authentication required"
                    return
            method = getattr(self, 'smtp_' + command, None)
            if not method:
                self.push('502 Error: command "%s" not implemented.' % command)
                if self.debug:
                    print '502 Error: command "%s" not implemented.' % command
                return
            method(arg)
            return
        else:
            if self.__state != self.DATA:
                self.push('451 Internal confusion.')
                return
            # Remove extraneous carriage returns and de-transparency according
            # to RFC 821, Section 4.5.2.
            data = []
            for text in line.split('\r\n'):
                if text and text[0] == '.':
                    data.append(text[1:])
                else:
                    data.append(text)
            self.__data = NEWLINE.join(data)
            status = self.__server.process_message(
                self.__peer,
                self.__mailfrom,
                self.__rcpttos,
                self.__data, data
            )
            self.__rcpttos = []
            self.__mailfrom = None
            self.__state = self.COMMAND
            self.set_terminator(b'\r\n')
            if not status:
                self.push('250 Ok')
            else:
                self.push(status)

    def smtp_MAIL(self, arg):
        self.msg_count += 1
        bounce_perc = self.soft_bounce_percent + self.hard_bounce_percent
        if bounce_perc:
            straw = random.random()
            if straw < self.soft_bounce_percent:
                return self.soft_bounce()
            elif straw < bounce_perc:
                return self.hard_bounce()

        print >> DEBUGSTREAM, '===> MAIL', arg
        address = self.__getaddr('FROM:', arg) if arg else None
        if not address:
            self.push('501 Syntax: MAIL FROM:<address>.')
            return
        if self.__mailfrom:
            self.push('503 Error: nested MAIL command.')
            return
        self.__mailfrom = address
        print >> DEBUGSTREAM, 'sender:', self.__mailfrom
        self.push('250 Ok')

    def bounce(self):
        """Return a bounce message to the sender."""
        # XXX
        answers = ("554 delivery error: we are simulating a user over quota.",
                   "554 delivery error: this user hypothetically doesn't exist.",
                   "552 Requested mail action aborted: exceeded storage allocation.",
                   "552 Requested mail action aborted: I don't like the look of your face, mister.",
                   '406 Out of file space.',
                   '503 Anonymous Senders Prohibited',
                   '550 MAILBOX NOT FOUND',
                   '451 qqt failure (#4.3.0)'
                   )
        self.push(random.choice(answers))

    def soft_bounce(self):
        """Return a soft bounce (4XX error code)."""
        answers = ('406 Out of file space.',
                   '466 Mailbox temporarily full.',
                   '421 Too many messages on this connection',
                   )
        self.push(random.choice(answers))

    def hard_bounce(self):
        """Return a soft bounce (4XX error code)."""
        answers = ('550 MAILBOX NOT FOUND',
                   "554 delivery error: we are simulating a user over quota.",
                   )
        self.push(random.choice(answers))

    def grumpy_bounce(self):
        """Return an error code to the sender in response to something other than
        rcpt to."""
        answers = ("599 I hate you.",
                   "534 Your face ugly.",
                   "420 Go away.",
                   "456 I'm grumpy right now.",
                   )
        self.push(random.choice(answers))
