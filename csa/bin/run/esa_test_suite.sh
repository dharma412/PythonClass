#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Required Arguments:
# 1. SUITE_NAME
#===========================================================#
# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export SARF_HOME=$DIR/../..


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


# Previous Run Link
if [[ $1 == http://* ]]
then
    echo "Preparing for re-run of failed test cases using $1"
    $SARF_HOME/bin/pybot_run --dut $DUT \
    -v link:$1 $SARF_HOME/tests/common/unittests/scp.txt
    python $SARF_HOME/tools/gather_failed_tests.py /tmp/output.xml /tmp/failed_tests.txt
    files="--argumentfile /tmp/failed_tests.txt"
    shift
fi

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
	--outputdir $SARF_OUTPUT_DIR
)

$SARF_HOME/bin/pybot_run \
	${common_args[*]} \
        --output $SUITE_NAME.xml \
	--report $SUITE_NAME.report.html \
	--log $SUITE_NAME.log.html \
	--debugfile $SUITE_NAME.debug \
	--exclude skip* \
	$files \
	$@
