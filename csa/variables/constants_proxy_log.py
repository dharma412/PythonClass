# $Id: //prod/main/sarf_centos/variables/constants_proxy_log.py#1 $
class proxy_log:
    """
    Constants related to file proxy_log
    """
    LOCATION = '/data/pub/proxylogs/proxyerrlog.current'

    TIMESTAMP = "-E \'^({VALUE})'",
    LOG_LEVEL = "-E -i '^(?[^ ]* +){5}({VALUE}){COLON}'",
    MODULE = "-E -i \'^(?[^{COLON}]*{COLON}){3} ({VALUE})'",
    TRANSACTION = "-E -i \'^(?[^{COLON}]*{COLON}){4} ({VALUE}) '",
    MESSAGE = "-E -i \'^(?[^{COLON}]*{COLON}){5} .*({VALUE})'",

