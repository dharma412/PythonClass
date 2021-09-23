#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/support_request.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)
from common.cli.cliexceptions import ConfigError


class SupportRequest(CliKeywordBase):
    """ Sends status information for support purposes."""

    def get_keyword_names(self):
        return ['support_request']

    def support_request(self,
                        name,
                        email,
                        ccoid,
                        contract_id,
                        subject,
                        description,
                        customer_support=DEFAULT,
                        additional_rcp='N',
                        technology=DEFAULT,
                        sub_technology=DEFAULT,
                        appliance=DEFAULT,
                        problem_category=DEFAULT,
                        problem_subcategory=DEFAULT,
                        email_rcp=None,
                        phone=DEFAULT,
                        existed=DEFAULT,
                        ticket_number=None,
                        print_req='N'):
        """Support Request.
        The information includes: status detail, tophosts, 10 seconds of rate,
        and showconfig. The showconfig output does not include uncommitted
        changes.

        Parameters:
        - `name`: string with the name of the contact person. Mandatory.
        - `email`: string with your email address value. Mandatory.
        - `subject`: string with ticket object. Mandatory.
        - `customer_support`: specify 'Yes' if this is ticket to Cisco IronPort
                Customer Support. Optional. Either 'Yes' or 'No'.
        - `additional_rcp`: specify 'Yes' if you want to send the support
                request to additional recipient(s). Either 'Yes' or 'No'.
                Optional.
        - `technology` : select a technology related to this support request.
           By default the first one in the list is selected.
           | 1 | Security - Management |
        - `sub_technology` - select a subtechnology related to this support request
           By default the first one in the list is selected.
           | 1 | Email-related issue |
           | 2 | Web-related issue |
           | 3 | Other issue |
        - `problem_category` - select the problem category
           By default the first one in the list is selected.
           One of the following:
           | 1 | Install |
           | 2 | Configure |
           | 3 | Operate |
           | 4 | Upgrade |
         - `problem_subcategory` - select a problem sub-category.
            By default the first one in the list is selected.
            If problem_category is 'Install' - then
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

        - `appliance`: Specify the IP of the appliance to which this support request applies.
                       By default the first one in the list is selected.
        - `email_rcp`: if additional recipient is chosen - specify the email
                address(es) to which you want to send the support request.
                Mandatory.
        - `phone`: string with contact phone number value. Optional.
        - `description`: enter a description of your issue. Mandatory.
        - `ccoid`: enter CCOID of the contact.Mandatory.
        - `contract_id`: enter contract id.Mandatory.
        - `existed`: specify 'Yes' if this support request associated
                with an existing support ticket.
        - `ticket_number`: existing support ticket number.
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
        | ... | appliance=10.76.68.183 |
        | ... | technology=1 |
        | ... | sub_technology=1 |
        | ... | additional_rcp=Yes |
        | ... | email_rcp=test@test.com |
        | ... | contract_id=12345 |
        | ... | ccoid=MYCCOID |
        | ... | phone=123123123 |
        | ... | comment=test |
        | ... | existed=yes |
        | ... | ticket_number=111 |
        | ... | print_req=no |
        | ${request_out} = | Support Request |
        | ... | Test User |
        | ... | user@mail.qa |
        | ... | New request |
        | ... | print_req=yes |
        | Log | ${req_out} |
        """
        add_rcp_ans = self._process_yes_no(additional_rcp)
        if add_rcp_ans == 'Y' and email_rcp is None:
            raise ConfigError( 'Email of additional recipients '\
                    'must be specified')

        exist_tick_ans = self._process_yes_no(existed)
        if exist_tick_ans == 'Y' and ticket_number is None:
            raise ConfigError('If ticket already exists - please '\
                                 'specify ticket number.')

        def_rcp = self._process_yes_no(customer_support)

        kwargs = {'ccoid_name': name,
                  'ccoid_contact':ccoid,
                  'contract_id':contract_id,
                  'corr_email': email,
                  'add_info': phone,
                  'subject': subject,
                  'descr': description,
                  'sub_categ': problem_subcategory,
                  'print_req': self._process_yes_no(print_req)}

        return self._cli.supportrequest(def_rcp, add_rcp_ans, email_rcp,
                       exist_tick_ans, ticket_number, technology,
                       sub_technology, appliance, problem_category, **kwargs)
