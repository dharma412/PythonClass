#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/tophosts.py#1 $ $DataTime:$  $Author: saurgup5 $

"""
    tophosts IAF 2 configurator
"""

from sal.containers import cfgholder
import clictorbase

class tophosts(clictorbase.IafCliConfiguratorBase):
    def __call__(self, option=1):
        # Returns a TopHostsObj object containing a sorted by the given option
        bs = self._tophosts_string(str(option))
        th = TopHostsObj()
        return th.parse(bs)

    def _tophosts_string(self, option=1):
        """ Parses the result of tophosts command. """
        self._writeln('tophosts')
        self._query('Sort results')
        self._query_select_list_item(str(option))
        return self._wait_for_prompt()


def _float(s):
    # filters out commas and converts string to a float
    return float(filter(lambda c: c.isdigit(), s))

def _right_side(line, delim=":"):
    return line.split(delim,1)[1].strip()

def _parse_ntuple(line):
    fields = line.split()
    output = []
    output.append( fields[0])
    output.append( fields[1])
    output.extend( map(_float, fields[2:]))
    return output

class TopHostsLine(cfgholder.CfgHolder):
    def __init__(self):
        cfgholder.CfgHolder.__init__(self)
        self.rank = None
        self.host = None
        self.active_recipients = None
        self.connection_out = None
        self.delivered_recipients = None
        self.soft_bounced = None
        self.hard_bounced = None

    def _parse(self, line):
        (self.rank, self.host, self.active_recipients, \
        self.connection_out, self.delivered_recipients, \
        self.soft_bounced, self.hard_bounced) = _parse_ntuple(line)


class TopHostsObj(cfgholder.CfgHolder):
    """This object is returned by the configurator tophosts() command.
    It is a report of the top recieving hosts on the DUT.  """

    def __init__(self):
        cfgholder.CfgHolder.__init__(self)
        # Common
        self.lines = []

    def update(self, ctor):
        self.parse(ctor.tophosts_string())

    def parse(self, bs):

        self._result={}
        lines = bs.split("\n")
        # Do a basic sanity check on the number of lines
        # and print error if we don't get what we expect.
        if (len(lines) < 4):
            raise ValueError, "TopHostsObj.parse: bad input string"

        for ii in xrange(len(lines)):
            if lines[0].find("Status as of") >= 0:
                break
            lines.pop(0)

        self._result['date'] = _right_side(lines[0])
        # check to see if the lines are wrapped
        line_hard = 1
        for line in lines:
            if line.find("Soft") >= 0:
                if line.find("Hard") < 0:
                    # Lines are hard wrapped, we will need to join them.
                    lines2=[]
                    for jline in lines[:line_hard]:
                        lines2.append(jline)

                    lines2[-1] += lines[line_hard] # add Hard line
                    lines2.append(lines[line_hard+1] + lines[line_hard+2])
                    lines2.append(lines[line_hard+3])

                    max_list = len(lines)-1
                    line_hard += 4
                    while (line_hard < max_list):
                        lines2.append(lines[line_hard].strip("\r") + \
                                      "     " + lines[line_hard+1])
                        line_hard += 2
                    lines = lines2
                    break
                else:
                    break
            else:
                line_hard += 1

        for line in lines[5:]:
            if len(line) > 30: # ick
                this_line = TopHostsLine()
                this_line._parse(line)
                rank = this_line['rank']
                del this_line['rank']
                self._result[rank] = this_line
        return self._result

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    th = tophosts(cli_sess)
    print th()
    print 'tophosts test DONE!'
