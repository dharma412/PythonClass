#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Common script for running test suites from Jenkins
# Required environment variables for Jenkins node
# configuration that is going to use this script:
#  - SMA: hostname of appliance attached to the node
# Required Arguments:
# 1. SMA_DUT_VERSION
#===========================================================#

# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#===========================================================#
# Global Variables Definition
#===========================================================#
export LD_LIBRARY_PATH=/usr/local/lib/firefox3/
export SARF_HOME=$DIR/../..
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/$SUITE_NAME

# Hostname of DUT
DUT=$1

# Version of AsyncOS on applinace
SMA_DUT_VERSION=${2:-zeus-7-8-0-572}

#===========================================================#
# Script Execution
#===========================================================#

# clean output directory
rm -rf $SARF_OUTPUT_DIR/*

# common arguments to both netinstall and test suite commands
common_args=(
	--dut $DUT
	--dut-version '7.8.0-572'
	--dut-model 'M670'
	--variable SMA_VERSION:$SMA_DUT_VERSION
	--outputdir $SARF_OUTPUT_DIR
	--skip-check
)

# netinstall
$SARF_HOME/bin/pybot_run \
	${common_args[*]} \
	$SARF_HOME/tests/common/recover_sma_build.txt