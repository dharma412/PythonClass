#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/util/pdf_parser.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import os

from common.util.utilcommon import UtilCommon

from sal.containers.pdf import PDFFile


class PDFParser(UtilCommon):
    """Keywords for generic PDF files parsing
    based on https://github.com/euske/pdfminer library.
    """

    def get_keyword_names(self):
        return ['pdf_parser_get_text',
                'pdf_parser_get_pages_count']

    def pdf_parser_get_text(self, path, pages=None, password='', codec='utf-8'):
        """Extract text from existing PDF file

        *Parameters:*
        - `path`: full path to existing PDF file
        - `pages`: page numbers to extract texts from. Can be comma separated string
        or list of page numbers. All document pages will be taken by default.
        Page numbering starts from zero.
        - `password`: PDF document password. Leave it empty for no password
        - `codec`: PDF charset encoding. 'utf-8' by default

        *Return:*
        - Unicode string containing requested PDF text

        *Exceptions:*
        - `ValueError`: if any of given parameters is not correct.

        *Examples:*
        | {text}= | PDF Parser Get Text | ${PDF_PATH} | 0,1 | codec=big5 |
        | Log | ${text} |
        | Should Contain | ${text} | ${PDF_TEXT_PART} |
        """
        if not os.path.exists(path):
            raise ValueError('The file {0} does not exist'.format(path))
        if pages is None:
            page_numbers = set()
        elif isinstance(pages, basestring):
            page_numbers = set(map(lambda x: int(x.strip()), pages.split(',')))
        elif isinstance(pages, (list, tuple)):
            page_numbers = set(map(int, pages))
        else:
            raise ValueError('"pagenos" value should be either comma separated ' \
                             'string or list of page numbers. "{0}" value is ' \
                             'given instead.'.format(pages))
        pdf_file = PDFFile(path, password)
        return pdf_file.get_text(page_numbers, codec)

    def pdf_parser_get_pages_count(self, path, password=''):
        """Get pages count in existing PDF file

        *Parameters:*
        - `path`: full path to existing PDF file
        - `password`: PDF document password. Leave it empty for no password

        *Exceptions:*
        - `ValueError`: if given path does not exist

        *Return:*
        - Number of pages in PDF document

        *Examples:*
        | ${pages_count}= | PDF Parser Get Pages Count | ${PDF_PATH} |
        | Should Be True | ${pages_count} > 0 |
        """
        if not os.path.exists(path):
            raise ValueError('The file {0} does not exist'.format(path))
        pdf_file = PDFFile(path, password)
        return pdf_file.get_pages_count()
