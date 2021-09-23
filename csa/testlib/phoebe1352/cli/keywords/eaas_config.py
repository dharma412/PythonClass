# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/eaas_config.py#1 $
# $DateTime: 2020/01/17 04:04:23 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase

class EaasConfig(CliKeywordBase):
    """Configure Advanced Phishing Protection settings"""

    def get_keyword_names(self):
        return ['eaas_config_register',
                'eaas_config_edit',
                'eaas_config_enable',
                'eaas_config_disable']

    def eaas_config_register(self, *args):
        """
        Keyword to register the appliance with APP portal

        eaasconfig > register

        Parameters:
        - `eaas_region`: Available list of APP region(s) for the registration
                         1. AMERICA
        - `eaas_passphrase`: Passphrase obtained from APP portal
        - `eaas_enable_app`: Would you like enable APP

        Examples:
        | Eaas Config Register              |
        | ... | eaas_region=AMERICA         |
        | ... | eaas_passphrase=ironport    |
        | ... | eaas_enable_app=Yes         |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.eaasconfig().register(**kwargs)

    def eaas_config_edit(self, *args):
        """
        Keyword to register the appliance with APP portal

        eaasconfig > edit

        Parameters:
        - `eaas_region`: Available list of APP region(s) for the registration
                         1. AMERICA
        - `eaas_passphrase`: Passphrase obtained from APP portal

        Examples:
        | Eaas Config Edit                  |
        | ... | eaas_region=AMERICA         |
        | ... | eaas_passphrase=ironport    |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.eaasconfig().edit(**kwargs)

    def eaas_config_enable(self, *args):
        """
        Keyword to register the appliance with APP portal

        eaasconfig > enable

        Parameters:
        - `eaas_enable_app`: Are you sure you want to enable APP

        Examples:
        | Eaas Config Enable | eaas_enable_app=Yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.eaasconfig().enable(**kwargs)

    def eaas_config_disable(self, *args):
        """
        Keyword to disable Advanced Phishing Protection

        eaasconfig > disable

        Parameters:
        - `eaas_disable_app`: Are you sure you want to enable APP

        Examples:
        | Eaas Config Disable | eaas_disable_app=Yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.eaasconfig().disable(**kwargs)
