#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/monitor/quarantines/qexceptions.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

class NoSuchQuarantine(ValueError): pass


class QuarantineIsAlreadyEnabled(ValueError): pass


class QuarantineIsNotEnabled(ValueError): pass


class NoMessagesFound(ValueError): pass


class MessageNotFound(ValueError): pass


class NoSuchMidInQuarantine(ValueError): pass


class SLBLIsAlreadyEnabled(ValueError): pass


class SLBLIsNotEnabled(ValueError): pass


class NoSuchRuleId(ValueError): pass


class NoMessagesInQuarantine(ValueError): pass


class QuarantinesAcceesDenied(ValueError): pass
