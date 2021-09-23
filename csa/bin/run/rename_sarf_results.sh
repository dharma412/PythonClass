#!/usr/local/bin/bash
# $Id $
# $DateTime $
# $Author $
#===========================================================#
# Script to rename the Robot report files on Jenkins
# Required Arguments:
# 1. Name of the report file.
# 2. Name of the JOB
#===========================================================#
set -x
export SARF_HOME=$HOME/work/sarf_centos
# directory where output files will be placed
SARF_OUTPUT_DIR=$HOME/public_html/wsa_qa

# Version of AsyncOS on applinace is taken from third argument
LOG_FILE_NAME=$1
shift

# name of the test suite is taken from first argument
JOB_NAME=$1
echo 'Renaming test files'

cp $SARF_OUTPUT_DIR/$LOG_FILE_NAME.xml $SARF_OUTPUT_DIR/$JOB_NAME.xml
cp $SARF_OUTPUT_DIR/$LOG_FILE_NAME.report.html $SARF_OUTPUT_DIR/$JOB_NAME.report.html
cp $SARF_OUTPUT_DIR/$LOG_FILE_NAME.log.html $SARF_OUTPUT_DIR/$JOB_NAME.log.html
cp $SARF_OUTPUT_DIR/$LOG_FILE_NAME.debug $SARF_OUTPUT_DIR/$JOB_NAME.debug
if [[ "$2" == "srts" ]] || [[ "$2" == "SRTS" ]]; then
    rm -f $SARF_HOME/tmp/SRTS_results/* 2>&1
    mkdir -p $SARF_HOME/tmp/SRTS_results/ 2>&1
    cp $SARF_OUTPUT_DIR/$JOB_NAME*  $SARF_HOME/tmp/SRTS_results/
elif [[ "$2" == "erts" ]] || [[ "$2" == "ERTS" ]]; then
    rm -f $SARF_HOME/tmp/ERTS_results/* 2>&1
    mkdir -p $SARF_HOME/tmp/ERTS_results/ 2>&1
    cp $SARF_OUTPUT_DIR/$JOB_NAME*  $SARF_HOME/tmp/ERTS_results/
elif [[ "$2" == "bats" ]] || [[ "$2" == "BATS" ]]; then
    rm -f $SARF_HOME/tmp/BATS_results/* 2>&1
    mkdir -p $SARF_HOME/tmp/BATS_results/ 2>&1
    cp $SARF_OUTPUT_DIR/$JOB_NAME*  $SARF_HOME/tmp/BATS_results/
else
    echo 'please pass the correct parameter'
fi

