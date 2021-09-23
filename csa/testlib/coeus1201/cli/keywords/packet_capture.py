#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/packet_capture.py#1 $

from common.cli.clicommon import CliKeywordBase

class PacketCapture(CliKeywordBase):
    """Captures packets off the network.

    All tcpdump style filters are supported (for example: tcp port 80 && tcp
    port 3128).

    The command runs in the background and writes the capture data to a file in
    the 'captures' directory.
    """

    def get_keyword_names(self):
        return [
            'packet_capture_setup',
            'packet_capture_start',
            'packet_capture_stop',
            'packet_capture_status',
        ]

    def packet_capture_setup(self, *args):
        """Packet Capture Setup

        packetcapture > setup

        Change packet capture settings

        Parameters:
        - `max_size`: maximum allowable size for the capture file (MB).
        - `stop_limit`: if you want to stop the capture when the file size is
        reached specify 'yes', either specify 'no'.  (If not, a new file will be
        started and the older capture data will be discarded.) Default is 'no'.
        - `if_name`: String of comma separated values that represents interfaces
        where each interface is specified either by name or number.
        The following interfaces are configured:
        * 'Management' or 1,
        * 'T1' or 2,
        * 'T2' or 3.
        - `filter`: specify the filter to be used for the capture. Default:
        '(tcp port 80 or tcp port 3128)'. Or specify word "CLEAR" to clear
        the filter and capture all packets on the selected interfaces.

        Examples:
        | Packet Capture Setup | max_size=100 | stop_limit=yes | if_name=1,2 |

        | Packet Capture Setup | filter=CLEAR |
        """

        kwargs = self._convert_to_dict(args)
        output = self._cli.packetcapture().setup(**kwargs)
        self._info(output)
        return output

    def packet_capture_start(self):
        """Packet Capture Start

        packetcapture > start

        Start packet capture.

        Example:
        | Packet Capture Start |
        """

        output = self._cli.packetcapture().start()
        self._info(output)
        return output

    def packet_capture_stop(self):
        """Packet Capture Stop

        packetcapture > stop

        Stop packet capture.

        Example:
        | Packet Capture Stop |
        """

        output = self._cli.packetcapture().stop()
        self._info(output)
        return output

    def packet_capture_status(self):
        """Packet Capture Status

        packetcapture > status

        Display packet capture status.

        Example:
        | Packet Capture Status |
        """

        output = self._cli.packetcapture().status()
        self._info(output)
        return output

