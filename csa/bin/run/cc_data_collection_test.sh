#!/usr/local/bin/bash
# $Id: //prod/main/sarf_centos/bin/run/cc_data_collection_test.sh#1 $ 
# $DateTime $ 
# $Author $
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Purpose: Test Script Launcher for the Code Coverage Tests
#
# Parameters:
#	DUT								- 		WSA
#	TEST_SUITE_NAME		-		Test Suite Name
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Set Test Home and Search Directory Paths
echo "Setting up the variables for code coverage tests..."
export SARF_HOME=$HOME/work/sarf
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH
export LD_LIBRARY_PATH=/usr/local/lib/firefox3/
echo "List Variables..."
echo "SARF_HOME: $SARF_HOME"
echo "PYTHONPATH: $PYTHONPATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Variables Processing
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Hostname of DUT is taken from second argument
#DUT=$1 && shift
DUT=${WSA}
# Name of the test suite is taken from first argument
TEST_SUITE_NAME=$1 && shift

TIMESTAMP=`date +%Y%m%d_%H%M%S`		#`python -c "from datetime import datetime; print datetime.now().strftime(\"%Y%m%d_%H%M%S\")"`
CC_TEST_RESULT=$TEST_SUITE_NAME\_$TIMESTAMP

echo "List Variables - Test..."
echo "DUT: $DUT"
echo "TEST_SUITE_NAME: $TEST_SUITE_NAME"
echo "CC_TEST_RESULT: $CC_TEST_RESULT"

# Directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/wsa_qa
# CC QA Backdoor Ops Script
CC_Data_Collection_Script=$SARF_HOME/tests/common/cc_qa_backdoor_operations.txt
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Script Execution
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# clean /tmp directory
$SARF_HOME/bin/run/clear_tmp.sh

echo "Starting | Code Coverage Data Collection..."

$SARF_HOME/bin/pybot_run --dut $DUT \
--outputdir $SARF_OUTPUT_DIR \
--output $CC_TEST_RESULT.xml --report $CC_TEST_RESULT.report.html \
--log $CC_TEST_RESULT.log.html --debugfile $CC_TEST_RESULT.debug \
--variable WSA_DUT:$DUT  --variable CC_SUITE_NAME:$CC_TEST_RESULT  \
--variable CC_TEST_RESULT:$CC_TEST_RESULT $CC_Data_Collection_Script

echo "Finished | Code Coverage Data Collection."
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
