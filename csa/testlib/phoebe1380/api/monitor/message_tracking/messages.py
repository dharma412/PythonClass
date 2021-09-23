from common.api.esa_api import EsaApi


class MessageTrackingMessages(EsaApi):
    def get_keyword_names(self):
        return [
            'message_tracking_messages',
        ]

    def message_tracking_messages(self, start_date=None, end_date=None, cisco_host=None, mail_policy_name=None, mail_policy_direction=None, search_option='messages', offset=None, limit=None, query_type=None, maximum_results=None):
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'mailPolicyName': mail_policy_name,
            'mailPolicyDirection': mail_policy_direction,
            'searchOption': search_option,
            'queryType': query_type,
            'offset': offset,
            'limit': limit,
            'maximumResults': maximum_results,
            # 'authType': auth_type,
            'ciscoHost': cisco_host
        }
        url = self.construct_message_tracking_api_url('messages', params)
        return self.read(url)
