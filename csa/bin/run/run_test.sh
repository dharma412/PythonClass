# $Id: //prod/main/sarf_centos/bin/run/run_test.sh#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

#===========================================================#
# That's a simple script to start SARF tests autonomously
# The first parameter is a name of the job.
# The results would be stored in a folder with that name
# All other parameters are just passed to SARF

# Example of usage:
#    run_test.sh example coeus75/unittests/cli/version.txt
#===========================================================#

export LD_LIBRARY_PATH=/usr/local/lib/firefox3/
export SARF_HOME=$HOME/work/sarf
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

# name of the job is taken from first argument
JOB_NAME=$1
# remove job name from argument list
shift
# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/$JOB_NAME

#===========================================================#
# Script Execution
#===========================================================#

# clean output directory
rm -rf $SARF_OUTPUT_DIR/*

$SARF_HOME/bin/pybot_run \
        --dut $WSA \
        --outputdir $SARF_OUTPUT_DIR \
        --output $JOB_NAME.xml \
        --report $JOB_NAME.report.html \
        --log $JOB_NAME.log.html \
        --debugfile $JOB_NAME.debug \
        $@