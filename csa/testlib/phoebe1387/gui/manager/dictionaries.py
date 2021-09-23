#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/dictionaries.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import re
import time

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions


IMPORT_BUTTON = '//input[@value=\'Import Dictionary...\']'
SERVER_RB = '//input[@id=\'import_server\']'
FILE_SELECT = '//select[@name=\'file_server\']'
ENC_SELECT = '//select[@name=\'encoding\']'
WEIGHT_SELECT = '//select[@name=\'default_weight\']'
NEXT_BUTTON = '//input[@class=\'submit\']'
DICT_TABLE = "//table[@class='cols']/tbody"
TERMS_TABLE = '//div[@id=\'terms_editor\']/div[3]/table/tbody[2]'
NAME_TEXT_BOX = '//input[@name=\'id\']'
WHOLEWORDS = '//input[@id=\'wholewords\']'
IGNORECASE = '//input[@id=\'ignorecase\']'

PAGE_PATH = ('Mail Policies', 'Dictionaries')


class Dictionaries(GuiCommon):
    """Interaction class for ESA WUI
       Mail Policies -> Dictionaries page.
    """

    def get_keyword_names(self):
        return ['dictionaries_import_external',
                'dictionaries_import_internal' ,
                'dictionaries_get_info']

    @go_to_page(PAGE_PATH)
    def dictionaries_import_external(self,
                                filename,
                                weight=None,
                                encoding=None):
        """Import dictionary from local computer to be used on ESA.
        Content dictionaries are groups of words or entries that
        work in conjunction with the Body Scanning feature on the
        appliance and are available to both content and message filters.
        Use the dictionaries you define to scan messages, message headers,
        and message attachments for terms included in the dictionary in order
        to take appropriate action in accordance with your corporate policies.
        For example, you could create a list of confidential or profane words,
        and, using a filter rule to scan messages that contain words in the list,
        drop, archive, or quarantine the message.

        *Parameters:*
        - `filename`: path to file on local computer to be used as dictionary
        - `weight`: when AsyncOS scans messages for the content dictionary terms,
        it "scores" the message by multiplying the number of term instances by the
        weight of term. Two instances of a term with a weight of three would result
        in a score of six. AsyncOS then compares this score with a threshold value
        associated with the content or message filter to determine if the message
        should trigger the filter action. Acceptable values are numbers
        in range 0..10
        - `encoding`: in some languages (double-byte character sets), the concepts
        of a word or word boundary, or case do not exist. Complex regular expressions
        that depend on concepts like what is or is not a character that would compose
        a word (represented as "\w" in regex syntax) cause problems when the locale is
        unknown or if the encoding is not known for certain. For that reason, you may
        want to disable word-boundary enforcement. Acceptable values are:
        | US-ASCII |
        | Unicode (UTF-8) |
        | Unicode (UTF-16) |
        | Western European/Latin-1 (ISO 8859-1) |
        | Western European/Latin-1 (Windows CP1252) |
        | Traditional Chinese (Big 5) |
        | Simplified Chinese (GB 2312) |
        | Simplified Chinese (HZ GB 2312) |
        | Korean (ISO 2022-KR) |
        | Korean (KS-C-5601/EUC-KR) |
        | Japanese (Shift-JIS (X0123)) |
        | Japanese (ISO-2022-JP) |
        | Japanese (EUC) |

        *Examples:*
        | Dictionaries Import External | ~/dict.txt | 0 | Unicode (UTF-8) |
        """
        raise NotImplementedError()

    @go_to_page(PAGE_PATH)
    def dictionaries_import_internal(self,
                              filename,
                              weight=None,
                              encoding=None):
        """Import one one of predefined dictionaries to be used on ESA.
        Content dictionaries are groups of words or entries that
        work in conjunction with the Body Scanning feature on the
        appliance and are available to both content and message filters.
        Use the dictionaries you define to scan messages, message headers,
        and message attachments for terms included in the dictionary in order
        to take appropriate action in accordance with your corporate policies.
        For example, you could create a list of confidential or profane words,
        and, using a filter rule to scan messages that contain words in the list,
        drop, archive, or quarantine the message.

        *Parameters:*
        - `filename`: path to one of predefined dictionaries on appliance
        - `weight`: when AsyncOS scans messages for the content dictionary terms,
        it "scores" the message by multiplying the number of term instances by the
        weight of term. Two instances of a term with a weight of three would result
        in a score of six. AsyncOS then compares this score with a threshold value
        associated with the content or message filter to determine if the message
        should trigger the filter action. Acceptable values are numbers
        in range 0..10
        - `encoding`: in some languages (double-byte character sets), the concepts
        of a word or word boundary, or case do not exist. Complex regular expressions
        that depend on concepts like what is or is not a character that would compose
        a word (represented as "\w" in regex syntax) cause problems when the locale is
        unknown or if the encoding is not known for certain. For that reason, you may
        want to disable word-boundary enforcement. Acceptable values are:
        | US-ASCII |
        | Unicode (UTF-8) |
        | Unicode (UTF-16) |
        | Western European/Latin-1 (ISO 8859-1) |
        | Western European/Latin-1 (Windows CP1252) |
        | Traditional Chinese (Big 5) |
        | Simplified Chinese (GB 2312) |
        | Simplified Chinese (HZ GB 2312) |
        | Korean (ISO 2022-KR) |
        | Korean (KS-C-5601/EUC-KR) |
        | Japanese (Shift-JIS (X0123)) |
        | Japanese (ISO-2022-JP) |
        | Japanese (EUC) |

        *Exceptions:*
        - `ValueError`: if given filename does not exist on appliance

        *Examples:*
        | Dictionaries Import Internal | proprietary_content.txt | 2 | US-ASCII |
        """
        self.click_button(IMPORT_BUTTON)
        if filename not in self._get_available_options_from_select(FILE_SELECT):
            raise ValueError("%s is not available on ESA" % (filename,))
        self._select_checkbox(SERVER_RB)
        self.select_from_list(FILE_SELECT, filename)
        if weight:
            self.select_from_list(WEIGHT_SELECT, weight)
        if encoding:
            self._select_encoding(encoding)
        self.click_button(NEXT_BUTTON)
        self._wait_until_element_is_present(NEXT_BUTTON, timeout=10)
        self.click_button(NEXT_BUTTON)

    @go_to_page(PAGE_PATH)
    def dictionaries_get_info(self):
        """Get information about existing dictionaries.

        *Return:*
        List of DictContainer objects. Each object contains the next fields:
        | name | Dictionary name |
        | match_whole_words | whether whole words matching is enabled,
        either True or false |
        | case_sensitive | whether dictionary search is case sensitive,
        either True or false  |
        | smart_identifiers | dictionary with smart identifiers |
        | words | dictionary whose keys are words and values are weights |

        *Examples:*
        | @{dicts}= | Dictionaries Get Info |
        | :FOR | ${dict} | IN | @{dicts} |
        |      | Log | ${dict.name} |
        """
        time.sleep(2)
        rows = int(self.get_matching_xpath_count("%s/tr" % DICT_TABLE))
        dictionary_list = []
        for row in range(2, rows + 1):
            link = "%s/tr[%d]/td/a", (DICT_TABLE,row)
            self.click_button("%s/tr[%d]/td/a" % (DICT_TABLE, row))
            dictionary_list.append(self._get_info())
            self.click_button(NEXT_BUTTON)
        return dictionary_list

    def _get_info(self):
        term_locator = lambda row:"%s/tr[%d]/td/div" % (TERMS_TABLE, row)
        weight_locator = lambda row:"%s/tr[%d]/td[2]/div" % (TERMS_TABLE, row)
        checkbox = lambda id:'sid_%s' % id
        weight = lambda id:'sid_%s_weight' % id
        dict_info = DictContainer()
        dict_info.name = self.get_value(NAME_TEXT_BOX)
        dict_info.match_whole_words = self._is_checked(WHOLEWORDS)
        dict_info.case_sensitive = self._is_checked(IGNORECASE)

        for identifier in ['cc', 'ssn', 'aba', 'cusip']:
            if self._is_checked(checkbox(identifier)):
               dict_info.smart_identifiers[identifier] = \
                    self.get_value(weight(identifier))

        rows = int(self.get_matching_xpath_count("%s/tr" % TERMS_TABLE))
        for row in range(2, rows + 1):
            word = self.get_text(term_locator(row))
            wt = self.get_text(weight_locator(row))
            dict_info.words[word] = int(wt)
        return dict_info

    def _select_encoding(self, encoding):
        encoding_list = self._get_available_options_from_select(ENC_SELECT)
        for enc in encoding_list:
            if enc.find(encoding.upper()) != -1:
                self.select_from_list(ENC_SELECT, enc)


class DictContainer(object):
    def __init__(self):
        self.name = None
        self.match_whole_words = False
        self.case_sensitive = False
        self.smart_identifiers = {}
        self.words = {}

