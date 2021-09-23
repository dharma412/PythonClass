#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/cert_config.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions
from sal.containers.yesnodefault import YES, NO, is_yes


class CertConfig(CliKeywordBase):
    """Configure cryptographic certificates by entering certificate and
    private key in PEM format.
    """

    def get_keyword_names(self):
        return ['cert_config_setup', ]

    def cert_config_setup(self,
                          rsa_cert,
                          rsa_key,
                          one_cert='yes',
                          replace='yes',
                          intermediate='yes',
                          intermediate_cert=None,
                          rsa_cert_outbound=None,
                          rsa_key_outbound=None,
                          rsa_cert_https=None,
                          rsa_key_https=None,
                          rsa_cert_ldap=None,
                          rsa_key_ldap=None):

        """Cert Config Setup.

        certconfig > setup

        Configure security certificate and key.

        Parameters:
        - `rsa_cert`: RSA certificate in PEM format. In case 'one_cert' is NO,
          it will be Inbound certificate.
        - `rsa_key`: RSA certificate key in PEM format. In case 'one_cert' is
          NO, it will be Inbound certificate key.
        - `one_cert`: Either YES or NO values. In case one certificate/key for
          receiving, delivery, https management access, and LDAPS should be used.
        - `replace`: Either YES or NO values.
        - `rsa_cert_outbound`: RSA certificate for Outbound in PEM format.
          None, by default. Available only if 'one_cert' is NO.
        - `rsa_key_outbound`: RSA certificate key for Outbound in PEM format.
          None, by default. Available only if 'one_cert' is NO.
        - `rsa_cert_https`: RSA certificate for https in PEM format. None, by
          default. Available only if 'one_cert' is NO.
        - `rsa_key_https`: RSA certificate key for https in PEM format. None, by
          default. Available only if 'one_cert' is NO.
        - `rsa_cert_ldap`: RSA certificate for ldap in PEM format. None, by
          default. Available only if 'one_cert' is NO.
        - `rsa_key_ldap`: RSA certificate key for ldap in PEM format. None, by
          default. Available only if 'one_cert' is NO.
        - `intermediate`: either 'Yes' if an intermediate certificate should be
        added or 'No' if not.
        - `intermediate_cert`: RSA intermediate certificate in PEM format.


        NOTE: Extra delimiters \'\\n\' should be added into certificates strings
        to split them in ~80 characters chunks. This is kind of workaround for a
        CLI bug that doesn't allow this script to send in large amounts of text
        at once.

        Examples:

        | Cert Config Setup | sma_cert | sma_key |intermediate=yes | intermediate_cert=c |
        | Cert Config Setup | sma_cert | sma_key | intermediate=no |
        | Cert Config Setup | ${cert} | ${key} | one_cert=NO | intermediate=NO| rsa_cert_outbound=${cert2} | rsa_key_outbound=${key2} | rsa_cert_https=${cert3} | rsa_key_http=${key3} | rsa_cert_ldap=${cert4} | rsa_key_ldap=${key4} |
        """

        intermediate = self._process_yes_no(intermediate)
        one_cert = self._process_yes_no(one_cert)
        replace = self._process_yes_no(replace)

        if is_yes(one_cert):
            cert_list = [(rsa_cert, rsa_key, intermediate_cert)]
        else:
            cert_list = [(rsa_cert, rsa_key), (rsa_cert_outbound, rsa_key_outbound),
                         (rsa_cert_https, rsa_key_https), (rsa_cert_ldap, rsa_key_ldap)]

        self._cli.certconfig().setup()(one_cert, replace, intermediate, cert_list)
