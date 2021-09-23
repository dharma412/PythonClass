#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/email/reporting/my_dashboard.py#1 $
# $DateTime: 2020/05/25 00:19:30 $
# $Author: sarukakk $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon

from my_dashboard_def.dashboard_widgets_container import DashboardWidgetsContainer


PAGE_PATH = ('Email', 'Reporting', 'My Reports')


class MyReport(GuiCommon):
    """Keywords for interaction with Email-> Reporting-> My Reports -> My Dashboard's SMA GUI page"""

    DASHBOARD_CONTAINERS = {}

    def get_keyword_names(self):
        return ['my_dashboard_reports_add',
                'my_dashboard_delete',
                'my_dashboard_report_exists']

    def _get_container(self, caption):
        if caption not in self.DASHBOARD_CONTAINERS:
            self.DASHBOARD_CONTAINERS[caption] = \
                    DashboardWidgetsContainer.create_instance(self, caption)
        return self.DASHBOARD_CONTAINERS[caption]

    @go_to_page(PAGE_PATH)
    def my_dashboard_reports_add(self, container_caption, report_caption,
                       from_page=None):
        dest_container = self._get_container(container_caption)
        dest_container.add_widget(report_caption, from_page)

    @go_to_page(PAGE_PATH)
    def my_dashboard_delete(self, container_caption, report_caption):
        """Delete existing report from My Dashboard tab. Changes are applied immediately
        for currently logged account.

        *Parameters:*
        - `container_caption`: container name.
        See `My Dashboard Add` keyword description for possible values list.
        - `report_caption`: report name to be deleted.
        See `My Dashboard Add` keyword description for possible values list.

        *Exceptions:*
        - `ValueError`: if container or report name is unknown or the report
        does not exist in cantainer

        *Examples:*
        | My Dashboard Delete | ${container_caption} | ${report_caption} |
        """
        dest_container = self._get_container(container_caption)
        dest_container.delete_widget(report_caption)

    @go_to_page(PAGE_PATH)
    def my_dashboard_report_exists(self, container_caption, report_caption):
        """Check whether report with given name exists in container.

        *Parameters:*
        - `container_caption`: container name.
        See `My Dashboard Add` keyword description for possible values list.
        - `report_caption`: report name to be deleted.
        See `My Dashboard Add` keyword description for possible values list.

        *Return:*
        ${True} or ${False}

        *Examples:*
        | Verify ${report_caption} report ${is_isnot} present in ${container_caption} |
        |  | ${verifier_kw}= | Set Variable If | '${is_isnot}'.lower() == 'is' |
        |  | ... | Should Be True | Should Not Be True |
        |  | ${is_exist}= | My Dashboard Report Exist | ${container_caption} | ${report_caption} |
        |  | Run Keyword | ${verifier_kw} | ${is_exist} |
        """
        dest_container = self._get_container(container_caption)
        return dest_container.is_widget_exist(report_caption)

