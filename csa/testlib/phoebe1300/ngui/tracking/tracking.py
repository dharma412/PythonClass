# imports
from common.constants import CONSTANTS

MESSAGE_TRACKING = CONSTANTS()

# Menu
MESSAGE_TRACKING.TRACKING_URL_PATH = 'tracking/search'
MESSAGE_TRACKING.TRACKING_HEADER_XPATH = "//a[@translate='header.message_tracking']"
MESSAGE_TRACKING.TRACKING_DISABLED = "//span[@translate='message-tracking.tracking_disabled']"

# Input text
MESSAGE_TRACKING.ATTACHMENT = "//*[@id='inputId_message-tracking.search.attachment']"
MESSAGE_TRACKING.ATTACHMENT_FILE_SHA_256 = "//*[@name='sha' and @type='text']"
MESSAGE_TRACKING.ATTACHMENT_THREAT_NAME = "//*[@name='threatName' and @type='text']"
MESSAGE_TRACKING.SENDER_XPATH = "//*[@id='inputId_message-tracking.search.sender']"
MESSAGE_TRACKING.ENVELOPE_RECIPIENT = "//*[@id='inputId_message-tracking.search.envelope_recipient']"
MESSAGE_TRACKING.SUBJECT = "//*[@id='inputId_message-tracking.search.subject']"
MESSAGE_TRACKING.REPLY_TO = "//*[@id='inputId_message-tracking.search.reply_to']"
MESSAGE_TRACKING.CONTENT_FILTER_NAME = "//*[@name='content_filter_name' and @type='text']"
MESSAGE_TRACKING.DLP_POLICY_NAME = "//*[@name='dlp_policy_name' and @type='text']"
MESSAGE_TRACKING.DMARC_FROM_DOMAIN = "//*[@name='dmark_label_name' and @type='text']"
MESSAGE_TRACKING.ETF_SOURCE = "//*[@name='etf_source_name' and @type='text']"
MESSAGE_TRACKING.FED_EXECUTIVE_NAME = "//*[@name='executive_name' and @type='text']"
MESSAGE_TRACKING.MESSAGE_FILTER = "//*[@name='message_filters' and @type='text']"
MESSAGE_TRACKING.OUTBREAK_FILTERS_URL_REWRITTEN = "//*[@name='outbreakFilters.urlRewrittenByOf' and @type='text']"
MESSAGE_TRACKING.OUTBREAK_FILTERS_VOF_THREAT_CATEGORY = "//*[@name='outbreakFilters.vofThreatCategory' and @type='text']"
# Outbreak filter text yet to add
MESSAGE_TRACKING.WEB_INTERACTION_URL_CLICKED = "//*[@name='web_interaction_label_name' and @type='text']"

# Advance search
MESSAGE_TRACKING.ADVANCE_SEARCH_PATH = "$ctrl.toggleAdvancedSearch()"
MESSAGE_TRACKING.MESSAGE_ID_HEADER_XPATH = "//input[@name='messageIdHeader']"
MESSAGE_TRACKING.CISCO_MID_XPATH = "//input[@name='mid']"
MESSAGE_TRACKING.SENDER_IP_XPATH = "//input[@name='senderIp']"

# Button
MESSAGE_TRACKING.SEARCH_BUTTON = "//*[@id='controlBtn_search0']"
MESSAGE_TRACKING.CLEAR_BUTTON = "//*[@id='controlBtn_search1']"

# DROPDOWN
MESSAGE_TRACKING.SENDER_OPTION = "//*[@class='quarantine-search__envelope ng-scope ng-isolate-scope']"

MESSAGE_TRACKING.ATTACHMENT_COMPARATOR = "//*[@id='quarantine-search_subject_message-tracking.search.attachment']"
MESSAGE_TRACKING.SENDER_COMPARATOR = "//*[@id='quarantine-search_subject_message-tracking.search.sender']"
MESSAGE_TRACKING.ENVELOPE_RECIPIENT_COMPARATOR = "//*[@id='quarantine-search_subject_message-tracking.search.envelope_recipient']"
MESSAGE_TRACKING.SUBJECT_COMPARATOR = "//*[@id='quarantine-search_subject_message-tracking.search.subject']"
MESSAGE_TRACKING.REPLY_TO_COMPARATOR = "//*[@id='quarantine-search_subject_message-tracking.search.reply_to']"

## EVENT Expandable Card
MESSAGE_TRACKING.MESSAGE_EVENT = "//*[@card-title=\"'%s'\"]/div/div/i"
MESSAGE_TRACKING.AMP_EVENT = 'advancedMalwareProtection'
MESSAGE_TRACKING.CONTENT_FILTERS = 'contentFilters'
MESSAGE_TRACKING.DLP_VIOLATIONS_EVENT = 'dlpViolations'
MESSAGE_TRACKING.DMARC_EVENT = 'dmarc'
MESSAGE_TRACKING.ETF_EVENT = 'externalThreatFeeds'
MESSAGE_TRACKING.FED_EVENT = 'forgedEmailDetection'
MESSAGE_TRACKING.GEO_LOCATION = 'geoLocation'
MESSAGE_TRACKING.MACRO_FILE_TYPE = 'macroFileTypeDetected'
MESSAGE_TRACKING.MESSAGE_FILTERS_EVENT = 'messageFilters'
MESSAGE_TRACKING.SMIME_EVENT = 'smime'
MESSAGE_TRACKING.SDR_EVENT = 'senderDomainReputation'
MESSAGE_TRACKING.URL_CATEGORIES_EVENT = 'urlCategories'
MESSAGE_TRACKING.WEB_INTERACTION_TRACKING_EVENT = 'webInteractionTracking'

# Event Checkboxes
MESSAGE_TRACKING.DANE_FAILURE = "//*[@field-name='daneFailure']"
MESSAGE_TRACKING.DELIVERED = "//*[@field-name='message_delivered']"
MESSAGE_TRACKING.GRAYMAIL = "//*[@field-name='graymail']"
MESSAGE_TRACKING.HARD_BOUNCED = "//*[@field-name='hardBounced']"
MESSAGE_TRACKING.MESSAGES_WITH_MALICIOUS_URL = "//*[@field-name='containedMaliciousUrls']"
MESSAGE_TRACKING.MESSAGES_WITH_NEUTRAL_URL = "//*[@field-name='containedNeutralUrls']"
MESSAGE_TRACKING.IN_OUTBREAK_QUARANTINE = "//*[@field-name='inOutbreakQuarantine']"
MESSAGE_TRACKING.SAFE_PRINT = "//*[@field-name='safeprintExt']"
MESSAGE_TRACKING.SOFT_BOUNCED = "//*[@field-name='softBounced']"
MESSAGE_TRACKING.SPAM_POSITIVE = "//*[@field-name='spamPositive']"
MESSAGE_TRACKING.IN_SPAM_QUARANTINE = "//*[@field-name='quarantinedAsSpam']"
MESSAGE_TRACKING.SUSPECT_SPAM = "//*[@field-name='suspectSpam']"
MESSAGE_TRACKING.VIRUS_POSITIVE = "//*[@field-name='virusPositive']"

# outbreakFilters not unique
MESSAGE_TRACKING.OUTBREAK_FILTERS_EVENT = "$ctrl.expandOnCheck(\\'outbreakFilters\\')"
MESSAGE_TRACKING.IN_POLICY_OR_VIRUS_QUARANTINE = "$ctrl.expandOnCheck('quarantinedTo')"

MESSAGE_TRACKING.MESSAGE_RECIEVED_OPTIONS = {'Today': "//*[@id='today0']",
                                             'Last 7 days': "//*[@id='seven_days1']",
                                             'Custom Range': "//*[@id='custom_range2']"}


class AmpMailFlowDirection:
    Incoming = "//*[@field-name='advancedMalwareProtection.mailflow_direction.incoming']"
    Outgoing = "//*[@field-name='advancedMalwareProtection.mailflow_direction.outgoing']"


class AmpDispositions:
    Clean = "//*[@field-name='advancedMalwareProtection.amp_dispositions.amp_clean']"
    Malicious = "//*[@field-name='advancedMalwareProtection.amp_dispositions.amp_malicious']"
    Unknown = "//*[@field-name='advancedMalwareProtection.amp_dispositions.amp_unknown']"
    Unscannable = "//*[@field-name='advancedMalwareProtection.amp_dispositions.amp_unscannable']"
    LowRisk = "//*[@field-name='advancedMalwareProtection.amp_dispositions.amp_lowrisk']"
    Malicious_Malware = "//*[@field-name='advancedMalwareProtection.amp_dispositions.amp_malware']"
    Malicious_Custom_Detection = "//*[@field-name='advancedMalwareProtection.amp_dispositions.amp_cd']"
    Malicious_Custom_Threshold = "//*[@field-name='advancedMalwareProtection.amp_dispositions.amp_ct']"


class ContentFiltersMailFlowDirection:
    Inbound = "//*[@field-name='contentFilters.mailflow_direction_cf.inbound']"
    Outbound = "//*[@field-name='contentFilters.mailflow_direction_cf.outbound']"


class ContentFiltersAction:
    Stopped = "//*[@field-name='contentFilters.content_filter.stopped']"


class DlpViolationSeverities:
    Critical = "//*[@field-name='dlpViolations.violation_severities.critical']"
    High = "//*[@field-name='dlpViolations.violation_severities.high']"
    Medium = "//*[@field-name='dlpViolations.violation_severities.medium']"
    Low = "//*[@field-name='dlpViolations.violation_severities.low']"


class DlpAction:
    Delivered = "//*[@field-name='dlpViolations.dlp_action.delivered']"
    Encrypted = "//*[@field-name='dlpViolations.dlp_action.encrypted']"
    Dropped = "//*[@field-name='dlpViolations.dlp_action.dropped']"


class DmarcAction:
    Passed = "//*[@field-name='dmarc.action.passed']"
    Failed = "//*[@field-name='dmarc.action.failed']"


class EtfSelectIocs:
    FileHash = "//*[@field-name='externalThreatFeeds.etf_select_iocs.file_hash']"
    URL = "//*[@field-name='externalThreatFeeds.etf_select_iocs.url']"
    Domain = "//*[@field-name='externalThreatFeeds.etf_select_iocs.domain']"


class GeoLocation:
    No_Country_Info = "//*[@field-name='geoLocation..No_Country_Info']"
    Unknown_Country = "//*[@field-name='geoLocation..Unknown_Country']"
    Private_IP_Address = "//*[@field-name='geoLocation..Private_IP_Addresses']"
    Country_list = "//*[@for='checkbox_%s']"


class MacroMailFlowDirection:
    Inbound = "//*[@field-name='macroFileTypeDetected.mailflow_direction_mftd.inbound']"
    Outbound = "//*[@field-name='macroFileTypeDetected.mailflow_direction_mftd.outbound']"


class MacroFileTypes:
    Filetypes = "//*[@for='checkbox_%s']"


class InPolicyOrVirusQuarantine:
    Non_Existance_Quarantine_radio = "//*[@id ='radio_0' and @title='Non-Existing Quarantine Name']"
    Quarantine_list_radio = "//*[@id ='radio_3' and @title='Quarantine List']"
    Quarantine_list = "//*[@for='checkbox_%s']"


class OutbreakFilters:
    URL_Rewritten = "$ctrl.outBreakToggle($ctrl.isurlRewrittenByOfCheckbox,'urlRewritten')"
    VOF_Threat_Category = "$ctrl.outBreakToggle($ctrl.vofThreatCategoryCheckbox,'vofThreatCategory')"


class S_Mime:
    S_MIME_Verification_Decryption_Successful = "//*[@field-name='smime..smime_successful']"
    S_MIME_Verification_Decryption_Failed = "//*[@field-name='smime..smime_failed']"


class URLCategories:
    url_category = "//*[@for='checkbox_%s']"


class WebInteractionTrackingMailflowDirection:
    Inbound = "//*[@field-name='webInteractionTracking.mailflow_direction_wit.inbound']"
    Outbound = "//*[@field-name='webInteractionTracking.mailflow_direction_wit.outbound']"


class SearchResult:
    total_count = 'ng-bind=$ctrl.totalCount'
    result_table_details = "//*[@id='message-tracking-results__table-details%s']"
    message_status = "//*[@id='message-tracking-results__table-details%s']/div/div/div/div"
    expand_button = "//*[@id='message-tracking-results__collapse%s']"
    timestamp = "//*[@id='message-tracking-results__table-details%s']/div/div/span[2]/span"
    message_checkbox = "/div/div/div/ngsma-search-result-checkbox"
    policy_match_header = "//*[@id='message-tracking-results__table-details%s']/div/div/span[3]/span[1]"
    policy_match_value = "//*[@id='message-tracking-results__table-details%s']/div/div/span[3]/span[2]"
    sender_values = "//*[@id='message-tracking-results__table-details%s']/div[2]/div/div[%s]"
    tracking_result_verdict_header = "//*[@id='message-tracking-results__verdictsTable%s']/tbody/tr/td/li/div[1]"
    tracking_result_verdict_values = "//*[@id='message-tracking-results__verdictsTable%s']/tbody/tr/td/li/div[3]"

    message_mid = "/div/div/span/div"

    message = "//*[@ng-repeat='(rowRenderIndex, row) in rowContainer.renderedRows track by $index']/div/div/div/div/div"

    message_tracking_details = "div/button"

    # == > span1 mid , span2 timestamp span3 policy
    # //id="message-tracking-results__collapse1"

    # values = //*[@ng-repeat='(rowRenderIndex, row) in rowContainer.renderedRows track by $index']/div/div/div/div[2]/div/div/span
    # header //*[@ng-repeat='(rowRenderIndex, row) in rowContainer.renderedRows track by $index']/div/div/div/div[2]/div/div/p


class SearchResultRemediate:
    Remediate_button = '$ctrl.showRemediateActions()'
    batch_name = "//*[@name='batchName']"
    batch_description = "//textarea[@name='description']"
    delete_email_radio_button = "//*[@id='radioDelAction']"
    forward_email_to_radio_button = "//*[@id='radioFwdAction']"
    delete_and_forward_radio_button = "//*[@id='radioFwdDelAction']"
    forward_email_address = "ng-model=$ctrl.fwdEmail"
    delete_and_forward_email_address = "ng-model=$ctrl.delFwdEmail"
    apply = "$ctrl.remediateBatch()"
