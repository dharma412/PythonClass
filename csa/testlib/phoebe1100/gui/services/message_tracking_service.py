#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/services/message_tracking_service.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.guicommon import GuiCommon

TRACK_RADIOBUTTON = {'local': 'id=centralized_tracking_enabled_0',
                     'centralized': 'id=centralized_tracking_enabled_1'}
ENABLE_BUTTON = 'name=action:FormEditTracking'
ENABLE_CHECKBOX = 'id=master_tracking_enabled'
TRACK_CONN_CHECKBOX = 'id=track_connections'
SERVICE_DISABLED_FLAG = '//table[@class="pairs"]//td[@class="text-info"]'


class MessageTrackingService(GuiCommon):
    """Keywords are used to disable/enable
     Email Message Tracking Service and to edit
     its settings
    """

    def get_keyword_names(self):
        return ['message_tracking_enable',
                'message_tracking_disable',
                'message_tracking_is_enabled',
                'message_tracking_edit_settings']

    def _open_page(self):
        self._debug('Opening Message Tracking Service page')
        self._navigate_to('Security Services', "Message Tracking")

    def message_tracking_enable(self,
                                tracking=None,
                                track_info_for_rej_conn=None):
        """Enable Message Tracking Service

        Parameters:
         - tracking: Message Tracking Service Status.
        Acceptable values are 'local' or 'centralized'
         - track_info_for_rej_conn: Rejected Connection Handling.
        Acceptable values are ${True} or ${False}
        """
        self._info('Enabling Message Tracking Service')
        if self.message_tracking_is_enabled():
            self.info('Message Tracking Service is already enabled')
            return
        self.click_button(ENABLE_BUTTON)
        self._select_checkbox(ENABLE_CHECKBOX)
        self._edit_settings(tracking,
                            track_info_for_rej_conn)

    def message_tracking_disable(self):
        """Disable Message Tracking Service
        """
        self._info('Disabling Message Tracking Service')
        if not self.message_tracking_is_enabled():
            self.info('Message Tracking Service is already disabled')
            return
        self.click_button(ENABLE_BUTTON)
        self._unselect_checkbox(ENABLE_CHECKBOX)
        self._click_submit_button()

    def message_tracking_is_enabled(self):
        """Check whether Email Message Tracking Service
        is enabled

        Return:
            Boolean True or False
        """
        self._info('Checking if Message Tracking Service is enabled')
        self._open_page()
        return not self._is_element_present(SERVICE_DISABLED_FLAG)

    def message_tracking_edit_settings(self,
                                       tracking=None,
                                       track_info_for_rej_conn=None):
        """Edit Message Tracking Service settings

        Parameters:
         - tracking: Message Tracking Service Status.
        Acceptable values are 'local' or 'centralized'
         - track_info_for_rej_conn: Rejected Connection Handling.
        Acceptable values are ${True} or ${False}
        """
        self._info("Editing Message Tracking Service settings")
        self._open_page()
        self.click_button(ENABLE_BUTTON)
        self._edit_settings(tracking,
                            track_info_for_rej_conn)

    def _edit_settings(self,
                       tracking,
                       track_info_for_rej_conn):
        if tracking is not None:
            tracking = tracking.lower()
            self._click_radio_button(TRACK_RADIOBUTTON[tracking])
        if track_info_for_rej_conn is not None:
            if bool(track_info_for_rej_conn):
                self._select_checkbox(TRACK_CONN_CHECKBOX)
            else:
                self._unselect_checkbox(TRACK_CONN_CHECKBOX)
        self._click_submit_button()
