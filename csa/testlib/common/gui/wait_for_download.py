#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/wait_for_download.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import os
import re
import time
from common.gui.guicommon import GuiCommon


class WaitForDownload(GuiCommon):
    """Waiting for file downloading
    """

    def get_keyword_names(self):
        return [
            'wait_for_download',
        ]

    def _get_filemtime(self, file):
        filetimesecs = 0
        try:
            filetimesecs = os.path.getmtime(file)
        except:
            pass
        return filetimesecs

    def wait_for_download(self, filename, start_time=None, timeout=600, download_directory=None):
        """Waiting for file downloading.

        Parameters:
            - `filename`: a part of a filename, which is downloaded by firefox.
            - `start_time`: start time of downloading (with format: "%Y-%m-%d %H:%M:%S").
            If this parameter is missed, files, which downloading was started
            1 minute ago, are searched.
            - `timeout`: timeout for downloading. Default timeout is 10 minutes.
            - `download_directory`: download directory.

        Return:
        Location (path with filename) of downloaded file.

        Example:
           | Configure Autodownload For Browser | ${TEMPDIR} | application/pdf |
           | Launch DUT Browser |
           | Log Into DUT |
           | ${start_time}= | Get Time |
           | Navigate To | Management Appliance | Centralized Services | System Status |
           | Click Link | Printable (PDF) | don't wait |
           | ${saved_pdf}= | Wait For Download | system_status | start_time=${start_time} | timeout=60 |
        """

        filename = re.sub("\W", "_", filename)
        filename = re.sub("_+", "_", filename)
        filename = filename.strip("_")
        self._debug("filename: %s" % filename)

        if start_time is None:
            start_time = time.time() - 60
        else:
            start_time = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))

        self._debug("start_time: %s" % start_time)
        if download_directory is None:
            _download_dir = self._ff_profile.download_dir
        else:
            _download_dir = download_directory
        self._debug("_download_dir: %s" % _download_dir)

        _downloaded = False

        _timer_start = time.time()
        while (time.time() - _timer_start) < int(timeout):
            files = [f for f in os.listdir(_download_dir) if (f.find(filename) > -1)]
            for file in files:
                full_name = os.path.join(_download_dir, file)
                self._debug("file: %s" % file)
                filetimesecs = self._get_filemtime(full_name)
                self._debug("filetimesecs: %s" % filetimesecs)
                if filetimesecs >= start_time:
                    _downloaded = (file.find(".part") < 0)
                    if _downloaded:
                        return full_name
                    else:
                        break
            time.sleep(3)

        raise ValueError("Download of %s file was not finished successfully." % filename)
