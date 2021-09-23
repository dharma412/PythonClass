#!/usr/local/bin/bash
# $Id $ $DateTime $ $Author $
#===========================================================#
# Common script for running netinstall from Jenkins and 
# Executing Selenium Jar in the Client
#===========================================================#
# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export SARF_HOME=$DIR/../..
export PYTHONPATH=$SARF_HOME/resources:$SARF_HOME/variables:$SARF_HOME/testlib:$PYTHONPATH

#clear lingering selenium process
ps auxww | grep -Ei "\-port|pybot_run" | awk '{print $2}' | xargs kill -9

#Make all .sh scripts to execute
chmod +x $SARF_HOME/bin/run/*.sh

# Enable or disable ipv6 based on parameter ${INET_MODE}
#$SARF_HOME/bin/run/enable_disable_ipv6.sh $@

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

# Hostname of DUT is taken from second argument
DUT_1=$WSA

if [ $UPSTREAM_SERVER_A ]
then
    DUT_2=$UPSTREAM_SERVER_A
else
    DUT_2=$WSA2
fi

if [ $UPSTREAM_SERVER_B ]
then
    DUT_3=$UPSTREAM_SERVER_B
else
    DUT_3=$WSA3
fi

# Version of AsyncOS on applinace is taken from third argument
DUT_VERSION=$1
# remove version from argument list
shift

#Get the customer choice from job configuration
if [ "$NETINSTALL_REQUIRED" == "NO" ]; then
        NETINST_RQD="FALSE"
else
        NETINST_RQD="TRUE"
fi

#Run the scrip to delete apache log files from HTTP_SERVER
python $DIR/clean_apache_logs.py $*

#===========================================================#
# Script Execution
#===========================================================#

# clean the sarf output directory
python $DIR/clean_sarf_output_folder.py $SARF_OUTPUT_DIR

# Clear the tmp files
$SARF_HOME/bin/run/clear_tmp.sh

# make ssh default to ipv4
$SARF_HOME/bin/run/make_ssh_default_to_inet.sh

#Configure client to prefer ipv4
sudo /etc/rc.d/ip6addrctl prefer_ipv4
 
# clean orphan processes
$DIR/delete_orphan_processes.sh

#Check and make slot offline it needed
pybot  --variable DUT:$DUT_1  \
       --variable HTTP_SERVER:$SLICE_SERVER  \
       --variable BUILD:$WSA_VERSION \
       --variable BUILD_URL:$JOB_URL  \
       --variable SARF_HOME:$SARF_HOME  \
       --variable NODE:$NODE_NAME  \
       --variable JENKINS_URL:$JENKINS_URL  \
       --outputdir $SARF_OUTPUT_DIR  \
       --output check_pre_requisites.xml  \
       --report check_pre_requisites.report.html  \
       --log check_pre_requisites.log.html \
       --debugfile check_pre_requisites.debug  \
       $SARF_HOME/tests/common/check_pre_requisites.txt

# common arguments to both netinstall and test suite commands
common_args=(
	--dut $DUT_1
	--variable WSA_VERSION:$DUT_VERSION
	--outputdir $SARF_OUTPUT_DIR
)

# netinstall
flag=/tmp/netinstall_started

#Skip netinstall based on the customer input
if [ "$NETINST_RQD" != 'FALSE' ]
then
        #Netinstall for all WSA in a slot/slice
        for NU in 1 2 3
        do
        DUT=DUT_$NU
        if [ ${!DUT} ]
        then
                $SARF_HOME/bin/pybot_run \
                        --dut ${!DUT} \
                        --variable WSA_VERSION:$DUT_VERSION \
                        --outputdir $SARF_OUTPUT_DIR \
                        -v NETINST_FLAG:$flag \
                        $SARF_HOME/tests/common/install_wsa_build_if_necessary.txt
        fi
        done
fi

# test suite will be run only if netinstall passed
if [ ! -e $flag ]
then
    # Restore Threat Grid(TG) API Key to WSA
    python $DIR/copy_tg_apikey.py $DUT_1 restore_apikey

    #Clear apache logs and contents of tmp directory
    $SARF_HOME/bin/pybot_run \
        ${common_args[*]} \
        $SARF_HOME/tests/common/clear_apache_logs.txt

else
    echo "Netinstall failed. Suite $SUITE_NAME has not been run."
    exit $netinst
fi

# Disable ipv6 (call without parameters)
sudo python $SARF_HOME/bin/run/backup_logs.py $JOB_NAME

#Check if WSA is not accessible and set slot status to offline
#This is because WSA becomes unreachable mid run.
pybot  --variable DUT:$DUT_1  \
       --variable HTTP_SERVER:$SLICE_SERVER  \
       --variable SARF_HOME:$SARF_HOME  \
       --variable NODE:$NODE_NAME  \
       --variable JENKINS_URL:$JENKINS_URL  \
       --outputdir $SARF_OUTPUT_DIR  \
       --output check_status.xml  \
       --report check_status.report.html  \
       --log check_status.log.html \
       --debugfile check_status.debug  \
       $SARF_HOME/tests/common/check_wsa_status.txt

# Used to Start the Selenium Jar and Trigger the CURL request script from all the clients 
echo "Starting the Selenium Standalone Server"
ps auxwwww | grep 5543 |grep -v "grep" |awk {'print $2'} | xargs kill -9
BUILD_ID=dontKillMe nohup java -jar tools/selenium-server-standalone-2.52.0.jar -port 5543 &

# Clear the tmp files
$SARF_HOME/bin/run/clear_tmp.sh

