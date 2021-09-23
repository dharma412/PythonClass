from common.api.esa_api import EsaApi


class Blocklist(EsaApi):
    def get_keyword_names(self):
        return [
            'quarantine_blocklist_get',
            'quarantine_blocklist_add',
            'quarantine_blocklist_delete',
        ]

    def quarantine_blocklist_get(self, params={}):
        """
        ESA API Keyword to get Quarantine Blocklist details

        :Arguments:
            params - A dictionary consisting of following keys
                action : Type - string, Available Values - view
                viewBy : Type - string, Available Values - recipient,sender
                quarantineType : Type - string, Available Values - spam
                orderDir : Type - string, Available Values - desc,asc
                orderBy : Type - string, Available Values - recipient,sender
                offset : Type - string
                limit : Type - string
        
        :Examples:
            | ${params} =          | Create Dictionary                    |
            | ... | action         | view                                 |
            | ... | viewBy         | recipient                            |
            | ... | quarantineType | spam                                 |
            | ... | orderDir       | desc                                 |
            | ... | orderBy        | recipient                            |
            | ... | offset         | 0                                    |
            | ... | limit          | 1                                    |
            | ... | ${response} =  | Qurantine Blocklist Get | ${params}  |
        """
        url = self.construct_quarantine_api_url('blocklist')
        return self.read(url, params=params)

    def quarantine_blocklist_add(self, action='add', quarantine_type='spam', recipient_list=[], sender_list=[], view_by='sender'):
        """
        ESA API Keyword to add Quarantine Blocklist details

        :Arguments:
            action : Type - string, Available Values - add
            quarantine_type : Type - string, Available Values - spam
            recipient_list : Type - list
            sender_list : Type - list
            view_by : Type - string, Available Values - recipient,sender
        
        :Examples:
            | ${recipients} =       | Create List               |
            | ... | a@b.com         | b@c.com                   |
            | ${sender} =           | Create List               |
            | ... | c@d.com         | d@e.com                   |
            | ${response} =         | Quarantine Blocklist Add  |
            | ... | action          | view                      |
            | ... | view_by         | recipient                 |
            | ... | quarantine_type | spam                      |
            | ... | recipient_list  | ${recipients}             |
            | ... | sender_list     | ${sender}                 |
        """
        url = self.construct_quarantine_api_url('blocklist')
        params = {
            "action": action,
            "quarantineType": quarantine_type,
            "recipientList": recipient_list,
            "senderAddresses": sender_list,
            "viewBy": view_by
        }
        return self.create(url, data=params)

    def quarantine_blocklist_delete(self, quarantine_type='spam', sender_list=[], view_by='sender'):
        """
        ESA API Keyword to delete Quarantine Blocklist details

        :Arguments:
            quarantine_type : Type - string, Available Values - spam
            sender_list : Type - list
            view_by : Type - string, Available Values - sender
        
        :Examples:
            | ${response} =         | Quarantine Blocklist Delete |
            | ... | view_by         | sender                      |
            | ... | quarantine_type | spam                        |
            | ... | sender_list     | ${sender}                   |
        """
        url = self.construct_quarantine_api_url('blocklist')
        params = {
            "quarantineType": quarantine_type,
            "senderList": sender_list,
            "viewBy": view_by
        }
        return self.delete(url,  data=params)
