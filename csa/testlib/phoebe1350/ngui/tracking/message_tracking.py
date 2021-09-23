# imports
from common.gui.decorators import visit_page
from common.ngui.ngguicommon import NGGuiCommon
from common.gui.guiexceptions import InvalidUrlPathError, GuiFeatureDisabledError
from tracking import MESSAGE_TRACKING, AmpDispositions, AmpMailFlowDirection
from tracking import ContentFiltersMailFlowDirection, ContentFiltersAction, \
    DlpViolationSeverities, DlpAction, DmarcAction, EtfSelectIocs, GeoLocation, MacroMailFlowDirection, \
    MacroFileTypes, InPolicyOrVirusQuarantine, OutbreakFilters, URLCategories, WebInteractionTrackingMailflowDirection

from tracking import SearchResult, SearchResultRemediate
from tracking import RejectedConnections, RejectedConnectionsSearchResult

import time


class Tracking(NGGuiCommon):

    def get_keyword_names(self):
        return ['message_tracking_search', 'message_tracking_get_message_details', \
                'clear_tracking_search', 'message_tracking_remediate', \
                'message_tracking_search_rejected_connections', \
                'message_tracking_rejected_connections_get_message_details']

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
                                amp_protection_mailflow_directions=None,
                                amp_protection_dispositions=None,
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
                                web_interaction_tracking_mailflow_direction=None):
        """Message Tracking Search.

                Use this method to search for a particular email message or group of
                messages that match specified criteria.
        Usage:
         Message Tracking search        subject_data=Testing
        ...      subject_comparator=Begins with
        """

        self._check_tracking_is_disabled()
        if mesg_received:
            if MESSAGE_TRACKING.MESSAGE_RECIEVED_OPTIONS.has_key(mesg_received):
                self.click_element(MESSAGE_TRACKING.MESSAGE_RECIEVED_OPTIONS[mesg_received])
                if mesg_received == 'Custom Range':
                    if from_date:
                        # from date drop down
                        pass
                    if from_time:
                        # from time drop down
                        pass
                    if to_date:
                        # to date drop down
                        pass
                    if to_time:
                        # to time drop down
                        pass
            else:
                print "Invalid option.."

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

        # Advance options ...
        self.click_ng_button(MESSAGE_TRACKING.ADVANCE_SEARCH_PATH, 'Advanced Search')

        if mesg_id_header:
            self.input_text(MESSAGE_TRACKING.MESSAGE_ID_HEADER_XPATH, mesg_id_header)
        if sender_ip:
            self.input_text(MESSAGE_TRACKING.SENDER_IP_XPATH, sender_ip)
        if cisco_mid:
            self.input_text(MESSAGE_TRACKING.CISCO_MID_XPATH, cisco_mid)

        if amp_protection_mailflow_directions or amp_protection_dispositions:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.AMP_EVENT))
            for mail_flow in amp_protection_mailflow_directions:
                self.click_element(getattr(AmpMailFlowDirection, mail_flow))
            for amp_disposition in amp_protection_dispositions:
                self.click_element(getattr(AmpDispositions, amp_disposition))

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

        if s_mime:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.SMIME_EVENT))
            for smime_option in s_mime:
                self.select_custom_checkbox(getattr(S_Mime, smime_option))

        if safeprint:
            self.select_custom_checkbox(MESSAGE_TRACKING.SAFE_PRINT)

        if sdr_verdicts or sdr_threat_categories:
            self.click_element(MESSAGE_TRACKING.MESSAGE_EVENT % (MESSAGE_TRACKING.SDR_EVENT))
            # need to add sdr categories..

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

        self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
        self.wait_for_angular()

    def clear_tracking_search(self):
        """
        To clear the tracking search
        usage:
        Message Tracking search        geo_location=${geo_location}
        ...         geo_location_country_list=${geo_location_country_list}
        clear_tracking_search
        :return:
        """
        if MESSAGE_TRACKING.TRACKING_URL_PATH not in self.get_location():
            raise InvalidUrlPathError
        self.click_button(MESSAGE_TRACKING.CLEAR_BUTTON)
        self.wait_for_angular()

    def message_tracking_get_message_details(self):
        """
        To get the message tracking detail of the searched messages
        :return:  all messages in the search.. with key of mid and values of other fields data in that
        usage:
        {details}=     message_tracking_get_message_details
        LogMany    ${details}
        Log     ${details['20']}
        """

        mid_data = {}
        sender_options_range = 7
        self.wait_for_angular()
        if MESSAGE_TRACKING.TRACKING_RESULTS_PATH not in self.get_location():
            raise InvalidUrlPathError

        for tracking_message_result in range(int(self.get_text(SearchResult.total_count))):
            tmp_data = {}
            tmp_data['mid'] = self.get_text(
                SearchResult.result_table_details % (tracking_message_result) + SearchResult.message_mid)
            tmp_data['status'] = self.get_text(SearchResult.message_status % (tracking_message_result))
            tmp_data['timestamp'] = self.get_text(SearchResult.timestamp % (tracking_message_result))
            tmp_data[self.get_text(SearchResult.policy_match_header % (tracking_message_result))] = \
                self.get_text(SearchResult.policy_match_value % (tracking_message_result))
            for sender_options in range(1, sender_options_range):
                text_value = self.get_text(SearchResult.sender_values % (tracking_message_result, sender_options))
                header = text_value.split('\n')[0]
                value = text_value.split('\n')[1]
                tmp_data[header] = value
            try:
                self.click_element(SearchResult.expand_button % (tracking_message_result))
                verdict_header = self.find(SearchResult.tracking_result_verdict_header % (tracking_message_result),
                                           first_only=False)
                verdict_values = self.find(SearchResult.tracking_result_verdict_values % (tracking_message_result),
                                           first_only=False)
                verdict_dict = {}
                for header, values in zip(verdict_header, verdict_values):
                    verdict_dict[self.get_text(header)] = self.get_text(values)
                tmp_data['verdicts'] = verdict_dict
            except Exception as error:
                print "ERROR:Expand button is not visible ", error
            mid_data[tmp_data['mid']] = tmp_data
        return mid_data

    @visit_page(MESSAGE_TRACKING.TRACKING_HEADER_XPATH, MESSAGE_TRACKING.TRACKING_URL_PATH)
    def message_tracking_remediate(self, mid=None, batch_name=None, \
                                   description=None, delete_email=None,
                                   forward_email_address=None,
                                   delete_and_forward_email_address=None, ):
        """
        This keyword to remediate the mail after the tracking search
        :param mid: MID
        :param batch_name: name of batch
        :param description: description to search
        :param delete_email: delete email
        :param forward_email_address: forward email address field
        :param delete_and_forward_email_address: delete and email address field
        :return:
        usage:
        message_tracking_remediate       mid=62
        ...         batch_name=Test
        ...         description=welcome desc
        ...         delete_email=${True}
        """
        self.click_ng_button(MESSAGE_TRACKING.ADVANCE_SEARCH_PATH, 'Advanced Search')
        self.input_text(MESSAGE_TRACKING.CISCO_MID_XPATH, mid)
        self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
        self.wait_for_angular()
        for tracking_message_result in range(int(self.get_text(SearchResult.total_count))):
            current_mid = self.get_text(
                SearchResult.result_table_details % (tracking_message_result) + SearchResult.message_mid)
            if int(current_mid) == int(mid):
                self.select_ngsma_search_result_checkbox(
                    SearchResult.result_table_details % (tracking_message_result) + SearchResult.message_checkbox)
        self.wait_for_angular()

        self.click_ng_button(SearchResultRemediate.Remediate_button, 'Remediate')
        time.sleep(3)
        if batch_name:
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

        self.click_ng_button(SearchResultRemediate.apply, 'Apply')

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
                        # from date drop down
                        pass
                    if from_time:
                        # from time drop down
                        pass
                    if to_date:
                        # to date drop down
                        pass
                    if to_time:
                        # to time drop down
                        pass
            else:
                print "Invalid option.."

        if sender_ip:
            self.input_text(RejectedConnections.sender_ip_address, sender_ip)
        self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
        self.wait_for_angular()

    def _get_rejected_connections_details(self):
        icid_data = {}
        self.element_should_be_visible(RejectedConnectionsSearchResult.message_details)
        self.set_selenium_speed('0.25s')
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

    def message_tracking_rejected_connections_get_message_details(self, wait_time=None):
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
        if wait_time and wait_time >=0 :
            start_time =time.time()
            while (int(time.time()-start_time) <= int(wait_time)):
                details = self._get_rejected_connections_details()
                self.click_ng_button(MESSAGE_TRACKING.MODIFY,  'Modify')
                self.click_button(MESSAGE_TRACKING.SEARCH_BUTTON)
                self.wait_for_angular()
                print "time.time()-start_time", time.time()-start_time
        else:
            details = self._get_rejected_connections_details()

        return details