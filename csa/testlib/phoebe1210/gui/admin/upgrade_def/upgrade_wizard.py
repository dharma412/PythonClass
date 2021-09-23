#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/admin/upgrade_def/upgrade_wizard.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author

from common.gui.inputs_owner import InputsOwner
from common.gui.decorators import set_speed
from common.gui.guiexceptions import ConfigError

from wizard_pages import InitialOptionsPage, UpgradeDownloadedOptionsPage, \
    UpgradeProgressPage, DowloadProgressPage, \
    INSTALL_OPERATION, DOWNLOAD_AND_INSTALL_OPERATION, \
    DOWNLOAD_ONLY_OPERATION, get_asyncos_upgrades_map, \
    OPERATIONS_KEY, UPGRADE_FILE_KEY, DELETE_FILE_BUTTON


class SystemUpgradeWizard(InputsOwner):
    ALL_PAGES = (InitialOptionsPage, UpgradeDownloadedOptionsPage,
                 UpgradeProgressPage, DowloadProgressPage)

    def _extract_page_settings(self, all_settings, page_obj):
        page_inputs = dict(page_obj.get_registered_inputs())
        result = {}
        for name, value in all_settings.iteritems():
            if name in page_inputs:
                result[name] = value
        return result

    def _get_pages(self, settings):
        assert (OPERATIONS_KEY in settings)
        operation = settings[OPERATIONS_KEY]

        page_classes = None
        if self.gui._is_element_present(DELETE_FILE_BUTTON):
            if operation in (INSTALL_OPERATION, DOWNLOAD_AND_INSTALL_OPERATION):
                page_classes = [UpgradeDownloadedOptionsPage, UpgradeProgressPage]
            elif operation == DOWNLOAD_ONLY_OPERATION:
                page_classes = [UpgradeDownloadedOptionsPage, DowloadProgressPage]
        else:
            if operation == INSTALL_OPERATION:
                raise ConfigError('There are no upgrade downloaded and ' \
                                  'ready for install')
            elif operation == DOWNLOAD_AND_INSTALL_OPERATION:
                page_classes = [InitialOptionsPage, UpgradeProgressPage]
            elif operation == DOWNLOAD_ONLY_OPERATION:
                page_classes = [InitialOptionsPage, DowloadProgressPage]
        if page_classes is None:
            raise ValueError('Incorrect value "%s" is set for "%s" option. ' \
                             'Acceptable values are: %s' % (operation,
                                                            InitialOptionsPage.UPGRADE_OPERATION_RADIOGROUP[0],
                                                            (INSTALL_OPERATION, DOWNLOAD_AND_INSTALL_OPERATION, \
                                                             DOWNLOAD_ONLY_OPERATION)))
        else:
            return page_classes

    @set_speed(0, 'gui')
    def set(self, new_value):
        unused_settings = set(new_value.keys())
        for page_class in self._get_pages(new_value):
            page = page_class(self.gui)
            page_settings = self._extract_page_settings(new_value, page)
            unused_settings -= set(page_settings.keys())
            page.set(page_settings)
            page.next()
        if len(unused_settings) > 0:
            raise ValueError('Unknown "%s" key(s) are present in upgrade ' \
                             'settings.' % (list(unused_settings),))

    @set_speed(0, 'gui')
    def delete_current_upgrade(self):
        if self.gui._is_element_present(DELETE_FILE_BUTTON):
            dest_page = UpgradeDownloadedOptionsPage(self.gui)
            dest_page.delete_ugrade()
        else:
            raise ConfigError('There are no downloaded upgrades available')

    @set_speed(0, 'gui')
    def get_available_upgrades(self, only_versions=False):
        page = InitialOptionsPage(self.gui)
        all_names = page.get()[UPGRADE_FILE_KEY]
        if only_versions:
            return get_asyncos_upgrades_map(all_names).keys()
        else:
            return all_names
