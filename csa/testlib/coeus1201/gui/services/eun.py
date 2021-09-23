# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/eun.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ACK_CHECKBOX = "enable_splash_page"
VOLUME_QUOTA = "eun_volume_limit_enabled"
TIME_QUOTA = "eun_time_limit_enabled"

class EUN(GuiCommon):
    """
    Keywords for Security Services -> End-User Notification
    """

    def get_keyword_names(self):
        return [
                "eun_edit_settings",
                "eun_get_settings",
               ]

    def eun_edit_settings(self,
        http_language=None,
        logo=None,
        ack_enable=None,
        ack_time_between=None,
        ack_timeout=None,
        ack_msg=None,
        notification_type=None,
        notification_url=None,
        notification_msg=None,
        notification_contact=None,
        notification_email=None,
        notify_misclassification=None,
        url_cat_time_between=None,
        url_cat_msg=None,
        quota_time_enable=None,
        quota_volume_enable=None,
        quota_time=None,
        quota_volume=None,
        nativeftp_language=None,
        nativeftp_msg=None):

        """Edit End-User Notification.

        Parameters:
        - `http_language`: language to use for HTTP/HTTPS transactions
        - `logo`: specify whether an image can be displayed by the web browser
           as part of every notification and acknowledgement page.
           Possible values:
           * "No Image" - image will not be displayed
           * "Use Cisco IronPort Logo" - Cisco IronPort Logo will be displayed
           * <custom logo starting with http or https>
        - `ack_enable`: True to require end-user to click through
           acknowledgement page
        - `ack_time_between`: time between acknowledgements,
           must be 30 to 2678400 seconds, or use trailing s for
           seconds, m for minutes, h for hours
           (examples: 120s, 5m 30s, 4h)
        - `ack_timeout`: inactivity timeout,
           must be 30 to 2678400 seconds, or use trailing s for
           seconds, m for minutes, h for hours
           (examples: 120s, 5m 30s, 4h)
        - `ack_msg`: Specify additional text to be displayed on every
           acknowledgment page
        - `notification_type`: type of notification -
           'Use On-box End User Notification' or
           'Redirect to custom URL'
        - `notification_url`: if notification type is to redirect, specify
           URL location to redirect notification to
           e.g. 'http://maps.google.com'
        - `notification_msg`: custom message for notification page
        - `notification_contact`: contact info for notification page
        - `notification_email`: contact email address for notification page
        - `notify_misclassification`: True to Allow end-user to report
           misclassified pages to IronPort
        - `url_cat_time_between`: Timeout between URL category warning page,
           must be 30 to 2678400 seconds, or use trailing
           s for seconds, m for minutes, h for hours
           (examples: 120s, 5m 30s, 4h)
        - `url_cat_msg`: additional text to be displayed on this warning page
        - `quota_time_enable`: 'True' To enable Time quota Notification
            'False' To disable time quota and 'None' To use current or default value
        - `quota_volume_enable`: 'True' To enable volume quota Notification
            'False' To disable volume quota and 'None' To use current or default value
        - `quota_time`: amount of time left on each time quota
        - `quota_volume`: notification percentage of each volume quota
        - `nativeftp_language`: language to use for Native FTP transactions
        - `nativeftp_msg`: additional text to be displayed on every
           notification message for Native FTP transactions

        Example:
        | EUN Edit Settings |
        | | http_language=French |
        | | logo=http://abc.d/logo.jpg |
        | | ack_enable=True |
        | | ack_time_between=2m |
        | | ack_timeout=3h |
        | | ack_msg=additional message |
        | | notification_type=Use On-box End User Notification |
        | | notification_url=http://redirect_page.err.adh/hello |
        | | notification_msg=custom message for notification page |
        | | notification_contact=Dedushka |
        | | notification_email=dedushke@na.derevnu |
        | | notify_misclassification=True |
        | | url_cat_time_between=120s |
        | | url_cat_msg=sample message |
        | | quota_time_enable=True |
        | | quota_volume_enable=True |
        | | quota_time=20m |
        | | quota_volume=80% |
        | | nativeftp_language=Russian |
        | | nativeftp_msg=Bonjour! |

        | EUN Edit Settings |
        | | logo=No Image |
        """

        self._info("Editing End-User Notification settings...")
        self._open_page()
        # check if proxy configured or not
        self._is_proxy_configured()
        self._click_edit_settings_button()
        self._select_http_https_language(http_language)
        self._set_logo_image(logo)
        self._enable_end_user_ack(ack_enable)
        self._set_end_user_ack_time_between(ack_time_between)
        self._set_end_user_ack_inactivity_timeout(ack_timeout)
        self._set_ack_custom_message(ack_msg)
        self._enable_volume_quota(quota_volume_enable)
        self._set_volume_quota(quota_volume)
        self._enable_time_quota(quota_time_enable)
        self._set_time_quota(quota_time)

        REDIRECT_TO_URL = 'Redirect to Custom URL'
        ONBOX_NOTIFICATION = 'Use On-box End User Notification'

        if notification_type is not None:
            self._select_notification_type(notification_type)
        else:
            # get current type to know which parameters are proper
            notification_type = self._get_current_notification_type()

        if notification_type == REDIRECT_TO_URL:

            not_valid_here = ('notification_msg',
                'notification_contact',
                'notification_email',
                'notify_misclassification')
            for param in not_valid_here:
                if locals()[param] is not None:
                    self._warn('Parameter %s will be ignored, please' \
                    ' set proper value for notification_type' % (param,))

            self._set_notification_page_url(notification_url)
        elif notification_type == ONBOX_NOTIFICATION:

            if notification_url is not None:
                self._warn('Parameters notification_url will be ignored, please' + \
                    ' set proper value for notification_type')

            self._set_end_user_notification_custom_msg(notification_msg)
            self._set_end_user_notification_contact(notification_contact)
            self._set_end_user_notification_email_address(notification_email)
            self._manipulate_end_user_misclassification_reporting \
                (notify_misclassification)
        else:
            raise ValueError('Bad notification type "%s"' % (notification_type,))

        self._set_url_cat_time_between(url_cat_time_between)
        self._set_url_cat_custom_msg(url_cat_msg)
        self._select_native_ftp_language(nativeftp_language)
        self._set_nativeftp_custom_msg(nativeftp_msg)
        self._click_submit_button()

    def eun_get_settings(self):
        """Gets settings of  End-User Notification

        Parameters:
        None

        Example:
        | ${result} | EUN Get Settings |
        """
        ENTRY_ENTITIES = lambda row,col:\
            '//table[@class=\'pairs\']/tbody/tr[%s]%s' % (str(row),col)
        entries = {}

        self._open_page()
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*',''))) + 1
        if num_of_entries > 1:
            for row in xrange(1, num_of_entries):
                name = self.get_text(ENTRY_ENTITIES(row, '/th[1]'))
                if self._is_element_present(ENTRY_ENTITIES(row, '/td[1]')):
                    value = self.get_text(ENTRY_ENTITIES(row, '/td[1]'))
                    entries[key].update({name:value})
                else:
                    key = name
                    entries[key] = {}
        return entries

    def _open_page(self):
        """Open 'End-User Notification' page """
        self._navigate_to("Security Services", "End-User Notification")

    def _select_http_https_language(self, http_language=None):

        if http_language is None: return

        CONFIRM_BUTTON="xpath=//button[@type='button']"
        http_language_select = "error_page_language"
        http_language_option = "label=%s" % (http_language,)
        self.select_from_list(http_language_select, http_language_option)
        self._info("HTTP/HTTPS language is set to '%s'" % \
           (http_language,))
        self.click_button(CONFIRM_BUTTON, "don't wait")

    def _set_logo_image(self, logo):
        if logo is None: return

        logo_radio_button = {"No Image".lower(): "no_image",
                             "Use Cisco IronPort Logo".lower(): "use_logo_ironport",
                             "Use Custom Logo".lower(): "use_logo_custom"}
        logo_custom_url_field = "error_page_logo_display_value"

        if logo.startswith("http"):
            self.click_button(logo_radio_button["Use Custom Logo".lower()],
                "don't wait")
            self.input_text(logo_custom_url_field, logo)
            self._info("Custom Logo is set to '%s'" % (logo,))
        else: # assuming user will give valid input
            self._click_radio_button(logo_radio_button[logo.lower()])
            self._info("Logo image is set to '%s'" % (logo,))

    def _enable_end_user_ack(self, ack_enable):
        if ack_enable is None: return

        if ack_enable:
            self._select_checkbox(ACK_CHECKBOX)
            self._info("Enabled require end-user to click through "\
               "acknowledgement page checkbox")
        else:
            self.unselect_checkbox(ACK_CHECKBOX)
            self._info("Disabled require end-user to click through "\
               "acknowledgement page checkbox")

    def _set_end_user_ack_time_between(self, ack_time_between):
        if ack_time_between is None: return

        ack_time_between_field = "maxAckTtl_text"

        self.input_text(ack_time_between_field, ack_time_between)
        self._info("Set Time Between Acknowledgements to '%s'" % \
           ack_time_between)

    def _set_end_user_ack_inactivity_timeout(self, ack_timeout):
        if ack_timeout is None: return

        ack_timeout_field = "maxIPAckIdle_text"

        self.input_text(ack_timeout_field, ack_timeout)
        self._info("Set Inactivity Timeout to '%s' " % ack_timeout)

    def _enable_volume_quota(self, quota_volume_enable):
        if quota_volume_enable is None: return

        if self._is_visible(VOLUME_QUOTA):
            if quota_volume_enable:
                self._select_checkbox(VOLUME_QUOTA)
                self._info("Enabled Volume quota Notification")
            else:
                self._unselect_checkbox(VOLUME_QUOTA)
                self._info("Disabled Volume quota Notification")
        else:
            self._warn('Volume Quota Feature is not visible')
            raise guiexceptions.GuiControlNotFoundError('Volume Quota',
                                                   'End-User Notification')

    def _set_volume_quota(self, quota_volume):
        if quota_volume is None: return

        quota_volume_field = "eun_volume_limit"

        self.input_text(quota_volume_field, quota_volume)
        self._info("Volume quota notification is set to '%s'" % quota_volume)


    def _enable_time_quota(self, quota_time_enable):
        if quota_time_enable is None: return

        if self._is_visible(TIME_QUOTA):
            if quota_time_enable:
                self._select_checkbox(TIME_QUOTA)
                self._info("Enabled Time quota Notification")
            else:
                self._unselect_checkbox(TIME_QUOTA)
                self._info("Disabled Time quota Notification")
        else:
            self._warn('Time Quota Feature is not visible')
            raise guiexceptions.GuiControlNotFoundError('Time Quota',
                                                   'End-User Notification')

    def _set_time_quota(self, quota_time):
        if quota_time is None: return

        quota_time_field = "eun_time_limit"

        self.input_text(quota_time_field, quota_time)
        self._info("Time quota notification is set to '%s'" % quota_time)


    def _set_ack_custom_message(self, ack_msg):
        if ack_msg is None: return

        ack_msg_field = "errorPageUserAckText"

        self.input_text(ack_msg_field, ack_msg)
        self._info("Set 'Custom Message' for End-User "\
           "Acknowledgement page to '%s'" % ack_msg)

    def _select_notification_type(self, notification_type):
        notification_type_select = "redirection_enabled"

        self.select_from_list(notification_type_select,
            notification_type)
        self._info("Notification Type is set to '%s'" % \
           (notification_type,))

    def _get_current_notification_type(self):
        notification_type_select = "redirection_enabled"
        notification_type = self._get_selected_label(notification_type_select)
        self._info("Current Notification Type is '%s'" % \
           (notification_type,))
        return notification_type

    def _set_notification_page_url(self, notification_url):

        if notification_url is None: return

        notification_url_field = "redirection_url"
        self.input_text(notification_url_field, notification_url)
        self._info("Set Notification Page URL to "\
           "'%s'" % (notification_url,))

    def _set_end_user_notification_custom_msg(self, notification_msg):

        if notification_msg is None: return

        notification_msg_field  = "search_domains"

        self.input_text(notification_msg_field, notification_msg)
        self._info("Set 'Custom Message' for End-User Notification "\
           "page to '%s'" % notification_msg)

    def _set_end_user_notification_contact(self, notification_contact):
        if notification_contact is None: return

        notification_contact_field  = "contact_info"

        self.input_text\
                (notification_contact_field, notification_contact)
        self._info("Set 'Contact' for End-User Notification "\
           "page to '%s'" % notification_contact)

    def _set_end_user_notification_email_address(self, notification_email):
        if notification_email is None: return

        notification_email_field  = "contact_email"

        self.input_text(notification_email_field, notification_email)
        self._info("Set 'Email address' for End-User Notification "\
           "page to '%s'" % notification_email)

    def _manipulate_end_user_misclassification_reporting(self,
        notify_misclassification):

        if notify_misclassification is None: return

        notify_misclassification_checkbox = "allowUserFeedback"

        if notify_misclassification:
            self.select_checkbox(notify_misclassification_checkbox)
            self._info("Enabled 'End-User Misclassification Report'")
        else:
            self.unselect_checkbox(notify_misclassification_checkbox)
            self._info("Disabled 'End-User Misclassification Report'")

    def _set_url_cat_time_between(self, url_cat_time_between):
        if url_cat_time_between is None: return

        url_cat_time_between_field = "continueTimeout"

        self.input_text(url_cat_time_between_field, url_cat_time_between)
        self._info("Set URL Category 'Time Between Warning' to "\
           "'%s'" % (url_cat_time_between,))

    def _set_url_cat_custom_msg(self, url_cat_msg):
        if url_cat_msg is None: return

        url_cat_msg_field = "custom_warning_message"

        self.input_text(url_cat_msg_field, url_cat_msg)
        self._info("Set URL Category 'Custom Message' to "\
            "'%s'" % (url_cat_msg,))

    def _select_native_ftp_language(self, nativeftp_language):
        if nativeftp_language is None: return

        nativeftp_language_select = "ftp_eun_language"

        nativeftp_language_option = "label=%s" % (nativeftp_language,)
        self.select_from_list(nativeftp_language_select,
            nativeftp_language_option)
        self._info("Native FTP 'Language' set "\
            "to '%s'" % (nativeftp_language,))

    def _set_nativeftp_custom_msg(self, nativeftp_msg):
        if nativeftp_msg is None: return

        nativeftp_msg_field = "ftp_eun_message"

        self.input_text(nativeftp_msg_field, nativeftp_msg)
        self._info\
           ("Native FTP End User Notification 'Custom Message' set "\
           "to '%s'" % (nativeftp_msg,))
