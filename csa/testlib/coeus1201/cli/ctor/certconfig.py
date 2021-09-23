#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/certconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
     IAF 2 CLI configurator - certconfig
"""

import clictorbase as ccb
from sal.containers.yesnodefault import YES, NO, is_yes
from sal.deprecated.expect import EXACT

import sys
import re

class InvalidKeyCert(ccb.IafCliValueError): pass

class certconfig(ccb.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('certconfig')
        return self

    def setup(self):
        self._query_response('SETUP')
        return certconfigSetup(self._get_sess())

    # We are not composing cluster methods at this time because we
    # cannot test them.
    def clusterset(self):
        pass

    def clustershow(self):
        pass

class certconfigSetup(ccb.IafCliConfiguratorBase):
    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('key does not sign certificate', EXACT) : InvalidKeyCert,
            ('Invalid certificate...discarding', EXACT) : InvalidKeyCert,
        })

    def _sess_split(self, send_string):
        """ Workaround for a CLI bug that doesn't allow this script to send in
            large amounts of text at once. We split it up by line, delay a
            split second, then flush the input buffer after each line. """

        import time

        send_array = send_string.split("\n")
        for line in send_array:
            self._writeln(line)
            time.sleep(0.1)
            self._read_until('\n')
        self._writeln('')

    def __call__(self, select_cert, intermediate, cert_list, passphrase = None):
        try:
            self.clearbuf()
            self._expect([("Do you want to continue?", EXACT)], timeout=3)
            self._query_response("Y")
            if select_cert != None:
                self._query_response(2)
                self._expect([(">", EXACT)], timeout=3)
                try:
                    self._select_list_item(select_cert, self.getbuf())
                except:
                    raise ValueError('No certificate in the name provided exists on WSA')
                finally:
                    self._to_the_top(newlines=1)
            else:
                self._query_response(1)
                self._enter_certs(intermediate, cert_list, passphrase)
                self._to_the_top(newlines=1)
                return self.getbuf()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.interrupt()
            raise exc_type, exc_value, exc_traceback

    def _enter_certs(self, intermediate, cert_list, passphrase):
        for cert_tup in cert_list:
            self._expect([("paste cert in PEM format", EXACT)], timeout=3)
            self._sess_split(cert_tup[0])
            self._sess.write("\n.\n")

            self._expect([("paste key in PEM format", EXACT)], timeout=3)
            self._sess_split(cert_tup[1])
            self._sess.write("\n.\n")
            if passphrase != None:
               self._expect([("Enter passphrase:", EXACT)], timeout=3)
               self._sess.writeln(passphrase)

            self._expect('intermediate', EXACT, timeout=3)
            self._query_response(intermediate)

            if is_yes(intermediate):
                assert len(cert_tup) == 3
                self._sess_split(cert_tup[2])
                self._sess.write("\n.\n")

if __name__ == '__main__':
    rsa_priv_key1 = """-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQC+tICwpV5jT3KOevEACdz9bI1j8gwTirsoKtuYqiwcO083Mi/E
Lb/qMGXMOgBvjowJdUSiQBEiLffEul4Y6aOdUCg02KiMX0mOILVpGNIA+T172ce+
dULXWh4zaqG08ltRHqhm7jXmrZNSVC37PaTwdTNoRQhqkBhDsoOiS75/swIDAQAB
AoGAayyH8j5NiGRazgX7sPjaEDZUU6nw7X6W5eEIHojsV0VhpHR48biAVX2ziA3E
tu0WeC5GTyTQPDQ3PYE7ZqbPQp4oSTrqZmlfP3oxE16FBy9cfKKOHJu7UNWs6c/v
TI+We1vaCoLKkWxcA07HYfWnD8kyr4r5abGyGfbknhpDm4ECQQDhC4IPS+EtkDWd
Nytr8De5XrCjr/t+Jqb5wN8R+dZvuPAzHUL7ZZuKVGMFbV9378E6LylIi3LTj2YW
vPt9s77zAkEA2O/JlVa8zw4BhBue93PyYX4xhlqa4cIY8h8uICq51uBGT4TlbaxO
9D/VcE4udXummXdGQIkVxQCAvZ1fIWHsQQJAOnxLKL6HntfDl0AnQL4FPV+meGPb
8EULUA0X7AwJ9q8Rfbc1GTCm46Rat6ZdEUZ16TEogXn8NY8m8PHcSibUkQJAUp4n
uG87IuPjoetfBECtG4IS3GcfO0FPfM5xI6EB+5qYTGqBcd5Ah3bUE5xCx01bKnEp
WSScHNXPMeeANldzwQJATowoDz+uyduOwn26xoJPKEOfWC0YP0HOATD4+lvo3NPi
8CYJlu3Sv8Lb4Du6sje09ub+ezqBx86HL3Heskte4g==
-----END RSA PRIVATE KEY-----"""

    rsa_cert1 = """-----BEGIN CERTIFICATE-----
MIIDojCCAwugAwIBAgIJAOdlR3oaxK5fMA0GCSqGSIb3DQEBBQUAMIGTMQswCQYD
VQQGEwJVUzETMBEGA1UECBMKY2FsaWZvcm5pYTESMBAGA1UEBxMJc2FuIGJydW5v
MQ4wDAYDVQQKEwVDaXNjbzERMA8GA1UECxMISXJvbnBvcnQxFTATBgNVBAMTDFdl
YiBzZWN1cml0eTEhMB8GCSqGSIb3DQEJARYScmFtaml5ZXJAY2lzY28uY29tMB4X
DTEyMDQwNTIzMDE0OVoXDTM5MDgyMjIzMDE0OVowgZMxCzAJBgNVBAYTAlVTMRMw
EQYDVQQIEwpjYWxpZm9ybmlhMRIwEAYDVQQHEwlzYW4gYnJ1bm8xDjAMBgNVBAoT
BUNpc2NvMREwDwYDVQQLEwhJcm9ucG9ydDEVMBMGA1UEAxMMV2ViIHNlY3VyaXR5
MSEwHwYJKoZIhvcNAQkBFhJyYW1qaXllckBjaXNjby5jb20wgZ8wDQYJKoZIhvcN
AQEBBQADgY0AMIGJAoGBAL60gLClXmNPco568QAJ3P1sjWPyDBOKuygq25iqLBw7
TzcyL8Qtv+owZcw6AG+OjAl1RKJAESIt98S6Xhjpo51QKDTYqIxfSY4gtWkY0gD5
PXvZx751QtdaHjNqobTyW1EeqGbuNeatk1JULfs9pPB1M2hFCGqQGEOyg6JLvn+z
AgMBAAGjgfswgfgwHQYDVR0OBBYEFG80wd/KatJHV3Z6INaeu4tjI2xJMIHIBgNV
HSMEgcAwgb2AFG80wd/KatJHV3Z6INaeu4tjI2xJoYGZpIGWMIGTMQswCQYDVQQG
EwJVUzETMBEGA1UECBMKY2FsaWZvcm5pYTESMBAGA1UEBxMJc2FuIGJydW5vMQ4w
DAYDVQQKEwVDaXNjbzERMA8GA1UECxMISXJvbnBvcnQxFTATBgNVBAMTDFdlYiBz
ZWN1cml0eTEhMB8GCSqGSIb3DQEJARYScmFtaml5ZXJAY2lzY28uY29tggkA52VH
ehrErl8wDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOBgQCnqaann3dXPwhE
SUJmDbOn12G2w0kzj/HBMM/aliut+PQ0wmudOxAQ1CcYje90ZhB9XsQNuIAH50cw
NvqLYGK6OgnPODTRqrehis75+giMZZPenKYgkvaRXlj/6MRmuJ/0zjA6px/D9ohI
zpKGxq6VWOc8J1+azRYroUX2UTrUqQ==
-----END CERTIFICATE-----"""

    inter_cert1 = """-----BEGIN CERTIFICATE-----
MIIDojCCAwugAwIBAgIJAOdlR3oaxK5fMA0GCSqGSIb3DQEBBQUAMIGTMQswCQYD
VQQGEwJVUzETMBEGA1UECBMKY2FsaWZvcm5pYTESMBAGA1UEBxMJc2FuIGJydW5v
MQ4wDAYDVQQKEwVDaXNjbzERMA8GA1UECxMISXJvbnBvcnQxFTATBgNVBAMTDFdl
YiBzZWN1cml0eTEhMB8GCSqGSIb3DQEJARYScmFtaml5ZXJAY2lzY28uY29tMB4X
DTEyMDQwNTIzMDE0OVoXDTM5MDgyMjIzMDE0OVowgZMxCzAJBgNVBAYTAlVTMRMw
EQYDVQQIEwpjYWxpZm9ybmlhMRIwEAYDVQQHEwlzYW4gYnJ1bm8xDjAMBgNVBAoT
BUNpc2NvMREwDwYDVQQLEwhJcm9ucG9ydDEVMBMGA1UEAxMMV2ViIHNlY3VyaXR5
MSEwHwYJKoZIhvcNAQkBFhJyYW1qaXllckBjaXNjby5jb20wgZ8wDQYJKoZIhvcN
AQEBBQADgY0AMIGJAoGBAL60gLClXmNPco568QAJ3P1sjWPyDBOKuygq25iqLBw7
TzcyL8Qtv+owZcw6AG+OjAl1RKJAESIt98S6Xhjpo51QKDTYqIxfSY4gtWkY0gD5
PXvZx751QtdaHjNqobTyW1EeqGbuNeatk1JULfs9pPB1M2hFCGqQGEOyg6JLvn+z
AgMBAAGjgfswgfgwHQYDVR0OBBYEFG80wd/KatJHV3Z6INaeu4tjI2xJMIHIBgNV
HSMEgcAwgb2AFG80wd/KatJHV3Z6INaeu4tjI2xJoYGZpIGWMIGTMQswCQYDVQQG
EwJVUzETMBEGA1UECBMKY2FsaWZvcm5pYTESMBAGA1UEBxMJc2FuIGJydW5vMQ4w
DAYDVQQKEwVDaXNjbzERMA8GA1UECxMISXJvbnBvcnQxFTATBgNVBAMTDFdlYiBz
ZWN1cml0eTEhMB8GCSqGSIb3DQEJARYScmFtaml5ZXJAY2lzY28uY29tggkA52VH
ehrErl8wDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOBgQCnqaann3dXPwhE
SUJmDbOn12G2w0kzj/HBMM/aliut+PQ0wmudOxAQ1CcYje90ZhB9XsQNuIAH50cw
NvqLYGK6OgnPODTRqrehis75+giMZZPenKYgkvaRXlj/6MRmuJ/0zjA6px/D9ohI
zpKGxq6VWOc8J1+azRYroUX2UTrUqQ==
-----END CERTIFICATE-----"""

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    cc = certconfig(cli_sess)

    try:
        certconfig(cli_sess)().setup()(intermediate=YES,
            cert_list=[('a', 'b', 'c')])
    except InvalidKeyCert, ikc:
        print "Caught InvalidKeyCert error, just as we expected!"
        cli_sess.interrupt_writeln()
    else:
        raise "Did not catch InvalidKeyCert error. What happened?"

    cc().setup()(intermediate=YES,
         cert_list=[(rsa_cert1, rsa_priv_key1, inter_cert1)])
