from datetime import datetime
import asyncore
import os
from smtpd import SMTPServer
from AtlasTestConstants import JENKINS_SERVER

class EmlServer(SMTPServer):
    no = 0

    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None,rcpt_options=None):
        filepath=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','smtp_mails', 'mails'))
        filename = '/MailReader.eml'
        filename = filepath + filename
        f = open(filename, 'wb')
        f.write(data)
        f.close
        print ("%s saved." % filename)
        self.no += 1


def run():
    foo = EmlServer((JENKINS_SERVER.jenkins_private_ipi, 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
