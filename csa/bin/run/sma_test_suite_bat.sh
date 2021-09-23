#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Common script for running test suites from Jenkins
# Required environment variables for Jenkins node
# configuration that is going to use this script:
#  - SMA: hostname of appliance attached to the node
#  - SLICE_SERVER: hostname of the FreeBSD server attached
#                  to the node
# Required Arguments:
# 1. SUITE_NAME
# 2. DUT_VERSION
# 3. One or more test suits to run
#===========================================================#
# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export SARF_HOME=$DIR/../..
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

# Enable or disable ipv6 based on parameter ${INET_MODE}
$SARF_HOME/bin/run/enable_disable_ipv6.sh $@

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
DUT=$SMA

# Version of AsyncOS on applinace is taken from third argument
DUT_VERSION=$1
# remove version from argument list
shift

#===========================================================#
# Script Execution
#===========================================================#

# clean output directory
rm -rf $SARF_OUTPUT_DIR/*
# clean tmp directory
sudo rm -rf /var/tmp/customProfileDir*

# clean orphan processes
$DIR/delete_orphan_processes.sh

# common arguments to both netinstall and test suite commands
common_args=(
	--dut $DUT
	--variable SMA_VERSION:$DUT_VERSION
	--outputdir $SARF_OUTPUT_DIR
)

# netinstall
$SARF_HOME/bin/pybot_run \
	${common_args[*]} \
	$SARF_HOME/tests/common/install_sma_build.txt

# test suite will be run only if netinstall passed
if [ $? = 0 ]
then
    $SARF_HOME/bin/pybot_run \
	${common_args[*]} \
	--output $SUITE_NAME.xml \
	--report $SUITE_NAME.report.html \
	--log $SUITE_NAME.log.html \
	--debugfile $SUITE_NAME.debug \
	--exclude skip* \
	$@
    python $SARF_HOME/tools/django/copy_xml_to_db.py $SARF_OUTPUT_DIR
    $SARF_HOME/bin/pybot_run \
        ${common_args[*]} \
        -v collect_output:$SARF_OUTPUT_DIR/collect.tar.gz \
        tests/common/useful_scripts/collect_logs.txt
else
    echo "Netinstall failed. Suite $SUITE_NAME has not been run."
    exit 1
fi

# Disable ipv6 (call without parameters)
$SARF_HOME/bin/run/enable_disable_ipv6.sh