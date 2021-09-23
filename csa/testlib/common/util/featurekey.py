#!/usr/local/bin/python

# FILE COPIED FROM: /usr/local/cvsroot/godspeed/hermes/feature_key.py 1.40 2004/12/31 03:34:18

# -*- mode: python -*-
# $Header: //prod/main/sarf_centos/testlib/common/util/featurekey.py#1 $


import binascii
import cgi
import os
import re
import string
import struct
import sys
import time
import types

_SHARED_SECRET = "xYzzY"
_SALT = "nAcL"

# repeat until it is at least 8 bytes long
_SALT *= 8 / len(_SALT) + 1

MAGIC = "fEtR"
B2A = binascii.b2a_base64
A2B = binascii.a2b_base64
VERSION = 2
CLEARTEXT = 0
SIGNED = 0
PADKEY = 0
SIGNATURE_LENGTH = 16

if SIGNED or not CLEARTEXT:
    import POW

    CYPHER = POW.DES_EDE3_CBC
    DIGEST = POW.MD5_DIGEST


class MalformedKey:
    pass


class NotSupportedKey(MalformedKey):
    pass


def _secret(hardware_address):
    digest = POW.Digest(DIGEST)
    digest.update(_normalize_hardware_address(hardware_address))
    shared_digest = POW.Digest(DIGEST)
    shared_digest.update(_SHARED_SECRET)
    return digest.digest() + shared_digest.digest()


def _no_nuls(str):
    return str.replace('\0', '\1')


def _normalize_hardware_address(hardware_address):
    return hardware_address.replace(":", "").lower()[:12]


def normalize_message(message):
    return message.replace("-", "").strip()


class PascalField:
    def format_from_value(self, v):
        return '%dp' % (len(v) + 1)

    def format_from_keystream(self, key):
        if len(key):
            return '%dp' % (ord(key[0]) + 1)
        else:
            return '1p'


# this table is used for marshalling and demarshalling each field of a key.
# behold the absence of two big switch..case blocks in the code ;-)
#
# field_name : ( 'abbreviation' : 'struct-format' )
# where abbreviation is optional if a field is mandatory
key_fields = {'noise': ('', 'H'),
              'magic': ('', '4s'),
              'version': ('', 'H'),
              'component': ('C', PascalField()),
              'duration': ('d', 'L'),
              'deadline': ('D', 'L'),
              'enter_by': ('e', 'L'),
              'enter_after': ('E', 'L'),  # clock rollback enforcement
              # 'start_time'       : ('s', 'L'),
              'quantity': ('q', 'l'),
              'baseline': ('b', 'L'),  # useful for imh, else avoid
              'baseline_additive': ('+', ''),  # add to model baseline
              'key_additive': ('#', ''),  # add to prior key
              'duration_additive': ('@', ''),  # add to prior dormant time
              'clear': ('-', ''),
              'next_key': (',', ''),
              }

# when decoding optional fields, we lookup the abbreviation
key_fields_inverted_index = {}
for k, v in key_fields.items():
    if len(v[0]) == 1:
        key_fields_inverted_index[v[0]] = k


def generate_single(hardware_address, noise=None, **kv):
    return generate(hardware_address, noise, kv)


def generate(hardware_address, noise, *key_set):
    """encode an encrypted feature-key-set"""
    if noise is None:
        noise = int(time.time()) & (2 ** 16 - 1)

    def encode_kv(k, v):
        (code, format) = key_fields[k]
        if type(format) is types.InstanceType:
            format = format.format_from_value
        if callable(format):
            format = format(v)
        if format == '':
            return code
        # print "<!-- key %r format %s value %r -->" % (k, format, v)
        return code + struct.pack("!" + format, v)

    key = encode_kv('noise', noise)
    key += encode_kv('magic', MAGIC)
    key += encode_kv('version', VERSION)

    first_time = 1
    for kv in key_set:
        if not first_time:
            key += encode_kv('next_key', None)
        first_time = 0
        for k in ('deadline', 'duration'):
            if kv.has_key(k) and kv[k] is None:
                kv[k] = 0
        if kv.has_key('enter_by') and kv['enter_by'] is None:
            kv['enter_by'] = kv.get('expiry', 0)
        for k in kv.keys():
            if key_fields.has_key(k) and k not in ('noise', 'magic', 'version'):
                key += encode_kv(k, kv[k])

    if SIGNED:
        secret = _secret(hardware_address)
        hasher = POW.Digest(DIGEST)
        hasher.update(key)
        hasher.update(secret)
        key += hasher.digest()

    if PADKEY and len(key) % PADKEY:
        # pad to multple of PADKEY characters
        key += '\0' * (PADKEY - (len(key) % PADKEY))

    if CLEARTEXT:
        message = key
    else:
        secret = _no_nuls(_secret(hardware_address))
        cypher = POW.Symmetric(CYPHER)
        cypher.encryptInit(secret, _SALT)
        message = cypher.update(key) + cypher.final()

    message2 = ""
    while message != "":
        message2 += B2A(message[:57]).strip()
        message = message[57:]
    message = message2

    return "-".join([message[x: x + 5] for x in xrange(0, len(message), 5)])


def decode(input, hardware_address):
    """decode and validate an encrypted feature-key"""
    try:
        if not input:
            raise MalformedKey

        message = A2B(normalize_message(input))

        if CLEARTEXT:
            key = message
        else:
            secret = _no_nuls(_secret(hardware_address))
            cypher = POW.Symmetric(CYPHER)
            cypher.decryptInit(secret, _SALT)
            try:
                key = cypher.update(message) + cypher.final()
            except POW.SSLError:
                raise MalformedKey

        whole_key = key

        def decode_kv(key, k=None):
            """parse the next key-value pair from key
            returns the remainder of the key, the field name, and value.
            optionally takes the field name for "forced fields", such as the header."""
            if len(key) == 0:
                return (None, None, None)
            if k is None and len(key) >= 1:
                (code, key) = (key[0], key[1:])
                if not key_fields_inverted_index.has_key(code):
                    raise NotSupportedKey
                k = key_fields_inverted_index[code]
            (code, format) = key_fields[k]
            if type(format) is types.InstanceType:
                format = format.format_from_keystream
            if callable(format):
                format = format(key)
            l = struct.calcsize(format)
            # print "key %r format %s l %d" % (key, format, l)
            if len(key) < l:
                raise MalformedKey
            v = (l > 0 and struct.unpack("!" + format, key[:l]) or (None,))[0]
            return (key[l:], k, v)

        (key, k, noise) = decode_kv(key, 'noise')
        (key, k, magic) = decode_kv(key, 'magic')
        (key, k, version) = decode_kv(key, 'version')

        if magic != MAGIC:
            raise MalformedKey
        if version > VERSION:
            raise NotSupportedKey

        kv = {}
        key_set = [kv]
        while key is not None:
            (key, k, v) = decode_kv(key)
            if k == "next_key":
                kv = {}
                key_set.append(kv)
                continue
            if k is not None:
                kv[k] = v

        for k in ('deadline', 'duration', 'enter_by'):
            if kv.has_key(k) and kv[k] == 0:
                kv[k] = None
        if kv.has_key('enter_by'):
            kv['expiry'] = kv['enter_by']

        if SIGNED:
            secret = _secret(hardware_address)
            hasher = POW.Digest(DIGEST)
            hasher.update(whole_key[:-len(SIGNATURE_LENGTH)])
            hasher.update(secret)
            if hasher.digest() != SIGNATURE_LENGTH:
                raise MalformedKey

        return key_set
    except binascii.Error:
        raise MalformedKey
    except TypeError:
        raise MalformedKey


##############
# data entry #
##############


class rejected_by_filter:
    pass


class choice_filter:
    def __init__(self, *choices):
        self.choices = choices

    def check(self, s):
        if s not in self.choices:
            raise rejected_by_filter
        return s


class null_filter:
    def __init__(self):
        pass

    def check(self, s):
        return s


class or_filter:
    def __init__(self, *filters):
        self.filters = filters

    def check(self, s):
        for f in self.filters:
            try:
                return f.check(s)
            except rejected_by_filter:
                pass
        raise rejected_by_filter


class timespan_filter:
    def check(self, t):
        r = re.compile(
            "^(\d+)$|^(\d+)\s*m(?:inutes?)?$|^(\d+)\s*h(?:ours?)?$|^(\d+)\s*d(?:ays?)?$|^(\d+)\s*w(?:eeks?)?$|^(\d+)\s*m(?:onths?)?$|^(\d+)\s*y(?:ears?)?$")
        m = r.match(str(t))
        if not m:
            raise rejected_by_filter
        none_or_multiply = lambda x, n: x and (int(x) * n) or None
        return (none_or_multiply(m.group(1), 1)
                or none_or_multiply(m.group(2), 60)
                or none_or_multiply(m.group(3), 3600)
                or none_or_multiply(m.group(4), 86400)
                or none_or_multiply(m.group(5), 7 * 86400)
                or none_or_multiply(m.group(6), 31 * 86400)
                or none_or_multiply(m.group(7), 366 * 86400))


class number_filter:
    def check(self, t):
        r = re.compile("^(\d+)$")
        m = r.match(str(t))
        if not m:
            raise rejected_by_filter
        return int(m.group(1))


class equals_filter:
    def __init__(self, e):
        self.e = e

    def check(self, v):
        if self.e != v:
            raise rejected_by_filter
        return v


class mac_address_filter:
    def check(self, mac):
        if not mac:
            raise rejected_by_filter
        mac = mac.lower()
        hex_colon = "([0-9a-f]{1,2}):"
        hex2 = "([0-9a-f]{2})"
        m = (re.match(hex_colon * 6 + "$", mac + ":")
             or re.match(hex2 * 6 + "$", mac))
        if not m:
            raise rejected_by_filter
        mac = ":".join([string.zfill(h, 2) for h in m.groups()])
        return mac


class messaging_gateway_serial_number_filter:
    def check(self, mac):
        if not mac:
            raise rejected_by_filter
        r = re.compile("^[0-9A-F]{12}-[0-9A-Z]{7}$")
        m = r.match(mac.upper())
        if not m:
            raise rejected_by_filter
        return m.group(0)


class prompt:
    def __init__(self, attr, label, default=None, description=None, filter=None):
        self.attr = attr
        self.label = label
        self.default = default
        self.description = description
        self.filter = filter or null_filter()
        self.value = None

    def read(self):
        while (1):
            try:
                if self.description:
                    print
                    if self.label:
                        print "===", self.label.upper()
                        print
                    print self.description
                    print
                print "[%s]> " % ((self.default or ""),),
                value = sys.stdin.readline()
                if value:
                    value = value.strip()
                value = self.filter.check(value or self.default)
                self.value = value
                break
            except rejected_by_filter:
                print "That input is invalid.  Try again."
                print

    def render_html_row(self):
        return (self.render_html_error_message()
                + """<TR><TD VALIGN=TOP>"""
                + self.render_html_label()
                + """</TD><TD VALIGN=TOP>"""
                + self.render_html_input()
                + """</TD></TR>""") % self.__dict__

    def render_html_label(self):
        return """%(label)s:<BR><SMALL>%(description)s</SMALL>""" % self.__dict__

    def render_html_input(self):
        # XXX ought to cgi.escape
        v = self.value
        if v is None:
            v = self.default or ""
        v = cgi.escape(str(v))
        self.html_safe_value = v
        return """<INPUT TYPE="TEXT" NAME="%(attr)s" VALUE="%(html_safe_value)s">""" % self.__dict__

    def render_html_error_message(self):
        if getattr(self, 'rejected_by_filter', 0):
            return """<TR><TD COLSPAN=2><FONT COLOR="#FF0000">Input unacceptable</FONT></TD></TR>"""
        else:
            return ""


class read_only_prompt(prompt):
    def __init__(self, attr, label, default=None, description=None, filter=None):
        prompt.__init__(self, attr, label, default, description, filter)
        self.value = self.default

    def read(self):
        if self.description:
            print
            if self.label:
                print "===", self.label.upper()
                print
            print self.description
            print
        print "[%s]> " % ((self.value or ""),)

    def render_html_input(self):
        v = self.value
        if v is None:
            v = self.default or ""
        v = cgi.escape(str(v))
        self.html_safe_value = v
        return v


class silent_prompt(read_only_prompt):
    # oxymoron
    def read(self):
        pass

    def render_html_row(self):
        return ""


class next_key_prompt(silent_prompt):
    def __init__(self):
        silent_prompt.__init__(self, "next_key", 'next key')

    def render_html_row(self):
        return "<TR><TD COLSPAN=2><HR></TD></TR>"


class prompts:
    def __init__(self):
        self.prompts = []
        self.prompts_by_attr = {}

    def add(self, p):
        self.prompts.append(p)
        self.prompts_by_attr[p.attr] = p

    def remove(self, p):
        self.prompts.remove(p)
        del self.prompts_by_attr[p.attr]

    def get(self, attr):
        return self.prompts_by_attr[attr]

    def get_value(self, attr):
        return self.get(attr).value

    def read(self):
        for p in self.prompts:
            p.read()

    def cleanup(self):
        pass

    def render_html(self):
        rows = [p.render_html_row() for p in self.prompts]
        return "".join(["""<TABLE>"""] + rows + ["""</TABLE>\n"""])

    def check_response(self, form):
        rejected = 0
        for p in self.prompts:
            if form.has_key(p.attr):
                v = form.getvalue(p.attr)
            else:
                v = p.default
            try:
                p.value = p.filter.check(v)
            except:
                p.rejected_by_filter = 1
                rejected = 1
        return not rejected


def hardware_address_prompt():
    return prompt('hardware_address', "Hardware Address",
                  None,
                  """What is the Serial Number or Hardware Address (MAC) address of the management
port of the box?""",
                  or_filter(messaging_gateway_serial_number_filter(),
                            mac_address_filter()))


def component_prompt():
    return prompt('component', "Component",
                  'imh',
                  """Which part of the IronPort Messaging Gateway Appliance(tm) is being evaluated?""",
                  choice_filter('imh', 'unsub'))


def duration_prompt(default=30):
    return prompt('duration', "Duration",
                  default * 86400,
                  """How long does that component operate, in seconds?
(default is %d days; enter "forever" if appropriate)""" % default,
                  or_filter(timespan_filter(), equals_filter("forever"), equals_filter("clear")))


def deadline_prompt(default=None):
    return prompt('deadline', "Deadline",
                  default,
                  """When does that component expire, in seconds?
(default is %r; enter "forever" if appropriate)""" % default,
                  or_filter(timespan_filter(), equals_filter("forever")))


def quantity_prompt(default=256):
    return prompt('quantity', "Quantity",
                  default,
                  """How many items does this key grant?
(default is %d; enter "undefined" if appropriate)""" % default,
                  or_filter(number_filter(), equals_filter("undefined")))


def silent_quantity_prompt(default=1):
    return silent_prompt('quantity', 'Quantity',
                         default,
                         """Unseen""",
                         number_filter())


def enter_by_prompt(default=90, factory=prompt):
    return factory('enter_by', "Enter By",
                   default * 86400,
                   """How long until this key cannot be entered into the CLI?
 (default is %d days from now; enter "forever" if appropriate)""" % default,
                   or_filter(timespan_filter(), equals_filter("forever")))


def enter_after_prompt(default=2, factory=prompt):
    return factory('enter_after', "Enter After",
                   default * 86400,
                   """How ago before this key can be entered into the CLI?
 (default is %d days ago; enter "forever" if appropriate)""" % default,
                   or_filter(timespan_filter(), equals_filter("forever")))


class key_tool:
    def __init__(self):
        self.prompts = self.get_prompts()

    def get_prompts():
        ### override me
        return None

    def get_title():
        ### override me
        return ""

    def report_header(self):
        out = []
        for prompt in self.prompts.prompts:
            if isinstance(prompt, next_key_prompt):
                continue
            note = ""
            if prompt.attr is 'enter_by':
                note = " (within %d days)" % int((prompt.value - time.time() + 1) / 86400)
            elif prompt.attr is 'enter_after':
                note = " (earlier than %d days ago)" % int((time.time() - prompt.value) / 86400)
            out.append("%-20s: %s%s\n" % (prompt.label, prompt.value, note))
        out.append("==== cut here ====\n")
        return "".join(out)

    def report_key_generate(self):
        hw = self.prompts.get_value('hardware_address')
        kv = {}
        kv_list = [kv]
        for prompt in self.prompts.prompts:
            if isinstance(prompt, next_key_prompt):
                kv = {}
                kv_list.append(kv)
                continue
            kv[prompt.attr] = prompt.value
        return apply(generate, [hw, None] + kv_list)

    def report_footer(self):
        return "\n==== cut here ====\n"

    def report(self):
        print self.report_header()
        print self.report_key_generate()
        print self.report_footer()

    def is_cgi(self):
        return sys.argv[0].endswith(".cgi")

    def http_form_input(self):
        self.form = cgi.FieldStorage(keep_blank_values=1)

    def is_form_submit(self):
        submit = 0
        for prompt in self.prompts.prompts:
            submit |= self.form.has_key(prompt.attr)
        return submit

    def is_satisfactory(self):
        return self.is_form_submit() and self.prompts.check_response(self.form)

    def render_http_header(self):
        print "Content-Type: text/html"
        print

    def render_html_start(self):
        print """<HTML>"""
        print """<HEAD><TITLE>%s</TITLE></HEAD>""" % self.get_title()
        print """<BODY>"""

    def render_html_end(self):
        print """</BODY>"""
        print """</HTML>"""

    def render_html_input_form(self):
        print """<FORM>"""
        print self.prompts.render_html()
        print """<INPUT TYPE="SUBMIT" VALUE="Generate Key">"""
        print """</FORM>"""

    def render_html_error(self):
        print """<FONT COLOR="#FF0000">An input error occurred.</FONT><P>"""

    def render_html_pre_report(self):
        print """<PRE>"""

    def render_html_post_report(self):
        print """</PRE>"""

    def run_web(self):
        self.http_form_input()
        self.render_http_header()
        self.render_html_start()

        if self.is_satisfactory():
            self.prompts.cleanup()
            self.render_html_pre_report()
            self.report()
            self.render_html_post_report()
        else:
            if self.is_form_submit():
                self.render_html_error()
            self.render_html_input_form()

        self.render_html_end()

    def run(self):
        if self.is_cgi():
            self.run_web()
        else:
            self.prompts.read()
            print
            self.prompts.cleanup()
            self.report()


class Unspecified:
    pass


def generic_evaluation(component_name, quantity=Unspecified, duration=30, quantity_visible=Unspecified):
    hardware_address = hardware_address_prompt()
    component = silent_prompt("component", "Component", component_name)
    duration = duration_prompt(duration)
    duration_additive = silent_prompt("duration_additive", "Duration Additive", "Yes")
    enter_by = enter_by_prompt(90, read_only_prompt)
    enter_after = enter_after_prompt(2, read_only_prompt)
    p = prompts()
    p.add(component)
    p.add(hardware_address)
    p.add(duration)
    p.add(duration_additive)
    p.add(enter_by)
    p.add(enter_after)
    if quantity_visible is Unspecified:
        # prompt for a quantity if it is explicitly specified
        quantity_visible = (quantity is not Unspecified)
    if quantity is Unspecified:
        quantity = 1
    if quantity is not None:
        if quantity_visible:
            quantity = quantity_prompt(quantity)
        else:
            quantity = silent_quantity_prompt(quantity)
        p.add(quantity)

    def cleanup(duration=duration, duration_additive=duration_additive, enter_by=enter_by, enter_after=enter_after,
                quantity=quantity, p=p):
        if duration.value == "clear":
            # undocumented and apparently unused
            p.remove(duration)
            p.remove(duration_additive)
            p.remove(enter_by)
            p.remove(enter_after)
            p.add(silent_prompt("clear", "Clears everything", "Yes"))
            try:
                p.remove(quantity)
            except KeyError:
                pass
        if duration.value == "forever":
            # mimic customer care website
            d = deadline_prompt(None)
            p.add(d)
            # trim these to keep it small
            p.remove(duration)
            p.remove(duration_additive)
            p.remove(enter_by)
            p.remove(enter_after)
            # unnecessary
            # p.add(baseline)
        if enter_by.value == "forever":
            enter_by.value = None
        if enter_by.value:
            enter_by.value += int(time.time())
        if enter_after.value == "forever":
            enter_after.value = None
        if enter_after.value:
            enter_after.value = int(time.time()) - enter_after.value

    p.cleanup = cleanup
    return p


class imh_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("imh")

    def get_title(self):
        return "IMH Evaluation Key"


class unsub_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("unsub", 50000)

    def get_title(self):
        return "Unsub Evaluation Key"


class body_contains_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("body_contains")

    def get_title(self):
        return "Body Contains Key"


class max_interfaces(key_tool):
    def get_prompts(self):
        hardware_address = hardware_address_prompt()
        component = silent_prompt("component", "Component", "max_interfaces")
        quantity = quantity_prompt(256)
        p = prompts()
        p.add(hardware_address)
        p.add(component)
        p.add(quantity)
        return p

    def get_title(self):
        return "Max Interfaces Feature Key"


class aol(key_tool):
    def get_prompts(self):
        hardware_address = hardware_address_prompt()
        component = silent_prompt("component", "Component", "tagged_log")
        component2 = silent_prompt("component", "Component", "tcp_push")
        p = prompts()
        p.add(hardware_address)
        p.add(component)
        p.add(silent_prompt("quantity", "Quantity", 1))
        p.add(next_key_prompt())
        p.add(component2)
        p.add(silent_prompt("quantity", "Quantity", 1))
        return p

    def get_title(self):
        return "AOL's tagged_log and tcp_push key"


class Brightmail_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("Brightmail")

    def get_title(self):
        return "Brightmail Evaluation Key"


class mcafee_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("mcafee")

    def get_title(self):
        return "McAfee Evaluation Key"


class sophos_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("sophos")

    def get_title(self):
        return "Sophos Evaluation Key"


class centralized_management_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("clustering")

    def get_title(self):
        return "Centralized Management Key"


class vof_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("VOF")

    def get_title(self):
        return "Virus Outbreak Filters"


class throttle_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("throttle")

    def get_title(self):
        return "CPU trottling Key"


class dynamic_throttle_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("throttle_dynamic")

    def get_title(self):
        return "Dynamic Throttle  Evaluation Key"


class throttle_increment_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("throttle_increment")

    def get_title(self):
        return "Throttle Increment Evaluation Key"


class remote_upgrades_evaluation(key_tool):
    def get_prompts(self):
        return generic_evaluation("RemoteUpgrades", duration=90)

    def get_title(self):
        return "Remote Upgrades Evaluation Key"


class command_key:
    def __init__(self):
        if len(sys.argv) != 4:
            print "usage: command_key COMPONENT SERIAL DURATION"
            sys.exit(1)
        self.component = sys.argv[1]
        self.hw = sys.argv[2]
        self.duration = int(sys.argv[3])

    def render(self):
        print self.key

    def run(self):
        self.key = generate(self.hw, None,
                            {'component': self.component,
                             'duration': self.duration,
                             'baseline': 0,
                             'quantity': 1,
                             'duration_additive': 1})
        self.render()


class command_clear_key(command_key):
    def __init__(self):
        if len(sys.argv) != 3:
            print "usage: command_key COMPONENT SERIAL"
            sys.exit(1)
        self.component = sys.argv[1]
        self.hw = sys.argv[2]

    def run(self):
        self.key = generate(self.hw, None,
                            {'component': self.component,
                             'clear': 1})
        self.render()


class command_reset_key(command_key):
    def run(self):
        self.key = generate(self.hw, None,
                            {'component': self.component,
                             'clear': 1,
                             'duration': self.duration,
                             'baseline': 0,
                             'quantity': 1})
        self.render()


class combo_key:
    def __init__(self):
        if len(sys.argv) != 3:
            print "usage: combo_key SERIAL DURATION"
            sys.exit(1)
        self.hw = sys.argv[1]
        self.duration = int(sys.argv[2])

    def render(self):
        print self.key

    def run(self):
        self.key = generate(self.hw, None,
                            {'component': 'imh',
                             'duration': self.duration,
                             'baseline': 0,
                             'quantity': 1,
                             'duration_additive': 1},
                            {'component': 'sophos',
                             'duration': self.duration,
                             'baseline': 0,
                             'quantity': 1,
                             'duration_additive': 1},
                            {'component': 'Brightmail',
                             'duration': self.duration,
                             'baseline': 0,
                             'quantity': 1,
                             'duration_additive': 1},
                            {'component': 'VOF',
                             'duration': self.duration,
                             'baseline': 0,
                             'quantity': 1,
                             'duration_additive': 1})
        self.render()


# broken:
class nini(key_tool):
    def get_prompts(self):
        p = generic_evaluation("imh")
        p.add(next_key_prompt())
        p.add(silent_prompt("duration_additive", "Duration Additive", "Yes"))
        p.add(read_only_prompt("component", "Component", "sophos", ""))
        p.add(duration_prompt(45))
        p.add(silent_quantity_prompt(1))
        p.add(next_key_prompt())
        p.add(silent_prompt("duration_additive", "Duration Additive", "Yes"))
        p.add(read_only_prompt("component", "Component", "Brightmail", ""))
        p.add(duration_prompt(30))
        p.add(silent_quantity_prompt(1))
        p.add(next_key_prompt())
        p.add(silent_prompt("duration_additive", "Duration Additive", "Yes"))
        p.add(read_only_prompt("component", "Component", "VOF", ""))
        p.add(duration_prompt(30))
        p.add(silent_quantity_prompt(1))
        return p

    def get_title(self):
        return "Nini's Experimental Key"


if __name__ == '__main__':
    (command, ext) = os.path.splitext(os.path.split(sys.argv[0])[1])
    f = getattr(sys.modules[__name__], command, None)
    if f and callable(f):
        f().run()
    else:
        print "Content-Type: text/html\n\n"
        print "unknown command: %s" % command


# import tags
# hw = tags.hardware_address()
# feature_key.generate_single(hw, component='I', duration=60, baseline=0, quantity=1)
#   ZkxcH-H61yr-Hbezz-ROpt1-LjxpL-niPMS-YtK0c-dyIon-gvs=
# feature_key.generate_single(hw, component='I', duration=60, baseline=0, quantity=1)
# feature_key.generate_single(hw, component='I', deadline=None, quantity=1)
# feature_key.generate_single(hw, component='i', quantity=4)
# feature_key.generate_single(hw, component='i', quantity=10, baseline_additive=1, key_additive=1)
#   aRyoQ-0WG3Z-/fw/g-dre4O-0IoeO-Xmuu8-Qf
# feature_key.generate_single(hw, component='i', quantity=256)

# evaluation for 30 days, fascist entry
# feature_key.generate_single(hw, component='I', duration=30*86400, baseline=0, quantity=1, enter_after=(time.time() - 2*86400), enter_by=(time.time() + 30*86400))
# +gnIY-gPV/p-GVrUM-/lQPC-ZiNEQ-WsFfn-D8zMM-xpdvx-nAaki-sCRME-nKhA=

# evaluation for 30 days
# feature_key.generate_single(hw, component='I', duration=30*86400, baseline=0, quantity=1)
# N2IVe-5eN4t-x+c2f-+fFg4-cEECP-P6Ric-2brUZ-Z/ZiU-qdQ=

# evaluation over:
# feature_key.generate_single(hw, component='I', clear=1, quantity=1)
# vhDXA-Xb3IQ-o4q1+-BRl+M-wA==

# shortcut
# telnet /tmp/hermes.bd
# import os; import features; import feature_key
# features.register(feature_key.generate_single(os.getenv("SERIAL_NUMBER"), quantity=1, component='sophos'))


def nini(hw, duration=30):
    sys.argv = [sys.argv[0], hw, duration * 86400]
    combo_key().run()
