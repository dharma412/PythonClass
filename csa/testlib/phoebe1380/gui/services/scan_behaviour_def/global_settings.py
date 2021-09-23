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
ACTION_DESCONSTR_RADIOGROUP = ('Action when message cannot be deconstructed',
                               {'Deliver': "//input[@id='mimeparse_fail_action_deliver']",
                                'Bounce': "//input[@id='mimeparse_fail_action_bounce']",
                                'Drop': "//input[@id='mimeparse_fail_action_drop']"})
ENCODING_COMBO = ('Encoding to use',
                  "//select[@name='default_text_encoding']")
CONVERT_OPAQUE_RADIOGROUP = ('Convert opaque-signed messages',
                             {'Enabled': "//input[@id='smime_unpack_enabled']",
                              'Disabled': "//input[@id='smime_unpack_disabled']"})

SAFE_PRINT_MAX_FILE_SIZE = ('Maximum File Size', "//input[@name='sp_max_doc_size']")
SAFE_PRINT_MAX_PAGE_COUNT = ('Maximum Page Count', "//input[@name='sp_max_page_count']")
SAFE_PRINT_DOC_QUALITY = ('Document Quality', "//input[@name='sp_doc_quality']")
SAFE_PRINT_DEFAULT_FILE_TYPES = ('File Type Selection',
                                    { 'Select All': "//input[@id='select_all']",
                                      'Document': "//input[@id='Document']",
                                      'Microsoft Documents': "//input[@id='Microsoft Documents']"})

SAFE_PRINT_EXPAND_ALL_FILE_TYPES = "//a[@class='expandAll']"
SAFE_PRINT_COLLAPSE_ALL_FILE_TYPES = "//a[@class='collapseAll']"
# Reset operation is yet to be implemented
# Reset button does not work with Firefox v3
SAFE_PRINT_RESET_FILE_TYPES = "//input[@id='reset']"


class GlobalSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_radio_groups(new_value,
                               SKIP_IF_IN_LIST_RADIOGROUP,
                               SCAN_METADATA_RADIOGROUP,
                               ASSUME_PATTERN_RADIOGROUP,
                               ACTION_DESCONSTR_RADIOGROUP,
                               CONVERT_OPAQUE_RADIOGROUP)
        self._set_edits(new_value,
                        MAX_DEPTH,
                        MAX_SIZE,
                        SCAN_TIMEOUT,
                        SAFE_PRINT_MAX_FILE_SIZE,
                        SAFE_PRINT_MAX_PAGE_COUNT,
                        SAFE_PRINT_DOC_QUALITY)
        self._set_combos(new_value,
                         ENCODING_COMBO)

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
