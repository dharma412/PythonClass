#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/iniparser.py#1 $

# python imports
import ConfigParser
import os

# sarf imports
from common.util.utilcommon import UtilCommon


class IniParser(UtilCommon):
    """
    Wrap ConfigParser functionality into keywords
    """

    _rootdir = os.path.join(os.getenv("SARF_HOME"), "tests/testdata/cpt")
    _baselinedir = os.path.join(_rootdir, "baseline")

    def __init__(self, *args, **kwargs):
        UtilCommon.__init__(self, *args, **kwargs)
        self._config = ConfigParser.ConfigParser()

    def get_keyword_names(self):
        return [
            'read_config_file',
            'get_config_sections',
            'has_config_section',
            'get_config_options',
            'has_config_option',
            'get_config_option_value'
        ]

    def read_config_file(self, model):
        """
        Read the config file based on the given model
        Iterate through all the entries in the 'Common' area
        and read those files
        """
        upperModel = model.upper()
        path = os.path.join(self._rootdir, upperModel)
        self._config.read(path)
        commonList = self.get_config_options('Common')
        for option in commonList:
            value = self.get_config_option_value('Common', option)
            value_path = os.path.join(self._baselinedir, value)
            self._config.read(value_path)

    def get_config_sections(self):
        """ 
        Return a list of the sections available;
        DEFAULT is not included in the list
        """
        return self._config.sections()

    def has_config_section(self, section):
        """ 
        Indicates whether the named section is present in the
        configuration. The DEFAULT section is not acknowledged
        """
        return self._config.has_section(section)

    def get_config_options(self, section):
        """
        Returns a list of options available in the specified section
        """
        return self._config.options(section)

    def has_config_option(self, section, option):
        """
        If the given section exists, and contains the given option
        return True, otherwise return False
        """
        return self._config.has_option(section, option)

    def get_config_option_value(self, section, option):
        """
            Get an option value for the named section
            Remove leading and trailing spaces from the 
            option values: A value can have the format
            <val1>&<val2>|<val3>&<val4>
            "&" represents "and" operator; "|" is the "or" operator
        """
        returnString = ""
        rawValues = self._config.get(section, option)
        orList = rawValues.split("|")  # remove spaces between |
        for x in orList:
            andList = x.strip().split("&")  # remove spaces between ,
            # put andList together again
            andListString = ""
            for y in andList:
                andListString = andListString + "&" + y.strip()
            # remove leading ,
            andListString = andListString[1:]
            # put retrunString together
            returnString = returnString + "|" + andListString
        # remove leading |
        returnString = returnString[1:]

        return returnString
