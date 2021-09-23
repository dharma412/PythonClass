#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/manager/mail_flow_policies_def/policy_edit_controllers.py#2 $ $DateTime: 2019/10/03 22:25:46 $ $Author


from common.gui.decorators import set_speed

from policy_properties import Name, ConnectionBehavior, MaxMsgsPerCon, \
    MaxRcptsPerMsg, MaxMsgSize, MaxConnFromSingleIP, CustomSMTPBannerCode, \
    CustomSMTPBannerText, OverrideSMTPBannerHostname, MaxRecipientsPerHour, \
    MaxRecipientsPerHourCode, MaxRecipientsPerHourText, MaxRecipientsPerTimeInterval, \
    SenderRateLimitErrorCode, SenderRateLimitErrorText, Exceptions, \
    UseSenderBaseForFlowControl, GroupBySimilarityOfIPAddresses, \
    MaxInvalidRecipientsPerHour, DropConnectionIfDHAPThresholdIsReached, \
    MaxInvalidRecipientsPerHourCode, MaxInvalidRecipientsPerHourText, \
    SpamDetection, VirusProtection, TLS, AMPDetection, \
    VerifyClientCert, SMTPAuthentication, TLSIsMandatoryForAddressList, \
    RequireTLSToOfferSMTPAuth, DomainKeyDKIMSigning, DKIMVerification, ConformanceLevel, \
    SMIMEDecryptionVerification, DowngradePRAVerificationResult, HELOTest, ConsiderUntaggedBouncesToBeValid, \
    SMIMESignatureProcessing, SMIMEPublicKeyHarvesting, SMIMEHarvestCertificateOnFailure, SMIMEStoreUpdatedCertificate, \
    EnvelopeSenderDNSVerification, MalformedEnvelopeSendersSMTPCode, \
    MalformedEnvelopeSendersSMTPText, EnvelopeSendersWhoseDomainDoesNotResolveSMTPCode, \
    EnvelopeSendersWhoseDomainDoesNotResolveSMTPText, \
    EnvelopeSendersWhoseDomainDoesNotExistSMTPCode, \
    EnvelopeSendersWhoseDomainDoesNotExistSMTPText, UseSenderVerificationExceptionTable, \
    CustomSMTPRejectBannerCode, CustomSMTPRejectBannerText, \
    DKIMVerificationProfile, SPFSIDFProfile, \
    DMARCVerification, DMARCVerificationProfile, DMARCFeedbackReports, \
    RadioGroupProperty


class PolicyEditContainer(object):
    def __init__(self, gui_common):
        self.gui = gui_common
        self.__properties_cache = {}

    def get_owned_properties(self):
        """
        *Return*
        List of property classes managed by this container
        All classes should be descendants of Property base class
        """
        raise NotImplementedError('Should be implemented in subclasses')

    def _create_property_object(self, prop_class):
        """
        *Parameters:*
        - `prop_class`: property class, descendant of Property base class

        *Return:*
        `prop_class` class instance
        """
        return prop_class(self.gui)

    def _get_property_object(self, name):
        """
        *Parameters:*
        - `name`: name of property owned by this container

        *Exceptions:*
        - `ValueError`: if unknown property name is passed

        *Return:*
        Property object got from local cache (or newly created if was not
        present in cache)
        """
        if name in self.__properties_cache.keys():
            return self.__properties_cache[name]
        else:
            dest_property_cls = filter(lambda x: x.get_name() == name,
                                       self.get_owned_properties())
            if dest_property_cls:
                self.__properties_cache[name] = \
                    self._create_property_object(dest_property_cls[0])
                return self.__properties_cache[name]
            else:
                raise ValueError('Unknown property name "%s" is passed to a ' \
                                 'properties container "%s"' % (name,
                                                                self.__class__.__name__))

    def set_property(self, name, new_value):
        dest_prop = self._get_property_object(name)
        dest_prop.set(new_value)

    def get_property(self, name):
        dest_prop = self._get_property_object(name)
        return dest_prop.get()

    @set_speed(0.1, 'gui')
    def set(self, settings):
        """Set settings to the particular edit form

        *Parameters:*
        - `settings`: dictionary containing settings.
        Dictionary keys are setting names and values are its values

        *Exceptions:*
        - `ValueError`: if any of passed settings name/value is not correct
        """
        for name, value in settings.iteritems():
            self.set_property(name, value)

    @set_speed(0, 'gui')
    def get(self):
        """Return dictionary with all form properties

        *Return*
        Dictionary whose keys are property names
        and values contains its values
        """
        details = {}
        all_names = map(lambda x: x.get_name(),
                        self.get_owned_properties())
        for name in all_names:
            details[name] = self.get_property(name)
        return details


class CustomPolicyEdit(PolicyEditContainer):
    def get_owned_properties(self):
        return (  # Name
            Name,
            # Connection Behavior
            ConnectionBehavior,
            # Connections
            MaxMsgsPerCon,
            MaxRcptsPerMsg, MaxMsgSize, MaxConnFromSingleIP,
            # SMTP
            CustomSMTPBannerCode,
            CustomSMTPBannerText, OverrideSMTPBannerHostname,
            # Rate Limit for Hosts
            MaxRecipientsPerHour,
            MaxRecipientsPerHourCode, MaxRecipientsPerHourText,
            # Rate Limit for Envelope Senders
            MaxRecipientsPerTimeInterval, SenderRateLimitErrorCode,
            SenderRateLimitErrorText, Exceptions,
            # Flow Control
            UseSenderBaseForFlowControl, GroupBySimilarityOfIPAddresses,
            # Directory Harvest Attack Prevention (DHAP)
            MaxInvalidRecipientsPerHour,
            DropConnectionIfDHAPThresholdIsReached,
            MaxInvalidRecipientsPerHourCode, MaxInvalidRecipientsPerHourText,
            # Spam Detection
            SpamDetection,
            # AMP Detection
            AMPDetection,
            # Virus Protection
            VirusProtection,
            # Encryption and Authentication
            TLS, VerifyClientCert, SMTPAuthentication,
            TLSIsMandatoryForAddressList, RequireTLSToOfferSMTPAuth,
            # Domain Key/DKIM Signing
            DomainKeyDKIMSigning,
            # DKIM Verification
            DKIMVerification, DKIMVerificationProfile,
            # S/MIME DecryptionVerification
            SMIMEDecryptionVerification, SMIMESignatureProcessing,
            SMIMEPublicKeyHarvesting, SMIMEHarvestCertificateOnFailure,
            SMIMEStoreUpdatedCertificate,
            # SPF/SIDF Verification
            SPFSIDFProfile, ConformanceLevel,
            DowngradePRAVerificationResult, HELOTest,
            # DMARC Verification
            DMARCVerification, DMARCVerificationProfile, DMARCFeedbackReports,
            # Bounce Verification
            ConsiderUntaggedBouncesToBeValid,
            # Envelope Sender DNS Verification
            EnvelopeSenderDNSVerification, MalformedEnvelopeSendersSMTPCode,
            MalformedEnvelopeSendersSMTPText,
            EnvelopeSendersWhoseDomainDoesNotResolveSMTPCode,
            EnvelopeSendersWhoseDomainDoesNotResolveSMTPText,
            EnvelopeSendersWhoseDomainDoesNotExistSMTPCode,
            EnvelopeSendersWhoseDomainDoesNotExistSMTPText,
            # Use Sender Verification Exception Table
            UseSenderVerificationExceptionTable)


class DefaultPolicyEdit(PolicyEditContainer):
    def get_owned_properties(self):
        return (  # Connections
            MaxMsgsPerCon, MaxRcptsPerMsg, MaxMsgSize, MaxConnFromSingleIP,
            # SMTP
            CustomSMTPBannerCode, CustomSMTPBannerText,
            CustomSMTPRejectBannerCode, CustomSMTPRejectBannerText,
            OverrideSMTPBannerHostname,
            # Rate Limit for Hosts
            MaxRecipientsPerHour,
            MaxRecipientsPerHourCode, MaxRecipientsPerHourText,
            # Rate Limit for Envelope Senders
            MaxRecipientsPerTimeInterval, SenderRateLimitErrorCode,
            SenderRateLimitErrorText, Exceptions,
            # Flow Control
            UseSenderBaseForFlowControl, GroupBySimilarityOfIPAddresses,
            # Directory Harvest Attack Prevention (DHAP)
            MaxInvalidRecipientsPerHour,
            DropConnectionIfDHAPThresholdIsReached,
            MaxInvalidRecipientsPerHourCode, MaxInvalidRecipientsPerHourText,
            # Spam Detection
            SpamDetection,
            # AMP Detection
            AMPDetection,
            # Virus Protection
            VirusProtection,
            # Encryption and Authentication
            TLS, VerifyClientCert, SMTPAuthentication,
            TLSIsMandatoryForAddressList, RequireTLSToOfferSMTPAuth,
            # Domain Key/DKIM Signing
            DomainKeyDKIMSigning,
            # DKIM Verification
            DKIMVerification, DKIMVerificationProfile,
            # S/MIME DecryptionVerification
            SMIMEDecryptionVerification, SMIMESignatureProcessing,
            SMIMEPublicKeyHarvesting, SMIMEHarvestCertificateOnFailure,
            SMIMEStoreUpdatedCertificate,
            # SPF/SIDF Verification
            SPFSIDFProfile, ConformanceLevel,
            DowngradePRAVerificationResult, HELOTest,
            # DMARC Verification
            DMARCVerification, DMARCVerificationProfile, DMARCFeedbackReports,
            # Bounce Verification
            ConsiderUntaggedBouncesToBeValid,
            # Envelope Sender DNS Verification
            EnvelopeSenderDNSVerification, MalformedEnvelopeSendersSMTPCode,
            MalformedEnvelopeSendersSMTPText,
            EnvelopeSendersWhoseDomainDoesNotResolveSMTPCode,
            EnvelopeSendersWhoseDomainDoesNotResolveSMTPText,
            EnvelopeSendersWhoseDomainDoesNotExistSMTPCode,
            EnvelopeSendersWhoseDomainDoesNotExistSMTPText,
            # Use Sender Verification Exception Table
            UseSenderVerificationExceptionTable)

    def _create_property_object(self, prop_class):
        if issubclass(prop_class, RadioGroupProperty):
            return prop_class(self.gui, False)
        else:
            return prop_class(self.gui)
