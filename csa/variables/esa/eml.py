#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/variables/esa/eml.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import datetime
from mbox_eml_mixins import gather_files

__all__ = ['eml',]

doc_string =\
"""
Access .eml files in \'testdata\' directory.
Attributes are filenames in upper case without extension.

So, this module recursively gets all files with *.eml* extension.

*The attributes are created in this way*
1. Get filename without extension.
2. Make [1] upper case.
3. Set [2] as class attribute.
4. Set full file path as value of [2].

*Examples:*

* _eml.LOCK_ARCHIVE_ refers to '/home/ahrytski/work/sarf/tests/testdata/esa/contentscanning/rar/lock_archive.eml'

*How to use*:

1. Add line below to _Settings_ section:

Variables       esa/eml.py

2. In _Test Case_ it can be used as:

Inject Message  ${eml.LOCK_ARCHIVE}

The list of allowed values is generated automatically.

The real values may differ from given here.

This document was last updated: _%s_

*Allowed values are*:

""" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

class eml(): pass

for fname, fpath in gather_files('*.eml').iteritems():
    setattr(eml, fname, fpath)
    value = '- `%s.%s`: %s\n' % (eml.__name__, fname, fpath)
    doc_string += value

setattr(eml, '__doc__', doc_string)