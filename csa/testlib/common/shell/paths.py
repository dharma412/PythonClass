#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/common/shell/paths.py#2 $

"""
This module incorporates product filesystem paths.
A lot of utilities/tests want to know the directory layout to provide more
effective testing
"""
__revision = '$Revision: #2 $'
from sal.containers import cfgholder
from sal.containers.pathsholder import PathsHolder


def get_paths():
    paths = cfgholder.CfgHolder()

    paths.reporting_dir = PathsHolder(base='/data/pub/reporting/')
    paths.reporting_db_dir = PathsHolder(base='/data/db/reporting/db/')

    paths.counters_dir = PathsHolder( \
        base='/data/db/reporting/counters/current/')

    paths.lib_dir = PathsHolder(base='/data/lib/')

    paths.lib_pycbox = PathsHolder(base='/data/lib/pycbox/')
    paths.core_dumps = PathsHolder(base='/data/cores/')
    paths.binary_home = PathsHolder(base='/data/bin/', files={
        'heimdall_svc': 'heimdall_svc',
    })
    paths.config_home = PathsHolder(base='/data/db/config/')
    paths.heimdall_logs = PathsHolder(base='/data/log/heimdall/', files={
        'hermes': 'hermes/hermes.current',
        'heimdall': 'heimdall/heimdall.current',
        'wbrsd': 'wbrsd/wbrsd.current',
    })
    paths.stdout_logs = PathsHolder(base='/data/log/stdout/', files={
        'stdout_heimdall': 'stdout_heimdall.log',
    })
    paths.third_party_home = PathsHolder(base='/data/third_party/')
    paths.user_config = PathsHolder(base='/data/pub/configuration/')
    paths.user_logs = PathsHolder(base='/data/pub/', files={
        'accesslogs': 'accesslogs/aclog.current',
        'bypasslogs': 'bypasslogs/tmon_bypass.current',
        'configdefragd': 'configdefragd_logs/configdefragd_log.current',
        'gui': 'gui_logs/gui.current',
        'mcafee': 'mcafee_logs/mcafee_log.current',
        'proxylogs': 'proxylogs/proxyerrlog.current',
        'authlogs': 'authlogs/authlog.current',
        'haystackd': 'haystackd_logs/haystackd.current',
        'reportd': 'reportd_logs/reportd.current',
        'reportqueryd': 'reportqueryd_logs/reportqueryd.current',
        'smad': 'smad_logs/smad.current',
        'status': 'status/status.log.current',
        'system': 'system_logs/system.current',
        'updater': 'updater_logs/updater_log.current',
        'smartlicense': 'smartlicense/smartlicense.current',
        'wbnp': 'wbnp_logs/wbnp_log.current',
        'wbrs': 'wbrs_logs/wbrs_log.current',
        'webcat': 'webcat_logs/webcat_log.current',
        'webroot': 'webrootlogs/webrootlog.current',
        'welcomeack': 'welcomeack_logs/welcomeack_log.current',
        'trackstats': 'track_stats/prox_track.log',
    })
    paths.captures = PathsHolder(base='/data/pub/captures/')
    paths.eun_pages = PathsHolder(base='/data/db/eun/')

    return paths
