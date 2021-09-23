#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/trace_def/trace_output_parser.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

import json
from pprint import pprint
import re
import os

LEVEL2_MAGIC = 9999
PARSER_JS = """
var result = new Object();
var LEVEL2_MAGIC = 9999;
var str_result = "";

var is_node_containing_attribute = function(node, attr_name, attr_value) {
    if(node.attributes) {
        for(var attr_index = 0; attr_index < node.attributes.length; attr_index++) {
            var attr = node.attributes.item(attr_index);
            if(attr.nodeName.toLowerCase() == attr_name && attr.nodeValue == attr_value) {
                return true;
            }
        }
    }
    return false;
}
var trim = function(s) {
    return s.replace(/^\s+|\s+$/g, "");
}
var get_key_content = function(node) {
    if(node.getElementsByTagName("s").length > 0) {
        return trim(node.getElementsByTagName("s")[0].innerHTML);
    } else {
        return trim(node.innerHTML).replace(/:$/g, "");
    }
}

var all_rows = new Array();
var all_tables = window.document.getElementsByTagName("table");
for(var table_index = 0; table_index < all_tables.length; table_index++) {
    var table_node = all_tables.item(table_index);
    if(is_node_containing_attribute(table_node, "class", "pairs")) {
        var tbody_node = table_node.getElementsByTagName("tbody")[0];
        all_rows = new Array();
        for(var child_index = 0; child_index < tbody_node.childNodes.length;
            child_index++) {
            var child_row = tbody_node.childNodes.item(child_index);
            if(child_row.nodeName.toLowerCase() == "tr") {
                all_rows.push(child_row);
            }
        }
        break;
    }
}

var last_key_level1_item = "", last_key_level2_item = "";
var current_level = 1;
if(all_rows) {
    for(var row_index = 0; row_index < all_rows.length; row_index++) {
        var row_node = all_rows[row_index];
        var level_changed = false;

        if(is_node_containing_attribute(row_node, "class", "group")) {
            last_key_level1_item = get_key_content(row_node);
            result[last_key_level1_item] = new Array();
            level_changed = current_level != 1;
            current_level = 1;
            continue;
        }

        if(row_node.childNodes && last_key_level1_item) {
            for(var child_index = 0; child_index < row_node.childNodes.length;
                child_index++) {
                var cell_node = row_node.childNodes.item(child_index);
                if(cell_node.nodeName.toLowerCase() == "th" && cell_node.attributes) {
                    if(is_node_containing_attribute(cell_node, "colspan", "2")) {
                        last_key_level2_item = get_key_content(cell_node);
                        var pair = new Object()
                        pair[last_key_level2_item] = LEVEL2_MAGIC;
                        result[last_key_level1_item].push(pair);
                        level_changed = current_level != 2;
                        current_level = 2;
                        break;
                    }
                }
            }
        }
        if(level_changed) {
            continue;
        }

        var key = "";
        var value = "";
        if(row_node.childNodes) {
            for(var child_index = 0; child_index < row_node.childNodes.length;
                child_index++) {
                var cell_node = row_node.childNodes.item(child_index);
                if(cell_node.nodeName.toLowerCase() == "th" && !key) {
                    key = get_key_content(cell_node);
                }
                if(cell_node.nodeName.toLowerCase() == "td" && !value) {
                    value = row_index + 1;
                }
                if (key && value) {
                    break;
                }
            }
        }

        if(key && value && last_key_level1_item) {
            var pair = new Object()
            pair[key] = value;
            result[last_key_level1_item].push(pair);
        }
    }
}

return JSON.stringify(result);
"""

TRACE_TABLE = "//table[@class='pairs']"
TRACE_TABLE_DATA_CELL = lambda index: "%s/tbody/tr[%d]/td[last()]" % (TRACE_TABLE, index)


class TraceOutputParser(object):
    def __init__(self, gui_common):
        self.gui = gui_common

    def _parse_results_table(self):
        parse_result = self.gui._selenium.execute_script(PARSER_JS)
        self.gui._debug('JS eval result: %s' % (parse_result,))
        result_dict = json.loads(parse_result)
        return self._get_eval_result_pretty_formatted(result_dict)

    def _get_eval_result_pretty_formatted(self, js_eval_result_dict={}):
        result_dict = {}
        for key, entry_pairs in js_eval_result_dict.iteritems():
            prepared_key = re.sub(r'\n\s+', ' ', key)
            result_dict[prepared_key] = {}
            dest_dict = result_dict[prepared_key]
            for entry_pair in entry_pairs:
                entry_name = entry_pair.keys()[0]
                entry_pos = entry_pair[entry_name]
                if entry_pos == LEVEL2_MAGIC:
                    result_dict[prepared_key][entry_name] = {}
                    dest_dict = result_dict[prepared_key][entry_name]
                else:
                    dest_dict[entry_name] = self.gui.get_text(TRACE_TABLE_DATA_CELL(entry_pos))
        return result_dict

    def get_details(self):
        details = self._parse_results_table()
        pprint(details)
        return details
