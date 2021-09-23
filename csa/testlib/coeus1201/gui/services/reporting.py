#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/reporting.py#1 $
from common.gui.guicommon import GuiCommon

class Reporting(GuiCommon):
    """Keywords for Security Services -> Reporting
    """

    def get_keyword_names(self):
        return [
                'reporting_edit',
                'reporting_get_settings',
               ]

    def _open_page(self):
        """
       Navigate to Reporting configuration page.
        """
        self._navigate_to("Security Services", \
             "xpath=//a[text()='Reporting'" +
             " and contains(@href, 'centralized_web_reporting')]")

    def reporting_edit(self, type, anonymous=None):
        """Edit reporting settings.

        Parameters:
        - `type`: reporting type: "local" or "center"
        - `anonymous`: Anonymize usernames in reports: True or False;
           that parameter is applicable only for local reporting

        Examples:
        | Reporting Edit | local | anonymous=${True} |
        | Reporting Edit | local | anonymous=${False} |
        | Reporting Edit | local |
        | Reporting Edit | center |

        Exceptions:
        - `ValueError`: in case `type`'s value is not set as expected.

        """
        self._info('Editing reporting settings.')
        self._open_page()
        self._click_edit_settings_button()

        self._set_options(type, anonymous)

        if type == "local":
            self._click_submit_button()
        else:
            self._click_submit_button(accept_confirm_dialog=True, wait=False)

    def reporting_get_settings(self):
        """Get Reporting Settings.

        Parameters:
            None.

        Return:
            Dictionary keys of which are names of settings.

        Example:
        | ${result} | Reporting Get Settings |
        """
        name_locator = "//table[@class='pairs']/tbody/tr[1]/th[1]"
        value_locator = "//table[@class='pairs']/tbody/tr[1]/td[1]"
        self._open_page()
        entries = {}
        entries[self.get_text(name_locator)] = \
                   self.get_text(value_locator)
        return entries

    def _set_options(self, type, anonymous):
        ANONYMOUS_BUTTON="anonymyzing_enabled"

        TYPES={
               "local":"local_reporting",
               "center":"centralized_reporting"
        }
        if not TYPES.has_key(type):
            raise ValueError, "type %s is not supported; should be in $s" \
                % (type, str(TYPES.keys()))

        self._click_radio_button(TYPES[type])

        if type == "local":
            if anonymous is not None:
                if anonymous:
                    self.select_checkbox(ANONYMOUS_BUTTON)
                else:
                    self.unselect_checkbox(ANONYMOUS_BUTTON)
