#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/external_threatfeeds_manager.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from sal.containers import cfgholder

BUTTON_ADD_EXTERNAL_THREATFEEDS_SOURCE =  "//input[@value='Add Source']"
SOURCE_NAME="id=source_name"
SOURCE_DESCRIPTION="id=source_description"
SOURCE_HOSTNAME="id=source_hostname"
SOURCE_POLLING_PATH="id=source_polling_path"
SOURCE_COLLECTION_NAME="id=source_collection_name"
SOURCE_COLLECTION_AGE="id=source_collection_age"
POLL_CHUNK_SIZE="id=poll_chunk_size"
POLL_INTERVAL_HOUR="id=poll_interval_hour"
POLL_INTERNAL_MINS="id=poll_interval_mins"
SOURCE_USE_HTTPS_YES="id=use_https_yes"
SOURCE_USE_HTTPS_NO="id=use_https_no"
POLL_PORT="id=poll_port"
SOURCE_CONFIGURE_CRED_YES="id=source_config_cred_yes"
SOURCE_CONFIGURE_CRED_NO="id=source_config_cred_no"
SOURCE_AUTH_USER="id=cc_auth_user"
SOURCE_AUTH_PASS="id=cc_auth_pass"
EDIT_LINK = lambda row: "//table[@class='cols']/tbody/tr[%d]/td/a" % row
SUBMIT_BUTTON= "//*[@type='button' and @value='Submit']"
ETF_SOURCE_TABLE="//td[@id='content']/form/dl/dd/table"
HTTP_PROXY_YES="id=use_global_proxy_yes"
HTTP_PROXY_NO="id=use_global_proxy_no"


class ExternalThreatfeedsManager(GuiCommon):
    """
    External Threat Feeds Manager page interaction class.
    'Mail Policies -> External Threat Feeds Manager' section.
    """
    def _open_page(self):
        self._navigate_to('Mail Policies', 'External Threat Feeds Manager')

    def get_keyword_names(self):
        return ['external_threatfeeds_source_add',
                'external_threatfeeds_source_edit',
                'external_threatfeeds_source_delete',
                'external_threatfeeds_source_resume',
                'external_threatfeeds_source_suspend']

    def _click_link_to_edit(self, src_name, table_loc):
        (rowp, colp) = self._cell_indexes(src_name, table_loc)
        if rowp is None:
            raise ValueError, '"%s" is not present' % (src_name,)
        self.click_element(EDIT_LINK(rowp+1))

    def _cell_indexes(self, item_name, table_loc):
        self._info('Getting row, column for %s in %s table' %\
        (item_name, table_loc))
        rows = len(self._selenium.find_elements_by_xpath("%s/tbody/tr" % (table_loc)))
        cols = len(self._selenium.find_elements_by_xpath("%s/tbody/tr[1]/th" % (table_loc)))
        for col in xrange(0, cols):
            for row in xrange(0, rows):
                read_name = self._get_table_cell("xpath=%s.%s.%s"%(table_loc, row, col))
                if read_name == item_name:
                    return (row, col)
                elif item_name in read_name and 'view' in read_name.lower():
                    return (row, col)
        return (None, None)

    def _fill_source_details(self,
                         source_name=None,
                         new_source_name=None,
                         description=None,
                         hostname=None,
                         polling_path=None,
                         collection_name=None,
                         polling_age=None,
                         chunk_size=None,
                         polling_interval_hour=None,
                         polling_interval_mins=None,
                         use_https=None,
                         polling_port=None,
                         enable_proxy=None,
                         configure_credentials=None,
                         username=None,
                         password=None):
        """ Populates External Threat Feeds source table with data.

        Parameters:
        - `source_name`: Name of the external threat feed source.
        - `new_source_name`: Name of the external threat feed source used while editing an existing source.
        - `description`: description of the threat feed source which is to be added
        - `hostname`: host url of the threat source.
        - `polling_path`: polling path of the threat source to download threat feeds.
        - `collection_name`: type of threat feeds to be polled for.
        - `polling_age`: to configure the number of days old feeds to be downloaded from the threat source
        - `chunk_size`: to configure the number of chunk the feedage is divided to.
        - `polling_interval_hour`: polling interval(in hrs) for delta downloads
        - `polling_interval_mins`: polling interval(in mins) for delta downloads
        - `use_https`: enable/disable https depending on the threat feed source
        - `polling_port`: 80/443 port based on http or https. Custom port can also be configured..
        - `enable_proxy`: enable to use proxy server
        - `configure_credentials`: Enable credentials if the threat feed source supports authentication.
        - `username`: User name of the threat feed source url for authencating before download of the feeds.
        - `password`: User name of the threat feed source url for authencating before download of the feeds..

        Return:
        None
        """
        if source_name is not None:
            self.input_text(SOURCE_NAME, source_name)
        if new_source_name is not None:
            self.input_text(SOURCE_NAME, new_source_name)
        if description is not None:
            self.input_text(SOURCE_DESCRIPTION, description)
        if hostname is not None:
            self.input_text(SOURCE_HOSTNAME, hostname)
        if polling_path is not None:
            self.input_text(SOURCE_POLLING_PATH, polling_path)
        if collection_name is not None:
            self.input_text(SOURCE_COLLECTION_NAME, collection_name)
        if polling_age is not None:
            self.input_text(SOURCE_COLLECTION_AGE, polling_age)
        if chunk_size is not None:
            self.input_text(POLL_CHUNK_SIZE, chunk_size)
        if polling_interval_hour is not None:
            self.input_text(POLL_INTERVAL_HOUR, polling_interval_hour)
        if polling_interval_mins is not None:
            self.input_text(POLL_INTERNAL_MINS, polling_interval_mins)
        if  use_https is not None:
            if 'yes' in use_https.lower():
                self._click_radio_button(SOURCE_USE_HTTPS_YES)
            else:
                self._click_radio_button(SOURCE_USE_HTTPS_NO)
        if polling_port is not None:
            self.input_text(POLL_PORT, polling_port)
        if enable_proxy is not None:
            if 'yes' in enable_proxy.lower():
                self._click_radio_button(HTTP_PROXY_YES)
            else:
                self._click_radio_button(HTTP_PROXY_NO)
        if configure_credentials is not None:
            if 'yes' in configure_credentials.lower():
                self._click_radio_button(SOURCE_CONFIGURE_CRED_YES)
                self.input_text(SOURCE_AUTH_USER, username)
                self.input_text(SOURCE_AUTH_PASS, password)
            else:
                self._click_radio_button(SOURCE_CONFIGURE_CRED_NO)
        self.click_button(SUBMIT_BUTTON)

    def external_threatfeeds_source_add(self,
                         source_name=None,
                         description=None,
                         hostname=None,
                         polling_path=None,
                         collection_name=None,
                         polling_age=None,
                         chunk_size=None,
                         polling_interval_hour=None,
                         polling_interval_mins=None,
                         use_https=None,
                         polling_port=None,
                         enable_proxy=None,
                         configure_credentials=None,
                         username=None,
                         password=None):
        """ Adds new Threat Feeds Source.

        Parameters:
        - `source_name`: Name of the external threat feed source.
        - `description`: description of the threat feed source which is to be added
        - `hostname`: host url of the threat source.
        - `polling_path`: polling path of the threat source to download threat feeds.
        - `collection_name`: type of threat feeds to be polled for.
        - `polling_age`: to configure the number of days old feeds to be downloaded from the threat source
        - `chunk_size`: to configure the number of chunk the feedage is divided to.
        - `polling_interval_hour`: polling interval(in hrs) for delta downloads
        - `polling_interval_mins`: polling interval(in mins) for delta downloads
        - `use_https`: enable/disable https depending on the threat feed source
        - `polling_port`: 80/443 port based on http or https. Custom port can also be configured..
        - `enable_proxy`: enable to use proxy server
        - `configure_credentials`: Enable credentials if the threat feed source supports authentication.
        - `username`: User name of the threat feed source url for authencating before download of the feeds.
        - `password`: User name of the threat feed source url for authencating before download of the feeds..

        Return:
        None

        Examples:
        | External Threatfeeds Source Add |
        | ...  | source_name=test1 |
        | ...  | description=test modified to test1 |
        | ...  | hostname=test1.com |
        | ...  | polling_path=/test1-data |
        | ...  | collection_name=test1.ch |
        | ...  | polling_age=90 |
        | ...  | chunk_size=90 |
        | ...  | polling_interval_hour=5 |
        | ...  | polling_interval_mins=0 |
        | ...  | use_https=no |
        | ...  | enable_proxy=yes |
        | ...  | configure_credentials=yes |
        | ...  | username=guest_1 |
        | ...  | password=guest |

        """
        self._info('Adding Threat feeds source  %s' % source_name)
        self._open_page()
        self.click_button(BUTTON_ADD_EXTERNAL_THREATFEEDS_SOURCE)
        self._fill_source_details(source_name=source_name,
                         description=description,
                         hostname=hostname,
                         polling_path=polling_path,
                         collection_name=collection_name,
                         polling_age=polling_age,
                         chunk_size=chunk_size,
                         polling_interval_hour=polling_interval_hour,
                         polling_interval_mins=polling_interval_mins,
                         use_https=use_https,
                         polling_port=polling_port,
                         enable_proxy=enable_proxy,
                         configure_credentials=configure_credentials,
                         username=username,
                         password=password)

    def external_threatfeeds_source_edit(self,
                         source_name,
                         new_source_name=None,
                         description=None,
                         hostname=None,
                         polling_path=None,
                         collection_name=None,
                         polling_age=None,
                         chunk_size=None,
                         polling_interval_hour=None,
                         polling_interval_mins=None,
                         use_https=None,
                         polling_port=None,
                         enable_proxy=None,
                         configure_credentials=None,
                         username=None,
                         password=None):

        """ Edits External threatfeeds source..

        Parameters:
        - `source_name`: Name of the external threat feed source to be edited.
        - `new_source_name`: Name of the external threat feed source used while editing an existing source.
        - `description`: description of the threat feed source which is to be added
        - `hostname`: host url of the threat source.
        - `polling_path`: polling path of the threat source to download threat feeds.
        - `collection_name`: type of threat feeds to be polled for.
        - `polling_age`: to configure the number of days old feeds to be downloaded from the threat source.
        - `chunk_size`: to configure the number of chunk the feedage is divided to.
        - `polling_interval_hour`: polling interval(in hrs) for delta downloads
        - `polling_interval_mins`: polling interval(in mins) for delta downloads
        - `use_https`: enable/disable https depending on the threat feed source
        - `polling_port`: 80/443 port based on http or https. Custom port can also be configured..
        - `enable_proxy`: enable to use proxy server
        - `configure_credentials`: Enable credentials if the threat feed source supports authentication.
        - `username`: User name of the threat feed source url for authencating before download of the feeds.
        - `password`: User name of the threat feed source url for authencating before download of the feeds..

        Return:
        None

        Example:
        | External Threatfeeds Source Edit |  test |
        | ...  | new_source_name=test1 |
        | ...  | description=test modified to test1 |
        | ...  | hostname=test1.com |
        | ...  | polling_path=/test1-data |
        | ...  | collection_name=test1.ch |
        | ...  | polling_age=90 |
        | ...  | chunk_size=90 |
        | ...  | polling_interval_hour=5 |
        | ...  | polling_interval_mins=0 |
        | ...  | use_https=no |
        | ...  | enable_proxy=yes |
        | ...  | configure_credentials=yes |
        | ...  | username=guest_1 |
        | ...  | password=guest |

        """
        self._info('Editing External threatfeed source %s' % source_name)
        self._open_page()
        self._click_link_to_edit(source_name, ETF_SOURCE_TABLE)
        self._fill_source_details(new_source_name=new_source_name,
                         description=description,
                         hostname=hostname,
                         polling_path=polling_path,
                         collection_name=collection_name,
                         polling_age=polling_age,
                         chunk_size=chunk_size,
                         polling_interval_hour=polling_interval_hour,
                         polling_interval_mins=polling_interval_mins,
                         use_https=use_https,
                         enable_proxy=enable_proxy,
                         polling_port=polling_port,
                         configure_credentials=configure_credentials,
                         username=username,
                         password=password)

    def external_threatfeeds_source_delete(self, source_name):
        """ Deletes External Threat feeds source.

        Parameters:
        - `source_name`: Name of the external threat feed source to be deleted.

        Return:
            None

        Example:
        | External Threatfeeds Source Delete | test_source |

        """
        del_img = \
        lambda row: "%s/tbody/tr[%d]/td[7]/img" % (ETF_SOURCE_TABLE, row)
        self._info('Deleting External threatfeed source %s' % source_name)
        self._open_page()
        (rowp, colp) = self._cell_indexes(source_name, ETF_SOURCE_TABLE)
        if rowp is None:
            raise ValueError, '"%s" threatfeed source is not present' % source_name
        self.click_element(del_img(rowp+1), "don't wait")
        self._click_continue_button()

    def external_threatfeeds_source_resume(self, source_name):
        """ Deletes External Threat feeds source.

        Parameters:
        - `source_name`:- Name of the threatfeed source to be resumed

        Return:
            None

        Example:
        | External Threatfeeds Source Resume | test_source |

        """
        resume_img = \
        lambda row: "%s/tbody/tr[%d]/td[6]/a" % (ETF_SOURCE_TABLE, row)
        self._info('Resuming External threatfeed source %s' % source_name)
        self._open_page()
        (rowp, colp) = self._cell_indexes(source_name, ETF_SOURCE_TABLE)
        if rowp is None:
            raise ValueError, '"%s" threatfeed source is not present' % source_name
        resume_title = '%s/@title' %(resume_img(rowp+1))
        if self._selenium.get_attribute(resume_title) == 'Resume':
            self.click_element(resume_img(rowp+1), "don't wait")
        else:
            self._info('External threatfeed source is already resumed..')

    def external_threatfeeds_source_suspend(self, source_name):
        """ Deletes External Threat feeds source.

        Parameters:
        - `source_name`:- Name of the external threat feed source to be suspended

        Return:
            None

        Example:
        | External Threatfeeds Source Suspend | test_source |
        """
        suspend_img = \
        lambda row: "%s/tbody/tr[%d]/td[6]/a" % (ETF_SOURCE_TABLE, row)
        self._info('Supsending External threatfeed source %s' % source_name)
        self._open_page()
        (rowp, colp) = self._cell_indexes(source_name, ETF_SOURCE_TABLE)
        if rowp is None:
            raise ValueError, '"%s" threatfeed source is not present' % source_name
        suspend_title = '%s/@title' %(suspend_img(rowp+1))
        if self._selenium.get_attribute(suspend_title) == 'Suspend':
            self.click_element(suspend_img(rowp+1), "don't wait")
        else:
            self._info('External threatfeed source is already Suspended..')
