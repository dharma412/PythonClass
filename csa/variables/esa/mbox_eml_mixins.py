#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/variables/esa/mbox_eml_mixins.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import os
import fnmatch

testdata_path = os.path.join(os.getenv('SARF_HOME'), 'tests/testdata')

def gather_files(search_mask):
    gathered_files = {}
    for root, dirs, files in os.walk(testdata_path):
        for _file in files:
            if fnmatch.fnmatch(_file, search_mask):
                fpath = os.path.join(root, _file)
                fname = os.path.splitext(os.path.basename(fpath))[0].upper()
                if fname not in gathered_files.keys():
                    gathered_files[fname] = fpath
    return gathered_files