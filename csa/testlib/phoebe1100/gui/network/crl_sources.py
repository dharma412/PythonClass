#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/network/crl_sources.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import re

from common.gui.decorators import go_to_page, set_speed
from common.gui.guiexceptions import ConfigError
from common.gui.guicommon import GuiCommon

from crl_sources_def.crl_source_profile import CRLSourceProfile, \
    CRL_FILE_NAME
from crl_sources_def.crl_sources_settings import CRLSourcesSettings


class CRLSourceTestFailed(Exception):
    pass


ADD_SOURCE_BUTTON = "//input[@value='Add CRL Source...']"
EDIT_SETTINGS_BUTTON = "//input[@name='FormEditGlobals']"
UPDATE_BUTTON = "//input[@value='Update']"

SOURCES_TABLE = "//table[@class='cols']"
SOURCE_NAME_CELLS = "%s/tbody/tr[td]" % (SOURCES_TABLE,)
# idx starts from 1
SOURCE_CELL_BY_IDX = lambda row_idx, col_idx: "%s/tbody/tr[td][%d]/td[%s]" % \
                                              (SOURCES_TABLE, row_idx, col_idx)
SOURCE_EDIT_LINK = lambda name: "%s//td/a[normalize-space()='%s']" % \
                                (SOURCES_TABLE, name)
SOURCE_CHECKBOX_BY_NAME = lambda name: "%s//td[.//a[normalize-space()='%s']]" \
                                       "/preceding-sibling::td/input" % \
                                       (SOURCES_TABLE, name)
SOURCE_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']" \
                                  "/following-sibling::td[4]/img" % \
                                  (SOURCES_TABLE, name)
TABLE_HEADERS_MAP = {'Name': 2,
                     'CRL File Type': 3,
                     'Primary URL': 4,
                     'Secondary URL': 5}
SOURCES_DELETE_BUTTON = "//input[@value='Clear All CRL Sources']"
SOURCE_SELECT_ALL_CHECKBOX = "//input[@id='check_all']"

PAGE_PATH = ('Network', 'CRL Sources')


class CRLSources(GuiCommon):
    """Keywords for GUI interaction with Network ->
    CRL Sources page.
    """

    def get_keyword_names(self):
        return ['crl_sources_edit_settings',

                'crl_sources_is_source_exist',
                'crl_sources_add',
                'crl_sources_edit',
                'crl_sources_delete',
                'crl_sources_test',
                'crl_sources_update',
                'crl_sources_get_all']

    def _get_crl_sources_settings_controller(self):
        if not hasattr(self, '_crl_sources_settings_controller'):
            self._crl_sources_settings_controller = \
                CRLSourcesSettings(self)
        return self._crl_sources_settings_controller

    def _get_crl_source_profile_controller(self):
        if not hasattr(self, '_crl_source_profile_controller'):
            self._crl_source_profile_controller = \
                CRLSourceProfile(self)
        return self._crl_source_profile_controller

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def crl_sources_edit_settings(self, settings):
        """Edit global CRL Sources Settings

        *Parameters:*
        - `settings`: dictionary whose items can be:
        | `CRL check for inbound SMTP TLS` | whether to enable CRL check
        for inbound SMTP TLS. Either ${True} or ${False} |
        | `CRL check for outbound SMTP TLS` | whether to enable CRL check
        for outbound SMTP TLS. Either ${True} or ${False} |

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | CRL check for inbound SMTP TLS | ${True} |
        | ... | CRL check for outbound SMTP TLS | ${True} |
        | CRL Sources Edit Settings | ${settings} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        self._get_crl_sources_settings_controller().set(settings)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def crl_sources_is_source_exist(self, name):
        """Check whether CRL Source with given name exists

        *Parameters:*
        - `name`: the name of CRL Source

        *Examples:*
        | CRL Sources Add | ${SOURCE_NAME} | ${settings} |
        | ${is_exist}= | CRL Sources Is Source Exist | ${SOURCE_NAME} |
        | Should Be True | ${is_exist} |
        """
        return self._is_element_present(SOURCE_EDIT_LINK(name))

    @set_speed(0)
    def crl_sources_add(self, name, settings):
        """Add new CRL Source

        *Parameters:*
        - `name`: the name of newly added CRL Source
        - `settings`: dictionary whose items can be:
        | `CRL File Type` | the type of CRL file. Either 'PEM' or 'ASN.1' |
        | `Primary source URL` | primary source URL to download a
        CRL file from. Mandatory |
        | `Secondary source URL` | secondary source URL to use when the
        primary source is not available (optional) |
        | `Enable Scheduled auto update of CRL file` | whether to enable
        scheduled auto update of CRL file. Either ${True} or ${False} |
        | `Auto Update Period` | Either 'Daily', 'Weekly' or 'Monthly'.
        Available if `Enable Scheduled auto update of CRL file` is set
        to ${True} |
        | `Update on` | then name of a weekday to schedule update on. Available
        if `Auto Update Period` is set to 'Weekly'. Available values are
        capitalized weekday names |
        | `Scheduled Time` | time stamp in 24-hour format (HH:MM) |
        | `Enable this CRL Source` | whether to enable this CRL source.
        Set this option to ${True} if you want to have this enabled right after
        adding. |

        *Exceptions:*
        - `ConfigError`: if CRL Source with given name already exists
        - `ValueError`: if any of given settings is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Enable this CRL Source | ${True} |
        | ... | CRL File Type | ASN.1 |
        | ... | Primary source URL | http://example.com |
        | ... | Secondary source URL | http://d2.example.com |
        | ... | Enable Scheduled auto update of CRL file | ${True} |
        | ... | Auto Update Period | Weekly |
        | ... | Update on | Sunday |
        | ... | Scheduled Time | 00:00 |
        | CRL Sources Add | ${SOURCE_NAME} | ${settings} |
        """
        if self.crl_sources_is_source_exist(name):
            raise ConfigError('CRL Source named "%s" already exists' % \
                              (name,))
        self.click_button(ADD_SOURCE_BUTTON)
        controller = self._get_crl_source_profile_controller()
        settings.update({CRL_FILE_NAME[0]: name})
        controller.set(settings)
        self._click_submit_button()

    @set_speed(0)
    def crl_sources_edit(self, name, settings={}):
        """Edit existing CRL Source

        *Parameters:*
        - `name`: the name of CRL Source to be edited
        - `settings`: are the same as for the `CRL Sources Add` keyword plus:
        | `CRL File Name` | the name name of CRL Source |

        *Exceptions:*
        - `ValueError`: if any of given settings is not correct or
        CRL Source with given name does not exist

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | CRL File Type | PEM |
        | CRL Sources Edit | ${SOURCE_NAME} | ${settings} |
        """
        if not self.crl_sources_is_source_exist(name):
            raise ValueError('CRL Source named "%s" does not exist' % \
                             (name,))
        self.click_button(SOURCE_EDIT_LINK(name))
        controller = self._get_crl_source_profile_controller()
        controller.set(settings)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def crl_sources_delete(self, name):
        """Delete existing CRL Source

        *Parameters:*
        - `name`: the name of CRL Source to be deleted. Can be 'all'
        to clear all existing CRL sources

        *Exceptions:*
        - `ValueError`: if CRL Source with given name does not exist.
        In case there are no sources and `name` is 'all' then no exception
        will be generated

        *Examples:*
        | CRL Sources Delete | ${SOURCE_NAME} |
        """
        if name.lower() == 'all':
            if self._is_element_present(SOURCES_DELETE_BUTTON):
                self.click_button(SOURCES_DELETE_BUTTON, 'don\'t wait')
                self._click_continue_button()
            else:
                self._info('No CRL Sources to clean. Ignoring...')
        else:
            if not self._is_element_present(SOURCE_DELETE_LINK(name)):
                raise ValueError('CRL Source "%s" does not exist' % \
                                 (name,))
            self.click_button(SOURCE_DELETE_LINK(name), 'don\'t wait')
            self._click_continue_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def crl_sources_test(self, name, should_raise_exception=False):
        """Test existing CRL Source

        *Parameters:*
        - `name`: the name of CRL Source to be tested
        - `should_raise_exception`: whether to raise the CRLSourceTestFailed
        if source test has failed

        *Exceptions:*
        - `ValueError`: if CRL Source with given name does not exist.
        - `CRLSourceTestFailed`: if CRL Source test has failed

        *Return:*
        CRL Source test result as a string (if `should_raise_exception` is
        set to ${False} (default behavior))

        *Examples:*
        | Run Keyword And Expect Error | *CRLSourceTestFailed* |
        | ... | CRL Sources Test | ${SOURCE_NAME} | ${True} |
        """
        if not self._is_element_present(SOURCE_EDIT_LINK(name)):
            raise ValueError('CRL Source named "%s" does not exist' % \
                             (name,))
        self.click_button(SOURCE_EDIT_LINK(name))
        controller = self._get_crl_source_profile_controller()
        test_result = controller.test()
        if re.search(r'error was', test_result, re.I) and should_raise_exception:
            raise CRLSourceTestFailed('The test of "%s" CRL Source has been failed:' \
                                      '\n%s' % (name, test_result))
        else:
            return test_result

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def crl_sources_update(self, names):
        """Update given existing CRL Sources

        *Parameters:*
        - `names`: a list of CRL Source named to update or
        one name

        *Exceptions:*
        - `ValueError`: if any of given CRL Source names does
        not exist

        *Examples:*
        | CRL Sources Update | ${SOURCE_NAME} |
        """
        if isinstance(names, basestring):
            names = (names,)
        for name in names:
            if not self._is_element_present(SOURCE_CHECKBOX_BY_NAME(name)):
                raise ValueError('CRL Source named "%s" does not exist' % \
                                 (name,))
            self._select_checkbox(SOURCE_CHECKBOX_BY_NAME(name))
        self.click_button(UPDATE_BUTTON)
        self._check_action_result()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def crl_sources_get_all(self):
        """Get info about existing CRL Sources

        *Return:*
        Dictionary whose keys are corresponding column names in sources
        table and values are lists with column cells. Available headers
        are:

        | Name |
        | CRL File Type |
        | Primary URL |
        | Secondary URL |

        These lists will be empty if there are no CRL Sources defined

        *Examples:*
        | CRL Sources Delete | all |
        | ${info}= | CRL Sources Get All |
        | @{names}= | Get From Dictionary | ${info} | Name |
        | Should Be Empty | ${names} |
        """
        result = {}
        sources_count = int(self.get_matching_xpath_count(SOURCE_NAME_CELLS))
        for header_name, header_idx in TABLE_HEADERS_MAP.iteritems():
            result[header_name] = []
            for source_row_idx in xrange(1, 1 + sources_count):
                cell_value = self.get_text(SOURCE_CELL_BY_IDX(source_row_idx,
                                                              header_idx))
                result[header_name].append(cell_value.strip())
        return result
