#!/usr/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Common script for running test suites from Jenkins
# Required environment variables for Jenkins node
# configuration that is going to use this script:
#  - SMAs,WSAs: hostname of appliance attached to the node
#                  to the node
# Required Arguments:
# 1. SUITE_NAME
# 2. DUT_WSA_VERSION,DUT_SMA_VERSION
# 3. One or more test suits to run
#===========================================================#
# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export SARF_HOME=$DIR/../..
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

#clear lingering selenium process
ps auxww | grep -Ei "\-port|pybot_run" | awk '{print $2}' | xargs kill -9

# Kill the Shell Script process which is started by CFD jobs if any
ps awwwux | grep -Ei "CSC.*sh" | awk '{print $2}' | xargs kill -9

# Kill the python file if any running
ps awwwux | grep -E ".*py" | awk '{print $2}' | xargs kill -9

#Make all .sh scripts to execute
chmod +x $SARF_HOME/bin/run/*.sh

# Enable or disable ipv6 based on parameter ${INET_MODE}
$SARF_HOME/bin/run/enable_disable_ipv6.sh $@

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

# Hostname of SMA DUT is taken from the env variable`
DUT_SMA_1=$SMA
DUT_SMA_2=$SMA2

# Hostname of WSA  DUT is taken from the env variable`
DUT_WSA_1=$WSA
DUT_WSA_2=$WSA2
DUT_WSA_3=$WSA3

# Version of AsyncOS on applinace is taken from third argument
DUT_WSA_VERSION_1=$1
# remove version from argument list
shift

DUT_SMA_VERSION_1=$1
#remove version from argument list
shift

if [ ! -z "$DUT_WSA_2" ]
then
   DUT_WSA_VERSION_2=$1
   #remove version from argument list
   shift
fi

if [ ! -z "$DUT_WSA_3" ]
then
   DUT_WSA_VERSION_3=$1
   #remove version from argument list
   shift
fi

if [ ! -z "$DUT_SMA_2" ]
then
   DUT_SMA_VERSION_2=$1
   #remove version from argument list
   shift
fi

#===========================================================#
# Script Execution
#===========================================================#

# clean output directory
#rm -rf $SARF_OUTPUT_DIR/*
python $DIR/clean_sarf_output_folder.py $SARF_OUTPUT_DIR

# clean tmp directory
#sudo rm -rf /var/tmp/customProfileDir*
$SARF_HOME/bin/run/clear_tmp.sh
sudo rm -rf /var/tmp/tmp*
sudo rm -rf /tmp/tmp*

# clean orphan processes
$DIR/delete_orphan_processes.sh

# common arguments to both netinstall and test suite commands

#output=$(/usr/local/bin/python /home/testuser/work/sarf/tools/esa/node_check.py)
#echo $output

common_args=(
	--dut $DUT_SMA_1
	--dut $DUT_WSA_1
	--variable WSA_VERSION:$DUT_WSA_VERSION_1
	--variable SMA_VERSION:$DUT_SMA_VERSION_1
	--outputdir $SARF_OUTPUT_DIR
)

#SMA Net Install will remove it later 
flag=/tmp/netinstall_started
for NU in 1 2
do
   DUT_SMA=DUT_SMA_$NU
   DUT_SMA_VERSION=DUT_SMA_VERSION_$NU
   if [ ${!DUT_SMA} ]
   then
        $SARF_HOME/bin/pybot_run \
        --dut ${!DUT_SMA} \
        --variable SMA_VERSION:${!DUT_SMA_VERSION} \
        --outputdir $SARF_OUTPUT_DIR/${!DUT_SMA} \
        -v NETINST_FLAG:$flag \
        $SARF_HOME/tests/common/install_sma_build.txt
        #$SARF_HOME/tests/common/install_sma_build_if_necessary.txt
   fi
   #Terminate the script execution if net install is not successful
   if [ -e $flag ]
   then
      echo "Netinstall failed for SMA: ${!DUT_SMA} "
      echo "Terminating the script execution..."
      exit 1
   else
      echo "Netinstall passed for SMA: ${!DUT_SMA} "
   fi
 
done

# WSA install will happens only SMA install pass
if [ $? = 0 ]
then
  flag=/tmp/netinstall_started
  #WSA Net Install
  for NU in 1 2 3
  do
      DUT=DUT_WSA_$NU
      DUT_WSA_VERSION=DUT_WSA_VERSION_$NU
      if [ ${!DUT} ]
      then
         $SARF_HOME/bin/pybot_run \
            --dut ${!DUT} \
            --variable WSA_VERSION:${!DUT_WSA_VERSION} \
            --outputdir $SARF_OUTPUT_DIR/${!DUT} \
            -v NETINST_FLAG:$flag \
            $SARF_HOME/tests/common/install_wsa_build.txt
            #$SARF_HOME/tests/common/install_wsa_build_if_necessary.txt
      fi

      #Terminate the script execution if net install is not successful
      if [ -e $flag ]
      then
           echo "Netinstall failed for WSA: ${!DUT} "
           echo "Terminating the script execution..."
           exit 1
      else
           echo "Netinstall passed for WSA: ${!DUT} "
       fi

  done

else
    echo "Netinstall failed. Suite $SUITE_NAME has not been run."
    exit 1
fi

# test suite will be run only if netinstall passed
if [ ! -e $flag ]
then
    $SARF_HOME/bin/pybot_run \
	${common_args[*]} \
        --listener $SARF_HOME/tools/DynamicAutoTriage/Listener.py \
	--output $SUITE_NAME.xml \
	--report $SUITE_NAME.report.html \
	--log $SUITE_NAME.log.html \
	--debugfile $SUITE_NAME.debug \
	--exclude skip* \
	$@
    python $SARF_HOME/tools/django/copy_xml_to_db.py $SARF_OUTPUT_DIR
    $SARF_HOME/bin/pybot_run \
        ${common_args[*]} \
        -v collect_output:$SARF_OUTPUT_DIR/collect.tar.gz \
        tests/common/useful_scripts/collect_logs.txt
else
    echo "Netinstall failed. Suite $SUITE_NAME has not been run."
    exit 1
fi

# Disable ipv6 (call without parameters)
$SARF_HOME/bin/run/enable_disable_ipv6.sh

# clean tmp directory
$SARF_HOME/bin/run/clear_tmp.sh
sudo rm -rf /var/tmp/tmp*
sudo rm -rf /tmp/tmp*
