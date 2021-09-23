#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/admin/trace.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
from trace_def.trace_settings import TraceSettings
from trace_def.trace_output_parser import TraceOutputParser

START_TRACE_BUTTON = "//input[@value='Start Trace']"
DONE_BUTTON = "//input[@name='action:Done']"
NO_LISTENERS_MARK = 'There are no listeners defined.'

PAGE_PATH = ('System Administration', 'Trace')


class Trace(GuiCommon):
    """Keywords for interaction with ESA GUI System Administration ->
    Trace page
    """

    def get_keyword_names(self):
        return ['trace_get_details']

    def _get_trace_settings_controller(self):
        if not hasattr(self, '_trace_settings_controller'):
            self._trace_settings_controller = TraceSettings(self)
        return self._trace_settings_controller

    def _get_trace_output_parser(self):
        if not hasattr(self, '_trace_output_parser'):
            self._trace_output_parser = TraceOutputParser(self)
        return self._trace_output_parser

    @go_to_page(PAGE_PATH)
    def trace_get_details(self, settings):
        """Start trace command and return its results as dictionary

        *Parameters:*
        - `settings`: dictionary whose items are
        | `Source IP Address` | IP address of the remote client to mimic the
        source of the remote domain mandatory |
        | `Fully Qualified Domain Name` | fully qualified domain name of
        source IP. If not defined, a reverse DNS lookup will be performed
        on the source IP. |
        | `Trace Behavior on` | listener name to trace behaviour on |
        | `Domain Name to be Passed to HELO/EHLO` | domain name to be passed to
        HELO/EHLO |
        | `SMTP Authentication Username` | SMTP authentication username of
        source IP address. You should have already configured SMTP auth profile
        connected with listener passed to `Trace Behavior on` in order to
        set this field |
        | `SenderBase Network Owner ID` | senderbase network owner ID. Either
        "Lookup network owner ID associated with source IP" or your custom
        SBO value |
        | `SenderBase Reputation Score` | senderbase reputation score. Either
        "Lookup SBRS associated with source IP" or your custom SBRS value |
        | `Envelope Sender` | envelope Sender of the test message |
        | `Envelope Recipients` | envelope recipients of the test message.
        Can contain many items separated with comma |
        | `Message Body` | Message body for the test message, including
        headers |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct
        - `ConfigError`: if there are no listeners configured on appliance

        *Return:*
        Tree-like dictionary. Its structure highly depends on appliance
        configuration, so it is created dynamically from trace results table
        in appliance GUI.
        The first level keys are heading names, for example:
        "Envelope Sender Processing", "Envelope Recipient Processing",
        "Host Access Table Processing (Listener: InBoundMail)", etc.
        Second level items are key-values pairs for these headings,
        for example under "Host Access Table Processing (Listener: InBoundMail)"
        we can have "Fully Qualified Domain Name", "Matched On",
        "Policy Parameters", etc.
        For some records second-level item may also has leafs, for example
        Level 1 key: "Envelope Recipient Processing"
        Level 2 key: "Envelope Recipient: blabla1@blabla.com"
        Level 3 k/v pairs: {'Alias Expansion': 'No Change',
                            'Default Domain Processing': 'No Change',
                            'Domain Map Processing': 'No Change'}

        *Examples:*
        | ${trace_settings}= | Create Dictionary |
        | ... | Source IP Address | 8.8.8.8 |
        | ... | Fully Qualified Domain Name | google-public-dns-a.google.com |
        | ... | Trace Behavior on | InBoundMail |
        | ... | Domain Name to be Passed to HELO/EHLO | dummy |
        | ... | SenderBase Network Owner ID | Lookup network owner ID associated with source IP |
        | ... | SenderBase Reputation Score | 1.0 |
        | ... | Envelope Sender | blabla@blabla.com |
        | ... | Envelope Recipients | blabla1@blabla.com, blabla2@blabla.com |
        | ... | Message Body | blabla |
        | ${details}= | Trace Get Details | ${trace_settings} |
        | Log | ${details} |
        | ${hat_behavior}= | Get From Dictionary |
        | ... | ${details} | Host Access Table Processing (Listener: InBoundMail) |
        | ${named_policy}= | Get From Dictionary |
        | ... | ${hat_behavior} | Named Policy |
        | Should Be Equal | ${named_policy} | ACCEPTED |
        """
        if self._is_text_present(NO_LISTENERS_MARK):
            raise guiexceptions.ConfigError('You should configure at least one listener in ' \
                                            'order to use the Trace feature')

        controller = self._get_trace_settings_controller()
        controller.set(settings)
        self.click_button(START_TRACE_BUTTON)
        details = self._get_trace_output_parser().get_details()
        self.click_button(DONE_BUTTON)
        return details
