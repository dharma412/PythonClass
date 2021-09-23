from common.ngui.exceptions import DataNotFoundError
from common.ngui.ngguicommon import NGGuiCommon

class MailPolicyDetails(NGGuiCommon):

    def get_keyword_names(self):
        return ['get_incoming_policies',
                'get_outgoing_policies',
                'get_top_incoming_policies',
                'get_top_outgoing_policies',
                'view_policy_messages',
                'export_mail_policies',
                'add_policies_report_favourite']

    def get_incoming_policies(self):
        """
        To get the All Incoming Policies details
        :return: outgoing policies dict
        """
        return self._get_policy_table_details(MailPolicy.Incoming_Policies)

    def get_outgoing_policies(self):
        """
        To get the All Outgoing Policies details
        :return: outgoing policies dict
        """
        return self._get_policy_table_details(MailPolicy.Outgoing_Policies)

    def get_top_incoming_policies(self):
        """
        To get the Top incoming Policies details
        :return: incoming policies dict
        """
        return self._get_top_policies(MailPolicy.Top_Incoming_Mailpolicies_label,
                                 MailPolicy.Top_Incoming_Mailpolicies_value)

    def get_top_outgoing_policies(self):
        """
        To get the Top Outgoing Policies details
        :return: outgoing policies dict
        """
        return self._get_top_policies(MailPolicy.Top_Outgoing_Mailpolicies_label,
                                 MailPolicy.Top_Outgoing_Mailpolicies_value)

    def view_policy_messages(self, policy_type, policy_name):
        """
        To view the policy messages
        :param policy_type: Incoming|Outgoing
        :param policy_name:  <PolicyName>
        :return:  Navigated to the tracking page
        """
        if policy_type == 'Incoming':
            self.click_element('%s%s' %(MailPolicy.Incoming_Policies, MailPolicy.Policy_message %(policy_name)))
        elif policy_type == 'Outgoing':
            self.click_element('%s%s' % (MailPolicy.Outgoing_Policies, MailPolicy.Policy_message % (policy_name)))
        else:
            raise DataNotFoundError('Invalid Policy Type')
        self.select_window('NEW')

    def export_mail_policies(self):
        """
        To export the Mail Policies details
        :return:
        """
        self.click_button(MailPolicy.Export)
        self._wait_until_element_is_present(MailPolicy.Download, timeout=10)
        self.click_element(MailPolicy.Download)

    def _get_top_policies(self, label, value):
        details = {}
        self.set_selenium_speed('0s')
        if self._is_element_present(label):
            for eachrow in range(1, self.get_element_count(label) + 1):
                details[self.get_text('%s[%s]' % (label, eachrow))] = self.get_text('%s[%s]' % (value, eachrow))
            self.set_selenium_speed('0.5s')
        else:
            raise DataNotFoundError('Failed to find the Top policy details')
        return details

    def _get_policy_table_details(self, table):
        details = {}
        self.set_selenium_speed('0s')
        row_cell = '%s/div' %(table)
        if self._is_element_present(row_cell):
            for eachrow in range(1, self.get_element_count(row_cell)+1):
                details[self.get_text('%s/div[%s]/div/div[1]' %(table, eachrow))] = \
                    self.get_text('%s/div[%s]/div/div[2]' %(table, eachrow))
            self.set_selenium_speed('0.5s')
        else:
            raise DataNotFoundError('Failed to find the policy details')
        return details

    def add_policies_report_favourite(self, report):

        """To add Policies report to Favourite my reports
        :param report: Incoming|Outgoing
        :return: raise DataNotFoundError if results not found
        """
        report_index = {'Incoming':1, 'Outgoing':2}
        if report not in report_index:
            raise DataNotFoundError('Failed to find the policy report:%s' %report)
        self.click_button(MailPolicy.Add_Favourite %report_index[report])


class MailPolicy:
    
    Incoming_Policies = "//*[@title='Incoming Policies']/ancestor::div[@class='reporting_table__title-section ng-scope']" \
                        "/following-sibling::div[@class='reporting_table__body ng-scope']" \
                        "//div[@class='ui-grid-viewport ng-isolate-scope']/div"
    Outgoing_Policies = "//*[@title='Outgoing Policies']/ancestor::div[@class='reporting_table__title-section ng-scope']" \
                        "/following-sibling::div[@class='reporting_table__body ng-scope']" \
                        "//div[@class='ui-grid-viewport ng-isolate-scope']/div"
    Top_Incoming_Mailpolicies = "//*[@class='reporting_graph__wrapper ng-scope mailPolicyIncoming_graph-wrapper']"
    Top_Outgoing_Mailpolicies = "//*[@class='reporting_graph__wrapper ng-scope mailPolicyOutgoing_graph-wrapper']"
    Top_Incoming_Mailpolicies_label = "%s/div[1]/div" % Top_Incoming_Mailpolicies
    Top_Incoming_Mailpolicies_value = "%s/div[3]/div" % Top_Incoming_Mailpolicies
    Top_Outgoing_Mailpolicies_label = "%s/div[1]/div" % Top_Outgoing_Mailpolicies
    Top_Outgoing_Mailpolicies_value = "%s/div[3]/div" % Top_Outgoing_Mailpolicies
    Policy_message = "/div/div/div/div[2][text()='%s']/../../div[2]/div[2]/a"
    Export = "//*[@id='export']"
    Download = "//*[@ng-click='$ctrl.exportReport()']"
    Add_Favourite = "(//*[@class='ngsma-add-to-my-report__fav-btn'])[%s]"
