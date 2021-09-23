from common.gui.decorators import visit_page
from common.ngui.ngguicommon import NGGuiCommon
from common.gui.guiexceptions import InvalidUrlPathError, GuiFeatureDisabledError, GuiValueError
from common.ngui.exceptions import ElementNotFoundError, DataNotFoundError, UserInputError
from quarantine_def import CustomRange
from quarantine_def import QUARANTINE
import time

MSG_INFO_ROW = '//div[@class=\'ui-grid-canvas\']/div'
MSG_INFO_COLUMN = lambda row, column: '%s[%s]/div/div[%s]/div/div[2]' % (MSG_INFO_ROW, row, column)
MSG_INFO_COLUMN_SUB = lambda row, column: '%s[%s]/div/div[%s]/div/a' % (MSG_INFO_ROW, row, column)
MSG_INFO_COLUMN_LAST = lambda row, column: '%s[%s]/div/div[%s]/div' % (MSG_INFO_ROW, row, column)
class Quarantine(NGGuiCommon):

    def get_keyword_names(self):
        return ['spam_quarantine_search', 'spam_quarantine_delete', 'spam_quarantine_release', 'go_to_quarantine', 'go_to_quarantine_nowait']

    def _check_quarantine_is_disabled(self):
        try:
            self.element_should_not_be_visible(QUARANTINE.QUARANTINE_DISABLED)
        except Exception:
            self._info('Quarantine is disabled.')
            raise GuiFeatureDisabledError

    def _get_all_msgs_on_current_page(self, columns):
        rows_num = int(self.get_matching_xpath_count(MSG_INFO_ROW))
        msg_list = []
        for row in xrange(1, rows_num + 1):
            msg_dict = {}
            for column, name in enumerate(columns, 2):
                if column not in (5,6,7):
                    msg_dict[name] = self.get_text(MSG_INFO_COLUMN(row, column))
                elif column == 5:
                    msg_dict[name] = self.get_text(MSG_INFO_COLUMN_SUB(row, column))
                else:
                    msg_dict[name] = self.get_text(MSG_INFO_COLUMN_LAST(row, column))
            msg_list.append(msg_dict)
        return msg_list

    def _retrieve_all_msgs(self, is_admin):
        if is_admin:
            columns = ('from', 'rcpt_to', 'to', 'subject', 'date' , 'size')
        else:
            columns = ('from', 'subject', 'date', 'size')

        msg_list = self._get_all_msgs_on_current_page(columns)
        return msg_list

    @visit_page(QUARANTINE.QUARANTINE_HEADER_XPATH, QUARANTINE.QUARANTINE_URL_PATH)
    def spam_quarantine_search(self,
                              mesg_received='Today', from_date=None, from_time=None, to_date=None,
                              wheretype=None,
                              subject=None,
                              type_name=None,
                              envelope_type=None,
                              envelope_input=None,
                              is_admin=True):
        self.wait_for_angular()
        self._check_quarantine_is_disabled()
        self.click_button(QUARANTINE.CLEAR_SEARCH)
        if mesg_received:
            if QUARANTINE.QUARANTINE_RECIEVED_OPTIONS.has_key(mesg_received):
                self.click_element(QUARANTINE.QUARANTINE_RECIEVED_OPTIONS[mesg_received])
                if mesg_received == 'Custom Range':
                    if from_date:
                        self.select_date_on_calendar_widget(CustomRange.from_date_select, from_date)
                    if to_date:
                        self.select_date_on_calendar_widget(CustomRange.to_date_select, to_date)
            else:
                raise UserInputError("Invalid option provided:%s : \
                Available options:Today,Last 7 days,Custom Range"%mesg_received)
        self.wait_for_angular()

        if wheretype:
            self._info('Selecting type:%s' % (wheretype))
            self.select_custom_dropdown(QUARANTINE.QUARANTINE_SEARCH_WHERETYPE,wheretype)
        self.wait_for_angular()
        if subject:
            self._info('Selecting subject:%s' % (subject))
            self.select_custom_dropdown(QUARANTINE.QUARANTINE_SEARCH_WHERESUBJECT,subject)
        self.wait_for_angular()
        if type_name:
            self.input_text(QUARANTINE.QUARANTINE_SEARCH_WHERE_INPUT,type_name)
        self.wait_for_angular()
        if envelope_type:
            self._info('Selecting recipient:%s' % (envelope_type))
            self.select_custom_dropdown(QUARANTINE.QUARANTINE_SEARCH_ENVELOPE_TYPE,envelope_type)
        self.wait_for_angular()
        if envelope_input:
            self.input_text(QUARANTINE.QUARANTINE_SEARCH_ENVELOPE_INPUT,envelope_input)
        self.click_button(QUARANTINE.SEARCH_BUTTON)
        self.wait_for_angular()
        return self._retrieve_all_msgs(is_admin)

    def spam_quarantine_delete(self,
                              mesg_received='Today', from_date=None, from_time=None, to_date=None,
                              wheretype=None,
                              subject=None,
                              type_name=None,
                              envelope_type=None,
                              envelope_input=None,
                              is_admin=True):

        self.spam_quarantine_search(mesg_received=mesg_received,
                              from_date=from_date,
                              from_time=from_time,
                              to_date=to_date,
                              wheretype=wheretype,
                              subject=subject,
                              type_name=type_name,
                              envelope_type=envelope_type,
                              envelope_input=envelope_input,
                              is_admin=is_admin)
        self.wait_for_angular()
        time.sleep(5)
        self.select_ngsma_checkbox(QUARANTINE.SELECT_ALL)
        self.click_element(QUARANTINE.DELETE_BUTTON)
        self.click_element(QUARANTINE.CONFIRM_BUTTON)
        self.wait_for_angular()

    def spam_quarantine_release(self,
                              mesg_received='Today', from_date=None, from_time=None, to_date=None,
                              wheretype=None,
                              subject=None,
                              type_name=None,
                              envelope_type=None,
                              envelope_input=None,
                              is_admin=True):

        self.spam_quarantine_search(mesg_received=mesg_received,
                              from_date=from_date,
                              from_time=from_time,
                              to_date=to_date,
                              wheretype=wheretype,
                              subject=subject,
                              type_name=type_name,
                              envelope_type=envelope_type,
                              envelope_input=envelope_input,
                              is_admin=is_admin)
        self.wait_for_angular()
        time.sleep(5)
        self.select_ngsma_checkbox(QUARANTINE.SELECT_ALL)
        self.click_element(QUARANTINE.RELEASE_BUTTON)
        self.click_element(QUARANTINE.CONFIRM_BUTTON)
        self.wait_for_angular()

    @visit_page(QUARANTINE.QUARANTINE_HEADER_XPATH, QUARANTINE.QUARANTINE_URL_PATH)
    def go_to_quarantine(self):
        """
        This keyword to navigate to the Quarantine page
        :return:
        """
        self._info('Navigated to Quarantine page')

    @visit_page(QUARANTINE.QUARANTINE_HEADER_XPATH, QUARANTINE.QUARANTINE_URL_PATH, wait=False)
    def go_to_quarantine_nowait(self):
        self._info('Navigated to Quarantine page with nowait')
