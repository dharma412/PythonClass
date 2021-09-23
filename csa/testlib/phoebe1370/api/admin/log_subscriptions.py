from common.api.esa_api import EsaApi


class LogSubscriptions(EsaApi):
    def get_keyword_names(self):
        return [
            'log_subscriptions_list_subscriptions',
            'log_subscriptions_list_log_files',
            'log_subscriptions_get_log_file_content',
        ]

    def log_subscriptions_list_subscriptions(self, retrieval_method=None, use_auth=True, headers={}):
        """
        ESA keyword to send API calls to log subscriptions end point /config/logs/subscription

        *Params:*
        - `retrieval_method`: Method of log retreival. Accepted values are - manual, syslog_push,
                              scp_push

        *Examples:*
        | ${subscriptions}= | Log Subscriptions List Subscriptions |
        | ${subscriptions}= | Log Subscriptions List Subscriptions |
        | ...               | retrieval_method=syslog_push         |
        
        | ${auth_header}=   | Create Dictionary                    |
        | ...  Authorization| Bearer ${access_token}               |

        | ${response}=      | Log Subscriptions List Subscriptions |
        | ...               | use_auth=${False}                    |
        | ...               | headers=${auth_header}               |
        """
        params = {
            'retrievalMethod': retrieval_method
        }
        url = self.construct_log_subscriptions_api_url(params=params)
        return self.read(url, auth=use_auth, headers=headers)

    def log_subscriptions_list_log_files(self, category=None, start_date=None, end_date=None, compute_hash=None,
                                         use_auth=True, headers={}):
        """
        ESA keyword to send API calls to log subscriptions end point /config/logs/subscription

        *Params:*
        - `category`: Log category. Eg: amp, audit_logs, mail_logs etc
        - `start_date`: Start date for API query. Accepted format - 2020-08-23T06:45:00.000Z
        - `end_date`: Start date for API query. Accepted format - 2020-08-25T06:45:00.000Z
        - `compute_hash`: Whether to compute hash or not. Accepted values - True, False

        *Examples:*
        | ${log_files}=      | Log Subscriptions List Log Files |
        | ... | category     | amp                              |
        | ... | start_date   | 2020-08-23T06:45:00.000Z         |
        | ... | end_date     | 2020-08-25T06:45:00.000Z         |
        | ... | compute_hash | True                             |

        | ${auth_header}=   | Create Dictionary                 |
        | ...  Authorization| Bearer ${access_token}            |

        | ${response}=      | Log Subscriptions List Log Files  |
        | ... | category    | amp                               |
        | ... | start_date  | 2020-08-23T06:45:00.000Z          |
        | ... | end_date    | 2020-08-25T06:45:00.000Z          |
        | ...               | use_auth=${False}                 |
        | ...               | headers=${auth_header}            |
        """
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'computeHash': compute_hash
        }
        url = self.construct_log_subscriptions_api_url(category, params)
        return self.read(url, auth=use_auth, headers=headers)

    def log_subscriptions_get_log_file_content(self, download_url=None, use_auth=True, headers={}):
        """
        ESA keyword to send API calls to log subscriptions end point /config/logs/subscription

        *Params:*
        - `download_url`: Download URL retrieved from "Log Subscriptions List Log Files" keyword.

        *Examples:*
        | ${log_files}=      | Log Subscriptions List Log Files |
        | ... | category     | amp                              |
        | ... | start_date   | 2020-08-23T06:45:00.000Z         |
        | ... | end_date     | 2020-08-25T06:45:00.000Z         |
        | ... | compute_hash | True                             |

        | FOR  ${log_file}  IN  ${log_files}                                |
        |     ${download_url}=     | Get From Dictionary                    |
        |     ...                  | ${log_file}        | downloadUrl       |
        |     ${log_file_content}= | Log Subscriptions Get Log File Content |
        |     ...                  | download_url=${download_url}           |
        | END                                                               |

        | ${auth_header}=   | Create Dictionary                 |
        | ...  Authorization| Bearer ${access_token}            |

        | ${log_files}=      | Log Subscriptions List Log Files |
        | ... | category     | amp                              |
        | ... | start_date   | 2020-08-23T06:45:00.000Z         |
        | ... | end_date     | 2020-08-25T06:45:00.000Z         |
        | ... | compute_hash | True                             |
        | ...                | use_auth=${False}                |
        | ...                | headers=${auth_header}           |
        """
        url = self.api_url + download_url
        return self.read(url, auth=use_auth, headers=headers)
