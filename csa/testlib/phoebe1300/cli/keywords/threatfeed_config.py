#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/threatfeed_config.py#1 $
# $DateTime:
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class ThreatConfig(CliKeywordBase):
    """This class provide keywords to configure threat feeds on ESA.
       Below is the flow of threatfeedconfig command:

     esa> threatfeedconfig

    Choose the operation you want to perform:
    - SOURCECONFIG - Source Configuration.
    []> sourceconfig


    Choose the operation you want to perform:
    - ADD - Add a Source.
    []> add

    Choose the operation you want to perform:
    - POLL URL - Add source via Polling Path and Collection name.
    []> POLL URL

    Enter the Source name:
    []> Abuse

    Enter a description for this source:
    []> Abuse

    Enter the host name:
    []> hailataxii.com

    Enter the polling path:
    []> /taxii-data

    Enter the collection name:
    []> guest.Abuse_ch

    Enter the polling interval(in minutes):
    [60]>

    Do you want to use HTTPS? []> no

    Enter the polling port:
    [80]>

    Do you want to configure credentials? [N]>

    Abuse successfully added.

    Choose the operation you want to perform:
    - ADD - Add a Source.
    - LIST - List out all the Sources.
    - EDIT - Edit a source.
    - DELETE - Delete a source.
    []> list

    1. Abuse - Abuse

    Choose the operation you want to perform:
    - ADD - Add a Source.
    - LIST - List out all the Sources.
    - EDIT - Edit a source.
    - DELETE - Delete a source.
    []>
    []> edit

    1. Abuse - Abuse
    Enter the name or number of the source you wish to edit.
    []> 1

    Abuse - Abuse
    Enter the Source name:
    [Abuse]> source1

    Enter a description for this source:
    [Abuse]> source1

    Enter the host name:
    [hailataxii.com]> intelfeed.malwerewolf.com

    Enter the polling path:
    [/taxii-data]> /skym-taxii-ws/PollService

    Enter the collection name:
    [guest.Abuse_ch]> WEBFLOWS_2167721018_V3

    Enter the polling interval(in minutes):
    [60]> 15

    Do you want to use HTTPS? [N]>

    Enter the polling port:
    [80]>

    Do you want to configure credentials? [N]>

    source1 edited.

    Choose the operation you want to perform:
    - ADD - Add a Source.
    - LIST - List out all the Sources.
    - EDIT - Edit a source.
    - DELETE - Delete a source.
    []>
    []> delete

    1. source1 - source1
    Enter the name or number of the source you wish to delete.
    []> 1

    source1
    Are you sure you want to delete source1? [N]> y

    source1 is deleted.

    Choose the operation you want to perform:
    - ADD - Add a Source.
    []>
    """

    def get_keyword_names(self):
        return ['threatfeedconfig_setup',
                'threatfeedconfig_status',
                'threatfeedconfig_sourceconfig_poll_url_add',
                'threatfeedconfig_sourceconfig_poll_url_list',
                'threatfeedconfig_sourceconfig_poll_url_detail',
                'threatfeedconfig_sourceconfig_poll_url_edit',
                'threatfeedconfig_sourceconfig_poll_url_suspend',
                'threatfeedconfig_sourceconfig_poll_url_resume',
                'threatfeedconfig_sourceconfig_poll_url_delete', ]

    def threatfeedconfig_setup(self, *args):
        """
        This will setup threatfeed configuration

        threatfeedconfig -> setup

        *Parameters*:
        - `use_etf` : enable external threatfeed
                     Either 'yes' or 'no'
        - `confirm_disable` : want to disable. Either 'yes' or 'no'
        - `license_agreement` : accept agreement. Either 'yes' or 'no'
        - `custom_header` : want to enable for disable customer header. Either 'yes' or 'no'
        - `header_name` : Enter the header name
        - `header_content` : Enter the header content

        *Examples*:

        |  Threatfeedconfig Setup | use_etf=yes |
        |  ThreatfeedConfig Setup | use_etf=no | confirm_disable=yes |
        |  Threatfeedconfig Setup | use_etf=yes |  custom_header=yes  | header_name=test | header_content=false |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.threatfeedconfig('setup').setup(**kwargs)

    def threatfeedconfig_status(self, *args):
        """Run threatfeedconfig -> setup command. Using this keyword you're able to
        read current status of external threatfeed

        *Parameters:*

        *Return:*
        string containing user status after command finished. Can be one of:
        'disabled' or 'eanbled' (without quotes).

        *Examples:*
        | ${etf_status} | Threatfeedconfig Status |
        """
        return self._cli.threatfeedconfig('setup').threatfeed_status()

    def threatfeedconfig_sourceconfig_poll_url_add(self, *args):
        """
        Keyword to add a new poll url to get threat feeds.

        :params:
            poll_url_source_name: Source name.
            poll_url_source_description: Source description.
            poll_url_host_name: Hostname of the threat feeds repository.
            poll_url_polling_path: Polling path.
            poll_url_collection_name: Collection name.
            poll_url_polling_interval: Polling interval (default: 60 minutes)
            poll_url_use_https: Whether to use HTTPS or not.
            poll_url_polling_port: Polling port to use.
            poll_url_configure_credentials: Whether to use credentials.
        :return:
            None
        :examples:
            Threatfeedconfig Sourceconfig Poll Url Add
            ...  poll_url_source_name=Abuse
            ...  poll_url_source_description=Abuse
            ...  poll_url_host_name=hailataxii.com
            ...  poll_url_polling_path=/taxii-data
            ...  poll_url_collection_name=guest.Abuse_ch
            ...  poll_url_polling_interval=30
            ...  poll_url_use_https=N
            ...  poll_url_polling_port=80
            ...  poll_url_configure_credentials=N
        """
        kwargs = self._convert_to_dict(args)
        self._cli.threatfeedconfig('sourceconfig').add(**kwargs)

    def threatfeedconfig_sourceconfig_poll_url_list(self):
        """
        Keyword to list the configured threat feed poll urls
        :return:
            Returns the configured poll urls names in string format.

        :examples:
        ${poll_urls}=  Threatfeedconfig Sourceconfig Poll Url List
        Log  ${poll_urls}
        """
        return self._cli.threatfeedconfig('sourceconfig').list()

    def threatfeedconfig_sourceconfig_poll_url_detail(self, poll_url_source_name=None):
        """
        Keyword to detail the configured threat feed poll urls

        :params:
            poll_url_source_name: Source name.
        :return:
            Returns the configured poll urls names in string format.

        :examples:
        ${source_detail}=  Threatfeedconfig Sourceconfig Poll Url Detail
        ...  poll_url_source_name=Abuse
        Log  ${source_detail}
        """
        return self._cli.threatfeedconfig('sourceconfig').detail(poll_url_source_name)

    def threatfeedconfig_sourceconfig_poll_url_edit(self, *args):
        """
        Keyword to edit configuration of any configured  threat feed poll url

        :params:
            poll_url_source_name: Original source name.
            poll_url_source_newname: New source name.
            poll_url_source_description: Source description.
            poll_url_host_name: Hostname of the threat feeds repository.
            poll_url_polling_path: Polling path.
            poll_url_collection_name: Collection name.
            poll_url_polling_interval: Polling interval (default: 60 minutes)
            poll_url_use_https: Whether to use HTTPS or not.
            poll_url_polling_port: Polling port to use.
            poll_url_configure_credentials: Whether to use credentials.
        :return:
            None
        :examples:
            Threatfeedconfig Sourceconfig Poll Url Edit
            ...  poll_url_source_name=Abuse
            ...  poll_url_source_newname=Abusive
            ...  poll_url_source_description=Abusive
            ...  poll_url_host_name=aila.hailataxii.com
            ...  poll_url_polling_path=/aila-taxii-data
            ...  poll_url_collection_name=guest.Abusive_channel
            ...  poll_url_polling_interval=45
        """
        kwargs = self._convert_to_dict(args)
        self._cli.threatfeedconfig('sourceconfig').edit(**kwargs)

    def threatfeedconfig_sourceconfig_poll_url_suspend(self, *args):
        """
        Keyword to suspend any configured  threat feed poll url

        :params:
            poll_url_source_name: Source name to Suspend.
            confirm_suspend: Confirm Suspend operation (Yes/No)
        :return:
            None
        :examples:
            Threatfeedconfig Sourceconfig Poll Url Suspend
            ...  poll_url_source_name=Abusive
            ...  confirm_suspend=Yes
        """
        kwargs = self._convert_to_dict(args)
        self._cli.threatfeedconfig('sourceconfig').suspend(**kwargs)

    def threatfeedconfig_sourceconfig_poll_url_resume(self, *args):
        """
        Keyword to delete any configured  threat feed poll url

        :params:
            poll_url_source_name: Source name to Resume.
            confirm_resume: Confirm Resume operation (Yes/No)
        :return:
            None
        :examples:
            Threatfeedconfig Sourceconfig Poll Url Resume
            ...  poll_url_source_name=Abusive
            ...  confirm_resume=Yes
        """
        kwargs = self._convert_to_dict(args)
        self._cli.threatfeedconfig('sourceconfig').resume(**kwargs)

    def threatfeedconfig_sourceconfig_poll_url_delete(self, *args):
        """
        Keyword to delete any configured  threat feed poll url

        :params:
            poll_url_source_name: Source name to delete.
            confirm_delete: Confirm delete operation (Yes/No)
        :return:
            None
        :examples:
            Threatfeedconfig Sourceconfig Poll Url Delete
            ...  poll_url_source_name=Abusive
            ...  confirm_delete=Yes
        """
        kwargs = self._convert_to_dict(args)
        self._cli.threatfeedconfig('sourceconfig').delete(**kwargs)
