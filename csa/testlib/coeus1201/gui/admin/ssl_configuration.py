#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/ssl_configuration.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

class SSLConfiguration(GuiCommon):
    ui_elements_tls = {
        "MENU_ADMIN"         : "System Administration",
        "SUBMENU_SSL_CONFIG" : "SSL Configuration",
        "EDIT_SETTINGS"      : "//input[@value='Edit Settings']",
        "CIPHER_PROXY"       : "//textarea[@id='Proxy_ciphers']",
        "CIPHER_ERROR"       : "//div[@id='error_area_Proxy_ciphers']",
        "TLS_COMPRESSION"    : "//input[@id='Proxy_compression']",
        "SUBMIT_BUTTON"      : "//input[@value='Submit']",
        "RESULTS"            : "//span[@id='action-results-title']",
        "MSG"                : "//*[@id='action-results-message']"
    }

    #Valid list of services supported in ssl configuration
    services_list = ['application_mgmt', 'proxy', 'ldaps' , 'sicap', 'update']

    #Locators of the check box of tls/sslv3 protocol version in each service
    proxy = {
        'tls_1dot0': "//input[@id='Proxy_TLSv1.0']",
        'tls_1dot1' : "//input[@id='Proxy_TLSv1.1']",
        'tls_1dot2' : "//input[@id='Proxy_TLSv1.2']",
        'ssl_v3'    : "//input[@id='Proxy_SSLv3.0']"
    }

    application_mgmt = {
        'tls_1dot0' : "//input[@id='WebUI_TLSv1.0']",
        'tls_1dot1': "//input[@id='WebUI_TLSv1.1']",
        'tls_1dot2': "//input[@id='WebUI_TLSv1.2']",
        'ssl_v3'    : "//input[@id='WebUI_SSLv3.0']"
    }

    ldaps = {
        'tls_1dot0' : "//input[@id='LDAPS_TLSv1.0']",
        'tls_1dot1': "//input[@id='LDAPS_TLSv1.1']",
        'tls_1dot2': "//input[@id='LDAPS_TLSv1.2']",
        'ssl_v3'    : "//input[@id='LDAPS_SSLv3.0']"
    }
    sicap = {
        'tls_1dot0': "//input[@id='SICAP_TLSv1.0']",
        'tls_1dot2' : "//input[@id='SICAP_TLSv1.2']",
        'tls_1dot1' : "//input[@id='SICAP_TLSv1.1']",
        'ssl_v3'    : "//input[@id='SICAP_SSLv3.0']"
    }
    update = {
        'tls_1dot0' : "//input[@id='Updater_TLSv1.0']",
        'tls_1dot1': "//input[@id='Updater_TLSv1.1']",
        'tls_1dot2': "//input[@id='Updater_TLSv1.2']",
        'ssl_v3'    : "//input[@id='Updater_SSLv3.0']"
    }

    services_matrix = {
        'application_mgmt' :  application_mgmt,
        'proxy'                         :  proxy,
        'ldaps'                         :  ldaps,
        'sicap'                         :   sicap,
        'update'                     :   update
    }

    def get_keyword_names(self):
        return [
                'edit_ssl_configuration',
                'edit_ssl_cipher',
        ]

    def _get_ui_element(self,ui_element):
        self._info("Read Locator |  Locator: %s" %self.ui_elements_tls[ui_element])
        return self.ui_elements_tls[ui_element]

    def _open_page(self):
        """
        Navigate to SSL Configuration page
        """
        self._navigate_to(self._get_ui_element('MENU_ADMIN'), self._get_ui_element('SUBMENU_SSL_CONFIG'))

    def edit_ssl_configuration(self, proxy=None, ldaps=None, application_mgmt=None, sicap=None, update=None, compression=None, cipher=None):
        """
        Supported matrix
        application_mgmt      | tls1dot2 | tls1dot1 | tls1dot0 | sslv3 |
        proxy                           | tls1dot2 | tls1dot1 | tls1dot0 | sslv3 |
        ldaps                           | tls1dot2 | tls1dot1 | tls1dot0 | sslv3 |
        sicap                           | tls1dot2 | tls1dot1 | tls1dot0 | sslv3 |
        update                        | tls1dot2 | tls1dot1 | tls1dot0 | sslv3 |

        #Provide tls_version with y/n value separated by # for a given service
        and each tls version separated by ,
        Examples:
        Edit Ssl Configuration | proxy=tls1dot2#y,tls1dot1#y,tls1dot0#n,sslv3#n |
        | ldaps=tls1dot0#y,tls1dot1#y,tls1dot2#n,sslv3#n |
        | sicap=tls1dot0#y,tls1dot1#y,tls1dot2#n,sslv3#n |
        | application_mgmt=tls1dot0#y,tls1dot1#y,tls1dot2#n,sslv3#n |
        | proxy=tls1dot0#y,tls1dot1#y,tls1dot2#n,sslv3#n |
        | update=tls1dot0#y,tls1dot1#y,tls1dot2#n,sslv3#n |
        | compression=disable |
        | cipher=RC4-MD5:EXP-DHE-RSA-DES-CBC-SHA |

        Edit Ssl Configuration | proxy=tls1dot1#y,tls1dot0#n,sslv3#n |
        | compression=enable |
        Edit Ssl Configuration | compression=disable |

        Note:If disable option is chosen , tls compression will be disabled for proxy service
        """
        self._open_page()
        try:
            self._wait_until_element_is_present(self._get_ui_element('EDIT_SETTINGS'), 15)
        except:
            self._info("UI Element not preset. UI Element: Edit Settings | %s" %(self._get_ui_element('EDIT_SETTINGS')))
            self._info("Code will attempt to click inspite")

            
        self.click_button(self._get_ui_element('EDIT_SETTINGS'))

        if proxy:
            self._info("Proxy : %s" %proxy)
            enabled,disabled = self._helper(proxy)
            self._edit_ssl_configuration('proxy',enabled,disabled)

        if ldaps:
            self._info("Secure LDAP : %s" %ldaps)
            enabled,disabled = self._helper(ldaps)
            self._edit_ssl_configuration('ldaps',enabled,disabled)

        if application_mgmt:
            self._info("Application Management Service : %s" %application_mgmt)
            enabled,disabled = self._helper(application_mgmt)
            self._edit_ssl_configuration('application_mgmt',enabled,disabled)

        if sicap:
            self._info("Secure ICAP : %s" %sicap)
            enabled,disabled = self._helper(sicap)
            self._edit_ssl_configuration('sicap',enabled,disabled)

        if update:
            self._info("Update Service : %s" %update)
            enabled,disabled = self._helper(update)
            self._edit_ssl_configuration('update',enabled,disabled)

        if compression:
            compression = compression.strip().lower()
            self._info("Got %s as compression value" %compression)
            if compression in ['enable', 'disable']:
                self._info("Got %s value present in valid list" %compression)
                
                CHECKBOX = self._get_ui_element('TLS_COMPRESSION')
                self._info('TLS compression: %s' % compression)

                disable_option = False
                if compression == 'disable':
                    disable_option = True
                self._info('DEBUG : disable_option - %s' %disable_option)
                self._click_checkbox(disable_option, CHECKBOX)
            else:
                raise ValueError('Invalid TLS compression value: %s\n'\
                    'Valid options for Compression: enable | disable' %(compression))

        if cipher is not None:
            #Set the CIPHER String if CIPHER was passed.
            self.input_text(self._get_ui_element('CIPHER_PROXY'), "")
            self.input_text(self._get_ui_element('CIPHER_PROXY'), cipher)
            self.check_for_warning()

        SUBMIT = self._get_ui_element('SUBMIT_BUTTON')
        self.click_button(SUBMIT)
        self.check_for_warning()
        #Check if error is shown
        status,error_msg = self._check_for_error()
        if error_msg != "":
            self._info("GOT ERROR - %s" %error_msg)
            raise guiexceptions.GuiValueError(error_msg)

    def _edit_ssl_configuration(self, service, enable_list, disable_list):
        '''
        Appropriate protocol version is selected basedon the enabled/disabled list
        '''
        #Validating if the service is supported in ssl configuration
        self._info("Service: %s" %service)
        if service not in self.services_list:
            raise ValueError('Invalid service | Service: \'%s\'\n'\
            'Valid options for service are:\n'\
            '%s' % (service, "\n".join(self.services_list)))

        #Setting the tls/ssl version supported in each service
        #if service == 'proxy' or service == 'sicap':
            #protocol_versions = ['tls_1dot2', 'tls_1dot1', 'tls_1dot0', 'ssl_v3']
        #else:
            #protocol_versions = ['tls_1dot0' , 'ssl_v3']

        #All protocols are supported across services
        protocol_versions = ['tls_1dot2', 'tls_1dot1', 'tls_1dot0', 'ssl_v3']

        ############### Handling Enabled List##########################
        for tls in enable_list:
            if tls not in protocol_versions:
                raise ValueError('TLS Version not supported for service | TLS Version: \'%s\' | Service: \'%s\'' %(tls, service))
            self._info("Enabling TLS Version: %s for Service :%s" %(tls, service))
            enable = True
            CHECKBOX = self.services_matrix[service][tls]
            self._info("Enable | CHECKBOX value: %s" %CHECKBOX)
            self._click_checkbox(enable, CHECKBOX)
        ############### Handling Disabled List##########################
        for tls in disable_list:
            if tls not in protocol_versions:
                raise ValueError('TLS Version not supported for service | TLS Version: \'%s\' | Service: \'%s\'' % (tls, service))

            self._info("Disabling TLS Version: %s for Service :%s" %(tls,service))
            enable = False
            CHECKBOX = self.services_matrix[service][tls]
            self._info("Disable | CHECKBOX value: %s" %CHECKBOX)
            self._click_checkbox(enable, CHECKBOX)

    def edit_ssl_cipher(self, cipher = None):
        '''
        Edits the cipher suite to be used in proxy service
        Examples:
        | Edit Ssl Cipher | RC4-MD5:EXP-DHE-RSA-DES-CBC-SHA |

        '''
        self._open_page()
        self.click_button(self._get_ui_element('EDIT_SETTINGS'))
        self.input_text(self._get_ui_element('CIPHER_PROXY'), "")
        self.input_text(self._get_ui_element('CIPHER_PROXY'), cipher)
        self.check_for_warning()
        SUBMIT = self._get_ui_element('SUBMIT_BUTTON')
        self.click_button(SUBMIT)
        #Check if warning is shown for invalid ciphers
        status, error_msg = self._check_for_error()
        if error_msg != "":
            error_msg = self.get_text(self._get_ui_element('CIPHER_ERROR'))
            self._info("GOT ERROR - %s" %error_msg)
            raise ValueError\
                  ('Cipher value is invalid...'\
                  'Got this ERROR MSG- %s' %(error_msg))

    def _edit_tls_compression(self, action = None):
        '''
        If action = disable, checkbox is selected for disabling tls compression
        in proxy service and vice versa
        Allowed options are:
        action = enable | disable
        '''
        self._open_page()
        self.click_button(self._get_ui_element('EDIT_SETTINGS'))
        CHECKBOX = self._get_ui_element('TLS_COMPRESSION')
        self._info('Going to %s TLS compression' % action)
        #self.click_element(CHECKBOX, "don't wait")
        disable_option = False
        if action == 'disable':
            disable_option = True
        self._info('DEBUG : disable_option - %s' %disable_option)
        self._click_checkbox(disable_option,CHECKBOX)
        SUBMIT = self._get_ui_element('SUBMIT_BUTTON')
        self.click_button(SUBMIT)

    def _click_checkbox(self,enable,CHECKBOX):
        '''
        The given checkbox is unchecked or checked based on 'enable' value
        '''
        if enable and not self._is_checked(CHECKBOX):
            self._info("Enabling tls version ...")
            self.click_element(CHECKBOX, "don't wait")
        if not enable and self._is_checked(CHECKBOX):
            self._info("Disabling tls version ...")
            self.click_element(CHECKBOX, "don't wait")

    def _helper(self,service):
        '''
        Parses the argument of tls verisons with y/n value
        and return the list of tls_versions to be enabled and
        tls_versions to be disabled for service
        '''
        protocols = service.split(',')
        print "Protocols- ", protocols
        tls1dot2 = tls1dot1 = tls1dot0 = sslv3 = None
        for p in protocols:
            ver, value = p.split('#')
            ver = ver.strip().lower()
            value = str(value).strip().lower()
            print ver,value

            if ver == 'tls1dot2':
                tls1dot2 = value
            if ver == 'tls1dot1':
                tls1dot1 = value
            if ver == 'tls1dot0':
                tls1dot0 = value
            if ver == 'sslv3':
                sslv3 = value

        enabled = []
        disabled = []
        #Setting the list of the tls/ssl versions to be enabled and disabled
        if tls1dot2:
            enabled.append('tls_1dot2') if tls1dot2 == 'y' else disabled.append('tls_1dot2')
        if tls1dot1:
            enabled.append('tls_1dot1') if tls1dot1 == 'y' else disabled.append('tls_1dot1')
        if tls1dot0:
            enabled.append('tls_1dot0') if tls1dot0 == 'y' else disabled.append('tls_1dot0')
        if sslv3:
            enabled.append('ssl_v3') if sslv3 == 'y' else disabled.append('ssl_v3')
        self._info("Enabled tls versions: %s " %str(enabled))
        self._info("Disabled tls versions: %s " %str(disabled))

        return enabled,disabled

    def _check_for_error(self):
        '''
        Checks if operation performed in ssl configuration page resulted in Success/Error
        Returns the status as Success/Error
        If error occurred, the error message is returned
        '''
        status = self.get_text(self._get_ui_element('RESULTS'))
        if status == "Error":
            err_msg = self.get_text(self._get_ui_element('MSG'))
        else:
            err_msg = ""
        return status,err_msg

