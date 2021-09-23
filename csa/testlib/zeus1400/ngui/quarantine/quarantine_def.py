from common.constants import CONSTANTS

QUARANTINE = CONSTANTS()

QUARANTINE.QUARANTINE_URL_PATH       = 'quarantine/search'
QUARANTINE.QUARANTINE_HEADER_XPATH   = "//a[@translate='header.message_quarantine']"
QUARANTINE.QUARANTINE_DISABLED       = "//span[@translate='tracking.spamDisabled']"


QUARANTINE.QUARANTINE_RECIEVED_OPTIONS = {'Today': "//*[@id='today0']",
                                          'Last 7 days': "//*[@id='seven_days1']",
                                          'Custom Range': "//*[@id='custom_range2']"}
QUARANTINE.SEARCH_BUTTON = "//*[@id='controlBtn_search0']"
QUARANTINE.CLEAR_SEARCH = "//*[@id='controlBtn_clear_search1']"
QUARANTINE.DELETE_BUTTON = "//*[@id='deleteSelectedFile']"
QUARANTINE.RELEASE_BUTTON = "//*[@id='releaseSelectedFile']"
QUARANTINE.CONFIRM_BUTTON = "//md-dialog-actions/button[2]"

#DROPDOWN
QUARANTINE.QUARANTINE_SEARCH_WHERETYPE = "//*[@id='quarantine-search_whereType']"
QUARANTINE.QUARANTINE_SEARCH_WHERESUBJECT = "//*[@id='quarantine-search_whereSubject']"
QUARANTINE.QUARANTINE_SEARCH_ENVELOPE_TYPE = "//*[@id='quarantine-search_subject']"

#INPUT TEXT
QUARANTINE.QUARANTINE_SEARCH_WHERE_INPUT = "//*[@id='quarantine-search__input__where']"
QUARANTINE.QUARANTINE_SEARCH_ENVELOPE_INPUT = "//*[@id='quarantine-search_inputEnvelope']"
class CustomRange:
    from_date_select = "//*[@id='fromdataTimWidget']//*[@aria-label='Open calendar']"

#CHECKBOX
QUARANTINE.SELECT_ALL = '//*[@is-header="true"]'
