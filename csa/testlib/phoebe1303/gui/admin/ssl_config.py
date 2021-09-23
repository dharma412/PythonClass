#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/ssl_config.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

from ssl_config_def.ssl_config_settings import SSLConfigSettings


EDIT_SETTINGS_BUTTON = "//input[@value='Edit Settings...']"
CANCEL_BUTTON = "//input[@value='Cancel']"

PAGE_PATH = ('System Administration', 'SSL Configuration')

class SSLConfig(GuiCommon):
    def get_keyword_names(self):
        return ['ssl_configuration_settings_edit',
                'ssl_configuration_settings_get_all']

    def _get_ssl_conf_settings_controller(self):
        if not hasattr(self, '_ssl_conf_settings_controller'):
            self._ssl_conf_settings_controller = SSLConfigSettings(self)
        return self._ssl_conf_settings_controller

    @go_to_page(PAGE_PATH)
    def ssl_configuration_settings_edit(self, settings):
        """Edit SSL configuration settings

        *Parameters:*
        - `settings`: dictionary, whose items can be:
        | <category> Method TLS v1 | whether to enable TLS v1 for <category> |
        | <category> Method SSL v3 | whether to enable SSL v3 for <category> |
        | <category> Method SSL v2 | whether to enable SSL v2 for <category> |
        | <category> SSL Cipher(s) to use | what SSL Cipher(s) to use for
        <category>. All ciphers should be separated by colon char |

        Possible <category> values are:
        | GUI HTTPS |
        | Inbound SMTP |
        | Outbound SMTP |

        *Examples:*
        | ${settings}= | Create Dictionary |
        | :FOR | ${category} | IN | GUI HTTPS | Inbound SMTP | Inbound SMTP |
        | \ | Set To Dictionary | ${settings} |
        | \ | ... | ${category} Method TLS v1 | ${True} |
        | \ | ... | ${category} Method SSL v3 | ${False} |
        | \ | ... | ${category} Method SSL v2 | ${False} |
        | \ | ... | ${category} SSL Cipher(s) to use | RC4-SHA:RC4-MD5:ALL |
        | SSL Configuration Settings Edit | ${settings} |

	*Examples:*
        | ${settings}= | Create Dictionary |
        | :FOR | ${category} | IN | GUI HTTPS | Inbound SMTP
        | \ | Set To Dictionary | ${settings} |
        | \ | ... | ${category} Method TLS v1 | ${True} |
        | \ | ... | ${category} Method SSL v3 | ${False} |
        | \ | ... | ${category} Method SSL v2 | ${False} |
	| \ | ... | ${category} Method TLS v1.2 | ${True} |
        | \ | ... | ${category} SSL Cipher(s) to use | RC4-SHA:RC4-MD5:ALL |
	| \ | ... | ${category} TLS Renegotiation Enable | ${False} |
        | SSL Configuration Settings Edit | ${settings} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        controller = self._get_ssl_conf_settings_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def ssl_configuration_settings_get_all(self):
        """Get SSL configuration settings

        *Return:*
        - Dictionary. It has same set of items as in the `settings`
        parameter of `SSL Configuration Settings Edit` keyword

        *Examples:*
        | ${changed_settings}= | SSL Configuration Settings Get All |
        | Log Dictionary | ${changed_settings} |
        | ${inbound_smtp_method_sslv3}= | Get From Dictionary |
        | ... | ${changed_settings} | Inbound SMTP Method SSL v3 |
        | Should Be True |
        | ... | ${settings}['Inbound SMTP Method SSL v3'] == ${inbound_smtp_method_sslv3} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        controller = self._get_ssl_conf_settings_controller()
        result = controller.get()
        self.click_button(CANCEL_BUTTON)
        return result
