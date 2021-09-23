#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/parse_email.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import sys
from common.util.utilcommon import make_keyword, UtilCommon
from email.message import Message
from cStringIO import StringIO
from email.generator import Generator
import warnings


class MessageNotLoaded(RuntimeError): pass


class MessageAlreadyLoaded(RuntimeWarning): pass


class EmailMessageWrapper(UtilCommon):
    """
    Class for representing an email message.\n

    Singleton that uses shared state approach.\n
    It can work only with single instance of 'email.message.Message' class ('Message' object) at a time.\n
    For this, you should first load message into context, then do needed stuff, and then unload message.\n
    Then you can proceed with other messages in the same way.\n
    For example:\n
    _Message Load  ${msg}_\n
    _${as_string}=  Message As String_\n
    _Message Unload_\n

    This class wraps 'email.message.Message' class.\n
    Please refer to python docs to get more information on methods used here:\n
    http://docs.python.org/library/email.message.html

    Character sets\n
    http://www.iana.org/assignments/character-sets
    """
    __shared_state = {}

    def __init__(self, dut, dut_version):
        UtilCommon.__init__(self, dut, dut_version)
        self.__dict__ = self.__shared_state

    _has_msg = lambda self: hasattr(self, 'msg')

    def _is_message_loaded(self):
        """
        Method to check if message has been loaded.
        It would be better to have this as a decorator.
        But it is too complicated to use decorator that
        works with *args, **kwargs with RF.
        We have args parser for base classes through ArgumentParser.
        But it is overkill to use it here, as it is 1 line code anyway.
        """
        if not self._has_msg():
            raise MessageNotLoaded \
                ('Message is not loaded. Please load message first.')

    @make_keyword
    def message_is_loaded(self):
        """
        Check if message has been loaded into current context.

        *Examples*:
        | ${message_is_loaded}= | Message Is Loaded |
        | Should Be True | ${message_is_loaded} |

        *Return*:
        Boolean.
        """
        return self._has_msg()

    @make_keyword
    def message_load(self, msg):
        """
        Load message into current context.

        *Parameters*:
        - `msg`: Instance of 'email.message.Message' type.

        *Examples*:
        | ${drain}= | Null Smtpd Start |
        | Inject Message | ${mbox.UTF8_TEXT_ATT} |
        | ${msg}= | Null Smtpd Next Message | timeout=60 |
        | Message Load | ${msg} |

        *Exceptions*:
        - `MessageAlreadyLoaded`: Invoked if message is already loaded. This warning that does not inerrupt code execution.
        - `ValueError`: If `msg` is None.
        """
        if self._has_msg():
            warnings.warn("There is message loaded. Unloading old message.", MessageAlreadyLoaded)
            del self.msg
        if msg is None:
            raise ValueError('Message cannot be None')
        self.msg = msg

    @make_keyword
    def message_unload(self):
        """
        Unload message from current context.

        *Examples*:
        | Message Unload |
        """
        if self._has_msg():
            del self.msg

    @make_keyword
    def message_as_string(self, unixfrom=False):
        """
        Return the entire message flattened as a string.

        This keyword may not always format the message the way you want.
        For example, by default it mangles lines that begin with From.
        Please try to use `Message As Flatten String` in such case.

        *Parameters*:
        - `unixform`: When optional unixfrom is True, the envelope header
        is included in the returned string.
        unixfrom defaults to False.

        *Return*:
        String.

        *Examples*:
        | ${as_str}= | Message As String |
        | Log | ${as_str} |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.as_string(unixfrom)

    @make_keyword
    def message_as_flatten_string(self, mangle_from=False, maxheaderlen=60):
        """
        Represents message as string.

        *Parameters*:
        - `mangle_from`: When True, puts a > character in front of any line
        in the body that starts exactly as _From_,
        i.e. From followed by a space at the beginning of the line.
        - `maxheaderlen`: Specifies the longest length for a non-continued header.
        Optional. Default is 60.

        *Return*:
        String.

        *Examples*:
        | ${as_flatten_str}= | Message As Flatten String |
        | ... | mangle_from=${True} |
        | ... | maxheaderlen=1000 |
        | Log | ${as_flatten_str} |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        fp = StringIO()
        g = Generator(fp, mangle_from_=mangle_from, maxheaderlen=int(maxheaderlen))
        g.flatten(self.msg)
        return fp.getvalue()

    @make_keyword
    def message_is_multipart(self):
        """
        Return True if the message's payload is a list of sub-Message objects,
        otherwise return False.

        When Message is not multipart the payload should be a string object.

        *Parameters*:
        None

        *Return*:
        Boolean.

        *Examples*:
        | ${is_multipart}= | Message Is Multipart |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.is_multipart()

    @make_keyword
    def message_get_unixfrom(self):
        """
        Return the message's envelope header.
        Defaults to None if the envelope header was never set.

        *Return*:
        Message's envelope header if such exists, else None.

        *Examples*:
        | ${unixfrom}= | Message Get Unixfrom |
        | Log | ${unixfrom} |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_unixfrom()

    @make_keyword
    def message_get_payload(self, payload_index=None, decode=False):
        """
        Return the current payload, which will be a list of Message objects
        when Message is multipart, or a string when Message is not multipart.

        *Parameters*:
        - `payload_index`: Return the i-th element of the payload, counting from zero,
        if Message is multipart. Optional.
        - `decode`: Flag indicating whether the payload should be decoded or not,
        according to the Content-Transfer-Encoding header.
        Default is False.
        When True and the message is not a multipart, the payload will be decoded
        if this header's value is quoted-printable or base64.
        If some other encoding is used, or Content-Transfer-Encoding header is missing,
        or if the payload has bogus base64 data, the payload is returned as-is (undecoded).
        If the message is a multipart and the decode flag is True, then None is returned.
        If the payload is a list and you mutate the list object, you modify
        the message's payload in place.

        *Return*:
        List or String.

        *Examples*:
        | @{payload}= | Message Get Payload |
        | Log List | ${payload} |
        | Message Unload |
        | :FOR | ${p} | IN | @{payload} |
        | \ | Log | Now each payload is a Message object. Load it. |
        | \ | Message Load | ${p} |
        | \ | Message Keys |
        | \ | Message As String |
        | \ | ${headers}= | Message Items |
        | \ | Log Dictionary | ${headers} |
        | \ | Message Unload |

        *Exceptions*:
        - `IndexError`: if _payload_index_ is less than 0 or greater than
        or equal to the number of items in the payload.
        - `TypeError`: if the payload is a string (Message is not multipart)
        and _payload_index_ is given.
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        if payload_index is not None:
            payload_index = int(payload_index)
        return self.msg.get_payload(i=payload_index, decode=decode)

    @make_keyword
    def message_get_charset(self):
        """
        Return the Charset instance associated with the message's payload.

        Please refer to docs:
        http://docs.python.org/library/email.charset.html#email.charset.Charset

        *Examples*:
        | ${charset}= | Message Get Charset |
        | Log | ${charset} |

        *Return*:
        The Charset instance.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_charset()

    @make_keyword
    def message_has_key(self, name):
        """
        Check if message contains a header field named name.

        *Parameters*:
        - `name`: Header name.

        *Examples*:
        | Message Has Key | From |

        *Return*:
        Boolean. Return True if the message contains a header field named name,
        otherwise return False.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.has_key(name)

    @make_keyword
    def message_keys(self):
        """
        Return a list of all the message's header field names.

        *Examples*:
        | @{headers_k}= | Message Keys |
        | Log List | ${headers_k} |

        *Return*:
        List.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.keys()

    @make_keyword
    def message_values(self):
        """
        Return a list of all the message's field values.

        *Examples*:
        | @{headers_v}= | Message Values |
        | Log List | ${headers_v} |

        *Return*:
        List.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.values()

    @make_keyword
    def message_items(self):
        """
        Return a dictionary containing all the message's field headers and values.

        *Examples*:
        | ${headers}= | Message Items |
        | Log Dictionary | ${headers} |

        *Return*:
        Dictionary.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return dict(self.msg.items())

    @make_keyword
    def message_get(self, name, failobj=None):
        """
        Return the value of the named header field.

        *Parameters*:
        - `name`: The header to get.
        - `failobj`: Returned if the named header is missing (defaults to None).

        *Examples*:
        | ${subj}= | Message Get | Subject |

        *Return*:
        String.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get(name, failobj=failobj)

    @make_keyword
    def message_get_all(self, name, failobj=None):
        """
        Return a list of all the values for the field named name.
        If there are no such named headers in the message, failobj is returned.

        *Parameters*:
        - `name`: The header to get.
        - `failobj`: Returned if the named header is missing (defaults to None).

        *Examples*:
        | @{rcvd}= | Message Get All | Received |
        | Log List | ${rcvd} |

        *Return*:
        List.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_all(name, failobj=failobj)

    @make_keyword
    def message_get_content_type(self):
        """
        Return the message's content type.
        The returned string is coerced to lower case of the form maintype/subtype.
        If there was no Content-Type header in the message the default type
        as given by get_default_type() will be returned.

        *Examples*:
        | ${content_type}= | Message Get Content Type |

        *Return*:
        String.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_content_type()

    @make_keyword
    def message_get_content_maintype(self):
        """
        Return the message's main content type.
        This is the maintype part of the string returned by `Message Get Content Type`.

        *Examples*:
        | ${content_main_type}= | Message Get Content Maintype |

        *Return*:
        String.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_content_maintype()

    @make_keyword
    def message_get_content_subtype(self):
        """
        Return the message's sub-content type.
        This is the subtype part of the string returned by `Message Get Content Type`.

        *Examples*:
        | ${content_subtype}= | Message Get Content Subtype |

        *Return*:
        String.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_content_subtype()

    @make_keyword
    def message_get_default_type(self):
        """
        Return the default content type.

        *Examples*:
        | ${def_type}= | Message Get Default Type |

        *Return*:
        String.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_default_type()

    @make_keyword
    def message_get_params(self,
                           failobj=None,
                           header='Content-Type',
                           unquote=True):
        """
        Return the message's Content-Type parameters, as a dictionary.

        The elements of the returned list are key/value pairs, as split on the '=' sign.
        The left hand side of the '=' is the key, while the right hand side is the value.
        If there is no '=' sign in the parameter the value is the empty string,
        otherwise the value is as described in `Message Get Param` and is
        unquoted if optional unquote is True (the default).

        *Examples*:
        | ${params}= | Message Get Params |
        | Log Dictionary | ${params} |

        *Parameters*:
        - `failobj`: Optional failobj is the object to return if there is
        no Content-Type header(or _header_ passed as argument).
        Defaults to None.
        - `header`: Optional header is the header to search instead of Content-Type.
        - `unquote`: Unquote header. Boolean. True by default.

        *Return*:
        Dictionary.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return dict(self.msg.get_params(failobj=failobj, header=header, unquote=unquote))

    @make_keyword
    def message_get_param(self,
                          param,
                          failobj=None,
                          header='Content-Type',
                          unquote=True):
        """
        Return the value of the Content-Type header's parameter param as a string.

        Parameter keys are always compared case insensitively.

        *Parameters*:
        - `param`: The parameter to get from the _Content-Type_ header or
        other header given as argument.
        - `failobj`: If the message has no _Content-Type_ header or if
        there is no such parameter, then failobj is returned (defaults to None).
        - `header`: Optional header if given, specifies the message header to
        use instead of Content-Type.
        - `unquote`: Unquote header. Boolean. True by default.

        *Examples*:
        | ${param}= | Message Get Param | ${arg} |

        *Return*:
        The return value can either be a string, or a 3-tuple if the parameter
        was RFC 2231 encoded. When it's a 3-tuple, the elements of the value are
        of the form (CHARSET, LANGUAGE, VALUE).
        Note that both CHARSET and LANGUAGE can be None, in which case you should consider
        VALUE to be encoded in the us-ascii charset.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_param(param, failobj=failobj, header=header, unquote=unquote)

    @make_keyword
    def message_get_filename(self, failobj=None):
        """
        Return the value of the filename parameter of the
        Content-Disposition header of the message.
        If the header does not have a filename parameter,
        this method falls back to looking for the name parameter
        on the Content-Type header.

        If neither is found, or the header is missing, then failobj is returned.
        The returned string will always be unquoted.

        Parameter keys are always compared case insensitively.

        *Parameters*:
        - `failobj`: If the message has no _Content-Disposition_
        and _Content-Type_ header, then failobj is returned (defaults to None).

        *Examples*:
        | ${fname}= | Message Get Filename |

        *Return*:
        String.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_filename(failobj=failobj)

    @make_keyword
    def message_get_boundary(self, failobj=None):
        """
        Return the value of the boundary parameter of the Content-Type header of the message,
        or failobj if either the header is missing, or has no boundary parameter.
        The returned string will always be unquoted.

        *Parameters*:
        - `failobj`: If either the header is missing, or has no boundary parameter.
        Defaults to None.

        *Examples*:
        | ${boundary}= | Message Get Boundary |

        *Return*:
        String.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_boundary(failobj=failobj)

    @make_keyword
    def message_get_content_charset(self, failobj=None):
        """
        Return the charset parameter of the Content-Type header, coerced to lower case.
        Note that this keyword differs from `Message Get Charset`
        which returns the Charset instance for the default encoding of the message body.

        *Parameters*:
        - `failobj`: If there is no Content-Type header, or if that header
        has no charset parameter, failobj is returned.
        Defaults to None.

        *Examples*:
        | Message Get Content Charset |

        *Return*:
        String.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_content_charset(failobj=failobj)

    @make_keyword
    def message_get_charsets(self, failobj=None):
        """
        Return a list containing the character set names in the message.
        If the message is a multipart, then the list will contain one element
        for each subpart in the payload, otherwise, it will be a list of length 1.
        Each item in the list will be a string which is the value of the
        charset parameter in the Content-Type header for the represented subpart.

        *Parameters*:
        - `failobj`: If the subpart has no Content-Type header,
        no charset parameter, or is not of the text main MIME type,
        then that item in the returned list will be failobj.
        Defaults to None.

        *Examples*:
        | @{charsets}= | Message Get Charsets |

        *Return*:
        List.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.get_charsets(failobj=failobj)

    @make_keyword
    def message_get_preamble(self):
        """
        Returns the preamble attribute that contains leading
        extra-armor text for MIME documents.

        *Examples*:
        | ${preamble}= | Message Get Preamble |

        *Return*:
        String. Or None - if the message object has no preamble,
        the preamble attribute will be None .

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.preamble

    @make_keyword
    def message_set_preamble(self, s):
        """
        Returns the preamble attribute that contains leading
        extra-armor text for MIME documents.

        *Parameters*:
        - `s`: String to set as a preamble.

        *Examples*:
        | Message Set Preamble | lets start |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.preamble = s

    @make_keyword
    def message_get_epilogue(self):
        """
        Returns the epilogue attribute.

        *Examples*:
        | ${epilogue}= | Message get Epilogue |

        *Return*:
        String.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.epilogue

    @make_keyword
    def message_set_epilogue(self, s):
        """
        Returns the epilogue attribute.

        *Examples*:
        | Message Set Epilogue | the end |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.epilogue = s

    @make_keyword
    def message_defects(self):
        """
        Returns the defects attribute that contains a list of all the problems
        found when parsing this message.

        *Examples*:
        | @{defects}= | Message Defects |

        *Return*:
        List.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.defects

    @make_keyword
    def message_walk(self):
        """
        This keyword is an all-purpose generator which can be used to iterate over all
        the parts and subparts of a message object tree, in depth-first traversal order.

        You will typically use this keyword as the iterator in a FOR loop,
        each iteration returns the next subpart.

        *Examples*:
        | ${generator}= | Message Walk |
        | @{parts}= | Convert To List | ${generator} |
        | Message Unload |
        | :FOR | ${part} | IN | @{parts} |
        | \ | Message Load | ${part} |
        | \ | ${ct}= | Message Get Content Type |
        | \ | Message Unload |
        | \ | Log  ${ct} |

        *Return*:
        Generator object.

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        return self.msg.walk()

    @make_keyword
    def message_set_unixfrom(self, unixfrom):
        """
        Set the message's envelope header to unixfrom, which should be a string.

        *Parameters*:
        - `unixfrom`: Unix _From_ line.

        *Examples*:
        | ${date}= | Message Builder Utils Formatdate | localtime=${True} |
        | Message Set Unixfrom | From me@${CLIENT} ${date} |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.set_unixfrom(unixfrom)

    @make_keyword
    def message_attach(self, payload):
        """
        Add the given payload to the current payload, which must be None or a list of Message objects before the call.
        After the call, the payload will always be a list of Message objects.

        *Parameters*:
        - `payload`: The payload to add.

        *Examples*:
        | ${alternative_message}= | Message Builder Create MIMEMultipart | subtype=alternative |
        | Message Attach | ${alternative_message} |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.attach(payload)

    @make_keyword
    def message_set_payload(self, payload, charset=None):
        """
        Set the entire message object's payload to payload.

        Optional charset

        *Parameters*:
        - `payload`: The payload to set.
        - `charset`: Sets the message's default character set; see `Message Set Charset` for details.

        *Examples*:
        | Message Set Payload | ${raw_byte_data_as_payload} |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.set_payload(payload, charset=charset)

    @make_keyword
    def message_set_charset(self, charset):
        """
        Set the character set of the payload to charset.

        *Parameters*:
        - `charset`: Can either be a Charset instance (see email.charset), a string naming a character set, or None.
        If it is a string, it will be converted to a Charset instance.
        If charset is None, the charset parameter will be removed from the Content-Type header
        (the message will not be otherwise modified). Anything else will generate a TypeError.

        *Examples*:
        | Message Set Charset | utf-8 |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.set_charset(charset)

    @make_keyword
    def message_add_header(self, name, value, *args):
        """
        Extended header setting.

        *Parameters*:
        - `name`: The header field to add.
        - `value`: The primary value for the header.
        If the value contains non-ASCII characters, it must be specified as a three tuple in the format
        (CHARSET, LANGUAGE, VALUE), where CHARSET is a string naming the charset to be used to encode the value,
        LANGUAGE can usually be set to None or the empty string (see RFC 2231 for other possibilities),
        and VALUE is the string value containing non-ASCII code points.
        - `params`: Parameters of the header to add.

        *Examples*:
        | Message Add Header | Subject | This is subject |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        params = self._parse_args(args)
        self.msg.add_header(name, value, **params)

    @make_keyword
    def message_replace_header(self, name, value):
        """
        Replace a header.

        Replace the first header found in the message that matches `name`,
        retaining header order and field name case.

        *Parameters*:
        - `name`: The name of the header.
        - `value`: The value to set.

        *Examples*:
        | Message replace Header | Subject | New subject |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        - `KeyError`: If no matching header was found.
        """
        self._is_message_loaded()
        self.msg.replace_header(name, value)

    @make_keyword
    def message_set_default_type(self, ctype):
        """
        Set the default content type.

        *Parameters*:
        - `ctype`: Either a text/plain or message/rfc822, although this is not enforced.
        The default content type is not stored in the Content-Type header.

        *Examples*:
        | Message Set Default Type | text/plain |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.set_default_type(ctype)

    @make_keyword
    def message_set_param(self,
                          param,
                          value,
                          header='Content-Type',
                          requote=True,
                          charset=None,
                          language=''):
        """
        Set a parameter in the Content-Type header.
        If the parameter already exists in the header, its value will be replaced with value.
        If the Content-Type header has not yet been defined for this message,
        it will be set to text/plain and the new parameter value will be appended as per RFC 2045.

        Optional

        *Parameters*:
        - `header`: Specifies an alternative header to Content-Type.
        - `requote`: Defines whether all parameters should be quoted as necessary. (Default is True).
        - `charset`: If specified, the parameter will be encoded according to RFC 2231. String.
        - `language`: Specifies the RFC 2231 language, defaulting to the empty string.

        *Examples*:
        | Message Set Param | boundary | some==boundary=== |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.set_param(param,
                           value,
                           header=header,
                           requote=requote,
                           charset=charset,
                           language=language)

    @make_keyword
    def message_del_param(self, param, header='content-type', requote=True):
        """
        Remove the given parameter completely from the Content-Type header.


        The header will be re-written in place without the parameter or its value.
        All values will be quoted as necessary unless requote is False (the default is True).
        Optional header specifies an alternative to Content-Type.

        *Parameters*:
        - `param`: The parameter to remove.
        - `header`: Target header to remove parameter from. Optional. Defaults to 'content-type'.
        - `requote`: If True - all values will be quoted as necessary. (The default is True).

        *Examples*:
        | Message Del Param | boundary |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.del_param(param, header=header, requote=requote)

    @make_keyword
    def message_set_type(self, _type, header='Content-Type', requote=True):
        """
        Set the main type and subtype for the header(Content-Type by default).

        *Parameters*:
        - `_type`: String in the form maintype/subtype, otherwise a ValueError is raised.
        This method replaces the Content-Type header, keeping all the parameters in place.
        - `requote`: If is False, this leaves the existing header's quoting as is,
        otherwise the parameters will be quoted (the default).
        - `header`: An alternative header to use instead of 'Content-Type'.

        *Examples*:
        | Message Set Type | multipart/alternative |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        self.msg.set_type(_type, header=header, requote=requote)

    @make_keyword
    def message_set_boundary(self, boundary):
        """
        Set the boundary parameter of the Content-Type header to boundary.

        Will always quote boundary if necessary.

        *Parameters*:
        - `boundary`: The boundary to set.

        *Examples*:
        | Message Set Boundary | 123456 |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        - `HeaderParseError`: If the message object has no Content-Type header.
        """
        self._is_message_loaded()
        self.msg.set_boundary(boundary)

    @make_keyword
    def message_delete_item(self, name):
        """
        Delete all occurrences of the field with name _name_ from the message's headers.
        No exception is raised if the named field isn't present in the headers.

        *Parameters*:
        - `name`: The name of the field to delete from headers.

        *Examples*:
        | Message Delete Item | Received |

        *Exceptions*:
        - `MessageNotLoaded`: If Message is not loaded.
        """
        self._is_message_loaded()
        del self.msg[name]

    def get_keyword_names(self):
        return sys.modules[self.__class__.__module__].__keywords__
