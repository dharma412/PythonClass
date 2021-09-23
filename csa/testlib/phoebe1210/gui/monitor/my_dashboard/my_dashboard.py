#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/monitor/my_dashboard/my_dashboard.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon

from my_dashboard_def.dashboard_widgets_container import DashboardWidgetsContainer

PAGE_PATH = ('Monitor', 'My Dashboard')


class MyDashboard(GuiCommon):
    """Keywords for interaction with Monitor -> My Dashboard's ESA GUI page"""

    DASHBOARD_CONTAINERS = {}

    def get_keyword_names(self):
        return ['my_dashboard_add',
                'my_dashboard_delete',
                'my_dashboard_report_exist',
                'my_dashboard_get_all']

    def _get_container(self, caption):
        if caption not in self.DASHBOARD_CONTAINERS:
            self.DASHBOARD_CONTAINERS[caption] = \
                DashboardWidgetsContainer.create_instance(self, caption)
        return self.DASHBOARD_CONTAINERS[caption]

    @go_to_page(PAGE_PATH)
    def my_dashboard_add(self, container_caption, report_caption,
                         from_page=None):
        """Add new report to personal dashboard. Changes are applied immediately
        for currently logged account.

        *Parameters:*
        - `container_caption`: container name. Available container names are:
        | System Overview |
        | General |
        | Time Range |
        - `report_caption`: report name to be added. Available report names
        for different containers are (format and letter case should be kept):
        | *Report Caption* | *Available In Container* |
        | Status | System Overview |
        | Quarantines - Top 3 by Disk Usage (Policy and Virus) | System Overview |
        | Threat Level | System Overview |
        | Mail System Status | System Overview |
        | Version Information | System Overview |
        | Sender Details | General |
        | Gauges | General |
        | Rates (Events per Hour) | General |
        | Counters | General |
        | Incoming Mail Graph | Time Range |
        | Outgoing Mail Graph | Time Range |
        | Incoming Mail Summary | Time Range |
        | Outgoing Mail Summary | Time Range |
        | Top Senders by Total Threat Messages | Time Range |
        | Top Senders by Clean Messages | Time Range |
        | Incoming Mail Details | Time Range |
        | Top Destinations by Total Threat Messages | Time Range |
        | Top Destinations by Clean Messages | Time Range |
        | Outgoing Destinations Detail | Time Range |
        | Top Senders by Total Threat Messages | Time Range |
        | Top Senders by Clean Messages | Time Range |
        | Sender Details | Time Range |
        | Top Users by Clean Incoming Messages | Time Range |
        | Top Users by Clean Outgoing Messages | Time Range |
        | User Mail Flow Details | Time Range |
        | Top Incoming Content Filter Matches | Time Range |
        | Top Outgoing Content Filter Matches | Time Range |
        | Incoming Content Filter Matches | Time Range |
        | Outgoing Content Filter Matches | Time Range |
        | Threats by Type | Time Range |
        | Threat Summary | Time Range |
        | Threat Details | Time Range |
        | Top Incoming Virus Types Detected | Time Range |
        | Top Outgoing Virus Types Detected | Time Range |
        | Virus Types Detail | Time Range |
        | Incoming TLS Connections Graph | Time Range |
        | Incoming TLS Connections Summary | Time Range |
        | Incoming TLS Messages Summary | Time Range |
        | Incoming TLS Connections Details | Time Range |
        | Outgoing TLS Connections Graph | Time Range |
        | Outgoing TLS Connections Summary | Time Range |
        | Outgoing TLS Messages Summary | Time Range |
        | Outgoing TLS Connections Details | Time Range |
        | Received Connections | Time Range |
        | Received Recipients | Time Range |
        | SMTP Authentication Details By Domain Name | Time Range |
        | Top Offenders by Incident | Time Range |
        | Top Offenders by Rejected Recipients | Time Range |
        | Average Time Spent in Work Queue | Time Range |
        | Average Messages in Work Queue | Time Range |
        | Maximum Messages in Work Queue | Time Range |
        - `from_page`: page name as it is spelled in Monitor submenu. This parameter
        is required only if you want to add report from some particular page instead
        of 'My Dashboard' one. Make sure this report you want to add really
        exists on this page, otherwise you'll get ValueError exception.

        *Exceptions:*
        - `ConfigError`: if report with given caption already exist in the container
        - `ValueError`: if container or report name is unknown

        *Examples:*
        | @{VERIFICATION_DATA}= | Create List |
        | ... | System Overview | Version Information |
        | ... | General | Gauges |
        | ... | Time Range | Threats by Type |
        | :FOR | ${container_caption} | ${report_caption} | IN | @{VERIFICATION_DATA} |
        | \ | ${is_report_already_present}= | My Dashboard Report Exist |
        | \ | ... | ${container_caption} | ${report_caption} |
        | \ | Run Keyword If | not ${is_report_already_present} |
        | \ | ... | My Dashboard Add | ${container_caption} | ${report_caption} |
        """
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
    def my_dashboard_report_exist(self, container_caption, report_caption):
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

    @go_to_page(PAGE_PATH)
    def my_dashboard_get_all(self, container_caption):
        """Return all reports currently added to the particular container

        *Parameters:*
        - `container_caption`: container name.
        See `My Dashboard Add` keyword description for possible values list.

        *Return:*
        List of objects. Each object has *caption* property containing report caption
        and *full_caption* property containing report caption with category prefix.
        See `My Dashboard Add` keyword description for possible values list.
        Empty list will be returned in case when container does not contain any reports.

        *Examples:*
        | @{all_reports}= | My Dashboard Get All | ${container_caption} |
        | :FOR | ${report_obj} | IN | @{all_reports} |
        | \ | Log | Found report "${report_obj.caption}" (full name: "${report_obj.full_caption}") |
        """
        dest_container = self._get_container(container_caption)
        return dest_container.get_all_widgets()
