# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/services/sender_domain_reputation.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $
import functools
import common.gui.guiexceptions as guiexceptions

from common.gui.guicommon import GuiCommon

SENDER_DOMAIN_REPUTATION_PAGE_PATH = ('Security Services', 'Domain Reputation')
SENDER_DOMAIN_REPUTATION_XPATH = "//*[@id='content']/form/dl/dd/table/tbody/tr[1]/td"
SENDER_DOMAIN_REPUTATION_ENABLED_XPATH = "//input[@value='Enable...']"
EDIT_SETTINGS_BUTTON = "//input[@value='Edit Global Settings...']"
ENABLE_SENDER_DOMAIN_FILTERING = "//input[contains(@id, 'enabled') and @type='checkbox']"
ENABLE_EXTENDED_INFORMATION_EXCHANGE = "//input[contains(@id, 'extended_info') and @type='checkbox']"
ENABLE_EXCEPTION_BASED_ON_ENVELOPE_FROM = "//input[@id='env_from_only_match']"
SENDER_DOMAIN_REPUTATION_QUERY_TIMEOUT = "//input[@id='sdr_timeout']"
SENDER_DOMAIN_REPUTATION_STATUS = "//*[@id='content']/form/dl/dd/div[1]"
ENABLE_EXTENDED_INFORMATION_STATE = "//*[@id='content']/form/dl/dd/table/tbody/tr[2]/td"
EXCEPTION_LIST_EDIT_SETTINGS_BUTTON = "//input[@value='Edit Settings...']"
DOMAIN_EXCEPTION_LIST_COMBO = "//select[@id='domain_exception_list']"
SUBMIT_BUTTON = "//input[@value='Submit']"
CANCEL_BUTTON = "//input[@value='Cancel']"
SDR_ADDITIONAL_ATTRIBUTE_AGREEMENT_AGREE = "//button[contains(text(), 'I Agree')]"
SDR_ADDITIONAL_ATTRIBUTE_AGREEMENT_DECLINE = "//button[contains(text(), 'Decline')]"


def go_to_sender_domain_reputation(func):
    """
    This decorator is used to navigate and check Sender_Domain_Reputation feature.
    """

    @functools.wraps(func)
    def worker(self, *args, **kwargs):
        self._debug('Opening "%s" page' % (' -> '.join(SENDER_DOMAIN_REPUTATION_PAGE_PATH),))
        self._navigate_to(*SENDER_DOMAIN_REPUTATION_PAGE_PATH)
        return func(self, *args, **kwargs)

    return worker


class SenderDomainReputation(GuiCommon):
    """Keywords for ESA GUI interaction with
    Security Services -> Sender Domain Reputation
    """

    def get_keyword_names(self):
        return ['sender_domain_reputation_is_enabled',
                'sender_domain_reputation_enable',
                'sender_domain_reputation_disable',
                'sender_domain_reputation_edit_settings',
                'sender_domain_reputation_exception_list']

    @go_to_sender_domain_reputation
    def sender_domain_reputation_is_enabled(self):
        """
        Returns Sender Domain Reputation feature state

        *Parameters:*
        None

        *Return:*
        True if Sender Domain Reputation is enabled or False otherwise

        *Examples:*
        | ${sender_domain_reputation_state}= | Sender Domain Reputation Is Enabled |
        """
        result = False
        sender_domain_reputation = self.get_text(SENDER_DOMAIN_REPUTATION_STATUS)
        if sender_domain_reputation.lower() != 'sender domain reputation is currently disabled.':
            result = True
        return result

    @go_to_sender_domain_reputation
    def sender_domain_reputation_enable(self, *args):
        """
        Enables Sender Domain Reputation feature.

        *Parameters:*
        - `enable_extended_information_exchange`: Boolean flag to enable. Default value: ${False}
        - `sender_domain_reputation_query_timeout`: Value must be an integer from 1 to 10.
        - `enable_exception_based_on_envelope_from`: Match Exception List based on only Envelope-From
        - `accept_additional_attributes_agreement`: SDR inlcude additional attributes agreement. ${True} | ${False}

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed

        *Examples:*
        | Sender Domain Reputation Enable |
        | Sender Domain Reputation Enable | enable_extended_information_exchange=${True}  |
        | Sender Domain Reputation Enable | enable_extended_information_exchange=${False} |
        | Sender Domain Reputation Enable | sender_domain_reputation_query_timeout=7 |
        | Sender Domain Reputation Enable | enable_exception_based_on_envelope_from=${True} |
        | Sender Domain Reputation Enable | enable_exception_based_on_envelope_from=${False} |
        | Sender Domain Reputation Enable |
        | ... | enable_exception_based_on_envelope_from=${True}     |
        | ... | sender_domain_reputation_query_timeout=4            |
        | ... | enable_exception_based_on_envelope_from=${False}    |
        """
        settings = self._parse_args(args)

        if self._is_element_present(SENDER_DOMAIN_REPUTATION_ENABLED_XPATH):
            self.click_button(SENDER_DOMAIN_REPUTATION_ENABLED_XPATH)
            self._select_checkbox(ENABLE_SENDER_DOMAIN_FILTERING)

            if settings.has_key('enable_extended_information_exchange'):
                if settings['enable_extended_information_exchange']:
                    self._select_checkbox(ENABLE_EXTENDED_INFORMATION_EXCHANGE)

            if settings.has_key('sender_domain_reputation_query_timeout'):
                self.input_text(SENDER_DOMAIN_REPUTATION_QUERY_TIMEOUT,
                                settings['sender_domain_reputation_query_timeout'])

            if settings.has_key('enable_exception_based_on_envelope_from'):
                if settings['enable_exception_based_on_envelope_from']:
                    self._select_checkbox(ENABLE_EXCEPTION_BASED_ON_ENVELOPE_FROM)

            self.click_button(SUBMIT_BUTTON, "don't wait")
            self._click_additional_attributes_agreement(settings)
        elif self._is_element_present(CANCEL_BUTTON):
            self.click_button(CANCEL_BUTTON)
        else:
            raise guiexceptions.GuiError('Unknown page')

    @go_to_sender_domain_reputation
    def sender_domain_reputation_disable(self, *args):
        """
        Disables Sender Domain Reputation feature.

        *Parameters:*
        - `accept_additional_attributes_agreement`: SDR inlcude additional attributes agreement. ${True} | ${False}

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed

        *Examples:*
        | Sender Domain Reputation Disable |
        """

        settings = self._parse_args(args)

        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            self._unselect_checkbox(ENABLE_SENDER_DOMAIN_FILTERING)
            self.click_button(SUBMIT_BUTTON, "don't wait")
            self._click_additional_attributes_agreement(settings)
        else:
            self._debug('sender domain reputation feature is already disabled')

    @go_to_sender_domain_reputation
    def sender_domain_reputation_edit_settings(self, *args):
        """
        Edit Sender Domain Reputation settings

        *Parameters:*
        - `enable_extended_information_exchange`: Boolean parameter to enable or disable extended information exchange in
           Sender Domain Reputation.
        - `sender_domain_reputation_query_timeout`: Value must be an integer from 1 to 10.
        - `enable_exception_based_on_envelope_from`: Match Exception List based on only Envelope-From
        - `accept_additional_attributes_agreement`: SDR inlcude additional attributes agreement. ${True} | ${False}

        *Exceptions:*
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | Sender Domain Reputation Edit Settings                 |
        | ... | enable_extended_information_exchange=${False}    |
        | Sender Domain Reputation Edit Settings                 |
        | ... | sender_domain_reputation_query_timeout=6         |
        | Sender Domain Reputation Edit Settings                 |
        | ... | enable_exception_based_on_envelope_from=${True}  |
        | Sender Domain Reputation Edit Settings                 |
        | ... | enable_extended_information_exchange=${True}     |
        | ... | sender_domain_reputation_query_timeout=9         |
        | ... | enable_exception_based_on_envelope_from=${False} |
        """
        settings = self._parse_args(args)
        if settings:
            if self._is_element_present(SENDER_DOMAIN_REPUTATION_ENABLED_XPATH):
                raise guiexceptions.GuiFeatureDisabledError('Sender Domain Reputation feature is not enabled')

            if self._is_element_present(EDIT_SETTINGS_BUTTON):
                self.click_button(EDIT_SETTINGS_BUTTON)

                if settings.has_key('enable_extended_information_exchange'):
                    if settings['enable_extended_information_exchange']:
                        self._select_checkbox(ENABLE_EXTENDED_INFORMATION_EXCHANGE)
                    else:
                        self._unselect_checkbox(ENABLE_EXTENDED_INFORMATION_EXCHANGE)

                if settings.has_key('sender_domain_reputation_query_timeout'):
                    self.input_text(SENDER_DOMAIN_REPUTATION_QUERY_TIMEOUT,
                                    settings['sender_domain_reputation_query_timeout'])

                if settings.has_key('enable_exception_based_on_envelope_from'):
                    if settings['enable_exception_based_on_envelope_from']:
                        self._select_checkbox(ENABLE_EXCEPTION_BASED_ON_ENVELOPE_FROM)
                    else:
                        self._unselect_checkbox(ENABLE_EXCEPTION_BASED_ON_ENVELOPE_FROM)

                self.click_button(SUBMIT_BUTTON, "don't wait")
                self._click_additional_attributes_agreement(settings)
            elif self._is_element_present(CANCEL_BUTTON):
                self.click_button(CANCEL_BUTTON)
            else:
                raise guiexceptions.GuiError('Unknown page')
        else:
            raise guiexceptions.GuiValueError('One of the below parameters are expected:' \
                                              '\n1. enable_extended_information_exchange' \
                                              '\n2.sender_domain_reputation_query_timeout' \
                                              '\n3.enable_exception_based_on_envelope_from')

    @go_to_sender_domain_reputation
    def sender_domain_reputation_exception_list(self, *args):
        """
        Add exception list for sender domain config

        *Parameters:*
        - 'exception_list_name' : name of the global exception list

        *Exceptions:*
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | Sender Domain Reputation Exception List          |
        | ... | exception_list_name=${list_name} |
        """

        settings = self._parse_args(args)
        if settings:
            if self._is_element_present(EXCEPTION_LIST_EDIT_SETTINGS_BUTTON):
                self.click_button(EXCEPTION_LIST_EDIT_SETTINGS_BUTTON)

            if settings.has_key('domain_exception_list_name'):
                if settings['domain_exception_list_name']:
                    self.select_from_list(DOMAIN_EXCEPTION_LIST_COMBO, settings['domain_exception_list_name'])

            self._click_submit_button()

    def _click_additional_attributes_agreement(self, settings={}):
        if settings.has_key('accept_additional_attributes_agreement'):
            if settings['accept_additional_attributes_agreement']:
                if self._is_element_present(SDR_ADDITIONAL_ATTRIBUTE_AGREEMENT_AGREE):
                    self.click_button(SDR_ADDITIONAL_ATTRIBUTE_AGREEMENT_AGREE)
                else:
                    raise guiexceptions.GuiError('Could not find "I Agree" button')
            else:
                if self._is_element_present(SDR_ADDITIONAL_ATTRIBUTE_AGREEMENT_DECLINE):
                    self.click_button(SDR_ADDITIONAL_ATTRIBUTE_AGREEMENT_DECLINE)
                else:
                    raise guiexceptions.GuiError('Could not find "Decline" button')
        else:
            if self._is_element_present(SDR_ADDITIONAL_ATTRIBUTE_AGREEMENT_AGREE):
                self.click_button(SDR_ADDITIONAL_ATTRIBUTE_AGREEMENT_AGREE)
