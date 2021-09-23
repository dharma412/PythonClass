#!/usr/bin/env python

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
