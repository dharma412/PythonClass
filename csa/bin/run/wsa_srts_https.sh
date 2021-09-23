#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Script for running WSA SRTS HTTPS test suite
# Required Arguments:
# 1. DUT_VERSION
#===========================================================#

#===========================================================#
# Global Variables Definition
#===========================================================#

# get script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get tests directory
TESTS_DIR=$DIR/../../tests

#===========================================================#
# Script Execution
#===========================================================#

$DIR/wsa_test_suite.sh \
	srts_https \
	$@ \
	--include standard \
	$TESTS_DIR/coeus75/common_regression_tests/https
