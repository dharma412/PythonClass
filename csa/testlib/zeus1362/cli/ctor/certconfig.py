#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/certconfig.py#3 $
# $DateTime: 2020/06/30 21:10:18 $
# $Author: mrmohank $
"""
     IAF 2 CLI configurator - certconfig
"""

import clictorbase as ccb
from sal.containers.yesnodefault import YES, NO, is_yes
from sal.deprecated.expect import EXACT

import re

class InvalidKeyCert(ccb.IafCliValueError): pass

class certconfig(ccb.IafCliConfiguratorBase):
    def __call__(self,option=None):
        self._restart()
        if option != None:
            self._writeln(self.__class__.__name__)
            certconfig = self._read_until('>')
            return certconfig
        else:
            self._writeln(self.__class__.__name__)
            return self

    def certificate(self):
        self._query_response('CERTIFICATE')
        return CertificateConfig(self._get_sess())

    # We are not composing cluster methods at this time because we
    # cannot test them.
    def clusterset(self):
        pass

    def clustershow(self):
        pass

class CertificateConfig(ccb.IafCliConfiguratorBase):

    newlines = 1

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)

    def setup(self):
        self._query_response('SETUP')
        return certconfigSetup(self._get_sess())

    def print_certificates(self):
        """Prints and returns the raw input information"""
        self._query_response('PRINT')
        raw = None
        try:
            raw = self._read_until('Choose the operation')
            if not re.search('BEGIN CERTIFICATE', raw, re.MULTILINE):
                #Detected no certificates
                raw =  None
        finally:
            # return to the CLI prompt
            self._to_the_top(1)
        return raw

    def clear_certificates(self, clear=None):
        """Clears the existing certificates if there are certificates available"""
        self._query_response('CLEAR')
        self._read_until('clear all existing certificates')
        if clear:
            self._query_response(clear)
            self._read_until('Choose the operation')

        self._to_the_top(2)

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

    def __call__(self, one_cert, replace, intermediate, cert_list):
        # Are we entering one certificate for all, or individual certs for
        # each service?
        self._query_response(one_cert)
        # Get the current state of certs. If same_cert is 'N', then there are
        # currently 4 unique certs defined. If same_cert is 'Y', then there is
        # only one cert defined.
        same_cert = self._get_last_default()
        # If we are switching from multiple certs to a single cert, the CLI
        # prints an "are you sure?" message. Respond to it if necessary
        if one_cert and not same_cert:
            self._query_response(replace)
            # If we said to replace certs, enter them
            if replace:
                self._enter_certs(intermediate, cert_list)
        else:
            # verify that the test writer passed in the correct number of
            # certificates
            if is_yes(one_cert):
                assert len(cert_list) == 1
            else:
                assert len(cert_list) == 4
            # If that passes, enter certs
            self._enter_certs(intermediate, cert_list)

    def _enter_certs(self, intermediate, cert_list):
        expect_list = ('Inbound:', 'Outbound:', 'HTTPS', 'LDAPS')
        for cert_tup in cert_list:
            if len(cert_list) > 1:
                self._expect([(x, EXACT) for x in expect_list])
            self._sess_split(cert_tup[0])
            self._sess.write("\n.\n")

            self._expect([("paste key in PEM format", EXACT)], timeout=3)
            self._sess_split(cert_tup[1])
            self._sess.write("\n.\n")

            self._expect('intermediate', EXACT, timeout=3)
            self._query_response(intermediate)

            [self._sess.write("\n") for _ in range(3)]

            if is_yes(intermediate):
                assert len(cert_tup) == 3
                self._sess_split(cert_tup[2])
                self._sess.write("\n.\n")

if __name__ == '__main__':
    rsa_priv_key1 = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQC/Odq2HhzUqK7HVJSihBZjOCBb8XPH9KeYF2lOxFZdfNRm0h4P
HkT7NDHoi6GxD+De1UYpe6ZGjd3rAp4yPAHY7QPxF+Kqi596nZf+Wz7UMWKYzjcm
oETjMDfI/wQswvUQqcR1125+0kMlHMrllTAEUeWRLhUBXbDWTYXps8rTHQIDAQAB
AoGAFhILWDGpijHd2ku8y/UK0HDN60622kE2hqtNEDZA8ZFSwntF1ODdfVDM4dYb
11/JyG49JtSKoGIHVvR6ZbnfTIK6D+qkf5b+Ajx6NLxnV6ET5Fy3o3OazxWMOjdf
9vvt1WSTWnusLqMTo6QPViXN31zR7xz/rEQpu48N9AUTVtECQQD6AY/8Reb/IWDR
oVPKHWxJ3mtl/sOMdX4T3V2cxHCnxiLd0hI8E+hHbmE6cWRd4U9BmFGAgCjNNSqx
lVT/MKqfAkEAw8+F6CeWFDkEL/401cO5HfRbakA7tT1dycu9KmY82rc1vH0MUijT
fM9kuTqy/x/2XDR6D+gyMLP/PwTrPrWkwwJBANYNYGpur0jiGzNhHYx/hKf6d5ns
dyFbt4bqkawXxRzg2Bl0M4icwtPl/fk7/OMkdeeDssSC9mw8iUFiylN0J6ECQBI+
UYGRvp/fuA4opw+LjsHFtIavuWBneUeF3fgHUoAmNbF8DRvShfHI+N9xIqA2gCOT
GBRHU/XJr2xVrv1GuzUCQBT8CxPC/owgK29yuRrETK5FtSV9mNW9hq5vUZeY9qSA
xJ8UzqNLYBZazM75/O0253xzrDHmzV3s/rZNkBC5yUo=
-----END RSA PRIVATE KEY-----"""

    rsa_priv_key2 = """-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQDYUYkG/dLfTg5x1uExVAkC1jt5hJynu877nkxahGt9U3Lr6EC2
uoO0CvTAtkkp22Jd+64T/HYWYpUxKzp1Eq6xd7VcjeqhIPxI0RYvlC0NS4QJKhvZ
RiwB2ubVJeJInS0ITD96IbjrdEuL2cs0JYoHIkqcGWAFSM2OJorT/NzbuQIDAQAB
AoGABdADD5YIcYmmZ7avbGTmrRXWmUhP8U3hnO8++/us67wvTVl7S62tVkwpEXiU
dLR5ay8VGWJiRe22NpEDzBuJaBy6X4if9jBdywEo7h0JTXZY8Znu9zDvonbJQMC3
yHYY8aba4LJMJxKswPI82Aykh2imBf2lIykhVRt8gewenFECQQDvMM0T9MQV6Ry0
LvcZkqTw3ZvUWkI/xGPT8J1pVwjQlmPbXmIrJPi/MlMFvqBvqBN/3nwxsMQH7v+c
Czb++d0tAkEA54U/0BgNjL/R/Ti8C5+2wq1pkrrifMNJ8OgJzZ6z9/7pFfHgZ9g4
Ey3rfd/CvYDV8+nHRr09JOLiJ/4HBajIPQJAGJhpDhtGKoac9/44VH3azhXLl0ts
sofsR/ffB9z2QBSm0gDjkVIs7eQr21RdxP2Ae86R8L4fej1eNVqF3jQtRQJAcooq
yuHLelHAKt3xsnJ+sYunim8o8/6Ny0CQ8QhOEygq2q+CjP2cqGh0dB7KsoRV1UlY
THf9Ew2oQ47anIMnJQJABWEahr4cL1Ipsnzd49Q0TSPFE0d86+8GRCDwiTq/V2qo
zy8ksTS2m4uE5A4bG0vJHjNh4Lh2mUFnCnOfvisJMg==
-----END RSA PRIVATE KEY-----"""

    rsa_cert1 = """-----BEGIN CERTIFICATE-----
MIIDsjCCAxugAwIBAgIBATANBgkqhkiG9w0BAQQFADCBkzELMAkGA1UEBhMCVVMx
EzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVNhbiBCcnVubzEZMBcGA1UE
ChMQSXJvbnBvcnQgU3lzdGVtczELMAkGA1UECxMCUUExDTALBgNVBAMTBG1hdHQx
JDAiBgkqhkiG9w0BCQEWFW1saXNpdHphQGlyb25wb3J0LmNvbTAeFw0wMzA0MTcy
MTQxNTlaFw0wNDA0MTYyMTQxNTlaMIGGMQswCQYDVQQGEwJVUzETMBEGA1UECBMK
Q2FsaWZvcm5pYTESMBAGA1UEBxMJU2FuIEJydW5vMRkwFwYDVQQKExBJcm9ucG9y
dCBTeXN0ZW1zMQ0wCwYDVQQDEwRtYXR0MSQwIgYJKoZIhvcNAQkBFhVtbGlzaXR6
YUBpcm9ucG9ydC5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAL852rYe
HNSorsdUlKKEFmM4IFvxc8f0p5gXaU7EVl181GbSHg8eRPs0MeiLobEP4N7VRil7
pkaN3esCnjI8AdjtA/EX4qqLn3qdl/5bPtQxYpjONyagROMwN8j/BCzC9RCpxHXX
bn7SQyUcyuWVMARR5ZEuFQFdsNZNhemzytMdAgMBAAGjggEfMIIBGzAJBgNVHRME
AjAAMCwGCWCGSAGG+EIBDQQfFh1PcGVuU1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0
ZTAdBgNVHQ4EFgQUDAkbYX2t3XCV3PjkXAoM87VSsuEwgcAGA1UdIwSBuDCBtYAU
sBKk8MEydJl5VTAvfTEv/6KfL9mhgZmkgZYwgZMxCzAJBgNVBAYTAlVTMRMwEQYD
VQQIEwpDYWxpZm9ybmlhMRIwEAYDVQQHEwlTYW4gQnJ1bm8xGTAXBgNVBAoTEEly
b25wb3J0IFN5c3RlbXMxCzAJBgNVBAsTAlFBMQ0wCwYDVQQDEwRtYXR0MSQwIgYJ
KoZIhvcNAQkBFhVtbGlzaXR6YUBpcm9ucG9ydC5jb22CAQAwDQYJKoZIhvcNAQEE
BQADgYEAxybkwrA2ln4lelV0TWPdiDfgW5MhsNpeENHWFq6O8GGXlFuaqIYhjn2C
ueaswrjPR/3iipfme5nTcmESOkBDzQhSpW76KdtBjgqb9ZKzyK6AiwYuxUcSWv5Z
f0SG0zDkDDVK4IRx/iaeDXnGeRvpH9cbP/4fNLu8iPJTFdmLRU4=
-----END CERTIFICATE-----"""

    rsa_cert2 = """-----BEGIN CERTIFICATE-----
MIIDuzCCAySgAwIBAgIBATANBgkqhkiG9w0BAQQFADCBkTELMAkGA1UEBhMCVVMx
EzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVNhbiBCcnVubzEZMBcGA1UE
ChMQSXJvbnBvcnQgU3lzdGVtczELMAkGA1UECxMCUUExCzAJBgNVBAMTAlFBMSQw
IgYJKoZIhvcNAQkBFhVtbGlzaXR6YUBpcm9ucG9ydC5jb20wHhcNMDMwNDIxMTkx
NTQ0WhcNMDQwNDIwMTkxNTQ0WjCBkzELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNh
bGlmb3JuaWExFjAUBgNVBAcTDVNhbiBGcmFuY2lzY28xETAPBgNVBAoTCElyb25w
b3J0MQswCQYDVQQLEwJRQTERMA8GA1UEAxMIbWxpc2l0emExJDAiBgkqhkiG9w0B
CQEWFW1saXNpdHphQGlyb25wb3J0LmNvbTCBnzANBgkqhkiG9w0BAQEFAAOBjQAw
gYkCgYEA2FGJBv3S304OcdbhMVQJAtY7eYScp7vO+55MWoRrfVNy6+hAtrqDtAr0
wLZJKdtiXfuuE/x2FmKVMSs6dRKusXe1XI3qoSD8SNEWL5QtDUuECSob2UYsAdrm
1SXiSJ0tCEw/eiG463RLi9nLNCWKByJKnBlgBUjNjiaK0/zc27kCAwEAAaOCAR0w
ggEZMAkGA1UdEwQCMAAwLAYJYIZIAYb4QgENBB8WHU9wZW5TU0wgR2VuZXJhdGVk
IENlcnRpZmljYXRlMB0GA1UdDgQWBBR0EW0HUTzhHNF5I+2Lw32XfuyrYjCBvgYD
VR0jBIG2MIGzgBQnwUZ3epVTvYL2ERCdmooixITiyKGBl6SBlDCBkTELMAkGA1UE
BhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVNhbiBCcnVubzEZ
MBcGA1UEChMQSXJvbnBvcnQgU3lzdGVtczELMAkGA1UECxMCUUExCzAJBgNVBAMT
AlFBMSQwIgYJKoZIhvcNAQkBFhVtbGlzaXR6YUBpcm9ucG9ydC5jb22CAQAwDQYJ
KoZIhvcNAQEEBQADgYEAIdFeoJSCVgc13Gv/KGmE/HKb2yUhfJfJHI/k95i644Px
EWnpDtcxaw991+lCt+eAVKoMYkNjHK5Uy7xWQaZ+ny9J6lJq6WdWB6EFs+kTMe1H
jZmFbdJujLxqsoXKZ1izZs2wciRfDzoT5xvuCVKeu+AcC1Ajp/ltYZ+Pjr6/l9E=
-----END CERTIFICATE-----"""

    inter_cert1 = """-----BEGIN CERTIFICATE-----
MIIDsjCCAxugAwIBAgIBATANBgkqhkiG9w0BAQQFADCBkzELMAkGA1UEBhMCVVMx
EzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVNhbiBCcnVubzEZMBcGA1UE
ChMQSXJvbnBvcnQgU3lzdGVtczELMAkGA1UECxMCUUExDTALBgNVBAMTBG1hdHQx
JDAiBgkqhkiG9w0BCQEWFW1saXNpdHphQGlyb25wb3J0LmNvbTAeFw0wMzA0MTcy
MTQxNTlaFw0wNDA0MTYyMTQxNTlaMIGGMQswCQYDVQQGEwJVUzETMBEGA1UECBMK
Q2FsaWZvcm5pYTESMBAGA1UEBxMJU2FuIEJydW5vMRkwFwYDVQQKExBJcm9ucG9y
dCBTeXN0ZW1zMQ0wCwYDVQQDEwRtYXR0MSQwIgYJKoZIhvcNAQkBFhVtbGlzaXR6
YUBpcm9ucG9ydC5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAL852rYe
HNSorsdUlKKEFmM4IFvxc8f0p5gXaU7EVl181GbSHg8eRPs0MeiLobEP4N7VRil7
pkaN3esCnjI8AdjtA/EX4qqLn3qdl/5bPtQxYpjONyagROMwN8j/BCzC9RCpxHXX
bn7SQyUcyuWVMARR5ZEuFQFdsNZNhemzytMdAgMBAAGjggEfMIIBGzAJBgNVHRME
AjAAMCwGCWCGSAGG+EIBDQQfFh1PcGVuU1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0
ZTAdBgNVHQ4EFgQUDAkbYX2t3XCV3PjkXAoM87VSsuEwgcAGA1UdIwSBuDCBtYAU
sBKk8MEydJl5VTAvfTEv/6KfL9mhgZmkgZYwgZMxCzAJBgNVBAYTAlVTMRMwEQYD
VQQIEwpDYWxpZm9ybmlhMRIwEAYDVQQHEwlTYW4gQnJ1bm8xGTAXBgNVBAoTEEly
b25wb3J0IFN5c3RlbXMxCzAJBgNVBAsTAlFBMQ0wCwYDVQQDEwRtYXR0MSQwIgYJ
KoZIhvcNAQkBFhVtbGlzaXR6YUBpcm9ucG9ydC5jb22CAQAwDQYJKoZIhvcNAQEE
BQADgYEAxybkwrA2ln4lelV0TWPdiDfgW5MhsNpeENHWFq6O8GGXlFuaqIYhjn2C
ueaswrjPR/3iipfme5nTcmESOkBDzQhSpW76KdtBjgqb9ZKzyK6AiwYuxUcSWv5Z
f0SG0zDkDDVK4IRx/iaeDXnGeRvpH9cbP/4fNLu8iPJTFdmLRU4=
-----END CERTIFICATE-----"""

    inter_cert2 = """-----BEGIN CERTIFICATE-----
MIIDuzCCAySgAwIBAgIBATANBgkqhkiG9w0BAQQFADCBkTELMAkGA1UEBhMCVVMx
EzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVNhbiBCcnVubzEZMBcGA1UE
ChMQSXJvbnBvcnQgU3lzdGVtczELMAkGA1UECxMCUUExCzAJBgNVBAMTAlFBMSQw
IgYJKoZIhvcNAQkBFhVtbGlzaXR6YUBpcm9ucG9ydC5jb20wHhcNMDMwNDIxMTkx
NTQ0WhcNMDQwNDIwMTkxNTQ0WjCBkzELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNh
bGlmb3JuaWExFjAUBgNVBAcTDVNhbiBGcmFuY2lzY28xETAPBgNVBAoTCElyb25w
b3J0MQswCQYDVQQLEwJRQTERMA8GA1UEAxMIbWxpc2l0emExJDAiBgkqhkiG9w0B
CQEWFW1saXNpdHphQGlyb25wb3J0LmNvbTCBnzANBgkqhkiG9w0BAQEFAAOBjQAw
gYkCgYEA2FGJBv3S304OcdbhMVQJAtY7eYScp7vO+55MWoRrfVNy6+hAtrqDtAr0
wLZJKdtiXfuuE/x2FmKVMSs6dRKusXe1XI3qoSD8SNEWL5QtDUuECSob2UYsAdrm
1SXiSJ0tCEw/eiG463RLi9nLNCWKByJKnBlgBUjNjiaK0/zc27kCAwEAAaOCAR0w
ggEZMAkGA1UdEwQCMAAwLAYJYIZIAYb4QgENBB8WHU9wZW5TU0wgR2VuZXJhdGVk
IENlcnRpZmljYXRlMB0GA1UdDgQWBBR0EW0HUTzhHNF5I+2Lw32XfuyrYjCBvgYD
VR0jBIG2MIGzgBQnwUZ3epVTvYL2ERCdmooixITiyKGBl6SBlDCBkTELMAkGA1UE
BhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVNhbiBCcnVubzEZ
MBcGA1UEChMQSXJvbnBvcnQgU3lzdGVtczELMAkGA1UECxMCUUExCzAJBgNVBAMT
AlFBMSQwIgYJKoZIhvcNAQkBFhVtbGlzaXR6YUBpcm9ucG9ydC5jb22CAQAwDQYJ
KoZIhvcNAQEEBQADgYEAIdFeoJSCVgc13Gv/KGmE/HKb2yUhfJfJHI/k95i644Px
EWnpDtcxaw991+lCt+eAVKoMYkNjHK5Uy7xWQaZ+ny9J6lJq6WdWB6EFs+kTMe1H
jZmFbdJujLxqsoXKZ1izZs2wciRfDzoT5xvuCVKeu+AcC1Ajp/ltYZ+Pjr6/l9E=
-----END CERTIFICATE-----"""

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    cc = certconfig(cli_sess)

    try:
        certconfig(cli_sess)().setup()(one_cert=YES,
            replace=YES,
            intermediate=YES,
            cert_list=[('a', 'b', 'c')])
    except InvalidKeyCert, ikc:
        print 'Caught InvalidKeyCert error, just as we expected!'
        cli_sess.interrupt_writeln()
    else:
        raise Exception('Did not catch InvalidKeyCert error. What happened?')

    cc().setup()(one_cert=YES,
        replace=YES,
        intermediate=YES,
        cert_list=[(rsa_cert1, rsa_priv_key1, inter_cert1)])

    # Validating print_certificates() method
    certs_raw = cc().print_certificates()
    certs_raw = re.sub(r'\r\n', '\n', certs_raw)
    print certs_raw
    expr = re.compile(r'(-+BEGIN CERTIFICATE-+.*?-+END CERTIFICATE-+)',
        re.DOTALL)
    certs = expr.findall(certs_raw)
    if not (rsa_cert1 in certs and inter_cert1 in certs):
        raise Exception("Certificates didn't print")

    cc().setup()(one_cert=YES,
       replace=NO,
       intermediate=NO,
       cert_list=[(rsa_cert2, rsa_priv_key2)])

    cc().setup()(one_cert=NO,
       replace=YES,
       intermediate=NO,
       cert_list=[(rsa_cert1, rsa_priv_key1), (rsa_cert2, rsa_priv_key2),
                  (rsa_cert1, rsa_priv_key1),(rsa_cert2, rsa_priv_key2)])
