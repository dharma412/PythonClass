#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/monitor/quarantines/qexceptions.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

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
