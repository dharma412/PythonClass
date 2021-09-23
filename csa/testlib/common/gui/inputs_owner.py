#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/gui/inputs_owner.py#2 $
# $DateTime: 2019/09/09 11:25:44 $
# $Author: saurgup5 $

import inspect
import functools
import sys

CUSTOM_RADIO_FLAG = '<custom>'


def get_object_inputs_pairs(obj):
    """Return list of tuples declared
    inside obj, having length 2
    and whose name does not start with '_'
    """
    base_class = tuple
    return [v for k, v in inspect.getmembers(obj) \
            if isinstance(v, base_class) and (len(v) == 2) and not k.startswith('_')]


def get_module_inputs_pairs(module_name):
    """Return list of tuples declared globally
    inside module_name, having length 2
    and whose name does not start with '_'
    """
    return get_object_inputs_pairs(sys.modules[module_name])


def check_new_settings(func):
    """Decorator is applicable for InputsOwner
    method whose first parameter is new settings
    dictionary. It checks whether all keys in passed
    as first param `settings` dictionary are acceptable
    for the particular inputs owner
    """

    @functools.wraps(func)
    def decorator(self, settings, *args, **kwargs):
        self._check_if_inputs_are_registered(settings)

        return func(self, settings, *args, **kwargs)

    return decorator


class InputsOwner(object):
    """The class containing basic methods for quick
    interaction with Selenium inputs

    *Parameters:* (common)
    - `settings`: dictionary whose keys are human-readable
    control names and values are their values
    - `setting_name`: name of the setting to be set.
    In case it is not present in settings dictionary keys
    it will be ignored
    - `pairs`: multiple arguments containing 2-element tuples.
    Each tuple containing element name for RF as the first
    element and its locator as the second
    """

    def __init__(self, gui_common):
        self.gui = gui_common
        self._available_captions = set(map(lambda x: x[0], self._get_registered_inputs()))

    def _get_registered_inputs(self):
        """May return list of all inputs registered
        in this class. Each input is 2-element tuple
        containing setting caption and its locator.
        If returns non empty list then
        all setters will raise ValueError in case of
        unknown setting name
        """
        return []

    def _check_if_inputs_are_registered(self, settings):
        if not self._available_captions:
            return
        given_captions = set(settings.keys())
        if not given_captions.issubset(self._available_captions):
            raise ValueError('Unknown setting name(s) given: %s\n' \
                             'Acceptable setting names are: %s' % \
                             (list(given_captions.difference(self._available_captions)),
                              list(self._available_captions)))

    def _get_elements_values(self, getter, elements):
        details = {}
        for name, locator in elements:
            locator = self.gui._modify_locator(locator)
            if self.gui._is_element_present(locator):
                details[name] = getter(locator)
        return details

    def _get_values(self, *pairs):
        return self._get_elements_values(self.gui.get_value, pairs)

    def _get_texts(self, *pairs):
        return self._get_elements_values(self.gui.get_text, pairs)

    def _get_checkboxes(self, *pairs):
        return self._get_elements_values(self.gui._is_checked, pairs)

    def _get_radio_groups(self, *pairs):
        details = {}
        for group_name, group_items in pairs:
            for option_name, value_to_set in group_items.iteritems():
                if option_name == CUSTOM_RADIO_FLAG:
                    setter_name, getter_name, control_locator, radio_locator = \
                        value_to_set
                else:
                    radio_locator = value_to_set
                radio_locator = self.gui._modify_locator(radio_locator)
                if self.gui._is_element_present(radio_locator) and \
                        self.gui._is_checked(radio_locator):
                    if option_name == CUSTOM_RADIO_FLAG:
                        if hasattr(self, getter_name):
                            getter = getattr(self, getter_name)
                        else:
                            getter = getattr(self.gui, getter_name)
                        details[group_name] = getter(control_locator)
                    else:
                        details[group_name] = option_name
                    break
        return details

    @check_new_settings
    def _set_edit_text(self, settings, setting_name, edit_locator):
        if settings.has_key(setting_name):
            edit_locator = self.gui._modify_locator(edit_locator)
            element = self.gui._selenium.find_element_by_xpath(edit_locator)
            if self.gui._is_visible(edit_locator) and \
                    element.is_enabled() and element.is_displayed():
                if settings[setting_name]:
                    self.gui.input_text(edit_locator, settings[setting_name])

    @check_new_settings
    def _set_checkbox_state(self, settings, setting_name, cb_locator):
        if settings.has_key(setting_name):
            cb_locator = self.gui._modify_locator(cb_locator)
            self.gui._select_unselect_checkbox(cb_locator, settings[setting_name])

    @check_new_settings
    def _set_combo(self, settings, setting_name, combo_locator):
        if settings.has_key(setting_name):
            all_options = self.gui.get_list_items(combo_locator)
            all_options = [eachelement.strip() for eachelement  in all_options if eachelement]
            value_to_set = settings[setting_name]
            if value_to_set not in all_options:
                raise ValueError(
                    'Option "{selection}" not in {selections} in {list}'. \
                        format(selection=value_to_set,
                               selections=str(all_options),
                               list=setting_name))
            self.gui.select_from_list(combo_locator, value_to_set)

    @check_new_settings
    def _set_radio_group(self, settings, group_name, group_items):
        """
        *Parameters:*
        - `group_name`: radio group caption
        - `group_items`: dictionary. Items of this dictionary
        are radio buttons names and values are their locators.
        Also, this dictionary can contain key named CUSTOM_RADIO_FLAG.
        Value can is 4-items tuple containing:
        | Setter function name (selenium method or self method) |
        | Getter function name (selenium method or self method) |
        | custom control locator |
        | custom radio locator |
        """
        if settings.has_key(group_name):
            dest_option = settings[group_name]
            if dest_option in group_items.keys():
                radio_locator = group_items[dest_option]
                self.gui._click_radio_button(radio_locator)
            elif CUSTOM_RADIO_FLAG in group_items.keys():
                value_to_set = group_items[CUSTOM_RADIO_FLAG]
                radio_locator = None
                if isinstance(value_to_set, list) or \
                        isinstance(value_to_set, tuple):
                    if len(value_to_set) == 4:
                        setter_name, getter_name, control_locator, radio_locator = \
                            value_to_set
                    else:
                        raise RuntimeError('Incorrect definition of "%s" radiogroup ' \
                                           'detected' % (group_name,))
                if radio_locator:
                    self.gui._click_radio_button(radio_locator)
                if hasattr(self, setter_name):
                    setter = getattr(self, setter_name)
                else:
                    setter = getattr(self.gui, setter_name)
                setter(control_locator, dest_option)
            else:
                raise ValueError('There is no option named "%s" ' \
                                 'in radio group "%s"' % (dest_option, group_name))

    def _set_edits(self, settings, *pairs):
        for caption, locator in pairs:
            self._set_edit_text(settings, caption, locator)

    def _set_dual_list(self, settings, name, locator, button):
        if settings.has_key(name):
            all_options = self.gui.get_list_items(locator)
            values = settings[name]
            for value in values:
                if value not in all_options:
                    raise ValueError(
                        'Option "{selection}" not in {selections} in {list}'. \
                            format(selection=value,
                                   selections=str(all_options),
                                   list=name))
                self.gui.select_from_list(locator, value)
            self.gui.click_button(button, "don't wait")

        else:
            raise ValueError('Settings {settings} does not have key {name}'. \
                             format(settings=settings, name=name))

    def _set_checkboxes(self, settings, *pairs):
        for caption, locator in pairs:
            self._set_checkbox_state(settings, caption, locator)

    def _set_combos(self, settings, *pairs):
        for caption, locator in pairs:
            self._set_combo(settings, caption, locator)

    def _set_dual_lists(self, settings, button, *pairs):
        for caption, locator in pairs:
            self._set_dual_list(settings, caption, locator, button)

    def _set_radio_groups(self, settings, *pairs):
        for group_name, group_items in pairs:
            self._set_radio_group(settings, group_name, group_items)
