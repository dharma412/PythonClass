#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/cert_config.py#1 $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions

class CertConfig(CliKeywordBase):
    """Configure cryptographic certificates by entering certificate and
    private key in PEM format.
    """

    def get_keyword_names(self):
        return [
            'cert_config_setup',
        ]

    def  cert_config_setup(self,
                           rsa_cert=None,
                           rsa_key=None,
                           passphrase=None,
                           select_cert=None,
                           intermediate='yes',
                           intermediate_cert=None):
        """Cert Config Setup.

        certconfig > setup

        Configure security certificate and key.

        Parameters:
        - `rsa_cert`: Either RSA certificate in PEM format or None.
        - `rsa_key`: Either RSA certificate key in PEM format or None.
        - `passphrase': Passphrase is required for encrypted private key.
        - `select_cert': Either name(CN) of the certificate that has been uploaded to the WSA or None.
        - `intermediate`: either 'Yes' if an intermediate certificate should be
        added or 'No' if not.
        - `intermediate_cert`: RSA intermediate certificate in PEM format.

        NOTE: Extra delimiters \'\\n\' should be added into certificates strings
        to split them in ~80 characters chunks. This is kind of workaround for a
        CLI bug that doesn't allow this script to send in large amounts of text
        at once.

        Examples:

        | Cert Config Setup | a | k | intermediate=yes | intermediate_cert=c |

        | Cert Config Setup | a | k | intermediate=no |

        | Cert Config Setup | select_cert=test_appliance_cert |
        """

        intermediate = self._process_yes_no(intermediate)
        cert_list = [(rsa_cert, rsa_key, intermediate_cert)]
        return self._cli.certconfig().setup()(select_cert, intermediate, cert_list,passphrase)
