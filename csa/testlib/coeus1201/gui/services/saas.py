#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/saas.py#2 $
# $DateTime: 2019/11/17 23:33:35 $
# $Author: biaramba $

import common.gui.guiexceptions as guiexceptions
from constants import saas_cert_info
from common.gui.guicommon import GuiCommon

class Saas(GuiCommon):
    """WSA's configuration of identity provider for SaaS is done via GUI's
       'Security Services -> Identity Provider Settings for SaaS' page.
       This page allows user to enable, disable, and edit settings related
       to identity provider for SaaS."""

    cert_keys = ['name',
                 'org',
                 'org_unit',
                 'country',
                 'duration']

    upload_cert_keys = ['cert',
                        'key',
                        'key_is_encrypted',
                        'key_password',
                        ]

    def get_keyword_names(self):
        return ['saas_enable',
                'saas_disable',
                'saas_get_settings',
                'saas_edit_settings']

    def _open_page(self):
        """Open 'Identity Provider Settings for SaaS' """

        self._navigate_to('Network', 'Identity Provider for SaaS')
        self.warn = ''

    def saas_disable(self):
        """Disable identity provider for SaaS.

        Example:
        | Saas Disable |

        """
        saas_enable_checkbox = 'enabled'
        self._open_page()
        # check if Saas already disabled
        if not self._check_feature_status(feature='saas_id_provider'):
            return
        self._click_edit_settings_button()
        self.unselect_checkbox(saas_enable_checkbox)
        self._click_submit_button()

    def saas_get_settings(self):
        """Gets settings

        Example:
        | ${result} | Saas Get Settings |

        """
        ENTRY_ENTITIES = lambda row,col:\
            '//table[@class=\'pairs\']/tbody/tr[%s]%s' % (str(row),col)
        entries = {}

        self._open_page()
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*',''))) + 1
        for row in xrange(1, num_of_entries):
            if self._is_element_present(ENTRY_ENTITIES(row, '/th[1]')):
                name = self.get_text(ENTRY_ENTITIES(row, '/th[1]'))
                value = self.get_text(ENTRY_ENTITIES(row, '/td[1]'))
                entries[name] = value
        return entries

    def _set_domain_name(self, domain_name):

        domain_name_field = 'domain_name'
        if domain_name is not None:
            self.input_text(domain_name_field, domain_name)

    def _set_entity_id(self, entity_id):

        entity_id_field = 'entity_id'
        if entity_id is not None:
            self.input_text(entity_id_field, entity_id)

    def _enable_or_edit(self):
        """Enable or edit Identity Provider for Saas"""

        enable_and_edit_button = \
                 "xpath=//input[@value='Enable and Edit Settings...']"
        if self._check_feature_status(feature='saas_id_provider'):
            # Saas already enabled
            self._click_edit_settings_button()
        else:
            # Enabling Saas
            self.click_button(enable_and_edit_button)

    def _generate_or_upload_cert(self, cert_info):

        select_cert_radio_button = {'generate': 'generatedCertRadio',
                                    'upload': 'uploadedCertRadio'}
        if 'name' in cert_info.keys():
            self._click_radio_button(select_cert_radio_button['generate'])
            self._generate_cert(cert_info)
        elif 'cert' in cert_info.keys():
            self._click_radio_button(select_cert_radio_button['upload'])
            self._upload_cert_and_key(cert_info)
        else:
            raise ValueError\
             ('Invalid Keys for \'Identity Provider Signing Certificate\'')

    def _generate_cert(self, cert_info):

        cert_keys = {'name': 'dialogCertCommonName',
                     'org': 'dialogCertOrganization',
                     'org_unit': 'dialogCertOrganizationUnit',
                     'country': 'dialogCertCountry',
                     'duration': 'dialogCertExpiration'}
        generate_new_cert_button = 'generate_cert'
        GENERATE_BUTTON = "xpath=//button[contains(text(),'Generate')]"

        self.click_button(generate_new_cert_button, "don't wait")
        if len(cert_info) != 5:
            raise ValueError('\'cert_info\' should be of length 5')
        for cert_field, value in cert_info.iteritems():
            if cert_field not in cert_keys.keys():
                raise ValueError\
                   ('Invalid Key \'%s\' to Generate a new certificate. '\
                    'Here are the valid certificate fields '\
                    '%s' % (cert_field, cert_keys.keys()))
            self.input_text(cert_keys[cert_field], cert_info[cert_field])
        self.click_button(GENERATE_BUTTON)

    def _upload_cert_and_key(self, upload_cert):

        upload_fields = {'cert': 'uploadCertificate',
                         'key': 'uploadKey',
                         'key_is_encrypted': None,
                         'key_password': None,
                         }
        upload_files_button = 'uploadFiles'
        if len(upload_cert) != 4:
            raise ValueError('\'upload_cert\' should be of length 4')
        for cert_key, value in upload_cert.iteritems():
            if cert_key not in upload_fields.keys():
                raise ValueError\
                  ('Invalid Key \'%s\' to upload a certificate. '\
                   'Here are the valid upload fields '\
                   '%s' % (cert_key, upload_fields.keys()))
        self.choose_file(upload_fields['cert'], upload_cert['cert'])
        self.choose_file(upload_fields['key'], upload_cert['key'])
        self._set_key_is_encrypted(upload_cert['key_is_encrypted'])
        self._set_key_password(upload_cert['key_password'])
        self.click_button(upload_files_button)
        self.warn = self.check_for_warning()

    def saas_edit_settings(self,
                      domain_name=None,
                      entity_id=None,
                      cert_name=None,
                      cert_org=None,
                      cert_org_unit=None,
                      cert_country=None,
                      cert_duration=None,
                      cert_location=None,
                      cert_key=None,
                      key_is_encrypted=None,
                      key_password=None,
                      ):

        """Edit current settings for identity provider for SaaS.

        Parameters:
         - `domain_name` : identity provider domain name.
         - `entity_id`   : identity provider entity ID.
         - `cert_name`: certificate common name during certification generation
         - `cert_org`: certificate organization.
         - `cert_org_unit`: certificate organizational unit.
         - `cert_country`: certificate country.
         - `cert_duration`: duration before certificate expiration in months.
         - `cert_location`: location of a certificate file to upload.
         - `cert_key`: location of key file to upload.
         - `key_is_encrypted`: Either 'True' or 'False'
         - `key_password`: password for encrypted key

        Example:
        | Saas Edit Settings | domain_name=foo2.com | entity_id=cnn2.com | cert_location=%{HOME}/work/sarf_centos/tests/coeus75/unittests/testdata/cert.crt | cert_key=%{HOME}/work/sarf_centos/tests/coeus75/unittests/testdata/cert.key |
        | ... | key_is_encrypted=${True} |
        | ... | key_password=Secret |
        | Saas Edit Settings | domain_name=foo.com | entity_id=cnn.com | cert_name=abc | cert_org=ironport | cert_org_unit=QA | cert_country=US | cert_duration=31 |
        """
        cert_values = [cert_name,
                       cert_org,
                       cert_org_unit,
                       cert_country,
                       cert_duration]

        upload_cert_values = [cert_location,
                              cert_key,
                              key_is_encrypted,
                              key_password,
                              ]

        if cert_location != None:
            cert_info = dict(zip(self.upload_cert_keys, upload_cert_values))
        else:
            if all(cert_values):
                cert_info = dict(zip(self.cert_keys, cert_values))
            else:
                cert_info = saas_cert_info.DEFAULT

        self._open_page()
        if not self._check_feature_status(feature='saas_id_provider'):
            raise guiexceptions.GuiFeatureDisabledError\
             ('Cannot edit identity provider for SaaS as disabled')
        self._click_edit_settings_button()
        self._set_domain_name(domain_name)
        self._set_entity_id(entity_id)
        self._generate_or_upload_cert(cert_info)
        self._click_submit_button()
        # Validate if submitted.
        self._check_action_result()

    def saas_enable(self,
               domain_name=None,
               entity_id=None,
               cert_name=None,
               cert_org=None,
               cert_org_unit=None,
               cert_country=None,
               cert_duration=None,
               cert_location=None,
               cert_key=None,
               key_is_encrypted=None,
               key_password=None,
               ):
        """Enable identity provider for SaaS.

        Parameters:
         - `domain_name`: identity provider domain name.
                          Required if enabling for the very first time.
         - `entity_id`: identity provider entity ID.
                        Required if enabling for the very first time.
         - `cert_name`: certificate common name during certification generation
         - `cert_org`: certificate organization.
         - `cert_org_unit`: certificate organizational unit.
         - `cert_country`: certificate country.
         - `cert_duration`: duration before certificate expiration in months.
         - `cert_location`: location of a certificate file to upload.
         - `cert_key`: location of key file to upload.
         - `key_is_encrypted`: Either 'True' or 'False'
         - `key_password`: password for encrypted key

        Example:
        | Saas Enable | domain_name=foo3.com | entity_id=cnn3.com |
        | Saas Enable | domain_name=foo2.com | entity_id=cnn2.com | cert_location=%{HOME}/work/sarf_centos/tests/coeus75/unittests/testdata/cert.crt | cert_key=%{HOME}/work/sarf_centos/tests/coeus75/unittests/testdata/cert.key |
        | ... | key_is_encrypted=${True} |
        | ... | key_password=Secret |
                | Saas Enable | domain_name=foo.com | entity_id=cnn.com | cert_name=abc | cert_org=ironport | cert_org_unit=QA | cert_country=US | cert_duration=31 |
        """
        cert_values = [cert_name,
                       cert_org,
                       cert_org_unit,
                       cert_country,
                       cert_duration]

        upload_cert_values = [cert_location,
                              cert_key,
                              key_is_encrypted,
                              key_password,
                              ]

        if cert_location != None:
            cert_info = dict(zip(self.upload_cert_keys, upload_cert_values))
        else:
            if all(cert_values):
                cert_info = dict(zip(self.cert_keys, cert_values))
            else:
                cert_info = saas_cert_info.DEFAULT

        self._open_page()
        self._enable_or_edit()
        self._set_domain_name(domain_name)
        self._set_entity_id(entity_id)
        self._generate_or_upload_cert(cert_info)
        self._click_submit_button()
        # Validate if submitted.
        self._check_action_result()
        return self.warn
