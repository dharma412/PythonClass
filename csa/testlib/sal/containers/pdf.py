#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/containers/pdf.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from StringIO import StringIO

# PDFMiner lib is required for this module: pip install pdfminer
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager

# As of now commented loading process_pdf & PDFDocument need to fix as per latest library
# from pdfminer.pdfinterp import PDFResourceManager, process_pdf
# from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfparser import PDFParser


class PDFFile(object):
    def __init__(self, path, password=''):
        self._path = path
        self._password = password

    @property
    def path(self):
        return self._path

    @property
    def password(self):
        return self._password

    def get_text(self, page_numbers=set(), codec='utf-8'):
        maxpages = 0
        rsrcmgr = PDFResourceManager()
        result_fp = StringIO()
        try:
            device = TextConverter(rsrcmgr,
                                   result_fp,
                                   codec=codec,
                                   laparams=LAParams())
            with open(self._path, 'rb') as pdf_file:
                process_pdf(rsrcmgr,
                            device,
                            pdf_file,
                            page_numbers,
                            maxpages=maxpages,
                            password=self._password,
                            check_extractable=True)
            pdf_text = result_fp.getvalue().decode(codec)
            return pdf_text
        finally:
            device.close()
            result_fp.close()

    def get_pages_count(self):
        doc = PDFDocument()
        with open(self._path, 'rb') as fp:
            parser = PDFParser(fp)
            try:
                parser.set_document(doc)
                doc.set_parser(parser)
                doc.initialize(self._password)
                return len(list(doc.get_pages()))
            finally:
                parser.close()


if __name__ == '__main__':
    import os

    SARF_HOME = os.getenv('SARF_HOME')
    CODEC = 'big5'
    pdf_file = PDFFile(os.path.join(SARF_HOME,
                                    'tests/testdata/esa/contentscanning/pdf/chinese/chinese_text_1.pdf'))
    print 'Path to current PDF file: {0}'.format(pdf_file.path)
    print u'Full text of current PDF file:\n{0}\n\n'.format(
        pdf_file.get_text(codec=CODEC))
    pagenos = range(2)
    print u'Text of pages 0 to 2:\n{0}\n\n'.format(
        pdf_file.get_text(set(pagenos), codec=CODEC))
    print 'Total pages count: {0}'.format(pdf_file.get_pages_count())
