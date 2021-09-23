#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/manager/smimeharvestedpublickeys.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.decorators import set_speed
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

SMIMEPROFILE_TABLE = "//table[@class='cols']"
SETTINGS_TABLE = "//table[@class='pairs']"
POLICIES_DIV = "//*[@id='form']/dl/dd/div[2]"
FIND_PROFILE = "//input[@name='findemail']"
FIND_PUBLICKEY_BUTTON = "//input[@value='Find Public Key']"
CLEARALL_BUTTON = "//input[@id='clearall']"
EDIT_LINK = lambda row: "//table[@class='cols']/tbody/tr[%d]/td[2]/a" % row


class SMIMEHarvestedPublicKeys(GuiCommon):
    """
    'Mail Policies -> S/MIME Harvested Public Keys' section.
    """

    def _open_page(self):
        self._navigate_to('Mail Policies', 'Harvested Public Keys')

    def get_keyword_names(self):
        return ['smime_harvestedpublickeys_get_all',
                'smime_harvestedpublickeys_find',
                'smime_harvestedpublickeys_clearall',
                'smime_harvestedpublickeys_view_details']

    def _click_link_to_edit(self, profile_name, table_loc):
        (rowp, colp) = self._cell_indexes(profile_name, table_loc)
        if rowp is None:
            raise guiexceptions.GuiValueError, '"%s" is not present' % (profile_name,)
        self.click_element(EDIT_LINK(rowp + 1))

    def _cell_indexes(self, item_name, table_loc):
        self._info('Getting row, column for %s in %s table' % \
                   (item_name, table_loc))
        try:
            rows = self._selenium.find_elements_by_xpath('%s//tr' % table_loc)
            for row in rows:
                cells = row.find_elements_by_tag_name("td")
                for cell in cells:
                    if item_name == cell.text:
                        return rows.index(row), cells.index(cell)
        except guiexceptions.SeleniumClientException:
            return None, None
        return None, None

    @set_speed(0)
    def smime_harvestedpublickeys_get_all(self):
        """ Returns a list of names of all S/MIME Harvested Public Keys configured.

        Parameters:
        None

        Return:
        List. The names of all the S/MIME Harvested Public Keys configured.
        Example:
        | Smime Harvestedpublickeys Get All |
        """
        self._info('Getting list of all S/MIME Harvested Public Keys')
        self._open_page()
        try:
            rows = int(self.get_matching_xpath_count("%s/tbody/tr" % SMIMEPROFILE_TABLE))
        except guiexceptions.SeleniumClientException:
            ma_text = self.get_text(POLICIES_DIV)
            return ma_text
        profiles_configured = []
        for profile_indx in range(2, rows + 1):
            profilelist_actn = \
                str(self.get_text("%s/tbody/tr[%d]/td" % (SMIMEPROFILE_TABLE, profile_indx)))
            profiles_configured.append(profilelist_actn)
        return profiles_configured

    @set_speed(0)
    def smime_harvestedpublickeys_find(self, file_name):
        """ Searches S/MIME Harvested Public Key of name 'file_name'

        Parameters:
        - `file_name`:- Name of the file to be searched. String.

        Return:
            None

        Example:
        | Smime harvestedpublickeys Find | file_name |
        """
        self._open_page()
        self.input_text(FIND_PROFILE, file_name)
        self.click_button(FIND_PUBLICKEY_BUTTON)

    @set_speed(0)
    def smime_harvestedpublickeys_clearall(self):
        """ Clears all S/MIME Harvested Public Keys

        Parameters:
        None

        Return:
            None

        Example:
        | Smime Harvestedpublickeys Clearall |
        """
        self._open_page()
        self.click_button(CLEARALL_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @set_speed(0)
    def smime_harvestedpublickeys_view_details(self, email=None):
        """ Collects Public Key information related to specific email.

        Parameters:
        - `email`: Email of the S/MIME Harvested Public Keys. String.

        *Return:*
        Dictionary where keys are:

        | Public key |
        | Verification Address |
        | Domains |
        | Days Remaining |

        *Examples:*
        | ${info}= | Smime Harvestedpublickeys View Details | email=xcadomain4.com |
        | ${details}= | Get From Dictionary | ${info} | Details |
        | Log | ${details} |
        """
        self._open_page()
        self._click_link_to_edit(email, SMIMEPROFILE_TABLE)
        details_info = {}
        details_info['Details'] = self._get_details()
        return details_info

    def _get_details(self):
        details = {}
        for row in xrange(1, 5):
            key = self.get_text("%s/tbody/tr[%d]/th" % \
                                (SETTINGS_TABLE, row)).strip()
            value = self.get_text("%s/tbody/tr[%d]/td" % \
                                  (SETTINGS_TABLE, row)).strip()
            details[key] = value
        return details
