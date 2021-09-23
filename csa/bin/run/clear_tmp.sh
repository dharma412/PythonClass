#!/bin/sh
# $Id: //prod/main/sarf_centos/bin/run/clear_tmp.sh#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

# clean tmp directory
sudo rm -rf /var/tmp/customProfileDir*

# clean /tmp directory
sudo rm -rf /tmp/webp*
sudo rm -rf /tmp/webg*
sudo rm -rf /tmp/*

