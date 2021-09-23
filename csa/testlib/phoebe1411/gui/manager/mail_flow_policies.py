#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/mail_flow_policies.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import functools
import time

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
from common.util.ordered_dict import OrderedDict, chunks
from common.util.sarftime import CountDownTimer

from mail_flow_policies_def.policy_edit_controllers import CustomPolicyEdit, \
    DefaultPolicyEdit


ENV_SENDER_RATE_LIMIT_LINK = "//div[@id='envSenderRateLimitLinkClosed']"
ADD_POLICY_BUTTON = "//input[@value='Add Policy...']"
LISTENER_DROPDOWN = "//select[@name='listener_id']"
POLICIES_TABLE = "//table[@class='cols']"
POLICY_NAME_CELLS = "%s/tbody/tr" % (POLICIES_TABLE,)
POLICY_NAME_CELL = lambda row_num: "%s[%d]/td[1]" % (POLICY_NAME_CELLS,
                                                     row_num)
POLICY_EDIT_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                                 (POLICIES_TABLE, name)
DEFAULTPOLICY_EDIT_LINK = "//a[normalize-space()='Default Policy Parameters']"
POLICY_DELETE_LINK = lambda name: \
    "%s//td[.//a[normalize-space()='%s']]/following-sibling::td[2]/img" % \
    (POLICIES_TABLE, name)
CANCEL_BUTTON = "//input[@type='button' and @value='Cancel']"


PAGE_PATH = ('Mail Policies', 'Mail Flow Policies')
def go_to_listener(func):
    """Decorator is used for MailFlowPolicies class methods
    for navigating to the necessary page and selecting needed
    listener on this page.
    The first method argument should be destination listener name
    *Exceptions:*
    - `ValueError`: if given listener name does not exist
    """
    @functools.wraps(func)
    def decorator(self, listener, *args, **kwargs):
        self._debug('Navigating to "%s"' % (' -> '.join(PAGE_PATH),))
        self._navigate_to(*PAGE_PATH)
        available_listeners = self.get_list_items(LISTENER_DROPDOWN)
        dest_option = filter(lambda x: x.find(listener) >= 0,
                             available_listeners)
        if dest_option:
            self.select_from_list(LISTENER_DROPDOWN, dest_option[0])
            time.sleep(3)
        else:
            raise ValueError('There is no listener on appliance named '\
                             '"%s"' % (listener,))

        return func(self, listener, *args, **kwargs)
    return decorator

class MailFlowPolicies(GuiCommon):
    """
    Keywords for interaction with Mail Policies -> Mail Flow Policies page
    """

    def get_keyword_names(self):
        return ['mail_flow_policies_create_settings',
                'mail_flow_policies_add',
                'mail_flow_policies_edit',
                'mail_flow_policies_delete',
                'mail_flow_policies_get_details',
                'mail_flow_policies_get_all']

    def mail_flow_policies_create_settings(self, *args):
        """Create mail flow policy settings object

        *Parameters:*
        - `args`: <setting name>/<setting value> pairs that will
        be transformed into ordered dictionary

        *Exceptions*:
        - `ValueError`: if number of arguments is zero or not even

        *Return:*
        Ordered dictionary created from passed args

        *Examples:*
        | ${settings}= | Mail Flow Policies Create Settings |
        | ... | Connection Behavior | Accept |
        | ... | Max. Messages Per Connection | 10 |
        | Mail Flow Policies Add | InBoundMail | my_policy | ${settings} |
        """

        if len(args) % 2 != 0:
            raise ValueError('There should be even number of parameters')

        if len(args) == 0:
            raise ValueError('There should be at least two parameters')

        result_dict = OrderedDict()
        keyval_pairs = chunks(args, 2)
        for key, value in keyval_pairs:
            result_dict[key] = value
        return result_dict

    @go_to_listener
    def mail_flow_policies_add(self, listener, name, settings={}):
        """Add new policy for given listener

        *Parameters:*
        - `listener`: existing listener name to which this policy
        will be added
        - `name`: new policy name, mandatory
        - `settings`: ordered dictionary created by "Mail Flow Policies Create
        Settings" keyword (or simple dictionary if you don't care settings set order)
        containing policy settings.
        This dictionary can contain the next items:
        | `Connection Behavior` | connection behavior string,either
        "Accept<" or "Relay" or "Reject" or "TCP Refuse" |
        | `Max. Messages Per Connection` | count of maximum msgs per
        one connection, number. Also, can take "Use Default" value |
        | `Max. Recipients Per Message` | count of maximum recipients
        per one message, number. Also, can take "Use Default" value |
        | `Max. Message Size` | maximum size of one message in bytes
        (add a trailing K for kilobytes; M for megabytes). Also, can take
        "Use Default" value |
        | `Max. Concurrent Connections From a Single IP` | maximum number
        of concurrent connections from a single IP address, number. Also,
        can take "Use Default" value |
        | `Custom SMTP Banner Code` | custom SMTP banner code, number.
        Also, can take "Use Default" value |
        | `Custom SMTP Banner Text` | custom SMTP Banner Text. Also, can
        take "Use Default" value |
        | `Override SMTP Banner Hostname` | hostname to override SMTP Banner
        Hostname. Also, can take "Use Hostname from Interface" and
        "Use Default" values |
        | `Max. Recipients Per Hour` | maximum number of recipients per hour,
        number. Also, can take "Unlimited" and "Use Default" values |
        | `Max. Recipients Per Hour Code` | maximum recipients per hour code,
        number. Also, can take "Use Default" value |
        | `Max. Recipients Per Hour Text` | maximum recipients per hour text.
        Also, can take "Use Default" value |
        | `Max. Recipients Per Time Interval` | maximum number of recipients per
        time interval. Also, can take "Use Default" value |
        | `Sender Rate Limit Error Code` | sender rate limit error code, number.
        Also, can take "Use Default" value |
        | `Sender Rate Limit Error Text` | sender rate limit error text. Also,
        can take "Use Default" value |
        | `Exceptions` | whether to ignore rate limit for particular address lists.
        Can be name of existing address list or "USe Default" |
        | `Use SenderBase for Flow Control` | whether to use senderbase for flow
        control. Either "On", "Off" or "Use Default" |
        | `Group by Similarity of IP Addresses` | Possible values are "Off" or number
        of significant bits (from 0 to 32). Can only be enabled if `Use SenderBase
        for Flow Control` is set to "Off" |
        | `Max. Invalid Recipients Per Hour` | maximum number of invalid recipients
        per hour. Also, can take "Use Default" or "Unlimited" values |
        | `Drop Connection if DHAP threshold is Reached
        within an SMTP Conversation` | whether to drop connection if dhap threshold is
        reached within an smtp conversation. Can be "Use Default", "On" or "Off" |
        | `Max. Invalid Recipients Per Hour Code` | max. invalid recipients per hour code.
        Also, can take "Use Default" value |
        | `Max. Invalid Recipients Per Hour Text` | max. invalid recipients per hour text.
        Also, can take "Use Default" value |
        | `Spam Detection` | set spam detection feature state for this policy. Either
        "Use Default", "On" or "Off" |
        | `Virus Protection` | set virus protection feature state for this policy. Either
        "Use Default", "On" or "Off" |
        | `Sender Domain Reputation Verification` | set sdr feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Virus Outbreak Filters` | set vof feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Advanced Phishing Protection` | set app feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Graymail Detection` | set graymail detection feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Content Filters` | set content filter feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Message Filters` | set message filter feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `TLS` | set TLS feature state for the mail flow policy. Either "Use Default",
        "Off", "Preferred" or "Required" |
        | `Verify Client Certificate` | whether to verify client certificate for TLS
        connection. Available if `TLS` is not set to Off. ${False} by default |
        | `TLS is Mandatory for Address List` | address list name for which TLS is
        mandatory. Available only when `TLS` feature is set to "Preferred" |
        | `SMTP Authentication` | set SMTP authentication feature state for the policy.
        Either "Use Default", "Off", "Preferred" or "Required" |
        | `Require TLS To Offer SMTP Authentication` | whether to require TLS
        to offer SMTP authentication. Either ${True} or ${False}. Available of only
        if Both `TLS` and `SMTP Authentication` are enabled |
        | `Domain Key/DKIM Signing` | set domain key/DKIM signing for the policy. Either
        "Use Default", "On" or "Off" |
        | `DKIM Verification` | set DKIM verification for the policy. Either
        "Use Default", "On" or "Off" |
        | `Use DKIM Verification Profile` | existing DKIM verification profile name.
        Available only when `DKIM Verification` is set to "On" |
        | `S/MIME DecryptionVerification` | set S/MIME DecryptionVerification for the policy. Either
        "Use Default", "On" or "Off" |
        | `S/MIME SignatureProcessing` | set S/MIME Signature After Processing for the policy. Either
        "Use Default", "Preserve" or "Remove" |
        | `S/MIME PublicKeyHarvesting` | set S/MIME Public Key Harvesting for the policy. Either
        "Use Default", "Disable" or "Enable" |
        | `S/MIME HarvestCertificateOnFailure` | set S/MIME Harvest Certificates on Verification Failure for the policy. Either
        "Use Default", "Disable" or "Enable" |
        | `S/MIME StoreUpdatedCertificate` | set S/MIME Store Updated Certificate for the policy. Either
        "Use Default", "Disable" or "Enable" |
        | `SPF/SIDF Verification` | set SPF/SIDF verification for the policy. Either
        "Use Default", "On" or "Off" |
        | `Conformance Level` | conformance level value for `SPF/SIDF Verification`.
        Either: "SPF" or "SIDF Compatible" or "SIDF". Available only if
        `SPF/SIDF Verification` is set to "On" |
        | `Downgrade PRA verification result if 'Resent-Sender:' or
        'Resent-From:' were used` | whether to downgrade PRA verification result if
        'Resent-Sender:' or 'Resent-From:' were used. Either "Use Default", "Yes" or
        "No". Available only if `SPF/SIDF Verification` is set to "On" |
        | `HELO Test` | set HELO Test feature state for `SPF/SIDF Verification`.
        Either "Use Default", "Off" or "On". Available only if `SPF/SIDF Verification`
        is set to "On" |
        | `DMARC Verification` | set DMARC verification for the policy. Either
        "Use Default", "On" or "Off" |
        | `Use DMARC Verification Profile` | existing DMARC verification profile name.
        Available only when `DMARC Verification` is set to "On" |
        | `DMARC Feedback Reports` | whether to send aggregate feedback reports,
        either ${True} or ${False}. Available only when `DMARC Verification` is
        set to "On" |
        | `Consider Untagged Bounces to be Valid` | consider untagged bounces to be valid.
        Either Either "Use Default", "Yes" or "No". Applies only if bounce verification
        address tagging is in use. |
        | `Envelope Sender DNS Verification` | set envelope sender DNS verification
        feature state. Either "Use Default", "Off" or "On". |
        | `Malformed Envelope Senders SMTP Code` | malformed envelope senders SMPT code,
        number. Available only if `Envelope Sender DNS Verification` option is set
        to "On" |
        | `Malformed Envelope Senders SMTP Text` | malformed envelope senders SMPT text.
        Available only if `Envelope Sender DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not resolve SMTP Code` | envelope senders
        whose domain does not resolve SMTP code, number. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not resolve SMTP Text` | envelope senders
        whose domain does not resolve SMTP text. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not exist SMTP Code` | Envelope Senders
        whose domain does not exist SMTP code, number. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not exist SMTP Text` | Envelope Senders
        whose domain does not exist SMTP text, number. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Use Sender Verification Exception Table` | whether to use sender verification
        exception table. Either "Use Default", "On" or "Off" |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct

        *Examples:*
        | ${settings}= | Mail Flow Policies Create Settings |
        | ... | Connection Behavior | Relay |
        | ... | Max. Messages Per Connection | 20 |
        | ... | Max. Recipients Per Message | Use Default |
        | ... | Max. Message Size | 15M |
        | ... | Max. Concurrent Connections From a Single IP | 9 |
        | ... | Custom SMTP Banner Code | 230 |
        | ... | Custom SMTP Banner Text | blabla |
        | ... | Override SMTP Banner Hostname | Use Hostname from Interface |
        | ... | Max. Recipients Per Hour | 2 |
        | ... | Max. Recipients Per Hour Code | Use Default |
        | ... | Max. Recipients Per Hour Text | ololo |
        | ... | Max. Recipients Per Time Interval | Unlimited |
        | ... | Sender Rate Limit Error Code | 453 |
        | ... | Sender Rate Limit Error Text | Too many recipients received from the sender |
        | ... | Exceptions | Use Default |
        | ... | Use SenderBase for Flow Control | Off |
        | ... | Group by Similarity of IP Addresses | 6 |
        | ... | Max. Invalid Recipients Per Hour | 30 |
        | ... | Drop Connection if DHAP threshold is Reached within an SMTP Conversation | On |
        | ... | Max. Invalid Recipients Per Hour Code | 551 |
        | ... | Max. Invalid Recipients Per Hour Text | Too many invalid recipients |
        | ... | Spam Detection | On |
        | ... | Virus Protection | Off |
        | ... | Sender Domain Reputation Verification | On |
        | ... | Virus Outbreak Filters | On |
        | ... | Advanced Phishing Protection | On |
        | ... | Graymail Detection | On |
        | ... | Content Filters | On |
        | ... | Message Filters | On |
        | ... | TLS | Preferred |
        | ... | Verify Client Certificate | ${True} |
        | ... | TLS is Mandatory for Address List | None |
        | ... | SMTP Authentication | Preferred |
        | ... | Require TLS To Offer SMTP Authentication | ${True} |
        | ... | Domain Key/DKIM Signing | On |
        | ... | DKIM Verification | On |
        | ... | Use DKIM Verification Profile | DEFAULT |
        | ... | S/MIME DecryptionVerification | On |
        | ... | S/MIME SignatureProcessing | Preserve |
        | ... | S/MIME PublicKeyHarvesting | Enable |
        | ... | S/MIME HarvestCertificateOnFailure | Enable |
        | ... | S/MIME StoreUpdatedCertificate | Enable |
        | ... | SPF/SIDF Verification | On |
        | ... | Conformance Level | SIDF Compatible |
        | ... | Downgrade PRA verification result if 'Resent-Sender:' or 'Resent-From:' were used | No |
        | ... | HELO Test | Off |
        | ... | DMARC Verification | On |
        | ... | Use DMARC Verification Profile | DEFAULT |
        | ... | DMARC Feedback Reports | ${True} |
        | ... | Consider Untagged Bounces to be Valid | Yes |
        | ... | Envelope Sender DNS Verification | On |
        | ... | Malformed Envelope Senders SMTP Code | 550 |
        | ... | Malformed Envelope Senders SMTP Text | ololo |
        | ... | Envelope Senders whose domain does not resolve SMTP Code | 551 |
        | ... | Envelope Senders whose domain does not resolve SMTP Text | ololo |
        | ... | Envelope Senders whose domain does not exist SMTP Code | 552 |
        | ... | Envelope Senders whose domain does not exist SMTP Text | ololo |
        | ... | Use Sender Verification Exception Table | On |
        | Mail Flow Policies Add | InBoundMail | my_new_policy | ${settings} |
        """
        self.click_button(ADD_POLICY_BUTTON)

        settings.update({'Name': name})
        controller = self._get_policy_settings_controller(False)
        self._open_env_senders_section()
        controller.set(settings)
        self._click_submit_button()

    @go_to_listener
    def mail_flow_policies_edit(self, listener, name, settings={}):
        """Edit policy for given listener

        *Parameters:*
        - `listener`: existing listener name in which this policy
        will be edited
        - `name`: existing policy name. Can be "default" to edit
        default mail flow policy settings
        - `settings`: ordered dictionary created by "Mail Flow Policies Create
        Settings" keyword (or simple dictionary if you don't care settings set order)
        containing policy settings.
        *Important*: If policy name is "default" then all its settings do not
        contain the "Use Default" option. Also, the "default" policy doesn't
        contain the next options: "Name", "Connection Behavior".
        This dictionary can contain the next items:
        | `Name` | new policy name |
        | `Connection Behavior` | connection behavior string,either
        "Accept<" or "Relay" or "Reject" or "TCP Refuse" |
        | `Max. Messages Per Connection` | count of maximum msgs per
        one connection, number. Also, can take "Use Default" value |
        | `Max. Recipients Per Message` | count of maximum recipients
        per one message, number. Also, can take "Use Default" value |
        | `Max. Message Size` | maximum size of one message in bytes
        (add a trailing K for kilobytes; M for megabytes). Also, can take
        "Use Default" value |
        | `Max. Concurrent Connections From a Single IP` | maximum number
        of concurrent connections from a single IP address, number. Also,
        can take "Use Default" value |
        | `Custom SMTP Banner Code` | custom SMTP banner code, number.
        Also, can take "Use Default" value |
        | `Custom SMTP Banner Text` | custom SMTP Banner Text. Also, can
        take "Use Default" value |
        | `Override SMTP Banner Hostname` | hostname to override SMTP Banner
        Hostname. Also, can take "Use Hostname from Interface" and
        "Use Default" values |
        | `Max. Recipients Per Hour` | maximum number of recipients per hour,
        number. Also, can take "Unlimited" and "Use Default" values |
        | `Max. Recipients Per Hour Code` | maximum recipients per hour code,
        number. Also, can take "Use Default" value |
        | `Max. Recipients Per Hour Text` | maximum recipients per hour text.
        Also, can take "Use Default" value |
        | `Max. Recipients Per Time Interval` | maximum number of recipients per
        time interval. Also, can take "Use Default" value |
        | `Sender Rate Limit Error Code` | sender rate limit error code, number.
        Also, can take "Use Default" value |
        | `Sender Rate Limit Error Text` | sender rate limit error text. Also,
        can take "Use Default" value |
        | `Exceptions` | whether to ignore rate limit for particular address lists.
        Can be name of existing address list or "USe Default" |
        | `Use SenderBase for Flow Control` | whether to use senderbase for flow
        control. Either "On", "Off" or "Use Default" |
        | `Group by Similarity of IP Addresses` | Possible values are "Off" or number
        of significant bits (from 0 to 32). Can only be enabled if `Use SenderBase
        for Flow Control` is set to "Off" |
        | `Max. Invalid Recipients Per Hour` | maximum number of invalid recipients
        per hour. Also, can take "Use Default" or "Unlimited" values |
        | `Drop Connection if DHAP threshold is Reached
        within an SMTP Conversation` | whether to drop connection if dhap threshold is
        reached within an smtp conversation. Can be "Use Default", "On" or "Off" |
        | `Max. Invalid Recipients Per Hour Code` | max. invalid recipients per hour code.
        Also, can take "Use Default" value |
        | `Max. Invalid Recipients Per Hour Text` | max. invalid recipients per hour text.
        Also, can take "Use Default" value |
        | `Spam Detection` | set spam detection feature state for this policy. Either
        "Use Default", "On" or "Off" |
        | `Virus Protection` | set virus protection feature state for this policy. Either
        "Use Default", "On" or "Off" |
        | `Sender Domain Reputation Verification` | set sdr feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Virus Outbreak Filters` | set vof feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Advanced Phishing Protection` | set app feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Graymail Detection` | set graymail detection feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Content Filters` | set content filter feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `Message Filters` | set message filter feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `TLS` | set TLS feature state for the mail flow policy. Either "Use Default",
        "Off", "Preferred" or "Required" |
        | `Verify Client Certificate` | whether to verify client certificate for TLS
        connection. Available if `TLS` is not set to Off. ${False} by default |
        | `TLS is Mandatory for Address List` | address list name for which TLS is
        mandatory. Available only when `TLS` feature is set to "Preferred" |
        | `SMTP Authentication` | set SMTP authentication feature state for the policy.
        Either "Use Default", "Off", "Preferred" or "Required" |
        | `Require TLS To Offer SMTP Authentication` | whether to require TLS
        to offer SMTP authentication. Either ${True} or ${False}. Available of only
        if Both `TLS` and `SMTP Authentication` are enabled |
        | `Domain Key/DKIM Signing` | set domain key/DKIM signing for the policy. Either
        "Use Default", "On" or "Off" |
        | `DKIM Verification` | set DKIM verification for the policy. Either
        "Use Default", "On" or "Off" |
        | `Use DKIM Verification Profile` | existing DKIM verification profile name.
        Available only when `DKIM Verification` si set to "On" |
        | `S/MIME DecryptionVerification` | set S/MIME DecryptionVerification for the policy. Either
        "Use Default", "On" or "Off" |
        | `S/MIME SignatureProcessing` | set S/MIME Signature After Processing for the policy. Either
        "Use Default", "Preserve" or "Remove" |
        | `S/MIME PublicKeyHarvesting` | set S/MIME Public Key Harvesting for the policy. Either
        "Use Default", "Disable" or "Enable" |
        | `S/MIME HarvestCertificateOnFailure` | set S/MIME Harvest Certificates on Verification Failure for the policy. Either
        "Use Default", "Disable" or "Enable" |
        | `S/MIME StoreUpdatedCertificate` | set S/MIME Store Updated Certificate for the policy. Either
        "Use Default", "Disable" or "Enable" |
        | `SPF/SIDF Verification` | set SPF/SIDF verification for the policy. Either
        "Use Default", "On" or "Off" |
        | `Conformance Level` | conformance level value for `SPF/SIDF Verification`.
        Either: "SPF" or "SIDF Compatible" or "SIDF". Available only if
        `SPF/SIDF Verification` is set to "On" |
        | `Downgrade PRA verification result if 'Resent-Sender:' or
        'Resent-From:' were used` | whether to downgrade PRA verification result if
        'Resent-Sender:' or 'Resent-From:' were used. Either "Use Default", "Yes" or
        "No". Available only if `SPF/SIDF Verification` is set to "On" |
        | `HELO Test` | set HELO Test feature state for `SPF/SIDF Verification`.
        Either "Use Default", "Off" or "On". Available only if `SPF/SIDF Verification`
        is set to "On" |
        | `DMARC Verification` | set DMARC verification for the policy. Either
        "Use Default", "On" or "Off" |
        | `Use DMARC Verification Profile` | existing DMARC verification profile name.
        Available only when `DMARC Verification` is set to "On" |
        | `DMARC Feedback Reports` | whether to send aggregate feedback reports,
        either ${True} or ${False}. Available only when `DMARC Verification` is
        set to "On" |
        | `Consider Untagged Bounces to be Valid` | consider untagged bounces to be valid.
        Either Either "Use Default", "Yes" or "No". Applies only if bounce verification
        address tagging is in use. |
        | `Envelope Sender DNS Verification` | set envelope sender DNS verification
        feature state. Either "Use Default", "Off" or "On". |
        | `Malformed Envelope Senders SMTP Code` | malformed envelope senders SMPT code,
        number. Available only if `Envelope Sender DNS Verification` option is set
        to "On" |
        | `Malformed Envelope Senders SMTP Text` | malformed envelope senders SMPT text.
        Available only if `Envelope Sender DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not resolve SMTP Code` | envelope senders
        whose domain does not resolve SMTP code, number. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not resolve SMTP Text` | envelope senders
        whose domain does not resolve SMTP text. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not exist SMTP Code` | Envelope Senders
        whose domain does not exist SMTP code, number. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not exist SMTP Text` | Envelope Senders
        whose domain does not exist SMTP text, number. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Use Sender Verification Exception Table` | whether to use sender verification
        exception table. Either "Use Default", "On" or "Off" |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct

        *Examples:*
        | ${settings}= | Mail Flow Policies Create Settings |
        | ... | Connection Behavior | Relay |
        | ... | Max. Messages Per Connection | 20 |
        | ... | Max. Recipients Per Message | Use Default |
        | ... | Max. Message Size | 15M |
        | ... | Max. Concurrent Connections From a Single IP | 9 |
        | ... | Custom SMTP Banner Code | 230 |
        | ... | Custom SMTP Banner Text | blabla |
        | ... | Override SMTP Banner Hostname | Use Hostname from Interface |
        | ... | Max. Recipients Per Hour | 2 |
        | ... | Max. Recipients Per Hour Code | Use Default |
        | ... | Max. Recipients Per Hour Text | ololo |
        | ... | Max. Recipients Per Time Interval | Unlimited |
        | ... | Sender Rate Limit Error Code | 453 |
        | ... | Sender Rate Limit Error Text | Too many recipients received from the sender |
        | ... | Exceptions | Use Default |
        | ... | Use SenderBase for Flow Control | Off |
        | ... | Group by Similarity of IP Addresses | 6 |
        | ... | Max. Invalid Recipients Per Hour | 30 |
        | ... | Drop Connection if DHAP threshold is Reached within an SMTP Conversation | On |
        | ... | Max. Invalid Recipients Per Hour Code | 551 |
        | ... | Max. Invalid Recipients Per Hour Text | Too many invalid recipients |
        | ... | Spam Detection | On |
        | ... | Virus Protection | Off |
        | ... | Sender Domain Reputation Verification | On |
        | ... | Virus Outbreak Filters | On |
        | ... | Advanced Phishing Protection | On |
        | ... | Graymail Detection | On |
        | ... | Content Filters | On |
        | ... | Message Filters | On |
        | ... | TLS | Preferred |
        | ... | TLS is Mandatory for Address List | None |
        | ... | SMTP Authentication | Preferred |
        | ... | Require TLS To Offer SMTP Authentication | ${True} |
        | ... | Domain Key/DKIM Signing | On |
        | ... | DKIM Verification | On |
        | ... | Use DKIM Verification Profile | DEFAULT |
        | ... | S/MIME DecryptionVerification | On |
        | ... | S/MIME SignatureProcessing | Preserve |
        | ... | S/MIME PublicKeyHarvesting | Enable |
        | ... | S/MIME HarvestCertificateOnFailure | Enable |
        | ... | S/MIME StoreUpdatedCertificate | Enable |
        | ... | SPF/SIDF Verification | On |
        | ... | Conformance Level | SIDF Compatible |
        | ... | Downgrade PRA verification result if 'Resent-Sender:' or 'Resent-From:' were used | No |
        | ... | HELO Test | Off |
        | ... | Consider Untagged Bounces to be Valid | Yes |
        | ... | Envelope Sender DNS Verification | On |
        | ... | Malformed Envelope Senders SMTP Code | 550 |
        | ... | Malformed Envelope Senders SMTP Text | ololo |
        | ... | Envelope Senders whose domain does not resolve SMTP Code | 551 |
        | ... | Envelope Senders whose domain does not resolve SMTP Text | ololo |
        | ... | Envelope Senders whose domain does not exist SMTP Code | 552 |
        | ... | Envelope Senders whose domain does not exist SMTP Text | ololo |
        | ... |Use Sender Verification Exception Table | On |
        | Mail Flow Policies Edit | InBoundMail | my_existing_policy | ${settings} |
        """
        should_edit_default_policy = (name.lower() == 'default')
        if should_edit_default_policy:
            self.click_button(DEFAULTPOLICY_EDIT_LINK)
        else:
            try:
                self.click_button(POLICY_EDIT_LINK(name))
            except Exception:
                raise ValueError('There is no mail flow policy present with name '\
                                 '"%s"' % (name,))

        controller = self._get_policy_settings_controller(should_edit_default_policy)
        self._open_env_senders_section()
        controller.set(settings)
        self._click_submit_button()

    @go_to_listener
    def mail_flow_policies_delete(self, listener, name):
        """Delete existing policy for given listener

        *Parameters:*
        - `listener`: existing listener name in which this policy
        will be deleted
        - `name`: existing policy name.

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct or
        given policy is used by the ALL host and can not be removed

        *Examples:*
        | Mail Flow Policies Delete Policy | InBoundMail | MyPolicy |
        """
        try:
            self.click_button(POLICY_DELETE_LINK(name), 'don\'t wait')
        except Exception:
            raise ValueError('There is no mail flow policy present with name '\
                             '"%s" or the policy is being used by the ALL host' % (name,))
        self._click_continue_button()

    @go_to_listener
    def mail_flow_policies_get_details(self, listener, name):
        """Return existing policy details for given listener

        *Parameters:*
        - `listener`: existing listener name in which this policy
        will be scanned
        - `name`: existing policy name. Can be "default" for default
        policy

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct

        *Return:*
        Dictionary containing particular mail flow policy settings.
        *Important* For "default" policy there are no settings named
        "Name" and "Connection Behavior". Also, its values can not
        be equal to "Use Default" string
        Its keys and values are:
        | `Name` | policy name |
        | `Connection Behavior` | connection behavior string,either
        "Accept<" or "Relay" or "Reject" or "TCP Refuse" |
        | `Max. Messages Per Connection` | count of maximum msgs per
        one connection, number. Also, can take "Use Default" value |
        | `Max. Recipients Per Message` | count of maximum recipients
        per one message, number. Also, can take "Use Default" value |
        | `Max. Message Size` | maximum size of one message in bytes
        (add a trailing K for kilobytes; M for megabytes). Also, can take
        "Use Default" value |
        | `Max. Concurrent Connections From a Single IP` | maximum number
        of concurrent connections from a single IP address, number. Also,
        can take "Use Default" value |
        | `Custom SMTP Banner Code` | custom SMTP banner code, number.
        Also, can take "Use Default" value |
        | `Custom SMTP Banner Text` | custom SMTP Banner Text. Also, can
        take "Use Default" value |
        | `Override SMTP Banner Hostname` | hostname to override SMTP Banner
        Hostname. Also, can take "Use Hostname from Interface" and
        "Use Default" values |
        | `Max. Recipients Per Hour` | maximum number of recipients per hour,
        number. Also, can take "Unlimited" and "Use Default" values |
        | `Max. Recipients Per Hour Code` | maximum recipients per hour code,
        number. Also, can take "Use Default" value |
        | `Max. Recipients Per Hour Text` | maximum recipients per hour text.
        Also, can take "Use Default" value |
        | `Max. Recipients Per Time Interval` | maximum number of recipients per
        time interval. Also, can take "Use Default" value |
        | `Sender Rate Limit Error Code` | sender rate limit error code, number.
        Also, can take "Use Default" value |
        | `Sender Rate Limit Error Text` | sender rate limit error text. Also,
        can take "Use Default" value |
        | `Exceptions` | whether to ignore rate limit for particular address lists.
        Can be name of existing address list or "USe Default" |
        | `Use SenderBase for Flow Control` | whether to use senderbase for flow
        control. Either "On", "Off" or "Use Default" |
        | `Group by Similarity of IP Addresses` | Possible values are "Off" or number
        of significant bits (from 0 to 32). Can only be enabled if `Use SenderBase
        for Flow Control` is set to "Off" |
        | `Max. Invalid Recipients Per Hour` | maximum number of invalid recipients
        per hour. Also, can take "Use Default" or "Unlimited" values |
        | `Drop Connection if DHAP threshold is Reached
        within an SMTP Conversation` | whether to drop connection if dhap threshold is
        reached within an smtp conversation. Can be "Use Default", "On" or "Off" |
        | `Max. Invalid Recipients Per Hour Code` | max. invalid recipients per hour code.
        Also, can take "Use Default" value |
        | `Max. Invalid Recipients Per Hour Text` | max. invalid recipients per hour text.
        Also, can take "Use Default" value |
        | `Spam Detection` | set spam detection feature state for this policy. Either
        "Use Default", "On" or "Off" |
        | `Virus Protection` | set virus protection feature state for this policy. Either
        "Use Default", "On" or "Off" |
        | `Sender Domain Reputation Verification` | set sdr feature state for this policy.
        Either "Use Default", "On" or "Off" |
        | `TLS` | set TLS feature state for the mail flow policy. Either "Use Default",
        "Off", "Preferred" or "Required" |
        | `Verify Client Certificate` | whether to verify client certificate for TLS
        connection. Either ${True} or ${False} |
        | `TLS is Mandatory for Address List` | address list name for which TLS is
        mandatory. Available only when `TLS` feature is set to "Preferred" |
        | `SMTP Authentication` | set SMTP authentication feature state for the policy.
        Either "Use Default", "Off", "Preferred" or "Required" |
        | `Require TLS To Offer SMTP Authentication` | whether to require TLS
        to offer SMTP authentication. Either ${True} or ${False}. Available of only
        if Both `TLS` and `SMTP Authentication` are enabled |
        | `Domain Key/DKIM Signing` | set domain key/DKIM signing for the policy. Either
        "Use Default", "On" or "Off" |
        | `DKIM Verification` | set DKIM verification for the policy. Either
        "Use Default", "On" or "Off" |
        | `Use DKIM Verification Profile` | existing DKIM verification profile name.
        Available only when `DKIM Verification` si set to "On" |
        | `S/MIME DecryptionVerification` | set S/MIME DecryptionVerification for the policy. Either
        "Use Default", "On" or "Off" |
        | `S/MIME SignatureProcessing` | set S/MIME Signature After Processing for the policy. Either
        "Use Default", "Preserve" or "Remove" |
        | `S/MIME PublicKeyHarvesting` | set S/MIME Public Key Harvesting for the policy. Either
        "Use Default", "Disable" or "Enable" |
        | `S/MIME HarvestCertificateOnFailure` | set S/MIME Harvest Certificates on Verification Failure for the policy. Either
        "Use Default", "Disable" or "Enable" |
        | `S/MIME StoreUpdatedCertificate` | set S/MIME Store Updated Certificate for the policy. Either
        "Use Default", "Disable" or "Enable" |
        | `SPF/SIDF Verification` | set SPF/SIDF verification for the policy. Either
        "Use Default", "On" or "Off" |
        | `Conformance Level` | conformance level value for `SPF/SIDF Verification`.
        Either: "SPF" or "SIDF Compatible" or "SIDF". Available only if
        `SPF/SIDF Verification` is set to "On" |
        | `Downgrade PRA verification result if 'Resent-Sender:' or
        'Resent-From:' were used` | whether to downgrade PRA verification result if
        'Resent-Sender:' or 'Resent-From:' were used. Either "Use Default", "Yes" or
        "No". Available only if `SPF/SIDF Verification` is set to "On" |
        | `HELO Test` | set HELO Test feature state for `SPF/SIDF Verification`.
        Either "Use Default", "Off" or "On". Available only if `SPF/SIDF Verification`
        is set to "On" |
        | `DMARC Verification` | set DMARC verification for the policy. Either
        "Use Default", "On" or "Off" |
        | `Use DMARC Verification Profile` | existing DMARC verification profile name.
        Available only when `DMARC Verification` is set to "On" |
        | `DMARC Feedback Reports` | whether to send aggregate feedback reports,
        either ${True} or ${False}. Available only when `DMARC Verification` is
        set to "On" |
        | `Consider Untagged Bounces to be Valid` | consider untagged bounces to be valid.
        Either Either "Use Default", "Yes" or "No". Applies only if bounce verification
        address tagging is in use. |
        | `Envelope Sender DNS Verification` | set envelope sender DNS verification
        feature state. Either "Use Default", "Off" or "On". |
        | `Malformed Envelope Senders SMTP Code` | malformed envelope senders SMPT code,
        number. Available only if `Envelope Sender DNS Verification` option is set
        to "On" |
        | `Malformed Envelope Senders SMTP Text` | malformed envelope senders SMPT text.
        Available only if `Envelope Sender DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not resolve SMTP Code` | envelope senders
        whose domain does not resolve SMTP code, number. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not resolve SMTP Text` | envelope senders
        whose domain does not resolve SMTP text. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not exist SMTP Code` | Envelope Senders
        whose domain does not exist SMTP code, number. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Envelope Senders whose domain does not exist SMTP Text` | Envelope Senders
        whose domain does not exist SMTP text, number. Available only if `Envelope Sender
        DNS Verification` option is set to "On" |
        | `Use Sender Verification Exception Table` | whether to use sender verification
        exception table. Either "Use Default", "On" or "Off" |

        *Examples:*
        | ${settings}= | Mail Flow Policies Get Details | InBoundMail | my_policy |
        | Log | ${settings} |
        | ${behavior} | Get From Dictionary | ${settings} | Connection Behavior |
        | Log | ${behavior} |
        """
        should_edit_default_policy = (name.lower() == 'default')
        if should_edit_default_policy:
            self.click_button(DEFAULTPOLICY_EDIT_LINK)
        else:
            try:
                self.click_button(POLICY_EDIT_LINK(name))
            except Exception:
                raise ValueError('There is no mail flow policy present with name '\
                                 '"%s"' % (name,))

        controller = self._get_policy_settings_controller(should_edit_default_policy)
        self._open_env_senders_section()
        details = controller.get()
        self.click_button(CANCEL_BUTTON)
        return details

    @go_to_listener
    def mail_flow_policies_get_all(self, listener):
        """Return existing policy names for given listener

        *Parameters:*
        - `listener`: existing listener name in which this policy
        will be scanned
        - `name`: existing policy name. Can be "default" for default
        policy

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct
        - `TimeoutError`: if Mail flow policies list has not been populated
        within acceptable time range

        *Return:*
        List of existing mail flow policies

        *Examples:*
        | @{policies}= | Mail Flow Policies Get All | InBoundMail |
        | Log Many | @{policies} |
        """
        policies_count = -1
        MAX_WAIT_TIME = 3
        timer = CountDownTimer(MAX_WAIT_TIME).start()
        while timer.is_active():
            # Substitute rows containing default policy and headers
            policies_count = int(self.get_matching_xpath_count(POLICY_NAME_CELLS)) - 2
            if policies_count >= 0:
                break
            time.sleep(1.0)
        if policies_count < 0:
            raise guiexceptions.TimeoutError('Mail flow policies list has not '\
                                             'been populated'\
                                             ' within %d seconds timeout' % \
                                             (MAX_WAIT_TIME,))
        all_names = []
        for row_num in xrange(2, 2 + policies_count):
            all_names.append(self.get_text(POLICY_NAME_CELL(row_num)))
        return all_names

    def _get_policy_settings_controller(self, is_default_policy):
        if is_default_policy:
            attr_name = '_default_settings_controller'
            controller_class = DefaultPolicyEdit
        else:
            attr_name = '_custom_settings_controller'
            controller_class = CustomPolicyEdit
        if not hasattr(self, attr_name):
            setattr(self, attr_name, controller_class(self))
        return getattr(self, attr_name)

    def _open_env_senders_section(self):
        time.sleep(1.0)
        self.click_button(ENV_SENDER_RATE_LIMIT_LINK, 'don\'t wait')
