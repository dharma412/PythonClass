#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/cert_config.py#3 $ $DateTime: 2020/07/01 01:42:07 $ $Author: mrmohank $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions
from sal.containers.yesnodefault import YES, NO, is_yes

class CertConfig(CliKeywordBase):
    """Configure cryptographic certificates by entering certificate and
    private key in PEM format.
    """

    def get_keyword_names(self):
        return ['cert_config_setup',
                'cert_config_options',
                'cert_config_clear_certificates',
                'get_cert_authority_status',
                'cert_authority_enable_disable',
                'cert_authority_print',
                'cert_authority_export',
                'cert_authority_import',
                'cert_authority_delete']

    def cert_config_options(self):
        """
        cli->certconfig
        Prints the options when the certconfig command is sent in CLI

        Parameters: None
        Examples:

        | ${certconfig_options}=  Cert Config Options |

        :return:
        """

        return self._cli.certconfig(option='yes')

    def cert_config_setup(self,
                          rsa_cert,
                          rsa_key,
                          one_cert='yes',
                          replace='yes',
                          intermediate='yes',
                          fqdn=None,
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
        replace= self._process_yes_no(replace)

        if is_yes(one_cert):
            cert_list = [(rsa_cert, rsa_key, intermediate_cert)]
        else:
            cert_list = [(rsa_cert, rsa_key), (rsa_cert_outbound, rsa_key_outbound),
                        (rsa_cert_https, rsa_key_https), (rsa_cert_ldap, rsa_key_ldap)]

        self._cli.certconfig().certificate().setup()(one_cert, replace, intermediate, cert_list, fqdn)

    def cert_config_clear_certificates(self,clear='no'):
        """
        cli->certconfig->clear
        Clears the existing certificates

        Parameters: None
        Examples:

        | Cert Config Clear Certificates |
         | Cert Config Clear Certificates  clear=yes |
        :return:
        """
        clear = self._process_yes_no(clear)
        self._cli.certconfig().certificate().clear_certificates(clear)

    def get_cert_authority_status(self, cert_auth_type='custom'):
        cert_raw_status = self._cli.certconfig().cert_authority_status().split('\r\n')
        for text in cert_raw_status:
            if 'Custom List:' in text and cert_auth_type == 'custom':
                return text.split(': ')[1]
            if 'System List:' in text and cert_auth_type == 'system':
                return text.split(': ')[1]

    def cert_authority_enable_disable(self, cert_auth_type='custom', enable=True):
        status = self.get_cert_authority_status(cert_auth_type)
        print ("status is %s ==" %status)
        if status == 'Enabled' and enable:
            self._info("Cert is already enabled")
            return "Already Enabled"
        elif status == 'Disabled' and enable is False:
            self._info("Cert is already Disabled")
            return "Already Disabled"
        else:
            curr_status = self._cli.certconfig().cert_authority_toggle_status(cert_auth_type, enable)
            self._info(curr_status)
            return curr_status

    def cert_authority_print(self, cert_auth_type='custom'):
        curr_status = self._cli.certconfig().cert_authority_print(cert_auth_type)

        cert_list_raw = curr_status.split('certificates:\r\n')[1].split('\r\n')
        cert_list_raw_final = [i for i in cert_list_raw if i]

        return self._refine_list(cert_list_raw_final)

    def cert_authority_export(self, cert_number, export_file_name, cert_type='custom', export_all=False):
        return self._cli.certconfig().cert_authority_export(cert_number, export_file_name, cert_type, export_all)

    def cert_authority_import(self, file_name, fqdn_validation=None):
        return self._cli.certconfig().cert_authority_import(file_name,fqdn_validation)

    def cert_authority_delete(self, cert_number, confirm_delete='y'):
        return self._cli.certconfig().cert_authority_delete(cert_number, confirm_delete)

    def _refine_list(self, cert_list):
        terminate = True
        cert_list_raw_final = cert_list
        for i in range(len(cert_list_raw_final)):
            if (cert_list_raw_final[i].startswith('C=') is False) \
                    and (cert_list_raw_final[i].startswith('OU=') is False) \
                    and (cert_list_raw_final[i].startswith('CN=') is False) \
                    and (cert_list_raw_final[i].startswith('O=') is False):
                cert_list_raw_final[i - 1] = cert_list_raw_final[i - 1] + ' ' + cert_list_raw_final[i]
                cert_list_raw_final.pop(i)
                break
        for item in cert_list_raw_final:
            if (item.startswith('C=') is False) \
                    and (item.startswith('OU=') is False) \
                    and (item.startswith('CN=') is False) \
                    and (item.startswith('O=') is False):
                terminate = False
                break
        if terminate is False:
            self.refine_list(cert_list_raw_final)
        else:
            return cert_list_raw_final