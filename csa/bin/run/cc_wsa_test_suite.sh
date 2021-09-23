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
# 3. Single test suite to run
#===========================================================#
# Get scripts directory
export SARF_HOME=$HOME/work/sarf
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

# Enable or disable ipv6 based on parameter ${INET_MODE}
$SARF_HOME/bin/run/enable_disable_ipv6.sh $@

#===========================================================#
# Global Variables Definition
#===========================================================#
export LD_LIBRARY_PATH=/usr/local/lib/firefox3/

# name of the test suite is taken from first argument
SUITE_NAME=$1 && shift

# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/$SUITE_NAME

# Hostname of DUT is taken from second argument
DUT=$WSA

# Version of AsyncOS on applinace is taken from third argument
DUT_VERSION=$1 && shift

#Run the scrip to delete apache log files from HTTP_SERVER
python $SARF_HOME/clean_apache_logs.py $*

#===========================================================#
# Script Execution
#===========================================================#
# clean output directory
#rm -rf $SARF_OUTPUT_DIR/*
# clean tmp directory
sudo rm -rf /var/tmp/customProfileDir*

# clean /tmp directory
if [ -d /tmp/ ]
then
	sudo rm -rf /tmp/*
fi

# clean orphan processes
$SARF_HOME/bin/run/delete_orphan_processes.sh

# common arguments to both netinstall and test suite commands
common_args=(
	--dut $DUT
	--variable WSA_VERSION:$DUT_VERSION
	--outputdir $SARF_OUTPUT_DIR
)

export RU_DT=`date +%y%m%d_%H%M%s`
files=" "

$SARF_HOME/bin/pybot_run \
${common_args[*]} \
--output $SUITE_NAME.xml \
--report $SUITE_NAME$RU_DT.report.html \
--log $SUITE_NAME$RU_DT.log.html \
--debugfile $SUITE_NAME$RU_DT.debug \
--exclude skip* \
$files \
$@

python $SARF_HOME/tools/django/copy_xml_to_db.py $SARF_OUTPUT_DIR
# $SARF_HOME/bin/pybot_run \
	# ${common_args[*]} \
	# -v collect_output:$SARF_OUTPUT_DIR/collect.tar.gz \
	# tests/common/useful_scripts/collect_logs.txt

