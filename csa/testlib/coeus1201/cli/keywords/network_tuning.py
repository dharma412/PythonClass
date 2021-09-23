#!/usr/bin/env python


# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/network_tuning.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $


from common.cli.clicommon import CliKeywordBase, DEFAULT

class NetworkTuning(CliKeywordBase):
    """Keywords for CLI command: networktuning."""

    def get_keyword_names(self):
        return [
                'network_tuning_send_space',
                'network_tuning_recv_space',
                'network_tuning_send_auto',
                'network_tuning_recv_auto',
                'network_tuning_mbuf_cluster_count',
                'network_tuning_send_buf_max',
                'network_tuning_recv_buf_max',
                'network_tuning_clean_fib_1'

                ]

    def network_tuning_send_space(self, send_space=DEFAULT):
        """Hidden CLI Command: networktuning > sendspace

        Parameters:
           - `send_space`: the new value of sendspace
        Examples:
        | Network Tuning Send Space| send_space=32768 |

	"""
        self._cli.networktuning().send_space(send_space)

    def network_tuning_recv_space(self, recv_space=DEFAULT):
        """Hidden CLI Command: networktuning > recvspace

        Parameters:
           - `recv_space`: the new value of recvspace

	Examples:
        | Network Tuning Recv Space| recv_space=65536 |
	"""
        self._cli.networktuning().recv_space(recv_space)

    def network_tuning_send_auto(self,  sendbuf_auto=DEFAULT):
        """Hidden CLI Command: networktuning > send_auto

        Parameters:
           - `sendbuf_auto`: Disable/enable the sendbuf_auto 0/1
        Examples:
        | Network Tuning Send Auto| sendbuf_auto=0 |
	"""
        self._cli.networktuning().send_auto(sendbuf_auto)


    def network_tuning_recv_auto(self,  recvbuf_auto=DEFAULT):
        """Hidden CLI Command: networktuning > recv_auto

        Parameters:
           - `recvbuf_auto`: Disable/enable the recvbuf_auto 0/1

	Examples:
        | Network Tuning Recv Auto| recvbuf_auto=0 |

        """
        self._cli.networktuning().recv_auto(recvbuf_auto)


    def network_tuning_mbuf_cluster_count(self,  nmbclusters=DEFAULT):
        """Hidden CLI Command: networktuning >mbuf_cluster_count

        Parameters:
           - `nmbclusters`: the new value of nmbclusters

        Examples:
        | Network Tuning Mbuf Cluster Count| nmbclusters=98304 |

        """
        self._cli.networktuning().mbuf_cluster_count(nmbclusters)


    def network_tuning_send_buf_max(self,  sendbuf_max=DEFAULT):
        """Hidden CLI Command: networktuning >sendbuf_max

        Parameters:
           - `sendbuf_max`:  the new value of sendbuf_max

        Examples:
        | Network Tuning Send Buf Max| sendbuf_max=0 |

        """
        self._cli.networktuning().send_buf_max(sendbuf_max)


    def network_tuning_recv_buf_max(self,  recvbuf_max=DEFAULT):
        """Hidden CLI Command: networktuning >recvbuf_max

        Parameters:
           - `recvbuf_max`: the new value of recvbuf_max

        Examples:
        | Network Tuning Recv Buf Max| recvbuf_max=262144 |

        """
        self._cli.networktuning().recv_buf_max(recvbuf_max)


    def network_tuning_clean_fib_1(self,  route_value=DEFAULT):
        """Hidden CLI Command: networktuning > clean_fib_1

        Parameters:
           - `route_value`: Clean (0)/Add default Management routes(1)

        Examples:
        | Network Tuning Clean Fib 1| route_value=0 |

        """
        self._cli.networktuning().clean_fib_1(route_value)
