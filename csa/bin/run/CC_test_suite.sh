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
#===========================================================#
# Get scripts directory
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#echo "*****" $DIR
#export SARF_HOME=$DIR/../..
export SARF_HOME=$HOME/work/sarf
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

#===========================================================#
# Global Variables Definition
#===========================================================#
export LD_LIBRARY_PATH=/usr/local/lib/firefox3/

# name of the test suite is taken from first argument
SUITE_NAME=$1
# remove suite name from argument list
shift

# directory where output files will be placed
#SARF_OUTPUT_DIR=$HOME/public_html/$SUITE_NAME

SARF_OUTPUT_DIR=$HOME/public_html/wsa_qa

echo "****" $SARF_OUTPUT_DIR
# Hostname of DUT is taken from second argument
#DUT=$WSA
DUT=$1

echo "********" $DUT
# remove DUT from argument list
shift
TESTSUITE_NAME=$1
echo "***testname**" $TESTSUITE_NAME

TEST_RESULT=$SUITE_NAME"_"$TESTSUITE_NAME
echo "Test result ***" $TEST_RESULT


#===========================================================#
# Script Execution
#===========================================================#

# clean output directory
#rm -rf $SARF_OUTPUT_DIR/*
# clean tmp directory
#sudo rm -rf /var/tmp/customProfileDir*
# clean /tmp directory
#sudo rm -rf /tmp/*

# clean orphan processes
#$DIR/delete_orphan_processes.sh


#common arguments to both netinstall and test suite commands
#common_args=(--dut $DUT --variable WSA_VERSION:$DUT_VERSION --outputdir $SARF_OUTPUT_DIR)

#test_name=$SARF_HOME/tests/coeus90/unittests/cli/samplegui.txt
#test_name=unittests/cli/samplegui.txt

test_name=unittests/cli/QABackdoorOperations.txt
echo  "****" $test_name

cd $SARF_HOME/tests/coeus90/
echo "***Executing QABackdoorOperation test-Stop WSA,Generate CC Report,Start WSA *****"

$SARF_HOME/bin/pybot_run --dut $DUT --output $TEST_RESULT.xml --report $TEST_RESULT.report.html --log $TEST_RESULT.log.html --debugfile $TEST_RESULT.debug --variable WSA_DUT:$DUT  --variable SUITES_NAME:$TESTSUITE_NAME  $test_name

#/home/sarukakk/work/sarf/bin/pybot_run --dut $DUT --output $SUITE_NAME.xml --report $SUITE_NAME.report.html --log $SUITE_NAME.log.html --debugfile $SUITE_NAME.debug--variable WSA_DUT:$DUT $test_name




#$SARF_HOME/bin/pybot_run \
#        ${common_args[*]} \
#        --output $SUITE_NAME.xml \
#        --report $SUITE_NAME.report.html \
#        --log $SUITE_NAME.log.html \
#        --debugfile $SUITE_NAME.debug \
#        --variable WSA_DUT:$DUT $test_name




#python $SARF_HOME/tools/django/copy_xml_to_db.py $SARF_OUTPUT_DIR
#    $SARF_HOME/bin/pybot_run \
#        ${common_args[*]} \
#        -v collect_output:$SARF_OUTPUT_DIR/collect.tar.gz \
#        tests/common/useful_scripts/collect_logs.txt
