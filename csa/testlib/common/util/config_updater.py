#!/usr/bin/env python

# $Id: //prod/main/sarf_centos/testlib/common/util/config_updater.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $


import xml.etree.ElementTree as ET
import os
from common.util.utilcommon import UtilCommon

# This constant is needed because the original <!DOCTYPE section misses into result XML data
SYSTEM_DOCTYPE = "<!DOCTYPE config SYSTEM \"config.dtd\">"


class ConfigUpdater(UtilCommon):
    """This python script finds needed nodes from input XML and replaces these nodes' values.
    Purpose: update of WSA system XML config files.
    """

    # keywords
    # reads given config XML file

    def read_xml_config(self, input_file):
        """Starts XML file reading.
        This keyword should be used before Set Xml Config Value and Write Xml Config.

        Parameters:
           - `input_file`: path of the input XML file

        Examples:
        | Read Xml Config |
        | ... | input_file=config.xml |
        """
        self.input_file = input_file
        in_file = open(input_file, "r")
        self.tree = ET.parse(in_file)
        in_file.close()

    # replaces value of the first found node to new value.
    def set_xml_config_value(self, xpath, value):
        """Sets node value. Uses XPATH locator to determine the node in the XML tree.
        This keyword should be used after Read Xml Config.

        Parameters:
           - `xpath`: XPATH of node
           - `value`: value that replaces node's value

        Examples:
        | Set Xml Config Value |
        | ... | xpath=./prox_acl_group_ip |
        | ... | value=11.22.33.0/24 |
        """
        root = self.tree.getroot()
        nodes = root.findall(xpath)
        if len(nodes) == 0:
            raise RuntimeError, 'No nodes found!'
        self._info('Found %d node(s)\n' % len(nodes))
        self._debug('Replacing value of the first node')
        node = nodes[0]
        self._info('Replacing value: %s -> %s' % (node.text, value))
        node.text = value

    # creates and saves new config with changes are made by set methods
    def write_xml_config(self, output_file=None):
        """Writes new config file with changes are made by set methods.
        This method will write to input_file If output_file parameter is None.
        This keyword should be used after Read Xml Config.

        Parameters:
           - `output_file`: path of the output XML file

        Examples:
        | Write Xml Config |
        | ... | output_file=output.xml |
        """
        if (output_file is None):
            self._debug('Output file parameter is None')
            in_file = open(self.input_file, "w")
            self._info('Output file %s' % in_file)
            in_file.write(SYSTEM_DOCTYPE)
            self.tree.write(in_file)
            in_file.close()
            self._info('done!')
        else:
            self._debug('Output file parameter is not None')
            out_file = open(output_file, "w+")
            self._info('Output file %s' % out_file)
            out_file.write(SYSTEM_DOCTYPE)
            self.tree.write(out_file)
            out_file.close()
            self._info('done!')

    # RF Hybrid API for Test Libraries
    def get_keyword_names(self):
        return [
            'read_xml_config',
            'set_xml_config_value',
            'write_xml_config',
        ]
