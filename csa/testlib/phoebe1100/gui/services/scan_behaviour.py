#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/services/scan_behaviour.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon, Wait
from common.gui.guiexceptions import ConfigError

from scan_behaviour_def.global_settings import GlobalSettings
from scan_behaviour_def.import_form import ImportForm, FILE_NAME_COMBO
from scan_behaviour_def.export_form import ExportForm, FILE_NAME

EDIT_SETTINGS_BUTTON = "//input[@value='Edit Global Settings...']"

IMPORT_BUTTON = "//input[@value='Import List...']"
EXPORT_BUTTON = "//input[@value='Export List...']"

ADD_MAPPING_BUTTON = "//input[@value='Add Mapping...']"
ATTACHMENT_TYPE = "//input[@id='attachment_type']"

HEADERS_MAP = {'Fingerprint / MIME': 1,
               'Type': 2}
MAPPINGS_TABLE = "//table[contains(@class, 'cols')]"
DATA_ROWS = "{0}//tr[td[contains(text(),'MIME Type') or contains(text(),'Fingerprint')]]".format(MAPPINGS_TABLE)
DATA_ROW_BY_IDX = lambda idx: "{0}[{1}]".format(DATA_ROWS, idx)
DATA_CELL_BY_ROW_COL = lambda row_idx, col_idx: "{0}/td[{1}]".format(
    DATA_ROW_BY_IDX(row_idx), col_idx)
TYPE_CELL_BY_NAME = lambda name: "{0}//td[normalize-space()='{1}']". \
    format(MAPPINGS_TABLE, name)
EDIT_LINK_BY_NAME = lambda name: "{0}//td[normalize-space()='{1}']" \
                                 "/following-sibling::td[1]/input". \
    format(MAPPINGS_TABLE, name)
DELETE_LINK_BY_NAME = lambda name: "{0}//td[normalize-space()='{1}']" \
                                   "/following-sibling::td[2]/img". \
    format(MAPPINGS_TABLE, name)

MAPPING_DIALOG = "//div[@id='mapping_dialog_c' and " \
                 "contains(@style, 'visibility: visible')]"
MAPPING_SUBMIT_BUTTON = "{0}//button[normalize-space()='Submit']".format(
    MAPPING_DIALOG)

CONFIRM_DIALOG = "//div[@id='confirmation_dialog_c' and " \
                 "contains(@style, 'visibility: visible')]"
CONTINUE_BUTTON = "{0}//button[last()]".format(CONFIRM_DIALOG)

PAGE_PATH = ('Security Services', 'Scan Behavior')


class ScanBehaviour(GuiCommon):
    def get_keyword_names(self):
        return ['scan_behaviour_edit_settings',

                'scan_behaviour_import_list',
                'scan_behaviour_export_list',

                'scan_behaviour_add_mapping',
                'scan_behaviour_edit_mapping',
                'scan_behaviour_delete_mapping',
                'scan_behaviour_is_mapping_exist',
                'scan_behaviour_get_all_mappings']

    def _get_cached_controller(self, cls):
        attr_name = '_{0}'.format(cls.__name__.lower())
        if not hasattr(self, attr_name):
            setattr(self, attr_name, cls(self))
        return getattr(self, attr_name)

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def scan_behaviour_edit_settings(self, settings):
        """Edit global scan behaviour settings

        *Parameters:*
        - `settings`: dictionary, whose items can be the following:
        | Action for attachments | Action for attachments with MIME
        types / fingerprints in table |
        | Maximum depth of attachment recursion | Maximum depth of
        attachment recursion to scan, number |
        | Maximum attachment size | Maximum attachment size to scan.
        You can add a trailing K or M to indicate size units |
        | Attachment Metadata scan | Either to scan ('Enabled')
        attachment metadata or not ('Disabled') |
        | Attachment scanning timeout | Attachment scanning timeout
        in seconds |
        | Assume attachment matches pattern | Assume attachment
        matches pattern if not scanned for any reason. Eiwther 'Yes'
        or 'No' |
        | Action when message cannot be deconstructed | Action
        when message cannot be deconstructed to remove specified
        attachments. Either 'Deliver', 'Bounce' or 'Drop' |
        | Encoding to use | Encoding to use when none is specified.
        Available encodings are: US-ASCII, Unicode (UTF-8),
        Unicode (UTF-16), Western European/Latin-1 (ISO 8859-1),
        Western European/Latin-1 (Windows CP1252), Traditional
        Chinese (Big 5), Simplified Chinese (GB 2312), Simplified
        Chinese (HZ GB 2312), Korean (ISO 2022-KR), Korean
        (KS-C-5601/EUC-KR), Japanese (Shift-JIS (X0123)),
        Japanese (ISO-2022-JP), Japanese (EUC) |
        | Convert opaque-signed messages | Convert opaque-signed
        messages to clear-signed (S/MIME unpacking). Either
        'Enabled' or 'Disabled' |

        *Exceptions:*
        - `ValueError`: if any of given options is not correct

        *Examples:*
        | ${new_settings}= | Create Dictionary |
        | ...  Action for attachments | Skip |
        | ...  Maximum depth of attachment recursion | 5 |
        | ...  Maximum attachment size | 5M |
        | ...  Attachment Metadata scan | Enabled |
        | ...  Attachment scanning timeout | 30 |
        | ...  Assume attachment matches pattern | No |
        | ...  Action when message cannot be deconstructed | Deliver |
        | ...  Encoding to use | US-ASCII |
        | ...  Convert opaque-signed messages | Disabled |
        | Scan Behaviour Edit Settings | ${new_settings} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        controller = self._get_cached_controller(GlobalSettings)
        controller.set(settings)
        self._click_submit_button()

    def _submit_import_export_changes(self):
        prev_timeout = self.set_selenium_timeout(5)
        try:
            self._click_submit_button()
        except Exception:
            self.click_button(CONTINUE_BUTTON)
            self._check_action_result()
        finally:
            self.set_selenium_timeout(prev_timeout)

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def scan_behaviour_import_list(self, filename):
        """Import mappings list from an existing file in
        configuration folder

        *Parameters:*
        - `filename`: name of the existing file in
        /data/pub/configuration folder on appliance

        *Examples:*
        | ${filename}= | Set Variable | mappings.txt |
        | Scan Behaviour Export List | ${filename} |
        | Scan Behaviour Import List | ${filename} |
        | ${is_my_mapping_exists}= | Scan Behaviour Is Mapping Exist | ${MY_TYPE} |
        | Should Be True | ${is_my_mapping_exists} |
        | Run On Dut | rm -f "/data/pub/configuration/${filename}" |
        """
        self.click_button(IMPORT_BUTTON)
        controller = self._get_cached_controller(ImportForm)
        controller.set({FILE_NAME_COMBO[0]: filename})
        self._submit_import_export_changes()

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def scan_behaviour_export_list(self, filename):
        """Export mappings list to a file in
        configuration folder

        *Parameters:*
        - `filename`: name of a file in
        /data/pub/configuration folder on appliance

        *Examples:*
        | ${filename}= | Set Variable | mappings.txt |
        | Scan Behaviour Export List | ${filename} |
        | Scan Behaviour Import List | ${filename} |
        | ${is_my_mapping_exists}= | Scan Behaviour Is Mapping Exist | ${MY_TYPE} |
        | Should Be True | ${is_my_mapping_exists} |
        | Run On Dut | rm -f "/data/pub/configuration/${filename}" |
        """
        self.click_button(EXPORT_BUTTON)
        controller = self._get_cached_controller(ExportForm)
        controller.set({FILE_NAME[0]: filename})
        self._submit_import_export_changes()

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def scan_behaviour_add_mapping(self, fg_mimetype):
        """Add a new mapping

        *Parameters:*
        - `fg_mimetype`: Fingerprint or MIME Type

        *Exceptions:*
        - `ConfigError`: if the same Fingerprint or MIME Type
        already defined

        *Examples:*
        | ${is_my_mapping_exists}= | Scan Behaviour Is Mapping Exist | ${MY_TYPE} |
        | Run Keyword If | not ${is_my_mapping_exists} |
        | ... | Scan Behaviour Add Mapping | ${MY_TYPE} |
        | ${is_my_mapping_exists}= | Scan Behaviour Is Mapping Exist | ${MY_TYPE} |
        | Should Be True | ${is_my_mapping_exists} |
        """
        if self._is_element_present(TYPE_CELL_BY_NAME(fg_mimetype)):
            raise ConfigError('Type "{0}" already exists'.format(fg_mimetype))
        self.click_button(ADD_MAPPING_BUTTON, 'don\'t wait')
        self.input_text(ATTACHMENT_TYPE, fg_mimetype)
        self.click_button(MAPPING_SUBMIT_BUTTON)
        self._check_action_result()

    @go_to_page(PAGE_PATH)
    def scan_behaviour_edit_mapping(self, old_fg_mimetype, new_fg_mimetype):
        """Edit an existing mapping

        *Parameters:*
        - `old_fg_mimetype`: existing Fingerprint or MIME Type
        - `new_fg_mimetype`: new Fingerprint or MIME Type

        *Exceptions:*
        - `ValueError`: if `old_fg_mimetype` does not exist in
        mappings list

        *Examples:*
        | Scan Behaviour Edit Mapping | png | bmp |
        """
        if not self._is_element_present(EDIT_LINK_BY_NAME(old_fg_mimetype)):
            raise ValueError('Type "{0}" does not exists'.format(old_fg_mimetype))
        self.click_button(EDIT_LINK_BY_NAME(old_fg_mimetype), 'don\'t wait')
        self.input_text(ATTACHMENT_TYPE, new_fg_mimetype)
        self.click_button(MAPPING_SUBMIT_BUTTON)
        self._check_action_result()

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def scan_behaviour_is_mapping_exist(self, fg_mimetype):
        """Check whether a mapping exists

        *Parameters:*
        - `fg_mimetype`: Fingerprint or MIME Type

        *Return:*
        - ${True} or ${False}

        *Examples:*
        | ${is_my_mapping_exists}= | Scan Behaviour Is Mapping Exist | ${MY_TYPE} |
        | Run Keyword If | not ${is_my_mapping_exists} |
        | ... | Scan Behaviour Add Mapping | ${MY_TYPE} |
        """
        return self._is_element_present(TYPE_CELL_BY_NAME(fg_mimetype))

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def scan_behaviour_delete_mapping(self, fg_mimetype):
        """Delete an existing mapping

        *Parameters:*
        - `fg_mimetype`: existing Fingerprint or MIME Type

        *Exceptions:*
        - `ValueError`: if `fg_mimetype` does not exist in
        mappings list

        *Examples:*
        | Scan Behaviour Delete Mapping | ${MY_TYPE} |
        | ${is_my_mapping_exists}= | Scan Behaviour Is Mapping Exist | ${MY_TYPE} |
        | Should Not Be True  ${is_my_mapping_exists} |
        """
        if not self._is_element_present(DELETE_LINK_BY_NAME(fg_mimetype)):
            raise ValueError('Type "{0}" does not exist'.format(fg_mimetype))
        self.click_button(DELETE_LINK_BY_NAME(fg_mimetype), 'don\'t wait')
        Wait(until=self._is_element_present,
             msg='Failed to wait until confirmation dialog appears',
             timeout=15).wait(CONTINUE_BUTTON)
        self.click_button(CONTINUE_BUTTON)
        self._check_action_result()

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def scan_behaviour_get_all_mappings(self):
        """Get all existing mappings

        *Return:*
        - List of dictionaries. Each dictionary has the following items:

        | Fingerprint / MIME | Description of current type.
        Either 'Fingerprint' or 'MIME Type' |
        | Type | type name |

        *Examples:*
        | @{all_mappings}= | Scan Behaviour Get All Mappings |
        | Log List | ${all_mappings} |
        | ${is_my_mapping_found}= | Set Variable | ${False} |
        | :FOR | ${info_dict} | IN | @{all_mappings} |
        | \ | ${type}= | Get From Dictionary | ${info_dict}  Type |
        | \ | ${is_my_mapping_found}= | Set Variable If | '${type}' == '${MY_TYPE}' |
        | \ | ... | ${True} | ${False} |
        | \ | Run Keyword If | ${is_my_mapping_found} | Exit For Loop |
        | Should Be True | ${is_my_mapping_found} |
        """
        mappings_count = int(self.get_matching_xpath_count(DATA_ROWS))
        print mappings_count
        result = []
        for row_idx in xrange(1, 1 + mappings_count):
            print row_idx
            info = {}
            for col_name, col_idx in HEADERS_MAP.iteritems():
                print col_name
                print col_idx
                info[col_name] = self.get_text(DATA_CELL_BY_ROW_COL(row_idx,
                                                                    col_idx))
            result.append(info)
        return result
