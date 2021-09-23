""" Includes Utilities to get the counter and group names.
"""

import datetime
import httplib
import string
import time

from optparse import OptionParser
import urllib
import urllib2
import base64
import simplejson as json
import pprint

_ = str


class TestError(Exception):
    pass


# Allowed length of iso8601 date time queries.
iso8601_format1 = '2014-07-05T19:20+01:00/2014-07-15T15:01+01:00'
iso8601_format2 = '2014-07-05T19:20Z/2014-07-15T15:21z'
iso8601_format1_len = len(iso8601_format1)
iso8601_format2_len = len(iso8601_format2)

SEC_IN_HOUR = 3600
HOURS_IN_DAY = 24

# Help in URI
HELP = 'help'

# Special dictionary keys
DETAILS = 'details'
DESCRIPTION = 'description'
PARAMETERS = 'parameters'

STORIES = 'stories'

## Special Help output dictionary keys
# Queried node
URI = 'uri'
# Immediate children of queried node
LINKS = 'links'
# Requested Content (reporting counters / health paramters)
DATA = 'data'

# Parameters
DURATION = 'duration'
MAX = 'max'
ENTITY_STARTS_WITH = 'starts_with'
ENTITY = 'entity'

supported_parameters = {
    DURATION: {DESCRIPTION: _("""\
Duration for which data is requested. This should be in ISO8601 format.""")},
    MAX: {
        DESCRIPTION: _("""Maximum number of entities to return. (1-1000)""")},
    ENTITY_STARTS_WITH: {DESCRIPTION: _("""\
Defines whether enitity is an exact match or it starts with the specified \
entity value.\
""")},
    ENTITY: {DESCRIPTION: _("""\
Entity for which the details are requested. This might be of various kinds \
(emails address, IP address, Domain name, etc) depending on the overall
request type.\
""")},
}

# average_mail_system_capacity_counters are used to split and join counter names of
# MAIL_SYSTEM_CAPACITY group.
average_mail_system_capacity_counters = {
    'WORKQUEUE_AVERAGE_TIME_SPENT': ['WORKQUEUE_TIME_TOTAL', 'WORKQUEUE_TIME_COUNT'],
    'WORKQUEUE_AVERAGE_MESSAGES': ['WORKQUEUE_MESSAGES_TOTAL', 'WORKQUEUE_MESSAGES_COUNT'],
    'AVERAGE_INCOMING_MESSAGE_SIZE_IN_BYTES': ['BYTES_IN', 'INCOMING_MESSAGES'],
    'AVERAGE_OUTGOING_MESSAGE_SIZE_IN_BYTES': ['BYTES_OUT', 'OUTGOING_MESSAGES'],
    'OVERALL_PERCENT_CPU_USAGE': ['CPU_TOTAL', 'CPU_COUNT'],
    'OVERALL_PERCENT_CPU_USAGE_FOR_ANTISPAM': ['ANTISPAM_CPU_TOTAL', 'ANTISPAM_CPU_COUNT'],
    'OVERALL_PERCENT_CPU_USAGE_FOR_ANTIVIRUS': ['ANTIVIRUS_CPU_TOTAL', 'ANTIVIRUS_CPU_COUNT'],
    'OVERALL_PERCENT_CPU_USAGE_FOR_MAIL_COUNT': ['MAIL_CPU_TOTAL', 'MAIL_CPU_COUNT'],
    'OVERALL_PERCENT_CPU_USAGE_FOR_REPORTING': ['REPORTING_CPU_TOTAL', 'REPORTING_CPU_COUNT'],
    'AVERAGE_MEMORY_PAGE_SWAPPING': ['SWAP_PAGE_OUT_TOTAL', 'SWAP_PAGE_OUT_COUNT'],
    'OVERALL_PERCENT_CPU_USAGE_FOR_QUARANTINE': ['QUARANTINE_CPU_TOTAL', 'QUARANTINE_CPU_COUNT'],
}

available_stats = {
    DETAILS: {
        DESCRIPTION: _("""Key statistical data of the appliance."""),
        PARAMETERS: (DURATION,),
    },
    'MAIL_INCOMING_TRAFFIC_SUMMARY': {
        DETAILS: {
            STORIES: ['US19131', 'ALL'],
            DESCRIPTION: _("""\
Summary of incoming mail activity on the appliance.\
"""),
        },

        'DETECTED_VIRUS': {DETAILS: {DESCRIPTION: _("""\
Number of messages (recipients) identified as virus positive.\
"""),
                                     }, },
        'THREAT_CONTENT_FILTER': {DETAILS: {DESCRIPTION: _("""\
Number of messages (recipients) that triggered at least one content filter \
with an action of drop, bounce, or quarantine.\
""")}, },
        'TOTAL_THREAT_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Total number of threat messages (recipients) detected by the appliance.\
""")}, },
        'BLOCKED_REPUTATION': {DETAILS: {DESCRIPTION: _("""\
Number of messages stopped by reputation filtering.\
""")}, },
        'BLOCKED_INVALID_RECIPIENT': {DETAILS: {DESCRIPTION: _("""\
Number of messages (recipients) rejected by recipient acceptance policies.\
""")}, },
        'DETECTED_SPAM': {DETAILS: {DESCRIPTION: _("""\
Number of messages (recipients) identified as spam or suspect spam.\
""")}, },
        'TOTAL_CLEAN_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Number of clean messages (recipients).\
""")}, },
        'TOTAL_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients).\
""")}, },
        'DETECTED_AMP': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) detected as malware by AMP.\
""")}, },
        'MALICIOUS_URL': {DETAILS: {DESCRIPTION: _("""\
Number of urls (recipients) identified as malicious.\
""")}, },
        'BLOCKED_DMARC': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) blocked by DMARC.\
""")}, },
        'MARKETING_MAIL': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) detected as marketing mail.\
""")}, },
        'IMS_SPAM_INCREMENT_OVER_CASE': {DETAILS: {DESCRIPTION: _("""\
Incoming messages (recipients) classified as spam by IMS, while these \
messages could have been classified as clean by IPAS.\
""")}, },

    },

    'MAIL_OUTGOING_TRAFFIC_SUMMARY': {
        DETAILS: {
            STORIES: ['US19131', 'ALL'],
            DESCRIPTION: _("""\
Summary of outgoing mail activity on the appliance.\
"""),
        },
        'DETECTED_SPAM': {DETAILS: {DESCRIPTION: _("""\
Number of messages identified as spam or suspect spam.\
""")}, },
        'DETECTED_VIRUS': {DETAILS: {DESCRIPTION: _("""\
Number of messages identified as virus positive.\
""")}, },
        'MALICIOUS_URL': {DETAILS: {DESCRIPTION: _("""\
Number of urls identified as malicious.\
""")}, },
        'THREAT_CONTENT_FILTER': {DETAILS: {DESCRIPTION: _("""\
Number of messages that triggered at least one content filter \
with an action of drop, bounce, or quarantine.\
""")}, },
        'TOTAL_CLEAN_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Number of clean messages.\
""")}, },
        'TOTAL_RECIPIENTS_PROCESSED': {DETAILS: {DESCRIPTION: _("""\
Total number of messages that are clean, viral, spam or blocked \
by filters.\
""")}, },
        'TOTAL_HARD_BOUNCES': {DETAILS: {DESCRIPTION: _("""\
String yet to be decided
""")}, },
        'TOTAL_RECIPIENTS_DELIVERED': {DETAILS: {DESCRIPTION: _("""\
Number of messages delivered.\
""")}, },
        'TOTAL_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Total number of messages.\
""")}, },
        'TOTAL_DLP_INCIDENTS': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) stopped by DLP.\
""")}, },

    },

    'MAIL_DLP_OUTGOING_TRAFFIC_SUMMARY': {
        DETAILS: {
            STORIES: ['US20364', 'ALL'],
            DESCRIPTION: _("""\
Summary of the incidents of data loss prevention (DLP) policy violations \
occurring in outgoing mail.\
"""),
        },
        'DLP_INCIDENTS_CRITICAL': {DETAILS: {DESCRIPTION: _("""\
Total number of critical severity DLP incidents.\
""")}, },
        'DLP_INCIDENTS_HIGH': {DETAILS: {DESCRIPTION: _("""\
Total number of high severity DLP incidents.\
""")}, },
        'DLP_INCIDENTS_MEDIUM': {DETAILS: {DESCRIPTION: _("""\
Total number of medium severity DLP incidents.\
""")}, },
        'DLP_INCIDENTS_LOW': {DETAILS: {DESCRIPTION: _("""\
Total number of low severity DLP incidents.\
""")}, },
        'TOTAL_DLP_INCIDENTS': {DETAILS: {DESCRIPTION: _("""\
Total number of DLP incidents.\
""")}, },

    },

    'MAIL_SYSTEM_CAPACITY': {
        DETAILS: {
            STORIES: ['US21001', 'ALL'],
            DESCRIPTION: _("""\
Summary of system capacity parameters for the appliance.\
"""),
        },
        'WORKQUEUE_AVERAGE_TIME_SPENT': {DETAILS: {DESCRIPTION: _("""\
Average time (in seconds) spent in workqueue.\
""")}, },
        'WORKQUEUE_MESSAGES_MAX': {DETAILS: {DESCRIPTION: _("""\
Maximum messages in workqueue.\
""")}, },
        'INCOMING_CONNECTIONS': {DETAILS: {DESCRIPTION: _("""\
Total incoming connections.\
""")}, },
        'INCOMING_MESSAGES': {DETAILS: {DESCRIPTION: _("""\
Total incoming messages.\
""")}, },
        'WORKQUEUE_AVERAGE_MESSAGES': {DETAILS: {DESCRIPTION: _("""\
Average messages in workqueue.\
""")}, },
        'AVERAGE_INCOMING_MESSAGE_SIZE_IN_BYTES': {DETAILS: {DESCRIPTION: _("""\
Average incoming message size in bytes.\
""")}, },
        'BYTES_IN': {DETAILS: {DESCRIPTION: _("""\
Total incoming message size in bytes.\
""")}, },
        'OUTGOING_CONNECTIONS': {DETAILS: {DESCRIPTION: _("""\
Total outgoing connections.\
""")}, },
        'OUTGOING_MESSAGES': {DETAILS: {DESCRIPTION: _("""\
Total outgoing messages.\
""")}, },
        'AVERAGE_OUTGOING_MESSAGE_SIZE_IN_BYTES': {DETAILS: {DESCRIPTION: _("""\
Average outgoing message size in bytes.\
""")}, },
        'BYTES_OUT': {DETAILS: {DESCRIPTION: _("""\
Total outgoing message size in bytes.\
""")}, },
        'OVERALL_PERCENT_CPU_USAGE': {DETAILS: {DESCRIPTION: _("""\
Overall average percent cpu usage.\
""")}, },
        'OVERALL_PERCENT_CPU_USAGE_FOR_ANTISPAM': {DETAILS: {DESCRIPTION: _("""\
Overall average percent CPU usage for antispam..\
""")}, },
        'OVERALL_PERCENT_CPU_USAGE_FOR_ANTIVIRUS': {DETAILS: {DESCRIPTION: _("""\
Overall average percent CPU usage for antivirus.\
""")}, },
        'OVERALL_PERCENT_CPU_USAGE_FOR_MAIL_COUNT': {DETAILS: {DESCRIPTION: _("""\
Overall average percent CPU usage for mail processing.\
""")}, },
        'OVERALL_PERCENT_CPU_USAGE_FOR_REPORTING': {DETAILS: {DESCRIPTION: _("""\
Overall average percent CPU usage for reporting.\
""")}, },
        'OVERALL_PERCENT_CPU_USAGE_FOR_QUARANTINE': {DETAILS: {DESCRIPTION: _("""\
Overall average percent CPU usage for quarantine.\
""")}, },
        'AVERAGE_MEMORY_PAGE_SWAPPING': {DETAILS: {DESCRIPTION: _("""\
Average memory page swapping.\
""")}, },

    },

    'MAIL_DMARC_INCOMING_TRAFFIC_SUMMARY': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20364', 'ALL'],
                  DESCRIPTION: _("""\
Information about DMARC verifications for incoming mail.\
"""),
                  },
        'DMARC_PASSED': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) that passed DMARC verification per domain.\
""")}, },
        'DMARC_FAILED_TOTAL': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) that failed DMARC verification per domain.\
""")}, },
        'DMARC_FAILED_REJECTED': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) that failed DMARC verification \
and were rejected per domain.\
""")}, },
        'DMARC_FAILED_QUARANTINED': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) that failed DMARC verification \
and were quarantined per domain.\
""")}, },
        'DMARC_FAILED_NONE': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) that failed DMARC verification \
and no action taken per domain.\
""")}, },
        'DMARC_TOTAL_ATTEMPTED': {DETAILS: {DESCRIPTION: _("""\
Total number of messages (recipients) subjected to DMARC verification per domain.\
""")}, }

    },

    'MAIL_SENDER_GROUP_SUMMARY': {
        DETAILS: {
            STORIES: ['US20367', 'ALL'],
            DESCRIPTION: _("""\
Summary of connections by mail flow policy action for all sender \
groups on the appliance.\
"""),
        },
        'CONNECTIONS_ACCEPT': {DETAILS: {DESCRIPTION: _("""\
Total number of connections undergone accept mail flow policy action.\
""")}, },
        'CONNECTIONS_RELAY': {DETAILS: {DESCRIPTION: _("""\
Total number of connections undergone relay mail flow policy action.\
""")}, },
        'CONNECTIONS_REJECT': {DETAILS: {DESCRIPTION: _("""\
Total number of connections undergone reject mail flow policy action.\
""")}, },
        'CONNECTIONS_TCP_REFUSE': {DETAILS: {DESCRIPTION: _("""\
Total number of connections undergone a TCP refuse mail flow policy action.\
""")}, },

    },

    'MAIL_URL_CATEGORY_SUMMARY': {
        DETAILS: {
            STORIES: ['US20367', 'ALL'],
            DESCRIPTION: _("""\
Information about URL categories occurring in incoming and outgoing mail.\
"""),
        },
        'INCOMING_COUNT': {DETAILS: {DESCRIPTION: _("""\
URL Category distribution for incoming mails.\
""")}, },
        'OUTGOING_COUNT': {DETAILS: {DESCRIPTION: _("""\
URL Category distribution for outgoing mails.\
""")}, },

    },

    'MAIL_URL_DOMAIN_SUMMARY': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Information about URL domains occurring in incoming and outgoing spam messages.\
"""),
                  },
        'INCOMING_COUNT': {DETAILS: {DESCRIPTION: _("""\
Number of URLs by domains in incoming spam messages.\
""")}, },
        'OUTGOING_COUNT': {DETAILS: {DESCRIPTION: _("""\
Number of URLs by domains in outgoing spam messages.\
""")}, },

    },

    'MAIL_URL_REPUTATION_SUMMARY': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Information about malicious and suspicious URLs occurring in incoming \
and outgoing messages.\
"""),
                  },
        'INCOMING_COUNT': {DETAILS: {DESCRIPTION: _("""\
URL Reputation distribution for incoming mails.\
""")}, },
        'OUTGOING_COUNT': {DETAILS: {DESCRIPTION: _("""\
URL Reputation distribution for outgoing mails.\
""")}, },

    },

    'MAIL_SECURITY_SUMMARY': {
        DETAILS: {
            STORIES: ['US20366', 'ALL'],
            DESCRIPTION: _("""\
Summary of Transport Layer Security (TLS)  for incoming and outgoing mail.\
"""),
        },
        'RECEIVED_CONN_TLS_SUCCESS': {DETAILS: {DESCRIPTION: _("""\
Total number of successful (TLS required) incoming TLS connections.\
""")}, },
        'RECEIVED_CONN_TLS_OPT_SUCCESS': {DETAILS: {DESCRIPTION: _("""\
Total number of successful (TLS preferred) incoming TLS connections.\
""")}, },
        'RECEIVED_CONN_TLS_FAIL': {DETAILS: {DESCRIPTION: _("""\
Total number of failed (TLS required) incoming TLS connections.\
""")}, },
        'RECEIVED_CONN_TLS_OPT_FAIL': {DETAILS: {DESCRIPTION: _("""\
Total number of failed (TLS preferred) incoming TLS connections.\
""")}, },
        'RECEIVED_CONN_PLAIN': {DETAILS: {DESCRIPTION: _("""\
Total number of unencrypted incoming connections.\
""")}, },
        'RECEIVED_CONN_TOTAL': {DETAILS: {DESCRIPTION: _("""\
Total number of incoming connections.\
""")}, },
        'RECEIVED_ENCRYPTED_TLS': {DETAILS: {DESCRIPTION: _("""\
Total number of TLS encrypted messages (recipients) in incoming mail.\
""")}, },
        'RECEIVED_UNENCRYPTED': {DETAILS: {DESCRIPTION: _("""\
Total number of unencrypted messages (recipients) in incoming mail.\
""")}, },
        'RECEIVED_TOTAL': {DETAILS: {DESCRIPTION: _("""\
Total recipients received.\
""")}, },
        'SENT_CONN_TLS_SUCCESS': {DETAILS: {DESCRIPTION: _("""\
Total number of successful (TLS required) outgoing TLS connections.\
""")}, },
        'SENT_CONN_TLS_OPT_SUCCESS': {DETAILS: {DESCRIPTION: _("""\
Total number of successful (TLS preferred) outgoing TLS connections.\
""")}, },
        'SENT_CONN_TLS_FAIL': {DETAILS: {DESCRIPTION: _("""\
Total number of failed (TLS required) outgoing TLS connections.\
""")}, },
        'SENT_CONN_TLS_OPT_FAIL': {DETAILS: {DESCRIPTION: _("""\
Total number of failed (TLS preferred) outgoing TLS connections.\
""")}, },
        'SENT_CONN_PLAIN': {DETAILS: {DESCRIPTION: _("""\
Total number of unencrypted outgoing connections.\
""")}, },
        'SENT_CONN_TOTAL': {DETAILS: {DESCRIPTION: _("""\
Total number of outgoing connections.\
""")}, },
        'SENT_ENCRYPTED_TLS': {DETAILS: {DESCRIPTION: _("""\
Total number of TLS encrypted messages (recipients) in outgoing mail.\
""")}, },
        'SENT_UNENCRYPTED': {DETAILS: {DESCRIPTION: _("""\
Total number of unencrypted messages (recipients) in outgoing mail.\
""")}, },
        'SENT_TOTAL': {DETAILS: {DESCRIPTION: _("""\
Total recipients sent.\
""")}, },

    },

    'MAIL_AUTHENTICATION_SUMMARY': {
        DETAILS: {
            STORIES: ['US20368', 'ALL'],
            DESCRIPTION: _("""\
Summary of SMTP Authentication statistics for incoming mail.\
"""),
        },
        'RECEIVED_CONN_TOTAL': {DETAILS: {DESCRIPTION: _("""\
Total number of incoming connections.\
""")}, },
        'RECEIVED_CONN_NOAUTH': {DETAILS: {DESCRIPTION: _("""\
Total number of incoming connections without authentication attempt.\
""")}, },
        'RECEIVED_CONN_CERT_SUCCESS': {DETAILS: {DESCRIPTION: _("""\
Total number of successful incoming connections authenticated with \
a client certificate.\
""")}, },
        'RECEIVED_CONN_CERT_FAIL': {DETAILS: {DESCRIPTION: _("""\
Total number of incoming connections failed to authenticate with \
a client certificate.\
""")}, },
        'RECEIVED_CONN_AUTH_SUCCESS': {DETAILS: {DESCRIPTION: _("""\
Total number of successful incoming connections authenticated with \
SMTP AUTH command.\
""")}, },
        'RECEIVED_CONN_AUTH_FAIL': {DETAILS: {DESCRIPTION: _("""\
Total number of received connections failed to authenticate with \
SMTP AUTH command.\
""")}, },
        'RECEIVED_TOTAL': {DETAILS: {DESCRIPTION: _("""\
Total number of recipients received.\
""")}, },
        'RECEIVED_AUTH': {DETAILS: {DESCRIPTION: _("""\
Total number of recipients received and authenticated.\
""")}, },
        'RECEIVED_NOAUTH': {DETAILS: {DESCRIPTION: _("""\
Total number of non-authenticated recipients received.\
""")}, },

    },

    'MAIL_INCOMING_MALWARE_THREAT_FILE_DETAIL_SUMMARY': {
        DETAILS: {
            STORIES: ['US20999', 'ALL'],
            DESCRIPTION: _("""\
Summary of malware threat files detected by Advanced Malware Protection (AMP) \
in incoming mail.\
"""),
        },
        'DETECTED_AMP_FILES': {DETAILS: {DESCRIPTION: _("""\
Total number of malware threat files detected by AMP.\
""")}, },

    },

    'MAIL_VIRUS_TYPE_DETAIL': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US19109', 'ALL'],
                  DESCRIPTION: _("""\
Details of top incoming and outgoing virus types identified by the appliance.\
"""),
                  },
        'TOTAL_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Total number of incoming and outgoing messages (recipients) infected by \
top n virus types, where n is the user-specified value. Default is top 10.\
""")}, },
        'INCOMING_TOTAL_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Total number of incoming messages (recipients) infected by top n virus types, \
where n is the user-specified value. Default is top 10.\
""")}, },
        'OUTGOING_TOTAL_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Total number of outgoing messages (recipients) infected by top n virus types, \
where n is the user-specified value. Default is top 10.\
""")}, },

    },

    'MAIL_DLP_OUTGOING_POLICY_DETAIL': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US20364', 'ALL'],
                  DESCRIPTION: _("""\
Details of the incidents of data loss prevention (DLP) policy violations \
occurring in outgoing mail.\
"""),
                  },
        'DLP_INCIDENTS_LOW': {DETAILS: {
            DESCRIPTION: _("""\
Total number of low severity DLP incidents by policy matches.\
""")}, },
        'DLP_INCIDENTS_MEDIUM': {DETAILS: {
            DESCRIPTION: _("""\
Total number of medium severity DLP incidents by policy matches.\
""")}, },
        'DLP_INCIDENTS_HIGH': {DETAILS: {
            DESCRIPTION: _("""\
Total number of high severity DLP incidents by policy matches.\
""")}, },
        'DLP_INCIDENTS_CRITICAL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of critical severity DLP incidents by policy matches.\
""")}, },
        'TOTAL_DLP_INCIDENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of DLP incidents.\
""")}, },
        'DLP_ACTION_ENCRYPTED': {DETAILS: {
            DESCRIPTION: _("""\
Total number of recipients (messages) matching DLP policy that were \
delivered (encrypted).\
""")}, },
        'DLP_ACTION_DELIVERED': {DETAILS: {
            DESCRIPTION: _("""\
Total number of recipients (messages) matching DLP policy that were \
delivered (clear).\
""")}, },
        'DLP_ACTION_DROPPED': {DETAILS: {
            DESCRIPTION: _("""\
Total number of recipients (messages) matching DLP policy that were dropped.\
""")}, },

    },

    'MAIL_INCOMING_DOMAIN_DETAIL': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US20363', 'US20366', 'ALL'],
                  DESCRIPTION: _("""\
Details of incoming mail activity for connecting domains.\
"""),
                  },
        'TOTAL_REJECTED_CONNECTIONS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of rejected connections by domain.\
""")}, },
        'TOTAL_ACCEPTED_CONNECTIONS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of accepted connections by domain.\
""")}, },
        'TOTAL_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of attempted recipients by domain.\
""")}, },
        'TOTAL_THROTTLED_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of throttled recipients by domain.\
""")}, },
        'BLOCKED_REPUTATION': {DETAILS: {
            DESCRIPTION: _("""\
Total number of reputation filtered recipients by domain.\
""")}, },
        'BLOCKED_INVALID_RECIPIENT': {DETAILS: {
            DESCRIPTION: _("""\
Total number of invalid recipients by domain.\
""")}, },
        'DETECTED_SPAM': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as spam or suspect \
spam per domain.\
""")}, },
        'DETECTED_VIRUS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as virus \
positive per domain.\
""")}, },
        'DETECTED_AMP': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified by Advanced Malware \
Protection per domain.\
""")}, },
        'THREAT_CONTENT_FILTER': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) stopped by content filter per domain.\
""")}, },
        'BLOCKED_DMARC': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) stopped due to DMARC verification per domain.\
""")}, },
        'TOTAL_THREAT_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of threat messages (recipients) per domain.\
""")}, },
        'MARKETING_MAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as marketing mail per domain.\
""")}, },
        'TOTAL_CLEAN_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of clean messages (recipients) by domain.\
""")}, },
        'CONN_TLS_FAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of failed (TLS Required) TLS connections by domain.\
""")}, },
        'CONN_TLS_SUCCESS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of successful (TLS required) TLS connections by domain.\
""")}, },
        'CONN_TLS_OPT_FAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of failed (TLS preferred) TLS connections by domain.\
""")}, },
        'CONN_TLS_OPT_SUCCESS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of successful (TLS preferred) TLS connections by domain.\
""")}, },
        'CONN_TLS_TOTAL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of TLS connections by domain.\
""")}, },
        'CONN_PLAIN': {DETAILS: {
            DESCRIPTION: _("""\
Total number of non-TLS connections by domain.\
""")}, },
        'ENCRYPTED_TLS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) over TLS.\
""")}, }

    },

    'MAIL_INCOMING_IP_HOSTNAME_DETAIL': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US20363', 'ALL'],
                  DESCRIPTION: _("""\
Details of incoming mail activity for connecting IP address and hostname.\
"""),
                  },
        'DNS_VERIFIED': {DETAILS: {
            DESCRIPTION: _("""\
DNS verified for IP.\
""")}, },
        'SBRS_SCORE': {DETAILS: {
            DESCRIPTION: _("""\
SBRS score for IP.\
""")}, },
        'LAST_SENDER_GROUP': {DETAILS: {
            DESCRIPTION: _("""\
Sender groups for IP.\
""")}, },
        'LAST_SENDER_GROUP_NAME': {DETAILS: {
            DESCRIPTION: _("""\
Sender group name for IP.\
""")}, },
        'TOTAL_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of attempted recipients by IP.\
""")}, },
        'BLOCKED_REPUTATION': {DETAILS: {
            DESCRIPTION: _("""\
Total number of reputation filtered recipients by IP.\
""")}, },
        'BLOCKED_INVALID_RECIPIENT': {DETAILS: {
            DESCRIPTION: _("""\
Total number of invalid recipients by IP.\
""")}, },
        'DETECTED_SPAM': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as spam or suspect spam \
by IP.\
""")}, },
        'DETECTED_VIRUS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as virus positive by IP.\
""")}, },
        'DETECTED_AMP': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as AMP positive by IP.\
""")}, },
        'THREAT_CONTENT_FILTER': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages that triggered at least one content filter with \
an action of drop, bounce, or quarantine by IP.\
""")}, },
        'BLOCKED_DMARC': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) blocked due to DMARC verification failure by IP.\
""")}, },
        'TOTAL_THREAT_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of spam, virus and threat filter messages (recipients) by IP.\
""")}, },
        'MARKETING_MAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) detected as marketing mail by IP.\
""")}, },
        'TOTAL_CLEAN_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total Number of clean messages (recipients) by IP.\
""")}, },

    },

    'MAIL_AUTHENTICATION_INCOMING_DOMAIN': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US20368', 'ALL'],
                  DESCRIPTION: _("""\
Details of SMTP Authentication statistics occurring in incoming mail by domain.\
"""),
                  },
        'TOTAL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of received connections.\
""")}, },
        'NOAUTH': {DETAILS: {
            DESCRIPTION: _("""\
Total number of incoming (received) connections without authentication attempt.\
""")}, },
        'CERT_SUCCESS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of successful incoming (received) connections authenticated \
with a client certificate from the domain.\
""")}, },
        'CERT_FAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of incoming (received) connections failed to authenticate \
with a client certificate from the domain.\
""")}, },
        'AUTH_SUCCESS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of successful incoming (received) connections authenticated \
with an SMTP AUTH command from the domain.\
""")}, },
        'AUTH_FAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of incoming (received) connections failed to authenticate \
with an SMTP AUTH command from the domain.\
""")}, },
        'AUTH_DISALLOW': {DETAILS: {
            DESCRIPTION: _("""\
Total number of incoming (received) connections disallowed to authenticate \
with an SMTP AUTH command from the domain.\
""")}, },
        'CERT_FALLBACK_SUCCESS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of successful incoming (received) connections authenticated \
with a fall-back from a client certificate to an SMTP AUTH command from the domain.\
""")}, },
        'CERT_FALLBACK_FAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of incoming (received) connections failed to authenticate with \
a fall-back from a client certificate to an SMTP AUTH command from the domain.
""")}, },

    },

    'MAIL_INCOMING_NETWORK_DETAIL': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US20363', 'ALL'],
                  DESCRIPTION: _("""\
Details of incoming mail activity for network owner.\
"""),
                  },
        'TOTAL_REJECTED_CONNECTIONS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of rejected connections for network owner.\
""")}, },

        'TOTAL_ACCEPTED_CONNECTIONS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of accepted connections for network owner.\
""")}, },
        'TOTAL_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of recipients for network owner.\
""")}, },
        'TOTAL_THROTTLED_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total throttled connections for network owner.\
""")}, },
        'BLOCKED_REPUTATION': {DETAILS: {
            DESCRIPTION: _("""\
Total number of reputation filtered recipients for network owner.\
""")}, },
        'BLOCKED_INVALID_RECIPIENT': {DETAILS: {
            DESCRIPTION: _("""\
Total number of invalid recipients for the network owner.\
""")}, },
        'DETECTED_SPAM': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as spam or suspect spam \
for network owner.\
""")}, },
        'DETECTED_VIRUS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as virus positive for \
network owner.\
""")}, },
        'DETECTED_AMP': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as AMP positive for \
network owner.\
""")}, },
        'THREAT_CONTENT_FILTER': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages that triggered at least one content filter with an \
action of drop, bounce, or quarantine for network owner.\
""")}, },
        'BLOCKED_DMARC': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages blocked due to DMARC verification failure for \
network owner.\
""")}, },
        'TOTAL_THREAT_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of threat recipients for network owner.\
""")}, },
        'MARKETING_MAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) detected as marketing mail for \
network owner.\
""")}, },
        'TOTAL_CLEAN_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total Number of clean messages (recipients) for network owner.\
""")}, },

    },

    'MAIL_SENDER_GROUP_DETAIL': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Details of connections by sender group.\
"""),
                  },
        'TOTAL_CONNECTIONS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of connections by sender group.\
""")}, },

    },

    'MAIL_CONTENT_FILTER_INCOMING': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Details of incoming content filter matches.\
"""),
                  },
        'RECIPIENTS_MATCHED': {DETAILS: {
            DESCRIPTION: _("""\
Total number of incoming recipients matched for content filter.\
""")}, },

    },

    'MAIL_CONTENT_FILTER_OUTGOING': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Details of outgoing content filter matches.\
"""),
                  },
        'RECIPIENTS_MATCHED': {DETAILS: {
            DESCRIPTION: _("""\
Total number of outgoing recipients matched for content filter.\
""")}, },

    },

    'MAIL_SENDER_DOMAIN_DETAIL': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US20365', 'ALL'],
                  DESCRIPTION: _("""\
Details of internal domains sending mails.\
"""),
                  },
        'DETECTED_SPAM': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as spam or suspect \
spam from the domain.\
""")}, },
        'DETECTED_VIRUS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as virus positive \
from the domain.\
""")}, },
        'THREAT_CONTENT_FILTER': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) stopped by content filter \
from the domain.\
""")}, },
        'TOTAL_DLP_INCIDENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of DLP incidents from the domain.\
""")}, },
        'TOTAL_THREAT_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of threat recipients from domain.\
""")}, },
        'TOTAL_CLEAN_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total Number of clean messages (recipients) from the domain.\
""")}, },
        'TOTAL_RECIPIENTS_PROCESSED': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages that are clean, viral, spam or blocked by filters \
from the domain.\
""")}, },

    },

    'MAIL_SENDER_IP_HOSTNAME_DETAIL': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US20363', 'ALL'],
                  DESCRIPTION: _("""\
Details of internal IP and hostname sending mails.\
"""),
                  },
        'DETECTED_SPAM': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as spam or suspect spam \
from IP.\
""")}, },
        'DETECTED_VIRUS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) identified as virus positive \
from IP.\
""")}, },
        'THREAT_CONTENT_FILTER': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) stopped by content filter \
from IP.\
""")}, },
        'TOTAL_DLP_INCIDENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of DLP incidents from IP.\
""")}, },
        'TOTAL_THREAT_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of threat recipients from IP.\
""")}, },
        'TOTAL_CLEAN_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total Number of clean messages (recipients) in outgoing mail from the IP.\
""")}, },
        'TOTAL_RECIPIENTS_PROCESSED': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) that are clean or identified as threats from IP.\
""")}, },

    },

    'MAIL_ENV_SENDER_RATE_LIMIT': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Details of rate limiting policy offenders.\
"""),
                  },
        'ENV_SENDER_INCIDENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of incidents by envelope sender.\
""")}, },
        'ENV_SENDER_REJECTED_RCPTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of incidents by rejected recipients.\
""")}, },

    },

    'MAIL_ENV_SENDER_STATS': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Details of mails by envelope senders.\
"""),
                  },
        'NUM_MSGS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages from envelope sender.\
""")}, },

    },

    'MAIL_HVM_MSG_FILTER_STATS': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Statistics for High Volume Mail (HVM) message filter \
(that uses Header Repeats rule).\
"""),
                  },
        'NUM_MATCHES': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages matched by filter.\
""")}, },

    },

    'MAIL_MSG_FILTER_STATS': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Details of message filter matches on the appliance.\
"""),
                  },
        'NUM_MATCHES': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) matched by message filter.\
""")}, },

    },

    'MAIL_SUBJECT_STATS': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US20367', 'ALL'],
                  DESCRIPTION: _("""\
Statistics for subjects of messages received by the appliance.\
"""),
                  },
        'NUM_MSGS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) by subject.\
""")}, },

    },

    'MAIL_VOF_THREAT_SUMMARY': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US21000', 'ALL'],
                  DESCRIPTION: _("""\
Information about threats detected by Outbreak Filters (OF).\
"""),
                  },
        'THREAT_DETECTED': {DETAILS: {DESCRIPTION: _("""\
Number of threats detected by OF per threat category.\
""")}, },

    },

    'MAIL_VOF_THREATS_BY_THREAT_TYPE': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US21000', 'ALL'],
                  DESCRIPTION: _("""\
Information about threat types detected by Outbreak Filters (OF).\
"""),
                  },
        'THREAT_DETECTED': {DETAILS: {
            DESCRIPTION: _("""\
Number of threats detected by OF per threat type.\
""")}, },

    },

    'MAIL_VOF_THREATS_BY_LEVEL': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US21000', 'ALL'],
                  DESCRIPTION: _("""\
Information about severity of threats detected by Outbreak Filters (OF).\
"""),
                  },
        'THREAT_DETECTED': {DETAILS: {
            DESCRIPTION: _("""\
Number of threats detected by OF per threat level.\
""")}, },

    },

    'MAIL_VOF_THREATS_BY_TIME_THRESHOLD': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US21000', 'ALL'],
                  DESCRIPTION: _("""\
Information about mails in Outbreak Filters (OF) quarantine.\
"""),
                  },
        'QUARANTINE_MESSAGE_EXIT': {DETAILS: {
            DESCRIPTION: _("""\
Number of messages quarantined by OF per amount of time spent in quarantine.\
""")}, },

    },

    'MAIL_VOF_THREATS_REWRITTEN_URL': {
        DETAILS: {PARAMETERS: (MAX,),
                  STORIES: ['US21000', 'ALL'],
                  DESCRIPTION: _("""\
Information about URLs rewritten by Outbreak Filters (OF).\
"""),
                  },
        'REWRITTEN_URL': {DETAILS: {
            DESCRIPTION: _("""\
Number of URL rewritten by OF per URL.\
""")}, },

    },

    'MAIL_INCOMING_MALWARE_THREAT_FILE_DETAIL': {
        DETAILS: {PARAMETERS: (MAX, ENTITY,),
                  STORIES: ['US20999', 'ALL'],
                  DESCRIPTION: _("""\
Details of malware threat files detected by Advanced Malware Protection (AMP) \
in incoming mail.\
"""),
                  },
        'DETECTED_AMP': {DETAILS: {
            DESCRIPTION: _("""\
Total number of malware threat files by threat file SHA256..\
""")}, },

    },

    'MAIL_DESTINATION_DOMAIN_DETAIL': {
        DETAILS: {PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  STORIES: ['US20368', 'US20332', 'US20366', 'ALL'],
                  DESCRIPTION: _("""\
Details of mails sent to destination domains.\
"""),
                  },
        'DETECTED_SPAM': {DETAILS: {
            DESCRIPTION: _("""\
Number of messages (recipients) identified as spam or suspect spam sent to destination domain.\
""")}, },
        'DETECTED_VIRUS': {DETAILS: {
            DESCRIPTION: _("""\
Number of messages (recipients) identified as virus positive sent to destination domain.\
""")}, },
        'THREAT_CONTENT_FILTER': {DETAILS: {
            DESCRIPTION: _("""\
Number of messages (recipients) that triggered at least one content filter with an action \
of drop, bounce, or quarantine sent to destination domain.\
""")}, },
        'TOTAL_THREAT_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of threat messages (recipients) sent to destination domain.\
""")}, },
        'TOTAL_CLEAN_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Number of clean messages (recipients) sent to destination domain.\
""")}, },
        'TOTAL_RECIPIENTS_PROCESSED': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) that are clean, viral, spam or blocked by \
filters sent to destination domain.\
""")}, },
        'HARD_BOUNCES': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) sent to destination domain and hard \
bounced by destination server.\
""")}, },
        'DELIVERED': {DETAILS: {
            DESCRIPTION: _("""\
Total messages (recipients) delivered to destination domain.\
""")}, },
        'TOTAL_RECIPIENTS': {DETAILS: {
            DESCRIPTION: _("""\
Total messages (recipients) sent to destination domain.\
""")}, },
        'CONN_TLS_FAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of failed (TLS Required) TLS connections by destination domain.\
""")}, },
        'CONN_TLS_SUCCESS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of successful (TLS Required) TLS connections by destination domain.\
""")}, },
        'CONN_TLS_OPT_FAIL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of failed (TLS Preferred) TLS connections by destination domain.\
""")}, },
        'CONN_TLS_OPT_SUCCESS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of successful (TLS Preferred) TLS connections by destination domain.\
""")}, },
        'CONN_LAST_TLS_STATUS': {DETAILS: {
            DESCRIPTION: _("""\
Last TLS connection status.\
""")}, },
        'CONN_TLS_TOTAL': {DETAILS: {
            DESCRIPTION: _("""\
Total number of connections sent using TLS.\
""")}, },
        'CONN_PLAIN': {DETAILS: {
            DESCRIPTION: _("""\
Total number of non-TLS connections.\
""")}, },
        'ENCRYPTED_TLS': {DETAILS: {
            DESCRIPTION: _("""\
Total number of messages (recipients) sent using TLS.\
""")}, },

    },

    'MAIL_USERS_DETAIL': {
        DETAILS: {DESCRIPTION: _("""\
Information about the mail sent and received by your internal users \
(per email address) through the appliance.\
"""),
                  STORIES: ['US19598', 'ALL'],
                  PARAMETERS: (MAX, ENTITY, ENTITY_STARTS_WITH),
                  },
        'OUTGOING_DETECTED_CONTENT_FILTER': {DETAILS: {
            DESCRIPTION: _("""\
Outgoing messages (recipients) that matched the content filters.\
""")}, },
        'INCOMING_MARKETING_MAIL': {DETAILS: {DESCRIPTION: _("""\
Incoming marketing messages (recipients).\
""")}, },
        'OUTGOING_DETECTED_SPAM': {DETAILS: {DESCRIPTION: _("""\
Outgoing messages (recipients) identified as spam-positive.\
""")}, },
        'INCOMING_DETECTED_VIRUS': {DETAILS: {DESCRIPTION: _("""\
Incoming messages (recipients) identified as virus-positive.\
""")}, },
        'INCOMING_DETECTED_AMP': {DETAILS: {DESCRIPTION: _("""\
Incoming messages (recipients) identified as AMP-positive.\
""")}, },
        'INCOMING_TOTAL_CLEAN_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Total incoming clean messages (recipients).\
""")}, },
        'INCOMING_DETECTED_SPAM': {DETAILS: {DESCRIPTION: _("""\
Incoming messages (recipients) identified as spam-positive.\
""")}, },
        'INCOMING_DETECTED_CONTENT_FILTER': {DETAILS: {
            DESCRIPTION: _("""\
Incoming messages (recipients) that matched the content filters.\
""")}, },
        'INCOMING_THREAT_CONTENT_FILTER': {DETAILS: {DESCRIPTION: _("""\
Incoming messages (recipients) stopped by the content filters.\
""")}, },
        'OUTGOING_TOTAL_CLEAN_RECIPIENTS': {DETAILS: {DESCRIPTION: _("""\
Total outgoing clean messages (recipients).\
""")}, },
        'OUTGOING_DETECTED_VIRUS': {DETAILS: {DESCRIPTION: _("""\
Outgoing messages (recipients) identified as virus-positive.\
""")}, },
        'INCOMING_DETECTED_IMS_SPAM_INCREMENT_OVER_CASE': {
            DETAILS: {DESCRIPTION: _("""\
Incoming messages (recipients) classified as spam by IMS, while these \
messages could have been classified as clean by IPAS.\
""")}, },
        'OUTGOING_DETECTED_IMS_SPAM_INCREMENT_OVER_CASE': {
            DETAILS: {DESCRIPTION: _("""\
Outgoing messages (recipients) classified as spam by IMS, while these \
messages could have been classified as clean by IPAS.\
""")}, },
        'OUTGOING_THREAT_CONTENT_FILTER': {DETAILS: {DESCRIPTION: _("""\
Outgoing messages (recipients) stopped by the content filters.\
""")}, },

    },
}

# DEFAULT_PERIOD is used to fire query to database.
DEFAULT_PERIOD = 'day'


def filter_params(keys):
    return filter(lambda x: x != DETAILS, keys)


def get_help(request):
    group_name = request.group_name
    counter_name = request.counter_name
    # Current URI help
    uri = {}
    # links information
    children = {}
    # return value - uri + links (if applicable)
    help_content = {}
    # root, groups, counters = 3
    levels_to_traverse = 3
    # Current URI path excluding 'help'
    uri_path = []
    # We start search at /stats/ or /health/
    root = request.uri_ctx.entire_path
    # fill all levels and filter non-existant ones
    levels = filter(lambda x: x is not None, [root, group_name, counter_name])
    # to track the current position in the dictonary
    current_level = available_stats
    for x in xrange(levels_to_traverse):
        uri_path.append(levels.pop(0))
        if not levels:
            uri['/'.join(uri_path).lower()] = \
                current_level[DETAILS][DESCRIPTION]
            for key in filter_params(current_level.iterkeys()):
                children[key.lower()] = current_level[key][DETAILS][DESCRIPTION]
            if children:
                help_content[LINKS] = children
            help_content[URI] = uri
            return (True, help_content)
        if levels[0] in current_level:
            current_level = current_level[levels[0]]
        else:
            return (False, 'Invalid URI')


conflicting_parameters = [set([MAX, ENTITY]), ]

open_file = None


def request_url(values):
    # print values
    req = urllib2.Request('%(protocol)s://%(host)s:%(port)s/api/v1.0/%(rest)s' \
                          % values)
    req.add_header('Accept', 'application/json')
    global open_file
    if values['cmdlist'] and open_file is not None:
        c1 = '-v -k --basic --user %(user)s:%(passwd)s' % values
        open_file.write('|'.join([c1, values['rest']]) + '\n')

    creds = base64.b64encode(':'.join([values['user'], values['passwd']]))
    req.add_header('Authorization', 'Basic %s' % creds)
    # urllib2._opener.handlers[1].set_http_debuglevel(100)
    try:
        r = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e
        print e.code
        # print e.reason
    except urllib2.URLError, e:
        print e.reason
    except:
        if not values['cmdlist']:
            raise
    else:
        data = r.read()
        data = json.loads(data)
        return data
        pprint.pprint(data)
        if DATA in data:
            return data[DATA]


def test(options):
    summary_counter_groups = []
    topn_counter_groups = []
    entity_counter_groups = []
    values = options
    rest = 'stats/%(group)s%(counter)s?%(args)s'
    query_args = {}
    if options['helptext']:
        rest = 'stats/%(group)s%(counter)s/help'

    for el in filter_params(available_stats.keys()):
        if PARAMETERS not in available_stats[el][DETAILS]:
            if values['story'] in available_stats[el][DETAILS][STORIES]:
                summary_counter_groups.append(el)
        else:
            if MAX in available_stats[el][DETAILS][PARAMETERS]:
                if values['story'] in available_stats[el][DETAILS][STORIES]:
                    topn_counter_groups.append(el)
            if ENTITY in available_stats[el][DETAILS][PARAMETERS]:
                if values['story'] in available_stats[el][DETAILS][STORIES]:
                    entity_counter_groups.append(el)
    if options['durtest']:
        # One counter from each type
        summary_counter_groups = summary_counter_groups[0]
        entity_counter_groups = entity_counter_groups[0]
        topn_counter_groups = entity_counter_groups
        durations = ['1h', '1d', options['fduration'],
                     options['fduration'].replace('z', '+00:00'),
                     options['fduration'].replace('z', '-00:00')]
    global open_file
    if options['cmdlist']:
        if open_file is None:
            open_file = open(values['filename'], 'w')
    entities = {}
    FILLED_DATA = 'Filled data'
    EMPTY_DATA = 'Empty data'
    print ''
    print '----------------'
    print 'SUMMARY COUNTERS'
    print '----------------'
    print ''
    durs = [FILLED_DATA]
    if values['eduration']:
        durs.append(EMPTY_DATA)
    for dur in durs:
        for sg in summary_counter_groups:
            query_args = {}
            print ''
            pprint.pprint('*' * 30 + ' New Counter Group ' + '*' * 30)
            print ''
            print sg + ' -- Duration: ' + dur
            print ''
            if dur is FILLED_DATA:
                duration = values['fduration']
            else:
                duration = values['eduration']
            if duration not in ('1d', '1h'):
                query_args = {'duration': duration}
            encoded_args = urllib.urlencode(query_args)
            if duration in ('1d', '1h'):
                encoded_args = encoded_args + '&' + duration
            values['rest'] = rest % {'group': sg.lower(), 'args': encoded_args,
                                     'counter': ''}
            data = request_url(values)
            if dur is FILLED_DATA:
                pprint.pprint(data)
            else:
                # verify_empty_summary
                if DATA in data:
                    for cnt in data[DATA]:
                        if not data[DATA][cnt] == 0:
                            raise TestError('summary failed: %s' % cnt)
            print ''
            pprint.pprint('-' * 10 + ' Individual Counters ' + '-' * 10)
            for cnt in filter_params(available_stats[sg].keys()):
                print ''
                values['rest'] = rest % {'group': sg.lower(),
                                         'args': encoded_args,
                                         'counter': '/' + cnt.lower()}
                data = request_url(values)
                if dur is FILLED_DATA:
                    pprint.pprint(data)
                else:
                    # verify_empty_summary
                    if DATA in data:
                        if not data[DATA][cnt] == 0:
                            raise TestError('summary failed: %s' % cnt)

    print ''
    print '----------------'
    print 'TOPN COUNTERS'
    print '----------------'
    print ''
    for dur in durs:
        for sg in topn_counter_groups:
            query_args = {}
            print ''
            pprint.pprint('*' * 30 + ' New Counter Group ' + '*' * 30)
            print ''
            print sg + ' -- Duration: ' + dur
            print ''
            if dur is FILLED_DATA:
                duration = values['fduration']
            else:
                duration = values['eduration']
            if duration not in ('1d', '1h'):
                query_args = {'duration': duration}
            if values['max']:
                query_args.update({'max': values['max']})
            encoded_args = urllib.urlencode(query_args)
            if duration in ('1d', '1h'):
                encoded_args = encoded_args + '&' + duration
            values['rest'] = rest % {'group': sg.lower(), 'args': encoded_args,
                                     'counter': ''}
            data = request_url(values)
            if DATA in data:
                for counter, val in data[DATA].items():
                    if val:
                        entities[sg] = val.keys()[0]
                        entities[sg + '/' + counter.upper()] = val.keys()[0]
            if dur is FILLED_DATA:
                pprint.pprint(data)
            else:
                # verify_empty_summary
                if DATA in data:
                    for cnt in data[DATA]:
                        if not data[DATA][cnt] == {}:
                            raise TestError('TopN failed: %s' % cnt)
            print ''
            pprint.pprint('-' * 10 + ' Individual Counters ' + '-' * 10)
            for cnt in filter_params(available_stats[sg].keys()):
                print ''
                values['rest'] = rest % {'group': sg.lower(),
                                         'args': encoded_args,
                                         'counter': '/' + cnt.lower()}
                data = request_url(values)
                if dur is FILLED_DATA:
                    pprint.pprint(data)
                else:
                    # verify_empty_summary
                    if DATA in data:
                        if not data[DATA][cnt] == {}:
                            raise TestError('TopN failed: %s' % cnt)

    print ''
    print '----------------'
    print 'ENTITY COUNTERS'
    print '----------------'
    print 'Entities Extracted from Topn Counters'
    print entities
    print '----------------'
    print ''
    for dur in durs:
        for types in [ENTITY, ENTITY_STARTS_WITH]:
            for sg in entity_counter_groups:
                query_args = {}
                print ''
                pprint.pprint('*' * 30 + ' New Counter Group ' + '*' * 30)
                print ''
                print sg + ' -- Duration: ' + dur
                if dur is FILLED_DATA:
                    duration = values['fduration']
                else:
                    duration = values['eduration']
                if duration not in ('1d', '1h'):
                    query_args = {'duration': duration}
                if sg in entities:
                    entity = entities[sg]
                    query_args.update({'entity': entity})
                    if types is ENTITY_STARTS_WITH:
                        print ''
                        print '=' * 20 + ' starts_with=true ' + '=' * 20
                        print ''
                        query_args.update({'starts_with': 'true'})
                else:
                    print ''
                    print 'NO ENTITY AVAILABLE FOR %s' % sg
                    print ''
                    continue
                encoded_args = urllib.urlencode(query_args)
                if duration in ('1d', '1h'):
                    encoded_args = encoded_args + '&' + duration
                values['rest'] = rest % {'group': sg.lower(),
                                         'args': encoded_args,
                                         'counter': ''}
                data = request_url(values)
                if dur is FILLED_DATA:
                    pprint.pprint(data)
                else:
                    # verify_empty_summary
                    if DATA in data:
                        if not data[DATA] == {}:
                            raise TestError('TopN failed: %s' % cnt)
                print ''
                pprint.pprint('-' * 10 + ' Individual Counters ' + '-' * 10)
                for cnt in filter_params(available_stats[sg].keys()):
                    print ''
                    if sg + '/' + cnt in entities:
                        local_entity = entities[sg + '/' + cnt]
                        query_args.update({'entity': local_entity})
                    elif sg in entities:
                        query_args.update({'entity': entity})
                    encoded_args = urllib.urlencode(query_args)
                    if duration in ('1d', '1h'):
                        encoded_args = encoded_args + '&' + duration
                    values['rest'] = rest % {'group': sg.lower(),
                                             'args': encoded_args,
                                             'counter': '/' + cnt.lower()}
                    data = request_url(values)
                    if dur is FILLED_DATA:
                        pprint.pprint(data)
                    else:
                        # verify_empty_summary
                        if DATA in data:
                            if not data[DATA] == {}:
                                raise TestError('TopN failed: %s' % cnt)


def test_topn(options):
    counter_groups = []
    values = options
    if values['fduration'] in ('1d', '1h'):
        rest = 'stats/%s?' + values['fduration']
    else:
        rest = 'stats/%s?duration=' + values['fduration']

    for el in filter_params(available_stats.keys()):
        if MAX in available_stats[el][DETAILS][PARAMETERS]:
            if values['story'] in available_stats[el][DETAILS][STORIES]:
                summary_counter_groups.append(el)
    for sg in summary_counter_groups:
        values['rest'] = rest % sg.lower()
        request_url(values)
        print '*' * 30


def test_entity(options):
    summary_counter_groups = []
    values = options
    if values['fduration'] in ('1d', '1h'):
        rest = 'stats/%s?' + values['fduration']
    else:
        rest = 'stats/%s?duration=' + values['fduration']

    for el in filter_params(available_stats.keys()):
        if PARAMETERS not in available_stats[el][DETAILS]:
            if values['story'] in available_stats[el][DETAILS][STORIES]:
                summary_counter_groups.append(el)
    for sg in summary_counter_groups:
        values['rest'] = rest % sg.lower()
        request_url(values)
        print '*' * 30


if __name__ == '__main__':
    global open_file

    parser = OptionParser(usage='usage: %prog [options]')
    parser.add_option("--port", dest="port", default="8443",
                      help="DUT port name to connect to - 8443")
    parser.add_option("--host", dest="host", default="c670e03.ibeng.sgg.cisco.com",
                      help="host - c670e03.ibeng.sgg.cisco.com")
    parser.add_option("--fduration", dest="fduration", default="1d",
                      help="Duration when data is filled - iso8601")
    parser.add_option("--eduration", dest="eduration", default=None,
                      help="Duration when data is not available - iso8601")
    parser.add_option("--protocol", dest="protocol", default="https",
                      help="Protocol - http(s)")
    parser.add_option("--user", dest="user", default="admin",
                      help="user - admin")
    parser.add_option("--passwd", dest="passwd", default="ironport",
                      help="password - ironport")
    parser.add_option("--story", dest="story", default="ALL",
                      help="User story - US19131")
    parser.add_option("--max", dest="max", default=2,
                      help="max - 2")
    parser.add_option("--dur-test", dest="durtest", default=False,
                      help="Test for all duration types - True")
    parser.add_option("--help-text", dest="helptext", default=False,
                      help="Help text query - True")
    parser.add_option("--cmd-list", dest="cmdlist", default=False,
                      help="print cmd list - True")
    parser.add_option("--filename", dest="filename", default='him.txt',
                      help="filename for cmd-list - him.txt")
    # parser.add_option("--logfile", dest="logfile", default='/tmp/api_log_file.txt',
    #                  help="Entire curl log dump file name. Default: /tmp/api_log_file.txt")
    # parser.add_option("-r","--repeat", dest="repeat_count", type='int', default=1,
    #                  help="number of times to loop around the file contents")
    # parser.add_option("-d","--delay", dest="repeat_delay", type='int', default=4,
    #                  help="number of seconds to wait before repeating the loop again")
    # parser.add_option("-v","--variable", action='append', dest="variables",
    #                  help="variables. syntax: -v D1:'16 May 2014' -v D2:'16 June 2014'")

    (options, args) = parser.parse_args()
    option_dict = vars(options)
    print option_dict
    try:
        test(option_dict)
    finally:
        if open_file is not None:
            open_file.close()
            open_file = None
