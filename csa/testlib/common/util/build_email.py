#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/build_email.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import sys
from common.util.utilcommon import UtilCommon, make_keyword

# MIME objects
from email.mime.base import MIMEBase
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.text import MIMEText

# Internationalized headers
from email.header import Header, decode_header

# encoders
from email.encoders import encode_quopri, \
    encode_base64, encode_noop, encode_7or8bit

# utils
from email.utils import quote, unquote, parseaddr, parsedate, \
    parsedate_tz, decode_params, decode_rfc2231, encode_rfc2231, \
    formataddr, formatdate, getaddresses, mktime_tz, make_msgid

# iterators
from email.iterators import body_line_iterator, \
    typed_subpart_iterator, _structure


class EmailMessageBuilder(UtilCommon):
    """
    This module provides keywords to work with email messages.
    - Create email and MIME objects from scratch;
    - Use internationalized headers;
    - Work with character sets;
    - Use encoders;
    - Use miscellaneous email utilities.

    Please refer to python docs to get more information on methods used here:\n
    http://docs.python.org/library/email

    Character sets\n
    http://www.iana.org/assignments/character-sets
    """

    @make_keyword
    def message_builder_create_mimebase(self, maintype, subtype, params={}):
        """
        Create MIMEBase object.

        *Parameters*:
        - `maintype`: The _Content-Type_ major type.
        - `subtype`: The _Content-Type_ minor type.
        - `params`: A parameter key=value dictionary and is passed directly to `Message Add Header`.

        *Examples*:
        | ${pp}= | Create Dictionary |
        | param1 | value1 |
        | param2 | value2 |
        | ${mime_base}= | Message Builder Create MIMEBase |
        | ... | text |
        | ... | html |
        | ... | params=${pp} |

        *Return*:
        MIMEBase object.
        """
        return MIMEBase(maintype, subtype, **params)

    @make_keyword
    def message_builder_create_mimemultipart(self,
                                             subtype='mixed',
                                             boundary=None,
                                             subparts=None,
                                             params={}):
        """
        Create MIMEMultipart object.

        *Parameters*:
        - `subtype`: The _Content-Type_ minor type. Defaults to _mixed_.
        - `boundary`: The multipart boundary string.
        When None (the default), the boundary is calculated when needed.
        - `subparts`: A sequence of initial subparts for the payload. List.
        You can always attach new subparts to the message by using the `Message Attach` method.
        - `params`: Additional parameters for the Content-Type header are taken from the keyword arguments,
        or passed here as a keyword dictionary.

        *Examples*:
        | ${parts}= | Create List | ${text1} | ${image1} |
        | ${mime_multi}= | Message Builder Create MIMEMultipart | subparts=${parts} |

        *Return*:
        MIMEMultipart object.
        """
        return MIMEMultipart(_subtype=subtype,
                             boundary=boundary,
                             _subparts=subparts,
                             **params)

    @make_keyword
    def message_builder_create_mimeapplication(self,
                                               data,
                                               subtype='octet-stream',
                                               encoder=encode_base64,
                                               params={}):
        """
        Create MIMEApplication object.

        *Parameters*:
        - `data`: A string containing the raw byte data.
        Optional _subtype specifies the MIME subtype and defaults to octet-stream.
        - `subtype`: The _Content-Type_ minor type.
        - `encoder`: A callable (i.e. function) which will perform the actual encoding of the data for transport.
        This callable takes one argument, which is the MIMEApplication instance.
        The default encoding is base64.
        - `params`: Dictionary of parameters.

        *Examples*:
        | ${data} | Get Binary File | /path/to/some/file/or/data/ |
        | ${mime_app}= | Message Builder Create MIMEApplication | ${data} |

        *Return*:
        MIMEApplication object.
        """
        return MIMEApplication(data,
                               _subtype=subtype,
                               _encoder=encoder,
                               **params)

    @make_keyword
    def message_builder_create_mimenonmultipart(self, maintype, subtype, params={}):
        """
        Create MIMENonMultipart object.

        *Parameters*:
        - `maintype`: The _Content-Type_ major type.
        - `subtype`: The _Content-Type_ minor type.
        - `params`: A parameter key=value dictionary.

        *Examples*:
        | ${mime_non}= | Message Builder Create MIMENonMultipart |
         text | plain |

        *Return*:
        MIMENonMultipart object.
        """
        return MIMENonMultipart(maintype, subtype, **params)

    @make_keyword
    def message_builder_create_mimeaudio(self,
                                         audiodata,
                                         subtype=None,
                                         encoder=encode_base64,
                                         params={}):
        """
        Create MIMEAudio object.

        *Parameters*:
        - `audiodata`: A string containing the raw audio data.
        - `subtype`: Specify the audio subtype in the _Content-Type_ header.
        - `encoder`: A callable (i.e. function) which will perform the actual encoding of the audio data for transport.
        This callable takes one argument, which is the MIMEAudio instance.
        The default encoding is base64.
        - `params`: A parameter key=value dictionary.

        *Examples*:
        | ${vv}= | Get Binary File | /path/to/some/file |
        | ${mime_audio}= | Message Builder Create MIMEAudio | ${vv} | subtype=mpeg3 |

        *Return*:
        MIMEAudio object.
        """
        return MIMEAudio(audiodata,
                         _subtype=subtype,
                         _encoder=encoder,
                         **params)

    @make_keyword
    def message_builder_create_mimeimage(self,
                                         imagedata,
                                         subtype=None,
                                         encoder=encode_base64,
                                         params={}):
        """
        Create MIMEImage object.

        *Parameters*:
        - `imagedata`: A string containing the raw image data.
        - `subtype`: Specify the image subtype, the _Content-Type_ minor type.
        - `encoder`: A callable (i.e. function) which will perform the actual encoding of the image data for transport.
        This callable takes one argument, which is the MIMEImage instance.
        The default encoding is base64.
        - `params`: A parameter key=value dictionary.

        *Examples*:
        | ${file}= | OperatingSystem.Get Binary File | /path/to/image/file/ironport_favicon.ico
        | ${image}= | Message Builder Create MIMEImage |
        | ... | ${file} |
        | ... | subtype=x-icon |
        | Message Builder Add Headers | ${image} | Content-ID=<image1> |

        *Return*:
        MIMEImage object.
        """
        return MIMEImage(imagedata,
                         _subtype=subtype,
                         _encoder=encoder,
                         **params)

    @make_keyword
    def message_builder_create_mimemessage(self, msg, subtype='rfc822'):
        """
        Create MIMEMessage object.

        *Parameters*:
        - `msg`: Must be an instance of class Message.
        - `subtype`: Sets the subtype of the message.

        *Examples*:
        | Message Builder Create MIMEMessage | ${msg1} |

        *Return*:
        MIMEMessage object.
        """
        return MIMEMessage(msg, _subtype=subtype)

    @make_keyword
    def message_builder_create_mimetext(self,
                                        text,
                                        subtype='plain',
                                        charset='us-ascii'):
        """
        Create MIMEText object.

        *Parameters*:
        - `text`: The string for the payload.
        - `subtype`: The minor type and defaults to _plain_.
        - `charset`: The character set of the text.

        *Examples*:
        | ${text}= | Message Builder Create MIMEText | some text goes here |

        *Return*:
        MIMEText object.
        """
        return MIMEText(text,
                        _subtype=subtype,
                        _charset=charset)

    def _parse_args(self, args):
        result = {}
        for arg in args:
            equal_sign_index = arg.index('=')
            key, value = (arg[:equal_sign_index], arg[equal_sign_index + 1:])
            if value.lower() in ('true', 'false', 'none'):
                value = eval(value.capitalize())
            result[key] = value
        return result

    @make_keyword
    def message_builder_add_headers(self, msg, *args):
        """
        Add headers to MIME object.

        *Parameters*:
        - `msg`: Object to add headers to.
        - `kwargs`: Header filed, name=value pairs.

        *Examples*:
        | Message Builder Add Headers | ${main_message} |
        | ... | From=${from} |
        | ... | To=${to} |
        | ... | Cc=${cc} |
        | ... | Subject=${subj} |
        | ... | Date=${date} |
        """
        kwargs = self._parse_args(args)
        for k, v in kwargs.iteritems():
            msg[k] = v

    @make_keyword
    def message_builder_create_mime_header(self,
                                           initial_value=None,
                                           charset=None,
                                           maxlinelen=None,
                                           header_name=None,
                                           continuation_ws=' ',
                                           errors='strict'):
        """
        Create a MIME-compliant header that can contain strings in different character sets.

        *Parameters*:
        - `initial_value`: The initial header value. Defaults to None (the initial header value is not set).
        May be a byte string or a Unicode string.
        - `charset`: Has the same meaning as the charset argument to the `Email Builder Append To Mime Header` keyword.
        It also sets the default character set for all subsequent `Email Builder Append To Mime Header` keyword calls
        that omit the charset argument. If charset is not provided (the default),
        the us-ascii character set is used both as `initial_value` initial charset and
        as the default for subsequent `Email Builder Append To Mime Header` calls.
        - `maxlinelen`: The maximum line length. For splitting the first line to a shorter value
        (to account for the field header which isn't included in `initial_value`, e.g. Subject)
        pass in the name of the field in `header_name`.
        The default `maxlinelen` is 76, and the default value for `header_name` is None,
        meaning it is not taken into account for the first line of a long, split header.
        - `header_name`: Name of the header field.
        - `continuation_ws`: The RFC 2822-compliant folding whitespace.
        Defaults to a single space character (" ").
        Is usually either a space or a hard tab character.
        This character will be prepended to continuation lines.
        - `errors`: Passed through to any unicode() or ustr.encode() call. Defaults to "strict".

        *Examples*:
        | ${cc}= | Message Builder Create Mime Header | initial_value=me@mail.qa | header_name=Cc |

        *Return*:
        Instance of email.header.Header class.
        """
        header = Header(s=initial_value,
                        charset=charset,
                        maxlinelen=maxlinelen,
                        header_name=header_name,
                        continuation_ws=continuation_ws,
                        errors=errors)
        return header

    @make_keyword
    def message_builder_append_to_mime_header(self,
                                              header,
                                              value,
                                              charset=None,
                                              errors='strict'):
        """
        Append the string to the MIME header.

        *Parameters*:
        - `header`: Instance of email.header.Header class.
        Value returned by `Email Builder Create Mime Header` keyword.
        - `value`: The value to append to the MIME header. Mandatory. May be a byte string or a Unicode string.
        - `charset`: If given, should be a Charset instance (see email.charset) or the name of a character set,
        which will be converted to a Charset instance.
        A value of None (the default) means that the charset given in the constructor is used.
        - `errors`: Passed through to any unicode() or ustr.encode() call. Defaults to "strict".

        *Examples*:
        | ${cc}= | Message Builder Create Mime Header |
        | Message Builder Append To Mime Header | ${cc} | others@mail.${NETWORK} |
        """
        header.append(value, charset=charset, errors=errors)

    @make_keyword
    def message_builder_encode_mime_header(self, header, splitchars=';, '):
        """
        Encode a message header into an RFC-compliant format, possibly wrapping long lines and encapsulating
        non-ASCII parts in base64 or quoted-printable encodings.

        *Parameters*:
        - `header`: The header to encode.
        - `splitchars`: String containing characters to split long ASCII lines on,
        in rough support of RFC 2822's highest level syntactic breaks.
        This doesn't affect RFC 2047 encoded lines.

        *Return*
        Encoded message header

        *Examples:*
        | ${subj}= | Message Builder Create Mime Header |
        | ... | initial_value=${subject} |
        | ... | charset=${charset} |
        | ... | header_name=Subject |
        | ${subj}= | Message Builder Encode Mime Header | ${subj} |
        | Message Builder Add Headers | ${msg} |
        | ... | From=${me} |
        | ... | To=${you} |
        | ... | Subject=${subj} |
        """
        return header.encode(splitchars=splitchars)

    @make_keyword
    def message_builder_decode_mime_header(self, header):
        """
        Decode a message header value without converting the character set.

        *Parameters*:
        - `header`: Header to decode.

        *Examples*:
        | Message Builder Decode Mime Header | ${cc} |

        *Return*:
        List of (decoded_string, charset) pairs containing each of the decoded parts of the header.
        """
        return decode_header(header)

    @make_keyword
    def message_builder_encode_quopri(self, msg):
        """
        Encodes the payload into quoted-printable form and sets
        the Content-Transfer-Encoding header to quoted-printable.

        *Parameters*:
        - `msg`: The message object.

        *Examples*:
        | Message Builder Encode Quopri | ${msg1} |
        """
        encode_quopri(msg)

    @make_keyword
    def message_builder_encode_base64(self, msg):
        """
        Encodes the payload into base64 form and sets the Content-Transfer-Encoding header to base64.

        *Parameters*:
        - `msg`: The message object.

        *Examples*:
        | ${mime_base}= | Message Builder Create MIMEBase | text | html |
        | Message Load | ${mime_base} |
        | Message Set Payload | <b>Some html text in the attachment.</b> |
        | Message Builder Encode Base64 | ${mime_base} |
        """
        encode_base64(msg)

    @make_keyword
    def message_builder_encode_7or8bit(self, msg):
        """
        This doesn't actually modify the message's payload,
        but it does set the Content-Transfer-Encoding header to
        either 7bit or 8bit as appropriate, based on the payload data.

        *Parameters*:
        - `msg`: The message object.

        *Examples*:
        | Message Builder Encode 7or8bit | ${msg1} |
        """
        encode_7or8bit(msg)

    @make_keyword
    def message_builder_encode_noop(self, msg):
        """
        This does nothing; it doesn't even set the Content-Transfer-Encoding header.

        *Parameters*:
        - `msg`: The message object.

        *Examples*:
        | Message Builder Encode Noop | ${msg1} |
        """
        encode_noop(msg)

    @make_keyword
    def message_builder_utils_quote(self, str):
        """
        Prepare string to be used in a quoted string.

        *Parameters*:
        - `str`: String.

        *Examples*:
        | Message Builder Utils Quote | "Some String" |

        *Return*:
        String with backslashes in str replaced by two backslashes,
        and double quotes replaced by backslash-double quote.
        """
        return quote(str)

    @make_keyword
    def message_builder_utils_unquote(self, str):
        """
        Remove quotes from a string.

        *Parameters*:
        - `str`: String.

        *Examples*:
        | Message Builder Utils Unquote | "Some String" |

        *Return*:
        String which is an unquoted version of str.
        If str ends and begins with double quotes, they are stripped off.
        Likewise if str ends and begins with angle brackets, they are stripped off.
        """
        return unquote(str)

    @make_keyword
    def message_builder_utils_parseaddr(self, address):
        """
        Parse address - which should be the value of some
        address-containing field such as To or Cc -
        into its constituent realname and email address parts.

        *Parameters:*
        - `address`: Address to parse.

        *Examples*:
        |${name} | ${addr}= | Message Builder Utils Parseaddr | Andriyko <sarfqa@mail.qa> |

        *Return*:
        Tuple. If parse fails - a 2-tuple of ('', '') is returned.
        """
        return parseaddr(address)

    @make_keyword
    def message_builder_utils_formataddr(self, pair):
        """
        The inverse of `Message Builder Utils Parseaddr`.

        *Parameters*:
        - `pair`: A 2-tuple of the form (realname, message_address) or string of comma-separated values.

        *Examples*:
        | ${from}= | Message Builder Utils Formataddr | SARF QA, me@mail.qa |

        *Return*:
        String value suitable for a To or Cc header.
        If the first element of pair is false, then the second element is returned unmodified.
        """
        return formataddr(self._convert_to_tuple(pair))

    @make_keyword
    def message_builder_utils_getaddresses(self, fieldvalues):
        """
        Returns a list of 2-tuples of the form returned by `Message Builder Utils Parseaddr`.

        *Parameters*:
        - `fieldvalues`: A sequence of header field values as might be returned by `Message Get ALL`.

        *Examples*:
        | Message Builder Utils Getaddresses | ${cc} |

        *Return*:
        List of 2-tuples.
        """
        return getaddresses(fieldvalues)

    @make_keyword
    def message_builder_utils_parsedate(self, var_date):
        """
        Attempts to parse a date according to the rules in RFC 2822.

        *Parameters*:
        - `date`: A string containing an RFC 2822 date, such as "Mon, 20 Nov 1995 19:12:08 -0500".

        *Examples*:
        | Message Builder Utils Parsedate | ${date_str} |

        *Return*:
        A 9-tuple that can be passed directly to time.mktime().
        If fails - None will be returned.
        Indexes 6, 7, and 8 of the result tuple are not usable.
        """
        return parsedate(var_date)

    @make_keyword
    def message_builder_utils_parsedate_tz(self, var_date):
        """
        Performs the same function as `Message Builder Utils Parsedate`.

        *Parameters:*
        - `date`: A string containing an RFC 2822 date, such as "Mon, 20 Nov 1995 19:12:08 -0500".

        *Examples*:
        | Message Builder Utils Parsedate TZ | ${date_str} |

        *Return*:
        Either None or a 10-tuple;
        The first 9 elements make up a tuple that can be passed directly to time.mktime(),
        and the tenth is the offset of the date's timezone from UTC (which is the official
        term for Greenwich Mean Time).
        Indexes 6, 7, and 8 of the result tuple are not usable.
        """
        return parsedate_tz(var_date)

    @make_keyword
    def message_builder_utils_mktime_tz(self, var_tuple):
        """
        Turn a 10-tuple as returned by `Message Builder Utils Parsedate Tz` into a UTC timestamp.

        *Parameters:*
        - `var_tuple`: A 10-tuple as returned by `Message Builder Utils Parsedate Tz`.

        *Examples*:
        | ${my_date} | Message Builder Utils Parsedate TZ | ${date_str} |
        | Message Builder Utils Mktime TZ | ${my_date} |

        *Return*:
        String.
        """
        return mktime_tz(var_tuple)

    @make_keyword
    def message_builder_utils_formatdate(self,
                                         timeval=None,
                                         localtime=False,
                                         usegmt=False):
        """
        Build a date string.

        *Parameters*:

        - `timeval`: If given is a floating point time value as accepted by time.gmtime() and time.localtime(),
        otherwise the current time is used.
        - `localtime`: A flag that when True, interprets timeval, and returns a date relative
        to the local timezone instead of UTC, properly taking daylight savings time into account.
        The default is False meaning UTC is used.
        - `usegmt`: A flag that when True, outputs a date string with the timezone as an ascii string GMT,
        rather than a numeric -0000. This is needed for some protocols (such as HTTP).
        This only applies when localtime is False. The default is False.

        *Examples*:
        | ${date}= | Message Builder Utils Formatdate | localtime=${True} |

        *Return*:
        Returns a date string as per RFC 2822, e.g.:
        Fri, 09 Nov 2001 01:08:47 -0000
        """
        return formatdate(timeval=timeval,
                          localtime=localtime,
                          usegmt=usegmt)

    @make_keyword
    def message_builder_utils_make_msgid(self, idstring=None):
        """
        Returns a string suitable for an RFC 2822-compliant Message-ID header.

        *Parameters*:
        - `idstring`: If given, is a string used to strengthen the uniqueness of the message id.

        *Examples*:
        | ${msg_id}= | Message Builder Utils Make Msgid |

        *Return*:
        A string suitable for an RFC 2822-compliant Message-ID header.
        """
        return make_msgid(idstring=idstring)

    @make_keyword
    def message_builder_utils_decode_rfc2231(self, s):
        """
        Decode the string s according to RFC 2231.

        *Parameters*:
        - `s`: String to decode.

        *Examples*:
        | ${str}= | Message Builder Utils Decode Rfc2231 | ${some_value} |

        *Return*:
        String.
        """
        return decode_rfc2231(s)

    @make_keyword
    def message_builder_utils_encode_rfc2231(self,
                                             s,
                                             charset=None,
                                             language=None):
        """
        Encode the string s according to RFC 2231.

        *Parameters*:
        - `s`: String to encode.
        - `charset`: The character set name to use. Defaults to None.
        - `language`: The language name to use. Defaults to None.

        *Examples*:
        | ${str}= | Message Builder Utils encode Rfc2231 | ${some_value} | charset=UTF-8 |

        *Return*:
        If neither of args is given, s is returned as-is.
        If charset is given but language is not,
        the string is encoded using the empty string for language.
        """
        return encode_rfc2231(s, charset=charset, language=language)

    @make_keyword
    def message_builder_utils_decode_params(self, params):
        """
        Decode parameters list according to RFC 2231.

        *Parameters*:
        - `params`: A sequence of 2-tuples containing elements of the form (content-type, string-value).

        *Examples*:
        | ${new_params} | Message Builder Utils Decode Params | ${params} |

        *Return*:
        New parameters in a sequence of 2-tuples.
        """
        return decode_params(params)

    @make_keyword
    def message_builder_iterators_body_line_iterator(self, msg, decode=False):
        """
        This iterates over all the payloads in all the subparts of msg, returning the string payloads line-by-line.
        Suitable for debugging purpose.

        *Parameters*:
        - `msg`: Message object.
        - `decode`: decode is passed through to `Message Get Payload`.

        *Examples*:
        | ${iterator}= | Mesage Builder Iterators Body Line Iterator | ${msg_obj} | decode=${True} |
        | ${pp}= | Convert To List | ${iterator} |

        *Return*:
        Iterator.
        """
        return body_line_iterator(msg, decode=decode)

    @make_keyword
    def message_builder_iterators_typed_subpart_iterator(self,
                                                         msg,
                                                         maintype='text',
                                                         subtype=None):
        """
        This iterates over all the subparts of msg, returning only those subparts that match the
        MIME type specified by maintype and subtype.

        *Parameters:*
        - `msg`: Message object.
        - `maintype`: The main MIME type to match against. Default to 'text'.
        - `subtype`: The MIME subtype to match against; if omitted, only the main type is matched.

        *Examples*:
        | ${iter}= | Mesage Builder Iterators Typed Subpart Iterator | ${msg_obj} |
        | ${parts}= | Convert To List | ${iter} |

        *Return*:
        Iterator. Returning only those subparts that match the MIME type specified by maintype and subtype.
        """
        return typed_subpart_iterator(msg,
                                      maintype=maintype,
                                      subtype=subtype)

    @make_keyword
    def message_builder_iterators_structure(self,
                                            msg,
                                            fp=None,
                                            level=0,
                                            include_default=False):
        """
        The following keyword has been added as a useful debugging tool.
        Prints an indented representation of the content types of the message object structure.

        *Parameters:*
        - `msg`: Message object.

        *Examples*:
        | ${iterator}= | Mesage Builder Iterators Structure | ${msg_obj} | decode=${True} |

        *Return*:
        String.
        """
        return _structure(msg,
                          fp=fp,
                          level=level,
                          include_default=include_default)

    def get_keyword_names(self):
        return sys.modules[self.__class__.__module__].__keywords__
