#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/range_request_download.py#1 $

from common.cli.clicommon import CliKeywordBase

class RangeRequestDownload(CliKeywordBase):
    """Change the proxy's policy for allowing range requests to the
    destination server.
    """

    def get_keyword_names(self):
        return [
            'range_request_download',
        ]

    def range_request_download(self, answer='yes'):
        """This keyword toggles the proxy's policy for allowing range requests
        to the destination server.

        Parameters:
        - `answer`: answer to the confirmation question. Either 'yes' or 'no'.
        Default 'yes'.

        NOTE: If this option is disabled (default) then the proxy will not pass
        along any Range Request headers to the destination server if the
        responses need to be scanned. The result of which is that the full
        object will be retrieved and, if required by the web access
        policies, scanned for malware.

        If this option is enabled then the proxy will pass along any Range
        Request headers to the destination server. The partial content
        retrieved will be bypassed from all response body scanning. In
        particular, the following access policies (components) will not be
        applicable:
        - mcafee/webroot scanning
        - mime-type detection and object blocking based on mime-type
        - blocking an object based on file size
        As a result, setting this option to enabled introduces
        a vulnerability that may allow malware to slip through undetected.

        Examples:
        | Range Request Download | answer=no |

        | Range Request Download |
        """

        self._cli.rangerequestdownload(answer)
