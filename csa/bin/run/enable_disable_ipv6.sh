#!/bin/sh
# $Id: //prod/main/sarf_centos/bin/run/enable_disable_ipv6.sh#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

# If protocol is set to ipv6, enable ipv6 on the box
# else disable it

ENABLE_IPV6="INET_MODE:ipv6"
CONF_FILE="/etc/rc.conf"
TEMP_FILE="/tmp/rc.cong"

found_ipv6="false"

for arg in "$@"
do
   if [ "$arg" = "$ENABLE_IPV6" ]
       then
           found_ipv6="true"
   fi
done
# remove all settings of ipv6_enable
grep -v ipv6_enable $CONF_FILE > $TEMP_FILE

if [ "$found_ipv6" = "true" ]
    then # add setting of ipv6_enable
       echo ipv6_enable="YES" >> $TEMP_FILE
fi

# Save changes in original file
sudo chmod 666 $CONF_FILE
sudo cp $TEMP_FILE $CONF_FILE
sudo chmod 444 $CONF_FILE
