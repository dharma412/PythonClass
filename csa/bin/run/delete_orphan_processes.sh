# $Id: //prod/main/sarf_centos/bin/run/delete_orphan_processes.sh#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

echo deleting orphan processes
ps auxww| grep pybot_run | grep -v grep| awk '{print $2}' | sudo xargs kill -9
