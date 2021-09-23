#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/https_proxy.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from constants import https_cert_info
from common.gui.guicommon import GuiCommon
from sal.containers.yesnodefault import  is_yes,is_no

DROP_GRP = lambda index: 'drop_customRadio_radioGroup[%d]' % (index,)
DROP_GRP = lambda index: 'drop_customRadio_invalidGroup[%d]' % (index,)
DROP_OCSPGRP = lambda index: 'drop_customRadio_ocspGroup[%d]' % (index,)
DECRYPT_GRP = lambda index: 'decrypt_customRadio_invalidGroup[%d]' % (index,)
DECRYPT_OCSPGRP = lambda index: 'decrypt_customRadio_ocspGroup[%d]' % (index,)
IMG_SCN_GRP = lambda index: 'img_scan_customRadio_invalidGroup[%d]' % (index,)
IMG_DROP_GRP = lambda index: 'img_drop_customRadio_invalidGroup[%d]' % (index,)
SCAN_GRP = lambda index: 'scan_customRadio_invalidGroup[%d]' % (index,)
SCAN_OCSPGRP = lambda index: 'scan_customRadio_ocspGroup[%d]' % (index,)



class HttpsProxy(GuiCommon):

    """HTTPS Proxy settings page interaction class.
    'Security Services -> HTTPS Proxy' section.
    """

    cert_keys = ['name',
                 'org',
                 'org_unit',
                 'country',
                 'duration',
                 'constraints']

    upload_cert_keys = ['cert',
                        'key',
                        'key_is_encrypted',
                        'key_password',
                        ]

    invalid_cert_keys = ['expired',
                         'mismatched',
                         'unrecognized',
                         'invalid_signing',
                         'invalid_leaf',
                         'other',
                         'select_all']
    ocsp_result_handling_keys = ['revoked',
                                 'unknown',
                                 'error',
                                 'select_all'
                                 ]

    ocsp_timeout_settings_keys =  ['val_cache_t',
                                   'inval_cache_t',
                                   'net_cache_t',
                                   'clock_skew',
                                   'max_time_resp']

    def get_keyword_names(self):
        return [
            'https_proxy_enable',
            'https_proxy_disable',
            'https_proxy_edit_settings',
            'ocsp_config_edit_settings',
            'https_proxy_get_settings',
            ]

    def _open_https_proxy_page(self):
        """Go to HTTPS proxy configuration page."""

        self._navigate_to('Security Services', 'HTTPS Proxy')
        if self._is_text_present('Feature key is missing.'):
            raise guiexceptions.GuiFeaturekeyMissingError\
              ("HTTPS feature is not available due to missing feature key")
        self.warn = ''

    def https_proxy_disable(self):
        """Disables HTTPS proxy

        Example:
        | HTTPS Proxy Disable |
        """
        https_proxy_checkbox = 'enabled'
        self._open_https_proxy_page()
        if not self._check_feature_status(feature='https_proxy'):
            return
        self._click_edit_settings_button()
        self.unselect_checkbox(https_proxy_checkbox)
        self._click_submit_button(wait=False,
                                  accept_confirm_dialog=True, accept_EULA=None)

    def _enable_or_edit(self):
        """Enable and edit HTTPS Proxy."""

        enable_proxy_button =\
                "//input[@value='Enable and Edit Settings...']"
        accept_license_button = 'action:AcceptLicense'
        if self._check_feature_status(feature='https_proxy'):
            self._click_edit_settings_button()
        else:
            self.click_button(enable_proxy_button)
            if self._is_text_present('HTTPS Proxy License Agreement'):
                self.click_button(accept_license_button)

    def _disable_or_enable_ocsp_checkbox(self, mode=None):
        """Enables or Disables OCSP checkbox"""
        ocsp_checkbox = "//label[text()='Enable Online Certificate Status Protocol (OCSP)']/../input"
        self._info('Setting OCSP to %s' % (mode,))
        if mode == 'enable':
            #if not self._check_feature_status(feature='ocsp'):
            if not self.is_checked('id=ocsp_enabled'): 
                self._info('Enabling OCSP')
                self.click_element(ocsp_checkbox, "don't wait")
                self._wait_for_text('id=arrow_closed', 'Advanced', timeout=10)
        if mode == 'disable':
            #if not self._check_feature_status(feature='ocsp'):
            if not self.is_checked('id=ocsp_enabled'):
                return
            self._info('Disabling OCSP')
            self.click_element(ocsp_checkbox, "don't wait")

    def _click_on_advanced_ocsp_link(self):
        """Clicks on the Advanced link"""
        advanced_link_open = "arrow_open"
        advanced_link_close = "arrow_closed"
        if self._is_visible(advanced_link_close):
            self.click_element(advanced_link_close, "don't wait")
        else:
            self._info('_click_on_advanced_ocsp_link:link not visible...')

    def _set_timeout_settings_for_ocsp(self, ocsp_timeout_settings_dict=None):
        """Fills the various user supplied timeouts in the GUI"""
        timeout_textbox_markers = {
                'val_cache_t'       :'ocsp_valid_response_cache_ttl',
                'inval_cache_t'     :'ocsp_invalid_response_cache_ttl',
                'net_cache_t':'ocsp_network_error_cache_timeout',
                'clock_skew'               :'ocsp_clock_skew',
                'max_time_resp'  :'ocsp_network_error_timeout'}
        if ocsp_timeout_settings_dict:
            for key,text in ocsp_timeout_settings_dict.iteritems():
                if ocsp_timeout_settings_dict[key]:
                    self.input_text(timeout_textbox_markers[key], text)

    def _set_ocsp_exemption_list(self, exempted_server=None):
        """Adds to the server exemption list textbox in the GUI"""
        exemption_list_field = 'ocsp_proxy_group_exempt_list'
        if exempted_server:
                self.input_text(exemption_list_field, exempted_server)

    def _set_https_ports(self, ports=None):

        https_ports_field = 'httpsPorts'
        if ports:
            ports = self._convert_to_tuple(ports)
            port_text = ",".join([str(p) for p in ports])
            self.input_text(https_ports_field, port_text)

    def _select_root_cert_for_signing(self, cert_info=None):
        if cert_info:
            if 'name' in cert_info.keys():
                self._generate_certificate(generate_cert=cert_info)
            elif 'cert' in cert_info.keys():
                self._upload_certificate(upload_cert=cert_info)
            elif 'signed_cert' in cert_info.keys():
                self._upload_signed_certificate(upload_cert=cert_info)
            else:
                raise guiexceptions.ConfigError\
                      ('Invalid Keys for \'Root Certificate for Signing\'')

    def _generate_certificate(self, generate_cert=None):

        cert_keys = {'name': 'dialogCertCommonName',
                     'org': 'dialogCertOrganization',
                     'org_unit': 'dialogCertOrganizationUnit',
                     'country': 'dialogCertCountry',
                     'duration': 'dialogCertExpiration',
                     'constraints': 'dialogCertIsCritical'}
        generate_cert_radio_button = "id=generatedCertRadio"
        generate_new_cert_button = "generate_cert"

        self._click_radio_button(generate_cert_radio_button)
        self.click_button(generate_new_cert_button, "don't wait")

        if len(generate_cert) is not 6:
            raise ValueError\
                ('\'generate_cert\' should be of length 6')
        for cert_field, value in generate_cert.iteritems():
            if cert_field not in cert_keys.keys():
                raise ValueError\
                      ('Invalid Key \'%s\' to Generate a new certificate. '\
                       'Here are the valid certificate fields '\
                       '%s' % (cert_field, cert_keys.keys()))
            if cert_field == 'constraints':
                if generate_cert['constraints']:
                    self.select_checkbox(cert_keys[cert_field])
            else:
                self.input_text(cert_keys[cert_field],
                    generate_cert[cert_field])
        self._click_continue_button('Generate')
        self._wait_until_text_is_present('successfully generated')

    def _upload_certificate(self, upload_cert=None):
        upload_fields = {'cert': 'uploadCertificate',
                         'key': 'uploadKey',
                         'key_is_encrypted': None,
                         'key_password': None,
                        }
        upload_cert_radio_button = 'id=uploadedCertRadio'
        upload_files_button = 'uploadFiles'
        if upload_cert:
            if len(upload_cert) is not 4:
                raise ValueError('\'upload_cert\' should be of length 4')
            for cert_key, value in upload_cert.iteritems():
                if cert_key not in upload_fields.keys():
                    raise guiexceptions.ConfigError\
                      ('Invalid Key \'%s\' to upload a certificate. '\
                       'Here are the valid upload fields '\
                       '%s' % (cert_key, upload_fields.keys()))
            self._click_radio_button(upload_cert_radio_button)
            self.choose_file(upload_fields['cert'], upload_cert['cert'])
            self.choose_file(upload_fields['key'], upload_cert['key'])
            self._set_key_is_encrypted(upload_cert['key_is_encrypted'])
            self._set_key_password(upload_cert['key_password'])
            self.click_button(upload_files_button)
            self.warn = self.check_for_warning()

    def _upload_signed_certificate(self, upload_cert=None):
        upload_fields = {'cert': 'uploadSignedCertificate'} #Keeping this as dic since we can include addition fileds later
        upload_files_button = 'uploadFileSigned'
        if upload_cert:
            if len(upload_cert) is not 1:
                raise ValueError('\'upload_cert\' should be of length 1')
            self.choose_file(upload_fields['cert'], upload_cert['signed_cert'])
            self.click_button(upload_files_button)
            self.warn = self.check_for_warning()

    def _invalid_certificate_handling(self, invalid_cert_handling=None):

        if invalid_cert_handling:
            if 'select_all' in invalid_cert_handling.keys():
                self._invalid_certificate_handling_select_all\
                  (invalid_cert_select_all=invalid_cert_handling['select_all'])
            else:
                self._invalid_certificate_by_cert_error\
                                  (invalid_cert_handling=invalid_cert_handling)

    def _invalid_certificate_by_cert_error(self, invalid_cert_handling=None):

        invalid_cert_keys = {
                 'expired': (DROP_GRP(0), DECRYPT_GRP(0), IMG_SCN_GRP(0),),
                 'mismatched': (IMG_DROP_GRP(1), DECRYPT_GRP(1), SCAN_GRP(1),),
                 'unrecognized': (DROP_GRP(2), DECRYPT_GRP(2), SCAN_GRP(2),),
                 'invalid_signing': (DROP_GRP(3), DECRYPT_GRP(3), SCAN_GRP(3),),
                 'invalid_leaf': (DROP_GRP(4), DECRYPT_GRP(4), SCAN_GRP(4),),
                 'other': (DROP_GRP(5), DECRYPT_GRP(5), SCAN_GRP(5),)}

        action_index = {'drop': 0, 'decrypt': 1, 'monitor': 2}
        if invalid_cert_handling:
            for cert_error, cert_action in invalid_cert_handling.iteritems():
                if cert_error.lower() not in invalid_cert_keys.keys():
                    raise ValueError\
                      ('Invalid Cert. error \'%s\' for Invalid Certificate '\
                        'Handling. Here are the valid certificate errors '\
                        '%s' % (cert_error, invalid_cert_keys.keys()))
                if cert_action is None:
                    continue
                if cert_action.lower() not in action_index.keys():
                    raise ValueError\
                          ('Invalid action \'%s\' for Invalid Certificate '\
                           'Handling. Here are the valid actions '\
                           '%s' % (cert_action, action_index.keys()))
                action = action_index[\
                         invalid_cert_handling[cert_error].lower()]
                self.click_element(invalid_cert_keys[cert_error][action],
                                   "don't wait")

    def _invalid_certificate_handling_select_all(self,
                                                invalid_cert_select_all=None):
        select_all = {'drop': "//div[@id='link_select_all_1']/a/span",
                      'decrypt': "//div[@id='link_select_all_2']/a/span",
                      'monitor': "//div[@id='link_select_all_3']/a/span"}
        if invalid_cert_select_all:
            if invalid_cert_select_all.lower() not in select_all.keys():
                raise guiexceptions.ConfigError\
                      ('Invalid action \'%s\' for Invalid Certificate '\
                       'Handling. Here are the valid actions '\
                       '%s' % (invalid_cert_select_all, select_all.keys()))
            self.click_element(select_all[invalid_cert_select_all.lower()],
                               "don't wait")

    def _ocsp_result_handling(self, ocsp_result_handling=None):
        """Method that selects OCSP result handling matrix in the GUI

        Specifying revoked or unknown or error values will
        take precedence over select_all option
        """
        individual_enables = ['revoked','unknown','error']
        if ocsp_result_handling:
            specified_enables = list(set(ocsp_result_handling.keys()) \
                                     & set(individual_enables))
            if specified_enables:
                    if 'select_all' in ocsp_result_handling.keys():
                        del ocsp_result_handling['select_all']
                    self._set_ocsp_transaction_conditions\
                                  (ocsp_result_handling=ocsp_result_handling)
                    return
            if 'select_all' in ocsp_result_handling.keys():
                self._ocsp_result_handling_select_all\
                  (ocsp_result_select_all=ocsp_result_handling['select_all'])

    def _set_ocsp_transaction_conditions(self, ocsp_result_handling=None):
        """Chooses the OCSP transaction policy actions
                         according to the choice supplied"""
        ocsp_transact_keys = {
            'revoked': (DROP_OCSPGRP(0), DECRYPT_OCSPGRP(0), SCAN_OCSPGRP(0),),
            'unknown': (DROP_OCSPGRP(1), DECRYPT_OCSPGRP(1), SCAN_OCSPGRP(1),),
            'error'  : (DROP_OCSPGRP(2), DECRYPT_OCSPGRP(2), SCAN_OCSPGRP(2),)}
        action_index = {'drop': 0, 'decrypt': 1, 'monitor': 2}
        if ocsp_result_handling:
            for ocsp_trasact, ocsp_action in ocsp_result_handling.iteritems():
                if ocsp_trasact.lower() not in ocsp_transact_keys.keys():
                    raise ValueError\
                    ('Invalid OCSP transaction. error \'%s\' for OCSP Result'\
                'Handling.Here are the valid OCSP result handling transactions'\
                '%s' % (ocsp_trasact, ocsp_transact_keys.keys()))
                if ocsp_action is None:
                    continue
                if ocsp_action.lower() not in action_index.keys():
                    raise ValueError\
                          ('Invalid action \'%s\' for OCSP Result '\
                           'Handling. Here are the valid actions '\
                           '%s' % (ocsp_action, action_index.keys()))
                action = action_index[ocsp_result_handling\
                                      [ocsp_trasact].lower()]
                self.click_element(ocsp_transact_keys[ocsp_trasact][action],
                                   "don't wait")

    def _ocsp_result_handling_select_all(self, ocsp_result_select_all=None):
        """Method that sets policy options to handle OCSP transactions"""
        select_all = {
        'drop' :
         "//tr[@id='ocsp_handling_tr']/td/table/tbody/tr[2]/th/div/a/span",
        'decrypt' :
         "//tr[@id='ocsp_handling_tr']/td/table/tbody/tr[2]/th[2]/div/a/span",
        'monitor' :
         "/tr[@id='ocsp_handling_tr']/td/table/tbody/tr[2]/th[3]/div/a/span"
        }
        if ocsp_result_select_all:
            if ocsp_result_select_all.lower() not in select_all.keys():
                raise guiexceptions.ConfigError\
                      ('Invalid action \'%s\' for OCSP Result'\
                       'Handling. Here are the valid actions '\
                       '%s' % (ocsp_result_select_all, select_all.keys()))
            self.click_element(select_all[ocsp_result_select_all.lower()],
                               "don't wait")

    def _ocsp_enable_or_disable_nonce(self, mode=None):
        """Enables/Disables nonce """
        nonce_checkbox = 'id=ocsp_use_nonce'
        if mode == 'enable':
                if self._is_checked(nonce_checkbox):
                    return
                self.select_checkbox(nonce_checkbox)
        if mode == 'disable':
                if self._is_checked(nonce_checkbox):
                    self.unselect_checkbox(nonce_checkbox)

    def _ocsp_enable_or_disable_upstreamproxy(self, mode=None):
        """Enables/Disables Upstream Proxy selection """
        upstreamproxy_checkbox = 'id=ocsp_use_upstream_proxy'
        if mode == 'enable':
                if not self._check_feature_status(feature='upstream_proxy'):
                    raise guiexceptions.GuiFeatureDisabledError\
                       ('Cannot configure to use upstream proxy\
                        for OCSP checking as no upstream proxies are defined')
                if self._is_checked(upstreamproxy_checkbox):
                    return
                self.click_element(upstreamproxy_checkbox, "don't wait")
        if mode == 'disable':
                if self._is_checked(upstreamproxy_checkbox):
                    self.click_element(upstreamproxy_checkbox, "don't wait")

    def _ocsp_select_upstreamproxy(self, selected_group=None):
        """Chooses the appropriate Upstream proxy from the dropdown"""
        ocsp_upstream_target = 'ocsp_proxy_group'
        if selected_group:
            ocsp_upstream_option = "label=%s" % (selected_group,)
            self.select_from_list(ocsp_upstream_target,
                                   ocsp_upstream_option)

    def https_proxy_edit_settings(self,
        ports=None,
        enable_decryption_auth=None,
	enable_decryption_enduser_notify=None,
	enable_decryption_enduser=None,
        enable_decryption_app=None,
        cert_name=None,
        cert_org=None,
        cert_org_unit=None,
        cert_country=None,
        cert_duration=None,
        cert_constraints=None,
        cert_location=None,
        cert_key=None,
        signed_cert_location=None,
        key_is_encrypted=None,
        key_password=None,
        err_expired=None,
        err_mismatched=None,
        err_unrecognized=None,
        err_invalidsigning=None,
        err_invalidleaf=None,
        err_other=None,
        err_select_all=None,
        enable_ocsp=None,
        val_cache_t=None,
        inval_cache_t=None,
        net_cache_t=None,
        clock_skew=None,
        max_time_resp=None,
        ocsp_revoke_cert=None,
        ocsp_unk_cert=None,
        ocsp_err=None,
        ocsp_select_all=None,
        crypt_nonce=None,
        upstream_proxy=None,
        upstream_proxy_grp=None,
        exempted_server=None):
        """Sets HTTPS proxy settings and OCSP options.

        Parameters:
        - `ports`: a comma separated string or list of transparent HTTPS Ports.

        - `cert_name`: certificate common name, in a string format.
              Leave empty if you are
                    going to upload a new certificate.

        - `cert_org`: certificate organization.

        - `cert_org_unit`: certificate organizational unit.

        - `cert_country`: certificate country.

        - `cert_duration`: duration before certificate expiration in months.

        - `cert_constraints`: set X509v3 basic constraints extension
                           to critical. Either 'True' or 'False'.

        - `cert_location`: location of a certificate file to upload.Leave empty
                        if you are generating new certificate.

        - 'signed_cert_location`: location of a signed certificate file to upload

        - `cert_key`: location of key file to upload.
        - `key_is_encrypted`: Either 'True' or 'False'
        - `key_password`: password for encrypted key
        - `enable_decryption_auth`: Enable decryption for authentication.
         Either 'True' or 'False'
	- `enable_decryption_enduser_notify`: Enable decryption for display of the
         end-user notification page. Either 'True' or 'False'
	- `enable_decryption_enduser`: Enable decryption for display of the
         end-user acknowledgement page. Either 'True' or 'False'
        - `enable_decryption_app`: Enable decryption for enhanced application
         visibility and control. Either 'True' or 'False'
        - `err_expired`: expired certificate error. Either 'Drop',
                    'Decrypt' or 'Monitor'.

        - `err_mismatched`: mismatched hostname certificate error.
                    One of 'Drop', 'Decrypt' or 'Monitor'.

        - `err_unrecognized`: unrecognized root authority certificate error.
                       One of 'Drop', 'Decrypt' or 'Monitor'.

        - `err_invalidsigning`: Invalid signing certificate error.
                       One of 'Drop', 'Decrypt' or 'Monitor'.

        - `err_invalidleaf`: Invalid leaf certificate error.
                       One of 'Drop', 'Decrypt' or 'Monitor'.

        - `err_other`: all other error types of certificate errors.
                One of 'Drop', 'Decrypt' or 'Monitor'.

        - `err_select_all`: to click 'Select all' for invalid certificate
               handling.
                     One of 'Drop', 'Decrypt' or 'Monitor'.

        - `enable_ocsp`: Enable OCSP (Online Certificate Status Protocol).
                         Enabled by Default.
                         Either 'True or 'False'.

        - `val_cache_t`: Valid response cache timeout
                                    (between 1 second and 7 days).
                               Use a trailing 's' for seconds,
                               'm' for minutes 'h' for hours or
                               'd' for days(Default is seconds).

        - `inval_cache_t`: Invalid response cache timeout
                                    (between 1 second and 7 days).
                                 Use a trailing 's' for seconds,
                                 'm' for minutes 'h' for hours or
                                 'd' for days(Default is seconds).

        - `net_cache_t`: Network error cache timeout
                                            (between 1 second and 24 hours).
                                      Use a trailing 's' for seconds,
                                      'm' for minutes or
                                      'h' for hours(Default is seconds).

        - `clock_skew`: Allowed clockskew between the OCSP responder & WSA
                                            (between 1 second and 60 minutes).
                       Use a trailing 's' for seconds or 'm' for minutes
                                                    (Default is seconds).

        - `max_time_resp`: Maximum time for the WSA to wait for an
                            OCSP response(between 1 second and 10 minutes).
                                    Use a trailing 's' for seconds or
                                    'm' for minutes(Default is seconds).

        - `ocsp_revoke_cert`:The action to be taken when the OCSP response
                            indicates a certificate status of "revoked".
                              One of 'Drop', 'Decrypt' or 'Monitor'.

        - `ocsp_unk_cert`:The action to be taken when the OCSP response
                            indicates a certificate status of "unknown".
                              One of 'Drop', 'Decrypt' or 'Monitor'.

        - `ocsp_err`:The action to be taken when the OCSP response was invalid
                       or the OCSP responder could not be contacted.
                       One 'Drop', 'Decrypt' or 'Monitor'.

        - `ocsp_select_all`:to click 'Select all' for ocsp result handling.
                            One of 'Drop', 'Decrypt' or 'Monitor'.

        - `crypt_nonce`: Use nonce to cryptographically bind OCSP requests
                        and responses.
                        Either 'Yes' or 'No'.

        - `upstream_proxy`: Use an upstream proxy for OCSP checking.
                           Either 'Yes' or 'No'.
                           Set to 'Yes' if an upstream_proxy_grp
                           value is specified.

        - `upstream_proxy_grp`: Select an upstream proxy group for
                                OCSP checking.

        - `exempted_server`: Specify servers exempt from upstream proxy in a
                             comma or space separated format

        Note: ocsp_revoke_cert,ocsp_unk_cert,ocsp_err
              takes precedence over ocsp_select_all

        Example:

        | HTTPS Proxy Edit Settings |
        | ... | ports=45,46 |
        | ... | cert_location=/home/user/cert.pem |
        | ... | cert_key=/home/user/key.pem |
        | ... | key_is_encrypted=${False} |
        | ... | err_expired=drop |
        | ... | err_mismatched=drop |
        | ... | err_unrecognized=monitor |
        | ... | err_invalidsigning=monitor |
        | ... | err_other=monitor |
        | ... | enable_decryption_auth=${True} |
        | ... | enable_decryption_enduser=${True} |
        | ... | enable_decryption_app=${True} |

        | HTTPS Proxy Edit Settings |
        | ... | ports=45,46 |
        | ... | err_select_all=drop |
        | ... | enable_decryption_auth=${False} |
        | ... | enable_decryption_enduser=${False} |
        | ... | enable_decryption_app=${False} |
	| ... | enable_decryption_enduser_notify=${False} |

        | HTTPS Proxy Edit Settings |
        | ... | ocsp_revoke_cert=Drop |
        | ... | ocsp_unk_cert=Decrypt |
        | ... | ocsp_err=Monitor |
        | ... | upstream_proxy=Yes |
        | ... | upstream_proxy_grp=grp1 |
        | ... | exempted_server=1.com |
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

        if cert_location:
            cert_info = dict(zip(self.upload_cert_keys, upload_cert_values))
        elif signed_cert_location:
            cert_info ={'signed_cert':signed_cert_location} #creating the certinfo as dic since same methoed with other options
        else:
            if all(cert_values):
                cert_values.append(cert_constraints)
                cert_info = dict(zip(self.cert_keys, cert_values))
            else:
                cert_info = https_cert_info.DEFAULT

        invalid_cert_values = [err_expired,
                               err_mismatched,
                               err_unrecognized,
                               err_invalidsigning,
                               err_invalidleaf,
                               err_other,
                               err_select_all]

        if err_select_all is not None:
            invalid_cert_handling = dict(zip(self.invalid_cert_keys,
                                             invalid_cert_values))
        else:
            invalid_cert_keys = self.invalid_cert_keys[:-1]
            invalid_cert_values = invalid_cert_values[:-1]

            if any(invalid_cert_values):
                invalid_cert_handling = dict(zip(invalid_cert_keys,
                                                 invalid_cert_values))
            else:
                invalid_cert_handling = None
        ocsp_result_handling_values = [ocsp_revoke_cert,
                                       ocsp_unk_cert,
                                       ocsp_err,
                                       ocsp_select_all]
        if ocsp_select_all is not None:
            ocsp_result_handling = dict(zip(self.ocsp_result_handling_keys,
                                             ocsp_result_handling_values))
        else:
            ocsp_result_handling_keys = self.ocsp_result_handling_keys[:-1]
            ocsp_result_handling_values = ocsp_result_handling_values[:-1]

            if any(ocsp_result_handling_values):
                ocsp_result_handling = dict(zip(ocsp_result_handling_keys,
                                                 ocsp_result_handling_values))
            else:
                ocsp_result_handling = None
        ocsp_timeout_settings_values =  [val_cache_t,
                                         inval_cache_t,
                                         net_cache_t,
                                         clock_skew,
                                         max_time_resp]
        if upstream_proxy:
            if not upstream_proxy_grp:
                raise ValueError(\
                'You must specify upstream_proxy_grp when you'\
                                 ' specify upstream_proxy')
            if any([upstream_proxy_grp,exempted_server]):
                upstream_proxy = 'y'
        if any(ocsp_timeout_settings_values):
            enable_ocsp = True
        self._open_https_proxy_page()
        if not self._check_feature_status(feature='https_proxy'):
            raise guiexceptions.GuiFeatureDisabledError\
                       ('Cannot edit HTTPS proxy as disabled')
        self._click_edit_settings_button()
        self._set_https_ports(ports)
        self._set_decryption_auth(enable_decryption_auth)
	#Enable or disable Decrypt for End-User Notification option
	self._set_decryption_enduser_notify(enable_decryption_enduser_notify)
        self._set_decryption_enduser(enable_decryption_enduser)
        self._set_decryption_app(enable_decryption_app)
        self._select_root_cert_for_signing(cert_info)
        self._invalid_certificate_handling(invalid_cert_handling)
        self._show_advanced()
        if not enable_ocsp:
            self._disable_or_enable_ocsp_checkbox(mode='disable')
        if enable_ocsp:
            self._disable_or_enable_ocsp_checkbox(mode='enable')
            if any(ocsp_timeout_settings_values):
                self._click_on_advanced_ocsp_link()
                self._set_timeout_settings_for_ocsp(dict(zip\
                (self.ocsp_timeout_settings_keys,\
                 ocsp_timeout_settings_values)))
            if ocsp_result_handling:
                for k in ocsp_result_handling.keys():
                    if not ocsp_result_handling[k]:
                        del ocsp_result_handling[k]
                self._ocsp_result_handling(ocsp_result_handling)
            if is_yes(crypt_nonce):
                self._ocsp_enable_or_disable_nonce(mode='enable')
            if is_no(crypt_nonce):
                self._ocsp_enable_or_disable_nonce(mode='disable')
            if is_yes(upstream_proxy):
                self._ocsp_enable_or_disable_upstreamproxy(mode='enable')
                if upstream_proxy_grp:
                    upstreamproxy_dropdown = 'ocsp_proxy_group'
                    upstreamproxy_dropdown_list = \
                        self.get_list_items(upstreamproxy_dropdown)
                    if upstream_proxy_grp not in upstreamproxy_dropdown_list:
                        raise ValueError(\
                        'Invalid upstream_proxy_grp specified- %s'\
                        %upstream_proxy_grp)
                    self._ocsp_select_upstreamproxy\
                               (selected_group=upstream_proxy_grp)
                if exempted_server:
                    self._set_ocsp_exemption_list(exempted_server)
            if is_no(upstream_proxy):
                self._ocsp_enable_or_disable_upstreamproxy(mode='disable')
        self._click_submit_button(wait=False)
        return self.warn

    def ocsp_config_edit_settings(self,
                      enable_ocsp=None,
                      val_cache_t=None,
                      inval_cache_t=None,
                      net_cache_t=None,
                      clock_skew=None,
                      max_time_resp=None,
                      ocsp_revoke_cert=None,
                      ocsp_unk_cert=None,
                      ocsp_err=None,
                      ocsp_select_all=None,
                      crypt_nonce=None,
                      upstream_proxy=None,
                      upstream_proxy_grp=None,
                      exempted_server=None):
        """Edits OCSP options-Can be used to Enable/Disable/Edit OCSP settings

        Parameters:

        - `enable_ocsp`:Enable OCSP (Online Certificate Status Protocol).
                        Enabled by Default . Either 'True or 'False'.

        - `val_cache_t`:
                     Valid response cache timeout(between 1 second and 7 days).
                     Use a trailing 's' for seconds,
                     'm' for minutes 'h' for hours or
                               'd' for days(Default is seconds).

        - `inval_cache_t`:Invalid response cache
                                timeout(between 1 second and 7 days).
                                 Use a trailing 's' for seconds,
                                 'm' for minutes 'h' for hours or
                                 'd' for days(Default is seconds).

        - `net_cache_t`: Network error cache timeout
                                       (between 1 second and 24 hours).
                                      Use a trailing 's' for seconds,
                                      'm' for minutes or
                                       'h' for hours(Default is seconds).

        - `clock_skew`: Allowed clock skew between the OCSP responder and WSA
                        Allowed Values -Between 1 second and 60 minutes.
                       Use a trailing 's' for seconds or 'm' for minutes
                       (Default is seconds).

        - `max_time_resp`: Maximum time for the WSA to wait for an
                                    OCSP response
                                      Allowed Values-Between 1 second and
                                      10 minutes.
                                      Use a trailing 's' for seconds or 'm'
                                      for minutes
                                      (Default is seconds).

        - `ocsp_revoke_cert`:The OCSP responder provided a certificate status
                             of "revoked".
                              Takes one of 'Drop', 'Decrypt' or 'Monitor'.

        - `ocsp_unk_cert`:The OCSP responder provided a certificate status of
                            "unknown".
                              Takes one of 'Drop', 'Decrypt' or 'Monitor'.

        - `ocsp_err`:The OCSP response was invalid or the OCSP responder could
                      not be contacted.
                       Takes one of 'Drop', 'Decrypt' or 'Monitor'.

        - `ocsp_select_all`:To click 'Select all' for OCSP result handling.
                            One of 'Drop', 'Decrypt' or 'Monitor'.

        - `crypt_nonce`: Use nonce to cryptographically bind OCSP requests and
                        responses.
                        Either 'Yes' or 'No'.

        - `upstream_proxy`: Use an upstream proxy for OCSP checking.
                           Either 'Yes' or 'No'.
                           Set to 'Yes' if an upstream_proxy_grp value is
                           specified.

        - `upstream_proxy_grp`: Select an
                               upstream proxy group for OCSP checking.

        - `exempted_server`: Specify servers exempt from upstream proxy in a
                            comma or space separated format

        Note: ocsp_revoke_cert,ocsp_unk_cert,ocsp_err takes precedence over
              ocsp_select_all

        Example:

        | OCSP Config Edit Settings |
        | ... | net_cache_t=5s |
        | ... | ocsp_select_all=Drop |
        | ... | upstream_proxy=Yes |
        | ... | crypt_nonce=Yes |
        | ... | upstream_proxy_grp=grp1 |
        | ... | exempted_server=1.com |

        | OCSP Proxy Edit Settings |
        | ... | enable_ocsp=${False} |

        """
        ocsp_result_handling_values = [ocsp_revoke_cert,
                                       ocsp_unk_cert,
                                       ocsp_err,
                                       ocsp_select_all]
        if ocsp_select_all is not None:
            ocsp_result_handling = dict(zip(self.ocsp_result_handling_keys,
                                             ocsp_result_handling_values))
        else:
            ocsp_result_handling_keys = self.ocsp_result_handling_keys[:-1]
            ocsp_result_handling_values = ocsp_result_handling_values[:-1]

            if any(ocsp_result_handling_values):
                ocsp_result_handling = dict(zip(ocsp_result_handling_keys,
                                                 ocsp_result_handling_values))
            else:
                ocsp_result_handling = None
        ocsp_timeout_settings_values =  [val_cache_t,
                                         inval_cache_t,
                                         net_cache_t,
                                         clock_skew,
                                         max_time_resp]
        if upstream_proxy:
            if not upstream_proxy_grp:
                raise ValueError('You must specify upstream_proxy_grp when you'\
                                 'specify upstream_proxy')
        if any([upstream_proxy_grp,exempted_server]):
            upstream_proxy = 'y'
        if any(ocsp_timeout_settings_values):
            enable_ocsp = True
        self._open_https_proxy_page()
        if not self._check_feature_status(feature='https_proxy'):
            raise guiexceptions.GuiFeatureDisabledError\
                       ('Cannot edit OCSP options as HTTPS proxy is disabled')
        self._click_edit_settings_button()
        if not enable_ocsp:
            self._disable_or_enable_ocsp_checkbox(mode='disable')
        if enable_ocsp:
            self._disable_or_enable_ocsp_checkbox(mode='enable')
            if any(ocsp_timeout_settings_values):
                self._click_on_advanced_ocsp_link()
                self._set_timeout_settings_for_ocsp(dict(\
                zip(self.ocsp_timeout_settings_keys,\
                    ocsp_timeout_settings_values)))
            if ocsp_result_handling:
                for k in ocsp_result_handling.keys():
                    if not ocsp_result_handling[k]:
                        del ocsp_result_handling[k]
                self._ocsp_result_handling(ocsp_result_handling)
            if is_yes(crypt_nonce):
                self._ocsp_enable_or_disable_nonce(mode='enable')
            if is_no(crypt_nonce):
                self._ocsp_enable_or_disable_nonce(mode='disable')
            if is_yes(upstream_proxy):
                self._ocsp_enable_or_disable_upstreamproxy(mode='enable')
                if upstream_proxy_grp:
                    upstreamproxy_dropdown = 'ocsp_proxy_group'
                    upstreamproxy_dropdown_list = \
                    self.get_list_items(upstreamproxy_dropdown)
                    if upstream_proxy_grp not in upstreamproxy_dropdown_list:
                        raise ValueError(\
                        'Invalid upstream_proxy_grp specified -%s'\
                        %upstream_proxy_grp)
                    self._ocsp_select_upstreamproxy\
                    (selected_group=upstream_proxy_grp)
                if exempted_server:
                    self._set_ocsp_exemption_list(exempted_server)
            if is_no(upstream_proxy):
                self._ocsp_enable_or_disable_upstreamproxy(mode='disable')
        self._click_submit_button(wait=False)

    def https_proxy_get_settings(self):
        """Gets HTTPS proxy settings.

        Parameters:
        None

        Example:
        | ${result} | HTTPS Proxy Get Settings |
        """
        ENTRY_ENTITIES = lambda row,col:\
            "xpath=(//table[@class='pairs'])[1]/tbody/tr[%s]%s" % (str(row),col)
        entries = {}

        self._open_https_proxy_page()

        selector_for_count = "(//table[@class='pairs'])[1]/tbody/tr"
        num_of_entries = int(self.get_matching_xpath_count(selector_for_count)) + 1
        self._debug("num_entries %d" % (num_of_entries,))

        for row in xrange(1, num_of_entries):
            if (self._is_element_present(ENTRY_ENTITIES(row, '/td[1]')) and
                    self._is_element_present(ENTRY_ENTITIES(row, '/th[1]'))):
                name = self.get_text(ENTRY_ENTITIES(row, '/th[1]'))
                value = self.get_text(ENTRY_ENTITIES(row, '/td[1]'))
                entries[name] = value
                self._debug("found in row %d: name '%s' value '%s'" % (row, name, value))
        return entries

    def https_proxy_enable(self,
        ports=None,
        enable_decryption_auth=None,
	enable_decryption_enduser_notify=None,
	enable_decryption_enduser=None,
        enable_decryption_app=None,
        cert_name=None,
        cert_org=None,
        cert_org_unit=None,
        cert_country=None,
        cert_duration=None,
        cert_constraints=None,
        cert_location=None,
        cert_key=None,
        key_is_encrypted=None,
        key_password=None,
        err_expired=None,
        err_mismatched=None,
        err_unrecognized=None,
        err_invalidsigning=None,
        err_invalidleaf=None,
        err_other=None,
        err_select_all=None,
        enable_ocsp=None,
        val_cache_t=None,
        inval_cache_t=None,
        net_cache_t=None,
        clock_skew=None,
        max_time_resp=None,
        ocsp_revoke_cert=None,
        ocsp_unk_cert=None,
        ocsp_err=None,
        ocsp_select_all=None,
        crypt_nonce=None,
        upstream_proxy=None,
        upstream_proxy_grp=None,
        exempted_server=None):
        """Enables HTTPS proxy settings and OCSP options.

        Parameters:
        --- HTTPS Ports to Proxy ---
        - `ports`: a comma separated string or list of transparent HTTPS Ports.
        --- Root Certificate for Signing ---
        - `cert_name`: certificate common name, in a string format. Leave empty
         if you are going to upload a new certificate.
        - `cert_org`: certificate organization.
        - `cert_org_unit`: certificate organizational unit.
        - `cert_country`: certificate country.
        - `cert_duration`: duration before certificate expiration in months.
        - `cert_constraints`: set X509v3 basic constraints extension
                           to critical. Either 'True' or 'False'.
        - `cert_location`: location of a certificate file to upload. Leave empty
                        if you are generating new certificate.
        - `cert_key`: location of key file to upload.
        - `key_is_encrypted`: Either 'True' or 'False'
        - `key_password`: password for encrypted key
        --- Decrypt for Authentication ---
        - `enable_decryption_auth`: Enable decryption for authentication.
         Either 'True' or 'False'
        --- Decrypt for End-User Acknowledgement ---
	- `enable_decryption_enduser_notify`: Enable decryption for display of the
         end-user notification  page. Either 'True' or 'False'
        - `enable_decryption_enduser`: Enable decryption for display of the
         end-user acknowledgement page. Either 'True' or 'False'
        --- Decrypt for Application Detection ---
        - `enable_decryption_app`: Enable decryption for enhanced application
         visibility and control. Either 'True' or 'False'
        --- Invalid Certificate Handling ---
        - `cert_key`: location of key file to upload.

        - `err_expired`: expired certificate error. One of 'Drop',
                    'Decrypt' or 'Monitor'.

        - `err_mismatched`: mismatched hostname certificate error.
                    One of 'Drop', 'Decrypt' or 'Monitor'.

        - `err_unrecognized`: unrecognized root authority certificate error.
                       One of 'Drop', 'Decrypt' or 'Monitor'.
        - `err_invalidsigning`: Invalid signing certificate error.
                       One of 'Drop', 'Decrypt' or 'Monitor'.

        - `err_invalidleaf`: Invalid leaf certificate error.
                       One of 'Drop', 'Decrypt' or 'Monitor'.

        - `err_other`: all other error types of certificate errors.
                One of 'Drop', 'Decrypt' or 'Monitor'.

        - `err_select_all`: to click 'Select all' for
                            invalid certificate handling.
                     One of 'Drop', 'Decrypt' or 'Monitor'.

        - `enable_ocsp`: Enable OCSP (Online Certificate Status Protocol).
                        Enabled by Default.
                        Either 'True or 'False'.

        - `val_cache_t`: Valid response cache timeout(between 1 second
                               and 7 days).
                               Use a trailing 's' for seconds, 'm' for minutes
                               'h' for hours or 'd' for days
                               (Default is seconds).

        - `inval_cache_t`: Invalid response cache timeout(between 1
                                 second and 7 days).
                            Use a trailing 's' for seconds, 'm' for minutes
                                 'h' for hours or 'd' for days
                                 (Default is seconds).

        - `net_cache_t`: Network error cache timeout
                                            (between 1 second and 24 hours).
                                      Use a trailing 's' for seconds,
                                      'm' for minutes or 'h' for hours
                                                  (Default is seconds).

        - `clock_skew`: Allowed clock skew between the OCSP responder and WSA
                                            (between 1 second and 60 minutes).
                            Use a trailing 's' for seconds or 'm' for minutes
                                                        (Default is seconds).

        - `max_time_resp`: Maximum time for the WSA to wait for
                                    an OCSP response
                                            (between 1 second and 10 minutes).
                                    Use a trailing 's'
                                    for seconds or 'm' for minutes
                                            (Default is seconds).

        - `ocsp_revoke_cert`:The OCSP responder provided a
                            certificate status of "revoked".
                              One of 'Drop', 'Decrypt' or 'Monitor'.

        - `ocsp_unk_cert`:The OCSP responder provided a certificate
                            status of "unknown".
                              one of 'Drop', 'Decrypt' or 'Monitor'.

        - `ocsp_err`:The OCSP response was invalid or the OCSP responder
                      could not be contacted.
                       one of 'Drop', 'Decrypt' or 'Monitor'.

        - `ocsp_select_all`:to click 'Select all' for ocsp result handling.
                            one of 'Drop', 'Decrypt' or 'Monitor'.

        - `crypt_nonce`: Use nonce to cryptographically bind OCSP
                        requests and responses.
                        Either 'Yes' or 'No'.

        - `upstream_proxy`: Use an upstream proxy for OCSP checking.
                           Either 'Yes' or 'No'.
                           Set to 'Yes' if an upstream_proxy_grp
                           value is specified.

        - `upstream_proxy_grp`: Select an upstream proxy group for
                                OCSP checking.

        - `exempted_server`: Specify servers exempt from upstream proxy
                            in a comma or space separated format.

        Note:- ocsp_revoke_cert,ocsp_unk_cert,ocsp_err takes precedence over
               ocsp_select_all

        Example:
        | HTTPS Proxy Enable |

        | HTTPS Proxy Enable |
        | ... | ports=45,46 |
        | ... | cert_location=/home/user/cert.pem |
        | ... | cert_key=/home/user/key.pem |
        | ... | key_is_encrypted=${True} |
        | ... | key_password=TopSecret |
        | ... | err_expired=drop |
        | ... | err_mismatched=drop |
        | ... | err_unrecognized=monitor |
        | ... | err_invalidsigning=monitor |
        | ... | err_other=monitor |

        | HTTPS Proxy Enable |
        | ... | ports=45,46 |
        | ... | err_select_all=drop |

        | HTTPS Proxy Enable |
        | ... | net_cache_t=5s |
        | ... | ocsp_revoke_cert=Drop |
        | ... | ocsp_unk_cert=Decrypt |
        | ... | ocsp_err=Monitor |
        | ... | upstream_proxy=Yes |
        | ... | crypt_nonce=Yes |
        | ... | upstream_proxy_grp=grp1 |
        | ... | exempted_server=1.com |
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
                cert_values.append(cert_constraints)
                cert_info = dict(zip(self.cert_keys, cert_values))
            else:
                cert_info = https_cert_info.DEFAULT

        invalid_cert_values = [err_expired,
                               err_mismatched,
                               err_unrecognized,
                               err_invalidsigning,
                               err_invalidleaf,
                               err_other,
                               err_select_all]

        if err_select_all is not None:
            invalid_cert_handling = dict(zip(self.invalid_cert_keys,
                                             invalid_cert_values))
        else:
            invalid_cert_keys = self.invalid_cert_keys[:-1]
            invalid_cert_values = invalid_cert_values[:-1]

            if any(invalid_cert_values):
                invalid_cert_handling = dict(zip(invalid_cert_keys,
                                                 invalid_cert_values))
            else:
                invalid_cert_handling = None
        ocsp_result_handling_values = [ocsp_revoke_cert,
                                       ocsp_unk_cert,
                                       ocsp_err,
                                       ocsp_select_all]
        if ocsp_select_all is not None:
            ocsp_result_handling = dict(zip(self.ocsp_result_handling_keys,
                                             ocsp_result_handling_values))
        else:
            ocsp_result_handling_keys = self.ocsp_result_handling_keys[:-1]
            ocsp_result_handling_values = ocsp_result_handling_values[:-1]

            if any(ocsp_result_handling_values):
                ocsp_result_handling = dict(zip(ocsp_result_handling_keys,
                                                 ocsp_result_handling_values))
            else:
                ocsp_result_handling = None
        ocsp_timeout_settings_values =  [val_cache_t,
                                         inval_cache_t,
                                         net_cache_t,
                                         clock_skew,
                                         max_time_resp]
        if upstream_proxy:
            if not upstream_proxy_grp:
                raise ValueError('You must specify upstream_proxy_grp when'\
                                 ' you specify upstream_proxy')
        if any([upstream_proxy_grp,exempted_server]):
            upstream_proxy = 'y'
        if any(ocsp_timeout_settings_values):
            enable_ocsp = True
        self._open_https_proxy_page()
        self._enable_or_edit()
        self._set_https_ports(ports)
        self._set_decryption_auth(enable_decryption_auth)
	#Enable or disable Decrypt for End-User Notification option
	self._set_decryption_enduser_notify(enable_decryption_enduser_notify)
        self._set_decryption_enduser(enable_decryption_enduser)
        self._set_decryption_app(enable_decryption_app)
        self._select_root_cert_for_signing(cert_info)
        self._invalid_certificate_handling(invalid_cert_handling)
        self._show_advanced()
        if not enable_ocsp:
            self._disable_or_enable_ocsp_checkbox(mode='disable')
        if enable_ocsp:
            self._disable_or_enable_ocsp_checkbox(mode='enable')
            if any(ocsp_timeout_settings_values):
                self._click_on_advanced_ocsp_link()
                self._set_timeout_settings_for_ocsp(dict(zip( \
                self.ocsp_timeout_settings_keys,ocsp_timeout_settings_values)))
            if ocsp_result_handling:
                for k in ocsp_result_handling.keys():
                    if not ocsp_result_handling[k]:
                        del ocsp_result_handling[k]
                self._ocsp_result_handling(ocsp_result_handling)
            if is_yes(crypt_nonce):
                self._ocsp_enable_or_disable_nonce(mode='enable')
            if is_no(crypt_nonce):
                self._ocsp_enable_or_disable_nonce(mode='disable')
            if is_yes(upstream_proxy):
                self._ocsp_enable_or_disable_upstreamproxy(mode='enable')
                if upstream_proxy_grp:
                    upstreamproxy_dropdown = 'ocsp_proxy_group'
                    upstreamproxy_dropdown_list = \
                    self.get_list_items(upstreamproxy_dropdown)
                    if upstream_proxy_grp not in upstreamproxy_dropdown_list:
                        raise ValueError(\
                        'Invalid upstream_proxy_grp specified - %s'\
                        %upstream_proxy_grp)
                    self._ocsp_select_upstreamproxy(upstream_proxy_grp)
                if exempted_server:
                    self._set_ocsp_exemption_list(exempted_server)
            if is_no(upstream_proxy):
                self._ocsp_enable_or_disable_upstreamproxy(mode='disable')
        self._click_submit_button(wait=False, accept_confirm_dialog=True)
        return self.warn

    def _set_decryption_auth(self, enable_decryption_auth):
        CHECKBOX="//input[@id='decrypt_https_for_auth_id']"
        self._set_checkbox(enable_decryption_auth, CHECKBOX)

    #Adding option to enble or disable Decrypt for End-User Notification checkbox
    def _set_decryption_enduser_notify(self, enable_decryption_enduser_notify):
        CHECKBOX="//input[@id='decrypt_for_eun_id']"
        self._set_checkbox(enable_decryption_enduser_notify, CHECKBOX)

    def _set_decryption_enduser(self, enable_decryption_enduser):
        CHECKBOX="//input[@id='decrypt_for_eua_id']"
        self._set_checkbox(enable_decryption_enduser, CHECKBOX)

    def _set_decryption_app(self, enable_decryption_app):
        CHECKBOX="//input[@id='apps_use_https']"
        self._set_checkbox(enable_decryption_app, CHECKBOX)
