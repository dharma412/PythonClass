#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/help/technical_support_def/contact_techsupport_output_analysis.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner

ELEMENTS_TABLE_HEADERS = "//table[@class='pairs']/tbody/tr/th"
ALL_HEADERS = ('Sent to', 'Contact Information', 'Technology',
               'Sub Technology', 'Issue Description',
               'Customer Support Case Number')

HEADER_BY_NAME = lambda name: "{0}[starts-with(normalize-space(),'{1}')]/following-sibling::td". \
    format(ELEMENTS_TABLE_HEADERS, name)
HEADERS_MAPPING = map(lambda x: (x, HEADER_BY_NAME(x)), ALL_HEADERS)


class TechnicalSupportOutputAnalysis(InputsOwner):

    @set_speed(0, 'gui')
    def get_element_text_fields(self):
        result = self._get_texts(*HEADERS_MAPPING)
        possible_problem_code_values = ('Problem code', 'Problem Code')
        for value in possible_problem_code_values:
            if self.gui._is_element_present(HEADER_BY_NAME(value)):
                result['Problem Code'] = self.gui.get_text(HEADER_BY_NAME(value))
                break
        return result
