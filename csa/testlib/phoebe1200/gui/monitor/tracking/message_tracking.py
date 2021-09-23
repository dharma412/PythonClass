# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/monitor/tracking/message_tracking.py#2 $
# $DateTime: 2019/07/12 08:23:29 $
# $Author: saurgup5 $

import time
import re
import sal.time

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from common.gui.decorators import set_speed
from sal.containers.cfgholder import CfgHolder
from common.util.sarftime import CountDownTimer
from collections import OrderedDict

SERIAL_NO = lambda rows: "//*[@id='resultTable']/tr[%s]/td" % (rows)
MESSAGE_DETAILS_CONTENT = "//*[@id='content']"
GET_MID = lambda mid: \
    "//*[@id='resultTable']/tr/td[contains(.,'MID')]/a[normalize-space()='%s']" % mid
SHOW_DETAILS = lambda mid_loc: \
    "%s/parent::td/following-sibling::td/a[contains(.,'Show Details')]" % mid_loc
URLCATEGORY_COMBO = "//select[@id='url_categories']"
URL_REWRITTEN = "xpath=//input[@id='url_rewritten_by_vof_name']"
VOF_THREAT = "xpath=//input[@id='vof_threat_category_name']"
MACRO_DETECTION_FILE_TYPES = "//select[@id='md_file_types']"
CONTENT_FILTER = "xpath=//input[@id='filter_name']"
ETF_SELECT_SOURCES_LIST = "//select[@id='threatfeeds_sources_list']"
ETF_THREAT_SOURCE_NAME = "xpath=//input[@id='threatfeeds_source_name']"
ADVANCED_CLOSED = '//tbody[@id="adv_closed"]//a/img[@alt="open"]'
ADVANCED_OPENED = '//tbody[@id="adv_open"]//a/img[@alt="close"]'


class MessageTracking(GuiCommon):
    """Message Tracking page interaction class.

    This class designed to interact with GUI elements of Email -> Message
    Tracking -> Message Tracking page. Use keywords, listed below, to manipulate
    with Message Tracking page.
    """

    def get_keyword_names(self):
        return ['message_tracking_search',
                'message_tracking_get_page_count',
                'message_tracking_get_total_result_count',
                'message_tracking_get_message_details', ]

    def _open_page(self):
        self._navigate_to('Monitor', 'Message Tracking')

    def message_tracking_search(self,
                                sender_data=None,
                                sender_comparator=None,
                                rcpt_data=None,
                                rcpt_comparator=None,
                                subject_data=None,
                                subject_comparator=None,
                                mesg_received=None,
                                start_date=None,
                                start_time=None,
                                end_date=None,
                                end_time=None,
                                sender_ip=None,
                                sender_ip_search_options=None,
                                attachment_name=None,
                                attachment_comparator=None,
                                attachment_file_sha256=None,
                                attachment_threat_name=None,
                                message_event=None,
                                dlp_policy=None,
                                url_clicked=None,
                                url_clicked_mailflow_directions=None,
                                vof_threat_category_name=None,
                                url_rewritten_by_vof_name=None,
                                dlp_violation_severities=None,
                                outbreak_filter_options=None,
                                url_category_options=None,
                                mesg_id_header=None,
                                ironport_mid=None,
                                query_timeout=None,
                                max_results=None,
                                macro_detection_mailflow_directions=None,
                                macro_detection_file_types=None,
                                amp_protection_mailflow_directions=None,
                                amp_protection_file_types=None,
                                amp_protection_malicious_file_types=None,
                                content_filter_name=None,
                                content_filters_mail_flow_direction=None,
                                content_filters_action=None,
                                external_threat_feeds_iocs=None,
                                external_threat_feeds_source_type=None,
                                external_threat_feeds_current_sources=None,
                                external_threat_feeds_source_name=None,
                                sender_domain_reputation_types=None):

        """Message Tracking Search.

        Use this method to search for a particular email message or group of
        messages that match specified criteria.

         Parameters:
          - `sender_data`: Envelope Sender, String
          - `sender_comparator`: accepts _Contains_ or _Is_ or _Begins With_or _Is Empty_
          - `rcpt_data`: Envelope Recipient, String
          - `rcpt_comparator`: accepts _Contains_ or _Is_ or _Begins With_
          - `subject_data`: Subject, String
          - `subject_comparator`: accepts _Contains_ or _Is_ or _Begins With_
          - `mesg_received`: time range for the data included: _last day_,
          _last week_ or _custom range_. Default _last day_
          - `start_date`: Start Date if Message Received is 'custom range'
          i.e: '01/17/2012'
          - `start_time`: Start Time if Message Received is 'custom range'
          i.e: '01:20'
          - `end_date`: End Date if Message Received is 'custom range'
          - `end_time`: End Time if Message Received is 'custom range'
          - `sender_ip`: Sender IP Address, String
          - `sender_ip_search_options`: either _rejected_connections_ or
          _messages_. Default _rejected_connections_.
          - `attachment_name`: name of the attachment file, String
          - `attachment_comparator`: accepts _Contains_ or _Is_ or _Begins With_
          - `attachment_file_sha256`: SHA256 checksum of the attachment
          - `attachment_threat_name`: Theat name of the attachment
          - `message_event`: Message Event, Array of Events
            Options are:
                virus positive
                hard bounced
                spam positive
                soft bounced
                suspect spam
                quarantined as spam
                delivered
                currently in outbreak quarantine
                dlp violations
                url categories
                outbreak filters
                advanced malware protection
                graymail
                macro detection
                content filter

          - 'content_filter_name': Name of the content filter
          - 'content_filters_mail_flow_direction': Mail flow directions of content filter
            Options are:
                Incoming
                Outgoing
          - 'content_filters_action': Selects the Stopped action for the content filter

          - `dlp_policy`: DLP Policy Name if message events contain
          dlp violations, String
          - `dlp_violation_severities`: Violation Severities if message events
          contain dlp violations, Array containing either of _critical_, _high_,
          _medium_, _low_
          - `url_clicked`: URL Clicked Name if message events contain
          url click tracking, String
          - `url_clicked_mailflow_directions`: Mail Flow Directions if message events
          contain url click tracking, Array containing either of incoming , outgoing, or both
          - `vof_threat_category_name`: Name of VOF Threat Category
          - `url_rewritten_by_vof_name`: Name of URL rewritten by OF
          - `outbreak_filter_options`: Either url_rewritten_by_of or vof_threat_category or both
          - `url_category_options`: URL Category options will be specified here :
             It can take the following values for different categories(Specify the value for the category you want) :
             adv- Advertisements
             alc- Alcohol
             art-Arts
             astr-Astrology
             auct-Auctions
             busi-Business and Industry
             chat-Chat and Instant Messaging
             plag-Cheating and Plagiarism
             cprn-Child Abuse Content
             csec-Computer Security
             comp-Computers and Internet
             date-Dating
             card-Digital Postcards
             food-Dining and Drinking
             dyn-Dynamic and Residential
             edu-Education
             ent-Entertainment
             extr-Extreme
             fash-Fashion
             fts-File Transfer Services
             filt-Filter Avoidance
             fnnc-Finance
             free-Freeware and Shareware
             gamb-Gambling
             game-Games
             gov-Government and Law
             hack-Hacking
             hate-Hate Speech
             hlth-Health and Nutrition
             lol-Humor
             ilac-Illegal Activities
             ildl-Illegal Downloads
             drug-Illegal Drugs
             infr-Infrastructure and Content Delivery Networks
             voip-Internet Telephony
             job-Job Search
             ling-Lingerie and Swimsuits
             lotr-Lotteries
             cell-Mobile Phones
             natr-Nature
             news-News
             ngo-Non-governmental Organizations
             nsn-Non-sexual Nudity
             comm-Online Communities
             osb-Online Storage and Backup
             trad-Online Trading
             pem-Organizational Email
             park-Parked Domains
             p2p-Peer File Transfer
             pers-Personal Sites
             img-Photo Search and Images
             pol-Politics
             porn-Pornography
             pnet-Professional Networking
             rest-Real Estate
             ref-Reference
             rel-Religion
             saas-SaaS and B2B
             kids-Safe for Kids
             sci-Science and Technology
             srch-Search Engines and Portals
             sxed-Sex Education
             shop-Shopping
             snet-Social Networking
             socs-Social Science
             scty-Society and Culture
             swup-Software Updates
             sprt-Sports and Recreation
             aud-Streaming Audio
             vid-Streaming Video
             tob-Tobacco
             trns-Transportation
             trvl-Travel
             nocat-Uncategorized URLs
             weap-Weapons
             whst-Web Hosting
             tran-Web Page Translation
             mail-Web-based Email
          - `mesg_id_header`: Message ID Header, String
          i.e: '<3aqsgl$38@allison.qa>'
          - `ironport_mid`: IronPort MID, Integer
          i.e: '17'
          - `query_timeout`: Query timeout, either _60_, _120_, _300_, _600_
          and _0_. Default _60_.
          - `max_results`: Max. results returned, either _250_, _500_ or _1000_
          Default _250_.
          - `macro_detection_mailflow_directions`: Mail Flow Direction.
          Incoming or Outgoing. Default - both
          - `macro_detection_file_types`: Supported file types for filtering
          Options are:
            Adobe Portable Document Format
            Archive Files
            OLE File types
            Microsoft Office Files
          - `amp_protection_mailflow_directions`: Mail flow Direction.
          Incoming or Outgoing. Default - both
          - `amp_protection_file_types`: Supported file types for file analysis
          Options are:
            Clean
            Unknown
            Mailicious
            Unscannable
            LowRisk
          - `amp_protection_malicious_file_types`: Supported malicous file types.
          Options are: Valid only when Malicious option is included in amp_protection_file_types
            Malware
            Custom Detection
            Custom Threshold
          - `sender_domain_reputation_types`: Types of sender domain reputation
          to track messages based on reputation.
          Options are:
            Awful
            Poor
            Tainted
            Weak
            Unknown
            Neutral
            Good
            Unscannable
            Not Scanned

         Return:
            A list of objects containing information about email messages.
            Each object has the following attributes:
                - `serial_no`: number of message.
                - `time`: date and time that the esa appliance received the
                message.
                - `sender`: address of the sender in the SMTP envelope
                - `recipient`: addresses of the recipients in the SMTP envelope.
                - `subject`: subject line of the message.
                - `last_state`: last state of message i.e: 'Dropped by antivirus'
                - `mid`: message ID

         Example:
         | @{message_event} | Set Variable | virus positive | graymail |
         | ... | dlp violations | url click tracking | macro detection |
         | ${urls} | Create List | adlt | adv |
         | @{dlp_severities} | Set Variable | high | low |
         | @{url_clicked_mailflow_directions} | Set Variable | incoming | outgoing |
         | @{md_mail_flow_direction} | Set Variable | incoming | outgoing |
         | @{md_file_types} | Set Variable | Microsoft Office Files | OLE File types |
         | @{amp_mail_flow_direction} | Set Variable | incoming | outgoing |
         | @{amp_file_types} | Set Variable | Clean | Malicious | Unknown | Unscannable |
         | @{sdr_types} | Set Variable | Awful | Weak | Unknown | Neutral |
         | ${result_list} = | Message Tracking Search |
         | ... | sender_data=Testing |
         | ... | sender_comparator=Contains |
         | ... | rcpt_data=tests |
         | ... | rcpt_comparator=Begins With |
         | ... | subject_data=Results |
         | ... | subject_comparator=Is |
         | ... | mesg_received=custom range |
         | ... | start_date=01/17/2012 |
         | ... | start_time=01:20 |
         | ... | end_date=01/25/2012 |
         | ... | end_time=10:17 |
         | ... | sender_ip=10.1.88.102 |
         | ... | sender_ip_search_options=messages |
         | ... | attachment_name=test res |
         | ... | attachment_file_sha256= 0b7e4f17727564cdc32b3a725988d53ce676bbff34b89ce1bf9af3df6975cae9 |
         | ... | attachment_threat_name= Win.Dropper.Kuluoz::tpd |
         | ... | attachment_comparator=Contains |
         | ... | message_event=${message_event} |
         | ... | dlp_policy=DLP policy |
         | ... | url_clicked=URL_CLICKED |
         | ... | dlp_violation_severities=${dlp_severities} |
         | ... | url_clicked_mailflow_directions=${url_clicked_mailflow_directions} |
         | ... | url_category_options=${urls} |
         | ... | mesg_id_header=<3aqsgl$38@allison.qa> |
         | ... | ironport_mid=17 |
         | ... | query_timeout=600 |
         | ... | max_results=500 |
         | ... | macro_detection_mailflow_directions=${md_mail_flow_direction} |
         | ... | macro_detection_file_types=${md_file_types} |
         | ... | amp_protection_mailflow_directions=${amp_mail_flow_direction} |
         | ... | amp_protection_file_types=${amp_file_types} |
         | ... | amp_protection_malicious_file_types=${amp_malicous_file_types} |
         | ... | sender_domain_reputation_types=${sdr_types} |
         | @{message_event} | Set Variable | virus positive | url categories |
         | ${urls} | Create List | adlt | adv | sprt |
         | ${result_list} =	| Message Tracking Search |
         | ... |  message_event=${message_event} |
         | ... |  url_category_options=${urls} |
         | Log |  ${result_list} |
        """
        _senderip_options = {'rejected_connections': 'search_type_connections',
                             'messages': 'search_type_messages'
                             }

        self._open_page()
        self._clear_previous_results()

        if sender_data:
            self._fill_mail_data(sender_data, "xpath=//input[@id='sender']",
                                 sender_comparator,
                                 "xpath=//select[@id='sender_match']")

        if rcpt_data:
            self._fill_mail_data(rcpt_data, "xpath=//input[@id='recipient']",
                                 rcpt_comparator,
                                 "xpath=//select[@id='recipient_match']")

        if subject_data:
            self._fill_mail_data(subject_data, "xpath=//input[@id='subject']",
                                 subject_comparator,
                                 "xpath=//select[@id='subject_match']")

        self._fill_mesg_received_data(mesg_received, start_date, start_time,
                                      end_date, end_time)

        # Click on the Advanced arrow to view advanced search options
        self.click_button(ADVANCED_CLOSED, "don't wait")

        if sender_ip:
            self.input_text("xpath=//input[@id='sender_ip']", sender_ip)

        if sender_ip_search_options:
            self._click_radio_button(_senderip_options[sender_ip_search_options])

        if attachment_name:
            self._fill_mail_data(attachment_name, 'attachment',
                                 attachment_comparator, 'attachment_match')

        if attachment_file_sha256:
            self.input_text('xpath=//input[@id="file_sha256"]', attachment_file_sha256)

        if attachment_threat_name:
            self.input_text('xpath=//input[id="spyname"]', attachment_threat_name)

        self._fill_mesg_event_data(message_event, dlp_policy, url_clicked, vof_threat_category_name,
                                   url_rewritten_by_vof_name, dlp_violation_severities, url_clicked_mailflow_directions,
                                   url_category_options, outbreak_filter_options, macro_detection_mailflow_directions,
                                   macro_detection_file_types, amp_protection_file_types,
                                   amp_protection_malicious_file_types,
                                   amp_protection_mailflow_directions, content_filter_name,
                                   content_filters_mail_flow_direction,
                                   content_filters_action, external_threat_feeds_iocs,
                                   external_threat_feeds_source_type,
                                   external_threat_feeds_current_sources, external_threat_feeds_source_name,
                                   sender_domain_reputation_types)

        if mesg_id_header:
            self.input_text("xpath=//input[@id='message_id']", mesg_id_header)

        if ironport_mid:
            self.input_text("xpath=//input[@id='mid']", ironport_mid)

        if query_timeout:
            self.select_from_list("xpath=//select[@id='query_timeout']",
                                  query_timeout)

        if max_results:
            self.select_from_list("xpath=//select[@id='max_results']",
                                  max_results)

        self.click_button("xpath=//input[@id='submitButton']", "don't wait")

        timeout = query_timeout or 60
        tmr = CountDownTimer(int(timeout) + 5).start()
        while tmr.is_active():
            if not self._is_visible("//*/img[contains(@src, 'load')]"):
                break
            time.sleep(1)
        searchlist = SearchResultList(self)
        searchlist._get_results()
        return searchlist

    def _fill_mail_data(self, data, data_locator, comparator=None,
                        comparator_locator=None):
        if comparator:
            if comparator in ['Contains', 'Is', 'Begins With', 'Is Empty']:
                self.select_from_list(comparator_locator, comparator)
            else:
                raise guiexceptions.GuiValueError(
                    "Incorrect comparator %s found" % comparator)
            if comparator != 'Is Empty':
                self.input_text(data_locator, data)
            else:
                self._info('Not able to input text')

    def _clear_previous_results(self):
        timer = sal.time.CountDownTimer(10).start()
        # 'Clear' button is not accessible until the result of the previous
        # search is loaded.
        while timer.is_active():
            if not self._is_text_present('Your query is processing'):
                break
            time.sleep(1.0)

        self.click_button("xpath=//input[@id='clearButton']", "don't wait")

    def _fill_mesg_received_data(self, mesg_received, start_date, start_time,
                                 end_date, end_time):

        mesg_rcpt = {'last day': 'id=timerange_today',
                     'last week': 'id=timerange_week',
                     'custom range': 'id=timerange_custom'
                     }

        if mesg_received and mesg_received.lower() in \
                ['last day', 'last week', 'custom range']:
            self._click_radio_button(mesg_rcpt[mesg_received.lower()])

        if start_date or start_time or end_date or end_time:
            if self._is_checked(mesg_rcpt['custom range']):
                if start_date:
                    self.input_text("xpath=//input[@id='date_from']",
                                    start_date)
                if start_time:
                    self.input_text("xpath=//input[@id='time_from']",
                                    start_time)
                if end_date:
                    self.input_text("xpath=//input[@id='date_to']", end_date)
                if end_time:
                    self.input_text("xpath=//input[@id='time_to']", end_time)

    def _fill_mesg_event_data(self, message_event, dlp_policy, url_clicked, vof_threat_category_name,
                              url_rewritten_by_vof_name, dlp_violation_severities, url_clicked_mailflow_directions,
                              url_category_options, outbreak_filter_options, macro_detection_mailflow_directions,
                              macro_detection_file_types, amp_protection_file_types,
                              amp_protection_malicious_file_types,
                              amp_protection_mailflow_directions, content_filter_name,
                              content_filters_mail_flow_direction,
                              content_filters_action, external_threat_feeds_iocs, external_threat_feeds_source_type,
                              external_threat_feeds_current_sources, external_threat_feeds_source_name,
                              sender_domain_reputation_types):
        message_event_option = {'virus positive': 'id=event_virus',
                                'hard bounced': 'id=event_bhard',
                                'spam positive': 'id=event_spam',
                                'soft bounced': 'id=event_bsoft',
                                'suspect spam': 'id=event_suspect',
                                'quarantined as spam': 'id=event_isq',
                                'delivered': 'id=event_del',
                                'currently in outbreak quarantine': 'id=event_quar',
                                'dlp violations': 'id=event_dlp',
                                'url click tracking': 'id=url_click_track',
                                'url categories': 'id=event_url_cat',
                                'outbreak filters': 'id=vof_filters',
                                'advanced malware protection': 'id=amp',
                                'graymail': 'id=event_gm',
                                'macro detection': 'id=event_md_file_type',
                                'content filters': 'id=content_filters',
                                'dane failure': 'id=event_dane_fail',
                                'external threat feeds': 'id=event_threatfeeds',
                                'sender domain reputation': 'id=event_sdr',
                                }

        of_options = {'url_rewritten_by_of': 'id=url_rewritten_by_vof',
                      'vof_threat_category': 'id=vof_threat_category'
                      }
        dlp_severity = {'critical': 'id=dlp_severity_critical',
                        'high': 'id=dlp_severity_high',
                        'medium': 'id=dlp_severity_medium',
                        'low': 'id=dlp_severity_low'
                        }
        mail_direction = {'incoming': 'id=mail_direction_incoming',
                          'outgoing': 'id=mail_direction_outgoing'
                          }
        macro_detection_mail_flow = {
            'incoming': 'id=macro_type_incoming',
            'outgoing': 'id=macro_type_outgoing'}

        etf_iocs = {
            'file hash': 'id=event_threatfeeds_file_hash',
            'url': 'id=event_threatfeeds_url'}

        etf_select_sources = {'all': 'tf_source_choice0',
                              'current': 'tf_source_choice1',
                              'specific_source': 'tf_radio_source_name'
                              }

        amp_protection_mail_flow = {
            'incoming': 'id=incoming_amp',
            'outgoing': 'id=outgoing_amp'
        }

        amp_file_types = {'clean': 'id=event_file_clean',
                          'malicious': {
                              'xpath': 'id=event_amp',
                              'malicious_file_types': {
                                  'malicious malware': 'id=event_file_rep_malware',
                                  'malicious custom detection': 'id=event_file_scd',
                                  'malicious custom threshold': 'id=event_file_ct',
                              }
                          },
                          'unknown': 'id=event_file_unknown',
                          'unscannable': 'id=event_file_unscannable',
                          'lowrisk': 'id=event_file_lowrisk'
                          }
        content_filters_mail_flow = {
            'incoming': 'id=content_filter_type_incoming',
            'outgoing': 'id=content_filter_type_outgoing'
        }
        content_filters_action_stopped = {
            'stopped': 'id=stopped'
        }
        sdr_types = {
            'awful': 'id=event_sdr_awful',
            'poor': 'id=event_sdr_poor',
            'tainted': 'id=event_sdr_tainted',
            'weak': 'id=event_sdr_weak',
            'unknown': 'id=event_sdr_unknown',
            'neutral': 'id=event_sdr_neutral',
            'good': 'id=event_sdr_good',
            'unscannable': 'id=event_sdr_unscannable',
            'not_scanned': 'id=event_sdr_not_scanned',
        }

        if message_event:
            for event in message_event:
                self.click_element(message_event_option[event.lower()],
                                   "don't wait")
        if dlp_policy and self._is_checked(
                message_event_option['dlp violations']):
            self.input_text("xpath=//input[@id='dlp_policy']", dlp_policy)
        if url_clicked and self._is_checked(
                message_event_option['url click tracking']):
            self.input_text("xpath=//input[@id='url_clicked']", url_clicked)
        if vof_threat_category_name and self._is_checked(
                message_event_option['outbreak filters']):
            self.select_checkbox(of_options['vof_threat_category'.lower()])
            self.input_text(VOF_THREAT, vof_threat_category_name)
        if url_rewritten_by_vof_name and self._is_checked(
                message_event_option['outbreak filters']):
            self.select_checkbox(of_options['url_rewritten_by_of'.lower()])
            self.input_text(URL_REWRITTEN, url_rewritten_by_vof_name)
        if dlp_violation_severities and self._is_checked(
                message_event_option['dlp violations']):
            for severity in dlp_violation_severities:
                self.select_checkbox(dlp_severity[severity.lower()])
        if url_clicked_mailflow_directions and self._is_checked(
                message_event_option['url click tracking']):
            for severity in url_clicked_mailflow_directions:
                self.select_checkbox(mail_direction[severity.lower()])
        if outbreak_filter_options and self._is_checked(
                message_event_option['outbreak filters']):
            for option in outbreak_filter_options:
                self.select_checkbox(of_options[option.lower()])
        if url_category_options and self._is_checked(
                message_event_option['url categories']):
            for category in url_category_options:
                self.select_from_list(URLCATEGORY_COMBO, category)
        if self._is_checked(message_event_option['macro detection']):
            if macro_detection_mailflow_directions:
                for direction in macro_detection_mailflow_directions:
                    self.select_checkbox(macro_detection_mail_flow[direction.lower()])
            if macro_detection_file_types:
                for file_type in macro_detection_file_types:
                    self.select_from_list(MACRO_DETECTION_FILE_TYPES, file_type)
        if self._is_checked(message_event_option['external threat feeds']):
            if external_threat_feeds_iocs:
                for ioc in external_threat_feeds_iocs:
                    self.select_checkbox(etf_iocs[ioc.lower()])
            if external_threat_feeds_source_type:
                self._click_radio_button(etf_select_sources[external_threat_feeds_source_type])
            if external_threat_feeds_current_sources:
                for current_source in external_threat_feeds_current_sources:
                    self.select_from_list(ETF_SELECT_SOURCES_LIST, current_source)
            if external_threat_feeds_source_name:
                self.input_text(ETF_THREAT_SOURCE_NAME, external_threat_feeds_source_name)
        if self._is_checked(message_event_option['advanced malware protection']):
            if amp_protection_mailflow_directions:
                for direction in amp_protection_mailflow_directions:
                    self.select_checkbox(amp_protection_mail_flow[direction.lower()])
            if amp_protection_file_types:
                for file_type in amp_protection_file_types:
                    if file_type.lower() == 'malicious':
                        self.select_checkbox(amp_file_types['malicious']['xpath'])
                        if amp_protection_malicious_file_types:
                            for malicious_file_type in amp_protection_malicious_file_types:
                                self.select_checkbox(amp_file_types['malicious'][
                                                         'malicious_file_types'][
                                                         malicious_file_type.lower()])
                    else:
                        self.select_checkbox(amp_file_types[file_type.lower()])
        if self._is_checked(message_event_option['content filters']):
            if content_filters_mail_flow_direction:
                for mail_flow_direction in content_filters_mail_flow_direction:
                    self.select_checkbox(content_filters_mail_flow[mail_flow_direction.lower()])
            if content_filters_action:
                for filter_actions in content_filters_action:
                    self.select_checkbox(content_filters_action_stopped[filter_actions.lower()])
            if content_filter_name:
                self.input_text(CONTENT_FILTER, content_filter_name)
        if self._is_checked(message_event_option['sender domain reputation']):
            if sender_domain_reputation_types:
                for sdr_type in sender_domain_reputation_types:
                    self.select_checkbox(sdr_types[sdr_type.lower()])

    def message_tracking_get_page_count(self, result_list):
        """Message Tracking Get Page Count.

        Use this method to get page count with message results

         Parameters:
          - `result_list`: a list of object containing information about email
          messages, which are returned by `Message Tracking Search` keyword

         Return:
            A value of page count.

         Example:
         | ${page_count} = | Message Tracking Get Page Count |
         | ... | ${result_list} |
         """
        return result_list.get_page_count()

    def message_tracking_get_total_result_count(self, result_list):
        """Message Tracking Get Total Result Count.

        Use this method to get count of total results

         Parameters:
          - `result_list`: a list of object containing information about email
          messages, which are returned by `Message Tracking Search` keyword

         Return:
            A value of total result count.

         Example:
         | ${result_count} = | Message Tracking Get Total Result Count |
         | ... | ${result_list} |
         """
        return result_list.get_total_result_count()

    def _wait_for_page(self, title_part, timeout_sec=10):
        timer = CountDownTimer(timeout_sec).start()
        while timer.is_active():
            titles = self.get_window_titles()
            for title in titles:
                if title.find(title_part) >= 0:
                    return title
            time.sleep(1)
        raise guiexceptions.GuiPageNotFoundError(
            'Page title containing "%s" has not been found' \
            ' within %d seconds timeout' % (title_part, timeout_sec))

    def _open_message_details_window(self, mid):
        mid_loc = GET_MID(mid)
        if not self._is_element_present(mid_loc):
            raise guiexceptions.GuiValueError \
                ('Could not find message with MID %s using locator %s' % (mid, mid_loc))
        self.click_element(SHOW_DETAILS(mid_loc), "don't wait")
        message_details_window = self._wait_for_page("Message Details")
        self.select_window(message_details_window)

    @set_speed(0)
    def _get_rows(self, rows_num, func, reverse=False):
        data = OrderedDict()
        for row in xrange(1, rows_num + 1):
            tr = func(row)
            if self._is_element_present(tr):
                key = self.get_text("%s//th" % (tr,)).strip(':')
                val = self.get_text("%s//td" % (tr,))
                if reverse:
                    data[val] = key
                else:
                    data[key] = val
        return data

    def message_tracking_get_message_details(self,
                                             mid,
                                             continue_search=None,
                                             get_message_details=True,
                                             get_processing_details=True,
                                             get_last_event=True,
                                             close_window=True, ):
        """
        Gets message details for given MID.

        *Parameters*:
        - `mid`: The MID of the message to get details.
        - `continue_search`: Extend the search timeframe to investigate more details.
        Available options are:
        | 3 weeks |
        | 1 month |
        | 2 months |
        | 3 months |
        | 6 months |
        | Entire Data Range |
        - `get_message_details`: Get Message Details datalist. Boolean. ${True} by default.
        - `get_processing_details`: Get Processing Details datalist. Boolean. ${True} by default.
        - `get_last_event`: Get Last Event from Processing Details datalist. Boolean. ${True} by default.
        - `close_window`: Close Message Details window. Boolean. ${True} by default.

        *Return*:
        Dictionary (CfgHolder that allows to access items using '.' dot).
        Dictionary has following keys:
        |                    | Type        | Key     | Value     |
        | last_event         | OrderedDict | Event   | Timestamp |
        | message_details    | OrderedDict | Header  | Value     |
        | processing_details | OrderedDict | Event   | Timestamp |

        Each dictionary above is an OrderedDict.
        This allows to get items preserving the order of insertion,
        thus gives a possibility to verify events of message processing.
        To get sequence of message events use: ${res.processing_details.keys()}

        *Example*:
        | ${res}= | Message Tracking Get Message Details | 4 | continue_search=3 months |
        | Log Dictionary | ${res} |
        | Log Dictionary | ${res.last_event} |
        | Log Dictionary | ${res.message_details} |
        | Log Dictionary | ${res.processing_details} |
        | Log List | ${res.processing_details.keys()} |
        | Log List | ${res.message_details.items()} |
        | Should Contain | ${res.last_event.keys()} | Message ${mid} quarantined in Spam Quarantine. |
        """
        message_details_loc = \
            "%s//dl[contains(dt, 'Message Details')]" % (MESSAGE_DETAILS_CONTENT,)
        processing_details_loc = \
            "%s//dl[contains(dt, 'Processing Details')]" % (MESSAGE_DETAILS_CONTENT,)
        self._open_message_details_window(mid)
        result = CfgHolder()
        if continue_search:
            self.select_from_list \
                ("//*[@id='continue_search']", continue_search)
            self.click_button \
                ("//*[@type='button' and @value='Continue Search']")
        if get_message_details:
            message_details_rows_num = \
                int(self.get_matching_xpath_count("%s//tr" % (message_details_loc,)))
            message_detail_row = lambda x: \
                "%s//tr[%s][not(contains(@class, 'group'))]" % (message_details_loc, x)
            result.message_details = \
                self._get_rows(message_details_rows_num, message_detail_row)
        if get_processing_details:
            processing_details_rows_num = \
                int(self.get_matching_xpath_count("%s//tr" % (processing_details_loc,)))
            processing_detail_row = lambda x: \
                "%s//tr[%s][not(contains(@style, 'border'))]" % (processing_details_loc, x)
            result.processing_details = \
                self._get_rows(processing_details_rows_num, processing_detail_row, reverse=True)
        if get_last_event:
            last_event = self.get_text \
                ("%s//tr//span[contains(@style,'background-color')]" % (processing_details_loc,))
            last_event_timestamp = self.get_text \
                ("%s//tr//span[contains(@style,'background-color')]/parent::td/preceding-sibling::th" % (
                processing_details_loc,))
            result.last_event = {last_event: last_event_timestamp}
        if close_window:
            if "message details" in self.get_title().lower():
                self.close_window()
        self.select_window('main')
        return result


class SearchResultList(object):

    def __init__(self, gui):
        self.result_list = {}
        self.gui = gui

    def __str__(self):
        return ', '.join(['%s=%s' % (k, v) for k, v in self.result_list.iteritems()])

    def get_page_count(self):
        page_html = self.gui.get_source()
        if re.search("Displaying [0-9]+", page_html):
            if re.search("Page [0-9]+", page_html):
                page = int(re.findall("Page [0-9]+ of ([0-9]+)", page_html)[0])
                return page
            else:
                return 1
        else:
            return 0

    def get_total_result_count(self):
        count = 0
        for page in self.result_list.keys():
            count = count + len(self.result_list[page])
        return count

    @set_speed(0, 'gui')
    def get_results_on_page(self, page=None):
        time_stamp = lambda rows: "//tbody[@id='resultTable']/tr[%s]/td[2]/a" % (rows)
        mid = lambda rows: "//tbody[@id='resultTable']/tr[%s]/td[3]/a" % (rows)
        sender = lambda rows: "//tbody[@id='resultTable']/tr[%s]/td[2]/table/tbody/tr/td[2]" % rows
        recipient = lambda rows: "//tbody[@id='resultTable']/tr[%s]/td[2]/table/tbody/tr[2]/td[2]" % rows
        subject = lambda rows: "//tbody[@id='resultTable']/tr[%s]/td[2]/table/tbody/tr[3]/td[2]" % rows
        last_state = lambda rows: "//tbody[@id='resultTable']/tr[%s]/td[2]/table/tbody/tr[4]/td[2]" % rows

        if page:
            # if page is greater than total pages raise error
            if page > self.get_page_count():
                raise guiexceptions.GuiValueError("Invalid page")
            # go to required page
            self._go_to_page(page)
        result_list = []
        rows = int(self.gui.get_matching_xpath_count(
            "//tbody[@id='resultTable']/tr"))
        while rows:
            result = CfgHolder()
            result.serial_no = self.gui.get_text(SERIAL_NO(rows - 1))
            result.time = self.gui.get_text(time_stamp(rows - 1))
            result.mid = self.gui.get_text(mid(rows - 1))
            result.sender = self.gui.get_text(sender(rows))
            result.recipient = self.gui.get_text(recipient(rows))
            result.subject = self.gui.get_text(subject(rows))
            result.last_state = self.gui.get_text(last_state(rows))
            rows = rows - 2
            result_list.append(result)
        return result_list

    def _go_to_page(self, page):
        html_page = self.gui.get_source()
        if len(self.result_list.keys()) == 1:
            return None
        else:
            current_page = int(re.findall("Page ([0-9]+)", html_page)[0])
            if current_page == page:
                return None
            if current_page > page:
                while current_page != page:
                    self._go_back()
                    current_page = int(re.findall("Page ([0-9]+)", html_page)[0])
                return None
            if current_page < page:
                while current_page != page:
                    self._go_next()
                    current_page = int(re.findall("Page ([0-9]+)", html_page)[0])
                return None

    def _get_results(self):
        pages = self.get_page_count()
        if pages == 0:
            self.gui._info("No results found.")
            return
        for page in range(pages):
            self.result_list[str(page + 1)] = self.get_results_on_page()
            if page < (pages - 1):
                self._go_next()

    def _go_back(self):
        back_page_link = "link=Previous"
        try:
            self.gui.click_element(back_page_link, "don't wait")
            time.sleep(5)
        except:
            # Reached the first page
            pass

    def _go_next(self):
        next_page_link = "link=Next"
        try:
            self.gui.click_element(next_page_link, "don't wait")
            time.sleep(5)
        except:
            # Reached the last page
            pass
