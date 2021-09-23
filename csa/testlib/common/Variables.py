# $Id: //prod/main/sarf_centos/testlib/common/Variables.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""
That modules is a simple wrapper for Robot's BuiltIn variable methods
If used from Robot, it returns all Robot's variables
If used outside of Robot, it allows setting and getting global variables
Usage:
import common.Variables
...
    variables = common.Variables.get_variables()
"""

from robot.libraries.BuiltIn import BuiltIn

variables_dictionary = {
    "${IPV_PARAM}": "-4",
    "${DUT_ADMIN}": "admin",
    "${DUT_ADMIN_PASSWORD}": "ironport",
    "${DUT_ADMIN_SSW_PASSWORD}": "Cisco12$",
}


def get_variables():
    try:
        return BuiltIn().get_variables()
    except:
        return variables_dictionary


def set_variable(key, value):
    variables_dictionary[key] = value


def del_variable(key):
    del variables_dictionary[key]
