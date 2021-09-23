from common.api.esa_api import EsaApi


class MailAmpFileReputationUpdate(EsaApi):
    def get_keyword_names(self):
        return [
            'reporting_mail_amp_reputation_update',
        ]

    def reporting_mail_amp_reputation_update(self, category='', start_date=None, end_date=None, top=None):
        """
        *ESA Reporting API Keyword* to send API queries to
        _mail_amp_reputation_update_ endpoint

        *Arguments*
            params - A dictionary consisting of following keys
                category : Type - string, Available Values -
                    console_url, filenames, msg_direction, old_disposition, timestamped_tuple
                start_date : Type - string, Allowed Pattern - 2020-07-06T19:00:00.000Z
                end_date : Type - string, Allowed Pattern - 2020-07-06T19:00:00.000Z
                top : Type - string, Allowed Pattern - 10, 20, 30 etc
        
        *Examples*
            | ${response}= | Reporting Mail Amp Reputation Update |
            | ...          | category=console_url                 |
            | ...          | start_date=2020-07-06T19:00:00.000Z  |
            | ...          | end_date=2020-07-07T20:00:00.000Z    |
            | ...          | top=25                               |
        """
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'top': top,
            # 'authType': auth_type,
            'device_type': 'esa'
        }
        url = self.construct_reporting_api_url(
            'mail_amp_reputation_update', category, params)
        return self.read(url)
