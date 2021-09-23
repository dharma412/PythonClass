#!/usr/bin/env python
# $Header: //prod/main/sarf_centos/testlib/coeus1201/util/accesslogparser.py#1 $

"""
AccessLogParser
------------
- grep the WGA access log file and parse entries
- return AccessLogResults object which contains information
  about the grep results.
"""
from common.shell import qlogreader
import sys
import re
example_aclog = ('1318962049.518 370 10.7.1.69 TCP_MISS/200 3850242 GET http://services.wga/test-data/SSE/merlin/TPCD_2.msi "IAF-W2K3-AD1\iafuser@myNtlmRealm" DIRECT/services.wga application/x-ole DEFAULT_CASE_11-iafTestPolicy-iafTestID-NONE-NONE-NONE-DefaultGroup <IW_infr,6.0,18,"The PC Detective",0,78375,2358,-,"-",-,-,-,"-",-,-,"-","-",-,-,nc,-,"Commercial System Monitor","-","Unknown","Unknown","-","-",83248.48,0,-,"-","-"> -')

def list_fold(l, index, total_items, join_str=' '):
    """ Fold total_items number of fields together, starting at the index.

>>> import accesslogparser
>>> lf = accesslogparser.list_fold
>>> a = ['1', '2', '3', '4', '5']
>>> lf(a, 2, 2)
>>> a
['1', '2', '3 4', '5']
>>> lf(a, -2, 2)
>>> a
['1', '2', '3 4 5']
    """
    neg_index = index < 0
    fold_str = l.pop(index)
    if neg_index:
        index += 1
    for i in range(total_items-1):
        fold_str += "%s%s" % (join_str, l.pop(index))
        if neg_index:
            index += 1
    if neg_index and index == 0:
        l.append(fold_str)
    else:
        l.insert(index, fold_str)

def remove_quotes(s):
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    else:
        return s

class LogCheckException(Exception):
    pass

class ParseError(Exception):
    pass

class AccessLogEntry:
    """ Hold all potential fields of the WGA access logs
    """
    def __init__(self):
        self.utime = 0
        self.elapsed = 0
        self.client = ''
        self.action = ''
        self.wbrs_score = ''
        self.status = 0
        self.bytes = 0
        self.http_line = ''
        self.ident = ''
        self.peer_tag = ''
        self.peerhost = ''
        self.mimetype = ''
        self.acl_dec_tag = ''
        self.policy_group = ''
        self.identity = ''
        self.oms_policy = ''
        self.data_security_policy = ''
        self.dlp_policy = ''
        self.routing_policy = ''

        # includes 5 previous attributes
        # left for backward compatibility
        self.routing_group = ''

        self.user_agent = ''
        self.url_filt_cat = ''

        # Webroot specific values
        self.wr_asw_verdict = ''
        self.wr_spyware_name = ''
        self.wr_trr = ''
        self.wr_spyid = ''
        self.wr_traceid = ''

        # Mcafee specific values
        self.mc_verdict = ''
        self.mc_filename = ''
        self.mc_scan_error = ''
        self.mc_detect_type = ''
        self.mc_virus_type = ''
        self.mc_virus_name = ''

        # Data Loss Prevention specific values
        self.ids_verdict = ''
        self.icap_verdict = ''

        # Firestones CA specific values
        self.fs_url_cat_code = ''
        self.fs_req_side_cat = ''

        # Sophos specific values
        self.sophos_verdict = ''
        self.sophos_code = ''
        self.sophos_class = ''
        self.sophos_name = ''

        # DVS specific values
        self.dvs_verdict = ''

        # WBRS Threat Type
        self.wbrs_threat = ''

        # AVC specific values
        self.avc_app = ''
        self.avc_type = ''
        self.avc_behavior = ''

        # Safe search specific values
        self.safe_srch_verdict = ''

        # Bandwidth control specific
        self.bw_avg = ''
        self.bw_throttle = ''

        # Mobile User Security specific values
        self.mus_tag = ''

        # Outbound AMW scan verdicts
        self.outbound_dvs_verdict_name = ''
        self.outbound_dvs_threat_name = ''

    def print_debug(self):
        print 'utime', self.utime
        print 'elapsed', self.elapsed
        print 'client', self.client
        print 'action', self.action
        print 'wbrs_score', self.wbrs_score
        print 'status', self.status
        print 'bytes', self.bytes
        print 'http_line', self.http_line
        print 'ident', self.ident
        print 'peer_tag', self.peer_tag
        print 'peer_host', self.peerhost
        print 'mimetype', self.mimetype
        print 'acl_dec_tag', self.acl_dec_tag
        print 'policy_group', self.policy_group
        print 'identity', self.identity
        print 'oms_policy', self.oms_policy
        print 'data_security_policy', self.data_security_policy
        print 'dlp_policy', self.dlp_policy
        print 'routing_policy', self.routing_policy
        print 'user_agent', self.user_agent
        print 'url_filt_cat', self.url_filt_cat

        # Webroot specific values
        print 'wr_spyware_name', self.wr_spyware_name
        print 'wr_asw_verdict', self.wr_asw_verdict
        print 'wr_trr', self.wr_trr
        print 'wr_spyid', self.wr_spyid
        print 'wr_traceid', self.wr_traceid

        # Mcafee specific values
        print 'mc_verdict', self.mc_verdict
        print 'mc_filename', self.mc_filename
        print 'mc_scan_error', self.mc_scan_error
        print 'mc_detect_type', self.mc_detect_type
        print 'mc_virus_type', self.mc_virus_type
        print 'mc_virus_name', self.mc_virus_name

        # Sophos specific values
        print 'sophos_verdict', self.sophos_verdict
        print 'sophos_code', self.sophos_code
        print 'sophos_class', self.sophos_class
        print 'sophos_name', self.sophos_name

        # Data Loss Prevention specific values
        print 'ids_verdict', self.ids_verdict
        print 'icap_verdict', self.icap_verdict

        # Firestone CA specific values
        print 'fs_url_cat_code', self.fs_url_cat_code
        print 'fs_req_side_cat', self.fs_req_side_cat

        # DVS specific values
        print 'dvs_verdict', self.dvs_verdict

        # WBRS Threat Type
        print 'wbrs_threat', self.wbrs_threat

        # AVC specific values
        print 'avc_app', self.avc_app
        print 'avc_type', self.avc_type
        print 'avc_behavior', self.avc_behavior

        # Safe search specific values
        print 'safe_srch_verdict', self.safe_srch_verdict

        # Bandwidth control specific
        print 'bw_avg', self.bw_avg
        print 'bw_throttle', self.bw_throttle

        # Mobile User Security specific values
        print 'mus_tag', self.mus_tag

        # Outbound AMW scan verdicts
        print 'outbound_dvs_verdict_name', self.outbound_dvs_verdict_name
        print 'outbound_dvs_threat_name', self.outbound_dvs_threat_name

class AccessLogResults(qlogreader.QlogResults):

    def build_misc_info(self):
        quoted_str = '("[ a-zA-Z0-9-:_./@]+"|-)'
        quoted_str_integer_re = '("[ a-zA-Z0-9-_./@]+"|[0-9-]+)'
        integer_re = '([0-9-]+)'
        score_re = '([a-z0-9-.]+)'
        cat_re = '([ \[\]a-zA-Z0-9-_]+)'
        misc_info_list = [
            cat_re,       # URL Cat
            score_re,     # WBRS Score
            quoted_str_integer_re,   # Webroot Verdict
            quoted_str,   # WR Name
            integer_re,   # WR TRR
            integer_re,   # WR Spy ID
            cat_re,       # Trace ID    --words like 'Skipped' are showing up
            quoted_str_integer_re,   # Mcafee Verdict
            quoted_str,   # Mcafee Filename
            integer_re,   # Mcafee Scan Error
            integer_re,   # Mcafee Detect Type
            integer_re,   # Mcafee Virus Type
            quoted_str,   # Mcafee Virus Name
            integer_re,   # Sophos verdict
            quoted_str_integer_re,   # Sophos code
            quoted_str,   # Sophos class
            quoted_str,   # Sophos name
            cat_re,       # DLP IDS verdict
            cat_re,       # DLP ICAP verdict
            cat_re,       # Firestones Decoded URL category code
            cat_re,       # Firestones request-side category
            quoted_str,   # DVS verdict
            quoted_str,   # WBRS Threat Type
            quoted_str_integer_re,  # AVC application
            quoted_str_integer_re,  # AVC type
            quoted_str_integer_re,  # AVC behavior
            quoted_str,   # Safe search verdict
            score_re,     # Bandwidth average
            integer_re,   # Bandwidth throttle flag
            cat_re,       # MUS tag
            quoted_str,   # Outbound DVS verdict name
            quoted_str,   # Outbound DVS threat name
        ]

        return '<%s>' % ','.join(misc_info_list)

    def parse(self):
        misc_info_str = self.build_misc_info()
        self.misc_info_re = re.compile(misc_info_str)

        MIME_INDEX = -4
        MISC_INFO_INDEX = -2

        qlogreader.QlogResults.parse(self)

        # No parsing to do if we have no entries
        if not self.found_lines:
            return

        self.access_entries = []
        # Operate on self.found_lines
        for line in self.found_lines:
            #separating user agent field from the accesslog entry
            if ">" in line:
                index = line.index('>')
                user_agent_line = line[index+1:]
                line = line[:index+1]
                line = line + ' -'
            aclog_fields = line.split()

            entry = AccessLogEntry()

            misc_info = self.misc_info_re.search(line)
            if not misc_info:
                raise ParseError, "Fatal error parsing misc info " \
                    "<url_cat,wbrs_score,wr_verdict,wr_spyname,wr_trr," \
                    "wr_spyid,wr_traceid,mcafee_verdict,mcafee_file," \
                    "mcafee_error,mcafee_type,mcafee_virus_type," \
                    "mcafee_virus_name,sophos_verdict,sophos_code," \
                    "sophos_class,sophos_name,ids_verdict,icap_verdict," \
                    "fs_url_cat_code,fs_req_side_cat,dvs_verdict," \
                    "wbrs_threat,avc_app,avc_type,avc_behavior," \
                    "safe_srch_verdict,bw_avg,bw_throttle,mus_tag," \
                    "outbound_dvs_verdict_name,outbound_dvs_threat_name>" \
                    "in line: \n\n%s\n" % line

            quoted_str_fields = (3,4,8,9,13,15,16,17,22,23,24,25,26,27,31,32)
            for field_num in quoted_str_fields:
                field_len = len(misc_info.group(field_num).split())
                list_fold(aclog_fields, MISC_INFO_INDEX - (field_len - 1), field_len)

            # Gotcha: The Mime type can come in two parts. A semicolon denotes this,
            # so if we find it then we collapse the two fields into one.
            if aclog_fields[MIME_INDEX] and \
               aclog_fields[MIME_INDEX].endswith(';'):
                list_fold(aclog_fields, MIME_INDEX, 2)

            entry.utime = int(float(aclog_fields[0]))
            entry.elapsed = int(aclog_fields[1])
            entry.client = aclog_fields[2]

            (entry.action, status) = aclog_fields[3].split('/', 2)
            entry.status = int(status)

            entry.bytes = int(aclog_fields[4])

            # I know the first 5 and the last 6, every thing else
            # is in the middle.
            entry.http_line = ' '.join(aclog_fields[5:-6])

            entry.ident = remove_quotes(aclog_fields[-6])
            (entry.peer_tag, entry.peerhost) = \
                                   aclog_fields[-5].split('/', 2)
            entry.mimetype = aclog_fields[-4]

            decision_tags = aclog_fields[-3].split('-', 2)
            if len(decision_tags) == 1:
                entry.acl_dec_tag = decision_tags[0]
            elif len(decision_tags) == 2:
                entry.acl_dec_tag, entry.policy_group = decision_tags
            elif len(decision_tags) == 3:
                entry.acl_dec_tag = decision_tags[0]
                entry.policy_group = decision_tags[1]
                # parse identity and other policies
                identity_policies = decision_tags[2].split('-')
                entry.identity = identity_policies[0]
                entry.oms_policy = identity_policies[1]
                entry.data_security_policy = identity_policies[2]
                entry.dlp_policy = identity_policies[3]
                entry.routing_policy = identity_policies[4]
                # include whole string with identity, OMS, Data Security, DLP
                # and Routing policies
                # left for backward compatibility
                entry.routing_group = decision_tags[2]
            else:
                raise ParseError, "Fatal error parsing the ACL decision " \
                                  "tag / Policy Group in this accesslog " \
                                  "entry: \n%s\n" % line

            # Preserve the '-' if aclog_fields[-3] == '-'
            if not entry.acl_dec_tag:
                entry.acl_dec_tag = '-'

            # Remove autogenerated integer from ACL decision tag
            tag_match = re.match(r'(.*)_[0-9]+$', entry.acl_dec_tag)
            if tag_match:
                entry.acl_dec_tag = tag_match.group(1)

            try:
                self._parse_misc_info(aclog_fields[-2], entry)
            except ParseError:
                raise ParseError, "Fatal error parsing misc info " \
                    "<url_cat,wbrs_score,wr_verdict,wr_spyname,wr_trr," \
                    "wr_spyid,wr_traceid,mcafee_verdict,mcafee_file," \
                    "mcafee_error,mcafee_type,mcafee_virus_type," \
                    "mcafee_virus_name,sophos_verdict,sophos_code," \
                    "sophos_class,sophos_name,ids_verdict,icap_verdict," \
                    "fs_url_cat_code,fs_req_side_cat,dvs_verdict," \
                    "wbrs_threat,avc_app,avc_type,avc_behavior," \
                    "safe_srch_verdict,bw_avg,bw_throttle,mus_tag," \
                    "outbound_dvs_verdict_name,outbound_dvs_threat_name>" \
                    "in line: \n\n%s\n" % line

            # parse user agent and custom fields
            quoted_field = False
            field_id = 0
            custom_fields = ['']
            for char in user_agent_line.strip():
                if char == ' ' and not quoted_field:
                    field_id += 1
                    custom_fields.append('')
                    continue
                if char == '"':
                    quoted_field = not quoted_field
                    continue
                custom_fields[field_id] += char

            entry.user_agent = custom_fields[0]

            self.access_entries.append(entry)

    def _parse_misc_info(self, info_str, entry):
        """ Parse out the following from an access log entry:

<URL_filt_cat,WBRS,verdict,spyname,wr_trr,wr_spyid,wr_traceid>
wr_trr - Threat Risk Ratio (Webroot specific)
wr_spyid - Threat identifier (Webroot specific)
wr_traceid - Scan identifier (Webroot specific)

"""
        mo = self.misc_info_re.search(info_str)
        if not mo:
            raise ParseError

        entry.url_filt_cat = mo.group(1)
        try:
            entry.wbrs_score = float(mo.group(2))
        except ValueError:
            entry.wbrs_score = mo.group(2)
        entry.wr_asw_verdict = remove_quotes(mo.group(3))
        entry.wr_spyware_name = remove_quotes(mo.group(4))
        entry.wr_trr = mo.group(5)
        entry.wr_spyid = mo.group(6)
        entry.wr_traceid = mo.group(7)
        entry.mc_verdict = remove_quotes(mo.group(8))
        entry.mc_filename = remove_quotes(mo.group(9))
        entry.mc_scan_error = mo.group(10)
        entry.mc_detect_type = mo.group(11)
        entry.mc_virus_type = mo.group(12)
        entry.mc_virus_name = remove_quotes(mo.group(13))
        entry.sophos_verdict = remove_quotes(mo.group(14))
        entry.sophos_code = remove_quotes(mo.group(15))
        entry.sophos_class = remove_quotes(mo.group(16))
        entry.sophos_name = remove_quotes(mo.group(17))
        entry.ids_verdict = mo.group(18)
        entry.icap_verdict = mo.group(19)
        entry.fs_url_cat_code = mo.group(20)
        entry.fs_req_side_cat = mo.group(21)
        entry.dvs_verdict = remove_quotes(mo.group(22))
        entry.wbrs_threat = remove_quotes(mo.group(23))
        entry.avc_app = remove_quotes(mo.group(24))
        entry.avc_type = remove_quotes(mo.group(25))
        entry.avc_behavior = remove_quotes(mo.group(26))
        entry.safe_srch_verdict = remove_quotes(mo.group(27))
        entry.bw_avg = mo.group(28)
        entry.bw_throttle = mo.group(29)
        entry.mus_tag = mo.group(30)
        entry.outbound_dvs_verdict_name = remove_quotes(mo.group(31))
        entry.outbound_dvs_threat_name = remove_quotes(mo.group(32))

if __name__=='__main__':
    alr = None
    aclog_entry = raw_input('Cut and paste an accesslog entry here, ' \
                            'and its fields will be parsed and printed:\n\n')
    if aclog_entry.strip():
        alr = AccessLogResults(out=aclog_entry)
    else:
        alr = AccessLogResults(out=example_aclog)
    print '\n'
    alr.access_entries[0].print_debug()
