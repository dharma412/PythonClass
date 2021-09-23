#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/content_filters_def/utils.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

import functools
import re


def go_to_filter(func):
    """Go to page defined by first decorated function's parameter.
    Can be applied only to GuiCommon descendant methods
    """
    @functools.wraps(func)
    def decorator(self, filter_type, *args, **kwargs):
        path = ('Mail Policies',)
        if filter_type.upper() == 'INCOMING':
            path += ('Incoming Content Filters',)
        elif filter_type.upper() == 'OUTGOING':
            path += ('Outgoing Content Filters',)
        else:
            raise ValueError('Unknown filter type is given ("%s")' % \
                             (filter_type,))
        self._debug('Navigating to "%s"' % (' -> '.join(path),))
        self._navigate_to(*path)

        return func(self, filter_type, *args, **kwargs)
    return decorator


def parse_value(text, possible_values, use_regexp=False):
    """Extract given value from text by comparison with regexp pattern or
    string from possible_values group

    *Parameters:*
    - `text`: text to search
    - `possible_values`: tuple of strings or regexp patterns to match with
    - `use_regexp`: whether possible_values are raw strings containing
    regexp patterns, either True or False

    *Exceptions:*
    - `ValueError`: if no match is found

    *Return:*
    matched value
    """
    if isinstance(possible_values, basestring):
        possible_values = (possible_values,)
    # Let's start search from the longest value
    values_list = list(possible_values)
    values_list = sorted(values_list, key=lambda x: len(x))
    values_list.reverse()

    for possible_value in values_list:
        if use_regexp:
            pattern = re.compile(possible_value, re.I)
            matches = pattern.search(text)
            if matches:
                return matches.group(0)
        else:
            if text.upper().find(possible_value.upper()) >= 0:
                return possible_value
    raise ValueError('Cannot find one of "%s" inside "%s"' % \
                     (possible_values, text))


def get_language_code(lang):
    """Get the code of the language to be configured
       on the GUI

    *Parameters:*
    - `lang`: language for which code needs to be returned

    *Exceptions:*
    - `ValueError`: if no match is found

    *Return:*
    matched value
    """

    if lang.lower() == 'english':
        return 'en'
    elif lang.lower() == 'spanish':
        return 'es'
    elif lang.lower() == 'german':
        return 'de'
    elif lang.lower() == 'french':
        return'fr'
    elif lang.lower() == 'italian':
        return 'it'
    elif lang.lower() == 'japanese':
        return 'ja'
    elif lang.lower() == 'korean':
        return 'ko'
    elif lang.lower() == 'portuguese':
        return 'pt'
    elif lang.lower() == 'russian':
        return 'ru'
    elif lang.lower() == 'chinese':
        return 'zh-cn'
    elif lang.lower() == 'taiwanese':
        return 'zh-tw'
    else:
        raise ValueError('Does not Match the available languages as given \
                          language type is ("%s")' % (lang,))
