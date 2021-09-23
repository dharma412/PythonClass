import secure_smtpd
import smtpdlib
# smtpd library customized to support v6

import ssl, asyncore, socket, logging, signal, time, sys

from .smtp_channel import SMTPChannel
from asyncore import ExitNow
from .process_pool import ProcessPool
from ssl import SSLError

try:
    from Queue import Empty
except ImportError:
    # We're on python3
    from queue import Empty


class SMTPServer(smtpdlib.SMTPServer):

    def __init__(self, localaddr, remoteaddr, ssl=False, \
                 certfile=None, tls=False, \
                 keyfile=None, ssl_version=ssl.PROTOCOL_SSLv23, \
                 require_authentication=False, credential_validator=None, \
                 maximum_execution_time=30, process_count=10, ssl_ctx=None, \
                 soft_bounce=0.0, hard_bounce=0.0, smtp_auth_succeed_perc=1.0, debug=False):
        smtpdlib.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.logger = logging.getLogger(secure_smtpd.LOG_NAME)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
        self.subprocesses = []
        self.require_authentication = require_authentication
        self.credential_validator = credential_validator
        self.ssl = ssl
        self.ssl_ctx = ssl_ctx
        self.starttls = tls
        self.maximum_execution_time = maximum_execution_time
        self.process_count = process_count
        self.process_pool = None
        self.msg_count = 0
        self.soft_bounce_perc = soft_bounce
        self.hard_bounce_perc = hard_bounce
        self.server_channel = {}
        self.debug = debug
        self.smtp_auth_succeed_perc = smtp_auth_succeed_perc

    def handle_accept(self):
        self.process_pool = ProcessPool(self._accept_subprocess, process_count=self.process_count)
        self.close()

    def _accept_subprocess(self, queue):
        while True:
            try:
                self.socket.setblocking(1)
                pair = self.accept()
                map = {}

                if pair is not None:
                    newsocket, fromaddr = pair
                    newsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    newsocket.settimeout(self.maximum_execution_time)

                    if self.ssl_ctx and not self.starttls:
                        newsocket = self.ssl_ctx.wrap_socket(
                            newsocket,
                            server_side=True)
                        print >> smtpdlib.DEBUGSTREAM, \
                            'Peer: %s - negotiated TLS: \
                            %s' % (repr(fromaddr), repr(newsocket.cipher()))
                    if self.ssl:
                        newsocket = ssl.wrap_socket(
                            newsocket,
                            server_side=True,
                            certfile=self.certfile,
                            keyfile=self.keyfile,
                            ssl_version=self.ssl_version,
                        )
                    self.server_channel = SMTPChannel(
                        self,
                        newsocket,
                        fromaddr,
                        require_authentication=self.require_authentication,
                        credential_validator=self.credential_validator,
                        map=map,
                        smtp_auth_succeed_perc=self.smtp_auth_succeed_perc,
                        debug=self.debug
                    )
                    self.server_channel.soft_bounce_percent = self.soft_bounce_perc
                    self.server_channel.hard_bounce_percent = self.hard_bounce_perc
                    if self.debug:
                        print "Channel:", self.server_channel.hard_bounce_percent, self.server_channel.soft_bounce_percent, self.smtp_auth_succeed_perc
                    asyncore.loop(map=map)

            except (ExitNow, SSLError):
                self._shutdown_socket(newsocket)
                # self.logger.info('_accept_subprocess(): smtp channel terminated asyncore.')
            except Exception as e:
                self._shutdown_socket(newsocket)
                # self.logger.error('_accept_subprocess(): uncaught exception: %s' % str(e))
            # except KeyboardInterrupt:
            # pass

    def _shutdown_socket(self, s):
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except Exception as e:
            self.logger.error('_shutdown_socket(): failed to cleanly shutdown socket: %s' % str(e))

    def run(self):
        try:
            asyncore.loop()
            if hasattr(signal, 'SIGTERM'):
                def sig_handler(signal, frame):
                    sys.exit(0)

                signal.signal(signal.SIGTERM, sig_handler)
            while 1:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
