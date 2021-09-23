#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/monitor/quarantines/qexceptions.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

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
