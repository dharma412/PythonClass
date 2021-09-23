#!/usr/bin/bash
# $Id $
# $DateTime $
# $Author $
#-----------------------------------------------------------------------------------------------------------------#
# Script to Launch Infra BATS from Jenkins
#
# The script requires the following ENV Variables
#   WSA: hostname of appliance attached to the node
#   SLICE_SERVER: hostname of the FreeBSD server attached to the node
#
# Required Arguments:
# 1. DUT_VERSION
# 2. One or more test suits to run
#-----------------------------------------------------------------------------------------------------------------#
# DO NETINSTALL of the Build. From the SARF Client of the SLOT
# And DO SSW on P1
#-----------------------------------------------------------------------------------------------------------------#
# Set up the Environment variables:
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export SARF_HOME=$DIR/../..
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH
export LD_LIBRARY_PATH=/usr/local/lib/firefox3/

#-----------------------------------------------------------------------------------------------------------------#
# Global Variables Definition
#-----------------------------------------------------------------------------------------------------------------#
NETINSTALL_REQUIRED="TRUE"
SUITE_NAME=infra
OUTPUT_DIR=$HOME/public_html/$SUITE_NAME
DUT=$WSA

# Version of AsyncOS on appliance is taken from first argument
DUT_VERSION=$1
shift

# common arguments to both netinstall and test suite commands
common_args=(
	--dut $DUT
	--variable WSA_VERSION:$DUT_VERSION
	--outputdir $OUTPUT_DIR
)
#-----------------------------------------------------------------------------------------------------------------#

# Setup script permissions and cleanup running processes (selenium, CFD Jobs, Python scripts)
chmod +x $SARF_HOME/bin/run/*.sh
ps auxww | grep -Ei "\-port|pybot_run|CSC.*sh|.*py" | awk '{print $2}' | xargs kill -9
python $DIR/clean_apache_logs.py $*

# clean the output directory, temp files
python $DIR/clean_sarf_output_folder.py $OUTPUT_DIR
$SARF_HOME/bin/run/clear_tmp.sh

# make ssh default to ipv4
$SARF_HOME/bin/run/make_ssh_default_to_inet.sh
#Configure client to prefer ipv4
sudo /etc/rc.d/ip6addrctl prefer_ipv4
# clean orphan processes
$DIR/delete_orphan_processes.sh

#-----------------------------------------------------------------------------------------------------------------#
# Script Execution: NETINSTALL
#-----------------------------------------------------------------------------------------------------------------#

# Check the slot if the resources required are running. If not, take the node offline
pybot  --variable DUT:$DUT  \
       --variable HTTP_SERVER:$SLICE_SERVER  \
       --variable BUILD:$WSA_VERSION \
       --variable BUILD_URL:$JOB_URL  \
       --variable SARF_HOME:$SARF_HOME  \
       --variable NODE:$NODE_NAME  \
       --variable JENKINS_URL:$JENKINS_URL  \
       --variable JOB_NAME:$JOB_NAME \
       --outputdir $OUTPUT_DIR  \
       --output check_pre_requisites.xml  \
       --report check_pre_requisites.report.html  \
       --log check_pre_requisites.log.html \
       --debugfile check_pre_requisites.debug  \
       $SARF_HOME/tests/common/check_pre_requisites.txt

# netinstall
flag=/tmp/netinstall_started

#Skip netinstall based on the customer input
if [ "$NETINSTALL_REQUIRED" != 'FALSE' ]
then
    #Netinstall for all WSA in a slot/slice
    $SARF_HOME/bin/pybot_run \
        --dut ${DUT} \
        --variable WSA_VERSION:$DUT_VERSION \
        --outputdir $OUTPUT_DIR \
        -v NETINST_FLAG:$flag \
        $SARF_HOME/tests/common/install_wsa_build_if_necessary.txt
fi

# Run the Test, if NetInstall result is PASS
if [ ! -e $flag ]
then
    $SARF_HOME/bin/pybot_run \
        ${common_args[*]} \
        #--listener $SARF_HOME/tools/DynamicAutoTriage/Listener.py 
        --output $SUITE_NAME.xml \
        --report $SUITE_NAME.report.html \
        --log $SUITE_NAME.log.html \
        --debugfile $SUITE_NAME.debug \
        --exclude skip* \
        $files \
        $@

    python $SARF_HOME/tools/django/copy_xml_to_db.py $OUTPUT_DIR

else
    echo "Netinstall failed. Suite $SUITE_NAME has not been run."
    exit $netinst
fi

# Disable ipv6 (call without parameters)
#$SARF_HOME/bin/run/enable_disable_ipv6.sh
sudo python $SARF_HOME/bin/run/backup_logs.py $JOB_NAME

#Check if WSA is not accessible and set slot status to offline. Run SSW on P1
$SARF_HOME/bin/pybot_run \
    --variable DUT:$DUT  \
    --variable HTTP_SERVER:$SLICE_SERVER  \
    --variable SARF_HOME:$SARF_HOME  \
    --variable NODE:$NODE_NAME  \
    --variable JENKINS_URL:$JENKINS_URL  \
    --outputdir $OUTPUT_DIR  \
    --output check_status.xml  \
    --report check_status.report.html  \
    --log check_status.log.html \
    --debugfile check_status.debug  \
    $SARF_HOME/tests/common/check_wsa_status.txt \
    $SARF_HOME/tests/coeus1170\unittests\cli\01__ssw.txt

# Clear the tmp files
$SARF_HOME/bin/run/clear_tmp.sh

#-----------------------------------------------------------------------------------------------------------------#
# Script Execution: RUN_INFRA_BATS
#-----------------------------------------------------------------------------------------------------------------#
# Set up the Environment variables: INFRA
# The tests are fired from KICK as an Execution Plan
DIR=workspace/infra/
export INFRA_HOME=$DIR
source $INFRA_HOME/bin/activate

# Setup script permissions and cleanup running processes (selenium, CFD Jobs, Python scripts)
chmod +x $INFRA_HOME/bin/*.sh

export DUT_P1=${DUT/./-p1.}
export DUT_IP_MGMT=`dig $DUT +short`
export DUT_IP_P1=`dig ${DUT_P1} +short`

export RTEST_USER=rtestuser
export RTEST_USER_PASSWORD=ironport
export ADMIN_USER=admin
export ADMIN_PASSWORD_SSW=Cisco1234\$
export CLIENT=${CLIENT}
export SNMP_SERVER=snmp.ibauto
export RPC_SERVER=${CLIENT}
export CLIENT_DEVICE_SNMP=${SNMP_SERVER}
export CLIENT_DEVICE_RPC=${RPC_SERVER}

#-----------------------------------------------------------------------------------------------------------------#
# Script Execution: PUBLISH_TEST_RESULTS
#-----------------------------------------------------------------------------------------------------------------#

#copy AppFault and SystemCore files to sarf output directory
BUILD_ID_NUMBER=`echo $WSA_VERSION | sed -E 's/coeus-//g'`


