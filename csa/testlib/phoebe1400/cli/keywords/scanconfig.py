#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/scanconfig.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase


class scanconfig(CliKeywordBase):

    """scanconfig -- Configure options for attachment scanning"""

    def get_keyword_names(self):
        return ['scan_config_new',
                'scan_config_print',
                'scan_config_delete',
                'scan_config_import',
                'scan_config_export',
                'scan_config_clear',
                'scan_config_setup',
                'scan_config_smime',
	            'scan_config_safe_print',	
                'scan_config_protected_attachment_config',
                'scan_config_protected_attachment_config_status',
                'scan_config_protected_attachment_config_new_password',
                'scan_config_protected_attachment_config_edit_password',
                'scan_config_protected_attachment_config_swap_password',
                'scan_config_protected_attachment_config_delete_password',
                'scan_config_protected_attachment_config_print_password']

    def scan_config_new(self, mime_type):
        """Create new MIME type that will be skipped/scanned.

        scanconfig > new

        *Parameters:*
        - `mime_type`: the MIME type or fingerprint for which you want to skip.
        Wildcard MIME types of the form "x/*" or "*/y" are allowed.

        *Examples:*
        | Scan Config New | application/pdf |
        """
        self._cli.scanconfig().new(mime_type)

    def scan_config_print(self):
        """Return a list of MIME types

        scanconfig > print

        *Return:*
        Raw output

        *Examples:*
        | ${mtypes}= | Scan Config Print |
        | Log | ${mtypes} |
        """
        return self._cli.scanconfig().Print()

    def scan_config_delete(self, num_or_type, choice='YES'):
        """Delete existing MIME type

        scanconfig > delete

        *Parameters:*
        - `num_or_type`: name of MIME type to be deleted or its number
        in the list (in print command output)
        - `choice`: removal confirmation, either yes or no

        *Examples:*
        | Scan Config Delete | application/pdf |
        """
        self._cli.scanconfig().delete(num_or_type, choice)

    def scan_config_import(self, file_name):
        """Import MIME types list from a file

        scanconfig > import

        *Parameters:*
        - `file_name`: path to a file from which list entries will be imported

        *Examples:*
        | Scan Config Import | types_list.txt |
        """
        self._cli.scanconfig().Import(file_name)

    def scan_config_export(self, file_name):
        """Import MIME types list to a file

        scanconfig > export

        *Parameters:*
        - `file_name`: path to a file to which list entries will be exported

        *Examples:*
        | Scan Config Export | types_list.txt |
        """
        self._cli.scanconfig().export(file_name)

    def scan_config_clear(self):
        """Clear MIME types list

        scanconfig > clear

        *Examples:*
        | Scan Config Clear |
        """
        self._cli.scanconfig().clear()

    def scan_config_setup(self, *args):
        """Configure attachments scanning options

        scanconfig > setup

        *Parameters:*
        - `operation`: default operation that will be applied to attachments,
        either:
        | 1 | Scan only attachments with MIME types or fingerprints in the list. |
        | 2 | Skip attachments with MIME types or fingerprints in the list. |
        - `depth`: the maximum depth of attachment recursion to scan, number
        - `max_size`: the maximum size of attachment to scan, in bytes
        - `scan_metadata`: whether to scan attachment metadata, yes or no
        - `timeout`: attachment scanning timeout, in seconds
        - `assume_dirty`: if a message has attachments that were not scanned for
        any reason (e.g. because of size, depth limits, or scanning timeout),
        assume the attachment matches the search pattern, yes or no
        - `timeout_for_zipfiles`: Timeout to assume zip files are unscannable if
        files in the archive can not be read.
        - `fail_action`: If a message could not be deconstructed into its
        component parts in order to remove specified attachments, the system should
        | 1 | Deliver |
        | 2 | Bounce |
        | 3 | Drop |
        - `bypass_on_error`: whether to bypass all filters or not, yes or no
        - `encoding`: encoding to use when none is specified for plain body
        text or anything with MIME type plain/text or plain/html
        | 1 | US-ASCII |
        | 2 | Unicode (UTF-8) |
        | 3 | Unicode (UTF-16) |
        | 4 | Western European/Latin-1 (ISO 8859-1) |
        | 5 | Western European/Latin-1 (Windows CP1252) |
        | 6 | Traditional Chinese (Big 5) |
        | 7 | Simplified Chinese (GB 2312) |
        | 8 | Simplified Chinese (HZ GB 2312) |
        | 9 | Korean (ISO 2022-KR) |
        | 10 | Korean (KS-C-5601/EUC-KR) |
        | 11 | Japanese (Shift-JIS (X0123)) |
        | 12 | Japanese (ISO-2022-JP) |
        | 13 | Japanese (EUC) |

        *Examples:*
        | Scan Config Setup | operation=2 | fail_action=Drop |
        | ... | timeout=10 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.scanconfig().setup(**kwargs)

    def scan_config_smime(self, use_smime='NO'):
        """Configure S/MIME unpacking

        scanconfig > smime

        *Parameters:*
        - `use_smime`: whether to convert opaque-signed messages to clear-signed.
        This will provide the clear text content for various blades to process.
        Yes or no

        *Examples:*
        | Scan Config SMIME | yes |
        """
        self._cli.scanconfig().smime(use_smime)

    def scan_config_safe_print(self, *args):
        """Configure SAFEPRINT settings

        scanconfig > safeprint

        *Parameters:*
        - `maximum_document_size`: Maximum document size that can be safe-printed.
        - `maximum_page_count`: Maximum page count that can be safe-printed.
        - `use_recommended_image_quality`: Use the recommended image quality for
                safe-printed documents.
                Allowed values: Yes or No.
        - `image_quality_value`: Image quality value for safe-printed documents(10 - 90).
                Valid only when use_recommended_image_quality param is set to No.
                Warning! Increasing the value will increase the size of safe-printed documents.
        - `modify_file_types`: Modify the file types selected for safeprint.
                Allowed values: Yes or No
        - `select_file_groups`: Comma separated list of numbers to select file types
                associated with the file groups.
        - `select_filetypes`: Comma separated list of numbers to select file types
                belonging to the above selected group.
        ` `select_file_action`: Action to be performed on the selected file groups
                and file types.
                Allowed values: PRINT | DELETE | ADD

        *Examples:*
        | Scan Config Safe Print                    |

        | Scan Config Safe Print                    |
        | ... | maximum_document_size=1024          |
        | ... | maximum_page_count=20               |
        | ... | use_recommended_image_quality=Yes   |
        | ... | modify_file_types=No                |

        | Scan Config Safe Print                    |
        | ... | maximum_document_size=102400        |
        | ... | maximum_page_count=5                |
        | ... | use_recommended_image_quality=No    |
        | ... | image_quality_value=50              |

        | Scan Config Safe Print                    |
        | ... | maximum_document_size=10240         |
        | ... | maximum_page_count=15               |
        | ... | modify_file_types=Yes               |
        | ... | select_file_groups=2                |
        | ... | select_filetypes=1,2                |
        | ... | select_file_action=delete           |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.scanconfig().safeprint(**kwargs)	

    def scan_config_protected_attachment_config(self, *args):	
        """Configure PROTECTEDATTACHMENTCONFIG settings	
        scanconfig > protectedattachmentconfig 	
        *Parameters:*	
        - `scan_password_protected_for_inbound_mails`: Do you want to scan password-protected attachments for inbound mails	
            attachments for inbound mails? Allowed values - Y/N	
        - `scan_password_protected_for_outbound_mails`: Do you want to scan password-protected attachments for inbound mails	
            attachments for outbound mails? Allowed values - Y/N	
        *Returns:*	
        None	
        *Examples:*	
        | Scan Config Protected Attachment Config             |
        | ... | scan_password_protected_for_inbound_mails=Y   |	
        | ... | scan_password_protected_for_outbound_mails=Y  |	
        """
        kwargs = self._convert_to_dict(args)
        # self._cli.scanconfig().protected_attachment().config(**kwargs)
        self._cli.scanconfig().protected_attachment_config(**kwargs).config()

    def scan_config_protected_attachment_config_status(self):	
        """Return the status of PROTECTEDATTACHMENTCONFIG settings	
        scanconfig > protectedattachmentconfig	
        *Parameters:*	
        None	
        *Returns:*	
        A dictionary containing the status of password protected attachments decryption settings.	
            Keys:   Scanning of password-protected attachments for inbound mails
                    Scanning of password-protected attachments for outbound mails
        *Examples:*	
        | ${status}=                | Scan Config Protected Attachment Config Status                                       |
        | ${inbound}=               | Get From Dictionary | Scanning of password-protected attachments for outbound mails  |	
        | Should Be Equal As String | ${inbound}          | enabled                                                        |	
        | ${outbound}=              | Get From Dictionary | Scanning of password-protected attachments for outbound mails  |	
        | Should Be Equal As String | ${outbound}         | disabled                                                       |	
        """	
        return self._cli.scanconfig().protected_attachment_config().status()

    def scan_config_protected_attachment_config_new_password(self, *args):
        """Configure PROTECTEDATTACHMENTCONFIG settings	
        scanconfig > protectedattachmentconfig -> new
        *Parameters:*	
        - `priority`: Enter a priority for the new password
        - `password`: Enter the new password	
        *Returns:*	
        None	
        *Examples:*	
        | Scan Config Protected Attachment Config New Password  |
        | ... | priority=0                                      |
        | ... | password=test123                                |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.scanconfig().protected_attachment_config().new_password(**kwargs)

    def scan_config_protected_attachment_config_edit_password(self, *args):
        """Configure PROTECTEDATTACHMENTCONFIG settings	
        scanconfig > protectedattachmentconfig -> edit
        *Parameters:*
        - `priority_or_password_to_edit`: Enter the priority or the password that you want to edit
        - `new_priority`: Enter a priority for the new password
        - `new_password`: Enter the new password	
        *Returns:*	
        None	
        *Examples:*	
        | Scan Config Protected Attachment Config Edit Password  |
        | ... | priority_or_password_to_edit=0                   |
        | ... | new_priority=0                                   |
        | ... | new_password=test1234                            |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.scanconfig().protected_attachment_config().edit_password(**kwargs)
    
    def scan_config_protected_attachment_config_swap_password(self, *args):
        """Configure PROTECTEDATTACHMENTCONFIG settings	
        scanconfig > protectedattachmentconfig -> swap
        *Parameters:*
        - `first_password_priority`: Enter the priority of the first password that you want to switch
        - `second_password_priority`: Enter the priority of the second password that you want to switch	
        *Returns:*	
        None	
        *Examples:*	
        | Scan Config Protected Attachment Config Swap Password  |
        | ... | first_password_priority=0                        |
        | ... | second_password_priority=1                       |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.scanconfig().protected_attachment_config().swap_password(**kwargs)

    def scan_config_protected_attachment_config_delete_password(self, *args):
        """Configure PROTECTEDATTACHMENTCONFIG settings	
        scanconfig > protectedattachmentconfig -> delete
        *Parameters:*
        - `password_priority`: Enter the priority of the password that you want to delete
        *Returns:*	
        None	
        *Examples:*	
        | Scan Config Protected Attachment Config Delete Password  |
        | ... | password_priority=1                                |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.scanconfig().protected_attachment_config().delete_password(**kwargs)

    def scan_config_protected_attachment_config_print_password(self):
        """Configure PROTECTEDATTACHMENTCONFIG settings	
        scanconfig > protectedattachmentconfig -> print
        *Parameters:*
        None
        *Returns:*	
        A list of dictionaries with `priority` and `password` as keys.
        *Examples:*	
        | ${passwords} = Scan Config Protected Attachment Config Print Password  |
        | Log List              | ${passwords}                                   |
        | ${password}           | Get From List         | 0                      |
        | ${password_priority}  | Get From Dictionary   | ${password} | priority |
        | ${password_value}     | Get From Dictionary   | ${password} | password |
        """
        return self._cli.scanconfig().protected_attachment_config().print_password()
