#!/usr/local/bin/bash
# $Id $ 
# $DateTime $ 
# $Author $
#===========================================================#
# Common script for running test suites from Jenkins
# Required environment variables for Jenkins node
# configuration that is going to use this script:
#  - WSA: hostname of appliance attached to the node
#  - SLICE_SERVER: hostname of the FreeBSD server attached
#                  to the node
# Required Arguments:
# 1. SUITE_NAME
# 2. DUT_VERSION
# 3. PREVIOUS_RUN_LINK
# 4. One or more test suits to run
#===========================================================#
# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export SARF_HOME=$DIR/../..
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

#clear lingering selenium process
ps auxww | grep -Ei "\-port|pybot_run" | awk '{print $2}' | xargs kill -9

#Make all .sh scripts to execute
chmod +x $SARF_HOME/bin/run/*.sh

# Enable or disable ipv6 based on parameter ${INET_MODE}
#$SARF_HOME/bin/run/enable_disable_ipv6.sh $@

#===========================================================#
# Global Variables Definition
#===========================================================#
export LD_LIBRARY_PATH=/usr/local/lib/firefox3/

# name of the test suite is taken from first argument
SUITE_NAME=$1
# remove suite name from argument list
shift

# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/$SUITE_NAME

# Hostname of DUT is taken from second argument
DUT_1=$WSA

if [ $UPSTREAM_SERVER_A ]
then
    DUT_2=$UPSTREAM_SERVER_A
else
    DUT_2=$WSA2
fi

if [ $UPSTREAM_SERVER_B ]
then
    DUT_3=$UPSTREAM_SERVER_B
else
    DUT_3=$WSA3
fi

# Version of AsyncOS on applinace is taken from third argument
DUT_VERSION=$1
# remove version from argument list
shift

#Run the scrip to delete apache log files from HTTP_SERVER
python $DIR/clean_apache_logs.py $*

# Previous Run Link
if [[ $1 == http://* ]]
then
    echo "Preparing for re-run of failed test cases using $1"
    $SARF_HOME/bin/pybot_run --dut $DUT \
    -v link:$1 $SARF_HOME/tests/common/unittests/scp.txt
    python $SARF_HOME/tools/gather_failed_tests.py /tmp/output.xml /tmp/failed_tests.txt
    files="--argumentfile /tmp/failed_tests.txt"
    shift
fi

#===========================================================#
# Script Execution
#===========================================================#

# clean the sarf output directory
python $DIR/clean_sarf_output_folder.py $SARF_OUTPUT_DIR

# clean tmp directory
$SARF_HOME/bin/run/clear_tmp.sh

# make ssh default to ipv4
$SARF_HOME/bin/run/make_ssh_default_to_inet.sh

#Configure client to prefer ipv4
sudo /etc/rc.d/ip6addrctl prefer_ipv4

#clean orphan processes
$DIR/delete_orphan_processes.sh

#Check and make slot offline it needed
pybot  --variable DUT:$DUT_1  \
       --variable SARF_HOME:$SARF_HOME  \
       --variable NODE:$NODE_NAME  \
       --variable JENKINS_URL:$JENKINS_URL  \
       --outputdir $SARF_OUTPUT_DIR  \
       --output check_status.xml  \
       --report check_status.report.html  \
       --log check_status.log.html \
       --debugfile check_status.debug  \
       $SARF_HOME/tests/common/check_wsa_status.txt

# common arguments to both netinstall and test suite commands
common_args=(
	--dut $DUT_1
	--variable WSA_VERSION:$DUT_VERSION
	--outputdir $SARF_OUTPUT_DIR
)

# Generate & Backup Threat Grid(TG) API Key from WSA
$SARF_HOME/bin/pybot_run \
             --dut ${DUT_1} \
             --variable WSA_VERSION:$DUT_VERSION \
             --outputdir $SARF_OUTPUT_DIR \
             $SARF_HOME/tests/common/get_analysis_key.txt


# netinstall
flag=/tmp/netinstall_started

#Netinstall for all WSA in a slot/slice
for NU in 1 2 3
do
DUT=DUT_$NU
if [ ${!DUT} ]
then
    $SARF_HOME/bin/pybot_run \
             --dut ${!DUT} \
             --variable WSA_VERSION:$DUT_VERSION \
             --outputdir $SARF_OUTPUT_DIR \
             -v NETINST_FLAG:$flag \
             $SARF_HOME/tests/common/install_wsa_build.txt
fi
done

# test suite will be run only if netinstall passed
if [ ! -e $flag ]
then
    # Restore Threat Grid(TG) API Key to WSA
    python $DIR/copy_tg_apikey.py $DUT_1 restore_apikey

    #Clear apache logs and contents of tmp directory
    $SARF_HOME/bin/pybot_run \
        ${common_args[*]} \
        $SARF_HOME/tests/common/clear_apache_logs.txt

    $SARF_HOME/bin/pybot_run \
	${common_args[*]} \
	--output $SUITE_NAME.xml \
	--report $SUITE_NAME.report.html \
	--log $SUITE_NAME.log.html \
	--debugfile $SUITE_NAME.debug \
	--exclude skip* \
	$files \
	$@
    python $SARF_HOME/tools/django/copy_xml_to_db.py $SARF_OUTPUT_DIR
    $SARF_HOME/bin/pybot_run \
        ${common_args[*]} \
        -v collect_output:$SARF_OUTPUT_DIR/collect.tar.gz \
        tests/common/useful_scripts/collect_logs.txt
else
    echo "Netinstall failed. Suite $SUITE_NAME has not been run."
    exit $netinst
fi

# Disable ipv6 (call without parameters)
#$SARF_HOME/bin/run/enable_disable_ipv6.sh
sudo python $SARF_HOME/bin/run/backup_logs.py $JOB_NAME
