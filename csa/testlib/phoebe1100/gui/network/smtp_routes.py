#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/network/smtp_routes.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
from common.gui.guiexceptions import GuiValueError

# locators
ROUTE_TABLE = "//table[@class='cols']"
SMTP_TABLE = "//tbody[@id='dest_hosts_rowContainer']"
SMTP_ROUTE_ADD_BUTTON = "//input[@value='Add Route...']"
SMTP_ROUTE_DELETE_BUTTON = "//*[@id='_click' and @value='Delete']"
SMTP_ROUTE_CLEAR_ALL_BUTTON = "//input[@value='Clear All Routes']"
SMTP_ROUTE_DELETE_CONFIRM_BUTTON = "//*[@type='button' and text()='Delete']"
SMTP_ROUTE_CANCEL_BUTTON = "//*[@type='button' and text()='Cancel']"
SMTP_ROUTE_IMPORT_CONFIRM_BUTTON = "//*[@type='button' and text()='Import']"
SMTP_ROUTE_EXPORT_CONFIRM_OVERWRITE_BUTTON = "//*[@type='button' and text()='Overwrite']"
SMTP_ROUTE_CLEAR_ALL_CONFIRM_BUTTON = "//*[@type='button' and text()='Clear All']"
SMTP_ROUTE_EXPORT_BUTTON = "//input[@value='Export Routes...']"
SMTP_ROUTE_IMPORT_BUTTON = "//input[@value='Import Routes...']"
RECEIVING_DOMAIN_TEXT = "//input[@name='new_domain']"
SMTP_AUTH_DROPDOWN = "//select[@id='out_smtp']"
ADD_ROW_BUTTON = "//*[@id='dest_hosts_domtable_AddRow']"
ROUTE_DELETE = lambda route: "//input[@value='%s']" % route
EXPORT_FILE_TEXT = "//input[@name='file_server']"
IMPORT_LIST = "//select[@id='impexpfile']"
all_other_domains = 'All Other Domains'


class SmtpRoutes(GuiCommon):
    """
    Library to interact with 'Network > SMTP Routes' page.
    """

    # TODO add pager support
    def get_keyword_names(self):
        return ['smtp_routes_add',
                'smtp_routes_edit',
                'smtp_routes_remove',
                'smtp_routes_clear_all',
                'smtp_routes_get_list',
                'smtp_routes_get_routes',
                'smtp_routes_export',
                'smtp_routes_import', ]

    def _open_page(self):
        self._navigate_to('Network', 'SMTP Routes')

    def _is_all(self, domain):
        if domain.lower() == 'all':
            return True
        return False

    def _open_edit_route_all_page(self, action=None):
        self._open_page()
        row_idx, col_idx = \
            self._get_element_index_by_name(ROUTE_TABLE, all_other_domains)
        route = self.get_text('%s//tr[%s]/td[2]' % (ROUTE_TABLE, row_idx))
        if action.lower() == 'add':
            if not route in '(not defined)':
                raise GuiValueError("'ALL' domain is already added")
            else:
                route_link = \
                    self._get_element_link(ROUTE_TABLE, all_other_domains)
                self.click_element(route_link)
        elif action.lower() == 'edit':
            if route in '(not defined)':
                raise GuiValueError("'ALL' domain is not configured.")
            else:
                route_link = \
                    self._get_element_link(ROUTE_TABLE, all_other_domains)
                self.click_element(route_link)
        else:
            route_link = self._get_element_link(ROUTE_TABLE, all_other_domains)
            self.click_element(route_link)

    def _open_edit_route_page(self, route):
        self._open_page()
        route_link = \
            self._get_element_link(ROUTE_TABLE, route)
        self.click_element(route_link)

    def _add_edit_smtp_destination(self,
                                   add_row_flag,
                                   destination=None,
                                   port=None,
                                   priority=None):
        if add_row_flag - 1:
            # click Add row button only if more than one smtp route added
            self.click_button(ADD_ROW_BUTTON, "don't wait")
        ROW_LOCATOR = lambda row, col: \
            "%s/tr[%s]/td[%s]//input" % (SMTP_TABLE, row, col)
        self._input_text_if_not_none(ROW_LOCATOR(add_row_flag, 1), priority)
        self._input_text_if_not_none(ROW_LOCATOR(add_row_flag, 2), destination)
        self._input_text_if_not_none(ROW_LOCATOR(add_row_flag, 3), port)

    def _add_smtp_routes(self, smtproutes):
        self._debug('Fill in destinations table')
        # 'smtproutes' - list of dictionaries
        # each dictionary is like
        # {'destination':'mail1.qa', 'port':'777', 'priority':'100'}
        add_row_flag = 1
        # allow to pass dictionary or list of dictionaries
        if isinstance(smtproutes, dict):
            smtproutes = [smtproutes, ]
        for smtproute in smtproutes:
            # should work but does not!?
            # self._add_edit_smtp_destination(add_row_flag, **smtproute)
            self._add_edit_smtp_destination(add_row_flag,
                                            destination=smtproute.get('destination', None),
                                            port=smtproute.get('port', None),
                                            priority=smtproute.get('priority', None))
            add_row_flag += 1

    def _clear_smtp(self):
        self._debug('Clear current set of SMTP destination hosts')
        del_column = 4
        del_rows = int(self.get_matching_xpath_count("%s/tr" % SMTP_TABLE))
        while del_rows > 1:
            self.click_link('%s//tr[%s]//td[%s]/img' % \
                            (SMTP_TABLE, del_rows, del_column), "don't wait")
            del_rows -= 1

    def _add_smtp_auth(self, smtp_auth):
        msg = "No outgoing SMTP authentication profiles are configured."
        self._debug('Configure smtp auth profile')
        if self._is_text_present(msg):
            raise GuiValueError(msg)
        # self._select_from_list_use_regex(SMTP_AUTH_DROPDOWN, smtp_auth)
        self.select_from_dropdown_list(SMTP_AUTH_DROPDOWN, smtp_auth)

    def smtp_routes_add(self,
                        recv_domain,
                        smtproutes,
                        smtp_auth=None):
        """
        Add new SMTP route.

        *Parameters*:
        - `recv_domain`: The receiving domain to configure routes for.
        Pass 'All' to configure 'All other domains'.
        - `smtproutes`: Dictionary or List of dictionaries describing routes table.
        Dictionary ot List of dictionaries.
        Dictionary can have following keys:
        - 'destination': The destination host for the domain. Mandatory.
          Enclose hostname in square brackets to force resolution via address (A) records, ignoring any MX records.
          Enter /dev/null by itself if you wish to discard the mail.
          Enter USEDNS to use normal DNS resolution for any route.
          This may not be used with "All Other Domains" default setting.
        - 'port': The port value. String. Optional.
        - 'priority': Any integer between 0 and 65535 to assign priority. Optional.
          0 is highest priority.
          Destinations assigned the same priority will be used in a round-robin manner.
        - `smtp_auth`: The SMTP authentication profile(outgoing). Optional.

        *Return*:
        None

        *Examples*:
        | ${dest1} | Create Dictionary | destination | mail1.qa | priority | 1001 | port | 101 |
        | ${dest2} | Create Dictionary | destination | mail2.qa | priority | 1002 | port | 102 |
        | ${dest3} | Create Dictionary | destination | mail3.qa | priority | 1003 | port | 103 |
        | ${dest4} | Create Dictionary | destination | mail4.qa | priority | 1004 | port | 104 |
        | @{dests} | Set Variable | ${dest1} | ${dest2} | ${dest3} | ${dest4} |
        | Smtp Routes Add |
        | ... | .qa |
        | ... | ${dests} |

        | ${dest1} | Create Dictionary | destination  /dev/null |
        | Smtp Routes Add |
        | ... | All |
        | ... | ${dest1} |

        | ${dest1} | Create Dictionary | destination | babar.mail.ua |
        | Smtp Routes Add |
        | ... | .ua |
        | ... | ${dest1} |
        """
        self._info('Add SMTP Route: %s' % recv_domain)
        if not self._is_all(recv_domain):
            self._open_page()
            self.click_button(SMTP_ROUTE_ADD_BUTTON)
            self._input_text_if_not_none(RECEIVING_DOMAIN_TEXT, recv_domain)
        else:
            self._open_edit_route_all_page(action='add')
        self._add_smtp_routes(smtproutes)
        if smtp_auth:
            self._add_smtp_auth(smtp_auth)
        self._click_submit_button()

    def smtp_routes_edit(self,
                         recv_domain,
                         new_recv_domain=None,
                         smtproutes=None,
                         smtp_auth=None):
        """
        Modifies SMTP route.

        *Parameters*:
        - `recv_domain`: The receiving domain to configure routes for.
        Pass 'All' to configure 'All other domains'.
        - `new_recv_domain`: Modify the receiving domain value. Optional.
        - `smtproutes`: Dictionary or List of dictionaries describing routes table.
        Dictionary ot List of dictionaries.
        Dictionary can have following keys:
          - 'destination': The destination host for the domain. Mandatory.
          Enclose hostname in square brackets to force resolution via address (A) records, ignoring any MX records.
          Enter /dev/null by itself if you wish to discard the mail.
          Enter USEDNS to use normal DNS resolution for any route.
          This may not be used with "All Other Domains" default setting.
          - 'port': The port value. String. Optional.
          - 'priority': Any integer between 0 and 65535 to assign priority. Optional.
          0 is highest priority.
          Destinations assigned the same priority will be used in a round-robin manner.
        - `smtp_auth`: The SMTP authentication profile(outgoing). Optional.

        *Return*:
        None

        *Examples*:
        | ${dest1} | Create Dictionary | destination | mail.all.qa | priority | 1 | port | 3333 |
        | ${dest2} | Create Dictionary | destination | mail.all.res.qa | priority | 2 | port | 5555 |
        | @{dests} | Set Variable | ${dest1} | ${dest2} |
        | Smtp Routes Edit |
        | ... | .qa |
        | ... | smtproutes=${dests} |

        | ${dest1} | Create Dictionary | destination | none.mail.com |
        | Smtp Routes Edit |
        | ... | .com |
        | ... | smtproutes=${dest1} |
        | ... | smtp_auth=auth1 |

        | ${dest1} | Create Dictionary | destination | /dev/null |
        | Smtp Routes Edit |
        | ... | all |
        | ... | smtproutes=${dest1} |
        """
        self._info('Edit SMTP route: %s' % recv_domain)
        if not self._is_all(recv_domain):
            self._open_edit_route_page(recv_domain)
            self._input_text_if_not_none(RECEIVING_DOMAIN_TEXT, new_recv_domain)
        else:
            self._open_edit_route_all_page(action='edit')
        if smtproutes:
            self._clear_smtp()
            self._add_smtp_routes(smtproutes)
        if smtp_auth:
            self._add_smtp_auth(smtp_auth)
        self._click_submit_button()

    def smtp_routes_remove(self, recv_domains, confirm=True):
        """
        Removes given SMTP route.

        *Parameters*:
        - `recv_domains`: The receiving domain(s) to delete. String or List.
        Add 'All' to the list or pass 'All' to clear 'All other domains'.
        - `confirm`: Boolean. Optional. ${True} - Press 'Confirm' button, ${False} - press 'Cancel' button.

        *Return*:
        None

        *Examples*:
        | Smtp Routes Remove | .qa, .ua |

        | Smtp Routes Remove | all |
        """
        if isinstance(recv_domains, basestring):
            recv_domains = recv_domains.split(',')
        self._info('Delete SMTP route(s): %s' % ','.join(recv_domains))
        self._open_page()
        for recv_domain in self._convert_to_tuple(recv_domains):
            if self._is_all(recv_domain.strip()):
                self._select_checkbox(ROUTE_DELETE('ALL'))
            else:
                self._select_checkbox(ROUTE_DELETE(recv_domain.strip()))
        self.click_button(SMTP_ROUTE_DELETE_BUTTON, "don't wait")
        if confirm:
            self.click_button(SMTP_ROUTE_DELETE_CONFIRM_BUTTON)
        else:
            self.click_button(SMTP_ROUTE_CANCEL_BUTTON)

    @set_speed(0)
    def smtp_routes_clear_all(self, confirm=True):
        """
        Clears all SMTP routes.

        *Parameters*:
        - `confirm`: Boolean. Optional. ${True} - Press 'Confirm' button, ${False} - press 'Cancel' button.

        *Return*:
        None

        *Examples*:
        | Smtp Routes Clear |
        """
        self._info('Clear all routes')
        self._open_page()
        if self._is_element_present(SMTP_ROUTE_CLEAR_ALL_BUTTON):
            self.click_button(SMTP_ROUTE_CLEAR_ALL_BUTTON, "don't wait")
            if confirm:
                self.click_button(SMTP_ROUTE_CLEAR_ALL_CONFIRM_BUTTON)
            else:
                self.click_button(SMTP_ROUTE_CANCEL_BUTTON)

    def smtp_routes_get_list(self):
        """
        Returns list of all domains for which smtproutes are configured

        *Parameters*:
        None

        *Return*:
        List. The list of all domains for which SMTP routes are configured.

        *Examples*:
        | Smtp Routes Get List |
        """
        self._open_page()
        return self._get_element_list(ROUTE_TABLE)

    def smtp_routes_get_routes(self, recv_domain):
        """
        Returns settings of the receiving domain.

        *Parameters*:
        - `recv_domain`: The receiving domain to fetch destinations table from.

        *Return*:
        Dictionary with route hostname as key and value is another dictionary holding priority and port.

        *Examples*:
        | Smtp Routes Get Routes | .qa |
        """
        self._info('Get "%s" route settings' % recv_domain)
        if not self._is_all(recv_domain):
            self._open_edit_route_page(recv_domain)
        else:
            self._open_edit_route_all_page()
        smtp_route_dict = {}
        rows = int(self.get_matching_xpath_count("%s/tr" % SMTP_TABLE))
        while rows:
            priority = \
                self.get_value('%s/tr[%s]/td[1]//input' % (SMTP_TABLE, rows))
            smtp_host = \
                self.get_value('%s/tr[%s]/td[2]//input' % (SMTP_TABLE, rows))
            port = \
                self.get_value('%s/tr[%s]/td[3]//input' % (SMTP_TABLE, rows))
            smtp_route_dict[smtp_host] = {'priority': priority, 'port': port}
            rows -= 1
        return smtp_route_dict

    @set_speed(0)
    def smtp_routes_export(self, filename, overwrite=True):
        """
        Export routes list into file.

        *Parameters*:
        - `filename`: The file to export SMTP routes list to.
        - `overwrite`: Boolean. Optional. ${True} - Press 'Overwrite' button, ${False} - press 'Cancel' button.

        *Return*:
        None

        *Examples*:
        | Smtp Routes Export | routes.txt |
        """
        self._info('Export routes list into: %s' % filename)
        self._open_page()
        if not self._is_element_present(SMTP_ROUTE_EXPORT_BUTTON):
            raise ValueError("No routes configured to export")
        self.click_button(SMTP_ROUTE_EXPORT_BUTTON)
        self.input_text(EXPORT_FILE_TEXT, filename)
        self._click_submit_button()
        if overwrite:
            try:
                self._validate_presence \
                    (SMTP_ROUTE_EXPORT_CONFIRM_OVERWRITE_BUTTON)
                self.click_button(SMTP_ROUTE_EXPORT_CONFIRM_OVERWRITE_BUTTON)
            except Exception:
                pass
        else:
            self.click_button(SMTP_ROUTE_CANCEL_BUTTON)

    def smtp_routes_import(self, filename, confirm=True):
        """
        Import routes list from file.

        *Parameters*:
        - `filename`: The file to import SMTP routes from.
        - `confirm`: Boolean. Optional. ${True} - Press 'Confirm' button, ${False} - press 'Cancel' button.

        *Return*:
        None

        *Examples*:
        | Smtp Routes Import | routes.txt |
        """
        self._info('Import routes list from: %s' % filename)
        self._open_page()
        self.click_button(SMTP_ROUTE_IMPORT_BUTTON)
        self.select_from_dropdown_list(IMPORT_LIST, filename)
        self._click_submit_button(wait=False)
        if confirm:
            self.click_button(SMTP_ROUTE_IMPORT_CONFIRM_BUTTON)
        else:
            self.click_button(SMTP_ROUTE_CANCEL_BUTTON)
