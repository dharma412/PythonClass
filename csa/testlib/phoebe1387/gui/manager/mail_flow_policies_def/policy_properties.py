#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/mail_flow_policies_def/policy_properties.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author

import copy

from common.gui import guiexceptions


CUSTOM_NAME_FLAG = '<custom>'
CUSTOM_VALUE_FLAG = 'custom'
DEFAULT_VALUE_FLAG = 'default'


class Property(object):
    def __init__(self, gui_common):
        self.gui = gui_common

    @classmethod
    def get_name(cls):
        raise NotImplementedError('Should be implemented in subclasses')

    def set(self, new_value):
        raise NotImplementedError('Should be implemented in subclasses')

    def get(self):
        raise NotImplementedError('Should be implemented in subclasses')


class TextBoxProperty(Property):
    def _get_locator(self):
        """
        *Return:*
        Selenium locator of destination edit box or textarea
        """
        raise NotImplementedError('Should be implemented in subclasses')

    def set(self, new_value):
        self.gui.input_text(self._get_locator(), new_value)

    def get(self):
        return self.gui.get_value(self._get_locator())


class CheckBoxProperty(Property):
    def _get_locator(self):
        """
        *Return:*
        Selenium locator of destination checkbox
        """
        raise NotImplementedError('Should be implemented in subclasses')

    def set(self, new_value):
        self.gui._set_checkbox(new_value, self._get_locator())

    def get(self):
        return self.gui._is_checked(self._get_locator())


class ComboBoxProperty(Property):
    def _get_locator(self):
        """
        *Return:*
        Selenium locator of destination combobox
        """
        raise NotImplementedError('Should be implemented in subclasses')

    def set(self, new_value):
        self.gui.select_from_list(self._get_locator(), new_value)

    def get(self):
        return self.gui.get_value(self._get_locator())


def get_key_by_value(source_dict, value):
    """Return the first ocurence of key containing
    value within source_dict or None if no key
    is found with given value
    """
    for key, val in source_dict.iteritems():
        if val == value:
            return key

class RadioGroupProperty(Property):
    def __init__(self, gui_common, is_default_option_available=True):
        super(RadioGroupProperty, self).__init__(gui_common)
        self._is_default_option_available = is_default_option_available

    def _get_radio_locator(self, name):
        """Return XPath locator of particular radio button
        in group

        *Parameters:*
        - `name`: text contained by the input label.
        If name is <custom> them custom radio locator
        will be returned

        *Exceptions*:
        - `RuntimeError`: if there is no custom control's locator defined
        for radio group with <custom> radio button

        *Return:*
        Radio button locator (if this radio button is present on the current
        web  page) or empty string if not present
        """
        if name == CUSTOM_NAME_FLAG:
            if self._get_custom_input_locator() is None:
                raise RuntimeError('There is no custom control '\
                                   'locator defined for class '\
                                   'named "%s"' % (self.__class__.__name__,))
            prefix = self._get_custom_input_locator()
        else:
            prefix = "//label[starts-with(., '%s')]" % (name,)

        possible_locators = ("%s/preceding-sibling::input[@name='%s'][1]" % (prefix,
                                                    self.get_group_name()),
                             "%s/parent::*/preceding-sibling::input[@name='%s'][1]" % \
                             (prefix, self.get_group_name()))
        for locator in possible_locators:
            if self.gui._is_element_present(locator):
                return locator
        return ''

    def get_group_name(self):
        """
        *Return:*
        The name of each radio in the particular group
        """
        raise NotImplementedError('Should be implemented in subclasses')

    def _get_custom_input_locator(self):
        """
        *Return:*
        Custom input locator. If no custom option is present then it can
        be ignored
        """
        return None

    def _get_options(self):
        """
        *Return:*
        Dictionary with radio group options.
        Key: option name or CUSTOM_NAME_FLAG if this option belongs to custom input
        Value:
        - None flag if this is simple option w/o additional settings
        - `DEFAULT_VALUE_FLAG` flag if this is the default option
        - `CUSTOM_VALUE_FLAG` flag if this is the custom option
        """
        return {'Use Default': DEFAULT_VALUE_FLAG,
                CUSTOM_NAME_FLAG: CUSTOM_VALUE_FLAG}

    def _set_custom_option(self, locator, value):
        """Set custom `value` to control with Selenium locator `locator`
        Override it in subclasses if destination custom is not edit box or
        textarea
        """
        self.gui.input_text(locator, value)

    def _get_custom_option(self, locator):
        """Get value from control with Selenium locator `locator`
        Override it in subclasses if destination custom is not edit box or
        textarea or combo box
        """
        return self.gui.get_value(locator)

    def _check_options_for_default_item(self):
        """
        *Return:*
        Options list with DEFAULT_VALUE_FLAG entry removed
        if _is_default_option_available is set to False
        """
        options = self._get_options()
        if self._is_default_option_available:
            return options
        else:
            new_options = copy.copy(options)
            key = get_key_by_value(new_options, DEFAULT_VALUE_FLAG)
            if key:
                del new_options[key]
            return new_options

    def _set_custom_stuff(self, options, new_value):
        dest_name = get_key_by_value(options, CUSTOM_VALUE_FLAG)
        if dest_name:
            radio_locator = self._get_radio_locator(dest_name)
            if radio_locator:
                self.gui._click_radio_button(radio_locator)
            self._set_custom_option(self._get_custom_input_locator(), new_value)
        else:
            raise ValueError('Unknown value "%s" is set to "%s" property' % \
                             (new_value, self.get_name()))

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: name of option containing fixed option
        or custom value (if this particular radio group contains it)

        *Exceptions:*
        - `ValueError`: if new_value is not present for the particular
        radio group
        - `RuntimeError`: if the particular class does not contain proper
        options to set
        """
        custom_input_locator = self._get_custom_input_locator()
        options = self._check_options_for_default_item()
        if not options:
            raise RuntimeError('The class "%s" does not contain '\
                               'any option to be set' % (self.__class__.__name__,))

        self.gui._debug('Setting value "%s" to "%s"\nAll available options are: %s' % \
                        (new_value, self.get_name(), options))
        if new_value in options.keys():
            radio_locator = self._get_radio_locator(new_value)
            if radio_locator:
                self.gui._click_radio_button(radio_locator)
        elif custom_input_locator is not None:
            # Property is simple control and has no radio buttons
            self._set_custom_stuff(options, new_value)
        else:
            raise ValueError('Unknown value "%s" is passed to "%s" property' % \
                             (new_value, self.get_name()))

    def get(self):
        """
        *Exceptions:*
        - `RuntimeError`: if the current property does not contain
        any option to be set

        *Return:*
        Name of currently selected option in the particular radio group
        or custom option text (if present and selected)
        or empty string if no option is selected
        """
        custom_input_locator = self._get_custom_input_locator()
        options = self._check_options_for_default_item()
        if not options:
            raise RuntimeError('The class "%s" does not contain '\
                               'any option to be set' % (self.__class__.__name__,))

        self.gui._debug('Getting value from "%s"\nAll available options are: %s' % \
                        (self.get_name(), options))
        for option_name, option_type in options.iteritems():
            radio_locator = self._get_radio_locator(option_name)
            if radio_locator and self.gui._is_checked(radio_locator):
                if option_type == CUSTOM_VALUE_FLAG:
                    if custom_input_locator is None:
                        raise RuntimeError('There is no custom input locator'\
                                           ' defined for class "%s"' % \
                                           (self.__class__.__name__,))
                    return self._get_custom_option(custom_input_locator)
                else:
                    return option_name

        if custom_input_locator is not None:
            # Property is simple control and has no radio buttons
            return self._get_custom_option(custom_input_locator)

        return ''


class Name(TextBoxProperty):
    LOCATOR = "//input[@name='new_id']"

    @classmethod
    def get_name(cls):
        return 'Name'

    def _get_locator(self):
        return self.LOCATOR


class ConnectionBehavior(ComboBoxProperty):
    LOCATOR = "//select[@name='behavior']"

    @classmethod
    def get_name(cls):
        return 'Connection Behavior'

    def _get_locator(self):
        return self.LOCATOR


class MaxMsgsPerCon(RadioGroupProperty):
    GROUP_NAME = 'def_max_msgs_per_session'
    CUSTOM_EDIT = "//input[@id='max_msgs_per_session']"

    @classmethod
    def get_name(cls):
        return 'Max. Messages Per Connection'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class MaxRcptsPerMsg(RadioGroupProperty):
    GROUP_NAME = 'def_max_rcpts_per_msg'
    CUSTOM_EDIT = "//input[@id='max_rcpts_per_msg']"

    @classmethod
    def get_name(cls):
        return 'Max. Recipients Per Message'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class MaxMsgSize(RadioGroupProperty):
    GROUP_NAME = 'def_max_message_size'
    CUSTOM_EDIT = "//input[@id='max_message_size']"

    @classmethod
    def get_name(cls):
        return 'Max. Message Size'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class MaxConnFromSingleIP(RadioGroupProperty):
    GROUP_NAME = 'def_max_concurrency'
    CUSTOM_EDIT = "//input[@id='max_concurrency']"

    @classmethod
    def get_name(cls):
        return 'Max. Concurrent Connections From a Single IP'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class CustomSMTPBannerCode(RadioGroupProperty):
    GROUP_NAME = 'def_smtp_banner_code'
    CUSTOM_EDIT = "//input[@id='smtp_banner_code']"

    @classmethod
    def get_name(cls):
        return 'Custom SMTP Banner Code'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class CustomSMTPBannerText(RadioGroupProperty):
    GROUP_NAME = 'def_smtp_banner_text'
    CUSTOM_EDIT = "//textarea[@id='smtp_banner_text']"

    @classmethod
    def get_name(cls):
        return 'Custom SMTP Banner Text'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class OverrideSMTPBannerHostname(RadioGroupProperty):
    GROUP_NAME = 'use_override_hostname'
    CUSTOM_EDIT = "//input[@id='override_hostname']"

    @classmethod
    def get_name(cls):
        return 'Override SMTP Banner Hostname'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
               'Use Hostname from Interface': None,
               CUSTOM_NAME_FLAG: CUSTOM_VALUE_FLAG}


class MaxRecipientsPerHour(RadioGroupProperty):
    GROUP_NAME = 'max_rcpts_per_hour'
    CUSTOM_EDIT = "//input[@id='Nmax_rcpts_per_hour']"

    @classmethod
    def get_name(cls):
        return 'Max. Recipients Per Hour'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Unlimited': None,
                CUSTOM_NAME_FLAG: CUSTOM_VALUE_FLAG}


class MaxRecipientsPerHourCode(RadioGroupProperty):
    GROUP_NAME = 'def_max_rcpts_per_hour_code'
    CUSTOM_EDIT = "//input[@id='max_rcpts_per_hour_code']"

    @classmethod
    def get_name(cls):
        return 'Max. Recipients Per Hour Code'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class MaxRecipientsPerHourText(RadioGroupProperty):
    GROUP_NAME = 'def_max_rcpts_per_hour_text'
    CUSTOM_EDIT = "//textarea[@id='max_rcpts_per_hour_text']"

    @classmethod
    def get_name(cls):
        return 'Max. Recipients Per Hour Text'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class MaxRecipientsPerTimeInterval(RadioGroupProperty):
    GROUP_NAME = 'env_sender_rate_limit_radio'
    CUSTOM_EDIT = "//input[@id='env_sender_rate_limit']"

    @classmethod
    def get_name(cls):
        return 'Max. Recipients Per Time Interval'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Unlimited': None,
                CUSTOM_NAME_FLAG: CUSTOM_VALUE_FLAG}


class SenderRateLimitErrorCode(RadioGroupProperty):
    GROUP_NAME = 'def_env_sender_rate_limit_code'
    CUSTOM_EDIT = "//input[@id='env_sender_rate_limit_code']"

    @classmethod
    def get_name(cls):
        return 'Sender Rate Limit Error Code'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class SenderRateLimitErrorText(RadioGroupProperty):
    GROUP_NAME = 'def_env_sender_rate_limit_text'
    CUSTOM_EDIT = "//textarea[@id='env_sender_rate_limit_text']"

    @classmethod
    def get_name(cls):
        return 'Sender Rate Limit Error Text'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class Exceptions(RadioGroupProperty):
    GROUP_NAME = 'def_env_sender_rate_limit_exceptions'
    CUSTOM_COMBO = "//select[@id='env_sender_rate_limit_exceptions']"

    @classmethod
    def get_name(cls):
        return 'Exceptions'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_COMBO

    def _set_custom_option(self, locator, value):
        self.gui.select_from_list(locator, value)


class UseSenderBaseForFlowControl(RadioGroupProperty):
    GROUP_NAME = 'use_sb'

    @classmethod
    def get_name(cls):
        return 'Use SenderBase for Flow Control'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class GroupBySimilarityOfIPAddresses(RadioGroupProperty):
    GROUP_NAME = 'use_significant_bits'
    CUSTOM_EDIT = "//input[@id='significant_bits']"

    @classmethod
    def get_name(cls):
        return 'Group by Similarity of IP Addresses'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT

    def _get_options(self):
        return {'Off': None,
                CUSTOM_NAME_FLAG: CUSTOM_VALUE_FLAG}


class MaxInvalidRecipientsPerHour(RadioGroupProperty):
    GROUP_NAME = 'dhap_limit'
    CUSTOM_EDIT = "//input[@id='Ndhap_limit']"

    @classmethod
    def get_name(cls):
        return 'Max. Invalid Recipients Per Hour'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Unlimited': None,
                CUSTOM_NAME_FLAG: CUSTOM_VALUE_FLAG}


class DropConnectionIfDHAPThresholdIsReached(RadioGroupProperty):
    GROUP_NAME = 'dhap_action'

    @classmethod
    def get_name(cls):
        return 'Drop Connection if DHAP threshold is Reached'\
               ' within an SMTP Conversation'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class MaxInvalidRecipientsPerHourCode(RadioGroupProperty):
    GROUP_NAME = 'dhap_code'
    CUSTOM_EDIT = "//input[@id='Ndhap_code']"

    @classmethod
    def get_name(cls):
        return 'Max. Invalid Recipients Per Hour Code'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class MaxInvalidRecipientsPerHourText(RadioGroupProperty):
    GROUP_NAME = 'def_dhap_message'
    CUSTOM_EDIT = "//input[@id='dhap_message']"

    @classmethod
    def get_name(cls):
        return 'Max. Invalid Recipients Per Hour Text'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_custom_input_locator(self):
        return self.CUSTOM_EDIT


class SpamDetection(RadioGroupProperty):
    GROUP_NAME = 'spam_check'

    @classmethod
    def get_name(cls):
        return 'Spam Detection'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class AMPDetection(RadioGroupProperty):
    GROUP_NAME = 'amp_check'

    @classmethod
    def get_name(cls):
        return 'AMP Detection'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class VirusProtection(RadioGroupProperty):
    GROUP_NAME = 'virus_check'

    @classmethod
    def get_name(cls):
        return 'Virus Protection'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class SenderDomainReputationVerification(RadioGroupProperty):
    GROUP_NAME = 'sdr_check'

    @classmethod
    def get_name(cls):
        return 'Sender Domain Reputation Verification'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}

class VirusOutbreakFilters(RadioGroupProperty):
    GROUP_NAME = 'vof_check'

    @classmethod
    def get_name(cls):
        return 'Virus Outbreak Filters'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}

class AdvancedPhishingProtection(RadioGroupProperty):
    GROUP_NAME = 'app_check'

    @classmethod
    def get_name(cls):
        return 'Advanced Phishing Protection'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}

class GraymailDetection(RadioGroupProperty):
    GROUP_NAME = 'graymail_check'

    @classmethod
    def get_name(cls):
        return 'Graymail Detection'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}

class ContentFilters(RadioGroupProperty):
    GROUP_NAME = 'cfilter_check'

    @classmethod
    def get_name(cls):
        return 'Content Filters'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}

class MessageFilters(RadioGroupProperty):
    GROUP_NAME = 'mfilter_check'

    @classmethod
    def get_name(cls):
        return 'Message Filters'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}

class TLS(RadioGroupProperty):
    GROUP_NAME = 'tls'

    @classmethod
    def get_name(cls):
        return 'TLS'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Off': None,
                'Preferred': None,
                'Required': None}


class VerifyClientCert(CheckBoxProperty):
    LOCATOR = "//input[@id='tls_verify']"

    @classmethod
    def get_name(cls):
        return 'Verify Client Certificate'

    def _get_locator(self):
        return self.LOCATOR


class SMTPAuthentication(RadioGroupProperty):
    GROUP_NAME = 'smtpauth_allow'

    @classmethod
    def get_name(cls):
        return 'SMTP Authentication'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Off': None,
                'Preferred': None,
                'Required': None}


class TLSIsMandatoryForAddressList(ComboBoxProperty):
    LOCATOR = "//select[@name='tls_exceptions']"

    @classmethod
    def get_name(cls):
        return 'TLS is Mandatory for Address List'

    def _get_locator(self):
        return self.LOCATOR


class RequireTLSToOfferSMTPAuth(CheckBoxProperty):
    LOCATOR = "//input[@id='smtpauth_requiretls']"

    @classmethod
    def get_name(cls):
        return 'Require TLS To Offer SMTP Authentication'

    def _get_locator(self):
        return self.LOCATOR


class DomainKeyDKIMSigning(RadioGroupProperty):
    GROUP_NAME = 'dkim_signing'

    @classmethod
    def get_name(cls):
        return 'Domain Key/DKIM Signing'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class DKIMVerification(RadioGroupProperty):
    GROUP_NAME = 'dkim_verification'

    @classmethod
    def get_name(cls):
        return 'DKIM Verification'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class DKIMVerificationProfile(ComboBoxProperty):
    LOCATOR = "//select[@id='dkim_verification_profile']"

    @classmethod
    def get_name(cls):
        return 'Use DKIM Verification Profile'

    def _get_locator(self):
        return self.LOCATOR


class SMIMEDecryptionVerification(RadioGroupProperty):
    GROUP_NAME = 'smime_gw_verification'

    @classmethod
    def get_name(cls):
        return 'S/MIME DecryptionVerification'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class SMIMESignatureProcessing(RadioGroupProperty):
    GROUP_NAME = 'remove_smime_signature'

    @classmethod
    def get_name(cls):
        return 'S/MIME SignatureProcessing'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Preserve': None,
                'Remove': None}


class SMIMEPublicKeyHarvesting(RadioGroupProperty):
    GROUP_NAME = 'smime_certificate_harvesting'

    @classmethod
    def get_name(cls):
        return 'S/MIME PublicKeyHarvesting'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Disable': None,
                'Enable': None}


class SMIMEHarvestCertificateOnFailure(RadioGroupProperty):
    GROUP_NAME = 'harvest_on_failure'

    @classmethod
    def get_name(cls):
        return 'S/MIME HarvestCertificateOnFailure'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Disable': None,
                'Enable': None}


class SMIMEStoreUpdatedCertificate(RadioGroupProperty):
    GROUP_NAME = 'store_updated_certs'

    @classmethod
    def get_name(cls):
        return 'S/MIME StoreUpdatedCertificate'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Disable': None,
                'Enable': None}


class SPFSIDFProfile(RadioGroupProperty):
    GROUP_NAME = 'spf_profile'

    @classmethod
    def get_name(cls):
        return 'SPF/SIDF Verification'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class DMARCVerification(RadioGroupProperty):
    GROUP_NAME = 'dmarc_verification'

    @classmethod
    def get_name(cls):
        return 'DMARC Verification'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class DMARCVerificationProfile(ComboBoxProperty):
    LOCATOR = "//select[@name='dmarc_verification_profile']"

    @classmethod
    def get_name(cls):
        return 'Use DMARC Verification Profile'

    def _get_locator(self):
        return self.LOCATOR


class DMARCFeedbackReports(CheckBoxProperty):
    LOCATOR = "//input[@id='dmarc_agg_reports']"

    @classmethod
    def get_name(cls):
        return 'DMARC Feedback Reports'

    def _get_locator(self):
        return self.LOCATOR


class ConformanceLevel(ComboBoxProperty):
    LOCATOR = "//select[@id='spf_conformance_level']"

    @classmethod
    def get_name(cls):
        return 'Conformance Level'

    def _get_locator(self):
        return self.LOCATOR


class DowngradePRAVerificationResult(RadioGroupProperty):
    GROUP_NAME = 'spf_downgrade'

    @classmethod
    def get_name(cls):
        return 'Downgrade PRA verification result '\
            'if \'Resent-Sender:\' or \'Resent-From:\' were used'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'No': None,
                'Yes': None}


class HELOTest(RadioGroupProperty):
    GROUP_NAME = 'spf_helo'

    @classmethod
    def get_name(cls):
        return 'HELO Test'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Off': None,
                'On': None}


class ConsiderUntaggedBouncesToBeValid(RadioGroupProperty):
    GROUP_NAME = 'accept_untagged_bounces'

    @classmethod
    def get_name(cls):
        return 'Consider Untagged Bounces to be Valid'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'Yes': None,
                'No': None}


class EnvelopeSenderDNSVerification(RadioGroupProperty):
    GROUP_NAME = 'sender_vrfy'

    @classmethod
    def get_name(cls):
        return 'Envelope Sender DNS Verification'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class MalformedEnvelopeSendersSMTPCode(TextBoxProperty):
    LOCATOR = "//input[@name='sender_vrfy_bad_domain_smtp_code']"

    @classmethod
    def get_name(cls):
        return 'Malformed Envelope Senders SMTP Code'

    def _get_locator(self):
        return self.LOCATOR


class MalformedEnvelopeSendersSMTPText(TextBoxProperty):
    LOCATOR = "//input[@name='sender_vrfy_bad_domain_smtp_text']"

    @classmethod
    def get_name(cls):
        return 'Malformed Envelope Senders SMTP Text'

    def _get_locator(self):
        return self.LOCATOR


class EnvelopeSendersWhoseDomainDoesNotResolveSMTPCode(TextBoxProperty):
    LOCATOR = "//input[@name='sender_vrfy_servfail_smtp_code']"

    @classmethod
    def get_name(cls):
        return 'Envelope Senders whose domain does not resolve SMTP Code'

    def _get_locator(self):
        return self.LOCATOR


class EnvelopeSendersWhoseDomainDoesNotResolveSMTPText(TextBoxProperty):
    LOCATOR = "//input[@name='sender_vrfy_servfail_smtp_text']"

    @classmethod
    def get_name(cls):
        return 'Envelope Senders whose domain does not resolve SMTP Text'

    def _get_locator(self):
        return self.LOCATOR


class EnvelopeSendersWhoseDomainDoesNotExistSMTPCode(TextBoxProperty):
    LOCATOR = "//input[@name='sender_vrfy_nxdomain_smtp_code']"

    @classmethod
    def get_name(cls):
        return 'Envelope Senders whose domain does not exist SMTP Code'

    def _get_locator(self):
        return self.LOCATOR


class EnvelopeSendersWhoseDomainDoesNotExistSMTPText(TextBoxProperty):
    LOCATOR = "//input[@name='sender_vrfy_nxdomain_smtp_text']"

    @classmethod
    def get_name(cls):
        return 'Envelope Senders whose domain does not exist SMTP Text'

    def _get_locator(self):
        return self.LOCATOR


class UseSenderVerificationExceptionTable(RadioGroupProperty):
    GROUP_NAME = 'domain_exception'

    @classmethod
    def get_name(cls):
        return 'Use Sender Verification Exception Table'

    def get_group_name(self):
        return self.GROUP_NAME

    def _get_options(self):
        return {'Use Default': DEFAULT_VALUE_FLAG,
                'On': None,
                'Off': None}


class CustomSMTPRejectBannerCode(TextBoxProperty):
    LOCATOR = "//input[@id='reject_banner_code']"

    @classmethod
    def get_name(cls):
        return 'Custom SMTP Reject Banner Code'

    def _get_locator(self):
        return self.LOCATOR


class CustomSMTPRejectBannerText(TextBoxProperty):
    LOCATOR = "//textarea[@id='reject_banner_text']"

    @classmethod
    def get_name(cls):
        return 'Custom SMTP Reject Banner Text'

    def _get_locator(self):
        return self.LOCATOR
