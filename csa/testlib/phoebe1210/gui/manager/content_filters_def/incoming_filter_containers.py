#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/manager/content_filters_def/incoming_filter_containers.py#2 $
# $DateTime: 2019/05/27 03:13:44 $
# $Author: saurgup5 $

from content_filter_properties import MessageBodyOrAttachmentProperty, \
    MessageBodyProperty, URLCategoryActionProperty, URLCategoryConditionProperty, \
    URLReputationActionProperty, URLReputationConditionProperty, MessageSizeProperty, \
    AttachmentProtectionProperty, AttachmentContentProperty, AttachmentFileInfoProperty, \
    SubjectHeaderProperty, OtherHeaderProperty, EnvelopeSenderProperty, \
    EnvelopeRecipientProperty, ReceivingListenerProperty, RemoteIPHostnameProperty, \
    ReputationScoreProperty, DKIMAuthenticationProperty, SPFVerificationProperty, \
    QuarantineProperty, EncryptOnDeliveryProperty, StripAttachmentByContentProperty, \
    StripAttachmentByFileInfoProperty, AddDisclaimerTextProperty, \
    BypassOutbreakFilterScanningProperty, BypassDKIMSigningProperty, \
    SendCopyBccProperty, NotifyProperty, ChangeRecipientToProperty, \
    SendToAlternateDestinationHostProperty, DeliverFromIPInterfaceProperty, \
    StripHeaderProperty, AddEditHeaderProperty, AddMessageTagProperty, \
    AddLogEntryProperty, EncryptAndDeliverNowFinalActionProperty, \
    BounceFinalActionProperty, SkipRemainingContentFiltersFinalActionProperty, \
    SMIMEGatewayMessageProperty, SMIMEGatewayVerifiedProperty, \
    DropFinalActionProperty, SMIMESignEncryptonDeliveryProperty, \
    SMIMESignEncryptFinalActionProperty, MessageLanguageProperty, \
    MacroDetectionConditionProperty, StripAttachmentWithMacroProperty, \
    GeoCountriesProperty, DomainReputationProperty
from properties_containers import FilterActions, FilterConditions


class IncomingFilterActions(FilterActions):
    @classmethod
    def get_properties(cls):
        return (QuarantineProperty, EncryptOnDeliveryProperty,
                StripAttachmentByContentProperty,
                StripAttachmentByFileInfoProperty, URLCategoryActionProperty, AddDisclaimerTextProperty,
                BypassOutbreakFilterScanningProperty, BypassDKIMSigningProperty, URLReputationActionProperty,
                SendCopyBccProperty, NotifyProperty, ChangeRecipientToProperty,
                SendToAlternateDestinationHostProperty, DeliverFromIPInterfaceProperty,
                StripHeaderProperty, AddEditHeaderProperty, AddMessageTagProperty,
                AddLogEntryProperty, EncryptAndDeliverNowFinalActionProperty, StripAttachmentWithMacroProperty,
                BounceFinalActionProperty, SkipRemainingContentFiltersFinalActionProperty,
                DropFinalActionProperty, SMIMESignEncryptonDeliveryProperty, SMIMESignEncryptFinalActionProperty)


OutgoingFilterActions = IncomingFilterActions


class IncomingFilterConditions(FilterConditions):
    @classmethod
    def get_properties(cls):
        return (MessageBodyOrAttachmentProperty,
                MessageBodyProperty, URLCategoryConditionProperty, MessageSizeProperty,
                AttachmentProtectionProperty, URLReputationConditionProperty,
                AttachmentContentProperty, AttachmentFileInfoProperty,
                SubjectHeaderProperty, OtherHeaderProperty, EnvelopeSenderProperty,
                EnvelopeRecipientProperty, ReceivingListenerProperty,
                RemoteIPHostnameProperty, ReputationScoreProperty,
                DKIMAuthenticationProperty, SPFVerificationProperty,
                SMIMEGatewayMessageProperty, SMIMEGatewayVerifiedProperty,
                MessageLanguageProperty, MacroDetectionConditionProperty,
                GeoCountriesProperty, DomainReputationProperty)


OutgoingFilterConditions = IncomingFilterConditions
