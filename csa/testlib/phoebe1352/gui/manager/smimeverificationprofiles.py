#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/smimeverificationprofiles.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import common.gui.guiexceptions as guiexceptions
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon
from sal.containers import cfgholder

SMIMEPROFILE_TABLE="//table[@class='cols']"
EDIT_LINK = lambda row: "//table[@class='cols']/tbody/tr[%d]/td/a" % row
SMIMEPROFILE_NAME_FIELD = "//input[@id='profile_name']"
SMIMEPROFILE_CERTIFICATE_FIELD = "//textarea[@name='certificate']"
DELETE_ALL_CHECKBOX = "//input[@value='delete[]']"
BUTTON_OPAQUEMESSAGE_EDIT =  "//input[@id='edit_settings']"
POLICIES_DIV = "//*[@id='form']/dl/dd/div[2]"
BUTTON_ADD_PROFILE_LIST =  "//input[@value='Add Public Key...']"
BUTTON_DELETE =  "//input[@value='Delete']"
CLEAR_ALL_BUTTON =  "//input[@id='clearall']"
IMPORT_PROFILE_BUTTON = "//input[@value='Import Public Keys...']"
SELECT_IMP_FILE = "//select[@id='impfile']"
SUBMIT_BUTTON = "//input[@type='submit']"
EXPORT_PROFILE_BUTTON = "//input[@id='export']"
INPUT_EXPORT_FILE = "//input[@id='expfile']"
FIND_PROFILE = "//input[@name='findemail']"
SMIME_OPAQUEMESSAGES_ENABLE = "//input[@id='on' and @name='smime_pack_unpack']"
SMIME_OPAQUEMESSAGES_DISABLE = "//input[@id='off' and @name='smime_pack_unpack']"
FIND_PROFILE_BUTTON = "//input[@value='Find Profiles']"
DISPLAY_HARVESTKEYS_BUTTON = "//input[@id='harvested_keys']"
DEL_OPT = \
lambda row: "//table[@class='cols']/tbody/tr[%d]/td[3]/input" % row

class SMIMEVerificationProfiles(GuiCommon):
    """
    'Mail Policies -> S/MIME Verification Profiles' section.
    """
    def _open_page(self):
        self._navigate_to('Mail Policies', 'Public Keys')

    def get_keyword_names(self):
        return ['smime_verificationprofiles_add',
                'smime_verificationprofiles_edit',
                'smime_verificationprofiles_deleteall',
                'smime_verificationprofiles_delete',
                'smime_verificationprofiles_get_all',
                'smime_verificationprofiles_get_details',
                'smime_verificationprofiles_import',
                'smime_verificationprofiles_export',
                'smime_verificationprofiles_find',
                'smime_opaquemessage_settings_edit']

    def _click_link_to_edit(self, profile_name, table_loc):
        (rowp, colp) = self._cell_indexes(profile_name, table_loc)
        if rowp is None:
            raise ValueError, '"%s" is not present' % (profile_name,)
        self.click_element(EDIT_LINK(rowp+1))

    def _cell_indexes(self, item_name, table_loc):
        self._info('Getting row, column for %s in %s table' %\
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

    def _smime_verificationprofiles(self,
                         smime_verificationprofiles_name=None,
                         smime_verificationprofiles_certificate=None):
        """ Populates S/MIME Verification Profiles with data.

        Parameters:
        - `smime_verificationprofiles_name`: S/MIME Profile Name, Mandatory.
        - `smime_verificationprofiles_certificate`: S/MIME Certificate For Verification , Mandatory

        Return:
        None
        """
        if smime_verificationprofiles_name is not None:
            self.input_text(SMIMEPROFILE_NAME_FIELD, smime_verificationprofiles_name)
        if smime_verificationprofiles_certificate is not None:
            self.input_text(SMIMEPROFILE_CERTIFICATE_FIELD, smime_verificationprofiles_certificate)
        self._click_submit_button()

    def smime_verificationprofiles_add(self,
                               smime_verificationprofiles_name=None,
                               smime_verificationprofiles_certificate=None):
        """ Adds new S/MIME Verification Profiles.

        Parameters:
        - `smime_verificationprofiles_name`: S/MIME Profile Name, Mandatory.
        - `smime_verificationprofiles_certificate`: S/MIME Certificate For Verification , Mandatory
        Return:
        None

        Examples:
        | Smime Verificationprofiles Add  |
        | ... | smime_verificationprofiles_name=profile1 |
        | ... | smime_verificationprofiles_certificate=${text} |
        """
        self._info('Adding S/MIME Verification Profiles %s' % smime_verificationprofiles_name)
        self._open_page()
        self.click_button(BUTTON_ADD_PROFILE_LIST)
        self._smime_verificationprofiles(smime_verificationprofiles_name=smime_verificationprofiles_name,
                               smime_verificationprofiles_certificate=smime_verificationprofiles_certificate)

    def smime_verificationprofiles_edit(self,
                                profile_name,
                                smime_verificationprofiles_name=None,
                                smime_verificationprofiles_certificate=None):
        """ Edits S/MIME Verification Profile.

        Parameters:
        - `profile_name`: name of S/MIME Verification Profile to edit. String.
        - `smime_verificationprofiles_name`: S/MIME Profile Name.
        - `smime_verificationprofiles_certificate`: S/MIME Certificate For Verification

        Return:
        None

        Example:
        | Smime Verificationprofiles Edit |
        | ... | profile1 |
        | ... | smime_verificationprofiles_name=profile2 |
        | ... | smime_verificationprofiles_certificate=${text1} |
        """
        self._info('Editing S/MIME Verification Profile %s' % profile_name)
        self._open_page()
        self._click_link_to_edit(profile_name, SMIMEPROFILE_TABLE)
        self._smime_verificationprofiles(smime_verificationprofiles_name=smime_verificationprofiles_name,
                               smime_verificationprofiles_certificate=smime_verificationprofiles_certificate)

    @set_speed(0)
    def smime_verificationprofiles_deleteall(self):
        """ Deletes all S/MIME Verification Profiles.

        Parameters:
        None

        Return:
            None

        Example:
        | Smime Verificationprofiles Deleteall |
        """
        self._open_page()
        self._select_checkbox(DELETE_ALL_CHECKBOX)
        self.click_button(BUTTON_DELETE, "don't wait")
        self._click_continue_button()

    def smime_verificationprofiles_delete(self, profile_name):
        """ Deletes S/MIME Verification Profile.

        Parameters:
        - `profile_name`:- Name of the S/MIME Verification Profile to be deleted. String.

        Return:
            None

        Example:
        | Smime Verificationprofiles Delete | profile2 |
        """
        self._info('Deleting S/MIME Verification Profile %s' % profile_name)
        self._open_page()
        (rowp, colp) = self._cell_indexes(profile_name, SMIMEPROFILE_TABLE)
        if rowp is None:
            raise ValueError, '"%s" S/MIME Verification Profile is not present' % profile_name
        self._select_checkbox(DEL_OPT(rowp+1))
        self.click_button(BUTTON_DELETE, "don't wait")
        self._click_continue_button()

    def smime_verificationprofiles_get_all(self):
        """ Returns a list of names of all the S/MIME Verification Profiles configured.

        Parameters:
        None

        Return:
        List. The names of all the S/MIME Verification Profiles configured.
        Example:
        | Smime Verificationprofiles Get All |
        """
        self._info('Getting list of all configured S/MIME Verification Profiles')
        self._open_page()
        try:
            rows = int(self.get_matching_xpath_count("%s/tbody/tr" % SMIMEPROFILE_TABLE))
        except guiexceptions.SeleniumClientException:
            ma_text = self.get_text(POLICIES_DIV)
            return ma_text
        profiles_configured = []
        for profile_indx in range(2, rows+1):
            profilelist_actn = \
            str(self.get_text("%s/tbody/tr[%d]/td" % (SMIMEPROFILE_TABLE, profile_indx)))
            profiles_configured.append(profilelist_actn)
        return profiles_configured

    def smime_verificationprofiles_get_details(self, profile_name):
        """ Returns an object with complete details of the given S/MIME Verification Profile.

        Parameters:
        - `profile_name`: Name of the S/MIME Verification Profile whose details need to be
        fetched. String.

        Return:
        RecursiveCfgHolder - Returns an object of type RecursiveCfgHolder with
        all the details of the given S/MIME Verification Profile.
        Allows to use '.' to access its keys, like
        cfg.smime_verificationprofiles_name, cfg.smime_verificationprofiles_certificate etc

        Example:
        | ${profilelist} | Smime Verificationprofiles Get Details | profile1 |
        """
        self._info('Getting options of "%s" S/MIME Verification Profile' % profile_name)
        self._open_page()
        self.items = cfgholder.RecursiveCfgHolder()
        self._click_link_to_edit(profile_name, SMIMEPROFILE_TABLE)
        self.items.smime_verificationprofiles_name = self._selenium.find_element_by_xpath(
            SMIMEPROFILE_NAME_FIELD).get_attribute('value')
        self.items.smime_verificationprofiles_certificate = self._selenium.find_element_by_xpath(
            SMIMEPROFILE_CERTIFICATE_FIELD).text
        return self.items

    def smime_opaquemessage_settings_edit(self,
                                unpack_opaque=None):
        """ Edits S/MIME Opaque Message Settings.

        Parameters:
        - `unpack_opaque`: S/MIME opaque message, Enable or Disable

        Return:
        None

        Example:
        | Smime Opaquemessage Settings Edit |
        | ... | unpack_opaque=Enable |
        """
        self._info('Editing S/MIME Opaque Message Settings')
        self._open_page()
        self.click_button(BUTTON_OPAQUEMESSAGE_EDIT)
        if unpack_opaque == 'Enable':
            self._click_radio_button(SMIME_OPAQUEMESSAGES_ENABLE)
        else:
            self._click_radio_button(SMIME_OPAQUEMESSAGES_DISABLE)
        self._click_submit_button()

    @set_speed(0)
    def smime_verificationprofiles_import(self, file_name):
        """ Imports 'file_name' S/MIME Verification Profiles.

        Parameters:
        - `file_name`:- Name of the S/MIME Verification Profile to be imported. String.

        Return:
            None

        Example:
        | Smime Verificationprofiles Import | file_name |
        """
        self._open_page()
        self.click_button(IMPORT_PROFILE_BUTTON)
        self.select_from_list(SELECT_IMP_FILE, file_name)
        self.click_button(SUBMIT_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @set_speed(0)
    def smime_verificationprofiles_export(self, file_name):
        """ Exports S/MIME Verification Profiles to 'file_name'

        Parameters:
        - `file_name`:- Name of the file to which S/MIME Verification Profile is to be exported. String.

        Return:
            None

        Example:
        | Smime Verificationprofiles Export | file_name |
        """
        self._open_page()
        self.click_button(EXPORT_PROFILE_BUTTON)
        self.input_text(INPUT_EXPORT_FILE, file_name)
        self._click_submit_button()

    @set_speed(0)
    def smime_verificationprofiles_find(self, file_name):
        """ Searches S/MIME Verification Profiles of name 'file_name'

        Parameters:
        - `file_name`:- Name of the file to be searched. String.

        Return:
            None

        Example:
        | Smime Verificationprofiles Find | file_name |
        """
        self._open_page()
        self.input_text(FIND_PROFILE, file_name)
        self.click_button(FIND_PROFILE_BUTTON)
