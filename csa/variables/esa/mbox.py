#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/variables/esa/mbox.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import datetime
from mbox_eml_mixins import gather_files

__all__ = ['mbox',]
doc_string = \
"""
Access mbox files in \'testdata\' directory.
Attributes are filenames in upper case without extension.

So, this module recursively gets all files with *.mbox* extension.

*The attributes are created in this way*
1. Get filename without extension.
2. Make [1] upper case.
3. Set [2] as class attribute.
4. Set full file path as value of [2].

*Examples:*

* _mbox.CLEAN_ refers to '/home/ahrytski/work/sarf/tests/testdata/esa/antispam/clean.mbox'
* _mbox.UTF8_TEXT_ATT_ refers to '/home/ahrytski/work/sarf/tests/testdata/esa/contentscanning/utf8_text_att.mbox'

*How to use*:

1. Add line below to _Settings_ section:

Variables       esa/mbox.py

2. In _Test Case_ it can be used as:

Log  ${mbox.CLEAN}

Inject Message  ${mbox.SPAM}

The list of allowed values is generated automatically.

The real values may differ from given here.

This document was last updated: _%s_

*Allowed values are*:

""" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

class mbox(): pass

for fname, fpath in gather_files('*.mbox').iteritems():
    setattr(mbox, fname, fpath)
    value = '- `%s.%s`: %s\n' % (mbox.__name__, fname, fpath)
    doc_string += value

setattr(mbox, '__doc__', doc_string)