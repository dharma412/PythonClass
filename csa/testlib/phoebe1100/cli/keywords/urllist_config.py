#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/urllist_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class urllistconfig(CliKeywordBase):
    """
    cli -> urllistconfig

    Configure urllists.
    """

    def get_keyword_names(self):
        return ['urllist_config_newwithoutimport',
                'urllist_config_newwithimport',
                'urllist_config_edit',
                'urllist_config_delete']

    def urllist_config_newwithoutimport(self, *args):
        """Create new urllist

        urllistconfig -> new

        *Parameters:*
        - `urllist_name`: Enter a name for the URL list, REQUIRED
        - `urldomain_name`: Enter the URL domain(s) in a list, REQUIRED

        *Examples:*
        | Urllist Config Newwithoutimport | urllist_name=list1 | urldomain_name=ironport.com cisco.com |
        | Urllist Config Newwithoutimport | urllist_name=list2 | urldomain_name=cisco.com hp.com ibm.com |
        | Urllist Config Newwithoutimport | urllist_name=list3 | urldomain_name=mcaffe.com |
        | Urllist Config Newwithoutimport | urllist_name=list4 | urldomain_name=sophos.com |
        | Urllist Config Newwithoutimport | urllist_name=list5 | urldomain_name=rediff.com |
        | Urllist Config Newwithoutimport | urllist_name=list6 | urldomain_name=gmail.com |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.urllistconfig().newwithoutimport(**kwargs)

    def urllist_config_newwithimport(self, *args):
        """Create new urllist

        urllistconfig -> new

        *Parameters:*
        - `import_urllist`: Want to import a URL list, REQUIRED(Value should be Y here)
        - `assign_newname`: Assign new name to list, Default Value = N
        - `urllist_newname`: Enter name of URL list, REQUIRED
        - `urllist_imported`: Enter the name of the file on machine, REQUIRED

        *Examples:*
        | Urllist Config Newwithimport | import_urllist=Y | urllist_imported=importfile_name |
        | Urllist Config Newwithimport | import_urllist=Y | assign_newname=Y | urllist_newname=list6 | urllist_imported=importfile_name |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.urllistconfig().newwithimport(**kwargs)

    def urllist_config_edit(self, *args):
        """Edit existing urllists

        urllistconfg -> edit

        *Parameters:*
        - `option`: Choose the operation you want to perform, REQUIRED
        - `urllist_rename`: Enter the number of URL list to rename, REQUIRED
        - `urllist_name`: Enter new name for the URL list, REQUIRED
        - `assign_newname`: Assign new name to list, Default Value = N
        - `urllist_newname`: Enter name of URL list, REQUIRED
        - `urllist_imported`: Enter the name of the file on machine, REQUIRED
        - `urllist_number`: Enter the number of URL list to export, REQUIRED
        - `urllist_exported`: Enter a name for the exported file', REQUIRED

        *Examples:*
        | Urllist Config Edit | option=rename | urllist_rename=2 | urllist_name=list7 |
        | Urllist Config Edit | option=export | urllist_number=3 | urllist_exported=test |
        | Urllist Config Edit | option=import | urllist_imported=importfile_name |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.urllistconfig().edit(**kwargs)

    def urllist_config_delete(self, urllist_to_delete):
        """Delete existing urllists

        urllistconfg -> delete

        *Parameters:*
        - `urllist_to_delete`: Enter the number of URL list you wish to delete, REQUIRED

        *Examples:*
        | Urllist Config Delete | 3 |
        """
        self._cli.urllistconfig().delete(urllist_to_delete)
