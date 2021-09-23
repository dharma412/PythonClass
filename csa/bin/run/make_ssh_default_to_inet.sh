#!/bin/sh
# $Id: //prod/main/sarf_centos/bin/run/make_ssh_default_to_inet.sh#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

# Edit ssh config so that all ssh connections defaul to ipv4 from the client.

CONF_FILE="/etc/ssh/ssh_config"
TEMP_FILE="/tmp/ssh.cong"


# remove all settings of ipv6_enable
grep -v AddressFamily $CONF_FILE > $TEMP_FILE
echo AddressFamily inet >> $TEMP_FILE

# Save changes in original file
sudo chmod 666 $CONF_FILE
sudo cp $TEMP_FILE $CONF_FILE
sudo chmod 444 $CONF_FILE
