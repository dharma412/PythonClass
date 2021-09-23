#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/TestLibrary.py#2 $
# $DateTime: 2019/06/11 06:52:26 $
# $Author: revlaksh $

import sys
import os
import re
import traceback

# in-house imports
import common.Variables
from common.util.misc import Misc


class TestLibrary():
    """ Base Test Library class """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def _parse_robot_vars(self, dut=None, dut_version=None, dut_prefix='DUT'):
        # get name of TestLibrary
        testlib = str(self.__class__)
        testlib = testlib[testlib.rfind('.') + 1:]

        # library variables
        try:
            self.robot_vars = common.Variables.get_variables()
        except:
            # no robot variables can be retrieved
            # all parameters should be specified explicitly
            if dut is None or dut_version is None:
                raise Exception("dut and dut_version arguments to " \
                                "%s are required as soon as they can not " \
                                "be retrieved from Robot Framework variables" %
                                (testlib,))

        # if dut is not set explicitly, take it from variable
        self.dut = str(dut or self.robot_vars['${%s}' % (dut_prefix,)])
        if dut_version:
            self.dut_version = dut_version
        else:
            # find a corresponding LIB_VERSION
            self.dut_version = Misc(None, None).get_library_name(self.dut)
            if int(self.robot_vars['${DUT_LIB_FLAG}']):
                self.dut_version = self.robot_vars['${DUT_LIB_VERSION}']
        self.dut_browser = self.robot_vars['${DUT_BROWSER}']
        print "self.dut_browser ", self.dut_browser

    def get_test_libraries(self, search_paths=None):
        libs = []
        if search_paths is not None:
            for search_path in search_paths:
                self.append_entries(search_path, libs)
        return libs

    # return a dictionary where keys are keyword's names
    # and values are instantiated objects of test libraries that implement the
    # keyword.
    # parameters will be passed to TestLibrary's __init__
    def get_keywords(self, test_libs, *args, **kwargs):
        # dictionary keyword:library object
        # initially contain global keywords
        keywords = {}

        # fill keywords dictionary
        for lib in test_libs:
            module_name = lib[:lib.rfind('.')]
            class_name = lib[lib.rfind('.') + 1:]
            last_module = module_name[module_name.rfind('.') + 1:]
            duplicated_keyword = False
            try:
                lib_module = __import__(module_name, globals(),
                                        locals(), [last_module], -1)
                print "lib_module, ", lib_module, class_name, args, kwargs
                lib_obj = getattr(lib_module, class_name)(*args, **kwargs)
                for keyword in lib_obj.get_keyword_names():
                    if keywords.has_key(keyword):
                        duplicated_keyword = True
                        raise Exception(
                            "Duplicated keyword: %s\n" \
                            "First occurence: %s\n" \
                            "Second occurence: %s\n" % \
                            (keyword, keywords[keyword].__class__,
                             lib_obj.__class__))
                    else:
                        keywords[keyword] = lib_obj
            except:
                if duplicated_keyword:
                    raise
                print "Error while processing test library:", module_name
                traceback.print_exc()
        return keywords

    # Robot Framework Hybrid Library API methods
    def get_keyword_names(self):
        return self.keywords.keys()

    def __getattr__(self, name):
        if self.keywords.has_key(name):
            return getattr(self.keywords[name], name)

    def append_entries(self, root, list=None):
        """
        Detect robot modules in the specified directory
          and append them to the specified list
        The criteria for detection are the following:
            file is located in root folder or its subfolders
            file name starts with a letter
            file name ends with ".py"
            file has a class with method get_keyword_names

        """
        # prepare initial list
        if list is None:
            list = []

        # get testlib location
        testlib = ''
        for path in sys.path:
            if path.endswith('testlib'):
                testlib = path
                break
        if not testlib:
            raise Exception('testlib can not be found in sys.path')

        # remove trailing slash
        if root.endswith("/"):
            root = root[:-1]

        # root module and root path for entries
        root_module = root.replace('/', '.')
        root = os.path.join(testlib, root)
        nodes = [root]
        # check if root directory exists
        if (not os.path.exists(root)):
            return list
        print "\nAppend_entries", "root=", root, "before:", list.__len__(),
        if (os.path.isdir(root) == False):
            raise Exception("root should be a folder")
        while nodes.__len__() > 0:
            node = nodes[0]
            if (os.path.isfile(node) == True):
                in_file = open(node, "r")
                _class = None

                for line_raw in in_file:
                    m = re.match(" *class +([^ :\(]*)", line_raw)
                    if m:
                        _class = str(node[(root.__len__() + 1):-3]) \
                                     .replace("/", ".") + "." + m.group(1)
                    m = re.match(" *def.*get_keyword_names.*", line_raw)
                    if m:
                        if not _class == None:
                            _class = root_module + '.' + _class
                            if not list.__contains__(_class):
                                list.append(_class)
                            _class = None
                in_file.close
            else:
                if (os.path.isdir(node) == True):
                    dir_list = os.listdir(node)
                    for entry in dir_list:
                        entry_full = '/'.join([node, entry])
                        if os.path.isdir(entry_full) or entry.endswith(".py"):
                            nodes.append(entry_full)
            nodes.pop(0)
        if len(list) != 0:
            for lib in list:
                print lib
            print
        return list
