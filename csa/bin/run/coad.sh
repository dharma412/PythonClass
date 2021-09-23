#!/usr/local/bin/bash

errmsg="Run the script as ./coad -w|-d|--wsa|--dut <WSAIP> -m <list of mail ids to receive the result of the test> -u <username: dev|devtest|bvt>"

if test $# -eq 6
then
	while [[ $# > 1 ]]
	do
		key="$1"

		case $key in
		    -d|--dut|-w|--wsa)
			    wsaip="$2"
			    shift # past argument
		    ;;
		    -m|--mail)
			    mail="$2"
			    shift # past argument
		    ;;
		    -u|--user)
			    user="$2"
			    shift # past argument
		    ;;
		    *)
			    echo "$1 is not a valid option"
			    echo $errmsg
		    ;;
		esac
		shift
	done
else
	echo $errmsg
	exit 1
fi

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
LOGPATH="~/public_html/coad"

Date="$(date +'%a-%d%m%Y-%H%M%S')"
`mkdir -p $LOGPATH`
logfile="$LOGPATH/${Date}"

exec >> "${logfile}"
exec 2>&1

ssh -6 cisco@2001:420:5440:2003:ce30::69 "sudo /home/cisco/coad/runcoad.sh $wsaip $mail $user"
