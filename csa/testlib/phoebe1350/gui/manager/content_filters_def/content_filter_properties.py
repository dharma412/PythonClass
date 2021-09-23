#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/content_filters_def/content_filter_properties.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

import inspect
import sys

from utils import parse_value,get_language_code


MESSAGE_LANGUAGE_RESULT_OP = ('english',
                       'german',
                       'spanish',
                       'french',
                       'italian',
                       'japanese',
                       'korean',
                       'portuguese',
                       'russian',
                       'chinese',
                       'taiwanese',
                       'undetermined')

NUMBER_COMPARISON_OP = ('Greater than',
                     'Greater than or equal to',
                     'Less than',
                     'Less than or equal to',
                     'Equal to',
                     'Does not equal')
STRING_COMPARISON_OP = ('Contains',
                     'Does Not Contain',
                     'Equals',
                     'Does Not Equal',
                     'Begins with',
                     'Does Not Begin With',
                     'Ends With',
                     'Does Not End With')
IS_NOT_COMPARISON_OP = ('Is', 'Is not')
FILETYPE = ('Compressed',
                '-- ace', '-- arc', '-- arj', '-- binhex', '-- bz',
                '-- bz2', '-- cab', '-- gzip', '-- lha', '-- rar', '-- sit',
                '-- tar', '-- unix', '-- x-windows-packager', '-- zip', '-- zoo',
            'Documents',
                '-- doc, docx', '-- mdb', '-- mpp', '-- ole', '-- pdf',
                '-- ppt, pptx', '-- pub', '-- rtf', '-- wps', '-- x-wmf',
                '-- xls, xlsx',
            'Executables',
                '-- exe', '-- java', '-- msi', '-- pif',
            'Images',
                '-- bmp', '-- cur', '-- gif', '-- ico', '-- jpeg', '-- pcx',
                '-- png', '-- psd', '-- psp', '-- tga', '-- tiff', '-- x-pict2',
            'Media',
                '-- aac', '-- aiff', '-- asf', '-- avi', '-- flash', '-- midi',
                '-- mov', '-- mp3', '-- mpeg', '-- ogg', '-- ram', '-- snd',
                '-- wav', '-- wma', '-- wmv',
            'Text',
                '-- html', '-- txt', '-- xml')
AUTH_RESULT_OP = ('Pass',
                  'Neutral (message not signed)',
                  'Temperror (recoverable error occurred)',
                  'Permerror (unrecoverable error occurred)',
                  'Hardfail (authentication tests failed)',
                  'None (authentication not performed)')
VERIFICATION_RESULT_OP = ('None',
                          'Pass',
                          'Neutral',
                          'SoftFail',
                          'Fail',
                          'TempError',
                          'PermError')
FILENAME_COMPARISON_OP = ('contains', 'is', 'begins with', 'ends with')
IIA_VEDICT_RESULTS = ('Inappropriate',
                      'Suspect or Inappropriate',
                      'Suspect',
                      'Unscannable',
                      'Clean')


def handle_option_not_found_event(option_name, property_name, docstring=''):
    if docstring:
        print 'Unknown key name is given for "%s" property:'\
              ' "%s".\nPlease use only dictionary items declared'\
              ' in property documentation:\n%s' % (option_name,
                                                   property_name,
                                                   docstring)
    raise ValueError('Unknown key name is given for "%s" property:'\
                     ' "%s"' % (option_name, property_name))


class ContentFilterProperty(object):
    """Base class for all content filter properties
    """

    def __init__(self, gui_common):
        """
        *Parameters:*
        - `gui_common`: instance of GuiCommon class
        """
        self.gui = gui_common

    @classmethod
    def get_name(cls):
        """
        *Return:*
        Property name
        """
        raise NotImplementedError('Should be implemented in subclasses')

    def set(self, new_value):
        """Set new_value in Selenium GUI to property

        *Parameters:*
        - `new_value`: new value to be set by Selenium
        """
        raise NotImplementedError('Should be implemented in subclasses')

    def get(self):
        """Get value from Selenium GUI

        *Return:*
        Property value got by Selenium
        """
        raise NotImplementedError('Should be implemented in subclasses')


def get_property_class_by_name(property_name):
    """Return property class by its name

    *Parameters:*
    - `property_name`: property name. Should equal to one of values
    returned by get_name() static method within classes declared inside
    this module

    *Exceptions:*
    - `ValueError`: if no class is found for property with given name

    *Return:*
    Property class. Property is subclass of ContentFilterProperty
    """
    base_class = ContentFilterProperty
    all_subclasses = [v for k, v in inspect.getmembers(sys.modules[__name__]) \
                      if inspect.isclass(v) and issubclass(v, base_class) and \
                         v != base_class]
    searched_class = filter(lambda x: x.get_name() == property_name,
                            all_subclasses)
    if searched_class:
        return searched_class[0]
    else:
        raise ValueError('There is no class for property named "%s"' % (property_name,))


class MessageBodyOrAttachmentProperty(ContentFilterProperty):
    CONTAINS_TEXT_RADIO = "//input[@id='MessageBodyOrAttachment_radio_match_text']"
    CONTAINS_TEXT_EDIT = "//input[@id='MessageBodyOrAttachment_match_text']"

    CONTAINS_SMART_IDENTIFIER_RADIO = "//input[@id='MessageBodyOrAttachment_radio_smart_id']"
    CONTAINS_SMART_IDENTIFIER_COMBO = "//select[@id='MessageBodyOrAttachment_smart_id']"

    CONTAINS_ITEM_RADIO = "//input[@id='MessageBodyOrAttachment_radio_content_dict']"
    CAINTAINS_ITEM_DICT_COMBO = "//select[@id='MessageBodyOrAttachment_content_dict']"

    NUMBER_OF_MATCHES = "//input[@id='MessageBodyOrAttachment_threshold']"

    @classmethod
    def get_name(cls):
        return 'Message Body or Attachment'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: Whether the message body or attachment contain text that
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
        """
        for key, value in new_value.items():
            if key == 'Contains text':
                self.gui._click_radio_button(self.CONTAINS_TEXT_RADIO)
                self.gui.input_text(self.CONTAINS_TEXT_EDIT, value)
            elif key == 'Contains smart identifier':
                self.gui._click_radio_button(self.CONTAINS_SMART_IDENTIFIER_RADIO)
                self.gui.select_from_list(self.CONTAINS_SMART_IDENTIFIER_COMBO,
                                          value)
            elif key == 'Contains term in content dictionary':
                self.gui._click_radio_button(self.CONTAINS_ITEM_RADIO)
                self.gui.select_from_list(self.CAINTAINS_ITEM_DICT_COMBO,
                                          value)
            elif key == 'Number of matches required':
                self.gui.input_text(self.NUMBER_OF_MATCHES, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class MessageBodyProperty(ContentFilterProperty):
    CONTAINS_TEXT_RADIO = "//input[@id='OnlyMessageBody_radio_match_text']"
    CONTAINS_TEXT_EDIT = "//input[@id='OnlyMessageBody_match_text']"

    CONTAINS_SMART_IDENTIFIER_RADIO = "//input[@id='OnlyMessageBody_radio_smart_id']"
    CONTAINS_SMART_IDENTIFIER_COMBO = "//select[@id='OnlyMessageBody_smart_id']"

    CONTAINS_ITEM_RADIO = "//input[@id='OnlyMessageBody_radio_content_dict']"
    CAINTAINS_ITEM_DICT_COMBO = "//select[@id='OnlyMessageBody_content_dict']"

    NUMBER_OF_MATCHES = "//input[@id='OnlyMessageBody_threshold']"

    @classmethod
    def get_name(cls):
        return 'Message Body'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the message body contain text matching a
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
        """
        for key, value in new_value.items():
            if key == 'Contains text':
                self.gui._click_radio_button(self.CONTAINS_TEXT_RADIO)
                self.gui.input_text(self.CONTAINS_TEXT_EDIT, value)
            elif key == 'Contains smart identifier':
                self.gui._click_radio_button(self.CONTAINS_SMART_IDENTIFIER_RADIO)
                self.gui.select_from_list(self.CONTAINS_SMART_IDENTIFIER_COMBO,
                                          value)
            elif key == 'Contains term in content dictionary':
                self.gui._click_radio_button(self.CONTAINS_ITEM_RADIO)
                self.gui.select_from_list(self.CAINTAINS_ITEM_DICT_COMBO,
                                          value)
            elif key == 'Number of matches required':
                self.gui.input_text(self.NUMBER_OF_MATCHES, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class URLCategoryConditionProperty(ContentFilterProperty):
    AVAILABLE_CATEGORIES_COMBO = "//select[@id='UrlCategoryCondition_condition_categories_available_condition_categories']"
    ADD_BUTTON = "//input[@value='Add >']"

    SELECTED_CATEGORIES_COMBO = "//select[@id='UrlCategoryCondition_condition_categories_chosen_condition_categories']"
    REMOVE_BUTTON = "//input[@value='< Remove']"

    URL_WHITELIST_COMBO = "//select[@id='UrlCategoryCondition_url_whitelist']"
    INCLUDE_ATTACHMENTS = "//input[@id='UrlCategoryCondition_include_attachments']"

    @classmethod
    def get_name(cls):
        return 'URL Category Condition'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: Does any URL in the message body belong to one of the selected categories
        Dictionary can contain the next items:
        | Add Categories | <value> |
        <value> contains list of URL Categories to be added
        or
        | Remove Categories | <value> |
        <value> contains list of URL Categories to be removed
        or
        | Use a URL whitelist | <value> |
        <value> contains url whitelist value
        *Examples:*
        | ${urls} | Create List | Arts | Adult |
        | ${new_value1} | Create Dictionary | Add Categories | ${urls} |
        | ... |  Use a URL whitelist | urllist2 |
        | ${conditions} | Content Filter Create Conditions |
        | ... | URL Category Condition | ${new_value1} |
        | ... |  Include Attachments | Yes |
        """
        for key, value in new_value.items():
            if key == 'Add Categories':
                for list in value:
                    self.gui.select_from_list(self.AVAILABLE_CATEGORIES_COMBO,list)
                self.gui.click_button(self.ADD_BUTTON, "don't wait")
            elif key == 'Remove Categories':
                for list in value:
                    self.gui.select_from_list(self.SELECTED_CATEGORIES_COMBO,list)
                self.gui.click_button(self.REMOVE_BUTTON, "don't wait")
            elif key == 'Use a URL whitelist':
                self.gui.select_from_list(self.URL_WHITELIST_COMBO,value)
            elif key == 'Include Attachments':
                if value.lower() == 'yes':
                    self.gui._select_checkbox(self.INCLUDE_ATTACHMENTS)
                else:
                    self.gui._unselect_checkbox(self.INCLUDE_ATTACHMENTS)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))

class URLReputationConditionProperty(ContentFilterProperty):

    URL_REP_WBRS = "//input[@id='UrlReputationCondition_url_reputation_rule_wbrs']"
    URL_REP_EXTERNAL_THREAT_FEEDS = "//input[@id='UrlReputationCondition_url_reputation_rule_tf_source']"

    URL_WHITELIST_REPUTATION_COMBO = "//select[@id='UrlReputationCondition_url_whitelist']"

    MALICIOUS_RADIO = "//input[@id='UrlReputationCondition_url_reputation_Malicious']"
    NEUTRAL_RADIO = "//input[@id='UrlReputationCondition_url_reputation_Neutral']"
    CLEAN_RADIO = "//input[@id='UrlReputationCondition_url_reputation_Clean']"
    CUSTOMRANGE_RADIO = "//input[@id='UrlReputationCondition_url_reputation_Custom']"
    NOSCORE_RADIO = "//input[@id='UrlReputationCondition_url_reputation_No Score']"

    CUSTOMRANGE_MIN_EDIT = "//input[@id='UrlReputationCondition_min_score']"
    CUSTOMRANGE_MAX_EDIT = "//input[@id='UrlReputationCondition_max_score']"

    AVAILABLE_SOURCE_COMBO = "//select[@id='UrlReputationCondition_tf_source_name_available_tf_source_name']"
    SOURCE_ADD_BUTTON = "//input[@value='Add >' and contains(@onclick, 'UrlReputationCondition_tf_source_name_available_tf_source_name')]"

    SELECTED_SOURCE_COMBO = "//select[@id='UrlReputationCondition_tf_source_name_chosen_tf_source_nam']"
    SOURCE_REMOVE_BUTTON = "//input[@value='< Remove' and contains(@onclick, 'UrlReputationCondition_tf_source_name_chosen_tf_source_name')]"

    MESSAGE_BODY_SUBJECT = "//input[@id='UrlReputationCondition_check_url_within_message_body']"
    ONLY_ATTACHMENTS = "//input[@id='UrlReputationCondition_check_url_within_attachments']"
    MSG_BDY_ATTACHMENTS = "//input[@id='UrlReputationCondition_check_url_within_include_all']"

    @classmethod
    def get_name(cls):
        return 'URL Reputation Condition'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: This rule evaluates URL's using their Web Based Reputation Score (WBRS)
        Dictionary can contain the next items:
        | URL Reputation Type | URL Reputation Wbrs |
        | URL Reputation Type | URL Reputation External Threat Feeds |
        | Use a URL Reputation whitelist | <value> |
        <value> contains url whitelist value
        or
        | Malicious Reputation URL |
        or
        | Suspect Reputation URL |
        or
        | Clean Reputation URL |
        or
        | NoScore Reputation URL |
        or
        | CustomRange Reputation URL Min value | <value> |
        <value> contains the min CustomRange value
        or
        | CustomRange Reputation URL Max value | <value> |
        <value> contains the max CustomRange value
        *Examples:*
        | ${new_value} | Create Dictionary |
        | ... |  Use a URL Reputation whitelist | webreputation |
        | ... |  Suspect Reputation URL | None |
        | ... |  Scan Type | All |
        | ${actions} | Content Filter Create Conditions |
        | ... | URL Reputation Condition | ${new_value} |
        | Add Sources | <value> |
        <value> contains list of Threat feed sources to be added
        or
        | Remove Sources | <value> |
        <value> contains list of Threat feed sourcesto be removed
        """

        for key, value in new_value.items():
            if  key.lower() == 'url reputation type':
                if value.lower() == 'url reputation wbrs':
                    self.gui._click_radio_button(self.URL_REP_WBRS)
                elif value.lower() == 'url reputation external threat feeds':
                    self.gui._click_radio_button(self.URL_REP_EXTERNAL_THREAT_FEEDS)
            elif key.lower() == 'use a url reputation whitelist':
                self.gui.select_from_list(self.URL_WHITELIST_REPUTATION_COMBO,value)
            elif key.lower() == 'malicious reputation url':
                self.gui._click_radio_button(self.MALICIOUS_RADIO)
            elif key.lower() == 'suspect reputation url':
                self.gui._click_radio_button(self.NEUTRAL_RADIO)
            elif key.lower() == 'clean reputation url':
                self.gui._click_radio_button(self.CLEAN_RADIO)
            elif key.lower() == 'noscore reputation url':
                self.gui._click_radio_button(self.NOSCORE_RADIO)
            elif key.lower() == 'customrange reputation url min value':
                self.gui._click_radio_button(self.CUSTOMRANGE_RADIO)
                self.gui.input_text(self.CUSTOMRANGE_MIN_EDIT,value)
            elif key.lower() == 'customrange reputation url max value':
                self.gui._click_radio_button(self.CUSTOMRANGE_RADIO)
                self.gui.input_text(self.CUSTOMRANGE_MAX_EDIT,value)
            elif key.lower() == 'scan type':
                if value.lower() == 'message body and subject':
                    self.gui._click_radio_button(self.MESSAGE_BODY_SUBJECT)
                elif value.lower() == 'only attachments':
                    self.gui._click_radio_button(self.ONLY_ATTACHMENTS)
                elif value.lower() == 'all':
                    self.gui._click_radio_button(self.MSG_BDY_ATTACHMENTS)
            elif key.lower() == 'add sources':
                for list in value:
                    self.gui.select_from_list(self.AVAILABLE_SOURCE_COMBO,list)
                self.gui.click_button(self.SOURCE_ADD_BUTTON, "don't wait")
            elif key.lower() == 'remove sources':
                for list in value:
                    self.gui.select_from_list(self.SELECTED_SOURCE_COMBO,list)
                self.gui.click_button(self.SOURCE_REMOVE_BUTTON, "don't wait")
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))

class MessageSizeProperty(ContentFilterProperty):
    MESSAGE_COMBO = "//select[@id='MessageSize_operator']"
    MESSAGE_SIZE_EDIT = "//input[@id='MessageSize_message_size']"

    @classmethod
    def get_name(cls):
        return 'Message Size'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the message size is within a specified range.
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
        """
        for key, value in new_value.items():
            if key == 'Message size is':
                operator_value = parse_value(value, NUMBER_COMPARISON_OP)
                self.gui.select_from_list(self.MESSAGE_COMBO,
                                          operator_value)
                message_size = parse_value(value, r'(\d+)', True)
                self.gui.input_text(self.MESSAGE_SIZE_EDIT, message_size)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))

class MacroDetectionConditionProperty(ContentFilterProperty):
    AVAILABLE_FILE_TYPES = "//select[@id='Macro_Detection_Rule_macro_file_type_available_macro_file_type']"
    ADD_BUTTON = "xpath=(//input[@value='Add >'])[2]"

    SELECTED_FILE_TYPES = "//select[@id='Macro_Detection_Rule_macro_file_type_chosen_macro_file_type']"
    REMOVE_BUTTON = "xpath=(//input[@value='< Remove'])[2]"

    @classmethod
    def get_name(cls):
        return 'Macro Detection'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: Dictionary to identify macros embedded in email attachments.
                       Dictionary can contain the following items:
            | Add Macros | <value> |
            <value> can contain one or multiple type(s) from available Macros: OFFICE, OLE, PDF
            | Remove Macros | <value> |
            <value> can contain list of Macros to be removed which were selected previously.
        *Examples:*
            | ${macros} | Create List | OFFICE | PDF |
            | ${macro_dict} | Create Dictionary | Add Macros | ${macros} |
            | ${conditions} | Content Filter Create Conditions |
            | ... | Macro Detection | ${macro_dict} |
        """

        for key, value in new_value.items():
            if key == 'Add Macros':
                for list in value:
                    self.gui.select_from_list(self.AVAILABLE_FILE_TYPES,list)
                self.gui.click_button(self.ADD_BUTTON, "don't wait")
            elif key == 'Remove Macros':
                for list in value:
                    self.gui.select_from_list(self.SELECTED_FILE_TYPES,list)
                self.gui.click_button(self.REMOVE_BUTTON, "don't wait")
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class StripAttachmentWithMacroProperty(ContentFilterProperty):
    AVAILABLE_FILE_TYPES = "//select[@id='StripAttachmentWithMacro_md_action_file_types_available_md_action_file_types']"
    ADD_BUTTON = "xpath=(//input[@value='Add >'])[3]"

    SELECTED_FILE_TYPES = "//select[@id='StripAttachmentWithMacro_md_action_file_types_chosen_md_action_file_types']"
    REMOVE_BUTTON = "xpath=(//input[@value='< Remove'])[3]"

    REPLACEMENT_MESSAGE = "//textarea[@id='StripAttachmentWithMacro_replace_message']"

    @classmethod
    def get_name(cls):
        return 'Strip Attachment With Macro'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: Dictionary to identify macros embedded in email attachments.
                       Dictionary can contain the following items:
            | Add Macros | <value> |
            <value> can contain one or multiple type(s) from available Macros: OFFICE, OLE, PDF
            | Remove Macros | <value> |
            <value> can contain list of Macros to be removed which were selected previously.
            | Replacement Message | Custom Replacement Message (Optional) |
        *Examples:*
            | ${macros} | Create List | OFFICE | PDF |
            | ${macro_dict} | Create Dictionary |
            | ... | Add Macros | ${macros} |
            | ... | Replacement Message | Attachment stripped by Macro Detection |
            | ${actions} | Content Filter Create Actions |
            | ... | Strip Attachment With Macro | ${macro_dict} |
        """

        for key, value in new_value.items():
            if key == 'Add Macros':
                for list in value:
                    self.gui.select_from_list(self.AVAILABLE_FILE_TYPES,list)
                self.gui.click_button(self.ADD_BUTTON, "don't wait")
            elif key == 'Remove Macros':
                for list in value:
                    self.gui.select_from_list(self.SELECTED_FILE_TYPES,list)
                self.gui.click_button(self.REMOVE_BUTTON, "don't wait")
            elif key == 'Replacement Message':
                self.gui.input_text(self.REPLACEMENT_MESSAGE, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))

class AttachmentContentProperty(ContentFilterProperty):
    CONTAINS_TEXT_RADIO = "//input[@id='AttachmentContent_radio_match_text']"
    CONTAINS_TEXT_EDIT = "//input[@id='AttachmentContent_match_text']"

    CONTAINS_SMART_IDENTIFIER_RADIO = "//input[@id='AttachmentContent_radio_smart_id']"
    CONTAINS_SMART_IDENTIFIER_COMBO = "//select[@id='AttachmentContent_smart_id']"

    CONTAINS_ITEM_RADIO = "//input[@id='AttachmentContent_radio_content_dict']"
    CAINTAINS_ITEM_DICT_COMBO = "//select[@id='AttachmentContent_content_dict']"

    NUMBER_OF_MATCHES = "//input[@id='AttachmentContent_threshold']"

    @classmethod
    def get_name(cls):
        return 'Attachment Content'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the message contains an attachment that
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
        """
        for key, value in new_value.items():
            if key == 'Contains text':
                self.gui._click_radio_button(self.CONTAINS_TEXT_RADIO)
                self.gui.input_text(self.CONTAINS_TEXT_EDIT, value)
            elif key == 'Contains smart identifier':
                self.gui._click_radio_button(self.CONTAINS_SMART_IDENTIFIER_RADIO)
                self.gui.select_from_list(self.CONTAINS_SMART_IDENTIFIER_COMBO,
                                          value)
            elif key == 'Contains term in content dictionary':
                self.gui._click_radio_button(self.CONTAINS_ITEM_RADIO)
                self.gui.select_from_list(self.CAINTAINS_ITEM_DICT_COMBO,
                                          value)
            elif key == 'Number of matches required':
                self.gui.input_text(self.NUMBER_OF_MATCHES, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class AttachmentFileInfoProperty(ContentFilterProperty):
    FILENAME_CONTAINS_RADIO = "//input[@id='AttachmentFileInfo_radio_filename']"
    FILENAME_CONTAINS_COMBO = "//select[@id='AttachmentFileInfo_filename_op']"
    FILENAME_CONTAINS_EDIT = "//input[@id='AttachmentFileInfo_filename']"

    FILENAME_CONTAINS_TERM_RADIO = \
                    "//input[@id='AttachmentFileInfo_radio_content_dict']"
    FILENAME_CONTAINS_TERM_COMBO = \
                        "//select[@id='AttachmentFileInfo_content_dict']"

    FILETYPE_RADIO = "//input[@id='AttachmentFileInfo_radio_filetype']"
    FILETYPE_OP_COMBO = "//select[@id='AttachmentFileInfo_filetype_op']"
    FILETYPE_COMBO = "//select[@id='AttachmentFileInfo_filetype']"

    MIMETYPE_RADIO = "//input[@id='AttachmentFileInfo_radio_mimetype']"
    MIMETYPE_OP_COMBO = "//select[@id='AttachmentFileInfo_mimetype_op']"
    MIMETYPE_EDIT = "//input[@id='AttachmentFileInfo_mimetype']"

    ETF_RADIO="//input[@id='AttachmentFileInfo_radio_etf']"
    ETF_AVAILABLE_CATEGORIES_COMBO = "//select[@id='AttachmentFileInfo_etf_list_available_etf_list']"
    ETF_SELECTED_CATEGORIES_COMBO = "//select[@id='AttachmentFileInfo_etf_list_chosen_etf_list']"
    ETF_ADD_BUTTON = "//input[@value='Add >' and contains(@onclick, 'AttachmentFileInfo_etf_list_available_etf_list')]"
    ETF_REMOVE_BUTTON = "//input[@value='< Remove' and contains(@onclick, 'AttachmentFileInfo_etf_list_chosen_etf_list')]"
    ETF_FILEHASH_EXCEPTION_COMBO = "//select[@id='AttachmentFileInfo_etf_filehash']"

    IIA_VERDICT_RADIO = "//input[@id='AttachmentFileInfo_radio_imageverdict']"
    IIA_VERDICT_OP_COMBO = "//select[@id='AttachmentFileInfo_imageverdict_op']"
    IIA_VERDICT_RESULT_COMBO = "//select[@id='AttachmentFileInfo_imageverdict']"

    ATTACHMENT_IS_CORRUPT_RADIO = "//input[@id='AttachmentFileInfo_radio_corrupt']"

    @classmethod
    def get_name(cls):
        return 'Attachment File Info'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the message contains an attachment of a filetype
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
        or
        | Attachment is corrupt | <value is ignored> |


        *Examples:*
        | ${new_value}= | Create Dictionary | File type is |
        | ... | Is not compressed |
        """
        for key, value in new_value.iteritems():
            if key == 'Filename':
                self.gui._click_radio_button(self.FILENAME_CONTAINS_RADIO)
                comparison_operator = parse_value(value,
                                                  STRING_COMPARISON_OP)
                self.gui.select_from_list(self.FILENAME_CONTAINS_COMBO,
                                          comparison_operator)
                filename_part = value[len(comparison_operator) + 1:]
                self.gui.input_text(self.FILENAME_CONTAINS_EDIT, filename_part)
            elif key == 'Filename contains term in content dictionary':
                self.gui._click_radio_button(self.FILENAME_CONTAINS_TERM_RADIO)
                self.gui.select_from_list(self.FILENAME_CONTAINS_TERM_COMBO,
                                          value)
            elif key == 'File type is':
                self.gui._click_radio_button(self.FILETYPE_RADIO)
                comparison_operator = parse_value(value,
                                                  IS_NOT_COMPARISON_OP)
                self.gui.select_from_list(self.FILETYPE_OP_COMBO,
                                          comparison_operator)
                filetype = parse_value(value, FILETYPE)
                self.gui.select_from_list(self.FILETYPE_COMBO,
                                          filetype)
            elif key == 'MIME type is':
                self.gui._click_radio_button(self.MIMETYPE_RADIO)
                comparison_operator = parse_value(value,
                                                  IS_NOT_COMPARISON_OP)
                self.gui.select_from_list(self.MIMETYPE_OP_COMBO,
                                          comparison_operator)
                mimetype = value[len(comparison_operator) + 1:]
                self.gui.input_text(self.MIMETYPE_EDIT, mimetype)
            elif key == 'Image Analysis Verdict':
                self.gui._click_radio_button(self.IIA_VERDICT_RADIO)
                comparison_operator = parse_value(value,
                                                  IS_NOT_COMPARISON_OP)
                self.gui.select_from_list(self.IIA_VERDICT_OP_COMBO,
                                          comparison_operator)
                result_part = parse_value(value, IIA_VEDICT_RESULTS)
                self.gui.select_from_list(self.IIA_VERDICT_RESULT_COMBO,
                                          result_part)

            elif key.lower() == 'external threat feeds':
                self.gui._click_radio_button(self.ETF_RADIO)
                for k,v in value.iteritems():
                    if k.lower()== 'etf add categories':
                        for list in v:
                            self.gui.select_from_list(self.ETF_AVAILABLE_CATEGORIES_COMBO,list)
                        self.gui.click_button(self.ETF_ADD_BUTTON, "don't wait")
                    elif k.lower() == 'etf remove categories':
                        for list in v:
                            self.gui.select_from_list(self.ETF_SELECTED_CATEGORIES_COMBO,list)
                        self.gui.click_button(self.ETF_REMOVE_BUTTON, "don't wait")
                    elif key.lower() == 'use a file hash exception list':
                        self.gui.select_from_list(self.ETF_FILEHASH_EXCEPTION_COMBO,value)

            elif key == 'Attachment is Corrupt':
                self.gui._click_radio_button(self.ATTACHMENT_IS_CORRUPT_RADIO)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class AttachmentProtectionProperty(ContentFilterProperty):
    ATTACHMENT_PROTECTED_RADIO = "//input[@id='AttachmentProtected_radio_protected']"
    ATTACHMENT_NOT_PROTECTED_RADIO = "//input[@id='AttachmentProtected_radio_unprotected']"

    @classmethod
    def get_name(cls):
        return 'Attachment Protection'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the message contains a password-protected or encrypted
        attachment.
        Dictionary can contain the next items:
        | Attachment Protection | <value> |
        <value> be one of these values:
        | One or more attachments are protected |
        | One or more attachments are not protected |

        *Examples:*
        | ${new_value}= | Create Dictionary | Attachment Protection |
        | ... | One or more attachments are protected |
        """
        for key, value in new_value.items():
            if key == 'Attachment Protection':
                if value == 'One or more attachments are protected':
                    self.gui._click_radio_button(self.ATTACHMENT_PROTECTED_RADIO)
                elif value == 'One or more attachments are not protected':
                    self.gui._click_radio_button(self.ATTACHMENT_NOT_PROTECTED_RADIO)
                else:
                    raise ValueError('Unknown value "%s" is given for "%s" property' % \
                                     (value, self.get_name()))
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SubjectHeaderProperty(ContentFilterProperty):
    SUBJECT_HEADER_RADIO = "//input[@id='SubjectHeader_radio_match_text']"
    SUBJECT_HEADER_CONTAINS_OP = "//select[@id='SubjectHeader_operator']"
    SUBJECT_HEADER_EDIT = "//input[@id='SubjectHeader_match_text']"

    CONTAINS_ITEM_RADIO = "//input[@id='SubjectHeader_radio_content_dict']"
    DICT_COMBO = "//select[@id='SubjectHeader_content_dict']"

    @classmethod
    def get_name(cls):
        return 'Subject Header'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the subject header contains
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
        """
        for key, value in new_value.items():
            if key == 'Subject Header':
                self.gui._click_radio_button(self.SUBJECT_HEADER_RADIO)
                comparison_op = parse_value(value, STRING_COMPARISON_OP)
                self.gui.select_from_list(self.SUBJECT_HEADER_CONTAINS_OP,
                                      comparison_op)
                header = value[len(comparison_op) + 1:]
                self.gui.input_text(self.SUBJECT_HEADER_EDIT, header)
            elif key == 'Contains term in content dictionary':
                self.gui._click_radio_button(self.CONTAINS_ITEM_RADIO)
                self.gui.select_from_list(self.DICT_COMBO, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class OtherHeaderProperty(ContentFilterProperty):
    HEADER_NAME_EDIT = "//input[@id='OtherHeader_header']"

    HEADER_EXIST_RADIO = "//input[@id='OtherHeader_radio_exists']"

    HEADER_VALUE_RADIO = "//input[@id='OtherHeader_radio_match_text']"
    HEADER_VALUE_OP_COMBO = "//select[@id='OtherHeader_operator']"
    HEADER_VALUE_EDIT = "//input[@id='OtherHeader_match_text']"

    HEADER_DICT_RADIO = "//input[@id='OtherHeader_radio_content_dict']"
    HEADER_DICT_COMBO = "//select[@id='OtherHeader_content_dict']"

    @classmethod
    def get_name(cls):
        return 'Other Header'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the message contains the specified header.
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
        """
        if 'Header Name' not in new_value.keys():
            raise ValueError('"Header Name" key is mandatory for "%s" property:' % \
                             (self.get_name(),))

        for key, value in new_value.items():
            if key == 'Header Name':
                self.gui.input_text(self.HEADER_NAME_EDIT,
                                    value)
            elif key == 'Header exists':
                self.gui._click_radio_button(self.HEADER_EXIST_RADIO)
            elif key == 'Header value':
                self.gui._click_radio_button(self.HEADER_VALUE_RADIO)
                comparison_op = parse_value(value, STRING_COMPARISON_OP)
                self.gui.select_from_list(self.HEADER_VALUE_OP_COMBO,
                                      comparison_op)
                header = value[len(comparison_op) + 1:]
                self.gui.input_text(self.HEADER_VALUE_EDIT, header)
            elif key == 'Header value contains term in content dictionary':
                self.gui._click_radio_button(self.HEADER_DICT_RADIO)
                self.gui.select_from_list(self.HEADER_DICT_COMBO, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class EnvelopeSenderProperty(ContentFilterProperty):
    ENVELOPE_SENDER_RADIO = "//input[@id='EnvelopeSender_radio_match_text']"
    ENVELOPE_SENDER_OP_COMBO = "//select[@id='EnvelopeSender_operator']"
    ENVELOPE_SENDER_EDIT = "//input[@id='EnvelopeSender_match_text']"

    ENVELOPE_LDAP_RADIO = "//input[@id='EnvelopeSender_radio_ldap_group']"
    ENVELOPE_LDAP_EDIT = "//input[@id='EnvelopeSender_ldap_group']"

    CONTAINS_DICT_RADIO = "//input[@id='EnvelopeSender_radio_content_dict']"
    DICT_COMBO = "//select[@id='EnvelopeSender_content_dict']"

    @classmethod
    def get_name(cls):
        return 'Envelope Sender'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the Envelope Sender (i.e., the Envelope From,
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
        """
        for key, value in new_value.items():
            if key == 'Envelope Sender':
                self.gui._click_radio_button(self.ENVELOPE_SENDER_RADIO)
                comparison_op = parse_value(value, STRING_COMPARISON_OP)
                self.gui.select_from_list(self.ENVELOPE_SENDER_OP_COMBO,
                                          comparison_op)
                sender = value[len(comparison_op) + 1:]
                self.gui.input_text(self.ENVELOPE_SENDER_EDIT, sender)
            elif key == 'Matches LDAP group':
                self.gui._click_radio_button(self.ENVELOPE_LDAP_RADIO)
                self.gui.input_text(self.ENVELOPE_LDAP_EDIT, value)
            elif key == 'Contains term in content dictionary':
                self.gui._click_radio_button(self.CONTAINS_DICT_RADIO)
                self.gui.select_from_list(self.DICT_COMBO, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class EnvelopeRecipientProperty(ContentFilterProperty):
    ENVELOPE_RECIPIENT_RADIO = "//input[@id='EnvelopeRecipient_radio_match_text']"
    ENVELOPE_RECIPIENT_OP_COMBO = "//select[@id='EnvelopeRecipient_operator']"
    ENVELOPE_RECIPIENT_EDIT = "//input[@id='EnvelopeRecipient_match_text']"

    ENVELOPE_LDAP_RADIO = "//input[@id='EnvelopeRecipient_radio_ldap_group']"
    ENVELOPE_LDAP_EDIT = "//input[@id='EnvelopeRecipient_ldap_group']"

    CONTAINS_DICT_RADIO = "//input[@id='EnvelopeRecipient_radio_content_dict']"
    DICT_COMBO = "//select[@id='EnvelopeRecipient_content_dict']"

    @classmethod
    def get_name(cls):
        return 'Envelope Recipient'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the Envelope Recipient, (i.e. the Envelope To,
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
        """
        for key, value in new_value.items():
            if key == 'Envelope Recipient':
                self.gui._click_radio_button(self.ENVELOPE_RECIPIENT_RADIO)
                comparison_op = parse_value(value, STRING_COMPARISON_OP)
                self.gui.select_from_list(self.ENVELOPE_RECIPIENT_OP_COMBO,
                                          comparison_op)
                sender = value[len(comparison_op) + 1:]
                self.gui.input_text(self.ENVELOPE_RECIPIENT_EDIT, sender)
            elif key == 'Matches LDAP group':
                self.gui._click_radio_button(self.ENVELOPE_LDAP_RADIO)
                self.gui.input_text(self.ENVELOPE_LDAP_EDIT, value)
            elif key == 'Contains term in content dictionary':
                self.gui._click_radio_button(self.CONTAINS_DICT_RADIO)
                self.gui.select_from_list(self.DICT_COMBO, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class ReceivingListenerProperty(ContentFilterProperty):
    COMPARISON_OP_COMBO = "//select[@id='ReceivingListener_operator']"
    LISTENER_NAME_COMBO = "//select[@id='ReceivingListener_listener']"

    @classmethod
    def get_name(cls):
        return 'Receiving Listener'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the message arrives via the specified listener
        Dictionary can contain the next items:
        | Receiving Listener | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part is existing listener name

        *Examples:*
        | ${new_value}= | Create Dictionary | Receiving Listener | Is InBoundMail |
        """
        for key, value in new_value.items():
            if key == 'Receiving Listener':
                comparison_op = parse_value(value, IS_NOT_COMPARISON_OP)
                self.gui.select_from_list(self.COMPARISON_OP_COMBO,
                                          comparison_op)
                listener_name = value[len(comparison_op) + 1:]
                self.gui.select_from_list(self.LISTENER_NAME_COMBO, listener_name)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class RemoteIPHostnameProperty(ContentFilterProperty):
    OPERATOR_COMBO = "//select[@id='RemoteIP_operator']"
    REMOTE_IP_EDIT = "//input[@id='RemoteIP_ip']"

    @classmethod
    def get_name(cls):
        return 'Remote IP/Hostname'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether the message is sent from a remote host that matches
        a specified IP address or Hostname
        Dictionary can contain the next items:
        | Remote IP/Hostname | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part is IP/Hostname name

        *Examples:*
        | ${new_value}= | Create Dictionary | Remote IP/Hostname | Is 1.1.1.1 |
        """
        for key, value in new_value.items():
            if key == 'Remote IP/Hostname':
                comparison_op = parse_value(value, IS_NOT_COMPARISON_OP)
                self.gui.select_from_list(self.OPERATOR_COMBO,
                                          comparison_op)
                hostname = value[len(comparison_op) + 1:]
                self.gui.input_text(self.REMOTE_IP_EDIT, hostname)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class ReputationScoreProperty(ContentFilterProperty):
    SCORE_RADIO = "//input[@id='ReputationScore_radio_score']"
    SCORE_OP_COMBO = "//select[@id='ReputationScore_contain_op']"
    SCORE_VALUE_EDIT = "//input[@id='ReputationScore_score']"

    NOSCORE_RADIO = "//input[@id='ReputationScore_radio_noscore']"

    @classmethod
    def get_name(cls):
        return 'Reputation Score'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: what is the sender's SenderBase Reputation Score.
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
        """
        for key, value in new_value.items():
            if key == 'Score':
                self.gui._click_radio_button(self.SCORE_RADIO)
                comparison_op = parse_value(value, NUMBER_COMPARISON_OP)
                self.gui.select_from_list(self.SCORE_OP_COMBO,
                                          comparison_op)
                scoreval = value[len(comparison_op) + 1:]
                self.gui.input_text(self.SCORE_VALUE_EDIT, scoreval)
            elif key == 'is "None" (no score defined)':
                self.gui._click_radio_button(self.NOSCORE_RADIO)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class DKIMAuthenticationProperty(ContentFilterProperty):
    AUTHENTICATION_RESULT_OP = "//select[@id='DKIMAuthentication_operator']"
    AUTHENTICATION_ERROR_COMBO = "//select[@id='DKIMAuthentication_pattern']"

    @classmethod
    def get_name(cls):
        return 'DKIM Authentication'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether DKIM Authentication is passed
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
        """
        for key, value in new_value.items():
            if key == 'DKIM Authentication Result':
                comparison_op = parse_value(value, IS_NOT_COMPARISON_OP)
                self.gui.select_from_list(self.AUTHENTICATION_RESULT_OP,
                                          comparison_op)
                error_pattern = parse_value(value, AUTH_RESULT_OP)
                self.gui.select_from_list(self.AUTHENTICATION_ERROR_COMBO,
                                          error_pattern)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class ForgedEmailDetectionProperty(ContentFilterProperty):
    @classmethod
    def get_name(cls):
        return 'Forged Email Detection'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: detects messages with forged sender address.
        Dictionary can contain the next items:
        | Forged Email Detection | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Forged Email Detection |
        | ... | ololo |
        """
        for key, value in new_value.items():
            if key == 'Forged Email Detection':
                pass
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SPFVerificationProperty(ContentFilterProperty):
    VERIFICATION_OP_COMBO = "//select[@id='SPFStatus_relop']"
    VERIFICATION_RESULT_CHECKBOX = lambda cls, result: \
        "//input[@id='SPFStatus_results[]::%s']" % (result,)

    @classmethod
    def get_name(cls):
        return 'SPF Verification'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: what are the SPF Verification results to match.
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
        """
        for key, value in new_value.items():
            if key == 'SPF Verification':
                comparison_op = parse_value(value, IS_NOT_COMPARISON_OP)
                self.gui.select_from_list(self.VERIFICATION_OP_COMBO,
                                          comparison_op)
                result = parse_value(value, VERIFICATION_RESULT_OP)
                self.gui._select_checkbox(self.VERIFICATION_RESULT_CHECKBOX(\
                                                result.lower()))
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))



class MessageLanguageProperty(ContentFilterProperty):
    MESSGLANG_OP_COMBO = "//select[@id='MessageLanguage_relop']"
    MESSGLANG_RESULT_CHECKBOX = lambda cls, result: \
        "//input[@id='MessageLanguage_results[]::%s']" % (result,)
    MESSGLANG_RESULT_CHECKBOX_UNKNOWN = "//input[@id='MessageLanguage_result_uk']"

    @classmethod
    def get_name(cls):
        return 'Message Language'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: what are the Message Language results to match.
        Dictionary can contain item:
        | Message Language | <value> |
        <value> is string containing 2 parts. First part can be one of these values:
        | Is | Is not |
        and the second part is one of these values:
        | English |
        | Spanish |
        | German |
        | French |
        | Italian |
        | Japanese |
        | Korean |
        | Portuguese |
        | Russian |
        | Chinese |
        | Taiwan |
        | Undetermined |

        *Examples:*
        | ${new_value}= | Create Dictionary | Message Language | Is English Spanish Taiwanese |
        | ${new_value}= | Create Dictionary | Message Language | Is English |
        | ${new_value}= | Create Dictionary | Message Language | Is English Spanish |
        """
        for key, value in new_value.items():
            if key == 'Message Language':
                comparison_op = parse_value(value, IS_NOT_COMPARISON_OP)
                self.gui.select_from_list(self.MESSGLANG_OP_COMBO, comparison_op)
                #Getting the languages from the value and converting to a list
                intermediatevalues=value[len(comparison_op) + 1:]
                languages=intermediatevalues.split()
                for language in languages:
                    if language.lower() == 'undetermined':
                        self.gui._select_checkbox(self.MESSGLANG_RESULT_CHECKBOX_UNKNOWN)
                    else:
                        result = parse_value(language, MESSAGE_LANGUAGE_RESULT_OP)
                        lang_code = get_language_code(result)
                        self.gui._select_checkbox(self.MESSGLANG_RESULT_CHECKBOX(\
                                                    lang_code.lower()))
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SMIMEGatewayMessageProperty(ContentFilterProperty):
    @classmethod
    def get_name(cls):
        return 'S/MIME Gateway Message'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: checks if a message is S/MIME gateway-to-gateway.
        Dictionary can contain the next items:
        | S/MIME Gateway Message | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | S/MIME Gateway Message |
        | ... | ololo |
        """
        for key, value in new_value.items():
            if key == 'S/MIME Gateway Message':
                pass
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SMIMEGatewayVerifiedProperty(ContentFilterProperty):
    @classmethod
    def get_name(cls):
        return 'S/MIME Gateway Verified'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: obtains the S/MIME gateway-to-gateway verification.
        Dictionary can contain the next items:
        | S/MIME Gateway Verified | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | S/MIME Gateway Verified |
        | ... | ololo |
        """
        for key, value in new_value.items():
            if key == 'S/MIME Gateway Verified':
                pass
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class QuarantineProperty(ContentFilterProperty):
    SEND_TO_QUAR_COMBO = "//select[@id='Quarantine_quarantine']"
    DUPLICATE_MSG_CHECKBOX = "//input[@id='Quarantine_duplicate']"

    @classmethod
    def get_name(cls):
        return 'Quarantine'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: flags the message to be held in one of the system
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
        """
        for key, value in new_value.items():
            if key == 'Send message to quarantine':
                self.gui.select_from_list(self.SEND_TO_QUAR_COMBO,
                                          value)
            elif key == 'Duplicate message':
                if value:
                    self.gui._select_checkbox(self.DUPLICATE_MSG_CHECKBOX)
                else:
                    self.gui._unselect_checkbox(self.DUPLICATE_MSG_CHECKBOX)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class EncryptOnDeliveryProperty(ContentFilterProperty):
    ENCRYPTION_RULE = "//select[@id='Encrypt_Deferred_Action_otls']"
    ENCRYPTION_PROFILE = "//select[@id='Encrypt_Deferred_Action_profile']"
    SUBJECT = "//input[@id='Encrypt_Deferred_Action_subject']"

    @classmethod
    def get_name(cls):
        return 'Encrypt on Delivery'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: the message continues to the next stage of processing.
        When all processing is complete, the message is encrypted and delivered.
        Dictionary can contain item:
        *Parameters:*
        - `new_value`: whether to encrypt the message, then deliver without
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
        """
        for key, value in new_value.items():
            if key == 'Encryption Rule':
                self.gui.select_from_list(self.ENCRYPTION_RULE, value)
            elif key == 'Encryption Profile':
                self.gui.select_from_list(self.ENCRYPTION_PROFILE,
                                          value)
            elif key == 'Subject':
                self.gui.input_text(self.SUBJECT, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class StripAttachmentByContentProperty(ContentFilterProperty):
    CONTAINS_TEXT_RADIO = "//input[@id='StripAttachment_radio_attachment_text']"
    CONTAINS_TEXT_EDIT = "//input[@id='StripAttachment_attachment_text']"

    CONTAINS_SMART_IDENTIFIER_RADIO = "//input[@id='StripAttachment_radio_smart_id']"
    CONTAINS_SMART_IDENTIFIER_COMBO = "//select[@id='StripAttachment_smart_id']"

    CONTAINS_ITEM_RADIO = "//input[@id='StripAttachment_radio_content_dict']"
    CAINTAINS_ITEM_DICT_COMBO = "//select[@id='StripAttachment_content_dict']"

    NUMBER_OF_MATCHES = "//input[@id='StripAttachment_threshold']"

    REPLACE_MESSAGE_EDIT = "//textarea[@id='StripAttachment_replace_message']"

    @classmethod
    def get_name(cls):
        return 'Strip Attachment by Content'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: drops all attachments on messages that contain text
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
        """
        for key, value in new_value.items():
            if key == 'Attachment contains':
                self.gui._click_radio_button(self.CONTAINS_TEXT_RADIO)
                self.gui.input_text(self.CONTAINS_TEXT_EDIT, value)
            elif key == 'Contains smart identifier':
                self.gui._click_radio_button(self.CONTAINS_SMART_IDENTIFIER_RADIO)
                self.gui.select_from_list(self.CONTAINS_SMART_IDENTIFIER_COMBO,
                                          value)
            elif key == 'Attachment contains term in content dictionary':
                self.gui._click_radio_button(self.CONTAINS_ITEM_RADIO)
                self.gui.select_from_list(self.CAINTAINS_ITEM_DICT_COMBO,
                                          value)
            elif key == 'Number of matches required':
                self.gui.input_text(self.NUMBER_OF_MATCHES, value)
            elif key == 'Replacement Message':
                self.gui.input_text(self.REPLACE_MESSAGE_EDIT, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class StripAttachmentByFileInfoProperty(ContentFilterProperty):
    FILENAME_CONTAINS_RADIO = "//input[@id='StripAttachmentByFileInfo_radio_filename']"
    FILENAME_CONTAINS_COMBO = "//select[@id='StripAttachmentByFileInfo_operation']"
    FILENAME_CONTAINS_EDIT = "//input[@id='StripAttachmentByFileInfo_filename_text']"

    FILESIZE_RADIO = "//input[@id='StripAttachmentByFileInfo_radio_filesize']"
    FILESIZE_EDIT = "//input[@id='StripAttachmentByFileInfo_filesize']"

    FILETYPE_RADIO = "//input[@id='StripAttachmentByFileInfo_radio_filetype']"
    FILETYPE_COMBO = "//select[@id='StripAttachmentByFileInfo_filetype']"

    MIMETYPE_RADIO = "//input[@id='StripAttachmentByFileInfo_radio_mimetype']"
    MIMETYPE_EDIT = "//input[@id='StripAttachmentByFileInfo_mimetype']"

    MACRO_DETECTED_RADIO = "//input[@id='StripAttachmentByFileInfo_radio_ismacrodetected']"

    IIA_VERDICT_RADIO = "//input[@id='StripAttachmentByFileInfo_radio_imageverdict']"
    IIA_RESULT_COMBO = "//select[@id='StripAttachmentByFileInfo_imageverdict']"

    ETF_RADIO="//input[@id='StripAttachmentByFileInfo_radio_etf']"
    ETF_AVAILABLE_CATEGORIES_COMBO = "//select[@id='StripAttachmentByFileInfo_etf_list_available_etf_list']"
    ETF_SELECTED_CATEGORIES_COMBO = "//select[@id='StripAttachmentByFileInfo_etf_list_chosen_etf_list']"
    ETF_ADD_BUTTON = "//input[@value='Add >' and contains(@onclick, 'StripAttachmentByFileInfo_etf_list_available_etf_list')]"
    ETF_REMOVE_BUTTON = "//input[@value='< Remove' and contains(@onclick, 'StripAttachmentByFileInfo_etf_list_chosen_etf_list')]"
    ETF_FILEHASH_EXCEPTION_COMBO = "//select[@id='StripAttachmentByFileInfo_etf_filehash']"

    REPLACEMENT_MSG_EDIT = "//textarea[@id='StripAttachmentByFileInfo_replace_message']"

    @classmethod
    def get_name(cls):
        return 'Strip Attachment by File Info'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: drops all attachments on messages that match the
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
        | Macro Detected |
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

        *Examples:*
        | ${new_value}= | Create Dictionary | Filename | Contains blabla |
        | ... | Replacement Message | my replacement message |
        """
        for key, value in new_value.items():
            if key == 'Filename':
                self.gui._click_radio_button(self.FILENAME_CONTAINS_RADIO)
                comparison_operator = parse_value(value,
                                                  FILENAME_COMPARISON_OP)
                self.gui.select_from_list(self.FILENAME_CONTAINS_COMBO,
                                          comparison_operator)
                filename_part = value[len(comparison_operator) + 1:]
                self.gui.input_text(self.FILENAME_CONTAINS_EDIT,
                                    filename_part)
            elif key == 'File size is greater than':
                self.gui._click_radio_button(self.FILESIZE_RADIO)
                size = parse_value(value, r'(\d+)', True)
                self.gui.input_text(self.FILESIZE_EDIT, size)
            elif key == 'File type is':
                self.gui._click_radio_button(self.FILETYPE_RADIO)
                filetype = parse_value(value, FILETYPE)
                self.gui.select_from_list(self.FILETYPE_COMBO,
                                          value)
            elif key == 'MIME type is':
                self.gui._click_radio_button(self.MIMETYPE_RADIO)
                self.gui.input_text(self.MIMETYPE_EDIT, value)
            elif key == 'Macro Detected':
                self.gui._click_radio_button(self.MACRO_DETECTED_RADIO)
            elif key == 'Image Analysis Verdict is':
                self.gui._click_radio_button(self.IIA_VERDICT_RADIO)
                result = parse_value(value, IIA_VEDICT_RESULTS)
                self.gui.select_from_list(self.IIA_RESULT_COMBO,
                                          result)
            elif key.lower() == 'external threat feeds':
                self.gui._click_radio_button(self.ETF_RADIO)
                for k,v in value.iteritems():
                    if k.lower()== 'etf add categories':
                        for list in v:
                            self.gui.select_from_list(self.ETF_AVAILABLE_CATEGORIES_COMBO,list)
                        self.gui.click_button(self.ETF_ADD_BUTTON, "don't wait")
                    elif k.lower() == 'etf remove categories':
                        for list in v:
                            self.gui.select_from_list(self.ETF_SELECTED_CATEGORIES_COMBO,list)
                        self.gui.click_button(self.ETF_REMOVE_BUTTON, "don't wait")
                    elif key.lower() == 'use a file hash exception list':
                        self.gui.select_from_list(self.ETF_FILEHASH_EXCEPTION_COMBO,value)

            elif key == 'Replacement Message':
                self.gui.input_text(self.REPLACEMENT_MSG_EDIT, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class URLCategoryActionProperty(ContentFilterProperty):
    AVAILABLE_CATEGORIES_COMBO = "//select[@id='UrlCategoryAction_action_categories_available_action_categories']"
    URL_ADD_BUTTON = "//input[@value='Add >' and contains(@onclick, 'UrlCategoryAction_action_categories_available_action_categories')]"

    SELECTED_CATEGORIES_COMBO = "//select[@id='UrlCategoryAction_action_categories_chosen_action_categories']"
    REMOVE_BUTTON = "xpath=(//input[@value='< Remove'])[2]"

    URL_WHITELIST_COMBO = "//select[@id='UrlCategoryAction_url_whitelist']"

    DEFANG_RADIO = "//input[@id='UrlCategoryAction_action_on_url_defang']"

    REDIRECT_RADIO = "//input[@id='UrlCategoryAction_action_on_url_redirect_to_proxy']"

    REPLACE_RADIO = "//input[@id='UrlCategoryAction_action_on_url_replace_with_text']"
    REPLACE_EDIT = "//input[@id='UrlCategoryAction_replace_text']"

    ALL_MESSAGES_RADIO = "//input[@id='UrlCategoryAction_perform_action_0']"
    UNSIGNED_MESSAGES_RADIO = "//input[@id='UrlCategoryAction_perform_action_1']"

    @classmethod
    def get_name(cls):
        return 'URL Category Action'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: Does any URL in the message body belong to one of the selected categories
        Dictionary can contain the next items:
        | Add Categories | <value> |
        <value> contains list of URL Categories to be added
        or
        | Remove Categories | <value> |
        <value> contains list of URL Categories to be removed
        or
        | Use a URL whitelist | <value> |
        <value> contains url whitelist value
        or
        | Defang URL |
        or
        | Redirect to Cisco Security Proxy |
        or
        | Replace URL with text message | <value> |
        <value> contains the replaced text
        or
        | Perform Action for All Messages |
        or
        | Perform Action for Unsigned Messages |

        *Examples:*
        | ${urls} | Create List  Arts  Adult |

        | ${new_value} | Create Dictionary | Add Categories  ${urls} |
        | ... |  Use a URL whitelist | anup |
        | ... |  Replace URL with text message | webcat |
        | ... |  Perform Action for Unsigned Messages | None |
        | ${actions} | Content Filter Create Actions |
        | ... | URL Category Action | ${new_value} |
        """
        for key, value in new_value.items():
            if key == 'Add Categories':
                for list in value:
                    self.gui.select_from_list(self.AVAILABLE_CATEGORIES_COMBO,list)
                self.gui.click_button(self.URL_ADD_BUTTON, "don't wait")
            elif key == 'Remove Categories':
                for list in value:
                    self.gui.select_from_list(self.SELECTED_CATEGORIES_COMBO,list)
                self.gui.click_button(self.REMOVE_BUTTON, "don't wait")
            elif key == 'Use a URL whitelist':
                self.gui.select_from_list(self.URL_WHITELIST_COMBO,value)
            elif key == 'Defang URL':
                self.gui._click_radio_button(self.DEFANG_RADIO)
            elif key == 'Redirect to Cisco Security Proxy':
                self.gui._click_radio_button(self.REDIRECT_RADIO)
            elif key == 'Replace URL with text message':
                self.gui._click_radio_button(self.REPLACE_RADIO)
                self.gui.input_text(self.REPLACE_EDIT,value)
            elif key == 'Perform Action for All Messages':
                self.gui._click_radio_button(self.ALL_MESSAGES_RADIO)
            elif key == 'Perform Action for Unsigned Messages':
                self.gui._click_radio_button(self.UNSIGNED_MESSAGES_RADIO)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class URLReputationActionProperty(ContentFilterProperty):

    URL_REP_ACTION_WBRS = "//input[@id='UrlReputationAction_url_reputation_rule_wbrs']"
    URL_REP_ACTION_EXTERNAL_THREAT_FEEDS = "//input[@id='UrlReputationAction_url_reputation_rule_tf_source']"

    URL_WHITELIST_REPUTATION_COMBO = "//select[@id='UrlReputationAction_url_whitelist']"

    MALICIOUS_RADIO = "//input[@id='UrlReputationAction_url_reputation_Malicious']"
    NEUTRAL_RADIO = "//input[@id='UrlReputationAction_url_reputation_Neutral']"
    CLEAN_RADIO = "//input[@id='UrlReputationAction_url_reputation_Clean']"
    CUSTOMRANGE_RADIO = "//input[@id='UrlReputationAction_url_reputation_Custom']"
    NOSCORE_RADIO = "//input[@id='UrlReputationAction_url_reputation_No Score']"
    DEFANG_REPUTATION_RADIO = "//input[@id='UrlReputationAction_action_on_url_defang']"
    REDIRECT_REPUTATION_RADIO = "//input[@id='UrlReputationAction_action_on_url_redirect_to_proxy']"
    REPLACE_REPUTATION_RADIO = "//input[@id='UrlReputationAction_action_on_url_replace_with_text']"
    ALL_MESSAGES_REPUTATION_RADIO = "//input[@id='UrlReputationAction_perform_action_0']"
    UNSIGNED_MESSAGES_REPUTATION_RADIO = "//input[@id='UrlReputationAction_perform_action_1']"

    CUSTOMRANGE_MIN_EDIT = "//input[@id='UrlReputationAction_min_score']"
    CUSTOMRANGE_MAX_EDIT = "//input[@id='UrlReputationAction_max_score']"
    REPLACEURL_REPUTATION_EDIT = "//input[@id='UrlReputationAction_replace_text']"

    STRIP_ATTACHMENT_EDIT = "//textarea[@id='UrlReputationAction_strip_attachment']"

    AVAILABLE_SOURCE_COMBO = "//select[@id='UrlReputationAction_tf_source_name_available_tf_source_name']"
    SOURCE_ADD_BUTTON = "//input[@value='Add >' and contains(@onclick, 'UrlReputationAction_tf_source_name_available_tf_source_name')]"

    SELECTED_SOURCE_COMBO = "//select[@id='UrlReputationAction_tf_source_name_chosen_tf_source_nam']"
    SOURCE_REMOVE_BUTTON = "//input[@value='< Remove' and contains(@onclick, 'UrlReputationAction_tf_source_name_chosen_tf_source_name')]"

    MESSAGE_BODY_SUBJECT = "//input[@id='UrlReputationAction_check_url_within_message_body']"
    ONLY_ATTACHMENTS = "//input[@id='UrlReputationAction_check_url_within_attachments']"
    MSG_BDY_ATTACHMENTS = "//input[@id='UrlReputationAction_check_url_within_include_all']"

    @classmethod
    def get_name(cls):
        return 'URL Reputation Action'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: This rule evaluates URL's using their Web Based Reputation Score (WBRS)
        Dictionary can contain the next items:
        | Use a URL Reputation whitelist | <value> |
        <value> contains url whitelist value
        or
        | Malicious Reputation URL |
        or
        | Suspect Reputation URL |
        or
        | Clean Reputation URL |
        or
        | NoScore Reputation URL |
        or
        | CustomRange Reputation URL Min value | <value> |
        <value> contains the min CustomRange value
        or
        | CustomRange Reputation URL Max value | <value> |
        <value> contains the max CustomRange value
        or
        | Defang Reputation URL |
        or
        | Redirect Reputation URL to Cisco Security Proxy |
        or
        | Replace Reputation URL with text message | <value> |
        <value> contains the replaced text
        or
        | Perform Action for All URL Repuation Messages |
        or
        | Perform Action for Unsigned URL Reputation Messages |

        *Examples:*

        | ${new_value} | Create Dictionary |
        | ... |  Use a URL Reputation whitelist | webreputation |
        | ... |  Replace Reputation URL with text message | webcat |
        | ... |  Malicious Reputation URL | None |
        | ... |  Perform Action for Unsigned URL Reputation Messages | None |
        | ${actions} | Content Filter Create Actions |
        | ... | URL Reputation Action | ${new_value} |
        """
        for key, value in new_value.items():
            if  key.lower() == 'url reputation type':
                if value.lower() == 'url reputation wbrs':
                    self.gui._click_radio_button(self.URL_REP_ACTION_WBRS)
                elif value.lower() == 'url reputation external threat feeds':
                    self.gui._click_radio_button(self.URL_REP_ACTION_EXTERNAL_THREAT_FEEDS)
            elif key.lower() == 'use a url reputation whitelist':
                self.gui.select_from_list(self.URL_WHITELIST_REPUTATION_COMBO,value)
            elif key.lower() == 'malicious reputation url':
                self.gui._click_radio_button(self.MALICIOUS_RADIO)
            elif key.lower() == 'suspect reputation url':
                self.gui._click_radio_button(self.NEUTRAL_RADIO)
            elif key.lower() == 'clean reputation url':
                self.gui._click_radio_button(self.CLEAN_RADIO)
            elif key.lower() == 'noscore reputation url':
                self.gui._click_radio_button(self.NOSCORE_RADIO)
            elif key.lower() == 'customrange reputation url min value':
                self.gui._click_radio_button(self.CUSTOMRANGE_RADIO)
                self.gui.input_text(self.CUSTOMRANGE_MIN_EDIT,value)
            elif key.lower() == 'customrange reputation url max value':
                self.gui._click_radio_button(self.CUSTOMRANGE_RADIO)
                self.gui.input_text(self.CUSTOMRANGE_MAX_EDIT,value)
            elif key.lower() == 'defang reputation url':
                self.gui._click_radio_button(self.DEFANG_REPUTATION_RADIO)
            elif key.lower() == 'redirect reputation url to cisco security proxy':
                self.gui._click_radio_button(self.REDIRECT_REPUTATION_RADIO)
            elif key.lower() == 'replace reputation url with text message':
                self.gui._click_radio_button(self.REPLACE_REPUTATION_RADIO)
                self.gui.input_text(self.REPLACEURL_REPUTATION_EDIT,value)
            elif key.lower() == 'perform action for all url reputation messages':
                self.gui._click_radio_button(self.ALL_MESSAGES_REPUTATION_RADIO)
            elif key.lower() == 'perform action for unsigned url reputation messages':
                self.gui._click_radio_button(self.UNSIGNED_MESSAGES_REPUTATION_RADIO)
            elif key.lower() == 'strip attachment with text message':
                self.gui.input_text(self.STRIP_ATTACHMENT_EDIT,value)
            elif key.lower() == 'scan type':
                if value.lower() == 'message body and subject':
                    self.gui._click_radio_button(self.MESSAGE_BODY_SUBJECT)
                elif value.lower() == 'only attachments':
                    self.gui._click_radio_button(self.ONLY_ATTACHMENTS)
                elif value.lower() == 'all':
                    self.gui._click_radio_button(self.MSG_BDY_ATTACHMENTS)
            elif key.lower() == 'add sources':
                for list in value:
                    self.gui.select_from_list(self.AVAILABLE_SOURCE_COMBO,list)
                self.gui.click_button(self.SOURCE_ADD_BUTTON, "don't wait")
            elif key.lower() == 'remove sources':
                for list in value:
                    self.gui.select_from_list(self.SELECTED_SOURCE_COMBO,list)
                self.gui.click_button(self.SOURCE_REMOVE_BUTTON, "don't wait")
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class AddDisclaimerTextProperty(ContentFilterProperty):
    ABOVE_MESSAGE = "//input[@id='DisclaimerText_radio_Add_Heading_Action']"
    BELOW_MESSAGE = "//input[@id='DisclaimerText_radio_Add_Footer_Action']"

    DISCLAIMER_PROFILE = "//select[@id='DisclaimerText_resource']"

    @classmethod
    def get_name(cls):
        return 'Add Disclaimer Text'

    def set(self, new_value):
        """
        To set this property at least one disclaimer text resource should be
        already defined

        *Parameters:*
        - `new_value`: adds text above or below the message body.
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
        """
        for key, value in new_value.items():
            if key == 'Add to':
                if value.upper().find('ABOVE') >= 0:
                    self.gui._click_radio_button(self.ABOVE_MESSAGE)
                elif value.upper().find('BELOW') >= 0:
                    self.gui._click_radio_button(self.BELOW_MESSAGE)
                else:
                    raise ValueError('Unknown value is set to "Add to" option of'\
                                     ' "%s" property' % (self.get_name(),))
            elif key == 'Disclaimer Text':
                self.gui.select_from_list(self.DISCLAIMER_PROFILE, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class BypassOutbreakFilterScanningProperty(ContentFilterProperty):
    @classmethod
    def get_name(cls):
        return 'Bypass Outbreak Filter Scanning'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether to bypass Outbreak Filter scanning for message.
        Dictionary can contain item:
        | Bypass Outbreak Filter Scanning | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Bypass Outbreak Filter Scanning |
        | ... | Enable! |
        """
        for key, value in new_value.items():
            if key == 'Bypass Outbreak Filter Scanning':
                pass
            else:
                raise ValueError('Unknown key name is given for "%s" property:'\
                                 ' "%s"' % (key, self.get_name()))


class BypassDKIMSigningProperty(ContentFilterProperty):
    @classmethod
    def get_name(cls):
        return 'Bypass DKIM Signing'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether to bypass DKIM Signing for message.
        Dictionary can contain item:
        | Bypass DKIM Signing | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Bypass DKIM Signing | Activate it |
        """
        for key, value in new_value.items():
            if key == 'Bypass DKIM Signing':
                pass
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SendCopyBccProperty(ContentFilterProperty):
    EMAIL_ADDRESSES = "//textarea[@id='BCC_addresses']"

    SUBJECT = "//input[@id='BCC_subject']"
    RETURN_PATH = "//input[@id='BCC_return_path']"
    ALTERNATE_MAIL_HOST = "//input[@id='BCC_altmailhost']"

    @classmethod
    def get_name(cls):
        return 'Send Copy (Bcc:)'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: copies this message anonymously to specified recipient(s)
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
        """
        for key, value in new_value.items():
            if key == 'Email Addresses':
                self.gui.input_text(self.EMAIL_ADDRESSES, value)
            elif key == 'Subject':
                self.gui.input_text(self.SUBJECT, value)
            elif key == 'Return Path':
                self.gui.input_text(self.RETURN_PATH, value)
            elif key == 'Alternate Mail Host':
                self.gui.input_text(self.ALTERNATE_MAIL_HOST, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class NotifyProperty(ContentFilterProperty):
    EMAIL_ADDRESSES = "//textarea[@id='Notify_addresses']"
    SENDER_CHECKBOX = "//input[@id='Notify_notify_sender']"
    RECIPIENT_CHECKBOX = "//input[@id='Notify_notify_recipients']"

    SUBJECT = "//input[@id='Notify_subject']"
    RETURN_PATH = "//input[@id='Notify_return_path']"
    NOTIFY_TEMPLATE = "//select[@id='Notify_template']"

    INCUDE_ORIGINAL_MSG = "//input[@id='Notify_includeOriginal']"

    @classmethod
    def get_name(cls):
        return 'Notify'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: reports this message to specified recipient(s)
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
        """
        for key, value in new_value.items():
            if key == 'Email Addresses':
                self.gui.input_text(self.EMAIL_ADDRESSES, value)
            elif key == 'Email Addresses Sender':
                if value:
                    self.gui._select_checkbox(self.SENDER_CHECKBOX)
                else:
                    self.gui._unselect_checkbox(self.SENDER_CHECKBOX)
            elif key == 'Email Addresses Recipient(s)':
                if value:
                    self.gui._select_checkbox(self.RECIPIENT_CHECKBOX)
                else:
                    self.gui._unselect_checkbox(self.RECIPIENT_CHECKBOX)
            elif key == 'Subject':
                self.gui.input_text(self.SUBJECT, value)
            elif key == 'Return Path':
                self.gui.input_text(self.RETURN_PATH, value)
            elif key == 'Use Template':
                self.gui.select_from_list(self.NOTIFY_TEMPLATE,
                                          value)
            elif key == 'Include original message as attachment':
                if value:
                    self.gui._select_checkbox(self.INCUDE_ORIGINAL_MSG)
                else:
                    self.gui._unselect_checkbox(self.INCUDE_ORIGINAL_MSG)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class ChangeRecipientToProperty(ContentFilterProperty):
    EMAIL_ADDRESS = "//input[@id='ChangeRecipient_address']"

    @classmethod
    def get_name(cls):
        return 'Change Recipient to'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: changes a recipient of the message.
        Dictionary can contain the next items:
        | Email Address | <new recipient's email address> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Email Address | mm@me.com |
        """
        for key, value in new_value.items():
            if key == 'Email Address':
                self.gui.input_text(self.EMAIL_ADDRESS, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SendToAlternateDestinationHostProperty(ContentFilterProperty):
    MAIL_HOST = "//input[@id='ChangeHost_address']"

    @classmethod
    def get_name(cls):
        return 'Send to Alternate Destination Host'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: changes the destination mail host for the message.
        Dictionary can contain the next items:
        | Mail Host | <new messages's destination mail host> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Mail Host | me.com |
        """
        for key, value in new_value.items():
            if key == 'Mail Host':
                self.gui.input_text(self.MAIL_HOST, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class DeliverFromIPInterfaceProperty(ContentFilterProperty):
    IP_INTERFACE_COMBO = "//*[@id='AlternateSourceInterface_interface']"

    @classmethod
    def get_name(cls):
        return 'Deliver from IP Interface'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: send from the specified IP Interface.
        Dictionary can contain the next items:
        | Send from IP Interface | <appliance's IP interface DNS> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Send from IP Interface |
        | ... | a001.d1.c600-08.auto |
        """
        for key, value in new_value.items():
            if key == 'Send from IP Interface':
                self.gui.select_from_list(self.IP_INTERFACE_COMBO, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class StripHeaderProperty(ContentFilterProperty):
    HEADER_NAME = "//input[@id='StripHeader_header_name']"

    @classmethod
    def get_name(cls):
        return 'Strip Header'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: remove specific headers from the message before
        delivering. All matching headers are removed.
        Dictionary can contain the next items:
        | Header Name | <header name to by removed> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Header Name |
        | ... | X-My-Cool-Header |
        """
        for key, value in new_value.items():
            if key == 'Header Name':
                self.gui.input_text(self.HEADER_NAME, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class AddEditHeaderProperty(ContentFilterProperty):
    HEADER_NAME = "//input[@id='AddEditHeader_header_name']"

    VALUE_FOR_NEW_HEADER_RADIO = "//input[@id='AddEditHeader_operation_add']"
    VALUE_FOR_NEW_HEADER_EDIT = "//input[@id='AddEditHeader_add_value']"

    PREPEND_VALUE_RADIO = "//input[@id='AddEditHeader_operation_prepend']"
    PREPEND_VALUE_EDIT = "//input[@id='AddEditHeader_prepend_value']"

    APPEND_TO_VALUE_RADIO = "//input[@id='AddEditHeader_operation_append']"
    APPEND_TO_VALUE_EDIT = "//input[@id='AddEditHeader_append_value']"

    SEARCH_AND_REPLACE_RADIO = "//input[@id='AddEditHeader_operation_edit']"
    SEARCH_FOR_EDIT = "//input[@id='AddEditHeader_remove_value']"
    REPLACE_WITH_EDIT = "//input[@id='AddEditHeader_edit_value']"

    @classmethod
    def get_name(cls):
        return 'Add/Edit Header'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: inserts a header and value pair into
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
        """
        for key, value in new_value.items():
            if key == 'Header Name':
                self.gui.input_text(self.HEADER_NAME, value)
            elif key == 'Specify Value for New Header':
                self.gui._click_radio_button(self.VALUE_FOR_NEW_HEADER_RADIO)
                self.gui.input_text(self.VALUE_FOR_NEW_HEADER_EDIT, value)
            elif key == 'Prepend to the Value of Existing Header':
                self.gui._click_radio_button(self.PREPEND_VALUE_RADIO)
                self.gui.input_text(self.PREPEND_VALUE_EDIT, value)
            elif key == 'Append to the Value of Existing Header':
                self.gui._click_radio_button(self.APPEND_TO_VALUE_RADIO)
                self.gui.input_text(self.APPEND_TO_VALUE_EDIT, value)
            elif key == 'Search & Replace from the Value of Existing Header':
                self.gui._click_radio_button(self.SEARCH_AND_REPLACE_RADIO)
            elif key == 'Search for':
                self.gui.input_text(self.SEARCH_FOR_EDIT, value)
            elif key == 'Replace with':
                self.gui.input_text(self.REPLACE_WITH_EDIT, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class AddMessageTagProperty(ContentFilterProperty):
    TERM_EDIT = "//input[@id='MessageTag_message_tag']"

    @classmethod
    def get_name(cls):
        return 'Add Message Tag'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: message Tags are metadata to be used
        elsewhere in the system. For example, DLP Policies
        allow filtering by message tags.
        Dictionary can contain the next items:
        | Enter a term | <tag to be added> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Enter a term |
        | ... | blabla |
        """
        for key, value in new_value.items():
            if key == 'Enter a term':
                self.gui.input_text(self.TERM_EDIT, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class AddLogEntryProperty(ContentFilterProperty):
    ENTRY_EDIT = "//input[@id='LogEntry_log_message']"

    @classmethod
    def get_name(cls):
        return 'Add Log Entry'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether to insert customized text into IronPort Text
        Mail Logs.
        Dictionary can contain the next items:
        | Text | <text to be inserted> |, mandatory

        *Examples:*
        | ${new_value}= | Create Dictionary | Text |
        | ... | blabla |
        """
        for key, value in new_value.items():
            if key == 'Text':
                self.gui.input_text(self.ENTRY_EDIT, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class EncryptAndDeliverNowFinalActionProperty(ContentFilterProperty):
    ENCRYPTION_RULE = "//select[@id='Encrypt_Action_otls']"
    ENCRYPTION_PROFILE = "//select[@id='Encrypt_Action_profile']"
    SUBJECT = "//input[@id='Encrypt_Action_subject']"

    @classmethod
    def get_name(cls):
        return 'Encrypt and Deliver Now (Final Action)'

    def set(self, new_value):
        """
        This parameter can be set only if there are availavle
        encryption profiles on ESA appliance

        *Parameters:*
        - `new_value`: whether to encrypt the message, then deliver without
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
        """
        for key, value in new_value.items():
            if key == 'Encryption Rule':
                self.gui.select_from_list(self.ENCRYPTION_RULE, value)
            elif key == 'Encryption Profile':
                self.gui.select_from_list(self.ENCRYPTION_PROFILE,
                                          value)
            elif key == 'Subject':
                self.gui.input_text(self.SUBJECT, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class BounceFinalActionProperty(ContentFilterProperty):
    @classmethod
    def get_name(cls):
        return 'Bounce (Final Action)'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether to send the message back to the sender
        Dictionary can contain the next items:
        | Bounce (Final Action) | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Bounce (Final Action) |
        | ... | Give me it now |
        """
        for key, value in new_value.items():
            if key == 'Bounce (Final Action)':
                pass
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SkipRemainingContentFiltersFinalActionProperty(ContentFilterProperty):
    @classmethod
    def get_name(cls):
        return 'Skip Remaining Content Filters (Final Action)'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether to deliver the message to the next stage of processing,
        skipping any further content filters. Depending on configuration this may
        mean deliver the message to recipient(s), quarantine, or begin Outbreak
        Filters scanning.
        Dictionary can contain the next items:
        | Skip Remaining Content Filters (Final Action) | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Skip Remaining Content Filters (Final Action) |
        | ... | yeah |
        """
        for key, value in new_value.items():
            if key == 'Skip Remaining Content Filters (Final Action)':
                pass
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class DropFinalActionProperty(ContentFilterProperty):
    @classmethod
    def get_name(cls):
        return 'Drop (Final Action)'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether to drop and discard the message.
        Dictionary can contain the next items:
        | Drop (Final Action) | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Drop (Final Action) |
        | ... | ololo |
        """
        for key, value in new_value.items():
            if key == 'Drop (Final Action)':
                pass
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SMIMESignEncryptonDeliveryProperty(ContentFilterProperty):
    SMIME_PROFILE = "//select[@id='Smime_Gateway_Deferred_Action_profile']"

    @classmethod
    def get_name(cls):
        return 'S/MIME Sign/Encrypt on Delivery'

    def set(self, new_value):
        """
        Provides deferred S/MIME gateway-to-gateway signing/encryption

        *Parameters:*
        - `new_value`: Provides deferred S/MIME gateway-to-gateway signing/encryption.
        Dictionary can contain the next items:
        | SMIMEProfile | <value> |
        value is the SMIME Signing Profile

        *Examples:*
        | ${new_value}= | Create Dictionary | SMIMEProfile | aaa |
        """
        for key, value in new_value.items():
            if key == 'SMIMEProfile':
                self.gui.select_from_list(self.SMIME_PROFILE, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SMIMESignEncryptFinalActionProperty(ContentFilterProperty):
    SMIME_PROFILE = "//select[@id='Smime_Gateway_Action_profile']"

    @classmethod
    def get_name(cls):
        return 'S/MIME Sign/Encrypt (Final Action)'

    def set(self, new_value):
        """
        The S/MIME gateway-to-gateway sign and encrypt filter action
        is used to sign and encrypt outgoing messages
        *Parameters:*
        - `new_value`: Signs and encrypt outgoing messages.
        Dictionary can contain the next items:
        | SMIMEProfile | <value> |
        value is the SMIME Signing Profile

        *Examples:*
        | ${new_value}= | Create Dictionary | SMIMEProfile | aaa |
        """
        for key, value in new_value.items():
            if key == 'SMIMEProfile':
                self.gui.select_from_list(self.SMIME_PROFILE, value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class GeoCountriesProperty(ContentFilterProperty):
    AVAILABLE_COUNTRIES = "//select[@id='Geolocation_Rule_geolocation_name_available_geolocation_name']"
    ADD_BUTTON = "xpath=(//*[@id='ruleform_Geolocation_Rule']/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input[1])"

    SELECTED_COUNTRIES = "//select[@id='Geolocation_Rule_geolocation_name_chosen_geolocation_name']"
    REMOVE_BUTTON = "xpath=(//*[@id='ruleform_Geolocation_Rule']/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input[1])"

    @classmethod
    def get_name(cls):
        return 'Geolocation'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: Does any URL in the message body belong to one of the selected categories
        Dictionary can contain the next items:
        | Add Countries | <value> |
        <value> contains list of Country names to be added.
        Check Web UI to know about available country names.
        or
        | Remove Countries | <value> |
        <value> contains list of Country names to be removed
        or

        *Return:*
        None

        *Examples:*
        | ${countries} | Create List |
        | ... | Afghanistan          |
        | ... | Bangladesh           |
        | ... | China                |
        | ... | Ireland              |
        | ... | Japan                |
        | ... | Korea, Republic of   |
        | ... | Pakistan             |
        | ${country_settings} | Create Dictionary |
        | ... | Add Countries | ${countries}      |
        | ${conditions} | Content Filter Create Conditions |
        | ... | Geolocation | ${country_settings}          |
        """
        for key, value in new_value.items():
            if key == 'Add Countries':
                for list in value:
                    self.gui.select_from_list(self.AVAILABLE_COUNTRIES, list)
                self.gui.click_button(self.ADD_BUTTON, "don't wait")
            elif key == 'Remove Countries':
                for list in value:
                    self.gui.select_from_list(self.SELECTED_COUNTRIES, list)
                self.gui.click_button(self.REMOVE_BUTTON, "don't wait")
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class DomainReputationProperty(ContentFilterProperty):
    DOMAIN_REPUTATION = "//input[@id='DomainReputation_dr_parent_sdr']"
    DOMAIN_REPUTATION_VERDICT = "//input[@id='DomainReputation_dr_sdr_child1_verdict']"
    DOMAIN_AGE = "//input[@id='DomainReputation_dr_sdr_child1_age']"
    DOMAIN_AGE_CONDITION = "//select[@id='DomainReputation_contain_op']"
    DOMAIN_AGE_VALUE = "//input[@id='DomainReputation_domain_age']"
    DOMAIN_AGE_UNIT = "//select[@id='DomainReputation_calendar_op']"
    DOMAIN_REPUTATION_UNSCANNABLE = "//input[@id='DomainReputation_dr_sdr_child1_noservice']"
    DOMAIN_EXTERNAL_THREATFEEDS = "//input[@id='DomainReputation_dr_parent_stix']"
    DOMAIN_EXTERNAL_THREATFEEDS_AVAILABLE_SOURCES = "//select[@id='DomainReputation_dr_stix_tf_source_names_available_dr_stix_tf_source_names']"
    DOMAIN_EXTERNAL_THREATFEEDS_SELECTED_SOURCES = "//select[@id='DomainReputation_dr_stix_tf_source_names_chosen_dr_stix_tf_source_names']"
    DOMAIN_EXTERNAL_THREATFEEDS_ADD_BUTTON = "//*[@id='error_field_DomainReputation_dr_stix_tf_source_names']//input[@value='Add >']"
    DOMAIN_EXTERNAL_THREATFEEDS_REMOVE_BUTTON = "//*[@id='error_field_DomainReputation_dr_stix_tf_source_names']//input[@value='< Remove']"
    DOMAIN_EXTERNAL_THREATFEEDS_ENVELOPE_SENDER = "//input[@id='DomainReputation_headers[]::mail-from']"
    DOMAIN_EXTERNAL_THREATFEEDS_FROM_HEADER = "//input[@id='DomainReputation_headers[]::from']"
    DOMAIN_EXTERNAL_THREATFEEDS_REPLY_TO = "//input[@id='DomainReputation_headers[]::reply-to']"
    DOMAIN_EXTERNAL_THREATFEEDS_OTHER_HEADER = "//input[@id='DomainReputation_header_other']"
    DOMAIN_EXTERNAL_THREATFEEDS_OTHER_HEADER_VALUE = "//input[@id='DomainReputation_other_header_value']"
    DOMAIN_EXCEPTION_LIST = "//select[@id='DomainReputation_domain_exception_list']"

    @classmethod
    def get_name(cls):
        return 'Domain Reputation'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: Does any URL in the message body belong to one of the selected categories
        Dictionary can contain the next items:
        | Sender Domain Reputation | <value> |
        <value> contains list of Country names to be added.
        Check Web UI to know about available country names.
        or
        | External Threat Feeds | <value> |
        <value> contains list of Country names to be removed
        or

        | Use A Domain Exception List | <value> |
        <value> contains list of Country names to be removed
        or

        *Return:*
        None

        *Examples:*|
        | ${sdr_verdict_settings} | Create Dictionary                   |
        | ... | Sender Domain Reputation Verdict | Awful to Good        |
        | ${sdr_settings} | Create Dictionary                           |
        | ... | Sender Domain Reputation | ${sdr_verdict_settings}      |

        | ${sdr_age_settings} | Create Dictionary                       |
        | ... | Sender Domain Age Condition | Less Than                 |
        | ... | Sender Domain Age Value | 7                             |
        | ... | Sender Domain Age Unit | Week(s)                        |
        | ${sdr_settings} | Create Dictionary                           |
        | ... | Sender Domain Age |  ${sdr_age_settings}                |

        | ${sdr_settings} | Create Dictionary                           |
        | ... | Sender Domain Reputaion Unscannable |  ${True}          |

        | ${conditions} | Content Filter Create Conditions              |
        | ... | Sender Domain Reputation | ${sdr_settings}              |

        | ${available_sources} | Create List | Test1 | Test2 | Test3 |
        | ${ext_threat_feeds_action} | Create Dictionary |
        | ... | Available Sources | ${available_sources} |
        | ... | Envelope Sender | ${True} |
        | ... | From Header | ${True} |
        | ... | Reply-to | ${True} |
        | ... | Other Header | Test-Header-1,Test-Header-2 |
        """
        for key, value in new_value.items():
            if key == 'Sender Domain Reputation':
                if 'Sender Domain Reputation Verdict' in value:
                    self.gui._click_radio_button(self.DOMAIN_REPUTATION_VERDICT)
                    # NotImplemented: Drag and drop of the SDR slide bar
                elif 'Sender Domain Age' in value:
                    self.gui._click_radio_button(self.DOMAIN_AGE)
                    settings = value['Sender Domain Age']
                    sdr_age_condition_map = {
                        'greater than': '>',
                        'greater than or equal to': '>=',
                        'less than': '<',
                        'less than or equal to': '<=',
                        'equal to': '==',
                        'does not equal': '!=',
                        'unknown': 'unknown',
                    }
                    sdr_age_unit_map = {
                        'days(s)': 'days',
                        'week(s)': 'weeks',
                        'month(s)': 'months',
                        'year(s)': 'years',
                    }
                    self.gui.select_from_list(self.DOMAIN_AGE_CONDITION,
                                              sdr_age_condition_map[settings[
                                                  'Sender Domain Age Condition'].lower()])
                    self.gui.input_text(self.DOMAIN_AGE_VALUE,
                                        settings['Sender Domain Age Value'])
                    self.gui.select_from_list(self.DOMAIN_AGE_UNIT,
                                              sdr_age_unit_map[settings[
                                                  'Sender Domain Age Unit'].lower()])
                elif 'Sender Domain Reputaion Unscannable' in value:
                    self.gui._click_radio_button(
                        self.DOMAIN_REPUTATION_UNSCANNABLE)
            elif key == 'External Threat Feeds':
                self.gui._click_radio_button(self.DOMAIN_EXTERNAL_THREATFEEDS)
                for source in value['Available Sources']:
                    self.gui.select_from_list(
                        self.DOMAIN_EXTERNAL_THREATFEEDS_AVAILABLE_SOURCES,
                        source)
                    self.gui.click_button(
                        self.DOMAIN_EXTERNAL_THREATFEEDS_ADD_BUTTON,
                        "don't wait")
                if 'Envelope Sender' in value:
                    if value['Envelope Sender'] is True:
                        self.gui._select_checkbox(
                            self.DOMAIN_EXTERNAL_THREATFEEDS_ENVELOPE_SENDER)
                    else:
                        self.gui._unselect_checkbox(
                            self.DOMAIN_EXTERNAL_THREATFEEDS_ENVELOPE_SENDER)
                if 'From Header' in value:
                    if value['From Header'] is True:
                        self.gui._select_checkbox(
                            self.DOMAIN_EXTERNAL_THREATFEEDS_FROM_HEADER)
                    else:
                        self.gui._unselect_checkbox(
                            self.DOMAIN_EXTERNAL_THREATFEEDS_FROM_HEADER)
                if 'Reply-to' in value:
                    if value['Reply-to'] is True:
                        self.gui._select_checkbox(
                            self.DOMAIN_EXTERNAL_THREATFEEDS_REPLY_TO)
                    else:
                        self.gui._unselect_checkbox(
                            self.DOMAIN_EXTERNAL_THREATFEEDS_REPLY_TO)
                if 'Other Header' in value:
                    if value['Other Header'] != 'None':
                        self.gui._select_checkbox(
                            self.DOMAIN_EXTERNAL_THREATFEEDS_OTHER_HEADER)
                        self.gui.input_text(
                            self.DOMAIN_EXTERNAL_THREATFEEDS_OTHER_HEADER_VALUE,
                            value['Other Header'])
                    else:
                        self.gui._unselect_checkbox(
                            self.DOMAIN_EXTERNAL_THREATFEEDS_OTHER_HEADER)
            elif key == 'Use a Domain Exception list':
                self.gui.select_from_list(self.DOMAIN_EXCEPTION_LIST,
                                          value)
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))


class SafePrintProperty(ContentFilterProperty):
    STRIP_UNSCANNABLE_ATTACHMENTS_YES = "//input[@id='Safeprint_Matching_Attachments_Action_strip_radio_yes']"
    STRIP_UNSCANNABLE_ATTACHMENTS_NO = "//input[@id='Safeprint_Matching_Attachments_Action_strip_radio_no']"
    CUSTOM_REPLACEMENT_MESSAGE = "//textarea[@id='Safeprint_Matching_Attachments_Action_custom_replacement_text']"
    ACTION_SAFEPRINT_ALL = "//input[@id='Safeprint_Matching_Attachments_Action_matching_radio_all']"
    ACTION_SAFEPRINT_MATCHING = "//input[@id='Safeprint_Matching_Attachments_Action_matching_radio_matching']"

    @classmethod
    def get_name(cls):
        return 'Safe Print'

    def set(self, new_value):
        """
        *Parameters:*
        - `new_value`: whether to enable safe print all attachments or not.
        Dictionary can contain the next items:
        | Safe Print All | <value is ignored> |

        *Examples:*
        | ${new_value}= | Create Dictionary | Safe Print All | Yes |
         """
        for key, value in new_value.items():
            if key.lower() == 'strip unscannable attachment':
                if value.lower() == 'yes':
                    self.gui._click_radio_button(self.STRIP_UNSCANNABLE_ATTACHMENTS_YES)
                elif value.lower() == 'no':
                    self.gui._click_radio_button(self.STRIP_UNSCANNABLE_ATTACHMENTS_NO)
                else:
                    raise ValueError('Unknown value "%s" is given for "%s" property.\n' \
                            'Allowed values are: Yes or No' \
                            % (value, key))
            elif key.lower() == 'custom replacement message':
                self.gui.input_text(self.CUSTOM_REPLACEMENT_MESSAGE, value)
            elif key.lower() == 'action for attachment':
                if value.lower() == 'safeprint all attachments':
                    self.gui._click_radio_button(self.ACTION_SAFEPRINT_ALL)
                elif value.lower() == 'safeprint matching attachments':
                    self.gui._click_radio_button(self.ACTION_SAFEPRINT_MATCHING)
                else:
                    raise ValueError('Unknown value "%s" is given for "%s" property.\n' \
                            'Allowed values are: "Safeprint all attachments" or ' \
                            '"Safeprint matching attachments"' % (value, key))
            else:
                handle_option_not_found_event(key, self.get_name(),
                                              inspect.getdoc(self.set))

if __name__ == '__main__':
    text = 'Is not this thing'
    val = parse_value(text, IS_NOT_COMPARISON_OP)
    print val
    print text[len(val) + 1:]

    text = 'GREATER THAN blabla '
    val = parse_value(text, NUMBER_COMPARISON_OP)
    print val
    print text[len(val) + 1:]

    text = 'GREATER THAN 234234 bytes '
    val = parse_value(text, r'(\d+)', True)
    print val
