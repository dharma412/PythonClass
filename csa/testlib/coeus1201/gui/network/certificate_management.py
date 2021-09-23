#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/certificate_management.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from constants import https_cert_info
from common.gui.guicommon import GuiCommon
from sal.containers.yesnodefault import  is_yes,is_no


MANAGED_CERT_BUTTON = "//input[@alt='Manage Trusted Root Certificates...']"

class CertManagemen(GuiCommon):

    """Certificate Management page interaction class.
    'Network -> Certificate Management' section.
    """

    def get_keyword_names(self):
        return [
            'certificate_management_import_root_certificate',
            'certificate_management_delete_root_certificate',
            'certificate_management_untrust_root_certificates',
            'certificate_management_trust_root_certificates',
            'certificate_management_untrust_all_root_certificates',
            'certificate_management_trust_all_root_certificates'
            ]

    def _open_certificate_management_page(self):
        """Go to Certificate Management page."""

        self._navigate_to('Network', 'Certificate Management')
        if self._is_text_present('Feature key is missing.'):
            raise guiexceptions.GuiFeaturekeyMissingError\
              ("Certificate Management feature is not available due to missing feature key")

    def certificate_management_untrust_root_certificates(self, certificates):
        """
        Override Trust for the specified certificates
        Parameters:
        - `certificates`: string of comma-separated certificates. If an entry
         on the list is overridden, it will not be treated as a trusted root
         certificate authority
        Example:
        | Certificate Management Untrust Root Certificates | A-Trust-nQual-01, A-Trust-nQual-03 |
        """
        self._manage_trust(False, certificates)

    def certificate_management_trust_root_certificates(self, certificates):
        """
        Set Trust for the specified certificates
        Parameters:
        - `certificates`: string of comma-separated certificates. If an entry
         on the list is not overridden, it will be treated as a trusted root
         certificate authority
        Example:
        | Certificate Management Trust Root Certificates | A-Trust-nQual-01, A-Trust-nQual-03 |
        """
        self._manage_trust(True, certificates)

    def certificate_management_untrust_all_root_certificates(self):
        """
        Override Trust for all certificates
        Example:
        | Certificate Management Untrust All Root Certificates |
        """
        self._manage_trust(False, None)

    def certificate_management_trust_all_root_certificates(self):
        """
        Set Trust for all certificates
        Example:
        | Certificate Management Trust All Root Certificates |
        """
        self._manage_trust(True, None)

    def _manage_trust(self, trust=None, certificates=None):
        """
        set/unset trust for specified/all certificates
        If trust = True, enable; else disable
        If certificates = None, for all; else for the certificates in the list
        """
        CHECKBOX = lambda name: \
            "xpath=//td[text() = '%s']/../../../../../../td[3]/input" % name
        CHECKBOX_ALL = lambda index: \
            "xpath=(//table[@class='cols']/tbody/tr/td/a/../..)[%s]/td[3]/input" % index
        self._open_certificate_management_page()
        self.click_button(MANAGED_CERT_BUTTON)
        if certificates == None:
            index = 1
            old_speed = self.set_selenium_speed(0)
            try:
                while(True):
                    self._set_checkbox(not trust, CHECKBOX_ALL(index))
                    index += 1
            except:
                self._info("Processed " + str((index-1)) + " certificates")
            self.set_selenium_speed(old_speed)
        else:
            for certificate in self._convert_to_tuple(certificates):
                self._info(certificate)
                self._set_checkbox(not trust, CHECKBOX(certificate))
        self._click_submit_button()

    def certificate_management_import_root_certificate(self, location=None):
        """Import custom root authority certificates.

        Parameters:
        - `location`: location of a certificate file to import.

        Example:
        | Certificate Management Import Root Certificate | /home/user/cert.pem |
        | Certificate Management Import Root Certificate | location=/home/user/cert.pem |
        """
        import_button = "xpath=//input[@value='Import...']"
        import_field = 'certificate'
        self._open_certificate_management_page()
        if not self._check_feature_status(feature='https_proxy'):
            raise guiexceptions.GuiFeatureDisabledError\
                 ('Cannot import root auth. certificate as HTTPS proxy '\
                  'is disabled')
        else:
            self.click_button(MANAGED_CERT_BUTTON)
            self.click_button(import_button)
            self.choose_file(import_field, location)
            self._click_submit_button()

    def certificate_management_delete_root_certificate(self, name=None):
        """Deletes custom root authority certificate.

        `name`: common name of the custom root authority certificate
               to be deleted.

        Example:
        | Certificate Management Delete Root Certificate | name=commonCertificateName |
        """

        self._open_certificate_management_page()
        if self._is_text_present\
                         ('No custom Root Authority certificates have been '\
                                                                 'imported.'):
            raise guiexceptions.GuiFeatureDisabledError\
             ('Cannot perform delete operation as no certificate present')
        self.click_button(MANAGED_CERT_BUTTON)
        cert_row = "xpath=//td[text() = '%s']/../../../../../../td[4]//img" % name

        if not cert_row:
            raise guiexceptions.GuiControlNotFoundError\
                   ('Root auth. certificate \'%s\''% (name,), 'HTTPS Proxy')

        self.click_element(cert_row, "don't wait")
        self._click_continue_button()

