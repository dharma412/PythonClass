#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/monitor/quarantines/slbl.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from locators import *
from sal.containers.cfgholder import CfgHolder
from qexceptions import SLBLIsAlreadyEnabled, SLBLIsNotEnabled, QuarantineIsNotEnabled
from qcommon import QuarantinesCommon


class Slbl(QuarantinesCommon):
    sq = 'Spam Quarantine'

    def _open_spam_page(self):
        self._navigate_to('Monitor', self.sq)

    def _not_enabled(self):
        row_idx, col_idx = self._is_quarantine_present(self.sq)
        if not self._is_enabled(row_idx):
            raise QuarantineIsNotEnabled(self.sq)
        return self._is_element_present(SLBL_ENABLE_BUTTON)

    def quarantines_slbl_enable(self):
        """
        Enable SLBL.

        *Parameters*:
        None

        *Return*
        None

        *Examples*:
        | Quarantines Slbl Enable |

        *Exceptions*:
        - `QuarantineIsNotEnabled`: if Spam Quarantine is disabled.
        - `SLBLIsAlreadyEnabled`: if SLBL is enabled already.
        """
        self._open_spam_page()
        if self._not_enabled():
            self.click_button(SLBL_ENABLE_BUTTON)
        else:
            raise SLBLIsAlreadyEnabled('The SLBL is already enabled')

    def quarantines_slbl_is_enabled(self):
        """
        Check SLBL status.

        *Parameters*:
        None

        *Return*
        Boolean. ${True} if SLBL is enabled.

        *Examples*:
        | ${res} | Quarantines Slbl Is Enabled |

        *Exceptions*:
        - `QuarantineIsNotEnabled`: if Spam Quarantine is disabled.
        """
        self._open_spam_page()
        return not self._is_element_present(SLBL_ENABLE_BUTTON)

    def quarantines_slbl_disable(self):
        """
        Disable SLBL.

        *Parameters*:
        None

        *Return*
        None

        *Examples*:
        | Quarantines Slbl Disable |

        *Exceptions*:
        - `QuarantineIsNotEnabled`: if Spam Quarantine is disabled.
        - `SLBLIsNotEnabled`: if SLBL is disabled.
        """
        self._open_spam_page()
        if self._not_enabled():
            raise SLBLIsNotEnabled('The SLBL is not enabled')
        self.click_button(SLBL_EDIT_BUTTON)
        self._unselect_checkbox(SLBL_ENABLE_DISABLE)
        self._click_submit_button()

    def quarantines_slbl_edit_settings(self, action=None, max_entries=None):
        """
        Edit SLBL settings (SLBL should be enabled).

        *Parameters*:
        - `action`: Blocklist Action. Either _quarantine_ or _delete_.
        - `max_entries`: Maximum List Items Per User.

        *Return*
        None

        *Examples*:
        | Quarantines Slbl Edit Settings | action=delete | max_entries=50 |

        *Exceptions*:
        - `QuarantineIsNotEnabled`: if Spam Quarantine is disabled.
        - `SLBLIsNotEnabled`: if SLBL is disabled.
        """
        self._open_spam_page()
        if self._not_enabled():
            raise SLBLIsNotEnabled('The SLBL is not enabled')
        self.click_button(SLBL_EDIT_BUTTON)
        self._select_checkbox(SLBL_ENABLE_DISABLE)
        self.select_from_dropdown_list(SLBL_BLOCK_LIST_ACTION, action)
        self._input_text_if_not_none(SLBL_MAX_ENTRIES, max_entries)
        self._click_submit_button()

    def quarantines_slbl_get_settings(self):
        """
        Get SLBL settings (parse table at Quarantines page).

        *Parameters*:
        None

        *Return*
        Dictionary(CfgHolder).
        | _Keys_ |
        | blocklist_action |
        | end_user_safelist_blocklist |
        | maximum_list_items_per_user |

        *Examples*:
        | ${res}= | Quarantines Slbl Get Settings |
        | Log Dictionary | ${res} |
        | Should Be True | '${res.maximum_list_items_per_user}'=='50' |

        *Exceptions*:
        - `QuarantineIsNotEnabled`: if Spam Quarantine is disabled.
        - `SLBLIsNotEnabled`: if SLBL is disabled.
        """
        self._open_spam_page()
        if self._not_enabled():
            raise SLBLIsNotEnabled('The SLBL is not enabled')
        details = CfgHolder()
        rows = int(self.get_matching_xpath_count("%s//tr/th" % SLBL_TABLE))
        for row in xrange(1, rows + 1):
            _key, _value = self.get_text("%s//tr[%s]" % \
                                         (SLBL_TABLE, row)).split(':', 1)
            details.__setattr__(self._normalize(_key), _value.strip())
        return details
