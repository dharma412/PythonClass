#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/support_request.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)
from common.cli.cliexceptions import ConfigError


class SupportRequest(CliKeywordBase):
    """ Sends status information for support purposes."""

    def get_keyword_names(self):
        return ['support_request']

    def support_request(self,
                        name=None,
                        email=None,
                        subject=None,
                        description=None,
                        customer_support=DEFAULT,
                        additional_rcp='no',
                        technology=DEFAULT,
                        sub_technology=DEFAULT,
                        problem_category=DEFAULT,
                        problem_subcategory=DEFAULT,
                        email_rcp=None,
                        phone=DEFAULT,
                        existed=DEFAULT,
                        ticket_number=DEFAULT,
                        ccoid_option=DEFAULT,
                        ccoid=None,
                        contract_id=None,
                        print_req='no'):
        """Support Request.
        The information includes: status detail, tophosts, 10 seconds of rate,
        and showconfig. The showconfig output does not include uncommitted
        changes.

        Parameters:
        - `name`: string with the name of the contact person.
        - `email`: string with your email address value. Mandatory.
        - `subject`: string with ticket object. Mandatory.
        - `customer_support`: specify 'Yes' if this is ticket to Cisco IronPort
                Customer Support. Optional. Either 'Yes' or 'No'.
        - `additional_rcp`: specify 'Yes' if you want to send the support
                request to additional recipient(s). Either 'Yes' or 'No'.
                Optional.
        - `technology` : select a technology related to this support request
           | 1 | Security - Email and Web |
           | 2 | Security - Management |
        - `sub_technology` - select a subtechnology related to this support request
           If technology selected is  1 - Security - Email and Web  then
           sub_technology is one of the following:
           | 1 | Cisco Email Security Appliance (C1x0,C3x0, C6x0, X10x0) - Misclassified\nMessages |
           | 2 | Cisco Email Security Appliance (C1x0,C3x0, C6x0, X10x0) - SBRS |
           | 3 | Cisco Email Security Appliance (c1x0,C3x0, C6x0, X10x0) - Other |
           | 4 | Email Security Appliance - Virtual |
           If technology selected is 2 - Security - Management | then
           sub_technology is one of the following
           | 1 | Email-related issue |
           | 2 | Web-related issue |
           | 3 | Other issue |
        - `problem_category` - select the problem category
           If sub_technology is Email Security Appliance - Virtual,
           then problem_category is one of the following:
           | 1 | Installation |
           | 2 | Licensing |
           For everything else, it is one of the following:
           | 1 | Install |
           | 2 | Configure |
           | 3 | Operate |
           | 4 | Upgrade |
         - `problem_subcategory` - select a problem sub-category:
            if problem_category is 'Install' - then
            problem_subcategory is one of the following:
            | 1 | Software Failure |
            | 2 | Password Recovery |
            | 3 | Configuration Assistance |
            | 4 | Interoperability |
            | 5 | Hardware Failure |
            | 6 | Software Selection/Download Assistance |
            | 7 | Licensing |
            | 8 | Data Corruption |
            | 9 | Error Messages, Logs |
            | 10 | Install, Uninstall or Upgrade |
            if problem_catory is 'Configure' - then
            problem_subcategory is one of the following:
            | 1 | Data Corruption |
            | 2 | Configuration Assistance |
            | 3 | Password Recovery |
            | 4 | Interoperability |
            | 5 | Hardware Failure |
            | 6 | Error Messages, Logs |
            | 7 | Licensing |
            | 8 | Software Failure |
            if problem_catory is 'Operate' - then
            problem_subcategory is one of the following:
            | 1 | Interoperability |
            | 2 | Password Recovery |
            | 3 | Licensing |
            | 4 | Hardware Failure |
            | 5 | Error Messages, Logs |
            | 6 | Software Failure |
            if problem_catory is 'Upgrade' - then
            problem_subcategory is one of the following:
            | 1 | Error Messages, Logs |
            | 2 | Hardware Failure |
            | 3 | Interoperability |
            | 4 | Configuration Assistance |
            | 5 | Install, Uninstall or Upgrade |
            | 6 | Software Failure |
            | 7 | Licensing |
            | 8 | Data Corruption |
            | 9 | Software Selection/Download Assistance |
            | 10 | Password Recovery |

        - `email_rcp`: if additional recipient is chosen - specify the email
                address(es) to which you want to send the support request.
                Mandatory.
        - `phone`: string with contact phone number value. Optional.
        - `description`: enter a description of your issue. Mandatory.
        - `existed`: specify 'Yes' if this support request associated
                with an existing support ticket.
        - `ticket_number`: existing support ticket number.
        - `ccoid_option`: whether to create new CCOID or use existing one.
                Only numbers should be given. '1' for creating new CCOID.
                Existing CCOID's order -  recent ones will be at the top.
        - `ccoid`: new CCOID of the contact person. Required for creating
                new CCOID.
        - `contract_id`: contract ID of the contact person.
        - `print_req`: print the support request to the screen. Default to
          'no'.

        Return:
        If `print_req` is set to 'yes', the return value is the content of
        support request mail.

        Exceptions:
        - `ConfigError`: in case no ticket number was provided when answer to
          `existed` is 'yes' or in case no additional recipients were defined
           when answering 'yes' to `additional_rcp`.

        Examples:
        | Support Request |
        | ... | name=Test |
        | ... | email=qa@test.com |
        | ... | subject=test |
        | ... | description=test |
        | ... | customer_support=No |
        | ... | technology=1 |
        | ... | sub_technology=4 |
        | ... | additional_rcp=Yes |
        | ... | email_rcp=test@test.com |
        | ... | ccoid_option=1 |
        | ... | ccoid=tester |
        | ... | contract_id=1 |

        | ${req_out} = | Support Request |
        | ... | name=Test |
        | ... | email=qa@test.com |
        | ... | subject=test |
        | ... | description=test |
        | ... | customer_support=No |
        | ... | technology=1 |
        | ... | sub_technology=2 |
        | ... | problem_category=1 |
        | ... | problem_subcategory=2 |
        | ... | additional_rcp=Yes |
        | ... | email_rcp=test@test.com |
        | ... | ccoid_option=2 |
        | ... | contract_id=1 |
        | ... | print_req=yes |
        | Log | ${req_out} |

        """
        add_rcp_ans = self._process_yes_no(additional_rcp)

        kwargs = {'def_rcp': self._process_yes_no(customer_support),
                  'add_rcp': add_rcp_ans,
                  'corr_email': email,
                  'tech': technology,
                  'sub_tech': sub_technology,
                  'categ': problem_category,
                  'add_info': phone,
                  'subj': subject,
                  'descr': description,
                  'print_req': self._process_yes_no(print_req)}

        # This is needed as there is no problem_subcategory
        # when the sub_technology is Email Security Appliance - Virtual
        if sub_technology != '4':
            kwargs['sub_categ'] = problem_subcategory

        if add_rcp_ans == 'Y':
            if email_rcp is None:
                raise ConfigError('Email of additional recipients ' \
                                  'must be specified')
            else:
                kwargs['rcp_email'] = email_rcp

        exist_tick_ans = self._process_yes_no(existed)
        if exist_tick_ans == 'Y':
            if not ticket_number:
                raise ConfigError('If ticket already exists - please ' \
                                  'specify ticket number.')
            else:
                kwargs['exist_tick'] = exist_tick_ans
                kwargs['tick_num'] = ticket_number

        if int(ccoid_option) == 1:
            if ccoid is None:
                raise ConfigError('If you want to create new ccoid - please ' \
                                  'specify the ccoid.')
            else:
                kwargs['select_ccoid'] = ccoid_option
                kwargs['new_ccoid'] = ccoid
        else:
            kwargs['select_ccoid'] = ccoid_option

        kwargs['contact_name'] = name
        kwargs['contract_id'] = contract_id

        return self._cli.supportrequest(**kwargs)
