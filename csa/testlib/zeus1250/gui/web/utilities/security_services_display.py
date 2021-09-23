#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/utilities/security_services_display.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
# $Author: sarukakk $

from sal.containers import cfgholder

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

from sma.constants import sma_config_masters

masters_map = {
    sma_config_masters.CM91 : 'coeus_8_5_',
    sma_config_masters.CM105 : 'coeus_10_5_',
    sma_config_masters.CM110 : 'coeus_10_0_',
    sma_config_masters.CM115 : 'coeus_10_0_',
    sma_config_masters.CM117 : 'coeus_11_7_',
    sma_config_masters.CM118 : 'coeus_11_8_'
}

EDIT_SETTINGS_BUTTON = 'xpath=//input[@value="Edit Display Settings..."]'
CM_STATUS_LABEL = lambda cm: '//label[contains(@for, \'%s\')]' % (masters_map[cm],)
ENABLE_CM_CHECKBOX = lambda cm: 'id=%senabled' % (masters_map[cm],)
OPTION_LOCATOR = lambda cm, attribute: masters_map[cm] + attribute
CONTINUE_BUTTON = '//button[text() ="Continue"]'
CONFIRM_SCANNING_YES_BUTTON = "//div[@id='confirmation_dialog']//button[normalize-space(text())='Yes']"

TRANS_MODE = lambda cm_name: 'id=%sbypass_proxy' % (masters_map[cm_name],)
FTP_PROXY = lambda cm_name: 'id=%sftp' % (masters_map[cm_name],)
HTTPS_PROXY = lambda cm_name: 'id=%shttps' % (masters_map[cm_name],)
SOCKS_PROXY = lambda cm_name: 'id=%ssocks' % (masters_map[cm_name],)
UPSTREAM_PROXY_GROUP = lambda cm_name: 'id=%srouting' % (masters_map[cm_name],)
ACCEPTABLE_USE_CONTROLS = lambda cm_name: 'id=%surl_filtering' % (masters_map[cm_name])
AVC = lambda cm_name: 'id=%savc' % (masters_map[cm_name])
CONNECT_SECURE_MOBILITY = lambda cm_name: 'id=%smus' % (masters_map[cm_name])
WEB_REPUTATION_FILTERS = lambda cm_name: 'id=%swbrs' % (masters_map[cm_name])
ACTIVE_SCRIPTING = lambda cm_name: 'id=%sadaptive_scanning' % (masters_map[cm_name])
WEBROOT_ANTI_MALWARE= lambda cm_name: 'id=%smerlin' % (masters_map[cm_name])
MACFEE_ANTI_MALWARE = lambda cm_name: 'id=%smcafee' % (masters_map[cm_name])
SOPHOS_ANTI_MALWARE = lambda cm_name: 'id=%ssophos' % (masters_map[cm_name])
END_USER_ACK = lambda cm_name: 'id=%senable_splash_page' % (masters_map[cm_name])
DATA_SECURITY_FILTERS = lambda cm_name: 'id=%sdlp_onbox' % (masters_map[cm_name])
EXTERNAL_DLP_SERVERS = lambda cm_name: 'id=%sexternal_dlp' % (masters_map[cm_name])
CREDENTIAL_ENCRYPTION = lambda cm_name: 'id=%suse_secure_client_auth' % (masters_map[cm_name])
IDENTITY_PROVIDER_FOR_SAAS = lambda cm_name: 'id=%ssaas' % (masters_map[cm_name])

LIST_LABEL = lambda label: 'label=%s' % (label,)
URL_FILTERING_LIST = lambda cm_name: 'id=%surl_filtering_select' % (masters_map[cm_name])
MUS_LIST = lambda cm_name: 'id=%smus_select' % (masters_map[cm_name])

AUC_MODE_FIRESTONE = "Cisco IronPort Web Usage Controls"

AMP = lambda cm_name: 'id=%samp_file_rep' % (masters_map[cm_name])
AMP_FILE_ANLYSIS = lambda cm_name: 'id=%samp_file_analysis' % (masters_map[cm_name])

class SecurityServicesDisplay(GuiCommon):
    """ Keywords for interaction with Web -> Utilities ->
        Security Service Display GUI page
    """

    def get_keyword_names(self):
        return [
            'security_services_display_get_settings',
            'security_services_display_hide_cm',
            'security_services_display_unhide_cm',
            'security_services_display_edit_cm_settings',
        ]

    def _open_page(self):
        self._navigate_to('Web', 'Utilities', 'Security Services Display')

    def _verify_cm_name(self, name):
        if name not in masters_map:
            raise guiexceptions.GuiValueError('Invalid %s name for Configuration Master' %\
                (name,))

    def _verify_cm_initialized(self, cm_name):
        status_text = self.get_text(CM_STATUS_LABEL(cm_name))
        if 'not initialized' in status_text.lower():
            raise guiexceptions.GuiFeatureDisabledError(status_text)

    def _verify_cm_not_hidden(self, cm_name):
        if not self._is_checked(ENABLE_CM_CHECKBOX(cm_name)):
            raise guiexceptions.ConfigError('%s is hidden' % (cm_name,))

    def _check_enable_cm_checkbox(self, cm):
        self.select_checkbox(ENABLE_CM_CHECKBOX(cm))

    def _uncheck_enable_cm_checkbox(self, cm):
        self.unselect_checkbox(ENABLE_CM_CHECKBOX(cm))

    def _click_edit_settings_button(self):
        try:
            self.click_button(EDIT_SETTINGS_BUTTON)
        except Exception as error:
            if self._is_text_present('Centralized Configuration Manager is currently disabled.'):
                raise guiexceptions.GuiFeatureDisabledError('Centralized Configuration Manager is currently disabled')

    def _get_attributes(self, cm):
        if cm == sma_config_masters.CM91:
            available_attributes = DisplayOptions.cm91_attributes
        elif cm == sma_config_masters.CM105:
            available_attributes = DisplayOptions.cm105_attributes
        elif cm == sma_config_masters.CM110:
            available_attributes = DisplayOptions.cm110_attributes
        elif cm == sma_config_masters.CM115:
            available_attributes = DisplayOptions.cm115_attributes
        elif cm == sma_config_masters.CM117:
            available_attributes = DisplayOptions.cm117_attributes
        elif cm == sma_config_masters.CM118:
            available_attributes = DisplayOptions.cm118_attributes

        return available_attributes

    def _retrieve_options(self, cm):
        available_attributes = self._get_attributes(cm)
        options = DisplayOptions(cm)

        for attribute in available_attributes:
            locator = OPTION_LOCATOR(cm, attribute)
            if  self._is_checked(locator):
                options[attribute] = True
            elif not self._is_checked(locator):
                options[attribute] = False
            else:
                options[attribute] = value

        return options

    def _click_continue_button(self):
        if self._is_element_present(CONTINUE_BUTTON):
            self.click_button(CONTINUE_BUTTON)

    def _select_checkbox(self, locator, mode):
        if mode is not None:
            if not mode:
                self.unselect_checkbox(locator)
            else:
                if not self._is_checked(locator):
                    self.click_element(locator, "don't wait")

    def _is_enabled(self, mode):
        if mode is None:
            return "wasn't changed"
        else:
            if mode:
                return 'enabled'
            else:
                return 'disabled'

    def _set_transparent_mode(self, cm, mode):
        self._select_checkbox(TRANS_MODE(cm), mode)
        self._info('Trasparent mode %s' % (self._is_enabled(mode),))

    def _set_ftp_proxy(self, cm, mode):
        self._select_checkbox(FTP_PROXY(cm), mode)
        self._info('Ftp proxy %s' % (self._is_enabled(mode),))

    def _set_https_proxy(self, cm, mode):
        self._select_checkbox(HTTPS_PROXY(cm), mode)
        self._info('Http proxy %s' % (self._is_enabled(mode),))

    def _set_socks_proxy(self, cm, mode):
        self._select_checkbox(SOCKS_PROXY(cm), mode)
        self._info('SOCKS proxy %s' % (self._is_enabled(mode),))

    def _set_upstream_proxy_groups(self, cm, mode):
        self._select_checkbox(UPSTREAM_PROXY_GROUP(cm), mode)
        self._info('Upstream proxy groups %s' % (self._is_enabled(mode),))

    def _set_acceptable_use_controls(self, cm, mode, avc_mode=None):
        if mode is not None:
            if not mode :
                self.unselect_checkbox(ACCEPTABLE_USE_CONTROLS(cm))
                self._info('Disabled acceptable use controls')
            else:
                if not self._is_checked(ACCEPTABLE_USE_CONTROLS(cm)):
                    self.click_element(ACCEPTABLE_USE_CONTROLS(cm), "don't wait")
                if not isinstance(mode, bool):
                    self.select_from_list(URL_FILTERING_LIST(cm), mode)
                else:
                    self._select_checkbox(AVC(cm), avc_mode)
                self._info('Enabled acceptable use controls')

    def _set_any_connect_secure_mobility(self, cm, mode):
        if cm != sma_config_masters.CM63 and mode is not None:
            if not mode:
                self.unselect_checkbox(CONNECT_SECURE_MOBILITY(cm))
                self._info('Disabled anyConnect secure mobility')
            else:
                if not self._is_checked(CONNECT_SECURE_MOBILITY(cm)):
                   self.click_element(CONNECT_SECURE_MOBILITY(cm), "don't wait")
                if not isinstance(mode, bool):
                    self.select_from_list(MUS_LIST(cm), LIST_LABEL(mode))
                self._info('Enabled anyConnect secure mobility')

    def _set_web_reputation_filters(self, cm, mode, scanning=None):
        if mode is not None:
            if not mode:
                self.unselect_checkbox(WEB_REPUTATION_FILTERS(cm))
                self._info('Disabled web reputation filters')
            else:
                if not self._is_checked(WEB_REPUTATION_FILTERS(cm)):
                    self.click_element(WEB_REPUTATION_FILTERS(cm), "don't wait")
                self._info('Enabled web reputation filters')
                if cm in (sma_config_masters.CM91, sma_config_masters.CM105, sma_config_masters.CM110, sma_config_masters.CM117):
                    self._select_checkbox(ACTIVE_SCRIPTING(cm), bool(scanning))
                if self._is_element_present(CONFIRM_SCANNING_YES_BUTTON):
                    self.click_element(CONFIRM_SCANNING_YES_BUTTON, "don't wait")

    def _set_webroot_anti_malware(self, cm, mode):
        self._select_checkbox(WEBROOT_ANTI_MALWARE(cm), mode)
        self._info('Webroot anti-malware %s' % (self._is_enabled(mode),))

    def _set_mcafee_anti_malware(self, cm, mode):
        self._select_checkbox(MACFEE_ANTI_MALWARE(cm), mode)
        self._info('Mcafee anti-malware %s' % (self._is_enabled(mode),))

    def _set_sophos_anti_malware(self, cm, mode):
        if cm != sma_config_masters.CM63:
            self._select_checkbox(SOPHOS_ANTI_MALWARE(cm), mode)
            self._info('Sophos  anti-malware %s' % (self._is_enabled(mode),))

    def _set_end_user_ack(self, cm, mode):
        self._select_checkbox(END_USER_ACK(cm), mode)
        self._info('End user acknowledgement %s' % (self._is_enabled(mode),))

    def _set_data_security_filters(self, cm, mode):
        self._select_checkbox(DATA_SECURITY_FILTERS(cm), mode)
        self._info('Data security filters %s' % (self._is_enabled(mode),))

    def _set_external_dlp_servers(self, cm, mode):
        self._select_checkbox(EXTERNAL_DLP_SERVERS(cm), mode)
        self._info('External dlp servers %s' % (self._is_enabled(mode),))

    def _set_credential_encryption(self, cm, mode):
        if cm != sma_config_masters.CM63:
            self._select_checkbox(CREDENTIAL_ENCRYPTION(cm), mode)
            self._info('Credential encryption %s' % (self._is_enabled(mode),))

    def _set_identity_provider_for_saas(self, cm, mode):
        if cm != sma_config_masters.CM63:
            self._select_checkbox(IDENTITY_PROVIDER_FOR_SAAS(cm), mode)
            self._info('Identity provider for saa %s' % (self._is_enabled(mode),))

    def _set_advanced_malware_protection(self, cm, mode, file_analysis):
        if cm == sma_config_masters.CM91:
            self._select_checkbox(AMP(cm), mode)
            self._info('Advanced Malware Protection %s' % \
                (self._is_enabled(mode),))
            if mode:
                self._select_checkbox(AMP_FILE_ANLYSIS(cm), file_analysis)
                self._info('Enable File Analysis %s' % \
                    (self._is_enabled(file_analysis),))

    def _configure_cm_settings(self, cm_name, transparent_mode=None,
            ftp_proxy=None, https_proxy=None, upstream_proxy_groups=None,
            acceptable_use_controls=None, avc_mode=None,
            any_connect_secure_mobility=None,web_reputation_filters=None,
            scanning=None, webroot_anti_malware=None, mcafee_anti_malware=None,
            sophos_anti_malware=None,
            end_user_ack=None, data_security_filters=None,
            external_dlp_servers=None, credential_encryption=None,
            identity_provider_for_saas=None, socks_proxy=None,
            amp_file_rep=None, amp_file_analysis=None):

        self._set_transparent_mode(cm_name, transparent_mode)

        self._set_ftp_proxy(cm_name, ftp_proxy)

        self._set_https_proxy(cm_name, https_proxy)

        self._set_socks_proxy(cm_name, socks_proxy)

        self._set_acceptable_use_controls(cm_name, acceptable_use_controls, avc_mode)

        self._set_any_connect_secure_mobility(cm_name, any_connect_secure_mobility)

        self._set_upstream_proxy_groups(cm_name, upstream_proxy_groups)

        self._set_web_reputation_filters(cm_name, web_reputation_filters, scanning)

        self._set_webroot_anti_malware(cm_name, webroot_anti_malware)

        self._set_mcafee_anti_malware(cm_name, mcafee_anti_malware)

        self._set_sophos_anti_malware(cm_name, sophos_anti_malware)

        self._set_end_user_ack(cm_name, end_user_ack)

        self._set_data_security_filters(cm_name, data_security_filters)

        self._set_external_dlp_servers(cm_name, external_dlp_servers)

        self._set_credential_encryption(cm_name, credential_encryption)

        self._set_identity_provider_for_saas(cm_name, identity_provider_for_saas)

        self._set_advanced_malware_protection(cm_name, amp_file_rep, amp_file_analysis)

    def security_services_display_get_settings(self, cm_name):
        """Retrieve information about Configuration Master settings.

        Parameters:
            - `cm_name`: name of the Configuration Master to receive settings.

        Return:
            Object that contain information about Configuration Master and has
            the following attributes:
            - `cm`: name of the Configuration Master settings should apply to.
            - `bypass_proxy`: display transparent mode options.
            - `https`: display HTTPS proxy options.
            - `routing`: display upstream proxy options.
            - `wbrs`: display WBRS options.
            - `merlin`: display Webroot options.
            - `mcafee`: display McAfee options.
            - `enable_splash_page`: display EUA options.
            - `ftp`: display FTP proxy options.
            - `url_filtering`: display URL filtering options.
            - `url_filtering_select`: URL filtering engine to select.
            - `dlp_onbox`: display IDS Filters options.
            - `external_dlp`: display external DLP server options.
            - `avc`: display AVC options.
            - `mus`: display MUS options.
            - `mus_select`: settings for identifying remote users.
            - `sophos`: display Sophos options.
            - `use_secure_client_auth`: display credential encryption options.
            - `saas`: display SaaS options.
            - `adaptive_scanning`: display Adaptive Scanning.
            - `socks`: display SOCKS proxy options.
            - `amp_file_rep`: setting for Advanced Malware Protection.
            - `amp_file_analysis`: setting for Enable File Analysis.

        Examples:
            | ${options} | Security Services Display Get Settings | ${sma_config_masters.CM75} |

        Exceptions:
            - `GuiFeatureDisabledError`: in case if Configuration Masters are
              not initialized; in case if Centralized Configuration Manager is
              disabled'.
            - `GuiValueError`: in case if invalid Configuration Master
              specified.
        """
        self._open_page()

        self._verify_cm_name(cm_name)

        self._click_edit_settings_button()

        self._verify_cm_initialized(cm_name)

        self._verify_cm_not_hidden(cm_name)

        result = self._retrieve_options(cm_name)

        return result

    def security_services_display_unhide_cm(self, cm_name):
        """Unhide (enable) Configuration Master.

        Parameters:
            - `cm_name`: name of the Configuration Master to unhide.

        Examples:
            | Security Services Display Unhide Cm | ${sma_config_masters.CM75} |
            | Security Services Display Unhide Cm | ${sma_config_masters.CM77} |

        Exceptions:
            - `GuiFeatureDisabledError`: in case if Configuration Masters are
              not initialized; in case if Centralized Configuration Manager is
              disabled'.
            - `GuiValueError`: in case if invalid Configuration Master
              specified.
        """
        self._open_page()

        self._verify_cm_name(cm_name)

        self._click_edit_settings_button()

        self._verify_cm_initialized(cm_name)

        self._check_enable_cm_checkbox(cm_name)

        self._click_submit_button()

    def security_services_display_hide_cm(self, cm_name):
        """Hide (disable) Configuration Master.

        Parameters:
            - `cm_name`: name of the Configuration Master to hide.

        Examples:
            | Security Services Display Hide Cm | ${sma_config_masters.CM75} |
            | Security Services Display Hide Cm | ${sma_config_masters.CM77} |

        Exceptions:
            - `GuiFeatureDisabledError`: in case if Configuration Masters are
              not initialized; in case if Centralized Configuration Manager is
              disabled'.
            - `GuiValueError`: in case if invalid Configuration Master
              specified.
        """
        self._open_page()

        self._verify_cm_name(cm_name)

        self._click_edit_settings_button()

        self._verify_cm_initialized(cm_name)

        self._uncheck_enable_cm_checkbox(cm_name)

        self._click_submit_button()

    def security_services_display_edit_cm_settings(self, cm_name,
                            transparent_mode=None,
                            ftp_proxy=None,
                            https_proxy=None,
                            upstream_proxy_groups=None,
                            acceptable_use_controls=None,
                            avc_mode=None,
                            any_connect_secure_mobility=None,
                            web_reputation_filters=None,
                            scanning=None,
                            webroot_anti_malware=None,
                            mcafee_anti_malware=None,
                            sophos_anti_malware=None,
                            end_user_ack=None,
                            data_security_filters=None,
                            external_dlp_servers=None,
                            credential_encryption=None,
                            identity_provider_for_saas=None,
                            socks_proxy=None,
                            amp_file_rep=None,
                            amp_file_analysis=None):
        """ Edit Security Services Display Settings.

        Parameters:
            - `cm_name`: name of the Configuration Master which settings will
              be edited. String.
            - `transparent_mode`: display transparent mode options. Boolean
              value to enable/disable.
            - `ftp_proxy`: display FTP proxy option. Boolean value to
              enable/disable.
            - `https_proxy`: display HTTPS proxy option. Boolean value to
              enable/disable.
            - `acceptable_use_controls`: display URL filtering options. Boolean
              value to enable/disable.
            - `avc_mode`: display Application Visibility and Control.
            - `upstream_proxy_groups`: display upstream proxy groups option.
              Boolean value to enable/disable.
            - `any_connect_secure_mobility`: display AnyConnect Secure Mobility
              option. Boolean value to enable/disable. Not boolean to specify
              one of the available options: "IP Range" or "Cisco ASA".
            - `web_reputation_filters`: display web reputation filters option.
              Boolean value to enable/disable.
              option will not be changed.
            - `scanning`: display Adaptive Scanning. Available only for
              configuration Master 7.5 and 7.7 if web_reputation_filters is enabled.
            - `webroot_anti_malware`:  display webroot anti-malware option.
              Boolean value to enable/disable.
            - `mcafee_anti_malware`: display mcafee anti-malware option.
              Boolean value to enable/disable.
            - `sophos_anti_malware`: display sophos anti-malware option.
              Boolean value to enable/disable.
            - `end_user_ack`: display End user acknowledgement option. Boolean
              value to enable/disable.
            - `data_security_filters`: display data security filters option.
              Boolean value to enable/disable.
            - `external_dlp_servers`: display external dlp servers option.
              Boolean value to enable/disable.
            - `credential_encryption`: display credential encryption option.
              Boolean value to enable/disable.
            - `identity_provider_for_saas`: display Identity Provider for SaaS
              option. Boolean value to enable/disable.
              If one of the options above is None, it will not be changed.
            - `socks_proxy`: display SOCKS proxy options.
              Boolean value to enable/disable.
            - `amp_file_rep`: setting for Advanced Malware Protection.
              Boolean value to enable/disable.
            - `amp_file_analysis`: setting for Enable File Analysis.
              Boolean value to enable/disable. Available if amp_file_rep is enabled.

        Examples:
            | Security Services Display Edit Cm Settings | ${sma_config_masters.CM75} | transparent_mode=${False} |
            | Security Services Display Edit Cm Settings | ${sma_config_masters.CM77} | socks_proxy=${True} |

        Exceptions:
            - `GuiFeatureDisabledError`: in case if Configuration Masters are
              not initialized; in case if Centralized Configuration Manager is
              disabled'.
            - `GuiValueError`: in case if invalid Configuration Master
              specified.
        """

        self._open_page()

        self._verify_cm_name(cm_name)

        self._click_edit_settings_button()

        self._verify_cm_initialized(cm_name)

        self._verify_cm_not_hidden(cm_name)

        self._configure_cm_settings(cm_name, transparent_mode, ftp_proxy,
                https_proxy, upstream_proxy_groups, acceptable_use_controls,
                avc_mode, any_connect_secure_mobility,
                web_reputation_filters, scanning,
                webroot_anti_malware, mcafee_anti_malware, sophos_anti_malware,
                end_user_ack, data_security_filters, external_dlp_servers,
                credential_encryption, identity_provider_for_saas, socks_proxy,
                amp_file_rep, amp_file_analysis)

        #self._click_submit_button(False)
        self._click_submit_button(wait=False, accept_confirm_dialog=True)

        self._click_continue_button()

class DisplayOptions(cfgholder.CfgHolder):
    """Class holding configuration settings for Display of Security Services.

    Attributes:
        Common for all Configuration Masters:
            - `cm`: name of the Configuration Master settings should apply to.
              String.
            - `all`: used only to enable or disable all options in one shot.
              Boolean. If this option is set all other options are neglected.

            - `bypass_proxy': display transparent mode options.
            - `ftp`: display FTP proxy options.
            - `https`: display HTTPS proxy options.
            - `routing`: display upstream proxy options.

            - `url_filtering`: display URL filtering options. Boolean value to
               enable/disable.
            - `url_filtering_select`: URL filtering engine to select. Applies
               only if `url_filtering` is True.
            - `avc`: display AVC options. Appies only if `url_filtering` is
              'cisco'.

            - `mus`: display MUS options.
            - `mus_select`: settings for identifying remote users. String.
               Applies only is `mus` is True.

            - `wbrs`: display WBRS options.
            - `merlin`: display Webroot options.
            - `mcafee`: display McAfee options.
            - `sophos`: display Sophos options.

            - `enable_splash_page`: display EUA options.

            - `dlp_onbox`: display IDS Filters options.
            - `external_dlp`: display external DLP server options.
            - `use_secure_client_auth`: display credential encryption options.
            - `saas`: display SaaS options.

            Additional attributes for Configuration Master 7.5
            - `adaptive_scanning`: display Adaptive Scanning. Available only
              if wbrs is enabled.

            Additional attributes for Configuration Master 7.7. See attributes
            for Configuration Master 7.5 and also.
            - `socks`: display SOCKS proxy options.

            Additional attributes for Fuego build
            - `amp_file_rep`: setting for Advanced Malware Protection.
            - `amp_file_analysis`: setting for Enable File Analysis.

    Exceptions:
        - `GuiValueError`: in case if invalid Configuration Master specified.
    """
    common_attributes = ('bypass_proxy', 'https', 'routing', 'wbrs',
                    'merlin', 'mcafee', 'enable_splash_page' ,'ftp',
                    'url_filtering', 'dlp_onbox', 'external_dlp',
                    'url_filtering_select', 'avc', 'mus', 'mus_select',
                    'sophos', 'use_secure_client_auth', 'saas',
                    'adaptive_scanning')
    cm91_attributes = common_attributes
    cm105_attributes = cm91_attributes + ('socks',)
    cm110_attributes = cm105_attributes + ('amp_file_rep', 'amp_file_analysis')
    cm115_attributes = cm110_attributes
    cm117_attributes = cm115_attributes
    cm118_attributes = cm117_attributes

    def __init__(self, cm, all=None, **kwargs):
        cfgholder.CfgHolder.__init__(self, {'cm': cm, 'all': all})

        if str(cm) == sma_config_masters.CM91:
            attributes = self.cm91_attributes
        elif str(cm) == sma_config_masters.CM105:
            attributes = self.cm105_attributes
        elif str(cm) == sma_config_masters.CM110:
            attributes = self.cm110_attributes
        elif str(cm) == sma_config_masters.CM115:
            attributes = self.cm115_attributes
        elif str(cm) == sma_config_masters.CM117:
            attributes = self.cm117_attributes
        elif str(cm) == sma_config_masters.CM118:
            attributes = self.cm118_attributes
        else:
            raise guiexceptions.GuiValueError('Invalid Configuration Master name: %s' % (cm,))

        for attribute in attributes: self[attribute] = kwargs.get(attribute)
