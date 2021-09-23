#!/usr/local/bin/bash
# $Id $
# $DateTime $
# $Author $
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This script is written and maintained by the WSA Automation Team.
# Backup the code coverage files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
COVERAGE_BACKUP_FOLDER=/data/home/code_coverage_backup/
mkdir -p $COVERAGE_BACKUP_FOLDER
Dir_C_Code="/usr/build/iproot/coeus/prox/prox.coveragedir"
if [ -d $Dir_C_Code ]
then
	cp -rf $Dir_C_Code $COVERAGE_BACKUP_FOLDER
fi
	
Dir_Python_Code="/data/coverage_data"
Dir_Python_Coverage="/data/release/coeus-*/bin/coverage"

if [ -d $Dir_Python_Code ]
then
	cp -rf $Dir_Python_Code $COVERAGE_BACKUP_FOLDER
fi

#if [ -d $Dir_Python_Coverage ]
#then
#	cp -rf $Dir_Python_Coverage $COVERAGE_BACKUP_FOLDER
#fi	
