from common.cli.clicommon import (CliKeywordBase, DEFAULT) 

class CsaConfig(CliKeywordBase):
    """Configure Cisco Security Awareness Settings""" 

    def get_keyword_names(self):
        return['csa_config_enable',
               'csa_config_edit',
               'csa_config_disable',
               'csa_show_list',
               'csa_update_list']

    def csa_config_enable(self,
                         csa_region,
                         csa_token,
                         csa_polling_interval):
        """
        Keyword to register the appliance with CSA Portal

        csaconfig > enable

        Parameters: 
        - 'csa_region': Available list of CSA region(s) for enable
                        1. AMERICA
                        2. EUROPE
        - 'csa_token': Token obtained from CSA portal
        - 'csa_polling_interval': Poll interval between (60minutes/1hour - 7days)

        Examples:
        | Csa Config Enable     |
        | ...  | csa_region=AMERICA|
        | ...  | csa_token=nfFGfKJhzUSkv3EuVoD6bA=    |
        | ...  | csa_polling_interval=1 Hour   |
        """
        kwargs = {
                 'csa_region': csa_region,
                 'csa_token': csa_token,
                 'csa_polling_interval': csa_polling_interval
                 }
        self._cli.csaconfig().enable(kwargs)

    def csa_config_edit(self,
                       csa_region,
                       csa_set_token=None,
                       csa_token=DEFAULT,
                       csa_polling_interval=DEFAULT):
        """
        Keyword to edit the csa configuration

        csaconfig > edit 

        Parameters: 
        - 'csa_region': Available list of CSA region(s) for enable
                        1. AMERICAS
                        2. EUROPE
        - 'csa_token': Token obtained from CSA portal 

        | Csa Config Edit   |
        | ...  | csa_region=AMERICAS    |
        | ...  | csa_set_token=Y    |
        | ...  | csa_token=nfFGfKJhzUSkv3EuVoD6bA=    |
        | ...  | csa_polling_interval=2 day    |
        """
        kwargs = {
                 'csa_region': csa_region,
                 'csa_token': csa_token,
                 'csa_polling_interval': csa_polling_interval
                 }

        if csa_set_token is not None:
            kwargs.update({'csa_set_token': csa_set_token})

        self._cli.csaconfig().edit(kwargs)

    def csa_config_disable(self, csa_disable=DEFAULT):
        """
        Keyword to disable Cisco Security Awareness(CSA)
          
        csaconfig > disable

        Parameters:
        - `csa_disable`: Are you sure you want to disable CSA 

        Examples:
        | Csa Config Disable | csa_disable=Yes |
        """
        self._cli.csaconfig().disable(csa_disable='yes') 

    def csa_show_list(self):
        """ Displays the downloaded csa list.

        *Parameters*:
         None

        *Return*:
         Returns list variable with the Report ID, Last Updated Time and List Status of csa

        *Examples*:

        |@{showlist_detail}= |  Csa Show List  |

        """

        out1=  self._cli.csaconfig().showlist()
        list1=  [out1.report_id,out1.last_updated,out1.list_status]
        return list1

    def csa_update_list(self):
        """ Update the csa list.

        *Parameters*:
         None

        *Return*:
         Command output

        *Examples*:
        |${output}=   Csa Update List  |

        """
      
        return str(self._cli.csaconfig().updatelist())
