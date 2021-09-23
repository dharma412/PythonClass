#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/management/services/pvo_quarantines_def/migration_wizard.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner
from wizard_pages import PVOMigrationModePage, PVOMigrationAutomaticPage, \
                                             PVOMigrationCustomPage, PVOMigrationFinalPage, \
                                             WIZARD_MODE_CUSTOM, WIZARD_MODE_AUTOMATIC, \
                                             WIZARD_MODE_KEY


LAUNCH_WIZARD_BUTTON = \
     "//input[@type='button' and contains(@value, 'Launch Migration Wizard...')]"


class PVOMigrationWizard(InputsOwner):
    PAGES = { WIZARD_MODE_CUSTOM: (PVOMigrationModePage,
                                   PVOMigrationCustomPage,
                                   PVOMigrationFinalPage),
            WIZARD_MODE_AUTOMATIC: (PVOMigrationModePage,
                                    PVOMigrationAutomaticPage,
                                    PVOMigrationFinalPage) }

    @set_speed(0, 'gui')
    def set(self, settings):
        available_settings_captions = set(settings.keys())
        if WIZARD_MODE_KEY in settings and \
           settings[WIZARD_MODE_KEY] == WIZARD_MODE_CUSTOM:
            wizard_pages = self.PAGES[WIZARD_MODE_CUSTOM]
        else:
            wizard_pages = self.PAGES[WIZARD_MODE_AUTOMATIC]
        for page_class in wizard_pages:
            page_settings = {}
            page_controller = page_class(self.gui)
            registered_input_names = map(lambda x: \
                                x[0], page_controller.registered_inputs())
            for key, value in settings.iteritems():
                if key in registered_input_names:
                    page_settings[key] = value
            available_settings_captions = available_settings_captions - \
                                          set(page_settings.keys())
            page_controller.set(page_settings)
            page_controller.go_to_next()
        if len(available_settings_captions) > 0:
            # some settings were not used
            raise ValueError('Incorrect setting name(s) %s passed.\nAvailable setting'\
                             ' names are: %s' % (list(available_settings_captions),
                                                 settings.keys()))

