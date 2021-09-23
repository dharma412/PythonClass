#!/usr/bin/env python -tt

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs


SKIP_IF_IN_LIST_RADIOGROUP = ('Action for attachments',
                                {'Scan': "//input[@id='skip_if_in_list_scan']",
                                 'Skip': "//input[@id='skip_if_in_list_skip']"})
MAX_DEPTH = ('Maximum depth of attachment recursion',
             "//input[@name='depth_limit']")
MAX_SIZE = ('Maximum attachment size',
             "//input[@name='size_limit']")
SCAN_METADATA_RADIOGROUP = ('Attachment Metadata scan',
                                {'Enabled': "//input[@id='scan_metadata_enabled']",
                                 'Disabled': "//input[@id='scan_metadata_disabled']"})
SCAN_TIMEOUT = ('Attachment scanning timeout',
                "//input[@name='scan_timeout']")
ASSUME_PATTERN_RADIOGROUP = ('Assume attachment matches pattern',
                             {'Yes': "//input[@id='assume_dirty_yes']",
                              'No': "//input[@id='assume_dirty_no']"})
ASSUME_ZIP_FILE_UNSCANNABLE_RADIOGROUP = ('Assume zip file to be unscannable',	
                               {'Yes': "//input[@id='assume_unscannable_zip_dirty_yes']",	
                                'No': "//input[@id='assume_unscannable_zip_dirty_no']"})
ACTION_DESCONSTR_RADIOGROUP = ('Action when message cannot be deconstructed',
                               {'Deliver': "//input[@id='mimeparse_fail_action_deliver']",
                                'Bounce': "//input[@id='mimeparse_fail_action_bounce']",
                                'Drop': "//input[@id='mimeparse_fail_action_drop']"})
BYPASS_ALL_FILTERS_RADIOGROUP = ('Bypass all filters',	
                                 {'Yes': "//input[@id='abort_on_runtime_error_yes']",	
                                  'No': "//input[@id='abort_on_runtime_error_no']"})
ENCODING_COMBO = ('Encoding to use',
                  "//select[@name='default_text_encoding']")
CONVERT_OPAQUE_RADIOGROUP = ('Convert opaque-signed messages',
                             {'Enabled': "//input[@id='smime_unpack_enabled']",
                              'Disabled': "//input[@id='smime_unpack_disabled']"})

SAFE_PRINT_MAX_FILE_SIZE = ('Maximum File Size', "//input[@name='sp_max_doc_size']")
SAFE_PRINT_MAX_PAGE_COUNT = ('Maximum Page Count', "//input[@name='sp_max_page_count']")
SAFE_PRINT_DOC_QUALITY_RADIOGROUP = ('Document Quality',	
                                     {"Use Default Value": "//input[@id='sp_doc_quality_default']",	
                                      "Enter Custom Value": "//input[@id='sp_doc_quality_custom']"})	
SAFE_PRINT_CUSTOM_DOC_QUALITY = ('Custom Document Quality Value', "//input[@name='sp_doc_quality']")
SAFE_PRINT_DEFAULT_FILE_TYPES = ('File Type Selection',
                                    { 'Select All': "//input[@id='select_all']",
                                      'Document': "//input[@id='Document']",
                                      'Microsoft Documents': "//input[@id='Microsoft Documents']"})

SAFE_PRINT_EXPAND_ALL_FILE_TYPES = "//a[@class='expandAll']"
SAFE_PRINT_COLLAPSE_ALL_FILE_TYPES = "//a[@class='collapseAll']"
# Reset operation is yet to be implemented
# Reset button does not work with Firefox v3
SAFE_PRINT_RESET_FILE_TYPES = "//input[@id='reset']"
SAFE_PRINT_WATERMARK_RADIOGROUP = ('Watermark',	
                                   {"Enabled": "//input[@id='sp_watermark_enabled']",	
                                    "Disabled": "//input[@id='sp_watermark_disabled']"})	
SAFE_PRINT_CUSTOM_WATERMARK_TEXT = "//input[@id='sp_watermark_text']"	
SAFE_PRINT_COVER_PAGE_RADIOGROUP = ('Cover Page',	
                                    {"Enabled": "//input[@id='sp_front_page_enabled']",	
                                     "Disabled": "//input[@id='sp_front_page_disabled']"})	
SAFE_PRINT_COVER_PAGE_CUSTOM_TEXT = "//input[@id='sp_front_page_text']"	
INBOUND_PWD_PROTECTED_ATTACHMENTS_DECRYPTION_RADIOGROUP = ('Decrypt Inbound Password Protected Attachments',	
                             {'Yes': "//input[@id='enable_ppfa_inbound_enabled']",	
                              'No': "//input[@id='enable_ppfa_inbound_disabled']"})	
OUTBOUND_PWD_PROTECTED_ATTACHMENTS_DECRYPTION_RADIOGROUP = ('Decrypt Outbound Password Protected Attachments',	
                             {'Yes': "//input[@id='enable_ppfa_outbound_enabled']",	
                              'No': "//input[@id='enable_ppfa_outbound_disabled']"})	
# Actions for Unscannable Messages due to decoding errors found during URL Filtering Actions	
# DE --> Decoding Error	
UNSCANNABLE_DE_ADVANCED_ARROW = "//*[@id='basic_decode_err_settings_url_rewrite']//a[contains(text(), 'Advanced')]"	
UNSCANNABLE_ENABLE_DE_ACTION_RADIOGROUP = (	
        'Enable Actions for Unscannable Messages due to decoding errors',	
        {'Yes': "//input[@id='de_enabled']",	
         'No': "input[@id='de_disabled']"})	
UNSCANNABLE_DE_ACTION_APPLY_COMBO = (	
        'Unscannable Decoding Error Action',	
        "//select[@id='de_action']")	
UNSCANNABLE_DE_QUARANTINE_COMBO = (	
        'Unscannable Decoding Error Send To Quarnatine',	
        "//select[@name='de_quarantine_name']")	
UNSCANNABLE_DE_MODIFY_SUBJECT_RADIOGROUP = (	
        'Unscannable Decoding Error Modify Message Subject',	
        {'No': "//input[@id='de_subj_no']",	
         'Prepend': "//input[@id='de_subj_pre']",	
         'Append': "//input[@id='de_subj_app']"})	
UNSCANNABLE_DE_SUBJECT = (	
        'Unscannable Decoding Error Message Subject',	
        "//input[@id='de_subj_txt']")	
UNSCANNABLE_DE_ADD_CUSTOM_HEADER_RADIOGROUP = (	
        'Unscannable Decoding Error Add Custom Header',	
        {'Yes': "//input[@id='de_hdr_yes']",	
         'No': "//input[@id='de_hdr_no']"})	
UNSCANNABLE_DE_CUSTOM_HEADER_NAME = (	
        'Unscannable Decoding Error Custom Header Name',	
        "//input[@id='de__hdr_n']")	
UNSCANNABLE_DE_CUSTOM_HEADER_VALUE = (	
        'Unscannable Decoding Error Custom Header Value',	
        "//input[@id='de__hdr_t']")	
UNSCANNABLE_DE_MODIFY_RECIPIENT_RADIOGROUP = (	
        'Unscannable Decoding Error Modify Recipient',	
        {'Yes': "//input[@id='de_rbyes']",	
         'No': "//input[@id='de_rbno']"})	
UNSCANNABLE_DE_RECIPIENT_ADDRESS = (	
        'Unscannable Decoding Error Recipient Address',	
        "//input[@id='de_rbaddr']")	
UNSCANNABLE_DE_ALT_DESTINATION_RADIOGROUP = (	
        'Unscannable Decoding Error Send To Alternate Destination Host',	
        {'Yes': "//input[@id='de_altyes']",	
         'No': "//input[@id='de_altno']"})	
UNSCANNABLE_DE_ALT_DESTINATION_HOST = (	
        'Unscannable Decoding Error Alternate Destination Host',	
        "//input[@id='de_alttxt']")	
# Actions for Unscannable Messages due to Extraction Failures	
# EF --> Extraction Failures	
UNSCANNABLE_EF_ADVANCED_ARROW = "//*[@id='basic_us_settings_ef']//a[contains(text(), 'Advanced')]"	
UNSCANNABLE_ENABLE_EF_ACTION_RADIOGROUP = (	
        'Enable Actions for Unscannable Messages due to Extraction Failures',	
        {'Yes': "//input[@id='ef_enabled']",	
         'No': "input[@id='ef_disabled']"})	
UNSCANNABLE_EF_ACTION_APPLY_COMBO = (	
        'Unscannable Extraction Failures Action',	
        "//select[@id='ef_action']")	
UNSCANNABLE_EE_QUARANTINE_COMBO = (	
        'Unscannable Extraction Failures Send To Quarnatine',	
        "//select[@name='ef_quarantine_name']")	
UNSCANNABLE_EF_MODIFY_SUBJECT_RADIOGROUP = (	
        'Unscannable Extraction Failures Modify Message Subject',	
        {'No': "//input[@id='ef_subj_no']",	
         'Prepend': "//input[@id='ef_subj_pre']",	
         'Append': "//input[@id='ef_subj_app']"})	
UNSCANNABLE_EF_SUBJECT = (	
        'Unscannable Extraction Failures Message Subject',	
        "//input[@id='ef_subj_txt']")	
UNSCANNABLE_EF_ADD_CUSTOM_HEADER_RADIOGROUP = (	
        'Unscannable Extraction Failures Add Custom Header',	
        {'Yes': "//input[@id='ef_hdr_yes']",	
         'No': "//input[@id='ef_hdr_no']"})	
UNSCANNABLE_EF_CUSTOM_HEADER_NAME = (	
        'Unscannable Extraction Failures Custom Header Name',	
        "//input[@id='ef__hdr_n']")	
UNSCANNABLE_EF_CUSTOM_HEADER_VALUE = (	
        'Unscannable Extraction Failures Custom Header Value',	
        "//input[@id='ef__hdr_t']")	
UNSCANNABLE_EF_MODIFY_RECIPIENT_RADIOGROUP = (	
        'Unscannable Extraction Failures Modify Recipient',	
        {'Yes': "//input[@id='ef_rbyes']",	
         'No': "//input[@id='ef_rbno']"})	
UNSCANNABLE_EF_RECIPIENT_ADDRESS = (	
        'Unscannable Extraction Failures Recipient Address',	
        "//input[@id='ef_rbaddr']")	
UNSCANNABLE_EF_ALT_DESTINATION_RADIOGROUP = (	
        'Unscannable Extraction Failures Send To Alternate Destination Host',	
        {'Yes': "//input[@id='ef_altyes']",	
         'No': "//input[@id='ef_altno']"})	
UNSCANNABLE_EF_ALT_DESTINATION_HOST = (	
        'Unscannable Extraction Failures Alternate Destination Host',	
        "//input[@id='ef_alttxt']")	
# Actions for Unscannable Messages due to RFC Violations	
# RFCV --> RFC Violations	
UNSCANNABLE_RFCV_ADVANCED_ARROW = "//*[@id='basic_us_settings_rfc']//a[contains(text(), 'Advanced')]"	
UNSCANNABLE_ENABLE_RFCV_ACTION_RADIOGROUP = (	
        'Enable Actions for Unscannable Messages due to RFC Violations',	
        {'Yes': "//input[@id='rfc_enabled']",	
         'No': "input[@id='rfc_disabled']"})	
UNSCANNABLE_RFCV_ACTION_APPLY_COMBO = (	
        'Unscannable RFC Violations Action',	
        "//select[@id='rfc_action']")	
UNSCANNABLE_RFCV_QUARANTINE_COMBO = (	
        'Unscannable RFC Violations Send To Quarnatine',	
        "//select[@name='rfc_quarantine_name']")	
UNSCANNABLE_RFCV_MODIFY_SUBJECT_RADIOGROUP = (	
        'Unscannable RFC Violations Modify Message Subject',	
        {'No': "//input[@id='rfc_subj_no']",	
         'Prepend': "//input[@id='rfc_subj_pre']",	
         'Append': "//input[@id='rfc_subj_app']"})	
UNSCANNABLE_RFCV_SUBJECT = (	
        'Unscannable RFC Violations Message Subject',	
        "//input[@id='rfc_subj_txt']")	
UNSCANNABLE_RFCV_ADD_CUSTOM_HEADER_RADIOGROUP = (	
        'Unscannable RFC Violations Add Custom Header',	
        {'Yes': "//input[@id='rfc_hdr_yes']",	
         'No': "//input[@id='rfc_hdr_no']"})	
UNSCANNABLE_RFCV_CUSTOM_HEADER_NAME = (	
        'Unscannable RFC Violations Custom Header Name',	
        "//input[@id='rfc__hdr_n']")	
UNSCANNABLE_RFCV_CUSTOM_HEADER_VALUE = (	
        'Unscannable RFC Violations Custom Header Value',	
        "//input[@id='rfc__hdr_t']")	
UNSCANNABLE_RFCV_MODIFY_RECIPIENT_RADIOGROUP = (	
        'Unscannable RFC Violations Modify Recipient',	
        {'Yes': "//input[@id='rfc_rbyes']",	
         'No': "//input[@id='rfc_rbno']"})	
UNSCANNABLE_RFCV_RECIPIENT_ADDRESS = (	
        'Unscannable RFC Violations Recipient Address',	
        "//input[@id='rfc_rbaddr']")	
UNSCANNABLE_RFCV_ALT_DESTINATION_RADIOGROUP = (	
        'Unscannable RFC Violations Send To Alternate Destination Host',	
        {'Yes': "//input[@id='rfc_altyes']",	
         'No': "//input[@id='rfc_altno']"})	
UNSCANNABLE_RFCV_ALT_DESTINATION_HOST = (	
        'Unscannable RFC Violations Alternate Destination Host',	
        "//input[@id='rfc_alttxt']")

class GlobalSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
	self.gui.click_button(UNSCANNABLE_DE_ADVANCED_ARROW, "don't wait")	
        self.gui.click_button(UNSCANNABLE_EF_ADVANCED_ARROW, "don't wait")	
        self.gui.click_button(UNSCANNABLE_RFCV_ADVANCED_ARROW, "don't wait")
        self._set_radio_groups(new_value,
                               SKIP_IF_IN_LIST_RADIOGROUP,
                               SCAN_METADATA_RADIOGROUP,
                               ASSUME_PATTERN_RADIOGROUP,
	                       ASSUME_ZIP_FILE_UNSCANNABLE_RADIOGROUP,
                               ACTION_DESCONSTR_RADIOGROUP,
	                               BYPASS_ALL_FILTERS_RADIOGROUP,	
                               CONVERT_OPAQUE_RADIOGROUP,	
                               SAFE_PRINT_DOC_QUALITY_RADIOGROUP,	
                               SAFE_PRINT_WATERMARK_RADIOGROUP,	
                               SAFE_PRINT_COVER_PAGE_RADIOGROUP,	
                               INBOUND_PWD_PROTECTED_ATTACHMENTS_DECRYPTION_RADIOGROUP,	
                               OUTBOUND_PWD_PROTECTED_ATTACHMENTS_DECRYPTION_RADIOGROUP,	
                               UNSCANNABLE_ENABLE_DE_ACTION_RADIOGROUP,	
                               UNSCANNABLE_DE_MODIFY_SUBJECT_RADIOGROUP,	
                               UNSCANNABLE_DE_ADD_CUSTOM_HEADER_RADIOGROUP,	
                               UNSCANNABLE_DE_MODIFY_RECIPIENT_RADIOGROUP,	
                               UNSCANNABLE_DE_ALT_DESTINATION_RADIOGROUP,	
                               UNSCANNABLE_ENABLE_EF_ACTION_RADIOGROUP,	
                               UNSCANNABLE_EF_MODIFY_SUBJECT_RADIOGROUP,	
                               UNSCANNABLE_EF_ADD_CUSTOM_HEADER_RADIOGROUP,	
                               UNSCANNABLE_EF_MODIFY_RECIPIENT_RADIOGROUP,	
                               UNSCANNABLE_EF_ALT_DESTINATION_RADIOGROUP,	
                               UNSCANNABLE_ENABLE_RFCV_ACTION_RADIOGROUP,	
                               UNSCANNABLE_RFCV_MODIFY_SUBJECT_RADIOGROUP,	
                               UNSCANNABLE_RFCV_ADD_CUSTOM_HEADER_RADIOGROUP,	
                               UNSCANNABLE_RFCV_MODIFY_RECIPIENT_RADIOGROUP,	
                               UNSCANNABLE_RFCV_ALT_DESTINATION_RADIOGROUP)
        self._set_edits(new_value,
                        MAX_DEPTH,
                        MAX_SIZE,
                        SCAN_TIMEOUT,
                        SAFE_PRINT_MAX_FILE_SIZE,
                        SAFE_PRINT_MAX_PAGE_COUNT,
	                SAFE_PRINT_CUSTOM_DOC_QUALITY,	
                        UNSCANNABLE_DE_SUBJECT,	
                        UNSCANNABLE_DE_CUSTOM_HEADER_NAME,	
                        UNSCANNABLE_DE_CUSTOM_HEADER_VALUE,	
                        UNSCANNABLE_DE_RECIPIENT_ADDRESS,	
                        UNSCANNABLE_DE_ALT_DESTINATION_HOST,	
                        UNSCANNABLE_EF_SUBJECT,	
                        UNSCANNABLE_EF_CUSTOM_HEADER_NAME,	
                        UNSCANNABLE_EF_CUSTOM_HEADER_VALUE,	
                        UNSCANNABLE_EF_RECIPIENT_ADDRESS,	
                        UNSCANNABLE_EF_ALT_DESTINATION_HOST,	
                        UNSCANNABLE_RFCV_SUBJECT,	
                        UNSCANNABLE_RFCV_CUSTOM_HEADER_NAME,	
                        UNSCANNABLE_RFCV_CUSTOM_HEADER_VALUE,	
                        UNSCANNABLE_RFCV_RECIPIENT_ADDRESS,	
                        UNSCANNABLE_RFCV_ALT_DESTINATION_HOST)
        self._set_combos(new_value,
                         ENCODING_COMBO,	
                         UNSCANNABLE_DE_ACTION_APPLY_COMBO,	
                         UNSCANNABLE_EF_ACTION_APPLY_COMBO,	
                         UNSCANNABLE_RFCV_ACTION_APPLY_COMBO)

        if 'File Type Selection' in new_value:
            self.gui.click_button(SAFE_PRINT_EXPAND_ALL_FILE_TYPES, "don't wait")
            if new_value['File Type Selection'].lower() not in ['select all', 'document', 'microsoft documents']:
                # First, unselect all the file types then iterate over each file
                # type provided by user and select respective checbox
                self.gui._select_unselect_checkbox("//input[@id='select_all']", False)
                file_types = new_value['File Type Selection'].lower().split(',')
                for file_type in file_types:
                    xpath = "//input[@id='%s']" % file_type
                    self.gui._select_unselect_checkbox(xpath, True)
            else:
                self._set_checkbox_groups(new_value, SAFE_PRINT_DEFAULT_FILE_TYPES)
