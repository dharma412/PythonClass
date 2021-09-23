#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/variables/sma/constants.py#3 $
# $DateTime: 2019/09/17 02:03:56 $
# $Author: rajaks $


class sma_user_roles(object):
    """Constants for predefined user roles."""
    ADMIN = 'Administrator'
    OPERATOR = 'Operator'
    RO_OPERATOR = 'Read-Only Operator'
    GUEST = 'Guest'
    CLOUD_ADMIN = 'Cloud Administrator'
    TECHNICIAN = 'Technician'

    # Web Only Roles
    WEB_ADMIN = 'Web Administrator'
    WEB_POLICY_ADMIN = 'Web Policy Administrator'
    URL_FILT_ADMIN = 'URL Filtering Administrator'

    # Email Only Roles
    EMAIL_ADMIN = 'Email Administrator'
    HELP_DESK = 'Help Desk User'


class sma_log_types(object):
    """Constants for log types."""
    AUTH = 'Authentication Logs'
    AUDIT = 'Audit Logs'
    BACKUP = 'Backup Logs'
    CLI_AUDIT = 'CLI Audit Logs'
    CONF_HISTORY = 'Configuration History Logs'
    FTP_SERVER = 'FTP Server Logs'
    HTTP = 'HTTP Logs'
    HAYSTACK = 'Haystack Logs'
    MAIL = 'IronPort Text Mail Logs'
    LDAP_DEBUG = 'LDAP Debug Logs'
    NTP = 'NTP Logs'
    REPORTING = 'Reporting Logs'
    REPORTING_QUERY = 'Reporting Query Logs'
    SMA = 'SMA Logs'
    SNMP = 'SNMP Logs'
    SLBL = 'Safe/Block Lists Logs'
    EUQ_GUI = 'Spam Quarantine GUI Logs'
    EUQ = 'Spam Quarantine Logs'
    STATUS = 'Status Logs'
    SYSTEM = 'System Logs'
    TRACKING = 'Tracking Logs'
    UPDATER = 'Updater Logs'


class sma_user_locations(object):
    """Constants for user locations"""
    LOCAL = 'local'
    REMOTE = 'remote'
    ALL = 'all'


class sma_config_masters(object):
    """Constants for Configuration Masters"""
    CM57 = 'Configuration Master 5.7'
    CM63 = 'Configuration Master 6.3'
    CM71 = 'Configuration Master 7.1'
    CM75 = 'Configuration Master 7.5'
    CM77 = 'Configuration Master 7.7'
    CM80 = 'Configuration Master 8.0'
    CM81 = 'Configuration Master 8.1'
    CM85 = 'Configuration Master 8.5'
    CM87 = 'Configuration Master 8.7'
    CM91 = 'Configuration Master 9.1'
    CM100 = 'Configuration Master 10.0'
    CM105 = 'Configuration Master 10.5'
    CM110 = 'Configuration Master 11.0'
    CM115 = 'Configuration Master 11.5'
    CM117 = 'Configuration Master 11.7'
    CM118 = 'Configuration Master 11.8'
    CM120 = 'Configuration Master 12.0'
    CM125 = 'Configuration Master 12.5'
    CM140 = 'Configuration Master 14.0'

class sma_config_source(sma_config_masters):
    """Constants for selecting configuration source for Conf. Masters"""
    CONFIG_FILE = 'Web Configuration File'
    WSA_CONFIG_FILE = "/tmp/wsa.xml"


class sma_email_reports(object):
    """Constants for schedule/archived reports type for Email"""
    FILTERS = 'Content Filters'
    DLP_INCIDENT = 'DLP Incident Summary'
    DELIVERY = 'Delivery Status'
    DOMAIN_BASED = 'Domain-Based Executive Summary'
    EXECUTIVE = 'Executive Summary'
    IN_MAIL = 'Incoming Mail Summary'
    INT_USERS = 'Internal Users Summary'
    OUT_DESTINATIONS = 'Outgoing Destinations'
    OUT_MAIL = 'Outgoing Mail Summary'
    OUT_DOMAIN_SENDERS = 'Outgoing Senders: Domains'
    SENDER_GROUPS = 'Sender Groups'
    SYSTEM_CAP = 'System Capacity'
    TLS_CONN = 'TLS Connections'
    VOF = 'Outbreak Filters'
    VIRUS_TYPES = 'Virus Types'
    ADVANCED_MALWARE_PROTECTION = 'Advanced Malware Protection'
    ADVANCED_MALWARE_PROTECTION_FILE_ANALYSIS = 'Advanced Malware Protection File Analysis'


class sma_web_reports(object):
    """Constants for scheduled/archived reports type for Web"""
    OVERVIEW = 'Overview'
    USERS = 'Users'
    WEB_SITES = 'Web Sites'
    URL_CAT = 'URL Categories'
    URL_CAT_EXTENDED = 'Top URL Categories - Extended'
    APP_VISIBILITY = 'Application Visibility'
    TOP_APP_TYPES = 'Top Application Types - Extended'
    ANTIMALWARE = 'Anti-Malware'
    MALWARE_RISK = 'Client Malware Risk'
    WBRS_FILTERS = 'Web Reputation Filters'
    L4TM = 'L4 Traffic Monitor'
    USER_LOCATION = 'Reports by User Location'
    SYSTEM_CAP = 'Web System Capacity'
    SYSTEM_CAP_OVERVIEW = 'System Capacity Overview'
    SOCKS_PROXY = 'SOCKS Proxy'
    MY_REPORTS = 'My Reports'
    AMP = 'Advanced Malware Protection'
    AMP_VERDICT_UPDATES = 'Advanced Malware Protection Verdict Updates'

class sma_status_type(object):
    """Constants for Appliance Status info type."""
    SYSTEM = 'basic'
    SERVICES = 'services'
    PROXY = 'proxy'
    AUTH = 'authentication'

class sma_fkeys(object):
    """Constants for Feature keys."""
    CENTR_EMAIL_REPORTING = 'c_rep_processing'
    CENTR_EMAIL_MSG_TRACKING = 'c_track_processing'
    CENTR_WEB_REPORTING = 'c_web_rep_processing'
    CENTR_WEB_CONFIG = 'iccm_processing'
    CLOUD_ADMIN = 'cloud'
    SPAM_QUARANTINE = 'master_isq'
