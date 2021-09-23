#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Recover services on slice server (http server)
# Required Arguments:
# 1. SLICE_SERVER
#===========================================================#

# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#===========================================================#
# Global Variables Definition
#===========================================================#
export SARF_HOME=$DIR/../..
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/recover_server

# Hostname of DUT
SERVER=$1

#===========================================================#
# Script Execution
#===========================================================#

# clean output directory
rm -rf $SARF_OUTPUT_DIR/*

echo Recovering slice server $1
pybot -v SLICE_SERVER:$1 --outputdir $SARF_OUTPUT_DIR $SARF_HOME/tests/common/recover_slice_server.txt
