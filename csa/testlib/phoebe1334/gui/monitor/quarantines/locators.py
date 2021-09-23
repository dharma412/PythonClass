#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/monitor/quarantines/locators.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

## Locators

QUARANTINES_TABLE="//table[@class='cols']"

# Add/Edit quarantine
QUARANTINE_ADD_BUTTON = "//*[@value='Add Policy Quarantine...']"
QUARANTINE_DELETE_LINK = lambda row: "%s/tbody/tr[%s]/td[7]/img" % (QUARANTINES_TABLE,row)
QUARANTINE_DELETE_CONFIRM_BUTTON = "//*[@type='button' and text()='Delete']"
QUARANTINE_DELETE_CANCEL_BUTTON = "//*[@type='button' and text()='Cancel']"
QUARANTINE_NAME = "//*[@name='name']"
QUARANTINE_SPACE = "//*[@name='sizeMB']"
QUARANTINE_RETAIN_PERIOD = "//*[@name='period']"
QUARANTINE_RETAIN_PERIOD_UNITS_GETVAL = "//*[@name='periodUnits']"
QUARANTINE_RETAIN_PERIOD_UNITS =lambda opt: "//select[@name='periodUnits']/option[contains(text(),'%s')]" % opt
QUARANTINE_DEFAULT_ACTION =lambda action: "//*[@id='defaultAction_%s']" % action
QUARANTINE_MOD_SUBJ_ENABLE = "//*[@id='modify_subj']"
QUARANTINE_FREE_UP_SPACE = "//*[@id='automatic_action']"

QUARANTINE_MOD_SUBJ_ON_RELEASE = "//*[@id='tagSetting']"
QUARANTINE_MOD_SUBJ_TAG =lambda tag: "//*[@id='tagSetting']/option[@value='%s']" % tag
QUARANTINE_TAG_SUBJ_ON_RELEASE = "//*[@id='tagText']"
QUARANTINE_X_HEADER_ENABLE = "//*[@id='add_xheader']"
QUARANTINE_X_HEADER_NAME = "//*[@id='xheadName']"
QUARANTINE_X_HEADER_VALUE = "//*[@id='xheadText']"
QUARANTINE_STRIP_ATTACHMENTS_ON_RELEASE = "//*[@id='strip_attachments']"

QUARANTINE_USERS_LINK = "//*[@id='users_dialog_link']"
QUARANTINE_EXT_GROUPS_LINK = "//*[@id='groups_dialog_link']"
QUARANTINE_CUSTOM_ROLES_LINK = "//*[@id='custom_roles_dialog_link']"

QUARANTINE_USERS_DIALOG = "//*[@id='users_dialog']"
QUARANTINE_EXT_GROUPS_DIALOG = "//*[@id='groups_dialog']"
QUARANTINE_CUSTOM_ROLES_DIALOG = "//*[@id='custom_roles_dialog']"

QUARANTINE_DIALOGS_OK_BUTTON = lambda dialog: "%s//*[@type='button' and text()='OK']" % dialog
QUARANTINE_DIALOGS_CANCEL_BUTTON = lambda dialog: "%s//*[@type='button' and text()='Cancel']" % dialog

# Spam Quarantine locators
SPAM_QUARANTINE_ENABLE_DISABLE = "//*[@id='enabled']"
SPAM_QUARANTINE_OUT_OF_LIMIT_ACTION = "//*[@name='out_of_limit_action']"
SPAM_QUARANTINE_ENABLE_SCHEDULED_DELETE = lambda x: "//*[@id='disable_time_expire_%s']" % x
SPAM_QUARANTINE_SCHEDULED_DELETE_TTL = "//*[@id='message_ttl']"
SPAM_QUARANTINE_NOTIFY_IRONPORT_ON_MESSAGE_RELEASE = "//*[@id='to_corpus']"
SPAM_QUARANTINE_LOGO_CURRENT = "//*[@id='current_logo_id']"
SPAM_QUARANTINE_LOGO_IRONPORT = "//*[@id='default_logo_id']"
SPAM_QUARANTINE_LOGO_CUSTOM = "//*[@id='custom_logo_id']"
SPAM_QUARANTINE_LOGO_PATH = "//*[@id='upload_container']/input"
SPAM_QUARANTINE_LOGIN_PAGE_MESSAGE = "//*[@name='custom_login_message']"
SPAM_QUARANTINE_EUQ_ENABLE = "//*[@id='enable_end_user_access']"
SPAM_QUARANTINE_EUQ_AUTH_TYPE = "//*[@id='authentication']"
SPAM_QUARANTINE_EUQ_MAILBOX = lambda method: "//*[@id='method_%s']" % method
SPAM_QUARANTINE_EUQ_MAILBOX_SERVER = "//*[@name='server']"
SPAM_QUARANTINE_EUQ_MAILBOX_CONNECTION = "//*[@id='transport']"
SPAM_QUARANTINE_EUQ_MAILBOX_SERVER_PORT = "//*[@id='port']"
SPAM_QUARANTINE_EUQ_MAILBOX_APPEND_DOMAIN = "//*[@name='default_domain']"
SPAM_QUARANTINE_EUQ_MAILBOX_TEST_USER = "//*[@name='test_user']"
SPAM_QUARANTINE_EUQ_MAILBOX_TEST_PASSWORD = "//*[@name='test_password']"
SPAM_QUARANTINE_EUQ_HIDE_MESSAGE_BODIES = "//*[@id='hide_message_bodies']"
SPAM_QUARANTINE_EUQ_MAILBOX_TEST_BUTTON = "//*[@id='section_test']/table/tbody/tr[1]/th/input"
SPAM_QUARANTINE_NOTIFICATION_ENABLE = "//*[@id='enable_notification']"
SPAM_QUARANTINE_NOTIFICATION_FRIENDLY_USERNAME = "//*[@name='from_friendlyname']"
SPAM_QUARANTINE_NOTIFICATION_FROM_USERNAME = "//*[@name='from_username']"
SPAM_QUARANTINE_NOTIFICATION_FROM_DOMAIN = "//*[@name='from_domain']"
SPAM_QUARANTINE_NOTIFICATION_TO_ALL_USERS = "//*[@id='notifyToAllUsers']"
SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_USERS = "//*[@id='notifyToIncludeLdapQuery']"
SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_GROUP_QUERY = "//*[@id='ldapQuery']"
SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_GROUP_NAME = "//*[@id='ldapGroup']"
SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_USER_ADD_BTN = "//*[@id='btnAdd']"
SPAM_QUARANTINE_NOTIFICATION_TO_LDAP_USER_DEL_BTN = "//*[@id='btnDeleteUser']"
SPAM_QUARANTINE_NOTIFICATOIN_TO_CURRENT_QUERY_LIST = "//*[@id='queryGroupList[]']"
SPAM_QUARANTINE_NOTIFICATOIN_TO_CURRENT_QUERY_LIST_ALL = "//*[@id='queryGroupList[]']/option"
SPAM_QUARANTINE_NOTIFICATION_TO_EXCLUDE_LDAP_USERS = "//*[@id='notifyToExcludeLdapQuery']"
SPAM_QUARANTINE_NOTIFICATION_SUBJECT = "//*[@id='subject']"
SPAM_QUARANTINE_NOTIFICATION_TITLE = "//*[@id='title']"
SPAM_QUARANTINE_NOTIFICATION_LANGUAGE = "//*[@id='language']"
SPAM_QUARANTINE_NOTIFICATION_TEMPLATE = "//*[@id='template']"
SPAM_QUARANTINE_NOTIFICATION_FORMAT = "//*[@id='format']"
SPAM_QUARANTINE_NOTIFICATION_AUTO_LOGIN = "//*[@id='enable_auto_login']"
SPAM_QUARANTINE_NOTIFICATION_BOUNCE_ADDR = "//*[@id='bounce_address']"
SPAM_QUARANTINE_NOTIFICATION_CONSOLIDATE = "//*[@id='enable_alias_consolidation']"
SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_MONTHLY = "//*[@id='monthly']"
SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_WEEKLY = "//*[@id='weekly']"
SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAILY = "//*[@id='specificdays']"
SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAY = "//*[@id='single_day_picker']"
SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_DAILY_DAYS = lambda day: "//*[@id='multi_days_picker_%s']" % day
SPAM_QUARANTINE_NOTIFICATION_SCHEDULE_HOUR = lambda hour: "//*[@id='time_picker_%s00']" % hour

SPAM_QUARANTINE_DISABLE_CONFIRM_DIALOG = "//*[@id='confirmation_dialog']"
SPAM_QUARANTINE_DISABLE_CONFIRM_DIALOG_CONTINUE_BUTTON = "%s//button[text()='Continue']" % SPAM_QUARANTINE_DISABLE_CONFIRM_DIALOG
SPAM_QUARANTINE_DISABLE_CONFIRM_DIALOG_CANCEL_BUTTON = "%s//button[text()='Cancel']" % SPAM_QUARANTINE_DISABLE_CONFIRM_DIALOG

COMMON_CONFIRM_DIALOG = "//*[@id='confirmation_dialog']"
COMMON_CONFIRM_OK_CANCEL_BUTTON = lambda text: "%s//button[text()='%s']" % (COMMON_CONFIRM_DIALOG, text)

SPAM_QUARANTINE_USERS_LINK = "//*[@id='adminusers_dialog_link']"
SPAM_QUARANTINE_EXT_GROUPS_LINK = "//*[@id='external_admin_groups_dialog_link']"
SPAM_QUARANTINE_CUSTOM_ROLES_LINK = "//*[@id='custom_roles_dialog_link']"

SPAM_QUARANTINE_USERS_DIALOG = "//*[@id='adminusers_dialog']"
SPAM_QUARANTINE_EXT_GROUPS_DIALOG = "//*[@id='external_admin_groups_dialog']"
SPAM_QUARANTINE_CUSTOM_ROLES_DIALOG = "//*[@id='custom_roles_dialog']"

# Search locators
# Search table
QUARANTINE_SEARCH_TABLE = "//*[@id='search']"
QUARANTINE_SEARCH_TABLE_RESULTS_CONTAINER = "//table[@class='full-width']"
QUARANTINE_SEARCH_TABLE_MESSAGE_LIST_CONTAINER = "//*[@id='message_list']"
QUARANTINE_SEARCH_TABLE_MESSAGE_LIST = "//*[@id='message_list']//tbody[@class='yui-dt-data']"
QUARANTINE_SEARCH_TABLE_CELL_DATA = lambda locator, row_idx,col_idx: "%s//tr[%s]/td[%s]" % (locator, row_idx, col_idx)
QUARANTINE_SEARCH_TABLE_QUERY = "//*[@id='search_query']"
QUARANTINE_SEARCH_TABLE_BUTTON = "//*[@name='search']"
QUARANTINE_SEARCH_TABLE_ITEMS_PER_PAGE = "//select[@title='Rows per page' and contains(@id, 'pg0-0')]"
QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION = "//*[@id='messageActionList']"
QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_ON_ALL = "//*[@id='action_on_all']"
QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_MORE = "//*[@id='more_actions']"
QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_DELETE ="//*[@id='delete_btn']"
QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_RELEASE = "//*[@id='release_btn']"
QUARANTINE_SEARCH_TABLE_MESSAGE_ACTION_SUBMIT = "//*[@type='button' and @value='Submit']"
QUARANTINE_SEARCH_TABLE_COPY_DIALOG = "//*[@id='copy_dlg']"
QUARANTINE_SEARCH_TABLE_COPY_DIALOG_COPY_RECIPIENTS = "//*[@id='copy_recipients']"
QUARANTINE_SEARCH_TABLE_MOVE_DIALOG = "//*[@id='move_dlg']"
QUARANTINE_SEARCH_TABLE_MOVE_DIALOG_DST = "//*[@id='move_dst']"
QUARANTINE_SEARCH_TABLE_HANLDE_DIALOG_OK_CANCEL_BUTTON = lambda locator, text: "%s//button[text()='%s']" % (locator, text)
QUARANTINE_SEARCH_TABLE_SELECT_ALL_MIDS = "//*[@id='mid']"
QUARANTINE_SEARCH_TABLE_SORT_BY_SENDER = "//a[text()='Sender']"
QUARANTINE_SEARCH_TABLE_SORT_BY_SENDER = "//a[text()='Subject']"
QUARANTINE_SEARCH_TABLE_SORT_BY_SENDER = "//a[text()='Received']"
QUARANTINE_SEARCH_TABLE_SORT_BY_SENDER = "//a[text()='Scheduled Exit']"
QUARANTINE_SEARCH_TABLE_SORT_BY_SENDER = "//a[text()='Size']"
QUARANTINE_SEARCH_TABLE_VIEW_ALL_MESSAGES_BUTTON = "//*[@id='view_all']"
QUARANTINE_SEARCH_TABLE_PAGER_BAR = "//*[@id='dt-pag-nav-top']"
QUARANTINE_SEARCH_TABLE_ACTION_BAR = "//div[@class='action-bar']"

SEARCH_QUARANTINE_SEARCH_ACROSS_BUTTON = "//*[@type='button' and @value='Search Across Quarantines']"

# Search quarantine page (Search Quarantine button pressed)
SEARCH_QUARANTINE_CONTENT_TABLE = "//*[@id='content']"
SEARCH_QUARANTINE_IN = "%s//select[@name='name']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_RECEIVED = lambda x: "//*[@id='%s']" % x
SEARCH_QUARANTINE_RECEIVED_START = "//*[@id='period_start']"
SEARCH_QUARANTINE_RECEIVED_END = "//*[@id='period_end']"
SEARCH_QUARANTINE_ENVELOPE_SENDER_METHOD = "//select[@name='senderMethod']"
SEARCH_QUARANTINE_ENVELOPE_SENDER_TEXT = "%s//*[@name='senderText']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_ENVELOPE_RCPT_METHOD = "%s//select[@name='recipientMethod']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_ENVELOPE_RCPT_TEXT = "%s//*[@name='recipientText']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_SUBJECT_METHOD = "%s//select[@name='subjectMethod']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_SUBJECT_TEXT = "%s//*[@name='subjectText']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_ATTACHMENT_TEXT = "%s//*[@name='attachment_name']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_ATTACHMENT_SIZE_CONDITION = "%s//*[@id='size_condition']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_ATTACHMENT_SIZE_1 = "%s//*[@id='size1']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_ATTACHMENT_SIZE_2 = "%s//*[@id='size2']" % SEARCH_QUARANTINE_CONTENT_TABLE

SEARCH_QUARANTINE_ITEMS_PER_PAGE = "%s//*[@name='pageSize']" % SEARCH_QUARANTINE_CONTENT_TABLE
SEARCH_QUARANTINE_SEARCH_BUTTON = "//*[@type='submit' and @value='Search']"
SEARCH_QUARANTINE_SUBMIT_BUTTON = "//*[@type='button' and @value='Submit']"

QUARANTINES_SEARCH_ACROSS_SELECT = "//*[@id='all_quarantines0']"
QUARANTINES_SEARCH_ACROSS_ALL = "//*[@id='all_quarantines1']"
QUARANTINES_SEARCH_ACROSS_SELECT_MULTIPLE = "//*[@id='quarantines']"

# Quarantined message locator
MESSAGE_FORM = "//*[@id='msgform']"
MESSAGE_DETAILS_HEADERS = "//*[@id='msg_headers']"
MESSAGE_DETAILS_BODY = "//*[@id='msg_body']"
MESSAGE_DETAILS_RCPT_COPY_EMAIL = "//*[@id='customEmail']"
MESSAGE_DETAILS_RCPT_COPY_BUTTON = "//*[@name='CopyTo']"
MESSAGE_DETAILS_RESCAN_MESSAGE = "//*[@name='Rescan']"
MESSAGE_DETAILS_SELECT_ALL_QUARANTINES = "//*[@id='mids']"
MESSAGE_DETAILS_SELECT_QUARANTINE = lambda x: "//*[@id='%s']" % x
MESSAGE_DETAILS_MESSAGE_ACTION_LIST = "//*[@id='messageActionList']"
MESSAGE_DETAILS_MESSAGE_ACTION_SUBMIT = "//*[@type='button' and @value='Submit']"
MESSAGE_DETAILS_BACK_BUTTON = "//*[@name='Back']"
MESSAGE_DETAILS_MESSAGE_PARTS_TABLE = "//*[@id='content']//table[@class='cols'][2]"

COMMON_SUBMIT_BUTTON = "//*[@type='button' and @value='Submit']"

# Spam Quarantine
SPAM_QUARANTINE_TODAY_RANGE = "//*[@id='date1']"
SPAM_QUARANTINE_LAST_WEEK_RANGE = "//*[@id='date2']"
SPAM_QUARANTINE_DATES_RANGE = "//*[@id='date3']"
SPAM_QUARANTINE_DATE_RANGE = ("//*[@id='date_from']", "//*[@id='date_to']")
SPAM_QUARANTINE_DATES_RANGE_FROM = "//*[@id='date_from']"
SPAM_QUARANTINE_DATES_RANGE_TO = "//*[@id='date_to']"

SPAM_QUARANTINE_SEARCH_TABLE_RESULTS_CONTAINER = "//*[@id='quarantine_container']//tbody[@class='yui-dt-data']"
SPAM_QUARANTINE_SEARCH_TABLE_ITEMS_PER_PAGE = "//*[@id='pageSize']"
SPAM_QUARANTINE_SEARCH_TABLE_PAGER_BAR = "//*[@class='pager-bar']"
SPAM_QUARANTINE_SEARCH_FIELD = "//select[@name='search_field']" # From, To, Subject
SPAM_QUARANTINE_SEARCH_KIND = "//select[@name='search_kind']" # Contains, Is, Begins with,Ends, Does not contain
SPAM_QUARANTINE_SEARCH_TERMS = "//input[@name='ignore_escapes:search_terms']"
SPAM_QUARANTINE_ENV_RECIPIENT_SEARCH_KIND = "//select[@name='recipient_kind']"# Contains, Is, Begins with,Ends, Does not contain
SPAM_QUARANTINE_ENV_RECIPIENT_SEARCH_TERMS = "//input[@name='ignore_escapes:recipient_text']"
SPAM_QUARANTINE_CLEAR_SEARCH =  "//a[text()='Clear Search']"
SPAM_QUARANTINE_ADVANCED_SEARCH = "//a[contains(.,'Advanced Search')]"
SPAM_QUARANTINE_RELEASE_BUTTON = "//*[@id='release_selected1']"
SPAM_QUARANTINE_DELETE_BUTTON = "//*[@id='delete_selected1']"

SPAM_QUARANTINE_ACTION = "//*[@id='message_action1']"
SPAM_QUARANTINE_ACTION_SUBMIT_BUTTON ="//*[@id='process_selected1']"

SPAM_QUARANTINE_SEARCH_TABLE_SELECT_ALL_MIDS = "//*[@name='toggle_msg' and @value='mid[]']"
SPAM_QUARANTINE_ITEMS_FOUND = "//div[@class='action-bar']//td[contains(.,'items found')]"

SPAM_QUARANTINE_CONFIRM_DIALOG = "//*[@id='confirm_dialog']"
SPAM_QUARANTINE_CONFIRM_OK_CANCEL_BUTTON = lambda text: "%s//*[@value='%s']" % (SPAM_QUARANTINE_CONFIRM_DIALOG, text)

SPAM_MESSAGE_DETAILS_BACK_LINK = "//a[contains(.,'Back to messages')]"
SPAM_MESSAGE_DETAILS_RELEASE_BUTTON = "//*[@type='submit' and @value='Release']"
SPAM_MESSAGE_DETAILS_DELETE_BUTTON = "//*[@type='button' and @value='Delete']"
SPAM_MESSAGE_DETAILS_TABLE = "//table[@class='pairs']"

SPAM_QUARANTINE_QUICK_SEARCH_TEXTFIELD = "//[@name='ignore_escapes:criterion']"
SPAM_QUARANTINE_QUICK_SEARCH_BUTTON = "//[@name='button_simple']"

#SLBL
SLBL_TABLE = "//table[@class='pairs']"
SLBL_ENABLE_BUTTON = "//*[@name='slbl_enable' and @value='Enable...']"
SLBL_ENABLE_DISABLE = "//*[@id='enable_slbl']"
SLBL_BLOCK_LIST_ACTION = "//*[@id='slbl_blocklist_action']"
SLBL_MAX_ENTRIES = "//*[@id='max_slbl_entries']"
SLBL_EDIT_BUTTON = "//*[@value='Edit Settings...' and @name='slbl_enable']"

# Outbreak Manage By Rule
OUTBREAK_MANAGE_BY_RULE_SUMMARY_LINK = "%s//a[text()='Manage by Rule Summary']" % QUARANTINES_TABLE
OUTBREAK_MANAGE_BY_RULE_TABLE_RESULTS_CONTAINER = "//table[2][@class='cols']"

__all__ = [attr for attr in globals().keys() if attr[0]!='_']
