#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/manager/smimesendingprofiles.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import common.gui.guiexceptions as guiexceptions
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon
from sal.containers import cfgholder

SMIME_CERTIFICATE = "//select[@name='certificate_pair']"
SMIMEPROFILE_TABLE = "//table[@class='cols']"
EDIT_LINK = lambda row: "//table[@class='cols']/tbody/tr[%d]/td/a" % row
SMIMEPROFILE_NAME_FIELD = "//input[@id='profile_name']"
DELETE_ALL_CHECKBOX = "//input[@value='delete[]']"
POLICIES_DIV = "//*[@id='form']/dl/dd/div[2]"
BUTTON_ADD_PROFILE_LIST = "//input[@value='Add Profile...']"
BUTTON_DELETE = "//input[@value='Delete']"
IMPORT_PROFILE_BUTTON = "//input[@value='Import Profiles...']"
SELECT_IMP_FILE = "//select[@id='impfile']"
SUBMIT_BUTTON = "//input[@type='submit']"
EXPORT_PROFILE_BUTTON = "//input[@value='Export Profiles...']"
INPUT_EXPORT_FILE = "//input[@id='expfile']"
FIND_PROFILE = "//input[@name='findemail']"

SMIMEPROFILE_SIGN = "//input[@id='sign']"
SMIMEPROFILE_ENCRYPT = "//input[@id='encrypt']"
SMIMEPROFILE_SIGNENCRYPT = "//input[@id='sign_encrypt']"
SMIMEPROFILE_TRIPLE = "//input[@id='triple']"

SMIMEPROFILE_OPAQUE = "//input[@id='opaque']"
SMIMEPROFILE_DETACHED = "//input[@id='detached']"

SMIMEPROFILE_BOUNCE = "//input[@id='bounce']"
SMIMEPROFILE_DROP = "//input[@id='drop']"
SMIMEPROFILE_SPLIT = "//input[@id='split']"

FIND_PROFILE_BUTTON = "//input[@value='Find Profiles']"
DEL_OPT = \
    lambda row: "//table[@class='cols']/tbody/tr[%d]/td[6]/input" % row


class SMIMESendingProfiles(GuiCommon):
    """
    'Mail Policies -> Sending Profiles' section.
    """

    def _open_page(self):
        self._navigate_to('Mail Policies', 'Sending Profiles')

    def get_keyword_names(self):
        return ['smime_sendingprofiles_add',
                'smime_sendingprofiles_edit',
                'smime_sendingprofiles_deleteall',
                'smime_sendingprofiles_delete',
                'smime_sendingprofiles_get_all',
                'smime_sendingprofiles_import',
                'smime_sendingprofiles_export',
                'smime_sendingprofiles_find']

    def _click_link_to_edit(self, profile_name, table_loc):
        (rowp, colp) = self._cell_indexes(profile_name, table_loc)
        if rowp is None:
            raise ValueError, '"%s" is not present' % (profile_name,)
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

    def _smime_sendingprofiles(self,
                               smime_sendingprofiles_name=None,
                               smime_sendingprofiles_signing_certificate=None,
                               smime_sendingprofiles_mode=None,
                               smime_sendingprofiles_signmode=None,
                               smime_sendingprofiles_action=None):
        """ Populates S/MIME Sending Profiles with data.

        Parameters:
        - `smime_sendingprofiles_name`: S/MIME Profile Name, Mandatory.
        - `smime_sendingprofiles_signing_certificate`: S/MIME Certificate For Sending , Mandatory
        - `smime_sendingprofiles_mode`: S/MIME Mode , Mandatory
        - `smime_sendingprofiles_signmode`: S/MIME Sign Mode , Mandatory
        - `smime_sendingprofiles_action`: S/MIME Action , Mandatory

        Return:
        None
        """
        if smime_sendingprofiles_name is not None:
            self.input_text(SMIMEPROFILE_NAME_FIELD, smime_sendingprofiles_name)
        if smime_sendingprofiles_signing_certificate is not None:
            self.select_from_list(SMIME_CERTIFICATE, smime_sendingprofiles_signing_certificate)
        if smime_sendingprofiles_mode == 'Sign':
            self._click_radio_button(SMIMEPROFILE_SIGN)
        elif smime_sendingprofiles_mode == 'Encrypt':
            self._click_radio_button(SMIMEPROFILE_ENCRYPT)
        elif smime_sendingprofiles_mode == 'SignEncrypt':
            self._click_radio_button(SMIMEPROFILE_SIGNENCRYPT)
        elif smime_sendingprofiles_mode == 'Triple':
            self._click_radio_button(SMIMEPROFILE_TRIPLE)
        if smime_sendingprofiles_signmode == 'Opaque':
            self._click_radio_button(SMIMEPROFILE_OPAQUE)
        elif smime_sendingprofiles_signmode == 'Detached':
            self._click_radio_button(SMIMEPROFILE_DETACHED)
        if smime_sendingprofiles_action == 'Bounce':
            self._click_radio_button(SMIMEPROFILE_BOUNCE)
        elif smime_sendingprofiles_action == 'Drop':
            self._click_radio_button(SMIMEPROFILE_DROP)
        elif smime_sendingprofiles_action == 'Split':
            self._click_radio_button(SMIMEPROFILE_SPLIT)
        self._click_submit_button()

    @set_speed(0)
    def smime_sendingprofiles_add(self,
                                  smime_sendingprofiles_name=None,
                                  smime_sendingprofiles_signing_certificate=None,
                                  smime_sendingprofiles_mode=None,
                                  smime_sendingprofiles_signmode=None,
                                  smime_sendingprofiles_action=None):
        """ Adds new S/MIME Sending Profiles.

        Parameters:
        - `smime_sendingprofiles_name`: S/MIME Profile Name, Mandatory.
        - `smime_sendingprofiles_signing_certificate`: S/MIME Certificate For Sending , Mandatory
        - `smime_sendingprofiles_mode`: S/MIME Mode , Mandatory
        - `smime_sendingprofiles_signmode`: S/MIME Sign Mode , Mandatory
        - `smime_sendingprofiles_action`: S/MIME Action , Mandatory
        Return:
        None

        Examples:
        | Smime Sendingprofiles Add  |
        | ... | smime_sendingprofiles_name=profile1 |
        | ... | smime_sendingprofiles_signing_certificate=aaa |
        | ... | smime_sendingprofiles_mode=Encrypt  |
        | ... | smime_sendingprofiles_signmode=Detached  |
        | ... | smime_sendingprofiles_action=Bounce   |
        """
        self._info('Adding S/MIME Sending Profiles %s' % smime_sendingprofiles_name)
        self._open_page()
        self.click_button(BUTTON_ADD_PROFILE_LIST)
        self._smime_sendingprofiles(smime_sendingprofiles_name=smime_sendingprofiles_name,
                                    smime_sendingprofiles_signing_certificate=smime_sendingprofiles_signing_certificate,
                                    smime_sendingprofiles_mode=smime_sendingprofiles_mode,
                                    smime_sendingprofiles_signmode=smime_sendingprofiles_signmode,
                                    smime_sendingprofiles_action=smime_sendingprofiles_action)

    @set_speed(0)
    def smime_sendingprofiles_edit(self,
                                   profile_name,
                                   smime_sendingprofiles_name=None,
                                   smime_sendingprofiles_signing_certificate=None,
                                   smime_sendingprofiles_mode=None,
                                   smime_sendingprofiles_signmode=None,
                                   smime_sendingprofiles_action=None):
        """ Edits S/MIME Sending Profile.

        Parameters:
        - `profile_name`: name of S/MIME Sending Profile to edit. String.
        - `smime_sendingprofiles_name`: S/MIME Profile Name, Mandatory.
        - `smime_sendingprofiles_signing_certificate`: S/MIME Certificate For Sending , Mandatory
        - `smime_sendingprofiles_mode`: S/MIME Mode , Mandatory
        - `smime_sendingprofiles_signmode`: S/MIME Sign Mode , Mandatory
        - `smime_sendingprofiles_action`: S/MIME Action , Mandatory

        Return:
        None

        Example:
        | Smime Sendingprofiles Edit |
        | ... | profile1 |
        | ... | smime_sendingprofiles_name=profile2 |
        | ... | smime_sendingprofiles_signing_certificate=aaa |
        | ... | smime_sendingprofiles_mode=Encrypt  |
        | ... | smime_sendingprofiles_signmode=Detached  |
        | ... | smime_sendingprofiles_action=Bounce   |
        """
        self._info('Editing S/MIME Sending Profile %s' % profile_name)
        self._open_page()
        self._click_link_to_edit(profile_name, SMIMEPROFILE_TABLE)
        self._smime_sendingprofiles(smime_sendingprofiles_name=smime_sendingprofiles_name,
                                    smime_sendingprofiles_signing_certificate=smime_sendingprofiles_signing_certificate,
                                    smime_sendingprofiles_mode=smime_sendingprofiles_mode,
                                    smime_sendingprofiles_signmode=smime_sendingprofiles_signmode,
                                    smime_sendingprofiles_action=smime_sendingprofiles_action)

    @set_speed(0)
    def smime_sendingprofiles_deleteall(self):
        """ Deletes all S/MIME Sending Profiles.

        Parameters:
        None

        Return:
            None

        Example:
        | Smime Sendingprofiles Deleteall |
        """
        self._open_page()
        self._select_checkbox(DELETE_ALL_CHECKBOX)
        self.click_button(BUTTON_DELETE, "don't wait")
        self._click_continue_button()

    @set_speed(0)
    def smime_sendingprofiles_delete(self, profile_name):
        """ Deletes S/MIME Sending Profile.

        Parameters:
        - `profile_name`:- Name of the S/MIME Sending Profile to be deleted. String.

        Return:
            None

        Example:
        | Smime Sendingprofiles Delete | profile2 |
        """
        self._info('Deleting S/MIME Sending Profile %s' % profile_name)
        self._open_page()
        (rowp, colp) = self._cell_indexes(profile_name, SMIMEPROFILE_TABLE)
        if rowp is None:
            raise ValueError, '"%s" S/MIME Sending Profile is not present' % profile_name
        self._select_checkbox(DEL_OPT(rowp + 1))
        self.click_button(BUTTON_DELETE, "don't wait")
        self._click_continue_button()

    @set_speed(0)
    def smime_sendingprofiles_get_all(self):
        """ Returns a list of names of all the S/MIME Sending Profiles configured.

        Parameters:
        None

        Return:
        List. The names of all the S/MIME Sending Profiles configured.
        Example:
        | Smime Sendingprofiles Get All |
        """
        self._info('Getting list of all configured S/MIME Sending Profiles')
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
    def smime_sendingprofiles_import(self, file_name):
        """ Imports 'file_name' S/MIME Sending Profiles.

        Parameters:
        - `file_name`:- Name of the S/MIME Sending Profile to be imported. String.

        Return:
            None

        Example:
        | Smime Sendingprofiles Import | file_name |
        """
        self._open_page()
        self.click_button(IMPORT_PROFILE_BUTTON)
        self.select_from_list(SELECT_IMP_FILE, file_name)
        self.click_button(SUBMIT_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @set_speed(0)
    def smime_sendingprofiles_export(self, file_name):
        """ Exports S/MIME Sending Profiles to 'file_name'

        Parameters:
        - `file_name`:- Name of the file to which S/MIME Sending Profile is to be exported. String.

        Return:
            None

        Example:
        | Smime Sendingprofiles Export | file_name |
        """
        self._open_page()
        self.click_button(EXPORT_PROFILE_BUTTON)
        self.input_text(INPUT_EXPORT_FILE, file_name)
        self._click_submit_button()

    @set_speed(0)
    def smime_sendingprofiles_find(self, file_name):
        """ Searches S/MIME Sending Profiles of name 'file_name'

        Parameters:
        - `file_name`:- Name of the file to be searched. String.

        Return:
            None

        Example:
        | Smime Sendingprofiles Find | file_name |
        """
        self._open_page()
        self.input_text(FIND_PROFILE, file_name)
        self.click_button(FIND_PROFILE_BUTTON)
