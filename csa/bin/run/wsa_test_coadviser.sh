#!/usr/local/bin/bash
# $Id $
# $DateTime $
# $Author $
#===========================================================#
# Script to launch coad Tests from Jenkins
# Required Arguments:
# 1.  –w 172.29.186.54                |    WSA IP
# 2. –m pethanga@cisco.com    |    Mail to user
# 3.  –u bvt                                |    User
#===========================================================#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export SARF_HOME=$DIR/../..
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH
export SARF_HOME=~/work/sarf

#Make all .sh scripts to execute
chmod +x $SARF_HOME/bin/run/*.sh
#clear lingering selenium process
ps auxww | grep -Ei "\-port|pybot_run" | awk '{print $2}' | xargs kill -9

export LD_LIBRARY_PATH=/usr/local/lib/firefox3/

# name of the test suite is taken from first argument
SUITE_NAME=$1
# remove suite name from argument list
shift

# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/$SUITE_NAME

# Hostname of DUT is taken from second argument
DUT=$WSA

# Version of AsyncOS on applinace is taken from third argument
DUT_VERSION=$1
# remove version from argument list
shift
set EMAIL_ID=$1
shift
set USER_ID=$1
shift
echo "Variables: Suite: $SUITE_NAME | DUT: $DUT | EMail ID: $EMAIL_ID | User ID: $USER_ID"
#===========================================================#
# Global Variables Definition
#===========================================================#
# clean /tmp directory
sudo rm -rf /tmp/*
# netinstall
flag=/tmp/netinstall_started

#Netinstall for all WSA in a slot/slice
if [ ${WSA} ]
then
    echo "COAD TEST: Installing WSA Build if needed. | WSA Version: $DUT_VERSION"
    $SARF_HOME/bin/pybot_run \
             --dut ${WSA} \
             --variable WSA_VERSION:$DUT_VERSION \
             --outputdir ~/public_html/wsa_qa \
             -v NETINST_FLAG:$flag \
             $SARF_HOME/tests/common/install_wsa_build_if_necessary.txt
fi

# test suite will be run only if netinstall passed
if [ ! -e $flag ]
then

# common arguments to both netinstall and test suite commands
    common_args=(
        --dut $DUT
        --variable WSA_VERSION:$DUT_VERSION
        --outputdir $SARF_OUTPUT_DIR
        # Use new environment file so that the Tools server is not over consumed
        --variablefile $SARF_HOME/variables/environment/bat_wga_lab.py
    )

    #Run the Coad Tests
    echo "COAD TEST: Starting the run..."
    echo "Parameters: EMail> $EMAIL_ID | UserID: $USER_ID"

    $SARF_HOME/bin/pybot_run \
    ${common_args[*]}                \
    -v EMAIL_ID:$EMAIL_ID         \
    -v USER_ID:$USER_ID             \
    --exclude skip*                     \
    $files \
    $@
else
    echo "COAD TEST: Netinstall failed. Coad Tests have not been run. Please check the logs @ ~/public_html/wsa_qa/"
    exit
fi
