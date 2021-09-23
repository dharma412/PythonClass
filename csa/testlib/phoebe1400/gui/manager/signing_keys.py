#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/signing_keys.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

SIGNING_KEYS_TABLE =  "//table[@class='cols']"
ADD_KEY =             "//input[@value='Add Key...']"
KEY_NAME =            "//input[@name='newName']"
GENERATE_RADIO =      "//input[@id='createMethodGenerate']"
PASTE_RADIO =         "//input[@id='createMethodPaste']"
SELECT_SIZE =         "//select[@id='keySize']"
KEY_TEXT =            "//textarea[@id='data']"
SUBMIT_BUTTON =       "//input[@class='submit']"
DELETE_KEY_CHECKBOX = lambda key_name: "//input[@id='delete[]%s']" % \
                         (key_name, )
DELETE_ALL_CHECKBOX = "//input[@type='checkbox' and @value='delete[]']"
DELETE_BUTTON =       "//input[@id='delete' and @value='Delete']"
CLEAR_ALL_BUTTON =    "//input[@id='clearall']"
IMPORT_KEY_BUTTON =   "//input[@value='Import Keys...']"
EXPORT_KEY_BUTTON =   "//input[@value='Export Keys...']"
SELECT_IMP_FILE =     "//select[@id='impexpfile']"
CONFIRM_BUTTON=       "//button[@id='yui-gen27-button']"
INPUT_EXPORT_FILE =   "//input[@name='file']"

PAGE_PATH = ('Mail Policies', 'Signing Keys')

class SigningKeys(GuiCommon):
    """Keywords for ESA GUI
    interaction with Mail Policies -> Signing Keys
    """

    def get_keyword_names(self):
        return ['add_signing_keys',
                'edit_signing_keys',
                'get_key_signing_keys',
                'import_key_signing_keys',
                'export_key_signing_keys',
                'clear_all_keys_signing_keys',
		'delete_signing_keys']

    @go_to_page(PAGE_PATH)
    def add_signing_keys(self, key_name, option, value):
        """Add new Signing Key

        *Parameters:*
        - `key_name`: new key name. Should be unique and should begin with
           character, mandatory
        - `option`: Either 'generate' or 'paste', mandatory
        - `value`: If selected option is 'generate', then value is as below
	   In non-FIPS mode available sizes: 512,768,1024,1536,2048
	   In FIPS mode available sizes: 1024,1536,2048
	           If selected option is 'paste', then value is the text to be
	   pasted should be given

        *Examples:*
        | Add Signing Keys | testkey | generate | 1024 |
	| Add Signing Keys | testkey1 | paste | ${text} |
        """
        self.click_button(ADD_KEY)

        self.input_text(KEY_NAME, key_name)
        if option == 'paste':
	    self._click_radio_button(PASTE_RADIO)
            self.input_text(KEY_TEXT, value)
        elif option == 'generate':
            self._click_radio_button(GENERATE_RADIO)
	    self.select_from_list(SELECT_SIZE, str(value))

        self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    def edit_signing_keys(self, key_name, option, paste_text, key_size=1024):
        """Edit existing Signing Key

        *Parameters:*
        - `key_name`: existing key name that needs to be edited, mandatory
        - `option`: Either 'generate' or 'paste', mandatory
        - `key_size`: If selected option is 'generate', then key_size is mandatory.
	   In non-FIPS mode available sizes: 512,768,1024,1536,2048
	   In FIPS mode available sizes: 1024,1536,2048
	- `paste_text`: If selected option is 'paste', then key text to be pasted
	   should be given

        *Examples:*
        | Edit Signing Keys | testkey | generate | 2048 |
	| Edit Signing Keys | testkey1 | paste | ${text2} |
        """

        key_link = self._get_element_link(SIGNING_KEYS_TABLE, key_name, \
                                             only_clickable=True)
        if not self._is_element_present(key_link):
            raise ValueError('Key named "%s" is not present'  % \
                               (key_name,))
        self._wait_until_element_is_present(key_link, timeout=10)
        self.click_element(key_link)
        if option == 'paste':
	    self._click_radio_button(PASTE_RADIO)
            self.input_text(KEY_TEXT, paste_text)
        if option == 'generate':
            self._click_radio_button(GENERATE_RADIO)
	    self.select_from_list(SELECT_SIZE, str(key_size))

        self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    def get_key_signing_keys(self, key_name):
        """Get private key of an existing Signing Key

        *Parameters:*
        - `key_name`: existing key name, mandatory

        *Examples:*
        | ${privatekey} = | Get Key Signing Keys | testkey |
        """

        key_link = self._get_element_link(SIGNING_KEYS_TABLE, key_name, \
                                             only_clickable=True)
        if not self._is_element_present(key_link):
            raise ValueError('Key named "%s" is not present'  % \
                               (key_name,))
        self.click_element(key_link)
        value = self.get_text(KEY_TEXT)
        return value

    @go_to_page(PAGE_PATH)
    def import_key_signing_keys(self, file_name):
        """Import key from a file

        *Parameters:*
        - `file_name`: file name from which the key to be imported, mandatory

        *Examples:*
        | Import Key Signing Keys | imp_keys.txt |
        """

        self.click_button(IMPORT_KEY_BUTTON)
	self.select_from_list(SELECT_IMP_FILE, file_name)
        self.click_button(SUBMIT_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    def export_key_signing_keys(self, file_name):
        """Export key to a file

        *Parameters:*
        - `file_name`: file name to which the key to be exported, mandatory

        *Examples:*
        | Export Key Signing Keys | export_keys.txt |
        """

        self.click_button(EXPORT_KEY_BUTTON)
	self.input_text(INPUT_EXPORT_FILE, file_name)
        self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    def clear_all_keys_signing_keys(self):
        """Clears all the signing keys present

        *Examples:*
        | Clear All Keys Signing Keys |
        """

        self.click_button(CLEAR_ALL_BUTTON,  'don\'t wait')
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    def delete_signing_keys(self, key_name):
        """Delete existing signing keys

        *Parameters:*
        - `key_name`: existing key name or 'all' to delete all
		   the keys, mandatory

        *Exceptions:*
        - `ValueError`: if incorrect value is given

        *Examples:*
	| Delete Signing Keys | All |
        | Delete Signing Keys | testkey |
        """

	if key_name.lower() == 'all':
            dest_locator = DELETE_ALL_CHECKBOX
        else:
            dest_locator = DELETE_KEY_CHECKBOX(key_name)
        if not self._is_element_present(dest_locator):
            raise ValueError('Signing Key having name "%s" is not found' % \
                             (key_name,))
        self._select_checkbox(dest_locator)
        self.click_button(DELETE_BUTTON, 'don\'t wait')
        self._click_continue_button()
