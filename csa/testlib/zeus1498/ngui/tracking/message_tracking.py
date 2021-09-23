# imports
import time

from common.gui.decorators import visit_page
from common.ngui.ngguicommon import NGGuiCommon
from common.gui.guiexceptions import InvalidUrlPathError, GuiFeatureDisabledError, GuiValueError
from common.ngui.exceptions import ElementNotFoundError, DataNotFoundError, UserInputError

from tracking import MESSAGE_TRACKING, AmpDispositions, AmpMailFlowDirection
from tracking import ContentFiltersMailFlowDirection, ContentFiltersAction, \
    DlpViolationSeverities, DlpAction, DmarcAction, EtfSelectIocs, GeoLocation, MacroMailFlowDirection, \
    MacroFileTypes, InPolicyOrVirusQuarantine, OutbreakFilters, Remediation, URLCategories, WebInteractionTrackingMailflowDirection
from tracking import CustomRange, SearchResult, SearchResultRemediate, SearchResultMoreDetails
from tracking import RejectedConnections, RejectedConnectionsSearchResult, SenderDomainReputation
from tracking import APPForwarding, ToastWidget

class Tracking(NGGuiCommon):

    def get_keyword_names(self):
        return ['message_tracking_search', 'message_tracking_get_message_details', \
                'clear_tracking_search', 'message_tracking_remediate', \
                'message_tracking_search_rejected_connections', \
                'message_tracking_rejected_connections_get_message_details',
                'toast_widget_visible',
                'toast_widget_location',
                'toast_widget_visible_time',
                'toast_widget_content',
                'toast_widget_cancel',
                'toast_widget_view_details'
                ]

    def _check_tracking_is_disabled(self):
        try:
            self.element_should_not_be_visible(MESSAGE_TRACKING.TRACKING_DISABLED)
        except Exception:
            raise GuiFeatureDisabledError

    @visit_page(MESSAGE_TRACKING.TRACKING_HEADER_XPATH, MESSAGE_TRACKING.TRACKING_URL_PATH)
    def message_tracking_search(self,
                                mesg_received='Today', from_date=None, from_time=None, to_date=None,
                                to_time=None, attachment_name=None,
                                attachment_comparator=None,
                                attachment_file_sha256=None,
                                attachment_threat_name=None,
                                sender_envelope_option=None,
                                sender_data=None,
                                sender_comparator=None,
                                rcpt_data=None,
                                rcpt_comparator=None,
                                subject_data=None,
                                subject_comparator=None,
                                reply_to=None,
                                reply_to_comparator=None,
                                mesg_id_header=None,
                                sender_ip=None, cisco_mid=None,
                                cisco_hosts=None,
                                url=None, url_in_mail_body=None,
                                url_in_attachment=None,
                                amp_protection_mailflow_directions=None,
                                amp_protection_dispositions=None,
                                advance_phising_protection_forwarding=None,
                                content_filter_name=None,
                                content_filters_mail_flow_direction=None,
                                content_filters_action=None,
                                dane_failure=None,
                                delivered=None,
                                dlp_policy=None,
                                dlp_violation_severities=None,
                                dlp_action=None,
                                dmarc_from_domain=None,
                                dmarc_action=None,
                                external_threat_feeds_source_name=None,
                                external_threat_feeds_iocs=None,
                                fed_executive_name=None,
                                geo_location=None,
                                geo_location_country_list=None,
                                graymail=None,
                                hard_bounced=None,
                                macro_file_type_mailflow_direction=None,
                                macro_file_types=None,
                                message_filters=None,
                                message_malicious_urls=None,
                                message_neutral_urls=None,
                                outbreak_filters_url_rewritten=None,
                                outbreak_filters_vof_threat_category=None,
                                in_outbreak_quarantine=None,
                                in_policy_or_virus_quarantine_name=None,
                                in_policy_or_virus_quarantine_list=None,
                                remediation_result=None,
                                s_mime=None,
                                safeprint=None,
                                sdr_verdicts=None, sdr_threat_categories=None,
                                soft_bounced=None,
                                spam_positive=None,
                                in_spam_quarantine=None,
                                suspect_spam=None,
                                url_categories=None,
                                virus_positive=None,
                                web_interaction_tracking_url_clicked=None,
                                web_interaction_tracking_mailflow_direction=None,
                                wait_time=None):
        """Message Tracking Search.

                Use this method to search for a particular email message or group of
                messages that match specified criteria.
        Usage:
         Message Tracking search        subject_data=Testing
        ...      subject_comparator=Begins with
        """

        self.wait_for_angular()
        self._check_tracking_is_disabled()

        if mesg_received:
            if MESSAGE_TRACKING.MESSAGE_RECIEVED_OPTIONS.has_key(mesg_received):
                self.click_element(MESSAGE_TRACKING.MESSAGE_RECIEVED_OPTIONS[mesg_received])
                if mesg_received == 'Custom Range':
                    if from_date:
                        self.select_date_on_calendar_widget(CustomRange.from_date_select, from_date)
                    if from_time:
                        self.input_text(CustomRange.from_hour, from_time.split(":")[0])
                        self.input_text(CustomRange.from_mins, from_time.split(":")[1])
                    if to_date:
                        self.select_date_on_calendar_widget(CustomRange.to_date_select, to_date)
                    if to_time:
                        self.input_text(CustomRange.to_hour, to_time.split(":")[0])
                        self.input_text(CustomRange.to_mins, to_time.split(":")[1])
            else:
                raise UserInputError("Invalid option provided:%s : \
                Available options:Today,Last 7 days,Custom Range"%mesg_received)

        if attachment_comparator:
            self.select_custom_dropdown(MESSAGE_TRACKING.ATTACHMENT_COMPARATOR, attachment_comparator)
        if attachment_name:
            self.input_text(MESSAGE_TRACKING.ATTACHMENT, attachment_name)
        if attachment_file_sha256:
            self.input_text(MESSAGE_TRACKING.ATTACHMENT_FILE_SHA_256, attachment_file_sha256)
        if attachment_threat_name:
            self.input_text(MESSAGE_TRACKING.ATTACHMENT_THREAT_NAME, attachment_threat_name)

        if sender_envelope_option:
            self.select_custom_dropdown(MESSAGE_TRACKING.SENDER_OPTION, sender_envelope_option)
        if sender_comparator:
            self.select_custom_dropdown(MESSAGE_TRACKING.SENDER_COMPARATOR, sender_comparator)
        if sender_data:
            self.input_text(MESSAGE_TRACKING.SENDER_XPATH, sender_data)

        if rcpt_comparator:
            self.select_custom_dropdown(MESSAGE_TRACKING.ENVELOPE_RECIPIENT_COMPARATOR, rcpt_comparator)
        if rcpt_data:
            self.input_text(MESSAGE_TRACKING.ENVELOPE_RECIPIENT, rcpt_data)

        if subject_comparator:
            self.select_custom_dropdown(MESSAGE_TRACKING.SUBJECT_COMPARATOR, subject_comparator)
        if subject_data:
            self.input_text(MESSAGE_TRACKING.SUBJECT, subject_data)

        if reply_to_comparator:
            self.select_custom_dropdown(MESSAGE_TRACKING.REPLY_TO_COMPARATOR, reply_to_comparator)
        if reply_to:
            self.input_text(MESSAGE_TRACKING.REPLY_TO, reply_to)
        if cisco_hosts:
            self.select_custom_dropdown(MESSAGE_TRACKING.CISCO_HOSTS, cisco_hosts, regexp=True)

        self.click_ng_button(MESSAGE_TRACKING.ADVANCE_SEARCH_PATH, 'Advanced Search')

        if mesg_id_header:
            self.input_text(MESSAGE_TRACKING.MESSAGE_ID_HEADER_XPATH, mesg_id_header)
        if sender_ip:
            self.input_text(MESSAGE_TRACKING.SENDER_IP_XPATH, sender_ip)
        if cisco_mid:
            self.input_text(MESSAGE_TRACKING.CISCO_MID_XPATH, cisco_mid)
        if url:
            self.input_text(MESSAGE_TRACKING.URL, url)
        if url_in_mail_body:
            self.select_custom_checkbox(MESSAGE_TRACKING.URL_IN_BODY)
        if url_in_attachment:
            self.select_custom_checkbox(MESSAGE_TRACKING.URL_IN_ATTACHMENT)

        if amp_protection_mailflow_directions or amp_protection_dispositions:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.AMP_EVENT))
            for mail_flow in amp_protection_mailflow_directions:
                self.click_element(getattr(AmpMailFlowDirection, mail_flow))
            for amp_disposition in amp_protection_dispositions:
                self.click_element(getattr(AmpDispositions, amp_disposition))

        if advance_phising_protection_forwarding:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.APP_FORWARDING))
            for forwarding_action in advance_phising_protection_forwarding:
                self.click_element(getattr(APPForwarding, forwarding_action))

        if content_filter_name or content_filters_mail_flow_direction or content_filters_action:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.CONTENT_FILTERS))
            if content_filter_name:
                self.input_text(MESSAGE_TRACKING.CONTENT_FILTER_NAME, content_filter_name)
            for mail_flow in content_filters_mail_flow_direction:
                self.click_element(getattr(ContentFiltersMailFlowDirection, mail_flow))

            self.click_element(getattr(ContentFiltersAction, content_filters_action))

        if dane_failure:
            self.select_custom_checkbox(MESSAGE_TRACKING.DANE_FAILURE)
            self.custom_checkbox_should_be_selected(MESSAGE_TRACKING.DANE_FAILURE)

        if delivered:
            self.select_custom_checkbox(MESSAGE_TRACKING.DELIVERED)
            self.custom_checkbox_should_be_selected(MESSAGE_TRACKING.DELIVERED)

        if dlp_policy or dlp_violation_severities or dlp_action:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.DLP_VIOLATIONS_EVENT))
            if dlp_policy:
                self.input_text(MESSAGE_TRACKING.DLP_POLICY_NAME, dlp_policy)
                for violation_severities in dlp_violation_severities:
                    self.click_element(getattr(DlpViolationSeverities, violation_severities))
                for action in dlp_action:
                    self.click_element(getattr(DlpAction, action))

        if dmarc_from_domain or dmarc_action:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.DMARC_EVENT))
            if dmarc_from_domain:
                self.input_text(MESSAGE_TRACKING.DMARC_FROM_DOMAIN, dmarc_from_domain)
                for action in dmarc_action:
                    self.click_element(getattr(DmarcAction, action))

        if external_threat_feeds_source_name or external_threat_feeds_iocs:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.ETF_EVENT))
            if external_threat_feeds_source_name:
                self.input_text(MESSAGE_TRACKING.ETF_SOURCE, external_threat_feeds_source_name)
            for iocs in external_threat_feeds_iocs:
                self.click_element(getattr(EtfSelectIocs, iocs))

        if fed_executive_name:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.FED_EVENT))
            self.input_text(MESSAGE_TRACKING.FED_EXECUTIVE_NAME, fed_executive_name)

        if geo_location or geo_location_country_list:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.GEO_LOCATION))
            for each_geo_location in geo_location:
                self.click_element(getattr(GeoLocation, each_geo_location))
            for country in geo_location_country_list:
                if country == 'All':
                    pass
                else:
                    self.select_ng_repeat_checkbox(getattr(geoLocation, 'Country_list') % (country))

        if graymail:
            self.select_custom_checkbox(MESSAGE_TRACKING.GRAYMAIL)

        if hard_bounced:
            self.select_custom_checkbox(MESSAGE_TRACKING.HARD_BOUNCED)

        if macro_file_type_mailflow_direction or macro_file_types:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.MACRO_FILE_TYPE))
            for mail_flow in macro_file_type_mailflow_direction:
                self.select_custom_checkbox(getattr(MacroMailFlowDirection, mail_flow))
            for file_type in macro_file_types:
                self.select_ng_repeat_checkbox(getattr(MacroFileTypes, 'Filetypes') % (file_type))

        if message_filters:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.MESSAGE_FILTERS_EVENT))
            self.input_text(MESSAGE_TRACKING.MESSAGE_FILTER, message_filters)

        if message_malicious_urls:
            self.select_custom_checkbox(MESSAGE_TRACKING.MESSAGES_WITH_MALICIOUS_URL)
        if message_neutral_urls:
            self.select_custom_checkbox(MESSAGE_TRACKING.MESSAGES_WITH_NEUTRAL_URL)

        if outbreak_filters_url_rewritten or outbreak_filters_vof_threat_category:
            self.click_ng_button(MESSAGE_TRACKING.OUTBREAK_FILTERS_EVENT, '')
            if outbreak_filters_url_rewritten:
                self.click_ng_button(OutbreakFilters.URL_Rewritten, '')
                self.input_text(MESSAGE_TRACKING.OUTBREAK_FILTERS_URL_REWRITTEN, outbreak_filters_url_rewritten)
            if outbreak_filters_vof_threat_category:
                self.click_ng_button(OutbreakFilters.VOF_Threat_Category, '')
                self.input_text(MESSAGE_TRACKING.OUTBREAK_FILTERS_VOF_THREAT_CATEGORY,
                                outbreak_filters_vof_threat_category)

        if in_outbreak_quarantine:
            self.select_custom_checkbox(MESSAGE_TRACKING.IN_OUTBREAK_QUARANTINE)

        if in_policy_or_virus_quarantine_name or in_policy_or_virus_quarantine_list:
            self.click_ng_button(MESSAGE_TRACKING.IN_POLICY_OR_VIRUS_QUARANTINE, '')
            if in_policy_or_virus_quarantine_name:
                self.click_element(InPolicyOrVirusQuarantine.Non_Existance_Quarantine_radio)
            for quarantine in in_policy_or_virus_quarantine_list:
                self.click_element(InPolicyOrVirusQuarantine.Quarantine_list_radio)
                self.select_ng_repeat_checkbox(getattr(InPolicyOrVirusQuarantine, 'Quarantine_list') % (quarantine))

        if remediation_result:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.REMEDIATION_EVENT))
            for remediation_option in remediation_result:
                self.select_custom_checkbox(getattr(Remediation, remediation_option))

        if s_mime:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.SMIME_EVENT))
            for smime_option in s_mime:
                self.select_custom_checkbox(getattr(S_Mime, smime_option))

        if safeprint:
            self.select_custom_checkbox(MESSAGE_TRACKING.SAFE_PRINT)

        if sdr_verdicts or sdr_threat_categories:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.SDR_EVENT))
            self.wait_for_angular()
            self.set_selenium_speed('0.2s')
            if sdr_verdicts:
                for each_verdict in sdr_verdicts:
                    if SenderDomainReputation.verdicts.has_key(each_verdict):
                        if str(each_verdict) == 'Not Scanned':
                            self.select_ng_repeat_checkbox(SenderDomainReputation.verdicts['Not Scanned'])
                        else:
                            self.select_custom_checkbox(SenderDomainReputation.verdicts[each_verdict])
                    else:
                        raise UserInputError("Invalid option provided:%s"%each_verdict)

            if sdr_threat_categories:
                for each_category in sdr_threat_categories:
                    try:
                        self.select_ng_repeat_checkbox(getattr(SenderDomainReputation, 'threat_categories') % (each_category))
                    except Exception as error:
                        raise UserInputError("Invalid option provided:%s:%s" % (each_category,error))
            self.set_selenium_speed('1s')

        if soft_bounced:
            self.select_custom_checkbox(MESSAGE_TRACKING.SOFT_BOUNCED)

        if spam_positive:
            self.select_custom_checkbox(MESSAGE_TRACKING.SPAM_POSITIVE)

        if in_spam_quarantine:
            self.select_custom_checkbox(MESSAGE_TRACKING.IN_SPAM_QUARANTINE)

        if suspect_spam:
            self.select_custom_checkbox(MESSAGE_TRACKING.SUSPECT_SPAM)

        if url_categories:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.URL_CATEGORIES_EVENT))
            for url_category in url_categories:
                self.select_ng_repeat_checkbox(getattr(URLCategories, 'url_category') % (url_category))

        if virus_positive:
            self.select_custom_checkbox(MESSAGE_TRACKING.VIRUS_POSITIVE)

        if web_interaction_tracking_url_clicked or web_interaction_tracking_mailflow_direction:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.WEB_INTERACTION_TRACKING_EVENT))
            if web_interaction_tracking_url_clicked:
                self.input_text(MESSAGE_TRACKING.WEB_INTERACTION_URL_CLICKED, web_interaction_tracking_url_clicked)
            for mailflow_direction in web_interaction_tracking_mailflow_direction:
                self.select_custom_checkbox(getattr(WebInteractionTrackingMailflowDirection, mailflow_direction))

        self.click_ng_button(MESSAGE_TRACKING.ADVANCE_SEARCH_PATH, 'Advanced Search')

        if wait_time and wait_time >=0 :
            self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
            self.wait_for_angular()

            self._debug('waiting for wait time to over:%s'%wait_time)
            time.sleep(int(wait_time))
            self.click_button(MESSAGE_TRACKING.SHOW_FILTER)
            self.click_ng_button(MESSAGE_TRACKING.MODIFY, 'Modify')
            self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
            self.wait_for_angular()
        else:
            self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
            self.wait_for_angular()

    def _get_more_details(self, message_index):
        more_data = {}
        self.click_link(SearchResultMoreDetails.more_details % (message_index))
        self.wait_for_angular()
        self.set_selenium_speed('0.05s')
        more_data[self.get_text(SearchResultMoreDetails.message_id_header)] = self.get_text(
            SearchResultMoreDetails.message_id_values)
        more_data[self.get_text(SearchResultMoreDetails.last_state_header)] = self.get_text(
            SearchResultMoreDetails.last_state_value)
        more_data['timestamp'] = self.get_text(SearchResultMoreDetails.timestamp)
        more_data[self.get_text(SearchResultMoreDetails.mid)] = self.get_text(
            SearchResultMoreDetails.mid_value)
        more_data[self.get_text(SearchResultMoreDetails.sender)] = self.get_text(
            SearchResultMoreDetails.sender_value)
        more_data[self.get_text(SearchResultMoreDetails.subject)] = self.get_text(
            SearchResultMoreDetails.subject_value)
        more_data[self.get_text(SearchResultMoreDetails.sender_group)] = self.get_text(
            SearchResultMoreDetails.sender_group_value)
        more_data[self.get_text(SearchResultMoreDetails.message_size)] = self.get_text(
            SearchResultMoreDetails.message_size_value)

        if self._is_element_present(SearchResultMoreDetails.incoming_policy_match):
            more_data[self.get_text(SearchResultMoreDetails.incoming_policy_match)] = self.get_text(
            SearchResultMoreDetails.incoming_policy_match_value)
        else:
            self._debug('incoming_policy_match is not visible')

        if self._is_element_present(SearchResultMoreDetails.policy_match):
            more_data[self.get_text(SearchResultMoreDetails.policy_match)] = self.get_text(
            SearchResultMoreDetails.policy_match_value)
        else:
            self._debug('policy_match is not visible')

        more_data[self.get_text(SearchResultMoreDetails.recipient)] = self.get_text(
            SearchResultMoreDetails.recipient_value)
        more_data[self.get_text(SearchResultMoreDetails.attachments)] = self.get_text(
            SearchResultMoreDetails.attachments_value)
        more_data[self.get_text(SearchResultMoreDetails.smtp_auth_user_id)] = self.get_text(
            SearchResultMoreDetails.smtp_auth_user_id_value)
        more_data[self.get_text(SearchResultMoreDetails.cisco_hostname)] = self.get_text(
            SearchResultMoreDetails.cisco_hostname_value)
        more_data[self.get_text(SearchResultMoreDetails.header_from)] = self.get_text(
            SearchResultMoreDetails.header_from_value)
        more_data[self.get_text(SearchResultMoreDetails.reverse_dns_hostname)] = self.get_text(
            SearchResultMoreDetails.reverse_dns_hostname_value)
        more_data[self.get_text(SearchResultMoreDetails.ip_address)] = self.get_text(
            SearchResultMoreDetails.ip_address_value)
        more_data[self.get_text(SearchResultMoreDetails.sbrs_score)] = self.get_text(
            SearchResultMoreDetails.sbrs_score_value)

        more_data['summary'] = self.get_text(SearchResultMoreDetails.summary)
        self.set_selenium_speed('0.5s')
        print "more_data", more_data
        return more_data

    def _get_tracking_data(self, message_index=None, more_details=None):
        tmp_data = {}
        sender_options_range = 5
        self.set_selenium_speed('0.05s')
        tmp_data['mid'] = self.get_text(SearchResult.result_table_details % (message_index) + SearchResult.message_mid)
        tmp_data['status'] = self.get_text(SearchResult.message_status % (message_index))
        tmp_data['timestamp'] = self.get_text(SearchResult.timestamp % (message_index))
        tmp_data[self.get_text(SearchResult.policy_match_header % (message_index))] = \
            self.get_text(SearchResult.policy_match_value % (message_index))
        for sender_options in range(1, sender_options_range):
            text_value = self.get_text(SearchResult.sender_values % (message_index, sender_options))
            header = text_value.split('\n')[0]
            self._debug('Sender option header is %s'%header)
            value = self.get_text(SearchResult.sender_values_info % (message_index, sender_options))
            self._debug('Sender option value is %s'%value)
            tmp_data[header] = value
        try:
            self.click_element(SearchResult.expand_button % (message_index))
            verdict_header = self.find(SearchResult.tracking_result_verdict_header % (message_index), first_only=False)
            verdict_values = self.find(SearchResult.tracking_result_verdict_values % (message_index), first_only=False)
            verdict_dict = {}
            for header, values in zip(verdict_header, verdict_values):
                verdict_dict[self.get_text(header)] = self.get_text(values)
            tmp_data['verdicts'] = verdict_dict
        except Exception as error:
            self._info("ERROR:Expand button is not visible%s" % error)
        self.set_selenium_speed('0.5s')
        if more_details:
            tmp_data['More Details'] = self._get_more_details(message_index)
        return tmp_data

    def _get_message_details(self, mid, more_details=None):
        mid_data = {}
        self.set_selenium_speed('0.05s')
        for each_msg in range(int(self.get_text(SearchResult.total_count))):
            current_mid =self.get_text(SearchResult.result_table_details % (each_msg) + SearchResult.message_mid)
            if ',' in current_mid:
                current_mid_id= current_mid.split(',')
                for mid_id in current_mid_id:
                    if int(mid_id) == int(mid):
                        mid_data[mid_id] = self._get_tracking_data(message_index=each_msg, more_details=more_details)
                        break
                    else:
                        continue
            else:
                print "CURRENT MID", current_mid, mid
                if mid and int(current_mid) == int(mid):
                    mid_data[current_mid] = self._get_tracking_data(message_index=each_msg, more_details=more_details)
                    break
            if not mid:
                mid_data[current_mid] = self._get_tracking_data(message_index=each_msg, more_details=more_details)
        return mid_data

    def message_tracking_get_message_details(self, mid=None, more_details=None, retry_time=None):
        """
        To get the message tracking detail of the searched messages
        :param mid: MID
        :param more_details : To get the more details of the mid message details
        :return:  all messages in the search.. with key of mid and values of other fields data in that
        usage:
        To get the message details of mail of mid
        {details}=     message_tracking_get_message_details     mid=20
        LogMany    ${details}
        Log     ${details['20']}

        To get all message details in the view .
        {details}=     message_tracking_get_message_details
        LogMany    ${details}
        Log     ${details['20']}

        This keyword should be used along with Message Tracking search
        """

        mid_data = {}
        self.wait_for_angular()
        if MESSAGE_TRACKING.TRACKING_RESULTS_PATH not in self.get_location():
            raise InvalidUrlPathError
        if not self._is_element_present(SearchResult.total_count):
            raise GuiValueError('ERROR:No Message details found')

        if retry_time and retry_time >=0 :
            start_time =time.time()
            while (int(time.time()-start_time) <= int(retry_time)):
                self.click_button(MESSAGE_TRACKING.SHOW_FILTER)
                self.click_ng_button(MESSAGE_TRACKING.MODIFY, 'Modify')
                self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
                self.wait_for_angular()
                print "WAITING AND RETRY...."
                time.sleep(1)
                mid_data = self._get_message_details(mid, more_details=more_details)
                self.set_selenium_speed('0.5s')
                if mid_data.has_key(mid):
                    break
        else:
            mid_data = self._get_message_details(mid, more_details=more_details)
            self._debug("MID DATA Details")
            self._debug(mid_data)
            mid_data = {k.replace(" ", ""): v for k, v in mid_data.items()}

        if not mid_data.has_key(mid):
            raise DataNotFoundError('Data not found for MID:%s'%mid)
        return mid_data

    def _select_all_to_remediate(self):
        reached_max = 0
        latest_mid = self.get_text(SearchResult.result_table_details %(0) + SearchResult.message_mid)
        self._debug("Latest MID")
        self._debug(latest_mid)
        self.set_selenium_speed('0.05s')
        for each_scroll in range(int(latest_mid)):
            self.prev_count = self.get_text(SearchResult.total_count)
            for count in range(5):
                self.press_keys(SearchResult.scroll_bar, 'PAGE_DOWN')
            current_count = self.get_text(SearchResult.total_count)
            if int(current_count) == int(self.prev_count):
                reached_max +=1
            else:
                reached_max =0
            self._debug('Reached max count: %s'%reached_max)
            if reached_max > 6:
                self._debug('Reached max count:%s'%current_count)
                self._debug("Total Messages scrolled down")
                self._debug(self.get_text(SearchResult.total_count))
                self.click_element(SearchResultRemediate.remediate_all)
                max_limit_reached = self._wait_until_element_is_present(SearchResultRemediate.maximum_messages_title, timeout=5)
                if max_limit_reached:
                    self.click_ng_button(SearchResultRemediate.ok_button, 'Ok')
                return True
    def _select_mid_to_remediate(self, mid=None):
        mid_count = 0 
        if type(mid) in [str, unicode] and mid.upper() =='ALL':
            self._select_all_to_remediate()
            return True
        else:
            total_count = int(self.get_text(SearchResult.total_count))
            for each_msg in range(total_count):
                current_mid = self.get_text(SearchResult.result_table_details % (each_msg) + SearchResult.message_mid)
                if ',' in current_mid and ',' not in mid:
                    current_mid_id= current_mid.split(',')
                    for mid_id in current_mid_id:
                        if int(mid_id) == int(mid):
                            self.select_ngsma_search_result_checkbox(\
                                SearchResult.result_table_details % (each_msg) + SearchResult.message_checkbox)
                            break
                        else:
                            continue
                    mid_count += 1
                elif ',' in current_mid and ',' in mid:
                      current_mid_id= current_mid.split(',')
                      mid_list= mid.split(',')
                      for mid_id_current in current_mid_id:
                          if mid_count != len(mid_list):
                              for mid_id in mid_list:
                                  if int(mid_id) == int(mid_id_current):
                                     self.select_ngsma_search_result_checkbox(\
                                     SearchResult.result_table_details % (each_msg) + SearchResult.message_checkbox)
                                     mid_count += 1
                                     break
                                  else:
                                      continue
                          else:
                              break
                else:
                    if ',' in mid:
                       mid_list= mid.split(',')
                       if mid_count != len(mid_list):
                           for mid_id in mid_list:
                               if int(mid_id) == int(current_mid):
                                   self.select_ngsma_search_result_checkbox(\
                                   SearchResult.result_table_details % (each_msg) + SearchResult.message_checkbox)
                                   mid_count += 1
                                   break
                               else:
                                   continue
                       else:
                           break
                    elif int(current_mid) == int(mid):
                        self.select_ngsma_search_result_checkbox(\
                        SearchResult.result_table_details % (each_msg) + SearchResult.message_checkbox)
                        mid_count += 1
                        break
            if mid_count > 0:
                return True
            else:
                return False

    def message_tracking_remediate(self, mid=None, batch_name=None, \
                                   description=None, delete_email=None,
                                   forward_email_address=None,
                                   delete_and_forward_email_address=None, \
                                   confirm_remediation_action='Apply',\
                                   remediation_msg_count=None,\
                                   remediation_status=None,\
                                   remediation_status_action='Close', \
                                   wait_time=None, \
                                   retry_time=None,\
                                   toast_widget_action=None):
        """
        This keyword to remediate the mail after the tracking search
        :param mid: MID
        :param batch_name: name of batch
        :param description: description to search
        :param delete_email: delete email
        :param forward_email_address: forward email address field
        :param delete_and_forward_email_address: delete and email address field
        :param confirmation_action : Apply, Cancel, Close
        :param remediation_status : status message of remediation status window
        :param remediation_msg_count : count of message remediated shown in remediation status window
        :param remediation_status_action : remediation_status_action to do Close/Go Back (Close/Go Back/Go To Status Report)
        :param wait_time: if wait_time is seconds specified its waits for the time to checks for mid ...
        :param retry_time: if retry_time is seconds specified its retry for the time to checks for mid ...
        :param toast_widget_action: will do the toast widget action (Verify, Close, Cancel, Location, Content)
        :return: if toast_widget_action is not None it will return toast widget data based on its toast_widget_action
        :return:
        For mid=ALL , the retry_time option is invalid, use wait_time to wait for message to appear on tracking
        usage:
        message_tracking_remediate       mid=62
        ...         batch_name=Test
        ...         description=welcome desc
        ...         delete_email=${True}
        ...         retry_time=20

        The keyword message_tracking_search should be used before using this keyword.
        """

        self.set_selenium_speed('0.1s')
        toast_data = None
        mid_status = False
        if not mid:
            raise ("ERROR:MID input is missing")
        if retry_time and retry_time >=0 :
            start_time =time.time()
            while (int(time.time()-start_time) <= int(retry_time)):
                mid_status = self._select_mid_to_remediate(mid)
                if mid_status:
                    break
                self.click_button(MESSAGE_TRACKING.SHOW_FILTER)
                self.click_ng_button(MESSAGE_TRACKING.MODIFY, 'Modify')
                self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
                self.wait_for_angular()
            if not mid_status:
                raise ElementNotFoundError('MID not found:%s'%mid)
     	elif wait_time and wait_time >=0 :
            self._debug('waiting for wait time to over:%s'%wait_time)
            time.sleep(int(wait_time))
            self.click_button(MESSAGE_TRACKING.SHOW_FILTER)
            self.click_ng_button(MESSAGE_TRACKING.MODIFY, 'Modify')
            self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
            self.wait_for_angular()
            if not self._select_mid_to_remediate(mid):
                raise ElementNotFoundError('MID not found:%s'%mid)
        else:
            if not self._select_mid_to_remediate(mid):
                raise ElementNotFoundError('MID not found:%s'%mid)

        self.set_selenium_speed('1s')

        time.sleep(5)

        if self._wait_until_element_is_present(SearchResultRemediate.Remediate_button):
            self.click_element(SearchResultRemediate.Remediate_button)
        else:
            self._debug("Remediation button is disabled..")

        try:
            self._wait_until_element_is_present(SearchResultRemediate.confirm_action_title, timeout=5)
            time.sleep(5)
            self._debug("Remediate popup window displayed..")
        except Exception as error:
            raise GuiValueError('ERROR:Failed to remediate MID:%s:%s' %(mid,error))

        if batch_name:
            self._debug("Entering text in Remediation batch name")
            self.click_element(SearchResultRemediate.batch_name)
            self.input_text(SearchResultRemediate.batch_name, batch_name)

        if description:
            self.input_text(SearchResultRemediate.batch_description, description)

        if delete_email:
            self.click_element(SearchResultRemediate.delete_email_radio_button)

        if forward_email_address:
            self.click_element(SearchResultRemediate.forward_email_to_radio_button)
            self.input_text(SearchResultRemediate.forward_email_address, forward_email_address)

        if delete_and_forward_email_address:
            self.click_element(SearchResultRemediate.delete_and_forward_radio_button)
            self.input_text(SearchResultRemediate.delete_and_forward_email_address, delete_and_forward_email_address)

        if confirm_remediation_action.lower() == 'apply':
            self.click_ng_button(SearchResultRemediate.apply, 'Apply')
            self.set_selenium_speed('0s')
            if toast_widget_action:
                toast_data = self._handle_toast_widget_action(toast_widget_action.lower())
            self.set_selenium_speed('0.5s')
            self._wait_until_element_is_present(SearchResultRemediate.remediation_status_title, timeout=5)

            if remediation_status:
                status_text = str(self.get_text(SearchResultRemediate.remediation_status
                                                ).encode('ascii', 'ignore').decode('ascii'))
                self._debug("Remediation Status message:%s"%(status_text))
                if remediation_status not in status_text:
                    raise GuiValueError('Remediation status message not matched:%s'%status_text)

            if remediation_msg_count:
                remediation_action_count = int(self.get_text(SearchResultRemediate.remediation_action_count))
                if int(remediation_msg_count) != remediation_action_count:
                    self._debug("Remediation messge count")
                    self._debug(int(remediation_msg_count))
                    self._debug(remediation_action_count)
                    raise GuiValueError('Remediation action count not matched:%s'%remediation_action_count)

            if remediation_status_action != 'Close':
                if remediation_status_action.lower() == 'go back':
                    self.click_element(SearchResultRemediate.remediation_status_go_back)
                if remediation_status_action.lower() == 'go to status report':
                    self.click_element(SearchResultRemediate.go_to_status_report)
                self.wait_for_angular()
            else:
                self.click_element(SearchResultRemediate.close)

        elif confirm_remediation_action.lower() == 'Cancel':
            self.click_ng_button(SearchResultRemediate.cancel, 'Cancel')
        else:
            self.click_element(SearchResultRemediate.close)

        if toast_widget_action:
            return toast_data

    @visit_page(MESSAGE_TRACKING.TRACKING_HEADER_XPATH, MESSAGE_TRACKING.TRACKING_URL_PATH)
    def message_tracking_search_rejected_connections(self, mesg_received='Today', from_date=None, from_time=None, \
                                                     to_date=None, to_time=None, sender_ip=None):
        """Message Tracking Search rejected connections .

                Use this method to search for a particular email message or group of
                messages that match specified criteria in the rejected connections .
        Usage:
         ${msg_recv}=       Set Variable      Last 7 days
         message_tracking_search_rejected_connections     mesg_received=${msg_recv}
        """
        self.wait_for_angular()
        self._check_tracking_is_disabled()
        self.click_ng_button(RejectedConnections.rejected_connection_tab, 'Rejected Connections')
        if mesg_received:
            if MESSAGE_TRACKING.MESSAGE_RECIEVED_OPTIONS.has_key(mesg_received):
                self.click_element(MESSAGE_TRACKING.MESSAGE_RECIEVED_OPTIONS[mesg_received])
                if mesg_received == 'Custom Range':
                    if from_date:
                        self.select_date_on_calendar_widget(CustomRange.from_date_select, from_date)
                    if from_time:
                        self.input_text(CustomRange.from_hour, from_time.split(":")[0])
                        self.input_text(CustomRange.from_mins, from_time.split(":")[1])
                    if to_date:
                        self.select_date_on_calendar_widget(CustomRange.to_date_select, to_date)
                    if to_time:
                        self.input_text(CustomRange.to_hour, to_time.split(":")[0])
                        self.input_text(CustomRange.to_mins, to_time.split(":")[1])
            else:
                raise UserInputError("Invalid option provided:%s : \
                Available options:Today,Last 7 days,Custom Range" % mesg_received)

        if sender_ip:
            self.input_text(RejectedConnections.sender_ip_address, sender_ip)
        self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
        self.wait_for_angular()

    def _get_rejected_connections_details(self):
        icid_data = {}
        self.element_should_be_visible(RejectedConnectionsSearchResult.message_details)
        self.set_selenium_speed('0.2s')
        for tracking_message in range(int(self.get_text(RejectedConnectionsSearchResult.total_count))):
            tmp_data = {}
            tmp_data['icid'] = \
            self.get_text(RejectedConnectionsSearchResult.icid % (int(tracking_message))).split('\n')[1]
            tmp_data['status'] = self.get_text(RejectedConnectionsSearchResult.status % (int(tracking_message)))
            tmp_data['timestamp'] = self.get_text(RejectedConnectionsSearchResult.timestamp % (tracking_message))
            tmp_data['SenderIP'] = \
            self.get_text(RejectedConnectionsSearchResult.sender_ip % (tracking_message)).split('\n')[1]
            tmp_data['SBRSScore'] = \
            self.get_text(RejectedConnectionsSearchResult.sbrs_score % (tracking_message)).split('\n')[1]
            tmp_data['SenderGroup'] = \
            self.get_text(RejectedConnectionsSearchResult.sender_group % (tracking_message)).split('\n')[1]
            tmp_data['Rejected'] = \
            self.get_text(RejectedConnectionsSearchResult.rejected % (tracking_message)).split('\n')[1]
            icid_data[tmp_data['icid']] = tmp_data
        self.set_selenium_speed('1s')
        return icid_data

    def message_tracking_rejected_connections_get_message_details(self, retry_time=None):
        """
        To get the rejected connections message tracking detail of the searched messages
        :return:  all messages in the search.. with key of ICID and values of other fields data in that
        usage:
        message_tracking_search_rejected_connections
        {details}=     message_tracking_rejected_connections_get_message_details
        LogMany    ${details}
        Log     ${details['20']}
        """
        details = {}
        self.wait_for_angular()
        if MESSAGE_TRACKING.TRACKING_RESULTS_PATH not in self.get_location():
            raise InvalidUrlPathError
        if retry_time and retry_time >=0 :
            start_time =time.time()
            while (int(time.time()-start_time) <= int(retry_time)):
                details = self._get_rejected_connections_details()
                self.click_ng_button(MESSAGE_TRACKING.MODIFY,  'Modify')
                self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
                self.wait_for_angular()
        else:
            details = self._get_rejected_connections_details()
        return details

    @visit_page(MESSAGE_TRACKING.TRACKING_HEADER_XPATH, MESSAGE_TRACKING.TRACKING_URL_PATH)
    def clear_tracking_search(self):
        """
        To clear the tracking search
        usage:
        Message Tracking search        geo_location=${geo_location}
        ...         geo_location_country_list=${geo_location_country_list}
        clear_tracking_search
        return:
        """
        if MESSAGE_TRACKING.TRACKING_URL_PATH not in self.get_location():
            raise InvalidUrlPathError
        self.click_button(MESSAGE_TRACKING.CLEAR_BUTTON)
        self.wait_for_angular()

    def _handle_toast_widget_action(self, action):
        if action == 'verify':
            if self.toast_widget_visible():
                self._info('Toast widget is visible')
            else:
                raise ElementNotFoundError('Toast Widget is invisible')

        if action == 'cancel':
            self.toast_widget_cancel()

        if action == 'location':
            return self.toast_widget_location()

        if action == 'visible time':
            return self.toast_widget_visible_time()

        if action == 'content':
            return self.toast_widget_content()

    def toast_widget_visible(self):
        """"
        This keyword to find the toast widget visible or not
        return: True/False
        """
        return self._is_visible(ToastWidget.toast_widget)

    def toast_widget_location(self):
        if self.toast_widget_visible():
            element = self.get_webelement(ToastWidget.toast_widget)
            self._info("Toast widget location:%s" % element.location)
            return element.location

    def toast_widget_visible_time(self):
        start_time = time.time()
        duration = 20
        while (time.time() - start_time <= duration):
            if not self.toast_widget_visible():
                break
        visible_time = time.time() - start_time
        self._info("Toast Widget Visible Time:%s" % (visible_time))
        return visible_time

    def toast_widget_content(self):
        if self.toast_widget_visible():
            return self.get_text(ToastWidget.toast_widget_content)

    def toast_widget_cancel(self):
        if self.toast_widget_visible():
            self.click_element(ToastWidget.toast_widget_close_icon)
            self._info('Toast widget is cancelled..')
    def toast_widget_view_details(self, wait_time=0):
        start_time = time.time()
        while (time.time() - start_time <= wait_time):
            if self.toast_widget_visible():
                if self._is_visible(ToastWidget.toast_widget_view_details):
                    self._info('view details visible')
                    self.click_element(ToastWidget.toast_widget_view_details)
                    break

