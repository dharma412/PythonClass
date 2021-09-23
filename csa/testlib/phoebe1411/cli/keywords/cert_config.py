#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase, DEFAULT
import traceback

class certconfig(CliKeywordBase):
    """
    cli -> certconfig

    Provides keywords for configuring cryptographic certificates by entering
    certificate and private key in PEM format.
    """

    def get_keyword_names(self):
        return ['certconfig_certificate_new',
                'certconfig_certificate_import',
                'certconfig_certificate_paste',
                'certconfig_certificate_edit',
                'certconfig_certificate_delete',
                'certconfig_certificate_export',
                'certconfig_certificate_print',
                'certconfig_certauthority_custom_enable',
                'certconfig_certauthority_custom_disable',
                'certconfig_certauthority_custom_print',
                'certconfig_certauthority_custom_export',
                'certconfig_certauthority_custom_import',
                'certconfig_certauthority_custom_delete',
                'certconfig_certauthority_system_enable',
                'certconfig_certauthority_system_disable',
                'certconfig_certauthority_system_print',
                'certconfig_certauthority_system_export',
                'certconfig_default_warning_message_check',
                ]

    def certconfig_certificate_new(self, *args):
        """
        Creates a self-signed certificate.

        certconfig -> certificate -> new

        *Parameters*:
        - `certificate_type`: Type of certificate to choose, Default value = 1
        - `name`: Name for the certificate profile
        - `common_name`: Specify common
        - `fqdn_validation`: Pass Yes to enable FQDN validaion else pass No.
        - `org`: Specify organisation
        - `org_unit`: Specify organisation unit
        - `city`: Specify city or locality
        - `state`: Specify State
        - `country`: Specify Country(2 letter code)
        - `duration`: Specify duration before expiration (in days)
        - `priv_key_size`: Specify size of private key
        - `email_address`: Enter email address for 'subjectAltName' extension
        - `dns`: Enter the DNS you want to add
        - `another_dns`: Add another member, Default value = NO

        *Examples*:
        | Certconfig Certificate New | certificate_type=2 | name=mycert | common_name=somename |
        | ... | org=myorg | org_unit=myunit | city=mycity | state=mystate |
        | ... | country=IN | email_address=anuravik@cisco.com | dns=cisco.com | another_dns=NO |

        | Certconfig Certificate New | name=mycert | common_name=somename |
        | ... | org=myorg | org_unit=myunit | city=mycity | state=mystate |
        | ... | country=IN |
        """
        kwargs = self._convert_to_dict(args)
        try:
            return self._cli.certconfig().certificate().new(**kwargs)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certificate_edit(self, name, update_cert=False, cert=None,
                                    inter_cert_list=None, remove_cert_list=None, fqdn_validation=None):
        """
        Updates an existing certificate

        certconfig -> certificate -> edit

        *Parameters*:
        - `name`: Name for the certificate profile to update
        - `update_cert`: update the existing public certificate.
          Either True or False
        - `cert`: Specify the public certificate in PEM format
        - `inter_cert_list`: List of intermediate certificates to be added
        - `remove_cert_list`: List of intermediate certificates to be removed
        - `fqdn_validation`: Pass Yes to enable FQDN validaion else pass No.

        *Examples*:
        | ${Inter_Cert_List} | Create List | ${inter_cert1} | ${inter_cert2} |
        | ${Remove_Cert_List} | Create List | 1 |
        | Certconfig Certificate Edit | mycert |
        | ... | inter_cert_list=${Inter_Cert_List} |
        | ... | remove_cert_list=${Remove_Cert_List} |
        """
        try:
            self._cli.certconfig().certificate().edit(name,
             update_cert=update_cert, cert=cert,
             inter_cert_list=inter_cert_list, remove_cert_list=remove_cert_list,
             fqdn_validation=fqdn_validation)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certificate_import(self, cert_name, filename, password, fqdn_validation=None):
        """
        Imports a certificate from a local PKCS#12 file

        certconfig -> certificate -> import

        *Parameters*:
        - `cert_name`: Name for this certificate profile created by importing
        - `filename`: File name on the machine to be imported
        - `password`: Specify the password
        - `fqdn_validation`: Pass Yes to enable FQDN validaion else pass No.

        *Examples*:
        | Certconfig Certificate Import | newmycert | cert.txt | ironport |
        """
        try:
            self._cli.certconfig().certificate().\
              import_cert(cert_name, filename, password, fqdn_validation)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certificate_export(self, cert_name, filename, password):
        """
        Exports a certificate into a file

        certconfig -> certificate -> export

        *Parameters*:
        - `cert_name`: Name of the certificate profile to be exported
        - `filename`: File name for the exported certificate profile
        - `password`: Specify the password for this file

        *Examples*:
        | Certconfig Certificate Export | mycert | cert.txt | ironport |
        """
        try:
            self._cli.certconfig().certificate().\
              export_cert(cert_name, filename, password)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certificate_delete(self, *args):
        """
        Removes a certificate

        certconfig -> certificate -> delete

        *Parameters*:
        - `cert`: Name of the certificate profile to be deleted
        - `confirm`: Confirm deletion

        *Examples*:
        |  Certconfig Certificate Delete | cert=mycert | confirm=yes |
        """
        kwargs = self._convert_to_dict(args)
        try:
            self._cli.certconfig().certificate().delete(**kwargs)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certificate_paste(self, name, cert, key, cert_overwrite=False,
            inter_cert_list=None, remove_cert_list=None, fqdn_validation=None):
        """
        Paste a certificate into the CLI

        certconfig -> certificate -> paste

        *Parameters*:
        - `name`: Name for the certificate profile
        - `cert`: Specify the public certificate in PEM format
        - `key`: Specify the private key in PEM format
        - `cert_overwrite`: Confirm Certificate overwrite if already existing.
          Either True or False
        - `inter_cert_list`: List of intermediate certificates to be added
        - `remove_cert_list`: List of intermediate certificates to be removed
        - `fqdn_validation`: Pass Yes to enable FQDN validaion else pass No.

        *Examples*:
        | ${cert} | Set Variable | -----BEGIN CERTIFICATE-----\nMIIDsjCCAxugAwIBAgIBATANBgkqhkiG9w0BAQQFADCBkzELMAkGA1UEBhMCVVMx\nEzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVNhbiBCcnVubzEZMBcGAkGA1UECxMCUUExDTALBgNVBAMTBG1hdHQx\nJDAiBgkqhkiG9w0BCQEWFW1saXNpdHphQGlyb25wb3J0LmNvbTAeFw0wMzA0MTcy\nMTQxNTlaFw0wNDA0MTYyMTQxNTlaMIGGMQswCQYDVQQGEwJVUzETMBEGA1UECBMIEJydW5vMRkwFwYDVQQKExBJcm9ucG9y\ndCBTeXN0ZW1zMQ0wCwYDVQQDEwRtYXR0MSQwIgYJKoZIhvcNAQkBFhVtbGlzaXR6\nYUBpcm9ucG9ydC5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAL852rYe\181GbSHg8eRPs0MeiLobEP4N7VRil7\npkaN3esCnjI8AdjtA/EX4qqLn3qdl/5bPtQxYpjONyagROMwN8j/BCzC9RCpxHXX\nbn7SQyUcyuWVMARR5ZEuFQFdsNZNhemzytMdAgMBAAGjggEfMIIBGzAJBgNVHRME\nAIEdlbmVyYXRlZCBDZXJ0aWZpY2F0\nZTAdBgNVHQ4EFgQUDAkbYX2t3XCV3PjkXAoM87VSsuEwgcAGA1UdIwSBuDCBtYAU\nsBKk8MEydJl5VTAvfTEv/6KfL9mhgZmkgZYwgZMxCzAJBgNVBAYTAlVTMRMwEQYD\nVQQ4gQnJ1bm8xGTAXBgNVBAoTEEly\nb25wb3J0IFN5c3RlbXMxCzAJBgNVBAsTAlFBMQ0wCwYDVQQDEwRtYXR0MSQwIgYJ\nKoZIhvcNAQkBFhVtbGlzaXR6YUBpcm9ucG9ydC5jb22CAQAwDQYJKoZIhvcNAQEE\nBQADgENHWFq6O8GGXlFuaqIYhjn2C\nueaswrjPR/3iipfme5nTcmESOkBDzQhSpW76KdtBjgqb9ZKzyK6AiwYuxUcSWv5Z\nf0SG0zDkDDVK4IRx/iaeDXnGeRvpH9cbP/4fNLu8iPJTFdmLRU4=\n-----END CERTIFICATE----- |
        | Certconfig Certificate Paste | mycert1 | ${cert} | ${key} |
        | ... | cert_overwrite=${True} |
        """
        try:
            self._cli.certconfig().certificate().paste(name, cert, key,
              cert_overwrite=cert_overwrite, inter_cert_list=inter_cert_list,
              remove_cert_list=remove_cert_list, fqdn_validation=fqdn_validation)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certificate_print(self):
        """
        Display certificates assigned to services

        certconfig -> certificate -> print

        *Returns*:
          Output of the print command

        *Examples*:
        | ${output}= | Certconfig Certificate Print |
        """
        try:
            return self._cli.certconfig().certificate().print_cert()
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_custom_enable(self):
        """
        Enables the custom certificate authorities list

        certconfig -> certauthority -> custom -> enable

        *Examples*:
        | Certconfig Certauthority Custom Enable |
        """
        try:
            self._cli.certconfig().certauthority().custom().enable()
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_custom_disable(self):
        """
        Disables the custom certificate authorities list

        certconfig -> certauthority -> custom -> disable

        *Examples*:
        | Certconfig Certauthority Custom Disable |
        """
        try:
            self._cli.certconfig().certauthority().custom().disable()
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_custom_print(self):
        """
        Prints the list of custom certificate authorties

        certconfig -> certauthority -> custom -> print

        *Returns*:
          Output of the print command

        *Examples*:
        | ${output}= | Certconfig Certauthority Custom Print |
        """
        try:
            return self._cli.certconfig().certauthority().custom().print_cert()
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_custom_export(self, filename,
                                               export_all_certificates='Yes',
                                               export_cert_name=None):
        """
        Exports the list of custom certificate authorties

        certconfig -> certauthority -> custom -> export

        *Parameters*:
        - `filename`: Name for the exported file
        - `export_all_certificates`: Whether to export all certificates or not.
                    Default value is set to Yes which is similar to old behavior.
        - `export_cert_name`: Pass the certificate name to be exported.
                    Valid when the above parameter is set ot No.

        *Examples*:
        | Certconfig Certauthority Custom Export | cert_file.txt |
        | Certconfig Certauthority Custom Export                 |
        | ... | cert_file_3.txt                                  |
        | ... | export_all_certificates=No                       |
        | ... | export_cert_name=My Cert                         |
        """
        try:
            self._cli.certconfig().certauthority().custom().\
              export_cert(
                  filename=filename,
                  export_all_certificates=export_all_certificates,
                  export_cert_name=export_cert_name)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_custom_import(self, filename, check_format='No'):
        """
        Imports the list of custom certificate authorties

        certconfig -> certauthority -> custom -> import

        *Parameters*:
        - `filename`: Name of the file on the machine to import

        *Examples*:
        | Certconfig Certauthority Custom Import | cert_file.txt |
        """
        try:
           self._cli.certconfig().certauthority().custom().\
              import_cert(filename=filename, check_format=check_format)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_custom_delete(self, *args):
        """
        Delete the custom certificate authorities list

        certconfig -> certauthority -> custom -> delete

        *Parameters*:
        - `cert`: Name of the custom certificate authorities to be deleted
        - `confirm`: Confirm deletion

        *Examples*:
        |  Certconfig Certauthority Custom Delete | cert=mycert | confirm=yes |
        """
        kwargs = self._convert_to_dict(args)
        try:
            self._cli.certconfig().certauthority().custom().delete(**kwargs)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_system_enable(self):
        """
        Enables the system certificate authorities list

        certconfig -> certauthority -> system -> enable

        *Examples*:
        | Certconfig Certauthority System Enable |
        """
        try:
            self._cli.certconfig().certauthority().system().enable()
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_system_disable(self):
        """
        Disables the system certificate authorities list

        certconfig -> certauthority -> system -> disable

        *Examples*:
        | Certconfig Certauthority System Enable |
        """
        try:
            self._cli.certconfig().certauthority().system().disable()
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_system_print(self):
        """
        Prints the list of system certificate authorties

        certconfig -> certauthority -> system -> print

        *Returns*:
          Output of the print command

        *Examples*:
        | ${output}= | Certconfig Certauthority System Print |
        """
        try:
            return self._cli.certconfig().certauthority().system().print_cert()
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_certauthority_system_export(self, filename):
        """
        Exports the list of System certificate authorties

        certconfig -> certauthority -> system -> export

        *Parameters*:
        - `filename`: Name for the exported file

        *Examples*:
        | Certconfig Certauthority System Export | cert_file.txt |
        """
        try:
            self._cli.certconfig().certauthority().system().\
              export_cert(filename=filename)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

    def certconfig_default_warning_message_check(self):
        """
        Method to verify default warning message if user uses default certificate
        in LDAP and other configurations.

       cli -> certconfig

        *Examples*:
        | Certconfig Default Warning Message Check|

        """
        try:
            self._cli.certconfig().default_warning()
        except Exception as error:
            self._cli.restart()
            self._debug('ERROR IN DEFAULT WARNING: %s' %error)
            raise error
