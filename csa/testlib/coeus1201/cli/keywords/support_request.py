#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/support_request.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class SupportRequest(CliKeywordBase):
    """ Sends status information for support purposes."""

    def get_keyword_names(self):
        return [
            'support_request'
        ]

    def support_request(self,
        customer_support=DEFAULT,
        additional_rcp=DEFAULT,
        email_rcp=None,
        ccoid_option=DEFAULT,
        ccoid=None,
        name=None,
        contract_id=None,
        email=None,
        phone=DEFAULT,
        subject=None,
        comment=None,
        existed=DEFAULT,
        ticket_number=DEFAULT,
        tech = DEFAULT,
        subtech = DEFAULT,
        cat = DEFAULT,
        subcat = DEFAULT,
        ):
        """Support Request.
        The information includes: status detail, tophosts, 10 seconds of rate,
        and showconfig. The showconfig output does not include uncommitted
        changes.

        Parameters:
        - `customer_support`: specify 'Yes' if this is ticket to Cisco IronPort
                Customer Support. Optional. Either 'Yes' or 'No'.
        - `additional_rcp`: specify 'Yes' if you want to send the support request
                to additional recipient(s). Either 'Yes' or 'No'. Optional.
        - `email_rcp`: if additional recipient is chosen - specify the email
                address(es) to which you want to send the support request.
                Mandatory.
        - `ccoid_option`: whether to create new CCOID or use existing one.
                Only numbers should be given. '1' for creating new CCOID.
                Existing CCOID's order -  recent ones will be at the top.
        - `ccoid`: new CCOID of the contact person. Required for creating
                new CCOID.
        - `contract_id`: contract ID of the contact person.
        - `name`: string with the name of the contact person.
        - `email`: email address of your CCO User ID. Mandatory.
        - `phone`: string with contact phone number value. Optional.
        - `subject`: string with ticket object. Mandatory.
        - `comment`: additional comment to a ticket. Mandatory.
        - `existed`: specify 'Yes' if this support request associated
                with an existing support ticket.
        - `ticket_number`: existing support ticket number.
        - `tech` : select a technology related to this support request
           | 1 | Security - Email and Web |
           | 2 | Security - Management |
        - `subtec` - select a subtechnology related to this support request
           If technology selected is  1 - Security - Email and Web  then
           sub_technology is one of the following:
           | 1 | Cisco Web Security Appliance (WSA) - CIWUC |
           | 2 | Cisco Web Security Appliance (WSA) - Other |
           | 3 | Cisco Web Security Appliance (WSA) - WBRS |
           | 4 | Web Security Appliance - Virtual |
           If technology selected is 2 - Security - Management | then
           sub_technology is one of the following
           | 1 | Email-related issue |
           | 2 | Web-related issue |
           | 3 | Other issue |
        - `cat` - select the problem category
           If sub_technology is Web Security Appliance - Virtual,
           then problem_category is one of the following:
           | 1 | Installation |
           | 2 | Licensing |
           For everything else, it is one of the following:
           | 1 | Install |
           | 2 | Configure |
           | 3 | Operate |
           | 4 | Upgrade |
         - `subcat` - select a problem sub-category:
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
            | 9 | Product Feature/Function Question |
            if problem_catory is 'Operate' - then
            problem_subcategory is one of the following:
            | 1 | Interoperability |
            | 2 | Password Recovery |
            | 3 | Licensing |
            | 4 | Hardware Failure |
            | 5 | Error Messages, Logs |
            | 6 | Software Failure |
            | 7 | Product Feature/Function Question |
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
            | 11| Product Feature/Function Question |


        Examples:
        | Support Request |
        | ... | additional_rcp=Yes |
        | ... | email_rcp=test@test.com |
        | ... | ccoid_option=1
        | ... | ccoid=tester
        | ... | contract_id=123456
        | ... | name=Test |
        | ... | email=qa@test.com |
        | ... | phone=123123123 |
        | ... | subject=test |
        | ... | comment=test |
        | ... | existed=yes |
        | ... | ticket_number=111 |
        | ... | tech=1 |
        | ... | subtech=2 |
        | ... | cat=3 |
        | ... | subcat=4 |
        """

        if not all([contract_id, ccoid_option, ccoid, name, email,\
                  subject, comment]):
            raise ValueError('Not all data is specified.')

        kwargs = {'def_rcp': self._process_yes_no(customer_support),
                  'add_rcp': self._process_yes_no(additional_rcp),
                  'rcp_email': email_rcp,
                  'name': name,
                  'contract_id': contract_id,
                  'email': email,
                  'phone': phone,
                  'subject': subject,
                  'comment': comment,
                  'tech' : tech,
                  'subtech' : subtech,
                  'cat' : cat,
                  }

        if str(subtech) != '4':
            kwargs['subcat'] = subcat

        if ccoid_option == 1 and ccoid is None:
            raise ConfigError('If you want to create new ccoid - please '\
                                 'specify the ccoid.')
        else:
	    kwargs['select_ccoid'] = ccoid_option
            kwargs['new_ccoid'] = ccoid

        if existed and existed != '' and existed.lower() != 'no':
            if not ticket_number:
                raise ValueError('If ticket exists - please '\
                                 'specify ticket_number.')
            else:
                kwargs['exist_tick'] = self._process_yes_no(existed)
                kwargs['tick_num'] = ticket_number

        self._cli.supportrequest(**kwargs)

