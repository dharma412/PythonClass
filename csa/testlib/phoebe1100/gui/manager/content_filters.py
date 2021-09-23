#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/manager/content_filters.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $


from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
from common.util.ordered_dict import OrderedDict, chunks

from content_filters_def.incoming_filter_containers import IncomingFilterActions, \
    IncomingFilterConditions
from content_filters_def.outgoing_filter_containers import OutgoingFilterActions, \
    OutgoingFilterConditions
from content_filters_def.properties_containers import PROPNAME_SUFFIX_MAGIC

from content_filters_def.utils import go_to_filter

FILTERS_LIST = "//dl[.//dt[normalize-space()='Filters']]"
ADD_FILTER = "//input[@name='action:NewFilter']"
FILTER_NAME = "//input[@id='fname']"
# FILTER_DESCRIPTION = "//*[@name='description']"
FILTER_DESCRIPTION = "xpath=(//textarea[@name='description'])[2]"
# FILTER_DESCRIPTION = "//*[@id='filter_form']/dl[1]/dd/table/tbody/tr[3]/td/textarea"
SAVE_BUTTON = "//input[@name='action:Save']"
DELETE_BUTTON = lambda filter_name: \
    "%s//td[.//a[normalize-space()='%s']]/following-sibling::td[3]/img" % \
    (FILTERS_LIST, filter_name)


class ContentFilters(GuiCommon):
    """Keywords for ESA GUI
    interaction with Mail Policies -> Incoming Content Filters
    and Mail Policies -> Outgoing Content Filters pages
    """

    def get_keyword_names(self):
        return ['content_filter_add',
                'content_filter_delete',
                'content_filter_create_actions',
                'content_filter_create_conditions']

    def _get_filter_actions_controller(self, filter_type):
        if filter_type.upper() == 'INCOMING':
            return IncomingFilterActions(self)
        elif filter_type.upper() == 'OUTGOING':
            return OutgoingFilterActions(self)
        else:
            raise ValueError('Unknown filter type is given ("%s")' % \
                             (filter_type,))

    def _get_filter_conditions_controller(self, filter_type):
        if filter_type.upper() == 'INCOMING':
            return IncomingFilterConditions(self)
        elif filter_type.upper() == 'OUTGOING':
            return OutgoingFilterConditions(self)
        else:
            raise ValueError('Unknown filter type is given ("%s")' % \
                             (filter_type,))

    def content_filter_create_actions(self, *args):
        """Transform list of actions with their values to ordered dictionary

        *Parameters:*
        - `args`: <action name>/<action options dictitonary> pairs that will
        be transformed into ordered dictionary

        *Exceptions*:
        - `ValueError`: if number of arguments is zero or not even

        *Return:*
        Ordered dictionary created from passed args

        *Examples:*
        | ${actions}= | Content Filter Create Actions |
        | ... | Quarantine | ${quarantine_action} |
        | ... | Strip Attachment by Content | ${strip_attachment_by_content_action} |
        | Content Filter Add | Incoming | my_filter |
        | ... | Super filter | ${actions} | ${conditions} |
        """
        return self._args_to_ordered_dict(args)

    def content_filter_create_conditions(self, *args):
        """Transform list of conditions with their values to ordered dictionary

        *Parameters:*
        - `args`: <condition name>/<condition options dictitonary> pairs that will
        be transformed into ordered dictionary

        *Exceptions*:
        - `ValueError`: if number of arguments is zero or not even

        *Return:*
        Ordered dictionary created from passed args

        *Examples:*
        | ${conditions}= | Content Filter Create Conditions |
        | ... | Message Body or Attachment | ${msg_body_or_attachment_cond} |
        | ... | Message Body | ${msg_body_cond} |
        | Content Filter Add | Incoming | my_filter |
        | ... | Super filter | ${actions} | ${conditions} |
        """
        return self._args_to_ordered_dict(args)

    def _args_to_ordered_dict(self, args):
        if len(args) % 2 != 0:
            raise ValueError('There should be even number of parameters')
        if len(args) == 0:
            raise ValueError('There should be at least two parameters')

        result_dict = OrderedDict()
        keyval_pairs = chunks(args, 2)
        for key, value in keyval_pairs:
            # Hack for multiple keys with same names
            modified_key = key
            while result_dict.has_key(modified_key):
                modified_key += PROPNAME_SUFFIX_MAGIC
            result_dict[modified_key] = value
        return result_dict

    @go_to_filter
    def content_filter_add(self, filter_type, name, description=None,
                           actions={}, conditions={}):
        """Add new content filter

        *Parameters:*
        - `filter_type`: new content filter type, either Incoming or
        Outgoing, mandatory
        - `name`: new filter name. Should be unique and should begin with
        character, mandatory
        - `description`: your description for newly created filter
        - `actions`: dictionary containing actions that will be included
        into this filter. Dictionary keys are actions names; same as
        corresponding container headers (case sensitive). Values are dictionaries
        which keys and value can be:
        `Key`: *Quarantine*
        `Value`: flags the message to be held in one of the system
        quarantine areas.
        Dictionary can contain the next items:
        | Send message to quarantine | <value> |
        <value> can be one of these values:
        | Policy |
        and
        | Duplicate message | <value> |
        Value can be ${True} or ${False}

        *Examples:*
        | ${new_value}= | Create Dictionary | Send message to quarantine | Policy |
        | ... | Duplicate message | ${True} |

        `Key`: *Encrypt on Delivery*
        `Value`: whether to encrypt the message, then deliver without
        further processing.
        Dictionary can contain the next items:
        | Encryption Rule | <value> |
        value can be one of these items:
        | Always use message encryption. |
        | Only use message encryption if TLS fails. |
        and
        | Encryption Profile | <name of existing encryption profile> |
        and
        | Subject | <message subject> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Encryption Rule |
        | ... | Only use message encryption if TLS fails. |
        | ... | Encryption Profile | My_Profile |
        | ... | Subject | $Subject |

        `Key`: *Strip Attachment by Content*
        `Value`: drops all attachments on messages that contain text
        matching a specified pattern. Archive file attachments (zip, tar)
        will be dropped if they contain a file that matches.
        Dictionary can contain the next items:
        | Attachment contains | <contained text> |
        or
        | Contains smart identifier | <value> |
        <value> can be one of:
        | ABA Routing Number |
        | Credit Card Number |
        | CUSIP |
        | Social Security Number (SSN) |
        or
        | Attachment contains term in content dictionary | <dictionary name> (should
        exist in Dictionaries list) |
        and
        | Number of matches required | <number in range 1..1000> |
        and
        | Replacement Message | <text of replacement message> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Attachment contains | blabla |
        | ... | Number of matches required | 50 | Replacement Message |
        | ... | my replacement message |

        `Key`: *Strip Attachment by File Info*
        `Value`: drops all attachments on messages that match the
        specified filename, file type, or MIME type. Archive file attachments
        (zip, tar) will be dropped if they contain a file that matches. IronPort
        Image Analysis will drop an attachment for images that match a specified
        IronPort Image Analysis verdict.
        Dictionary can contain the next items:
        | Filename | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Contains |
        | Does Not Contain |
        | Equals |
        | Does Not Equal |
        | Begins with |
        | Does Not Begin With |
        | Ends With |
        | Does Not End With |
        and the second part is some text
        or
        | File size is greater than | <bytes count> |
        or
        | File type is | <value> |
        <value> can be on of:
        | Compressed | -- ace | -- arc |-- arj | -- binhex | -- bz |
        | -- bz2 | -- cab< | -- gzip| -- lha | -- rar| -- sit | -- tar |
        | -- unix | -- x-windows-packager | -- zip | -- zoo | Documents |
        | -- doc, docx | -- mdb | -- mpp | -- ole | -- pdf | -- ppt, pptx |
        | -- pub | -- rtf | -- wps | -- x-wmf | -- xls, xlsx | Executables |
        | -- exe | -- java | -- msi | -- pif | Images | -- bmp | -- cur |
        | -- gif | -- ico | -- jpeg | -- pcx | -- png | -- psd | -- psp |
        | -- tga | -- tiff | -- x-pict2 | Media | -- aac | -- aiff | -- asf |
        | -- avi | -- flash | -- midi | -- mov | -- mp3 | -- mpeg | -- ogg |
        | -- ram | -- snd | -- wav | -- wma | -- wmv | Text | -- html | -- txt |
        | -- xml |
        or
        | MIME type is | <mime type name> |
        or
        | Image Analysis Verdict is | <value> |
        where value can be one of:
        | Inappropriate |
        | Suspect or Inappropriate |
        | Suspect |
        | Unscannable |
        | Clean |
        IIA feature should be enbled on appliance to use this feature
        and
        | Replacement Message | <text of replacement message> |
        or
        | Attachment is corrupt | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Filename | Contains blabla |
        | ... | Replacement Message | my replacement message |

        `Key`: *Add Disclaimer Text*
        `Value`: whether to add text above or below the message body.
        Dictionary can contain item:
        | Add to | <value> |
        value can be one of:
        | Above message (Heading) |
        | Below message (Footer) |
        and
        | Disclaimer Text | <name of dicslaimer text resource>

        *Examples:*
        | ${new_value}= | Create Dictionary | Add to | Below message (Footer) |
        | ... | Disclaimer Text | My_dics_text |

        `Key`: *Bypass Outbreak Filter Scanning*
        `Value`: whether to bypass Outbreak Filter scanning for message.
        Dictionary can contain item:
        | Bypass Outbreak Filter Scanning | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Bypass Outbreak Filter Scanning |
        | ... | Enable! |

        `Key`: *Bypass DKIM Signing*
        `Value`: whether to bypass DKIM Signing for message.
        Dictionary can contain item:
        | Bypass DKIM Signing | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Bypass DKIM Signing | Activate it |

        `Key`: *Send Copy (Bcc:)*
        `Value`: copies this message anonymously to specified recipient(s)
        Dictionary can contain the next items:
        | Email Addresses | <list of email eddressed separated with commas> |, mandatory
        and
        | Subject | <message's subject value> |
        and
        | Return Path | <message's return path value> |
        and
        | Alternate Mail Host | <message's alternate mail host value> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Email Addresses | mm@me.com |
        | ... | Return Path | path@example.com |

        `Key`: *Notify*
        `Value`: report this message to specified recipient(s)
        Dictionary can contain the next items:
        | Email Addresses | <list of email eddressed separated with commas> |, mandatory
        and
        | Email Addresses Sender | <${True or ${False}> |
        and
        | Email Addresses Recipient(s) | <${True or ${False}> |
        and
        | Subject | <message's subject value> |
        and
        | Return Path | <message's return path value> |
        and
        | Use Template | <name of existing notify text resource> |
        Corresponding text resource should be already cnfigured to use
        this feature
        and
        | Include original message as attachment | <${True} or ${False}> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Email Addresses | mm@me.com |
        | ... | Email Addresses Sender | ${True} |
        | ... | Include original message as attachment | ${True} |

        `Key`: *Change Recipient to*
        `Value`: changes a recipient of the message.
        Dictionary can contain the next items:
        | Email Address | <new recipient's email address> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Email Address | mm@me.com |

        `Key`: *Send to Alternate Destination Host*
        `Value`: changes the destination mail host for the message.
        Dictionary can contain the next items:
        | Mail Host | <new messages's destination mail host> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Mail Host | me.com |

        `Key`: *Deliver from IP Interface*
        `Value`: send from the specified IP Interface.
        Dictionary can contain the next items:
        | Send from IP Interface | <appliance's IP interface DNS> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Send from IP Interface |
        | ... | a001.d1.c600-08.auto |

        `Key`: *Strip Header*
        `Value`: remove specific headers from the message before
        delivering. All matching headers are removed.
        Dictionary can contain the next items:
        | Header Name | <header name to by removed> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Header Name |
        | ... | X-My-Cool-Header |

        `Key`: *Add/Edit Header*
        `Value`: inserts a header and value pair into
        the message or modifies value of an existing header
        before delivering.
        Dictionary can contain the next items:
        | Header Name | <New Header Name or Existing Header> |, mandatory
        and
        | Specify Value for New Header | <new header value> |
        or
        | Prepend to the Value of Existing Header | <text> |
        or
        | Append to the Value of Existing Header | <text> |
        or
        | Search & Replace from the Value of Existing Header | <${True}
        or ${False}> |
        and
        | Search for | <value to search for> (only if 'Search & Replace
        from the Value of Existing Header' is set to ${True}) |
        and
        | Replace with | <value to replace with> (only if 'Search & Replace
        from the Value of Existing Header' is set to ${True}) |

        *Examples:*
        | ${new_value}= | Create Dictionary | Header Name |
        | ... | X-My-Cool-Header |

        `Key`: *Add Message Tag*
        `Value`: message Tags are metadata to be used
        elsewhere in the system. For example, DLP Policies
        allow filtering by message tags.
        Dictionary can contain the next items:
        | Enter a term | <tag to be added> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Enter a term |
        | ... | blabla |

        `Key`: *Add Log Entry*
        `Value`: whether to insert customized text into IronPort Text
        Mail Logs.
        Dictionary can contain the next items:
        | Text | <text to be inserted> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Text |
        | ... | blabla |

        `Key`: *Encrypt and Deliver Now (Final Action)*
        `Value`: whether to encrypt the message, then deliver without
        further processing.
        Dictionary can contain the next items:
        | Encryption Rule | <value> |
        value can be one of these items:
        | Always use message encryption. |
        | Only use message encryption if TLS fails. |
        and
        | Encryption Profile | <name of existing encryption profile> |
        and
        | Subject | <message subject> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Encryption Rule |
        | ... | Only use message encryption if TLS fails. |
        | ... | Encryption Profile | My_Profile |
        | ... | Subject | $Subject |

        `Key`: *Bounce (Final Action)*
        `Value`: whether to send the message back to the sender
        Dictionary can contain the next items:
        | Bounce (Final Action) | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Bounce (Final Action) |
        | ... | Give me it now |

        `Key`: *Skip Remaining Content Filters (Final Action)*
        `Value`: whether to deliver the message to the next stage of processing,
        skipping any further content filters. Depending on configuration this may
        mean deliver the message to recipient(s), quarantine, or begin Outbreak
        Filters scanning.
        Dictionary can contain the next items:
        | Skip Remaining Content Filters (Final Action) | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Skip Remaining Content Filters (Final Action) |
        | ... | yeah |

        `Key`: *Drop (Final Action)*
        `Value`: whether to drop and discard the message.
        Dictionary can contain the next items:
        | Drop (Final Action) | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Drop (Final Action) |
        | ... | ololo |

        - `conditions`:  dictionary containing actions that will be included
        into this filter. Dictionary keys are condition names; same as
        corresponding container headers (case sensitive). Values are dictionaries
        which key/value pairs can be the next:

        `Key`: *Message Body or Attachment*
        `Value`: Whether the message body or attachment contain text that
        matches a specified pattern. Dictionary can contain the next items:
        | Contains text | <contained text> |
        or
        | Contains smart identifier | <identifier name> |
        or
        | Contains term in content dictionary | <dictionary name> (should
        exist in Dictionaries list) |
        and
        | Number of matches required | <number in range 1..1000> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Contains text | abcd |
        | ... | Number of matches required | 200 |

        `Key`: *Message Body*
        `Value`: whether the message body contain text matching a
        specified pattern. This does not include attachments or headers.
        Dictionary can contain the next items:
        | Contains text | <contained text> |
        or
        | Contains smart identifier | <identifier name> |
        or
        | Contains term in content dictionary | <dictionary name> (should
        exist in Dictionaries list) |
        and
        | Number of matches required | <number in range 1..1000> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Contains smart identifier |
        | ... | ABA Routing Number | Number of matches required | 200 |

        `Key`: *Message Size*
        `Value`: whether the message size is within a specified range.
        The size includes both headers and attachments.
        Dictionary can contain the next items:
        | Message size is | <value> |
        <value> is string that consists from 2 parts. First part can be one
        of these values:
        | Greater than |
        | Greater than or equal to |
        | Less than |
        | Less than or equal to |
        | Equal to |
        | Does not equal |
        The seconds part is message size in bytes

        *Examples:*
        | ${new_value}= | Create Dictionary | Message size is |
        | ... | Greater than or equal to 500 bytes |

        `Key`: *Attachment Content*
        `Value`: whether the message contains an attachment that
        contains text matching a specified pattern. This rule attempts
        to scan only content which the user would view as being an attachment.
        Dictionary can contain the next items:
        | Contains text | <contained text> |
        or
        | Contains smart identifier | <identifier name> |
        or
        | Contains term in content dictionary | <dictionary name> (should
        exist in Dictionaries list) |
        and
        | Number of matches required | <number in range 1..1000> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Contains term in content dictionary |
        | ... | profanity_txt |

        `Key`: *Attachment File Info*
        `Value`: whether the message contains an attachment of a filetype
        matching a specific filename or pattern based on its fingerprint (similar
        to a UNIX file command). Whether the declared MIME type of an attachment
        match, or does the IronPort Image Analysis engine find a suspect or
        inappropriate image.
        Dictionary can contain the next items:
        | Filename | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Contains |
        | Does Not Contain |
        | Equals |
        | Does Not Equal |
        | Begins with |
        | Does Not Begin With |
        | Ends With |
        | Does Not End With |
        and the second part is some text
        or
        | Filename contains term in content dictionary | <value> |
        <value> is existing content dictionary name
        or
        | File type is | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part can be one of:
        | Compressed | -- ace | -- arc |-- arj | -- binhex | -- bz |
        | -- bz2 | -- cab | -- gzip| -- lha | -- rar| -- sit | -- tar |
        | -- unix | -- x-windows-packager | -- zip | -- zoo | Documents |
        | -- doc, docx | -- mdb | -- mpp | -- ole | -- pdf | -- ppt, pptx |
        | -- pub | -- rtf | -- wps | -- x-wmf | -- xls, xlsx | Executables |
        | -- exe | -- java | -- msi | -- pif | Images | -- bmp | -- cur |
        | -- gif | -- ico | -- jpeg | -- pcx | -- png | -- psd | -- psp |
        | -- tga | -- tiff | -- x-pict2 | Media | -- aac | -- aiff | -- asf |
        | -- avi | -- flash | -- midi | -- mov | -- mp3 | -- mpeg | -- ogg |
        | -- ram | -- snd | -- wav | -- wma | -- wmv | Text | -- html | -- txt |
        | -- xml |
        or
        | MIME type is | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part can be MIME type name
        or
        | Image Analysis Verdict | <value> |
        Message analysis feature should be enabled ESA for this option
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part can be one of:
        | Inappropriate |
        | Suspect or Inappropriate |
        | Suspect |
        | Unscannable |
        | Clean |

        *Examples:*
        | ${new_value}= | Create Dictionary | File type is |
        | ... | Is not compressed |

        `Key`: *Attachment Protection*
        `Value`: whether the message contains a password-protected or encrypted
        attachment.
        Dictionary can contain the next items:
        | Attachment Protection | <value> |
        <value> be one of these values:
        | One or more attachments are protected |
        | One or more attachments are not protected |

        *Examples:*
        | ${new_value}= | Create Dictionary | Attachment Protection |
        | ... | One or more attachments are protected |

        `Key`: *Subject Header*
        `Value`: whether the subject header contains
        text that matches a specified pattern or match a term in a dictionary.
        Dictionary can contain the next items:
        | Subject Header | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Contains |
        | Does Not Contain |
        | Equals |
        | Does Not Equal |
        | Begins with |
        | Does Not Begin With |
        | Ends With |
        | Does Not End With |
        and the second part is some text
        or
        | Contains term in content dictionary | <dictionary name> (should
        exist in Dictionaries list) |

        *Examples:*
        | ${new_value}= | Create Dictionary | Subject Header |
        | ... | Does Not Contain blabla |

        `Key`: *Other Header*
        `Value`: whether the message contains the specified header.
        Whether the value of that header matches a specified pattern or a
        term in a dictionary.
        Dictionary can contain the next items:
        | Header Name | <matched header text> | - mandatory
        and
        | Header exists | <value here is ignored> |
        or
        | Header value | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Contains |
        | Does Not Contain |
        | Equals |
        | Does Not Equal |
        | Begins with |
        | Does Not Begin With |
        | Ends With |
        | Does Not End With |
        and the second part is some text
        or
        | Header value contains term in content dictionary | <dictionary name> (should
        exist in Dictionaries list) |

        *Examples:*
        | ${new_value}= | Create Dictionary | Header Name | blabla |
        | ... | Header value | Contains ololo |

        `Key`: *Envelope Sender*
        `Value`: whether the Envelope Sender (i.e., the Envelope From,
        <MAIL FROM>) matches a specified pattern.
        Dictionary can contain the next items:
        | Envelope Sender | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Contains |
        | Does Not Contain |
        | Equals |
        | Does Not Equal |
        | Begins with |
        | Does Not Begin With |
        | Ends With |
        | Does Not End With |
        and the second part is some text
        or
        | Matches LDAP group | <group name> |
        or
        | Contains term in content dictionary | <dictionary name> (should
        exist in Dictionaries list) |

        *Examples:*
        | ${new_value}= | Create Dictionary | Envelope Sender | Equals blabla |

        `Key`: *Envelope Recipient*
        `Value`: whether the Envelope Recipient, (i.e. the Envelope To,
        <RCPT TO>) matches a specified pattern. If a message has multiple recipients,
        only one recipient has to match for the specified action to affect the message
        to all recipients.
        Dictionary can contain the next items:
        | Envelope Recipient | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Contains |
        | Does Not Contain |
        | Equals |
        | Does Not Equal |
        | Begins with |
        | Does Not Begin With |
        | Ends With |
        | Does Not End With |
        and the second part is some text
        or
        | Matches LDAP group | <group name> |
        or
        | Contains term in content dictionary | <dictionary name> (should
        exist in Dictionaries list) |

        *Examples:*
        | ${new_value}= | Create Dictionary | Envelope Recipient | Equals blabla |

        `Key`: *Receiving Listener*
        `Value`: whether the message arrives via the specified listener
        Dictionary can contain the next items:
        | Receiving Listener | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part is existing listener name

        *Examples:*
        | ${new_value}= | Create Dictionary | Receiving Listener | Is InBoundMail |

        `Key`: *Remote IP/Hostname*
        `Value`: whether the message is sent from a remote host that matches
        a specified IP address or Hostname
        Dictionary can contain the next items:
        | Remote IP/Hostname | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part is IP/Hostname name

        *Examples:*
        | ${new_value}= | Create Dictionary | Remote IP/Hostname | Is 1.1.1.1 |

        `Key`: *Reputation Score*
        `Value`: what is the sender's SenderBase Reputation Score.
        The Reputation Score rule checks the SenderBase Reputation Score against
        another specified value.
        Dictionary can contain the next items:
        | Score | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Greater than |
        | Greater than or equal to |
        | Less than |
        | Less than or equal to
        | Equal to |
        | Does not equal |
        and the second part is score number in range -10.0..10.0
        or
        | is "None" (no score defined) | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | is "None" (no score defined) | ignored |

        `Key`: *DKIM Authentication*
        `Value`: whether DKIM Authentication is passed
        Dictionary can contain item:
        | DKIM Authentication Result | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part is one of these values:
        | Pass |
        | Neutral (message not signed) |
        | Temperror (recoverable error occurred) |
        | Permerror (unrecoverable error occurred) |
        | Hardfail (authentication tests failed) |
        | None (authentication not performed) |

        *Examples:*
        | ${new_value}= | Create Dictionary | DKIM Authentication Result | Is Pass |

        `Key`: *SPF Verification*
        `Value`: what are the SPF Verification results to match.
        Dictionary can contain item:
        | SPF Verification | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part is one of these values:
        | None |
        | Pass |
        | Neutral |
        | SoftFail |
        | Fail |
        | TempError |
        | PermError |

        *Examples:*
        | ${new_value}= | Create Dictionary | SPF Verification | Is SoftFail |

        `Key`: *Message Language*
        `Value`: Language in which message is written in
        Dictionary can contain item:
        | Message Language | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part is one of these values:
        | German |
        | English |
        | Spanish |
        | French |
        | Italian|
        | Japanese |
        | Korean |
        | Portuguese |
        | Russian |
        | Undetermined |
        | Chinese |
        | Taiwanese |

        *Examples:*
        | ${new_value}= | Create Dictionary | Message Language | Is Deutsch |
        | ${new_value}= | Create Dictionary | Message Language | Is English Spanish Taiwanese |

        *Exceptions:*
        - `ValueError`: if incorrect value is given

        `Key` : *Macro Detection*
        `Value` : Macros to be matched in email attachments.
        Dictionary can contain item:
        | Add Macros | <value> |
        <value> can contain one or multiple type(s) from available Macros:
        | OFFICE |
        | OLE |
        | PDF |

        | Remove Macros | <value> |
        <value> can contain a list of already configured Macros:
        | OFFICE |
        | OLE |
        | PDF |

        `Key` : *Geolocation*
        `Value` : Countries to be matched for incoming/outgoing connections.
        Dictionary can contain below items:
        | Add Countries | <value> |
        <value> can be one or multiple or ALL from the available countries.
        For example:
            Afghanistan            Aland Islands            Albania
            Algeria                American Samoa           Andorra
            Angola                 Anguilla                 Anonymous Proxy
            Antarctica             Antigua and Barbuda      Argentina
            Armenia                Aruba                    Asia/Pacific Region
            Australia              Austria                  Azerbaijan
            Bahamas                Bahrain                  Bangladesh
            Barbados               Belarus                  Belgium
            Belize                 Benin                    Bermuda
            Bhutan                 Bolivia                  Burundi
            Cambodia               Cameroon                 Canada
            Cape Verde             Cayman Islands           Central African Republic
            Chad                   Chile                    China
            Christmas Island       Cocos (Keeling) Islands  Colombia
            Comoros                Congo                    Congo, The Democratic Republic of the
            Cook Islands           Costa Rica               Cote d'Ivoire
            Croatia                Cuba                     Curacao
            Cyprus                 Czech Republic           Denmark
            Djibouti               Dominica                 Dominican Republic
            Ecuador                Egypt                    Europe

            Please refer to ESA WebUI for complete list of available counties list.

        *Examples:*
        | ${actions}= | Content Filter Create Actions |
        | ... | Quarantine |                         ${quarantine_action} |
        | ... | Strip Attachment by Content |        ${strip_attachment_by_content_action} |
        | ... | Strip Attachment by File Info |      ${strip_attachment_by_fileinfo_action} |
        | ... | Bypass Outbreak Filter Scanning |    ${bypass_outbreak_filter_action} |
        | ... | Bypass DKIM Signing |                ${bypass_DKIM_signing_action} |
        | ... | Send Copy (Bcc:) |                   ${send_copy_bcc_action} |
        | ... | Notify |                             ${notify_action} |
        | ... | Change Recipient to |                ${change_rcpt_to_action} |
        | ... | Send to Alternate Destination Host | ${send_to_alternate_action} |
        | ... | Strip Header |                       ${strip_header_action} |
        | ... | Add/Edit Header |                    ${add_edit_header_action} |
        | ... | Add Message Tag |                    ${add_message_tag_action} |
        | ... | Add Log Entry |                      ${add_log_entry_action} |
        | ... | Bounce (Final Action) |              ${bounce_final_action} |
        | ${conditions}= | Content Filter Create Conditions |
        | ... | Message Body or Attachment |         ${msg_body_or_attachment_cond} |
        | ... | Message Size |                       ${msg_size_cond} |
        | ... | Attachment Content |                 ${attachment_content_cond} |
        | ... | Attachment File Info |               ${attachment_fileinfo_cond} |
        | ... | Attachment Protection |              ${attachments_protection_cond} |
        | ... | Subject Header |                     ${subject_header_cond} |
        | ... | Other Header |                       ${other_header_cond} |
        | ... | Envelope Sender |                    ${envelope_sender_cond} |
        | ... | Envelope Recipient |                 ${envelope_recipient_cond} |
        | ... | Remote IP/Hostname |                 ${remote_ip_hostname_cond} |
        | ... | Reputation Score |                   ${reputation_score_cond} |
        | ... | DKIM Authentication |                ${dkim_auth_cond} |
        | ... | SPF Verification |                   ${spf_verification_cond} |
        | ... | Message Language |                   ${message_language_cond} |
        | ... | Geolocation      |                   ${counties_condtion}     |
        | Content Filter Add | Incoming | my_filter |
        | ... | Super filter | ${actions} | ${conditions} |
        """
        self.click_button(ADD_FILTER)

        self.input_text(FILTER_NAME, name)
        if description:
            self.input_text(FILTER_DESCRIPTION, description)
        if not actions:
            raise ValueError('Content filter "%s" should contain at least one action' % \
                             (name,))
        actions_controller = self._get_filter_actions_controller(filter_type)
        actions_controller.add(actions)
        if conditions:
            conditions_controller = self._get_filter_conditions_controller(filter_type)
            conditions_controller.add(conditions)

        self.click_button(SAVE_BUTTON)
        self._check_action_result()

    @go_to_filter
    def content_filter_delete(self, filter_type, name):
        """Delete existing content filter

        *Parameters:*
        - `filter_type`: content filter type, either Incoming or
        Outgoing, mandatory
        - `name`: existing filter name to deleted, mandatory
        - `description`: your description for newly created filter

        *Exceptions:*
        - `ValueError`: if incorrect value is given

        *Examples:*
        | Content Filter Delete | Incoming | my incoming filter |
        """
        try:
            self.click_button(DELETE_BUTTON(name), 'don\'t wait')
        except Exception as e:
            raise ValueError('Content filter having name "%s" is not found' % \
                             (name,))
        self._click_continue_button()
