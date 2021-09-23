# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/amp_config.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class ampconfig(CliKeywordBase):
    """
    cli -> ampconfig
    ampconfig
        Edit configuration for the following engines:
         Ironport FireAmp
    """

    def get_keyword_names(self):
        return ['ampconfig_case_setup',
                'ampconfig_case_advanced',
                'ampconfig_case_advanced_private',
                'ampconfig_case_clearcache',
                'ampconfig_case_modifytimeout',
                'ampconfig_case_file_group_print']


    def ampconfig_case_setup(self, *args):
        """
        This will edit the configuration of FireAmp.

        ampconfig -> setup

        Parameters:
        - `use_malware_protection` : use Advanced-Malware protection. Either 'yes' or 'no'
        - `protection_license_agreement` : accept licence aggrement. Either 'yes' or 'no'
        - `use_malware_file_analysis` : use Advanced-Malware file analysis. Either 'yes' or 'no'
        - `modify_filetypes` : modify the file types selected for File Analysis. Either 'yes' or 'no'
        - `change_filetypes` : change the file types selected for File Analysis. Either 'yes' or 'no'
        - `select_filetypes` : Enter comma separated serial numbers for file types or select all
        - `file_analysis_license_agreement` : accept licence agreement. Either 'yes' or 'no'
        - `processing_timeout` : Processing Timeout in sec. Default: 120 Range: 60-300
        - `protection_confirm_disable` : The system will no longer check messages for malwares.
           Either 'yes' or 'no'
        - `file_analysis_confirm_disable` : The system will no longer run file analysis for malware scan.
           Either 'yes' or 'no'
        - `upload_all_filetype` : Upload all filetypes supported by cloud service. Either 'yes' or 'no'
        - `upload_msdownload` : Upload filetype 'application/x-msdownload' for File Analysis.
           Either 'yes' or 'no'
        - `upload_dosexec` : Upload filetype 'application/x-dosexec' for File Analysis.
           Either 'yes' or 'no'
        - `upload_msdos_program` : Upload filetype 'application/x-msdos-program' for File Analysis.
           Either 'yes' or 'no'
        - `none_selected_proceed` : None of the files will be uploaded for File Analysis.
           Do you want to proceed. Either 'yes' or 'no'

        Examples:
        | ampconfig setup | use_malware_protection=yes | use_malware_file_analysis=yes | processing_timeout=180 |
        | ampconfig setup | use_malware_protection=yes | use_malware_file_analysis=yes | upload_all_filetype=yes | processing_timeout=180 |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.ampconfig().setup(**kwargs)

    def ampconfig_case_advanced(self,*args):
        """
        This will edit the configuration of FireAmp.

        ampconfig -> advanced

        Parameters:
        - `cloud_query_timeout` : Time limit to querying cloud to check file reputation in sec. Default: 2 Range: 1 - 5
        - `cloud_domain` : Server URL for AMP file analysis
        - `cloud_server_pool` : Reputation cloud server pool url
        - `use_recommended_threshold` : use the recommended reputation threshold: YES or NO
        - `reputation_threshold` : Specify threshold for AMP file reputation. Default: 60 Range: 1 - 100
        - `file_analysis_server_select` : Select the file analysis server type:
                                          1. AMERICAS (https://panacea.threatgrid.com)
                                          2. Private Cloud
        - `file_analysis_server_url` : Server URL for AMP file analysis(provided Private Cloud is selected)
        - `certificate_option` : There are two options -
                                 1. Use Cisco Trusted Root Certificate List
                                 2. Paste certificate to CLI
        - `paste_cert` : Paste the certificate(provided Paste certificate to CLI is selected)
        - `heartbeat_interval` : Heartbeat interval for AMP file reputaion. Default: 15 Range: 1 - 30
        - `enable_SSL_communication` : enable SSL communication for file reputation: YES or NO
        - `change_proxy` : to change proxy detail: YES or NO
        - `server_url` : tunnel(proxy) server url
        - `proxy_port` : proxy port
        - `username` : username for server url
        - `edit_passphrase` : to edit passphrase: YES or NO
        - `password` : password for server url
        - `use_existing_reputation_proxy` : Use the existing file reputation proxy: YES or NO
        - `change_proxy_settings` : to change the existing reputation proxy detail: YES or NO
        - `file_analysis_server_detail` : proxy settings server detail
        - `file_analysis_proxy_port` : file analysis proxy port
        - `file_analysis_proxy_username` : username for file analysis server url
        - `edit_password` : to edit passphrase: YES or NO
        - `file_analysis_proxy_password` : password for file analysis server url


        Examples:
        | ampconfig advanced | cloud_query_timeout=3 |
        | ... | cloud_domain=a.immunet.com |
        | ... | reputation_cloud_server=cloud-sa.amp.sourcefire.com |
        | ... | cloud_domain=a.immunet.com |
        | ... | use_recommended_threshold=YES |
        | ... | reputation_threshold=180 |
        | ... | file_analysis_server_select=Private Cloud |
        | ... | file_analysis_server_url=https://intel.api.sourcefire.com |
        | ... | certificate_option=Paste certificate to CLI |
        | ... | paste_cert=${CERTIFICATE} |
        | ... | heartbeat_interval=15 |
        | ... | enable_SSL_communication=YES |
        | ... | change_proxy=YES |
        | ... | server_url=1.1.1.1 |
        | ... | proxy_port=443 |
        | ... | username=admin |
        | ... | password=ironport |

        """
        kwargs = self._convert_to_dict(args)
        if not kwargs.has_key('file_analysis_server_select'):
            kwargs['file_analysis_server_select']='Private analysis cloud'
        if not kwargs.has_key('certificate_option'):
            kwargs['certificate_option']='Use Cisco Trusted Root Certificate List'
        self._cli.ampconfig().advanced(**kwargs)

    def ampconfig_case_advanced_private(self,*args):
        """
        This will edit the configuration of FireAmp.

        ampconfig -> advanced

        Parameters:
        - `cloud_query_timeout` : Time limit to querying cloud to check file reputation in sec. Default: 2 Range: 1 - 5
        - `cloud_domain` : Server URL for AMP file analysis
        - `cloud_server_pool` : Reputation cloud server pool url
        - `use_recommended_threshold` : use the recommended reputation threshold: YES or NO
        - `reputation_threshold` : Specify threshold for AMP file reputation. Default: 60 Range: 1 - 100
        - `file_analysis_server_select` : Select the file analysis server type:
                                          1. AMERICAS (https://panacea.threatgrid.com)
                                          2. Private Cloud
        - `file_analysis_server_url` : Server URL for AMP file analysis(provided Private Cloud is selected)
        - `certificate_option` : There are two options -
                                 1. Use Cisco Trusted Root Certificate List
                                 2. Paste certificate to CLI
        - `paste_cert` : Paste the certificate(provided Paste certificate to CLI is selected)
        - `heartbeat_interval` : Heartbeat interval for AMP file reputaion. Default: 15 Range: 1 - 30
        - `enable_SSL_communication` : enable SSL communication for file reputation: YES or NO
        - `change_proxy` : to change proxy detail: YES or NO
        - `server_url` : tunnel(proxy) server url
        - `proxy_port` : proxy port
        - `username` : username for server url
        - `edit_passphrase` : to edit passphrase: YES or NO
        - `password` : password for server url
        - `private_fa_config_type` : type of private config
        - `private_tg_type` : type of TG private cluster config
        - `tg_ip` : TG ip or Hostname
        - `tg_priority` : TG ip or Hostname
        - `tg_priority_edit` : TG ip or Hostname to be edited
        - `tg_priority_delete` : TG ip or Hostname to be deleted
        - `use_existing_reputation_proxy` : Use the existing file reputation proxy: YES or NO
        - `change_proxy_settings` : to change the existing reputation proxy detail: YES or NO
        - `file_analysis_server_detail` : proxy settings server detail
        - `file_analysis_proxy_port` : file analysis proxy port
        - `file_analysis_proxy_username` : username for file analysis server url
        - `edit_password` : to edit passphrase: YES or NO
        - `file_analysis_proxy_password` : password for file analysis server url

        Examples:
        | ampconfig case advanced private| cloud_query_timeout=3 |
        | ... | cloud_domain=a.immunet.com |
        | ... | reputation_cloud_server=cloud-sa.amp.sourcefire.com |
        | ... | cloud_domain=a.immunet.com |
        | ... | use_recommended_threshold=YES |
        | ... | reputation_threshold=180 |
        | ... | file_analysis_server_select=Private Cloud |
        | ... | file_analysis_server_url=https://intel.api.sourcefire.com |
        | ... | certificate_option=Paste certificate to CLI |
        | ... | paste_cert=${CERTIFICATE} |
        | ... | heartbeat_interval=15 |
        | ... | enable_SSL_communication=YES |
        | ... | change_proxy=YES |
        | ... | server_url=1.1.1.1 |
        | ... | proxy_port=443 |
        | ... | username=admin |
        | ... | password=ironport |
        | ... | private_fa_config_type=New Config |
        | ... | private_tg_type=New or Add or Edit or Delete|
        | ... | tg_ip=2.2.2.2 |
        | ... | tg_priority=2 |

        """
        kwargs = self._convert_to_dict(args)
        if not kwargs.has_key('file_analysis_server_select'):
            kwargs['file_analysis_server_select']='Private Cloud'
        if not kwargs.has_key('private_fa_config_type'):
            kwargs['private_fa_config_type']='OLD'
        if not kwargs.has_key('certificate_option'):
            kwargs['certificate_option']='Use Cisco Trusted Root Certificate List'
        self._cli.ampconfig().advanced(**kwargs)

    def ampconfig_case_clearcache(self,*args):
        """
        This will clear the the local File Reputation cache.

        ampconfig -> clearcache

        Parameters:
        - `clear_cache` : Clears the local File Reputation cache: Yes or No.

        Examples:
        | ampconfig clearcache | clear_cache=yes |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.ampconfig().cachesettings(**kwargs).clearcache(**kwargs)

    def ampconfig_case_modifytimeout(self,*args):
        """
        This will enter the cache expiry period values for cache settings.

        ampconfig -> modifytimeout

        Parameters:
        - `modify_timeout` : Select from the three options-
                             1. CLEAN
                             2. MALICIOUS
                             3. UNKNOWN

        Examples:
        | ampconfig modifytimeout | modify_timeout=CLEAN |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.ampconfig().cachesettings(**kwargs).modifytimeout(**kwargs)

    def ampconfig_case_file_group_print(self, *args):
        """
        This will edit the configuration of FireAmp.

        ampconfig -> setup

        Parameters:
        - `use_malware_protection` : use Advanced-Malware protection. Either 'yes' or 'no'
        - `protection_license_agreement` : accept licence aggrement. Either 'yes' or 'no'
        - `use_malware_file_analysis` : use Advanced-Malware file analysis. Either 'yes' or 'no'
        - `modify_filetypes` : modify the file types selected for File Analysis. Either 'yes' or 'no'
        - `select_file_groups` : Enter comma separated serial numbers for file groups
        - `select_file_action` : Select the action to perform. Add,Delete and Print options are available, but in this case we use print
        - `file_analysis_license_agreement` : accept licence agreement. Either 'yes' or 'no'

        Examples:
        | ampconfig case file group print | use_malware_protection=yes | use_malware_file_analysis=yes | modify_filetypes=yes | select_file_grou
ps=1 | select_file_action=print|

        """
        kwargs = self._convert_to_dict(args)
        return self._cli.ampconfig().setup_print(**kwargs)

