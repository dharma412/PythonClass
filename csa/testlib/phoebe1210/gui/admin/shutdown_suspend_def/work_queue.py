#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/admin/shutdown_suspend_def/work_queue.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner


class WorkQueueForm(InputsOwner):
    PROCESSING_STATUS = ('Work Queue Processing Status',
                         "//th[normalize-space()='Work Queue Processing Status:']/" \
                         "following-sibling::td")
    MESSAGES_IN_QUEUE = ('Messages in Work Queue',
                         "//th[normalize-space()='Messages in Work Queue:']/" \
                         "following-sibling::td")
    GENERATED_LABEL = ('Generated',
                       "//dt[normalize-space()='Work Queue Status']/" \
                       "following::table//td[@colspan='2']")

    @set_speed(0, 'gui')
    def get(self):
        result = self._get_texts(self.PROCESSING_STATUS,
                                 self.MESSAGES_IN_QUEUE)
        generated_value = self.gui.get_text(self.GENERATED_LABEL[1])
        result[self.GENERATED_LABEL[0]] = \
            generated_value[generated_value.find(':') + 1:].strip()
        return result
