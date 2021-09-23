#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/firefox_autodownload.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import os
import time
from common.gui.guicommon import GuiCommon


class FirefoxAutodownload(GuiCommon):
    """ Configure firefox browser to automatically download files
        of defined mime types
    """

    def get_keyword_names(self):
        return [
            'configure_autodownload_for_browser',
        ]

    def _create_autodownload_prefs_js(self, download_folder, mime_types):
        self._ff_profile.download_dir = download_folder
        self.prefs_js_path = os.path.join(self._ff_profile.directory, 'prefs.js')
        prefs_js = open(self.prefs_js_path, 'a+')

        # Generate Firefox's prefs.js.
        prefs_js.write('# Mozilla User Preferences\n')
        prefs_js.write('user_pref("browser.download.dir", "' + download_folder + '");\n')
        prefs_js.write('user_pref("browser.download.folderList", 2);\n')
        prefs_js.write('user_pref("browser.helperApps.neverAsk.saveToDisk","' + mime_types + '");\n')
        prefs_js.write('user_pref("browser.download.manager.showWhenStarting",false);\n')
        prefs_js.write('user_pref("pdfjs.disabled",true);\n')

        prefs_js.close()

    def configure_autodownload_for_browser(self, download_folder, mime_types):
        """Configures browser to proxy request through DUT by doing the
           followings:
              - stop all current running web browser.
              - stop the current running Selenium RC.
              - create a prefs.js file in existing Firefox profile directory.
              - restart Selenium RC again using the updated Firefox profile
                directory.

        Parameters:
            - `download_folder`: folder for saving downloadable files.
            - `mime_types`: A comma-separated list of MIME types to save to disk without asking what to use to open the file.

           Example:
           | Configure Autodownload For Browser | %{HOME} | text/csv |
        """
        try:
            self.close_browser()
            self._info('Delaying 5 seconds to allow Selenium RC to shutdown')
            time.sleep(5)
        except:
            pass
        self._create_autodownload_prefs_js(download_folder, mime_types)
        self._info('Delaying 5 seconds to allow Selenium RC to come up')
        time.sleep(5)
