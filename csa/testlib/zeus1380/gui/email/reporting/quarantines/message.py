#!/usr/bin/env python

from locators import *
from qcommon import QuarantinesCommon
from sal.containers.cfgholder import CfgHolder
from js_templates import js
import warnings

class QuarantinedMessage(QuarantinesCommon):
    """
    Class to work with separate quarantined message.
    Works with already opened messages.
    """
    def _go_back(self, go_back=True):
        if go_back:
            if self._is_element_present(MESSAGE_DETAILS_BACK_BUTTON):
                self.click_button(MESSAGE_DETAILS_BACK_BUTTON)

    def _select_quarantine(self, name=None, all=False):
        # first unselect all checkboxes
        # select-unselect ALL should clear all checkboxes
        self._select_checkbox(MESSAGE_DETAILS_SELECT_ALL_QUARANTINES)
        self._unselect_checkbox(MESSAGE_DETAILS_SELECT_ALL_QUARANTINES)
        # select quarantine by its name or all
        if all:
            self._select_checkbox(MESSAGE_DETAILS_SELECT_ALL_QUARANTINES)
        else:
            for _name in self._convert_to_tuple(name):
                self._select_checkbox(MESSAGE_DETAILS_SELECT_QUARANTINE(_name))

    def quarantines_message_get_details(self, go_back=True):
        """
        Return message details as it is seen in WUI.

        Works with already opened message.
        Use keyword `Quarantines Search Message` or `Quarantines Search Message By Mid`
        to find and open message.

        *Parameters*:
        - `go_back`: Boolean. Press "Back To Messages List" button or not. True by default.

        *Return*:
        Dictionary(CfgHolder).
        | _Keys_     | _Values types_        |
        | headers    | String                |
        | body       | String                |
        | sender     | String                |
        | recipients | String                |
        | subject    | String                |
        | parts      | Dictionary(CfgHolder) |

        *Exceptions*:
        None

        *Examples*:
        In this example we use `Quarantines Search Message` to find and open message in quarantine.
        | ${res}=  Quarantines Search Message |
        | ... | name=Virus |
        | ... | search_in=Virus |
        | ... | sender_rule=matches exactly |
        | ... | sender_text=test@mail.qa |
        | ... | received=last hour |
        | ... | recipient_rule=matches exactly |
        | ... | recipient_text=ahrytski@mail.qa |
        | Log | ${res} |
        | ${details}= | Quarantines Message Get Details |
        | Log Dictionary | ${details} |
        | Should Be Equal | ${details.sender} | me@mail.qa |
        | Should Be Equal | ${details.recipients} | you@mail.qa |
        | Should Be Equal | ${details.subject} | some subject string |
        """
        # stripping white spaces in sender, recipients, subject is dangerous???
        details = CfgHolder()
        details.headers = self.get_text(MESSAGE_DETAILS_HEADERS)
        details.body = self.get_text(MESSAGE_DETAILS_BODY)
        details.sender = self.get_text("%s//tr[contains(.,'Sender')]" % \
                                       MESSAGE_FORM).split(':',1)[1]
        details.recipients = self.get_text("%s//tr[contains(.,'Recipients')]" % \
                                           MESSAGE_FORM).split(':',1)[1]
        details.subject = self.get_text("%s//tr[contains(.,'Subject')]" % \
                                        MESSAGE_FORM).split(':',1)[1]
        if self._is_element_present(MESSAGE_DETAILS_MESSAGE_PARTS_TABLE):
            cols_num = int(self.get_matching_xpath_count("%s//tr[2]/th" %\
                                    MESSAGE_DETAILS_MESSAGE_PARTS_TABLE))
            cols_names = [self.get_text("%s//tr[2]/th[%s]" % \
            (MESSAGE_DETAILS_MESSAGE_PARTS_TABLE, col)) \
            for col in xrange(1, cols_num+1)]
            rows_num = int(self.get_matching_xpath_count\
            ("%s//tr" % MESSAGE_DETAILS_MESSAGE_PARTS_TABLE))
            rowno = 3
            details.parts = []
            while rowno <= rows_num:
                tmp = CfgHolder()
                for col_name in cols_names:
                    tmp.__setattr__\
                    (self._normalize(col_name),
                    self.get_text("%s//tr[%s]/td[%s]" % \
                    (MESSAGE_DETAILS_MESSAGE_PARTS_TABLE, rowno,
                    cols_names.index(col_name)+1)))
                details.parts.append(tmp)
                rowno+=1
            self._go_back(go_back=go_back)
        return details

    def quarantines_message_send_copy(self, rcpt=None, go_back=True):
        """
        Send copy of quarantined message to given RCPT.

        Works with already opened message.
        Use keyword `Quarantines Search Message` or `Quarantines Search Message By Mid`
        to find and open message.

        *Parameters*:
        - `rcpt`: Recipient to send copy to. String of comma separated email addresses.
        - `go_back`: Boolean. Press "Back To Messages List" button or not. True by default.

        *Return*:
        String with action result.

        *Exceptions*:
        None

        *Examples*:
        | ${res}= | Quarantines Message Send Copy |
        | ... | rcpt=ahrytski@mail.qa |
        | ... | go_back=${False} |
        | Log | ${res} |
        """
        self._input_text_if_not_none(MESSAGE_DETAILS_RCPT_COPY_EMAIL, rcpt)
        self.click_button(MESSAGE_DETAILS_RCPT_COPY_BUTTON)
        res = self._get_result()
        self._info(res)
        self._go_back(go_back=go_back)
        return res

    def quarantines_message_rescan(self, go_back=True):
        """
        Rescan message with antivirus.

        Works with already opened message.
        Use keyword `Quarantines Search Message` or `Quarantines Search Message By Mid`
        to find and open message.

        *Parameters*:
        - `go_back`: Boolean. Press "Back To Messages List" button or not. True by default.

        *Return*:
        String with action result.

        *Exceptions*:
        None

        *Examples*:
        | ${res}= | Quarantines Message Rescan |
        | ... | go_back=${False} |
        | Log  ${res} |
        """
        self.click_button(MESSAGE_DETAILS_RESCAN_MESSAGE)
        res = self._get_result()
        self._info(res)
        self._go_back(go_back=go_back)
        return res

    def quarantines_message_delete(self, name=None, from_all=False):
        """
        Delete quarantined message form quarantine(s).

        Works with already opened message.
        Use keyword `Quarantines Search Message` or `Quarantines Search Message By Mid`
        to find and open message.

        *Parameters*:
        - `name`: The name of the quarantine to delete message from.
        String of comma-separated values.
        - `from_all`: Boolean. Delete from all quarantines. False by default.

        *Return*:
        String with action result.

        *Exceptions*:
        None

        *Examples*:
        | ${res}= | Quarantines Message Delete |
        | ... | name=Virus |
        | Log | ${res} |
        """
        self._select_quarantine(name=name, all=from_all)
        self._select_from_list_use_regex\
            (MESSAGE_DETAILS_MESSAGE_ACTION_LIST, 'delete')
        self._click_submit_button()
        res = self._get_result()
        self._info(res)
        return res

    def quarantines_message_release(self,
                                    name=None,
                                    delay=None,
                                    from_all=False,
                                    go_back=True):
        """
        Release quarantined message form quarantine(s).

        Works with already opened message.
        Use keyword `Quarantines Search Message` or `Quarantines Search Message By Mid`
        to find and open message.

        *Parameters*:
        - `name`: The name of the quarantine to release message from.
        String of comma-separated values.
        - `delay`: Scheduled exit.
        | 8 Hours |
        | 24 Hours |
        | 48 Hours |
        | 1 Week |
        - `from_all`: Boolean. Release from all quarantines. False by default.
        - `go_back`: Boolean. Press "Back To Messages List" button or not. True by default.

        *Return*:
        String with action result.

        *Exceptions*:
        None

        *Examples*:
        | ${res}= | Quarantines Message Release |
        | ... | from_all=${True} |
        | ... | delay=1 week |
        | ... | go_back=${False} |

        | Log | ${res} |
        | ${res}= | Quarantines Message Release |
        | ... | from_all=${True} |
        """
        if (name is None) and (from_all is False):
            warning_text = "\n***\'name\' argument should be not None or" + \
                " \'from_all\' argument should be \'True\'***"
            warnings.warn(warning_text, RuntimeWarning)

        self._select_quarantine(name=name, all=from_all)
        if delay:
            self._select_from_list_use_regex(MESSAGE_DETAILS_MESSAGE_ACTION_LIST,
                delay,
                starts_with=False,
                contains=True)
        else:
            self._select_from_list_use_regex\
                (MESSAGE_DETAILS_MESSAGE_ACTION_LIST, 'release')
        self._click_submit_button()
        res = self._get_result()
        self._info(res)
        if delay is not None:
            self._go_back(go_back=go_back)
        return res

class SpamQuarantinedMessage(QuarantinedMessage):
    """
    Class to work with separate message in Spam Quarantine.
    Works with already opened messages.
    """
    def _go_back(self, go_back=True):
        if go_back:
            if self._is_element_present(SPAM_MESSAGE_DETAILS_BACK_LINK):
                self.click_element(SPAM_MESSAGE_DETAILS_BACK_LINK)

    def quarantines_spam_message_get_details(self, go_back=True):
        """
        Return message details as it is seen in WUI.

        Works with already opened message.
        Use keyword `Quarantines Search Spam Message` to find and open message.

        *Parameters*:
        - `go_back`: Boolean. Press "<<Back to messages" button or not. True by default.

        *Return*:
        Dictionary(CfgHolder).
        | _Keys_             | _Values types_ |
        | date               | String |
        | envelope_recipient | String |
        | from               | String |
        | message_body       | String |
        | subject            | String |
        | to                 | String |

        *Exceptions*:
        None

        *Examples*:
        | ${details}= | Quarantines Spam Message Get Details |
        | Log Dictionary | ${details} |
        | Should Be Equal | ${details.envelope_recipient} | ahrytski@mail.qa |
        | Should Be Equal | ${details.from} | test@mail.qa |
        | Should Contain | ${details.subject} | SPAM |
        """
        details = CfgHolder()
        rows = int(self.get_matching_xpath_count("%s//tr//descendant::th" % \
                                                 SPAM_MESSAGE_DETAILS_TABLE))
        for row in xrange(1, rows+1):
            _key, _value = self.get_text("%s//tr[%s]" % \
            (SPAM_MESSAGE_DETAILS_TABLE, row)).split(':',1)
            details.__setattr__(self._normalize(_key), _value.strip())
        details.message_body = \
        self.get_text\
        ("%s//div[@class='message_body']" % SPAM_MESSAGE_DETAILS_TABLE)
        self._go_back(go_back=go_back)
        return details

    def quarantines_spam_message_delete(self):
        """
        Delete message from Spam Quarantine.

        Works with already opened message.
        Use keyword `Quarantines Search Spam Message` to find and open message.

        *Parameters*:
        None

        *Return*:
        String with action result.

        *Exceptions*:
        None

        *Examples*:
        | ${res}= | Quarantines Spam Message Delete |
        | Log | ${res} |
        """
        if self._is_element_present("//*[@id='message_action1']"):
            self._select_from_list_use_regex("//*[@id='message_action1']", '-- delete')
            self.click_button("//*[@id='process_message']", "don't wait")
        else:
            self.click_button(SPAM_MESSAGE_DETAILS_DELETE_BUTTON, "don't wait")
        self.click_button(SPAM_QUARANTINE_CONFIRM_OK_CANCEL_BUTTON('Delete'))
        res = self._get_result()
        self._info(res)
        return res

    def quarantines_spam_message_release(self):
        """
        Release message from Spam Quarantine.

        Works with already opened message.
        Use keyword `Quarantines Search Spam Message` to find and open message.

        *Parameters*:
        None

        *Return*:
        String with action result.

        *Exceptions*:
        None

        *Examples*:
        | ${res}= | Quarantines Spam Message Release |
        | Log | ${res} |
        """
        if self._is_element_present("//*[@id='message_action1']"):
            self._select_from_list_use_regex("//*[@id='message_action1']", '-- release')
            self.click_button("//*[@id='process_message']", "don't wait")
        else:
            self.click_button(SPAM_MESSAGE_DETAILS_RELEASE_BUTTON)
        self.click_button(SPAM_QUARANTINE_CONFIRM_OK_CANCEL_BUTTON('Release'))
        res = self._get_result()
        self._info(res)
        return res
