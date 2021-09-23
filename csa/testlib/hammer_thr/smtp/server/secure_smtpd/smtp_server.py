import secure_smtpd
import smtpdlib
# smtpd library customized to support v6

import ssl, asyncore, socket
import signal, time, sys
import threading
import Queue

from .smtp_channel import SMTPChannel
from asyncore import ExitNow
from ssl import SSLError

MAIL_QUEUE = Queue.Queue(120 * 120)


class SMTPServer(smtpdlib.SMTPServer):

    def __init__(self, localaddr, remoteaddr, ssl=False, \
                 certfile=None, tls=False, \
                 keyfile=None, ssl_version=ssl.PROTOCOL_SSLv23, \
                 require_authentication=False, credential_validator=None, \
                 maximum_execution_time=30, process_count=1, ssl_ctx=None, \
                 soft_bounce=0.0, hard_bounce=0.0, debug=False):
        smtpdlib.SMTPServer.__init__(self, localaddr, remoteaddr)
        # self.logger = logging.getLogger(secure_smtpd.LOG_NAME )
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
        self.start_parallel_connections()

    def start_parallel_connections(self):
        print "starting server in daemon mode..."
        threads = []
        for connection in range(int(400)):
            t = threading.Thread(target=self.process_queue_mails)
            threads.append(t)
        t = threading.Thread(target=self.queue_incoming_connections)
        threads.append(t)
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()

    def process_queue_mails(self):
        while True:
            try:
                # print "Q-SIZE:%d \n " %(MAIL_QUEUE.qsize())
                if not MAIL_QUEUE.empty():
                    pair = MAIL_QUEUE.get()
                    map = {}
                    if pair is not None:
                        newsocket, fromaddr = pair
                        newsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        newsocket.settimeout(self.maximum_execution_time)
                        if self.ssl_ctx and not self.starttls:
                            newsocket = self.ssl_ctx.wrap_socket(newsocket, server_side=True)
                            print >> smtpdlib.DEBUGSTREAM, 'Peer: %s - negotiated TLS: \
                            %s' % (repr(fromaddr), repr(newsocket.cipher()))
                        if self.ssl:
                            newsocket = ssl.wrap_socket(newsocket, server_side=True, \
                                                        certfile=self.certfile, keyfile=self.keyfile, \
                                                        ssl_version=self.ssl_version)

                        self.server_channel = SMTPChannel(self, newsocket, fromaddr, \
                                                          require_authentication=self.require_authentication,
                                                          credential_validator=self.credential_validator,
                                                          map=map)
                        self.server_channel.soft_bounce_percent = self.soft_bounce_perc
                        self.server_channel.hard_bounce_percent = self.hard_bounce_perc
                        asyncore.loop(map=map, use_poll=True)
            except (ExitNow, SSLError):
                self._shutdown_socket(newsocket)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                self._shutdown_socket(newsocket)
                print "ERROR Incoming Connection:", e

    def queue_incoming_connections(self):
        while True:
            try:
                self.socket.setblocking(1)
                pair = self.accept()
                MAIL_QUEUE.put(pair)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print "ERROR Connection:", e

    def handle_accept(self):
        print 'ACCEPT.'

    # __accept subprocess is absolute handled threaded connection
    def _accept_subprocess(self):
        while True:
            try:
                self.socket.setblocking(1)
                pair = self.accept()
                map = {}
                MAIL_QUEUE.put([pair])

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
                        map=map
                    )
                    self.server_channel.soft_bounce_percent = self.soft_bounce_perc
                    self.server_channel.hard_bounce_percent = self.hard_bounce_perc
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
            print >> smtpdlib.DEBUGSTREAM, '_shutdown_socket(): \
            failed to cleanly shutdown socket: %s' % str(e)

    def run(self):
        try:
            asyncore.loop(use_poll=True)
            if hasattr(signal, 'SIGTERM'):
                def sig_handler(signal, frame):
                    sys.exit(0)

                signal.signal(signal.SIGTERM, sig_handler)
            while 1:
                time.sleep(0.25)
        except KeyboardInterrupt:
            pass
