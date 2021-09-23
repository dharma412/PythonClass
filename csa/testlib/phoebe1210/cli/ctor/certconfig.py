#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/certconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

"""
     IAF 2 CLI configurator - certconfig
"""

import clictorbase as ccb
from clictorbase import IafCliParamMap, REQUIRED, DEFAULT

from sal.containers.yesnodefault import YES, NO, is_yes
from sal.deprecated.expect import EXACT, REGEX
from sal.exceptions import TimeoutError

import re


class InvalidKeyCert(ccb.IafCliValueError): pass


class certconfig(ccb.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('certconfig')
        return self

    def certificate(self):
        self._query_response('CERTIFICATE')
        return certconfigCertificate(self._get_sess())

    def certauthority(self):
        self._query_response('CERTAUTHORITY')
        return certconfigCertauthority(self._get_sess())


class certconfigCertificate(ccb.IafCliConfiguratorBase):
    """
       certconfig -> CERTIFICATE
    """

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('key does not sign certificate', EXACT): InvalidKeyCert,
            ('Invalid certificate...discarding', EXACT): InvalidKeyCert,
            ('Invalid private key ...discarding', EXACT): InvalidKeyCert,
            ('Country should be a ISO two character country code', EXACT): ccb.IafCliValueError,
            ('the file .* does not exist.', REGEX): ccb.IafCliValueError,
            ('Certificate profile .* already exists.', REGEX): ccb.IafCliValueError,
        })

    def __call__(self):
        return self

    def new(self, input_dict=None, **kwargs):
        """
           certconfig -> CERTIFICATE -> NEW
        """
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['certificate_type'] = ['Create a self-signed SMIME certificate', DEFAULT, 1]
        param_map['name'] = ['name for this certificate profile', REQUIRED]
        param_map['common_name'] = ['Enter Common Name', REQUIRED]
        param_map['org'] = ['Enter Organization', REQUIRED]
        param_map['org_unit'] = ['Enter Organizational Unit', REQUIRED]
        param_map['city'] = ['Enter Locality or City', REQUIRED]
        param_map['state'] = ['Enter State', REQUIRED]
        param_map['country'] = ['Enter Country', REQUIRED]
        param_map['duration'] = ['Duration before expiration', DEFAULT]
        param_map['priv_key_size'] = ['size of private key', DEFAULT, 1]
        param_map['email_address'] = ['Enter email address', REQUIRED]
        param_map['dns'] = ['Enter the DNS you want to add', REQUIRED]
        param_map['another_dns'] = ['Add another member', DEFAULT, NO]
        param_map['view_CSR'] = ['view the CSR', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def import_cert(self, cert_name, filename, password):
        """
           certconfig -> CERTIFICATE -> IMPORT
        """
        self._query_response('IMPORT')
        self._query_response(cert_name)
        self._query_response(filename)
        self._expect(['Enter passphrase:', ], timeout=5)
        self._writeln(password)
        self._to_the_top(2)

    def paste(self, name, cert, key, cert_overwrite=False, inter_cert_list=None, remove_cert_list=None):
        """
           certconfig -> CERTIFICATE -> PASTE
        """
        self._query_response('PASTE')
        self._query_response(name)

        # check if name already exists
        try:
            self._query_response(timeout=5)
        except ccb.IafCliValueError, e:
            if cert_overwrite:
                self._writeln("Yes")
            else:
                raise e
        except TimeoutError, e:
            if self.getbuf().find("Paste public certificate in PEM format") != -1:
                pass
            else:
                raise e

        # Add Certificate
        self._sess_split(cert)
        self._sess.write("\n.\n")
        # Add Key
        self._expect([("Paste private key in PEM format", EXACT)], timeout=3)
        self._sess_split(key)
        self._sess.write("\n.\n")
        # Add intermediate certificate
        self._add_intermediate_cert(inter_cert_list, remove_cert_list)

    def _add_intermediate_cert(self, inter_cert_list=None, remove_cert_list=None):
        if inter_cert_list:
            for in_cert in inter_cert_list:
                self._query_response('Y')
                self._expect([("Paste intermediate certificate in PEM format", EXACT)], timeout=3)
                self._sess_split(in_cert)
                self._sess.write("\n.\n")
        self._query_response('N')
        if remove_cert_list:
            for cert_name in remove_cert_list:
                self._query_response('Y')
                self._query_select_list_item(cert_name)
        while 1:
            try:
                idx = self._query("Choose the operation", self._sub_prompt, timeout=5)
            except TimeoutError:
                self._writeln('N')
            if idx == 0:
                break
        self._to_the_top(2)

    def edit(self, name, update_cert=False, cert=None,
             inter_cert_list=None, remove_cert_list=None):
        """
           certconfig -> CERTIFICATE -> EDIT
        """
        self._query_response('EDIT')
        self._query_select_list_item(name)
        if update_cert:
            self._query_response('Y')
            # Add Certificate
            self._expect([("Paste public certificate in PEM format", EXACT)], timeout=3)
            self._sess_split(cert)
            self._sess.write("\n.\n")
        else:
            self._query_response('N')
        # Add intermediate certificate
        self._add_intermediate_cert(inter_cert_list, remove_cert_list)

    def delete(self, input_dict=None, **kwargs):
        """
           certconfig -> CERTIFICATE -> DELETE
        """
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['cert'] = ['certificate profile you wish to delete', DEFAULT, 1]
        param_map['confirm'] = ['you want to delete', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('DELETE')
        return self._process_input(param_map)

    def export_cert(self, cert_name, filename, password):
        """
           certconfig -> CERTIFICATE -> EXPORT
        """
        self._query_response('EXPORT')
        self._query_select_list_item(cert_name)
        self._query_response(filename)
        self._writeln(password)
        self._writeln(password)
        self._to_the_top(2)

    def print_cert(self):
        """
           certconfig -> CERTIFICATE -> PRINT
        """
        self._query_response('PRINT')
        raw = None
        try:
            raw = self._read_until('Choose the operation')
        finally:
            # return to the CLI prompt
            self._to_the_top(2)
        return raw

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


class certconfigCertauthority(ccb.IafCliConfiguratorBase):
    """
       certconfig -> CERTAUTHORITY
    """

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('key does not sign certificate', EXACT): InvalidKeyCert,
            ('Invalid certificate...discarding', EXACT): InvalidKeyCert,
            ('Could not read PEM data from file.', EXACT): ccb.IafCliValueError,
            ('the file \".*\" does not exist.', REGEX): ccb.IafCliValueError,
        })

    def custom(self):
        self._query_response('CUSTOM')
        return certconfigCustom(self._get_sess())

    def system(self):
        self._query_response('SYSTEM')
        return certconfigSystem(self._get_sess())


class certconfigCustom(ccb.IafCliConfiguratorBase):
    """
       certconfig -> CERTAUTHORITY -> CUSTOM
    """

    def enable(self):
        """
          certconfig -> CERTAUTHORITY -> CUSTOM -> ENABLE
        """
        self._query_response('ENABLE')
        self._to_the_top(3)

    def disable(self):
        """
          certconfig -> CERTAUTHORITY -> CUSTOM -> DISABLE
        """
        self._query_response('DISABLE')
        self._to_the_top(3)

    def print_cert(self):
        """
          certconfig -> CERTAUTHORITY -> CUSTOM -> PRINT
        """
        self._query_response('PRINT')
        raw = None
        try:
            raw = self._read_until('Choose the operation')
            # Strip off unwanted lines
            raw = raw.split('\r\n')
            raw = raw[4:len(raw)]
        finally:
            # return to the CLI prompt
            self._to_the_top(3)
        return raw

    def import_cert(self, filename):
        """
          certconfig -> CERTAUTHORITY -> CUSTOM -> IMPORT
        """
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(3)

    def export_cert(self, filename):
        """
          certconfig -> CERTAUTHORITY -> CUSTOM -> EXPORT
        """
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(3)


class certconfigSystem(ccb.IafCliConfiguratorBase):
    """
       certconfig -> CERTAUTHORITY -> SYSTEM
    """

    def enable(self):
        """
          certconfig -> CERTAUTHORITY -> SYSTEM -> ENABLE
        """
        self._query_response('ENABLE')
        self._to_the_top(3)

    def disable(self):
        """
          certconfig -> CERTAUTHORITY -> SYSTEM -> DISABLE
        """
        self._query_response('DISABLE')
        self._to_the_top(3)

    def print_cert(self):
        """
          certconfig -> CERTAUTHORITY -> SYSTEM -> PRINT
        """
        self._query_response('PRINT')
        raw = None
        try:
            raw = self._read_until('Choose the operation')
        finally:
            # return to the CLI prompt
            self._to_the_top(3)
        return raw

    def export_cert(self, filename):
        """
          certconfig -> CERTAUTHORITY -> SYSTEM -> EXPORT
        """
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(3)


if __name__ == '__main__':
    cert = """-----BEGIN CERTIFICATE-----
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

    key = """-----BEGIN RSA PRIVATE KEY-----
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

    cert_dict = {'name': 'mycert', 'common_name': 'somename',
                 'org': 'myorg', 'org_unit': 'myunit',
                 'city': 'mycity', 'state': 'mystate',
                 'country': 'IN',
                 }
    cc().certificate().new(input_dict=cert_dict)
    cc().certificate().edit(name='mycert', inter_cert_list=[inter_cert2, inter_cert1], remove_cert_list=[1])
    cc().certificate().paste(name='mycert', cert_overwrite=True, cert=cert, key=key)
    cc().certificate().export_cert(cert_name=1, filename='myfile.pem', password='ironport')
    cc().certificate().delete(cert='mycert', confirm='Y')
    cc().certificate().import_cert(cert_name=1, filename='myfile.pem', password='ironport')

    # certauthority functions
    cc().certauthority().custom().enable()
    cc().certauthority().custom().disable()
    cc().certauthority().custom().export_cert(filename='myfile')
    cc().certauthority().system().export_cert(filename='myfile')
    cc().certauthority().system().print_cert()
    cc().certauthority().custom().import_cert(filename='myfile')
