# $Id: //prod/main/sarf_centos/testlib/common/util/jenkins_nodes.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

class JenkinsNodes():
    wsa_ports = '8080, 22'
    sma_ports = '80, 22'
    http_server = '80,22'
    client = '22'

    nodes = {
        'IPv6_slice11': {
            'wsa011.wga': wsa_ports,
            'wsa070.wga': wsa_ports,
            'wsa071.wga': wsa_ports,
            'vm10bsd0088.wga': client,
            'vm10bsd0224.wga': http_server,
            'vm10bsd0251.wga': client,
            'vm10bsd0252.wga': client,
            'vm10bsd0300.wga': client,
        },
        'IPv6_slice12': {
            'wsa012.wga': wsa_ports,
            'vm10bsd0180.wga': client,
            'vm10bsd0225.wga': http_server,
        },
        'IPv6_slice13': {
            'wsa013.wga': wsa_ports,
            'vm10bsd0181.wga': client,
            'vm10bsd0226.wga': http_server,
        },
        'IPv6_slice21': {
            'wsa021.wga': wsa_ports,
            'vm10bsd0228.wga': client,
            'vm10bsd0234.wga': http_server,
            'vm10bsd0301.wga': client,
            'vm10bsd0302.wga': client,
        },
        'IPv6_slice22': {
            'wsa022.wga': wsa_ports,
            'vm10bsd0229.wga': client,
            'vm10bsd0235.wga': http_server,
        },
        'IPv6_slice23': {
            'wsa023.wga': wsa_ports,
            'vm10bsd0230.wga': client,
            'vm10bsd0236.wga': http_server,
        },
        'IPv6_slice24': {
            'wsa024.wga': wsa_ports,
            'vm10bsd0231.wga': client,
            'vm10bsd0237.wga': http_server,
        },
        'IPv6_slice32': {
            'wsa032.wga': wsa_ports,
            'wsa033.wga': wsa_ports,
            'm670w01.wga': sma_ports,
            'm670w02.wga': sma_ports,
            'vm10bsd0255.wga': client,
            'vm10bsd0258.wga': http_server,
        },
        'IPv6_slice34': {
            'wsa034.wga': wsa_ports,
            'm670w03.wga': sma_ports,
            'vm10bsd0257.wga': client,
            'vm10bsd0260.wga': http_server,
        },
        'IPv6_slice36': {
            'wsa036.wga': wsa_ports,
            'vm10bsd0276.wga': client,
            'vm10bsd0278.wga': http_server,
        },
        'IPv6_slice37': {
            'wsa037.wga': wsa_ports,
            'vm10bsd0277.wga': client,
            'vm10bsd0279.wga': http_server,
        },
        'IPv6_slice69': {
            'wsa069.wga': wsa_ports,
            'vm10bsd0319.wga': client,
            'vm10bsd0320.wga': http_server,
        },
        'IPv6_slice74': {
            'wsa074.wga': wsa_ports,
            'vm10bsd0335.wga': client,
            #            'vm10bsd0237.wga':http_server,
        },
        'IPv6_slice75': {
            'wsa075.wga': wsa_ports,
            'vm10bsd0336.wga': client,
            #            'vm10bsd0237.wga':http_server,
        },
        'IPv6_slice79': {
            'wsa079.wga': wsa_ports,
            'vm10bsd0037.wga': client,
            'vm10bsd0038.wga': http_server,
        },
        'IPv6_slice81': {
            'wsa081.wga': wsa_ports,
            'vm10bsd0345.wga': client,
            'vm10bsd0346.wga': http_server,
        },
    }
