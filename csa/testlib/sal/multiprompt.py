#!/usr/bin/env python
"""A special type of expect match for handling a number
of different ironport CLI prompts"""

import sal.net.iputils
import socket
import re
from sal.deprecated import expect

# constants to determine prompt type
SINGLE = 1
SINGLE_POD = 2
CLUSTER = 3
GROUP = 4
MACHINE = 5


def is_ip(ip):
    try:
        sal.net.iputils.inet_atohm(ip)
        return True
    except socket.error:
        return False


class MultiPrompt(expect.UserMatch):
    """A special type of expect match for handling a number
of different ironport CLI prompts"""

    def __init__(self, hostname):
        """ Compile all of the possible prompts that we will face
            in the ironport CLI.
        """
        if is_ip(hostname):
            self.hostname = socket.gethostbyaddr(hostname)[0]
        else:
            self.hostname = hostname
        self.single = "%s>" % self.hostname
        self.single_pod = "%s>" % self.hostname.rsplit('.', 1)[0]
        self.cluster = re.compile("\(Cluster (\S+)\)>")
        self.group = re.compile("\(Group (\S+)\)>")
        self.machine = re.compile("\(Machine (\S+)\)>")
        self.last_prompt = None
        self.last_prompt_type = None
        self.last_name = None
        self.mtype = None
        self.callback = None

    def __str__(self):
        s = []
        s.append('+' + self.__class__.__name__)
        s.append('|self.single: %s' % self.single)
        s.append('|self.single_pod: %s' % self.single)
        s.append('|self.cluster: %s' % self.cluster.pattern)
        s.append('|self.group: %s' % self.group.pattern)
        s.append('|self.machine: %s' % self.machine.pattern)
        s.append('|self.last_prompt: %s' % self.last_prompt)
        s.append('|self.last_prompt_type: %s' % self.last_prompt_type)
        s.append('|self.last_name: %s' % self.last_name)
        s.append('+self.mtype: %s' % self.mtype)
        return '\n'.join(s)

    def search(self, text, pos=0, endpos=2147483647):
        """ search for each prompt, setting attributes when
            we find out which mode we are in. Then return the
            last prompt.
        """
        n = text.find(self.single, pos, endpos)
        if n != -1:
            self.last_prompt = self.single
            self.last_prompt_type = SINGLE
            self.last_name = self.hostname
            return self.last_prompt
        n = text.find(self.single_pod, pos, endpos)
        if n != -1:
            self.last_prompt = self.single_pod
            self.last_prompt_type = SINGLE_POD
            self.last_name = self.hostname
            return self.last_prompt
        mo = self.cluster.search(text[pos:endpos])
        if mo:
            self.last_prompt = mo.group(0)
            self.last_prompt_type = CLUSTER
            self.last_name = mo.group(1)
            return self.last_prompt
        mo = self.group.search(text[pos:endpos])
        if mo:
            self.last_prompt = mo.group(0)
            self.last_prompt_type = GROUP
            self.last_name = mo.group(1)
            return self.last_prompt
        mo = self.machine.search(text[pos:endpos])
        if mo:
            self.last_prompt = mo.group(0)
            self.last_prompt_type = MACHINE
            self.last_name = mo.group(1)
            return self.last_prompt
        return None

    def get_match_object(self, mtype=None, callback=None):
        self.mtype = mtype
        self.callback = callback
        return (self, callback)

    def matchlen(self):
        if not self.last_prompt:
            return 0
        return len(self.last_prompt)
