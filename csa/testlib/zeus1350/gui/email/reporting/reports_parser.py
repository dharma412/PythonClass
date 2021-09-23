# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/email/reporting/reports_parser.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon
from credentials import DUT_ADMIN, DUT_ADMIN_PASSWORD

from reports_parser_def.base_reporting_table import DataTransformOptions, \
    BaseReportingTable
from reports_parser_def.data_load_monitor import \
    verify_data_load_percentage_value, change_time_range, \
    wait_until_data_loaded, NoDataFound
from reports_parser_def.reporting_tables_helpers import get_table_class_by_name, \
    reload_current_page_with_random_data
from reports_parser_def.search_form import SearchForm


class ReportsParser(GuiCommon):
    """
    Parses reports tables under Email > Reporting tab.

    *Quick reference on keywords in this module*\n
    * Can't parse charts as for now.
    * Can parse almost any report table.
    * Allows to define time range, items displayed.
    * Allows to wait for given percentage of data ready before parsing report.
    * Allows to search at any page where search box is present.
    * Allows to open needed item(click link) in the table and then fetch results.
    """

    IS_RANDOM_DATA_MODE = False

    def get_keyword_names(self):
        return ['reports_set_random_data_mode',
                'reports_parse',
                'reports_open_item',
                'reports_search',
                'reports_open_page',
                'reports_view_tracking_details',
                'reports_export']

    def _get_controller(self, cls, *args, **kwargs):
        if issubclass(cls, BaseReportingTable):
            # do not cache table classes
            return cls(self, *args, **kwargs)
        else:
            attr_name = '_{0}'.format(cls.__name__)
            if not hasattr(self, attr_name):
                setattr(self, attr_name, cls(self, *args, **kwargs))
            return getattr(self, attr_name)

    def _get_settings_adapted_to_controller(self, controller_instance,
                                            method_params_dict):
        result = {}
        controller_elements_names = \
            controller_instance.get_contained_elements_names()
        for name, value in method_params_dict.iteritems():
            if name in controller_elements_names and value is not None:
                result[name] = value
        return result

    @set_speed(0)
    def _open_page(self, path):
        if isinstance(path, basestring):
            path = map(lambda x: x.strip(), path.split(','))
        elif path is None:
            self._debug('Page path is not given. ' \
                        'Will stay on current page.')
            return
        elif not isinstance(path, (list, tuple)):
            raise ValueError('Expected path types are ' \
                             'string or tuple/list. {0} is given'.format(type(path)))
        self.navigate_to(*path)
        if self.IS_RANDOM_DATA_MODE:
            reload_current_page_with_random_data(self)
        else:
            wait_until_data_loaded(self)

    def _prepare_controller_view(self, page=None, name=None,
                                 time_range=None, items_displayed=None,
                                 wait_for_data_completed=None,
                                 wait_timeout=60):
        self._open_page(page)
        if wait_for_data_completed is not None:
            verify_data_load_percentage_value(self, float(wait_for_data_completed),
                                              time_range, int(wait_timeout))
        elif time_range is not None:
            change_time_range(self, time_range)
        controller = self._get_controller(get_table_class_by_name(name),
                                          name)
        if items_displayed is not None:
            controller.set_options({'items_displayed': items_displayed})
        return controller

    def reports_set_random_data_mode(self, is_enabled):
        """Set random data mode. In this mode all appliance will
        be filled by random data. Use this keyword for debug
        purposes

        *Parameters:*
        - `is_enabled`: whether to enable (${True) or disable
        (${False}) random data mode

        *Return:*
        - Previous mode value. Boolean

        *Examples:*
        | ${was_enabled_previously}= | Reports Set Random Data Mode | ${True} |
        | Reports Set Random Data Mode | ${was_enabled_previously} |
        """
        previous_mode = self.IS_RANDOM_DATA_MODE
        self.IS_RANDOM_DATA_MODE = bool(is_enabled)
        return previous_mode

    def reports_search(self,
                       page=None,
                       search_text=None,
                       search_option=None,
                       match_option=None):
        """Perform search. Does not return any results.
        Use `Reports Parse` keyword to parse results after search done.

        *Parameters*:
        - `page`: Navigate to given page. String of comma separated values.
        - `search_text` - Text to search for. Mandatory string.
        - `search_option` - Search for. String, case-insensitive. Options are as they seen in WUI.
        - `match_option` - Match option. String, case-insensitive. Options are as they seen in WUI.
        Either _exact match_ or _starts with_.

        *Return*:
        None

        *Examples*:
        | Reports Search |
        | ... | page=Email, Reporting, Incoming Mail |
        | ... | search_text=mail.qa |
        | ... | match_option=exact |
        | ... | search_option=Domain |
        | ${res}= | Reports Parse |
        | ... | name=Search Results for Domains |
        | ... | items_displayed=50 |
        | Log List | ${res} |

        *Exceptions*:
        - `ValueError`: if `search_option` or `match_option` are not in list of options.
        """
        self._open_page(page)
        controller = self._get_controller(SearchForm)
        settings = self._get_settings_adapted_to_controller(controller, locals())
        controller.set(settings)
        controller.start_search()

    def reports_open_item(self,
                          page=None,
                          name=None,
                          item=None,
                          time_range=None,
                          items_displayed=None,
                          wait_for_data_completed=None,
                          wait_timeout=60):
        """
        Open item (click on link) of the table(report) at the given page.

        *Parameters*:
        - `page`: Navigate to given page. String of comma separated values.
        Do not navigate if page is not given, we are at correct page.
        - `name`: Name(header) of the table(report) as it is seen in WUI.
        - `item`: An item to click on.
        - `time_range`: Select time range option in date box. Options are as they seen in WUI.
        | Hour |
        | Day |
        | Week |
        | 30 days |
        | 90 days |
        | Yesterday (00:00 to 23:59) |
        | Previous Calendar Month |
        | Custom Range... |
        - `items_displayed`: Select items displayed. Options are as they seen in WUI.
        | 10 |
        | 20 |
        | 50 |
        | 100 |
        - `wait_for_data_completed`: Wait for percentage of data completed.
        Will periodically re-open the page page until needed percentage got or timeout occurred.
        - `wait_timeout`: Wait (seconds) before timing out.

        *Exceptions*:
        - `NoDataFound`: If no data was found for given time range.
        - `ConfigError`: If given table has no such option(s)

        *Examples*:
        | Reports Open Item |
        | ... | page=Email, Reporting, Incoming Mail |
        | ... | name=Incoming Mail Details |
        | ... | item=blabla.net |
        | ${res}= | Reports Parse |
        | ... | name=IP Addresses |
        | Log List | ${res} |
        """
        controller = self._prepare_controller_view(page, name, time_range,
                                                   items_displayed, wait_for_data_completed, wait_timeout)
        controller.open_item(item)
        if self.IS_RANDOM_DATA_MODE:
            reload_current_page_with_random_data(self)

    def reports_view_tracking_details(self,
                                      page=None,
                                      name=None,
                                      where=None,
                                      what=None,
                                      time_range=None,
                                      items_displayed=None,
                                      wait_for_data_completed=None,
                                      wait_timeout=60):
        """
        Drill down to message tracking by clicking the link in the table.

        *Parameters*:
        - `page`: Navigate to given page. String of comma separated values.
        Do not navigate if page is not given, we are at correct page.
        - `name`: Name(header) of the table(report) as it is seen in WUI.
        - `where`: Text from column and row that allows to find proper cell in table.
        - `what`: The column to get information from and click link. Please refer to examples below.
        - `time_range`: Select time range option in date box. Options are as they seen in WUI.
        | Hour |
        | Day |
        | Week |
        | 30 days |
        | 90 days |
        | Yesterday (00:00 to 23:59) |
        | Previous Calendar Month |
        | Custom Range... |
        - `items_displayed`: Select items displayed. Options are as they seen in WUI.
        | 10 |
        | 20 |
        | 50 |
        | 100 |
        - `wait_for_data_completed`: Wait for percentage of data completed.
        Will periodically re-open the page page until needed percentage got or timeout occurred.
        - `wait_timeout`: Wait (seconds) before timing out.

        *Exceptions*:
        - `NoDataFound`: If no data was found for given time range.
        - `ConfigError`: If given table has no such option(s)

        *Return*:
        Dictionary(CfgHolder). Keys:
        | text | String | Text that is present in cell |
        | clicked | Boolean | True, if it is link and it was clicked |

        *Examples*:
        | ${res} | Reports View Tracking Details |
        | ... | page=Email, Reporting, Incoming Mail |
        | ... | name=Incoming Mail Details |
        | ... | wait_for_data_completed=50 |
        | ... | where=Sender Domain, No Domain Information |
        | ... | what=Spam Detected |
        | Log | ${res} |

        | ${res} | Reports View Tracking Details |
        | ... | page=Email, Reporting, Incoming Mail |
        | ... | name=Incoming Mail Details |
        | ... | time_range=Week |
        | ... | wait_for_data_completed=50 |
        | ... | where=Sender Domain, No Domain Information |
        | ... | what=Virus Detected |
        | Log | ${res} |

        | ${res} | Reports View Tracking Details |
        | ... | page=Email, Reporting, Outgoing Senders |
        | ... | name=Sender Details |
        | ... | where=Sender Domain, unknown domain |
        | ... | what=Total Messages |
        | Log | ${res} |

        | ${res} | Reports View Tracking Details |
        | ... | page=Email, Reporting, Outgoing Senders |
        | ... | name=Sender Details |
        | ... | where=Sender Domain, unknown domain |
        | ... | what=Total Threat |
        | Log | ${res} |

        | Reports Search |
        | ... | page=Email, Reporting, Outgoing Senders |
        | ... | search_option=Internal Sender IP Address |

        | ${res} | Reports View Tracking Details |
        | ... | name=Search Results for Internal Sender IP Addresses |
        | ... | where=Sender IP Address, 10.2.1.2 |
        | ... | what=Virus Detected |
        | Log | ${res} |

        | ${res} | Reports View Tracking Details |
        | ... | name=Counters |
        | ... | what=Completed Recipients |
        | Log | ${res} |

        | ${res} | Reports View Tracking Details |
        | ... | page=Email, Reporting, Overview |
        | ... | name=System Overview |
        | ... | where=Threat Level, Messages |
        | ... | what=Outbreak Quarantine |
        | Log | ${res} |

        | ${res} | Reports View Tracking Details |
        | ... | page=Email, Reporting, Overview |
        | ... | name=System Overview |
        | ... | where=Quarantines - Top 3 by Disk Usage, Virus |
        | ... | what=Messages |
        | Log | ${res} |
        """
        controller = self._prepare_controller_view(page, name, time_range,
                                                   items_displayed, wait_for_data_completed, wait_timeout)
        if where is not None:
            return controller.click_cell(where, what)
        else:
            return controller.click_cell(what)

    def reports_parse(self,
                      page=None,
                      name=None,
                      time_range=None,
                      items_displayed=None,
                      wait_for_data_completed=None,
                      wait_timeout=60,
                      columns=None,
                      use_normalize=False,
                      first_column_as_key=False,
                      get_full_text=False,
                      result_as_dictionary=False):
        """Returns dictionary(CfgHolder) or List of values parsed in table.

        *Parameters*:
        - `page`: Navigate to given page. String of comma separated values.
        Do not navigate if page is not given, we are at correct page.
        - `name`: Name(header) of the table(report) as it is seen in WUI.
        - `time_range`: Select time range option in date box. Options are as they seen in WUI.
        | Hour |
        | Day |
        | Week |
        | 30 days |
        | 90 days |
        | Yesterday (00:00 to 23:59) |
        | Previous Calendar Month |
        | Custom Range... |
        - `items_displayed`: Select items displayed. Options are as they seen in WUI.
        | 10 |
        | 20 |
        | 50 |
        | 100 |
        - `wait_for_data_completed`: Wait for percentage of data completed.
        Will periodically re-open the page page until needed percentage got or timeout occurred.
        - `wait_timeout`: Wait (seconds) before timing out.
        - `columns`: Define which columns should be shown in the table.
        Data will be fetched only from visible columns.
        - `use_normalize`: Normalize strings that should be used as key
        of dictionary(attribute of CfgHolder class).
        - `first_column_as_key`: Make first column of the row as dictionary key. Boolean.
        - `get_full_text`: Get full text from cell or not(Long values are truncated in WUI). Boolean.
        - `result_as_dictionary`: Return all data packed as dictionary. Boolean.
        Assumes that first column is unique value in the table.

        *Exceptions*:
        - `NoDataFound`: If no data was found for given time range.
        - `ValueError`: if no `name` was given.
        - `ConfigeError`: if the table has no corresponding option(s)

        *Return*:
        Dictionary(CfgHolder) or List depending on `result_as_dictionary` parameter value

        *Examples*:
        | ${res}= | Reports Parse |
        | ... | page=Email, Reporting, Overview |
        | ... | name=Incoming Mail Summary |
        | Log List | ${res} |

        | ${res}= | Reports Parse |
        | ... | page=Email, Reporting, Overview |
        | ... | name=Outgoing Mail Summary |
        | ... | result_as_dictionary=${True} |
        | ... | use_normalize=${True} |
        | Log Dictionary | ${res} |
        | Log | Virus Messages Detected: ${res.virus_detected.messages} |

        | ${res}= | Reports Parse |
        | ... | page=Email, Reporting, System Status |
        | ... | name=System Status |
        | Log List | ${res} |

        | ${res}= | Reports Parse |
        | ... | page=Email, Reporting, System Status |
        | ... | name=Gauges |
        | Log List | ${res} |

        | ${res}= | Reports Parse |
        | ... | page=Email, Reporting, DLP Incidents |
        | ... | name=DLP Incident Details |
        | ... | first_column_as_key=${True} |
        | ... | result_as_dictionary=${True} |
        | Log Dictionary | ${res} |

        An example of how to to use `Reports Search` and `Reports Parse` keywords together.
        | Reports Search |
        | ... | page=Email, Reporting, Overview |
        | ... | search_text=${CLIENT_IP} |
        | ... | search_option=Internal Sender IP Address |
        | ${res}= | Reports Parse |
        | ... | name=Search Results for Internal Sender IP Addresses |
        | Log List | ${res} |

        | ${res}= | Reports Parse |
        | ... | page=Email, Reporting, Outgoing Destinations |
        | ... | name=Outgoing Destinations Detail |
        | ... | columns=Spam Detected, Virus Detected, Stopped by Content Filter, Total Threat, Clean, Total Processed, Hard Bounced, Delivered |
        | ... | result_as_dictionary=${True} |
        | Log Dictionary | ${res} |
        """
        controller = self._prepare_controller_view(page, name, time_range,
                                                   items_displayed, wait_for_data_completed, wait_timeout)
        if columns is not None:
            controller.set_options({'columns': columns})
        table_data = controller.get_data(get_full_text)
        if not table_data:
            raise NoDataFound('The table "{0}" contains no data'.format(name))
        return controller.transform_data(table_data, DataTransformOptions(
            use_normalize, first_column_as_key, result_as_dictionary))

    def reports_open_page(self, page=None):
        """
        Just open needed page.
        This method can be used to perform some action(eg press button) on some page.

        *Parameters*:
        - `page`: Navigate to given page. String of comma separated values.
        Do not navigate if page is not given, we are at correct page.

        *Examples*:
        | Reports Open Page | page=Email, Reporting, Overview |
        """
        self._open_page(page)

    def reports_export(self,
                       page=None,
                       name=None,
                       columns=None,
                       time_range=None,
                       items_displayed=None,
                       wait_for_data_completed=None,
                       wait_timeout=60,
                       dest_path=None,
                       username=DUT_ADMIN,
                       password=DUT_ADMIN_PASSWORD):
        """Returns dictionary(CfgHolder) or List of values parsed in table.

        *Parameters*:
        - `page`: Navigate to given page. String of comma separated values.
        Do not navigate if page is not given, we are at correct page.
        - `name`: Name(header) of the table(report) as it is seen in WUI.
        - `time_range`: Select time range option in date box. Options are as they seen in WUI.
        | Hour |
        | Day |
        | Week |
        | 30 days |
        | 90 days |
        | Yesterday (00:00 to 23:59) |
        | Previous Calendar Month |
        | Custom Range... |
        - `items_displayed`: Select items displayed. Options are as they seen in WUI.
        | 10 |
        | 20 |
        | 50 |
        | 100 |
        - `wait_for_data_completed`: Wait for percentage of data completed.
        Will periodically re-open the page page until needed percentage got or timeout occurred.
        - `wait_timeout`: Wait (seconds) before timing out.
        - `columns`: Define which columns should be shown in the table
        - `dest_path`: destination path to save exported file. Will be temporary file path
        containing ".csv" extension if omitted

        *Exceptions*:
        - `NoDataFound`: If no data was found for given time range.
        - `ValueError`: if no `name` was given.
        - `ConfigeError`: if the table has no corresponding option(s)

        *Return*:
        - Path to exported file

        *Examples*:
        | ${path}= | Reports Export |
        | ... | page=Email, Reporting, Outgoing Destinations |
        | ... | name=Outgoing Destinations Detail |
        | ... | columns=Spam Detected, Virus Detected, Stopped by Content Filter, Total Threat, Clean, Total Processed, Hard Bounced, Delivered |
        | File Should Exist | ${path} |
        """
        controller = self._prepare_controller_view(page, name, time_range,
                                                   items_displayed, wait_for_data_completed, wait_timeout)
        if columns is not None:
            controller.set_options({'columns': columns})
        return controller.export_as(dest_path, username, password)
