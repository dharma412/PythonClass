#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/get_html_source.py#1 $

from common.gui.guicommon import GuiCommon


class GetHtmlSource(GuiCommon):
    """Get HTML source of the browser's page
    """

    def get_keyword_names(self):
        return [
            "get_html_source",
        ]

    def get_html_source(self):
        """ Returns HTML source of the browser's page.

        That info can be then used to investigate the failures

        Parameters: None

        Examples:
        | | TimeZone Edit       Europe  United Kingdom  London |
        | | ${code}= | Get HTML Source |
        | | Log | ${code} |

        """
        return self._selenium.get_html_source()
