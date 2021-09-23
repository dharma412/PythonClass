#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Common script for recovering appliance from Jenkins
# Required environment variables for Jenkins node
# configuration that is going to use this script:
#  - WSA: hostname of appliance attached to the node
# Required Arguments:
# 1. WSA_DUT_VERSION
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

# Version of AsyncOS on applinace is set to coeus-7-5-0-823 if not passed
WSA_DUT_VERSION=${2:-coeus-7-5-0-823}

#===========================================================#
# Script Execution
#===========================================================#

# clean output directory
rm -rf $SARF_OUTPUT_DIR/*

# common arguments to both netinstall and test suite commands
common_args=(
	--dut $DUT
	--dut-version '7.7.0-725'
	--dut-model 'S670'
	--variable WSA_VERSION:$WSA_DUT_VERSION
	--outputdir $SARF_OUTPUT_DIR
	--skip-check
)

# netinstall
$SARF_HOME/bin/pybot_run \
	${common_args[*]} \
	$SARF_HOME/tests/common/recover_wsa_build.txt