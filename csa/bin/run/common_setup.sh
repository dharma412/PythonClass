# $Id: //prod/main/sarf_centos/bin/run/common_setup.sh#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

#===========================================================#
# This is common setup script. All common steps for other test suites
# are done here
# This needs to be sourced in the main script as
# . common_setup.sh
#===========================================================#

export LD_LIBRARY_PATH=/usr/local/lib/firefox3/
export SARF_HOME=$HOME/work/sarf
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

# clean output directory
rm -rf $SARF_OUTPUT_DIR/*

# clean tmp directory
sudo rm -rf /var/tmp/customProfileDir*

# Verifies that there are no failed tests in runned suite
# and exits the script if such tests exist
# Parameters:
# - $1: path to xml result file
# - $2: fail error message text
function verify_pybot_result {
    result=1
    if [[ -f $1 ]]; then
        result=`awk -F '"' '/All Tests/ {print $2}' $1`
    fi
    if [[ $result -ne 0 ]]; then
        echo "$2" 1>&2
        exit 1
    fi
}

