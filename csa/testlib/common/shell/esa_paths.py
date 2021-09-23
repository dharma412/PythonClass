#!/usr/bin/python
"""
This module incorporates product filesystem paths.
A lot of utilities/tests want to know the directory layout to provide more
effective testing
"""

from sal.containers import cfgholder
from sal.containers.pathsholder import PathsHolder


def get_paths():

    paths = cfgholder.CfgHolder()

    paths.tracking_dir = PathsHolder(base='/data/pub/export/tracking/')

    paths.reporting_dir = PathsHolder(base='/data/pub/reporting/')
    paths.reporting_db_dir = PathsHolder(base='/data/db/reporting/db/')

    paths.slbl_dir = PathsHolder(base='/data/pub/slbl_db/')

    paths.counters_dir = PathsHolder( \
                                  base='/data/db/reporting/counters/current/')

    paths.lib_dir = PathsHolder(base='/data/lib/')

    paths.lib_pycbox = PathsHolder(base='/data/lib/pycbox/')
    paths.core_dumps = PathsHolder(base='/data/cores/')
    paths.binary_home = PathsHolder(base='/data/bin/', files={
        'heimdall_svc'      : 'heimdall_svc',
        'command_client'    : 'command_client'
    })
    paths.config_home = PathsHolder(base='/data/db/config/')
    paths.etc_home = PathsHolder(base='/data/etc/', files={
       'qabackdoor'        : 'rc.d/qabackdoor.sh',
    })
    paths.heimdall_logs = PathsHolder(base='/data/log/heimdall/', files={
        'csa'               : 'csa/csa.current',
        'eaas_app'          : 'eaas/eaas.current',
        'hermes'            : 'hermes/hermes.current',
        'heimdall'          : 'heimdall/heimdall.current',
        'heimdall_amp'      : 'amp/amp.current',
        'heimdall_gui'      : 'gui/gui.current',
        'sds'               : 'sds_client/sds_client.current',
        'heimdall_dlp_poleng'  : 'dlp_poleng/dlp_poleng.current',
        'heimdall_commandd'  : 'commandd/commandd.current',
        'heimdall_updaterd'  : 'updaterd/updaterd.current',
        'heimdall_url_rep_client'  : 'url_rep_client/url_rep_client.current',
        'heimdall_csn'       : 'csn/csn.current',
        'heimdall_journal_transformer' : 'kronos/kronos.current',
        'heimdall_beaker_connector'  :  'beaker_connector/beaker_connector.current',
        'heimdall_sse_connectord'  :  'sse_connectord/sse_connectord.current',
    })
    paths.stdout_logs = PathsHolder(base='/data/log/stdout/', files={
        'stdout_brightmail' : 'stdout_brightmail.log',
        'stdout_hermes'     : 'stdout_hermes.log',
        'stdout_mcafee'     : 'stdout_mcafee.log',
        'stdout_sophos'     : 'stdout_sophos.log',
        'stdout_thirdparty' : 'stdout_thirdparty.log',
    })
    paths.third_party_home = PathsHolder(base='/data/third_party/')
    paths.user_config = PathsHolder(base='/data/pub/configuration/')
    paths.user_logs = PathsHolder(base='/data/pub/', files={
        'antispam'          : 'antispam/antispam.current',
        'antivirus'         : 'antivirus/antivirus.current',
        'amp_logs'          : 'amp/amp.current',
        'asarchive'         : 'asarchive/antispam_archive.mbox.current',
        'audit_logs'        : 'audit_logs/audit_logs.current',
        'avarchive'         : 'avarchive/antivirus_archive.mbox.current',
        'beaker_client'     : 'beaker_client/beaker_client.current',
        'bounces'           : 'bounces/bounces.text.current',
        'brightmail'        : 'brightmail/brightmail.current',
        'case'              : 'case/case.current',
        'csa_logs'          : 'csa/csa.current',
        'encryption'        : 'encryption/encryption.current',
        'euq'               : 'euq_logs/euq.current',
        'euqgui'            : 'euqgui_logs/euqgui.current',
        'eaas'              : 'eaas/eaas.current',
        'gui'               : 'gui_logs/gui.current',
        'mail'              : 'mail_logs/mail.current',
        'status'            : 'status/status.log.current',
        'system'            : 'system_logs/system.current',
        'trackerd'          : 'trackerd_logs/trackerd.current',
        'reportd'           : 'reportd_logs/reportd.current',
        'reportqueryd'      : 'reportqueryd_logs/reportqueryd.current',
        'updater'           : 'updater_logs/updater_log.current',
        'smartlicense'      : 'smartlicense/smartlicense.current',
        'sntpd'             : 'sntpd_logs/sntpd.current',
        'scanning'          : 'scanning/scanning.text.current',
        'repeng'            : 'repeng/repeng.current',
        'ftpd'              : 'ftpd_logs/ftpd.current',
        'error'             : 'error_logs/errors.current',
        'crash_archive'     : 'crash_archive/crash.current',
        'authentication'    : 'authentication/authentication.current',
        'cli'               : 'cli_logs/cli.current',
        'slbld'             : 'slbld_logs/slbld.current',
        'web_client'        : 'web_client/web_client.current',
        'service_logs'      : 'service_logs/service_logs.current',
        'url_rep_client'    : 'url_rep_client/url_rep_client.current',
        'ipr_client'        : 'ipr_client/ipr_client.current',
        'threatfeeds'       : 'threatfeeds/threatfeeds.current',
        'mar'               : 'mar/mar.current',
        'remediation'       : 'remediation/remediation.current',
        'ipblockd'          : 'ipblockd_logs/ipblockd.current',
        'smtp_conversation' : 'smtp_conversation/smtp_conversation.current',
        'csn_logs'          : 'csn_logs/csn_logs.current',
        'ctr_logs'          : 'ctr_logs/ctr_logs.current',
        'slld'              : 'slld/sll.current',
        'content_scanner'   : 'content_scanner/content_scanner.current', 
        'easy_pov'          : 'easy_pov/easy_pov.current',
    })
    paths.captures_dir = PathsHolder(base='/data/pub/captures/')

    return paths
