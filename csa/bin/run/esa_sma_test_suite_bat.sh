#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Common script for running test suites from Jenkins
# Required environment variables for Jenkins node
# configuration that is going to use this script:
#  - SMA: hostname of SMA appliance attached to the node
#  - ESA: hostname of ESA appliance attached to the node
# Required Arguments:
# 1. SUITE_NAME
# 2. SMA_DUT_VERSION (actually, version of SMA under test in format x.x.x-xxx)
# 3. SMA_PREV_FCS_VERSION (version of the last SMA FCS build in format x.x.x-xxx)
# 3. ESA_DUT_VERSION (version of the current ESA FCS build in format x.x.x-xxx)
# 4. ESA_PREV_FCS_VERSION (version of the previous ESA FCS build in format x.x.x-xxx)
# 6. LAB_VARS_FILE (Name of a file containing server names for particular lab.
#    This file should be located in $SARF_HOME/variables/environment
#    folder)
# 7. One or more test suits to run
#===========================================================#
# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export SARF_HOME=$DIR/../..

# Enable or disable ipv6 based on parameter ${INET_MODE}
$SARF_HOME/bin/run/enable_disable_ipv6.sh $@

#===========================================================#
# Global Variables Definition
#===========================================================#
# name of the test suite is taken from first argument
SUITE_NAME=$1
# remove this param from argument list
shift
SMA_DUT_VERSION=$1
shift
SMA_PREV_FCS_VERSION=$1
shift
ESA_DUT_VERSION=$1
shift
ESA_PREV_FCS_VERSION=$1
shift
LAB_VARS_FILE=$1
shift

# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/$SUITE_NAME

# Hostnames are taken from the Jenkins environment
SMA_DUT=$SMA
SMA2_DUT=$SMA2
ESA_DUT=$ESA

#===========================================================#
# Script Execution
#===========================================================#

# Source common_setup.sh
. $DIR/common_setup.sh


# common arguments to both netinstall and test suite commands
common_args=(
    --outputdir $SARF_OUTPUT_DIR
    --variablefile $SARF_HOME/variables/environment/$LAB_VARS_FILE
    --variablefile $SARF_HOME/variables/error_log_branches/zeus.py
)
SMA_TEST_DIR=zeus${SMA_DUT_VERSION:0:1}${SMA_DUT_VERSION:2:1}


#===========================================================#
# Common Setup
#===========================================================#

## Netinstall ESA and SMA in parallel
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut=$ESA_DUT \
    --variable ESA_VERSION:$ESA_PREV_FCS_VERSION \
    $SARF_HOME/tests/common/install_esa_build.txt &
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut=$SMA_DUT \
    --variable SMA_VERSION:$SMA_PREV_FCS_VERSION \
    $SARF_HOME/tests/common/install_sma_build.txt &
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut=$SMA2_DUT \
    --variable SMA_VERSION:$SMA_DUT_VERSION \
    $SARF_HOME/tests/common/install_sma_build.txt &
wait
verify_pybot_result \
    $SARF_OUTPUT_DIR/install_esa_build.xml \
    "ESA netinstall failed. Suite $SUITE_NAME has not been run."
verify_pybot_result \
    $SARF_OUTPUT_DIR/install_sma_build.xml \
    "SMA netinstall failed. Suite $SUITE_NAME has not been run."
## Perform after-netinstall preconfiguration, ignore result verification
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut=$SMA_DUT \
    --dut=$ESA_DUT \
    $SARF_HOME/tests/$SMA_TEST_DIR/build_acceptance_tests/esa_sma_common_setup/after_netinstall.txt

## Upgrade ESA and SMA in parallel
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut=$ESA_DUT \
    --variable ESA_VERSION:$ESA_DUT_VERSION \
    $SARF_HOME/tests/$SMA_TEST_DIR/build_acceptance_tests/esa_sma_common_setup/upgrade_esa_build.txt &
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut=$SMA_DUT \
    --variable SMA_VERSION:$SMA_DUT_VERSION \
    $SARF_HOME/tests/$SMA_TEST_DIR/build_acceptance_tests/esa_sma_common_setup/upgrade_sma_build.txt &
wait
verify_pybot_result \
    $SARF_OUTPUT_DIR/upgrade_esa_build.xml \
    "ESA upgrade failed. Suite $SUITE_NAME has not been run."
verify_pybot_result \
    $SARF_OUTPUT_DIR/upgrade_sma_build.xml \
    "SMA upgrade failed. Suite $SUITE_NAME has not been run."
## Perform after-upgrade preconfiguration, ignore result verification
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut=$SMA_DUT \
    --dut=$ESA_DUT \
    $SARF_HOME/tests/$SMA_TEST_DIR/build_acceptance_tests/esa_sma_common_setup/after_upgrade.txt
#===========================================================#
# Common Setup Finished
#===========================================================#

## Test suite will run only if setup is passed
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut=$SMA_DUT \
    --dut=$ESA_DUT \
    --dut=$SMA2_DUT \
    --variable SMA_VERSION:$SMA_DUT_VERSION \
    --output $SUITE_NAME.xml \
    --report $SUITE_NAME.report.html \
    --log $SUITE_NAME.log.html \
    --debugfile $SUITE_NAME.debug \
    --exclude skip* \
    $@
export PYTHONPATH=$PYTHONPATH:$SARF_HOME/testlib
python $SARF_HOME/tools/django/copy_xml_to_db.py $SARF_OUTPUT_DIR

# Disable ipv6 (call without parameters)
$SARF_HOME/bin/run/enable_disable_ipv6.sh

