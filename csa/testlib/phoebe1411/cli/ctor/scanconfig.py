#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/scanconfig.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

import re

import clictorbase
from clictorbase import IafCliConfiguratorBase, DEFAULT, \
    IafCliValueError, IafCliParamMap

from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES, NO, is_yes

class scanconfig(clictorbase.IafCliConfiguratorBase):

    newlines = 1

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('The value \S+ is already in the table.', \
             REGEX): IafCliValueError,
            ('Could not reach target machine:', EXACT): IafCliValueError,
            ('Unable to perform operation due to an I/O error.', \
             EXACT): IafCliValueError,
            ('Configuration filesystem is full.', EXACT): IafCliValueError,
            ('Error writing file.', EXACT): IafCliValueError,
            ('Invalid type', EXACT): IafCliValueError,
            ('Parse error', EXACT): IafCliValueError,
            ('Error reading file.', EXACT): IafCliValueError,
            ('MIME types may only contain', EXACT): IafCliValueError,
            })

    def __call__(self):
        self._writeln('scanconfig')
        return self

    def new(self, mime_type):
        self._query_response('NEW')
        self._query_response(mime_type)
        self._to_the_top(self.newlines)

    def delete(self, num_or_type, choice=YES):
        self._query_response('DELETE')
        self._query_response(num_or_type)
        # It'is the confirmation to delete:
        # Question: Are you sure you want to delete the MIME type image/*?
        self._query_response(choice)
        self._to_the_top(self.newlines)

    def Print(self):
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return raw

    def Import(self, file_name):
        self._query_response('IMPORT')
        self._query_response(file_name)
        self._to_the_top(self.newlines)

    def export(self, file_name):
        self._query_response('EXPORT')
        self._query_response(file_name)
        self._to_the_top(self.newlines)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.newlines)

    def setup(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        # operation values are: Scan, Skip.
        param_map['operation'] = ['Choose one:', DEFAULT, 1]
        param_map['depth'] = ['Enter the maximum depth', DEFAULT]
        param_map['max_size'] = ['Enter the maximum size', DEFAULT]
        param_map['scan_metadata'] = ['scan attachment metadata', DEFAULT]
        param_map['timeout'] = ['attachment scanning timeout', DEFAULT]
        param_map['assume_dirty'] = ['assume the attachment matches' \
                                        ' the search pattern', DEFAULT]
        param_map['bypass_on_error'] = ['should all filters be bypassed',
                                         DEFAULT]
        param_map['timeout_for_zipfiles'] = ['zip file to be unscannable if', DEFAULT]
        # fail_action values are: Deliver, Bounce, Drop
        param_map['fail_action'] = ['message could not be deconstructed', \
                                         DEFAULT, 1]
        # encoding requires unique indent one of the following rows:
        #1. US-ASCII
        #2. Unicode (UTF-8)
        #3. Unicode (UTF-16)
        #4. Western European/Latin-1 (ISO 8859-1)
        #5. Western European/Latin-1 (Windows CP1252)
        #6. Traditional Chinese (Big 5)
        #7. Simplified Chinese (GB 2312)
        #8. Simplified Chinese (HZ GB 2312)
        #9. Korean (ISO 2022-KR)
        #10. Korean (KS-C-5601/EUC-KR)
        #11. Japanese (Shift-JIS (X0123))
        #12. Japanese (ISO-2022-JP)
        #13. Japanese (EUC)
        param_map['encoding'] = ['Configure encoding to use', \
                                         DEFAULT, 1]
        param_map['unscan_extract_failures']     = ['Unscannable messages due to extraction failures', DEFAULT]
        param_map['unscan_action_message']       = ['Action applied to the original message', DEFAULT]
        param_map['unscan_quarantine_policy']    = ['quarantine to send the message to', DEFAULT, True]
        param_map['unscan_alt_hostname']         = ['message to an alternate mailhost', DEFAULT]
        param_map['unscan_mailhost']             = ['mailhost to deliver to', DEFAULT]
        param_map['unscan_alt_email']            = ['message to an alternate email address', DEFAULT]
        param_map['unscan_address']              = ['address to deliver to', DEFAULT]
        param_map['unscan_add_header']           = ['to add a custom header', DEFAULT]
        param_map['unscan_header_name']          = ['the header name', DEFAULT]
        param_map['unscan_header_content']       = ['the header content', DEFAULT]
        param_map['unscan_modify_subject']       = ['modify the subject', DEFAULT]
        param_map['unscan_position_text']        = ['Select position of text', DEFAULT]
        param_map['unscan_text']                 = ['Enter the text to add', DEFAULT]
        param_map['rfc_violation_failures']      = ['Unscannable messages due to RFC violations', DEFAULT]
        param_map['rfc_action_message']          = ['Action applied to the original message', DEFAULT]
        param_map['rfc_quarantine_policy']       = ['quarantine to send the message to', DEFAULT, True]
        param_map['rfc_alt_hostname']            = ['message to an alternate mailhost', DEFAULT]
        param_map['rfc_mailhost']                = ['mailhost to deliver to', DEFAULT]
        param_map['rfc_alt_email']               = ['message to an alternate email address', DEFAULT]
        param_map['rfc_address']                 = ['address to deliver to', DEFAULT]
        param_map['rfc_add_header']              = ['to add a custom header', DEFAULT]
        param_map['rfc_header_name']             = ['the header name', DEFAULT]
        param_map['rfc_header_content']          = ['the header content', DEFAULT]
        param_map['rfc_modify_subject']          = ['modify the subject', DEFAULT]
        param_map['rfc_position_text']           = ['Select position of text', DEFAULT]
        param_map['rfc_text']                    = ['Enter the text to add', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        self._process_input(param_map)

    def smime(self, use_smime=NO):
        self._query_response('SMIME')
        self._query_response(use_smime)
        self._to_the_top(self.newlines)


    def safeprint(self, input_dict=None, **kwargs):
        if 'modify_file_types' in kwargs and is_yes(kwargs['modify_file_types']):
            param_map = IafCliParamMap(end_of_command='Enter comma separated numbers')
        else:
            param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['maximum_document_size'] = ['the maximum attachment size that you can safe print.', DEFAULT]
        param_map['maximum_page_count'] = ['maximum number of pages that you can safe print in an attachment', DEFAULT]
        param_map['use_recommended_image_quality'] = ['use the recommended image quality value to safe print an attachment', DEFAULT]
        param_map['image_quality_value'] = ['image quality value selected to safe print an attachment', DEFAULT]
        param_map['modify_file_types'] = ['modify the file types selected to safe print an attachment', DEFAULT]
        actual_dict = {}
        for key in kwargs.keys():
            if key in param_map._map.keys():
                actual_dict[key] = kwargs[key]
        param_map.update(input_dict or actual_dict)

        self._query_response('SAFEPRINT')
        self._process_input(param_map, do_restart=False)

        if 'modify_file_types' in kwargs and is_yes(kwargs['modify_file_types']):
            file_groups = kwargs['select_file_groups'].split(',')
            self._query_response(kwargs['select_file_groups'])
            for group in file_groups:
                if 'select_file_action' in kwargs and kwargs['select_file_action'].lower() != 'print':
                    file_group_map = self._get_group_file_types_map(group, kwargs['select_filetypes'])
                    self._query_response(kwargs['select_file_action'])
                    self._query_response(self._parse_file_types(file_group_map[group]))
                    self._writeln('')
                else:
                    self._query_response(kwargs['select_file_action'])

        self._to_the_top(2)

    def protected_attachment_config(self, input_dict=None, **kwargs):	
        param_map = IafCliParamMap(end_of_command='Choose the operation')	
        param_map['scan_for_inbound_mails'] = [	
            'scan password-protected attachments for inbound mails', DEFAULT]	
        param_map['scan_for_outbound_mails'] = [	
            'scan password-protected attachments for outbound mails', DEFAULT]	
        param_map.update(input_dict or kwargs)	
        self._query_response('PROTECTEDATTACHMENTCONFIG')	
        self._process_input(param_map)	
        self._to_the_top(self.newlines)	

    def protected_attachment_config_status(self):	
        status = {}	
        self.clearbuf()

        param_map = IafCliParamMap(end_of_command='Choose the operation')   
        param_map['scan_for_inbound_mails'] = [    
            'scan password-protected attachments for inbound mails', DEFAULT]   
        param_map['scan_for_outbound_mails'] = [   
            'scan password-protected attachments for outbound mails', DEFAULT]  
        param_map.update()
        self._query_response('PROTECTEDATTACHMENTCONFIG')   
        self._process_input(param_map)  
        self._to_the_top(self.newlines)

        output = self.getbuf()  
        if output:	
            key, value = re.search(r'(Decryption .* for Inbound mails):\s+(disabled|enabled)', output,	
                                   re.MULTILINE).groups()	
            status[key] = value	
            key, value = re.search(r'(Decryption .* for Outbound mails):\s+(disabled|enabled)', output,	
                                   re.MULTILINE).groups()	
            status[key] = value	
        return status	

    def _get_group_file_types_map(self, group, file_types):
        files_map = {}
        if '|' in file_types:
            files = file_types.split('|')

            for file in files:
                (group, f_types) = file.split(':')
                files_map[group] = f_types
        else:
            files_map[group] = file_types

        return files_map

    def _parse_file_types(self, file_list):
        file_list = re.sub(r'\[|\]|\'|\"', '', file_list)
        return file_list

