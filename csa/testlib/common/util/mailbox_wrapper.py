#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/mailbox_wrapper.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import atexit
import mailbox
import sys
import os
from common.util.utilcommon import make_keyword


class MailboxNotLoaded(RuntimeError): pass


class MailboxAlreadyLoaded(RuntimeError): pass


class MailboxMboxWrapper(object):
    """
    Class for representing a _mailbox.mbox_ files.\n

    Singleton that uses shared state approach.\n
    It can work only with single instance of _mailbox.mbox_ class at a time.\n
    For this, you should first load mailbox into context, then do needed stuff, and then unload mailbox.\n
    Then you can proceed with other messages in the same way.\n

    This class wraps 'mailbox.mbox' class.\n
    Please refer to python docs to get more information on methods used here:\n
    http://docs.python.org/library/mailbox.html

    Character sets\n
    http://www.iana.org/assignments/character-sets
    """
    LOCKED_PATHS = set()
    __shared_state = {}

    def __init__(self, *args, **kwargs):
        self.__dict__ = self.__shared_state

    _has_mbx = lambda self: hasattr(self, 'mbx')

    def _verify_if_mailbox_is_loaded(self):
        """
        Method to check if mailbox has been loaded.
        """
        if not self._has_mbx():
            raise MailboxNotLoaded \
                ('Mailbox is not loaded. Please load mailbox first.')

    def _is_mailbox_locked(self):
        """
        Method to check if mailbox is locked.
        """
        return self.mbx._locked

    @make_keyword
    def mailbox_is_loaded(self):
        """
        Check if mailbox has been loaded into current context.

        *Examples*:
        | ${mbx_is_loaded}= | Mailbox Is Loaded |
        | Should Be True | ${mbx_is_loaded} |

        *Return*:
        Boolean.
        """
        return self._has_mbx()

    @make_keyword
    def mailbox_is_locked(self):
        """
        Check if mailbox is locked.

        *Examples*:
        | ${is_locked}= | Mailbox Is Locked |
        | Should Be True | ${is_locked} |

        *Return*:
        Boolean.
        """
        self._verify_if_mailbox_is_loaded()
        return self._is_mailbox_locked()

    @make_keyword
    def mailbox_load(self, path, factory=None, create=True):
        """
        Load mailbox into current context(open/or add new) - creates instance of 'mailbox.mbox' class.

        *Parameters*:
        - `path`: Full path to the mbox (including its name).
        - `factory`: A callable object that accepts a file-like message representation
        (which behaves as if opened in binary mode) and returns a custom representation(eg _mailbox.MaildirMessage_).
        If factory is None, _mailbox.mboxMessage_ is used as the default message representation.
        - `create`: If is True, the mailbox is created if it does not exist.

        *Examples*:
        | Mailbox Load | /path/to/mbox/file.mbox |

        *Exceptions*:
        - `MailboxAlreadyLoaded`: If Mailbox is already loaded.
        """
        if self._has_mbx():
            raise MailboxAlreadyLoaded \
                ('Mailbox loaded already. Please unload mailbox first.')
        self.mbx = mailbox.mbox(path, factory=factory, create=create)
        self.LOCKED_PATHS.add('%s.lock' % self.mbx._file.name)

    @make_keyword
    def mailbox_unload(self):
        """
        Unload mailbox from current context.
        Does not matter was the mbox in the context or not.

        *Examples*:
        | Mailbox Unload |
        """
        if self._has_mbx():
            del self.mbx

    @make_keyword
    def mailbox_add_message(self, msg):
        """
        Add message to the mailbox and return the key that has been assigned to it.

        *Parameters*:
        - `msg`: May be a _mailbox.mboxMessage_ instance, an _email.message.Message_ instance, a string,
        or a file-like object (which should be open in text mode).
        If message is an instance of the appropriate format-specific Message subclass
        (e.g., if it's an mboxMessage instance and this is an mbox instance),
        its format-specific information is used.
        Otherwise, reasonable defaults for format-specific information are used.

        Please note that you should always lock the mailbox before making any modifications to its contents.
        Following of these rules is delegated to end-user. No extra-check is done inside this keyword.

        *Examples*:
        | Mailbox Add Message | ${msg1} |

        *Return*:
        Assigned key as String.

        *Exceptions*:
        - `MailboxNotLoaded`: If Mailbox is not loaded.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.add(msg)

    @make_keyword
    def mailbox_remove_message(self, key):
        """
        Delete the message corresponding to key from the mailbox.

        *Parameters*:
        - `key`: Remove element(message) from mbox by key.

        *Examples*:
        | Mailbox remove |

        *Return*:
        Return a file-like representation.

        *Exceptions*:
        - `KeyError`: If no such key exists.
        """
        self._verify_if_mailbox_is_loaded()
        self.mbx.remove(key)

    @make_keyword
    def mailbox_discard_message(self, key):
        """
        If the keyed message exists, remove it.
        Unlike `Mailbox Remove` this keyword does not raise 'KeyError' if key does not exists.

        *Parameters*:
        - `key`: Remove element(message) from mbox by key.

        *Examples*:
        | Mailbox Discard |
        """
        self._verify_if_mailbox_is_loaded()
        self.mbx.discard(key)

    @make_keyword
    def mailbox_setitem(self, key, message):
        """
        Replace the message corresponding to key with message.

        *Parameters*:
        - `key`: Get element(message) from mbox by key.
        - `message`: May be a Message instance, an _email.message.Message_ instance, a string, or a file-like object
        (which should be open in text mode). If message is an instance of the appropriate format-specific
        Message subclass (e.g., if it's an mboxMessage instance and this is an mbox instance),
        its format-specific information is used.
        Otherwise, the format-specific information of the message that currently corresponds to key is left unchanged.

        *Examples*:
        | Mailbox Setitem | 1 | ${some_msg_obj}

        *Exceptions*:
        - `KeyError`: If no message already corresponds to key.
        """
        self._verify_if_mailbox_is_loaded()
        self.mbx[key] = message

    @make_keyword
    def mailbox_keys(self):
        """
        Return a list of keys.

        *Examples*:
        | ${ks}= | Mailbox Keys |
        | Log List | ${ks} |

        *Return*:
        List.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.keys()

    @make_keyword
    def mailbox_values(self):
        """
        Return list of representations of all messages.

        *Examples*:
        | ${vs}= | Mailbox Values |
        | Log List | ${vs} |

        *Return*:
        List.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.values()

    @make_keyword
    def mailbox_items(self):
        """
        Return a dictionary of 'key=message' pairs, where key is a key and message is a message representation.

        *Examples*:
        | ${dd}= | Mailbox Items |
        | Log Dictionary | ${dd} |

        *Return*:
        Dictionary.
        """
        self._verify_if_mailbox_is_loaded()
        return dict(self.mbx.items())

    @make_keyword
    def mailbox_get(self, key, default=None):
        """
        Return a representation of the message corresponding to key.

        *Parameters*:
        - `key`: The key to get message for.
        - `default`: The value to return if no such key present. Defaults to None.

        *Examples*:
        | ${is_none}= | Mailbox Get | 100000 |
        | Should Be Equal As Strings | ${is_none} | ${None} |

        *Return*:
        Return the keyed message.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.get(key, default=default)

    @make_keyword
    def mailbox_get_message(self, key):
        """
        Return a representation of the message corresponding to key as an instance of the appropriate
        format-specific Message subclass, or raise a KeyError exception if no such message exists.

        *Parameters*:
        - `key`: The key to get.

        *Examples*:
        | ${msg} | Mailbox Get Message | 0 |
        | Message Load | ${msg} |

        *Return*:
        Return the keyed message.

        *Exceptions*:
        - `KeyError`: If no such message exists.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.get_message(key)

    @make_keyword
    def mailbox_get_string(self, key):
        """
        Return a string representation of the message corresponding to key,
        or raise a KeyError exception if no such message exists.

        *Parameters*:
        - `key`: The key to get.

        *Examples*:
        | ${msg_as_str} | Mailbox Get String | 0 |
        | Log | ${msg_as_str} |

        *Return*:
        Return the keyed message.

        *Exceptions*:
        - `KeyError`: If no such message exists.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.get_string(key)

    @make_keyword
    def mailbox_get_file(self, key):
        """
        Using the file after calling `Mailbox Flush` or `Mailbox Close` on the mbox instance
        may yield unpredictable results or raise an exception.

        *Parameters*:
        - `key`: Get element from mbox by key.

        *Examples*:
        | ${msg} | Mailbox Get File | 0 |
        | Log | ${msg} |

        *Return*:
        Return a file-like representation.

        *Exceptions*:
        - `KeyError`: If no such key assigned.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.get_file(key)

    @make_keyword
    def mailbox_has_key(self, key):
        """
        Check whether there is a key corresponding to message.

        *Parameters*:
        - `key`: Get element from mbox by key.

        *Examples*:
        | ${has_msg} | Mailbox Has Key | 12 |
        | Should Be True | ${has_msg} |

        *Return*:
        True if key corresponds to a message, False otherwise.

        *Exceptions*:
        - `KeyError`: If no such key assigned.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.has_key(key)

    @make_keyword
    def mailbox_count_messages(self):
        """
        Return a count of messages in the mailbox.

        *Examples*:
        | ${messages_count}= | Mailbox Count Messages |
        | Should Be Equal As Integers | ${messages_count} | 3 |

        *Return*:
        String.

        *Exceptions*:
        - `KeyError`: If no such key assigned.
        """
        self._verify_if_mailbox_is_loaded()
        return len(self.mbx)

    @make_keyword
    def mailbox_clear(self):
        """
        Delete all messages from the mailbox.

        *Examples*:
        | Mailbox Clear |

        *Exceptions*:
        - `KeyError`: If no such key assigned.
        """
        self._verify_if_mailbox_is_loaded()
        self.mbx.clear()

    @make_keyword
    def mailbox_pop(self, key, default=None):
        """
        Return a representation of the message corresponding to key and delete the message.

        *Parameters*:
        - `key`: The key to lookup by.
        - `default`: Value to return is there is keyed message. Defaults to None.

        *Examples*:
        | ${msg}= | Mailbox Pop | ${some_key} |
        | Message Load | ${msg} |

        *Return*:
        String or None.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.pop(key, default=default)

    @make_keyword
    def mailbox_pop_item(self):
        """
        Return an arbitrary (key, message) pair, where key is a key and message is a message representation,
        and delete the corresponding message.

        The message is represented as an instance of the appropriate format-specific Message subclass
        unless a custom message factory was specified when the Mailbox instance was initialized.

        *Examples*:
        | ${k} | ${v}= | Mailbox Pop Item |
        | Log | ${k} |
        | Message Load | ${v} |

        *Return*:
        Tuple (key, value).

        *Exceptions*:
        - `KeyError`: If the mailbox is empty.
        """
        self._verify_if_mailbox_is_loaded()
        return self.mbx.popitem()

    @make_keyword
    def mailbox_update(self, arg=None):
        """
        Updates the mailbox so that, for each given key and message, the message corresponding
        to key is set to message as if by using `Mailbox Setitem`.

        Each key must already correspond to a message in the mailbox or else a KeyError exception will be raised,
        so in general it is incorrect for arg to be a Mailbox instance.

        *Parameters*:
        - `arg`: A key-to-message mapping or an iterable of (key, message) pairs.

        *Examples*:
        | ${msg} | Mailbox Get Message | 1 |
        | ${dd} | Create List | 0 | ${msg} |
        | Mailbox Update | ${dd} |

        *Exceptions*:
        - `KeyError`: If the mailbox is empty.
        """
        self._verify_if_mailbox_is_loaded()
        self.mbx.update(arg=arg)

    @make_keyword
    def mailbox_flush(self):
        """
        Write any pending changes to the filesystem. For some Mailbox subclasses,
        changes are always written immediately and `Mailbox Flush` does nothing,
        but you should still make a habit of calling this method.

        *Examples*:
        | Mailbox Flush |
        """
        self._verify_if_mailbox_is_loaded()
        self.mbx.flush()

    @make_keyword
    def mailbox_lock(self):
        """
        Acquire an exclusive advisory lock on the mailbox so that other processes know not to modify it.

        You should always lock the mailbox before making any modifications to its contents.

        *Examples*:
        | Mailbox Lock |

        *Exceptions*:
        - `MailboxNotLoaded`: If Message is not loaded.
        - `ExternalClashError`: If the lock is not available.
        """
        self._verify_if_mailbox_is_loaded()
        self.mbx.lock()

    @make_keyword
    def mailbox_unlock(self):
        """
        Release the lock on the mailbox, if any.

        *Examples*:
        | Mailbox Unlock |

        *Exceptions*:
        - `MailboxNotLoaded`: If Mailbox is not loaded.
        """
        self._verify_if_mailbox_is_loaded()
        self.mbx.unlock()
        try:
            self.LOCKED_PATHS.remove('%s.lock' % self.mbx._file.name)
        except KeyError:
            pass

    @make_keyword
    def mailbox_close(self):
        """
        Flush the mailbox, unlock it if necessary, and close any open files.
        For some Mailbox subclasses, this method does nothing.

        *Examples*:
        | Mailbox Close |
        """
        self._verify_if_mailbox_is_loaded()
        self.mbx.close()

    def get_keyword_names(self):
        return sys.modules[self.__class__.__module__].__keywords__


@atexit.register
def clean_up_all_locked_files():
    for p in MailboxMboxWrapper.LOCKED_PATHS:
        if os.path.exists(p):
            try:
                os.unlink(p)
            except Exception as e:
                print e
