#!/usr/local/bin/bash
# $Id: //prod/main/sarf_centos/bin/run/esa_test_suite_run_yourself.sh#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

#==========================================================================#
# Shell script for running test specific suites (eg: srts/erts/fat etc)
# from Jenkins for single/multiple modules (eg: alerts,bounce,dns etc).
#
# Required Arguments:
# 1. LAB_VARS_FILE (Name of a file containing server names for particular lab.
#    This file should be located in $SARF_HOME/variables/environment
#    folder)
#
# Following parameters will be picked up from Jenkins job:
# 1.  ESA_DUT       : ESA hostname.
# 2.  ESA_VERSION   : Version on which ESA will be netinstalled (if required).
# 3.  SMA_DUT       : SMA hostname.
# 4.  SMA_VERSION   : Version on which SMA will be netinstalled (if required).
# 5.  NETINSTALL_ESA: Whether to netinstall ESA or not.
# 6.  REQUIRE_SMA   : Is SMA required for suites execution.
# 7.  NETINSTALL_SMA: Whether to netinstall SMA or not.
# 8.  TEST_DIR      : Complete path from which test modules will be picked up.
# 9.  SUITE_NAME    : Name of the suites to be executed (srts/erts/fat/TIMS_IDs)
# 10. MODULES       : Test module names (eg: alerts/bounce/dns/hat etc.)
#===========================================================================#

# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export SARF_HOME=$DIR/../..

#===========================================================#
# Global Variables Definition
#===========================================================#

LAB_VARS_FILE=$1
shift

# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/$BUILD_NUMBER

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
dut_args=()

#===========================================================#
# Netinstall ESA or SMA if required
#===========================================================#

## Netinstall ESA on the given build
if [ ! -z "$ESA_DUT" -a "$ESA_DUT" != " " ]
then
    dut_args+=(--dut=$ESA_DUT)
    if [ $NETINSTALL_ESA == true ]
    then
        if [ ! -z "$ESA_VERSION" -a "$ESA_VERSION" != " " ]
        then
            echo "=============================================================================="
            echo " * INFO: Starting ESA Netinstall on build $ESA_VERSION"
            echo "=============================================================================="
            $SARF_HOME/bin/pybot_run \
                ${common_args[*]} \
                --dut=$ESA_DUT \
                --variable ESA_VERSION:$ESA_VERSION \
                $SARF_HOME/tests/common/install_esa_build.txt &
        else
            echo "=============================================================================="
            echo " ** ERROR: Empty ESA_VERSION provided."
            echo " **        ESA_VERSION is required for netinstall 'eg: 9.0.0-500'"
            echo "=============================================================================="
            exit 2
        fi
    else
        echo "=============================================================================="
        echo " * INFO: ESA Netinstall Skipped"
        echo "=============================================================================="
    fi
else
    echo "=============================================================================="
    echo " *** ERROR: Empty ESA_DUT name provided."
    echo " ***        ESA hostname is required for test suite exection."
    echo "=============================================================================="
    exit 1
fi

## Netinstall SMA on the given build
if [ $REQUIRE_SMA == true ]
then
    if [ ! -z "$SMA_DUT" -a "$SMA_DUT" != " " ]
    then
        dut_args+=(--dut=$SMA_DUT)
        if [ $NETINSTALL_SMA == true ]
        then
            if [ ! -z "$SMA_VERSION" -a "$SMA_VERSION" != " " ]
            then
                echo "=============================================================================="
                echo " * INFO: Starting SMA Netinstall on build $SMA_VERSION"
                echo "=============================================================================="
                $SARF_HOME/bin/pybot_run \
                    ${common_args[*]} \
                    --dut=$SMA_DUT \
                    --variable SMA_VERSION:$SMA_VERSION \
                    $SARF_HOME/tests/common/install_sma_build.txt &
            else
                echo "=============================================================================="
                echo " ** ERROR: Empty SMA_VERSION provided."
                echo " **        SMA_VERSION is required for SMA netinstall 'eg: 9.5.0-085'"
                echo "=============================================================================="
                exit 2
            fi
        else
            echo "=============================================================================="
            echo " * INFO: SMA Netinstall Skipped"
            echo "=============================================================================="
        fi
    else
        echo "=============================================================================="
        echo " *** ERROR: Empty SMA_DUT name provided."
        echo " ***        SMA hostname is required for test suite exection."
        echo "=============================================================================="
        exit 1
    fi
fi

wait

if [ $NETINSTALL_ESA == true ]
then
    verify_pybot_result \
        $SARF_OUTPUT_DIR/install_esa_build.xml \
        "ESA netinstall failed. Test suites execution stopped"
fi

if [ $REQUIRE_SMA == true -a $NETINSTALL_SMA == true ]
then
    verify_pybot_result \
        $SARF_OUTPUT_DIR/install_sma_build.xml \
        "SMA netinstall failed. Test suites execution stopped"
fi

if [ -z "$MODULES" -o "$MODULES" == " " ]
then
    echo "=============================================================================="
    echo " *** ERROR: Test module name can't be EMPY. Please enter a valid module name."
    echo " *** Check RunYourself job's build page for detailed info about module names."
    echo "=============================================================================="
    exit 1
fi

modules=(${MODULES//,/ })
echo "=============================================================================="
echo "Modules to run:"
echo "---------------"

module_paths=()
for module in "${modules[@]}"
do
    module_path=$TEST_DIR$module
    echo $module_path
    module_paths+=($module_path)
done

echo "=============================================================================="

suites=(${SUITE_NAME//,/ })
include_tags=()
for tag in "${suites[@]}"
do
    include_tags+=(--include $tag)
done

RESULT_NAME='RunYourSelf'
$SARF_HOME/bin/pybot_run \
    ${common_args[*]} \
    ${dut_args[*]} \
    --dut-type-main=ESA \
    --output $RESULT_NAME.xml \
    --report $RESULT_NAME.report.html \
    --log $RESULT_NAME.log.html \
    --debugfile $RESULT_NAME.debug \
    --exclude skip* \
    ${include_tags[*]} \
    ${module_paths[*]}

export PYTHONPATH=$PYTHONPATH:$SARF_HOME/testlib
python $SARF_HOME/tools/django/copy_xml_to_db.py $SARF_OUTPUT_DIR
