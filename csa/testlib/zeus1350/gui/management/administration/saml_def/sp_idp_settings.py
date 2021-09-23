# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/administration/saml_def/sp_idp_settings.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

from common.gui.guiexceptions import ConfigError
from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs


class ServiceProviderSettings(InputsOwner):
    SP_NAME = ("SP Profile Name", "//input[@name='sp_name']")
    SP_ENTITY_ID = ("SP Entity ID", "//input[@name='sp_entity_id']")
    SP_NAME_ID_FORMAT = ("Name ID Format", "//textarea[@id='name_id_format']")
    SP_ACS_URL = ("Assertion Consumer URL", "//textarea[@id='sp_acs_location']")
    SP_CERTIFICATE = ("SP Certificate", "//input[@id='sp_certificate']")
    SP_PRIVATE_KEY = ("Private Key", "//input[@id='sp_cert_key']")
    SP_CERT_PASSWORD = ("Certificate Passphrase", "//input[@id='sp_cert_passphrase']")
    SP_SIGN_REQUESTS = ("Sign Requests", "//input[@id='sp_sign_requests_enable']")
    SP_SIGN_ASSERTIONS = ("Sign Assertions", "//input[@id='sp_sign_assertions_enable']")
    SP_ORG_NAME = ("Organization Name", "//input[@name='sp_org_name']")
    SP_ORG_DISPLAY_NAME = ("Organization Display Name", "//input[@name='sp_org_display_name']")
    SP_ORG_URL = ("Organization URL", "//input[@name='sp_org_url']")
    SP_TECHNICAL_CONTACT = ("Organization Technical Contact", "//input[@name='sp_tech_contact']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def set(self, new_value):
        self._set_edits(new_value,
                        self.SP_NAME,
                        self.SP_ENTITY_ID,
                        self.SP_NAME_ID_FORMAT,
                        self.SP_ACS_URL,
                        self.SP_CERTIFICATE,
                        self.SP_PRIVATE_KEY,
                        self.SP_CERT_PASSWORD,
                        self.SP_ORG_NAME,
                        self.SP_ORG_DISPLAY_NAME,
                        self.SP_ORG_URL,
                        self.SP_TECHNICAL_CONTACT)
        self._set_checkboxes(new_value,
                             self.SP_SIGN_REQUESTS,
                             self.SP_SIGN_ASSERTIONS)

    def get(self):
        raise NotImplementedError()


class IdentityProviderSettings(InputsOwner):
    IDP_NAME = ("IDP Profile Name", "//input[@name='idp_name']")
    IDP_CONFIGURATION_RADIO_BUTTON = (
        "Configuration Mode", {
            "Configure Keys Manually": "//input[@id='metadata_not_uploaded']",
            "Import IDP Metadata": "//input[@id='metadata_uploaded']"
        })
    IDP_ENTITY_ID = ("IDP Entity ID", "//input[@name='idp_entity_id']")
    IDP_SSO_URL = ("SSO URL", "//textarea[@name='idp_sso_url']")
    IDP_CERTIFICATE = ("Certificate", "//input[@id='idp_cert_file']")
    IDP_METADATA = ("Import IDP Metadata", "//input[@id='metadata_xml_id']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def set(self, new_value):
        self._set_radio_groups(new_value,
                               self.IDP_CONFIGURATION_RADIO_BUTTON)
        if new_value.has_key('Configuration Mode') and \
                new_value['Configuration Mode'].lower() == 'configure keys manually':
            self._set_edits(new_value,
                            self.IDP_NAME,
                            self.IDP_ENTITY_ID,
                            self.IDP_SSO_URL,
                            self.IDP_CERTIFICATE)
        elif new_value.has_key('Configuration Mode') and \
                new_value['Configuration Mode'].lower() == 'import idp metadata':
            self._set_edits(new_value, self.IDP_NAME, self.IDP_METADATA)
        else:
            raise ConfigError('"Configuration Mode" is a mandatory parameter.' \
                              + ' Allowed values are: "Configure Keys Manually" or "Import IDP Metadata"')

    def get(self):
        raise NotImplementedError()
