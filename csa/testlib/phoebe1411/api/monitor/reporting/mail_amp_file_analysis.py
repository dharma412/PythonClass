from common.api.esa_api import EsaApi


class MailAmpFileAnalysis(EsaApi):
    def get_keyword_names(self):
        return [
            'reporting_mail_amp_file_analysis_by_filename',
        ]
    
    def reporting_mail_amp_file_analysis_by_filename(self, category='', start_date=None, end_date=None, order_by=None, order_dir=None):
        """
        *ESA Reporting API Keyword* to send API queries to
        _mail_amp_file_analysis_by_filename_ endpoint

        *Arguments*
            params - A dictionary consisting of following keys
                category : Type - string, Available Values -
                    completed_timestamp, console_url, interim_verdict, msg_direction,
                    run_id, score, status, submit_timestamp, url, console_url, filenames,
                    msg_direction, old_disposition, timestamped_tuple
                start_date : Type - string, Allowed Pattern - 2020-07-06T19:00:00.000Z
                end_date : Type - string, Allowed Pattern - 2020-07-06T19:00:00.000Z
                order_by : Type - string, Available Values - submit_timestamp
                order_dir : Type - string, Available Values - desc,asc
        
        *Examples*
            | ${response}= | Reporting Mail Amp File Analysis By Filename |
            | ...          | start_date=2020-07-06T19:00:00.000Z          |
            | ...          | end_date=2020-07-07T20:00:00.000Z            |
            | ...          | order_by=submit_timestamp                    |
            | ...          | order_dir=desc                               |

            | ${response}= | Reporting Mail Amp File Analysis By Filename |
            | ...          | category=completed_timestamp                 |
            | ...          | start_date=2020-07-06T19:00:00.000Z          |
            | ...          | end_date=2020-07-07T20:00:00.000Z            |
            | ...          | order_by=submit_timestamp                    |
            | ...          | order_dir=desc                               |
        """
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'orderBy': order_by,
            'orderDir': order_dir,
            # 'authType': auth_type,
            'device_type': 'esa'
        }
        url = self.construct_reporting_api_url(
            'mail_amp_file_analysis_by_filename', category, params)
        return self.read(url)
