#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Common script for running test suites from Jenkins
# Required environment variables for Jenkins node
# configuration that is going to use this script:
#  - ESA: hostname of ESA appliance attached to the node
# Required Arguments:
# 1. SUITE_NAME
# 2. ESA_DUT_VERSION (version of the current ESA FCS build in format x.x.x-xxx)
# 3. LAB_VARS_FILE (Name of a file containing server names for particular lab.
#    This file should be located in $SARF_HOME/variables/environment
#    folder)
# 4. One or more test suites to run.
#===========================================================#
# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export SARF_HOME=$DIR/../..

#===========================================================#
# Global Variables Definition
#===========================================================#

# name of the test suite is taken from first argument
SUITE_NAME=$1
# remove this param from argument list
shift
ESA_DUT_VERSION=$1
shift
LAB_VARS_FILE=$1
shift
ESA_TEST_DIR=$1

# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/$SUITE_NAME

# Hostnames are taken from the Jenkins environment
ESA_DUT=$ESA
PRE_UPGRADE_SUITE_NAME=pre_upgrade

#===========================================================#
# Script Execution
#===========================================================#

# Source common_setup.sh
. $DIR/common_setup.sh

# common arguments to both netinstall and test suite commands
common_args=(
    --outputdir $SARF_OUTPUT_DIR
    --variablefile $SARF_HOME/variables/environment/$LAB_VARS_FILE
    --variablefile $SARF_HOME/variables/error_log_branches/phoebe.py
)

#===========================================================#
# Netinstall ESA if required 
#===========================================================#

## Netinstall current ESA build
if [ $SKIP_ESA_NETINSTALL == false ]
then
    echo "=============================================================================="
    echo " * INFO: Starting ESA Netinstall on build $ESA_DUT_VERSION"
    echo "=============================================================================="
    $SARF_HOME/bin/pybot_run \
        ${common_args[*]} \
        --dut=$ESA_DUT \
        --variable ESA_VERSION:$ESA_DUT_VERSION \
        $SARF_HOME/tests/common/install_esa_build.txt &
else
    echo "=============================================================================="
    echo " * INFO: ESA Netinstall Skipped"
    echo "=============================================================================="
fi

wait

if [ $SKIP_ESA_NETINSTALL == false ]
then
    verify_pybot_result \
        $SARF_OUTPUT_DIR/install_esa_build.xml \
        "ESA netinstall failed. Suite $SUITE_NAME has not been run."
fi

## Test suite will run only if Netinstall passed
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut-type-main=ESA \
    --dut=$ESA_DUT \
    --output $SUITE_NAME.xml \
    --report $SUITE_NAME.report.html \
    --log $SUITE_NAME.log.html \
    --debugfile $SUITE_NAME.debug \
    --exclude skip* \
    --exclude $PRE_UPGRADE_SUITE_NAME \
    --include autobat \
    $@
export PYTHONPATH=$PYTHONPATH:$SARF_HOME/testlib
python $SARF_HOME/tools/django/copy_xml_to_db.py $SARF_OUTPUT_DIR
