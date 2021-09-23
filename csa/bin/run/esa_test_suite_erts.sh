#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Common script for running erts test suites from Jenkins
# Required environment variables for Jenkins node
# configuration that is going to use this script:
#  - ESA: hostname of ESA appliance attached to the node
# Required Arguments:
# 1. SUITE_NAME
# 2. ESA_DUT_VERSION (version of the current ESA build in format x.x.x-xxx)
# 3. SMA_DUT_VERSION (version of the SMA FCS build in format x.x.x-xxx)
# 4. LAB_VARS_FILE (Name of a file containing server names for particular lab.
#    This file should be located in $SARF_HOME/variables/environment
#    folder)
# 5. One or more test suits to run
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
ESA_DUT_VERSION=$1
shift
SMA_DUT_VERSION=$1
shift
LAB_VARS_FILE=$1
shift

# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/$SUITE_NAME

# Hostnames are taken from the Jenkins environment
ESA_DUT=$ESA
SMA_DUT=$SMA
ESA2_DUT=$ESA2
SMA2_DUT=$SMA2

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
ESA_TEST_DIR=phoebe${ESA_DUT_VERSION:0:1}${ESA_DUT_VERSION:2:1}
SMA_TEST_DIR=zeus${SMA_DUT_VERSION:0:1}${SMA_DUT_VERSION:2:1}

#===========================================================#
# Common Setup
#===========================================================#

install_variables=(
    $ESA_DUT:ESA_VERSION:$ESA_DUT_VERSION:esa
    $ESA2_DUT:ESA_VERSION:$ESA_DUT_VERSION:esa
    $SMA_DUT:SMA_VERSION:$SMA_DUT_VERSION:sma
    $SMA2_DUT:SMA_VERSION:$SMA_DUT_VERSION:sma
)
## Netinstall DUTs
for var in "${install_variables[@]}"
do
    var_array=(`echo "$var" | tr ":" "\n"`)
    $SARF_HOME/bin/pybot_run \
        ${common_args[*]} \
        --dut=${var_array[0]} \
        --variable ${var_array[1]}:${var_array[2]} \
        --output install_${var_array[3]}_${var_array[1]}_build.xml \
        $SARF_HOME/tests/common/install_${var_array[3]}_build.txt &
done
wait

for var in "${install_variables[@]}"
do
    var_array=(`echo "$var" | tr ":" "\n"`)

    verify_pybot_result \
        $SARF_OUTPUT_DIR/install_${var_array[3]}_${var_array[1]}_build.xml \
        "${var_array[3]} netinstall failed. Suite $SUITE_NAME has not been run."

done

#===========================================================#
# Common Setup Finished
#===========================================================#

## Test suite will run only if setup is passed
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    --dut-type-main=ESA \
    --dut=$ESA_DUT \
    --dut=$SMA_DUT \
    --dut=$ESA2_DUT \
    --dut=$SMA2_DUT \
    --output $SUITE_NAME.xml \
    --report $SUITE_NAME.report.html \
    --log $SUITE_NAME.log.html \
    --debugfile $SUITE_NAME.debug \
    --exclude skip* \
    --suitestatlevel 2 \
    --tagstatinclude erts \
    --include erts \
    --exclude virtual \
    --exclude mode_ipv6 \
    $@
python $SARF_HOME/tools/django/copy_xml_to_db.py $SARF_OUTPUT_DIR

# Disable ipv6 (call without parameters)
$SARF_HOME/bin/run/enable_disable_ipv6.sh
