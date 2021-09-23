# $Id: //prod/main/sarf_centos/testlib/common/util/check_node.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import sys
from common.util.systools import SysTools
from common.util.jenkins_nodes import JenkinsNodes


def main(dic={}):
    errors = 0
    for key in dic.keys():
        print key, dic[key]
        try:
            SysTools(key, None).wait_until_dut_is_accessible(timeout=3, wait_for_ports=dic[key])
        except:
            errors += 1
    if errors > 0:
        print errors, 'errors detected'

    sys.exit(errors)


if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) != 2:
        raise Exception('Usage: python check_node <node_name>')
    dic = JenkinsNodes().nodes[sys.argv[1]]
    if not isinstance(dic, dict):
        raise Exception('invalid node ' + sys.argv[1])
    main(dic)
