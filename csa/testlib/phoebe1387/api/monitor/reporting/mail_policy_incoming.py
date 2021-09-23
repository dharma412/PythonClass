from common.api.esa_api import EsaApi


class MailPolicyIncoming(EsaApi):
    def get_keyword_names(self):
        return [
            'reporting_mail_policy_incoming',
        ]

    def reporting_mail_policy_incoming(self, category='', start_date=None, end_date=None, top=None, query_type=None, offset=None, limit=None):
        """
        *ESA Reporting API Keyword* to send API queries to
        _mail_policy_incoming_ endpoint

        *Arguments*
            params - A dictionary consisting of following keys
                category : Type - string, Available Values - recipients_matched
                start_date : Type - string, Allowed Pattern - 2020-07-06T19:00:00.000Z
                end_date : Type - string, Allowed Pattern - 2020-07-06T19:00:00.000Z
                top : Type - string, Allowed Pattern - 10, 20, 30 etc
                query_type : Type - string, Available Values - export, exportAll
                offset : Type - string, Allowed Pattern - 0, 20, 30 etc
                limit : Type - string, Allowed Pattern - 10, 20, 30 etc

        *Examples*
            | ${response}= | Reporting Mail Policy Incoming      |
            | ...          | start_date=2020-07-06T19:00:00.000Z |
            | ...          | end_date=2020-07-07T20:00:00.000Z   |

            | ${response}= | Reporting Mail Policy Incoming      |
            | ...          | category=recipients_matched         |
            | ...          | start_date=2020-07-06T19:00:00.000Z |
            | ...          | end_date=2020-07-07T20:00:00.000Z   |
            | ...          | query_type=export                   |
            | ...          | top=50                              |
            | ...          | offset=10                           |
        """
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'top': top,
            'query_type': query_type,
            'offset': offset,
            'limit': limit,
            # 'authType': auth_type,
            'device_type': 'esa'
        }
        url = self.construct_reporting_api_url(
            'mail_policy_incoming', category, params)
        return self.read(url)
