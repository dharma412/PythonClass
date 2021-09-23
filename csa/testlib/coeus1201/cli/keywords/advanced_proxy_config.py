#!/usr/bin/env python

# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/advanced_proxy_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class AdvancedProxyConfig(CliKeywordBase):
    """Keywords for CLI command: advancedproxyconfig."""

    def get_keyword_names(self):
        return [
                'advanced_proxy_config_set_track_time',
                'advanced_proxy_config_authentication',
                'advanced_proxy_config_caching',
                'advanced_proxy_config_dns',
                'advanced_proxy_config_native_ftp',
                'advanced_proxy_config_ftp_over_http',
                'advanced_proxy_config_https',
                'advanced_proxy_config_scanning',
                'advanced_proxy_config_misc',
                'advanced_proxy_config_proxyconn_new',
                'advanced_proxy_config_proxyconn_delete',
                'advanced_proxy_config_customheader_new',
                'advanced_proxy_config_customheader_edit',
                'advanced_proxy_config_customheader_delete',
                'advanced_proxy_config_contentencoding'
                ]

    def advanced_proxy_config_set_track_time(self, interval=DEFAULT):
        """Hidden CLI Command: advancedproxyconfig > settracktime

        Parameters:
           - `interval`: interval in seconds between printing the tracking
                         information.

        Examples:
        | Advanced Proxy Config Set Track Time | interval=10 |
        | Advanced Proxy Config Set Track Time | interval=00 |
        """
        self._cli.advancedproxyconfig().settracktime(interval=interval)

    def advanced_proxy_config_authentication(self, *args):
        """CLI Command: advancedproxyconfig > authentication

        Parameters:
            - `forward_auth`: When would you like to forward authorization
              request headers to a parent proxy. Either Always, Never, Only if
              not used by the WSA. Instead of list option's name its sequence
              number can be specified: 1, 2, 3.
            - `proxy_auth`: Proxy Authorization Realm to be displayed in the end
              user authentication dialog.
            _ `log`: whether to log the username that appears in the request
              URI: Yes/No.
            - `use_group_attr`: Should the Group Membership attribute be used
              for directory lookups in the Web UI: Yes/No.
            - `adv_ad`: whether to use advanced Active Directory: Yes/No
            - `case_insensitive`: whether to allow case insensitive username
              matching in policies: Yes/No
            - `wild_card`: whether to allow wild card matching with the
              character * for LDAP group names: Yes/No
            - `charset`: the charset used by the clients for basic
              authentication: ISO-8859-1 or UTF-8.
            - `ldap_referrals`: enable referrals for LDAP: Yes/No
            - `secure_auth`: enable secure authentication: Yes/No
            - `redirect_port`: redirect port for secure authentication.
            - `hostname`: the hostname to redirect clients for authentication.
            - `timeout`: the surrogate timeout.
            - `re_auth`: re-auth on request denied option: disabled or
              embedlinkinblockpage.
            - `send_negotiate`: send Negotiate header along with NTLM header for
              NTLMSSP authentication: Do not send Negotiate header or Send
              Negotiate header. 1 or 2 can be used instead respectively.
            - `mapping_update`: the IP address to user name mapping update
              interval for transparent user identification in seconds.
            - `transparent_id`: the maximum wait time for transparent user
              identification in seconds.
            - `masking`: username and IP address masking in logs and reports:
                1. Mask both user names and IP addresses in logs and reports
                2. Mask only usernames and replace them with IP addresses in logs
                and reports
                3. Show usernames and IP addresses in logs and reports


        Examples:
        | Advanced Proxy Config Authentication | forward_auth=Always | log=No | masking=Mask both |
        | Advanced Proxy Config Authentication | proxy_auth=Test Realm | charset=UTF-8 | adv_winbindd=Yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.advancedproxyconfig().authentication(**kwargs)

    def advanced_proxy_config_caching(self, cache_option, *args):
        """CLI Command: advancedproxyconfig > caching

        Parameters:
            - `cache_option`: advanced caching option. Either number or
              distinctive part of name: e.g. Safe
                1. Safe Mode
                2. Optimized Mode
                3. Aggressive Mode
                4. Customized Mode

              Note: following options are applied only when "Customized Mode" is
              selected as `cache_option`.

            - `allow_hits`: allow objects with a heurisitic expiration time to
              be served as not-modified If-Modified-Since hits from cache:
              Yes/No
            - `allow_etag`: allow ETAG mismatch on client revalidations: Yes/No
            - `allow_cache_request`: allow caching when requests are
              authenticated by the origin server: Yes/No
            - `allow_cache_server`: allow caching from servers whose DNS results
              do not match the TCP destination IP: Yes/No
            - `max_age_with`: the Heuristic maximum age to cache the document
              with Last-Modified Time but no actual caching value (in seconds).
            - `max_age_without`: the Heuristic maximum age to cache the document
              without Last-Modified Time and no actual caching value (in
              seconds).
            - `age_error_cache`: the Heuristic age to cache errors
              (HTTP_SERVICE_UNAVAIL, HTTP_GATEWAY_TIMEOUT etc) (in seconds).
            - `ignore_client`: ignore client directive to not fetch content from
              the cache: Yes/No
            - `reload_interval`: the time interval during which reload requests
              must be ignored by the proxy (in seconds).
            - `allow_convert`: allow proxy to convert reload requests into
              max-age requests: Yes/No
            - `ims_request_time`: Time in seconds after which an explicit IMS
              Refresh request must be issued.

        Examples:
        | Advanced Proxy Config Caching | Safe Mode |
        | Advanced Proxy Config Caching | Customized Mode | allow_hits=Yes | allow_etag=No | allow_cache_request=Yes |
        """
        modes = ('Safe Mode',
                'Optimized Mode',
                'Aggressive Mode',
                )
        if cache_option == 'Customized Mode':
            kwargs = self._convert_to_dict(args)
            kwargs['cache_option'] = cache_option
        elif cache_option in modes:
            kwargs = {}
            kwargs['cache_option'] = cache_option
        else:
            raise ValueError("Invalid cache option " + cache_option)

        self._cli.advancedproxyconfig().caching(**kwargs)

    def advanced_proxy_config_dns(self, *args):
        """CLI Command: advancedproxyconfig > DNS

        Parameters:
            - `url_format`: the URL format for the HTTP 307 redirection on DNS
              lookup failure.
            - `issue_redirect`: issue a HTTP 307 redirection on DNS lookup
              failure: Yes/No
            - `failover`: not to automatically failover to DNS results when
              upstream proxy (peer) is unresponsive: Yes/No
            - `find_web`: Find web server by: 0 = use DNS answers in order, 1 =
              use client supplied address then DNS, 2 = use client supplied
              address for next hop connection, DNS for Web Reputation, 3 = use
              client supplied address for next hop connection and
              Web Reputation: Either 1, 2 or 3.

        Examples:
        | Advanced Proxy Config DNS | url_format=%P://www.%H.com/%u | issue_redirect=No |
        | Advanced Proxy Config DNS | failover=Yes | find_web=0 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.advancedproxyconfig().dns(**kwargs)

    def advanced_proxy_config_ftp_over_http(self, *args):
        """CLI Command: advancedproxyconfig > ftpoverhttp

        Parameters:
            - `login`: the login name to be used for anonymous FTP access.
            - `password`: the password to be used for anonymous FTP access.

        Examples:
        | Advanced Proxy Config FTP over HTTP | login=testuser | password=ironport |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.advancedproxyconfig().ftpoverhttp(**kwargs)

    def advanced_proxy_config_native_ftp(self, *args):
        """CLI Command: advancedproxyconfig > nativeftp

        Parameters:
            - `enable`: enable FTP proxy: Yes/No
            - `port`: the ports that FTP proxy listens on.
            - `port_range_passive`: the range of port numbers for the proxy to
              listen on for passive FTP connections. Example: 11000-11009
            - `port_range_active`: the range of port numbers for the proxy to
              listen on for active FTP connections. Example: 12000-12009
            - `use_active`: use active mode when passive mode fails: Yes/No
            - `auth_format`: the authentication format:
                1. Check Point
                2. Raptor

            - `enable_cache`: enable caching: Yes/No
            - `enable_spoof`: enable server IP spoofing: Yes/No
            - `pass_msg`: pass FTP server welcome message to the clients: Yes/No
            - `cust_msg`: the customized server welcome message.
            - `max_path_size`: the max path size for the ftp server directory.

        Examples:
        | Advanced Proxy Config Native FTP | enable=No |
        | Advanced Proxy Config Native FTP | enable=Yes | port=8021 |
        | ... | port_range_passive=11000-11009 | port_range_active=12000-12009 |
        | ... | use_active=Yes | auth_format=Raptor | enable_cache=Yes |
        | ... | enable_spoof=Yes | pass_msg=No | cust_msg=Test message |
        | ... | max_path_size=1024 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.advancedproxyconfig().nativeftp(**kwargs)

    def advanced_proxy_config_https(self, *args):
        """CLI Command: advancedproxyconfig > HTTPS

        Parameters:
           - `uri_style`: HTTPS URI logging style.  Either 'fulluri' or
                          'stripquery'.
           - `decrypt`: whether or not to decrypt unauthenticated transparent
                        HTTPS requests for authentication purpose.  Either
                        'Yes' or 'No'.
           - `action`: action to be taken when HTTPS servers ask for client
                       certificate during handshake.  Either 'pass' or 'reply'.
           - `sni`: Enable server name indication (SNI) extension.
                    Either 'Yes' or 'No'.
           - `inter_certs`: Enable intermediate certificates download
                    Either 'Yes' or 'No'.
           - `decrypt_https`: Whether or not to decrypt HTTPS requests for End
                              User Notification purpose.
                              Either 'Yes' or 'No'.
           - `session_resumption`: Y or N
              answer to question "Do you want to enable session resumption"

        Examples:
        | Advanced Proxy Config HTTPS |
        | ... | uri_style=fulluri |
        | ... | decrypt=No |
        | ... | action=pass |
        | ... | sni=Yes |
        | ... | inter_certs=Yes |
        | ... | https_decrypt=No |
        | ... | session_resumption=Y |

        | Advanced Proxy Config HTTPS |
        | ... | uri_style=stripquery |
        | ... | decrypt=Yes |
        | ... | action=reply |
        | ... | sni=Yes |
        | ... | inter_certs=No |
        | ... | decrypt_https=Yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.advancedproxyconfig().https(**kwargs)

    def advanced_proxy_config_scanning(self, *args):
        """CLI Command: advancedproxyconfig > SCANNING

        Parameters:
           - `mw_scan`: specify whether or not proxy should do malware scanning
                        all content regardless of content type.  Either 'Yes'
                        or 'No'.

        Examples:
        | Advanced Proxy Config Scanning | mw_scan=Yes |
        | Advanced Proxy Config Scanning | mw_scan=No |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.advancedproxyconfig().scanning(**kwargs)

    def advanced_proxy_config_misc(self, *args):
        """CLI Command: advancedproxyconfig > Miscellaneous

        Parameters:
            - `health_chk`: respond to health checks from L4 switches (always
              enabled if WSA is in L4 transparent mode): Yes/No
            - `dynamic_adj`: perform dynamic adjustment of TCP receive
                window size: Yes/No
            - `dynamic_adj_send`: perform dynamic adjustment of TCP send
                window size: Yes/No
            - `buffer_clientside`:size of send buffer for client-side socket in bytes.
                An Integer between the range 0 to 262,144(0 for kernel default).
            - `cache_https`: Enable caching of HTTPS responses. Yes/No
            - `min_idle_timeout`: minimum idle timeout for checking unresponsive
              upstream proxy (in seconds).
            - `max_idle_timeout`: maximum idle timeout for checking unresponsive
              upstream proxy (in seconds).
            - `listen_p2`: listen on P2: Yes/No
            - `mode`: Mode of the proxy (value 1 to 4):
                1. Explicit forward mode only
                2. Transparent mode inline
                3. Transparent mode with L4 Switch or no device for redirection
                4. Transparent mode with WCCP v2 Router for redirection

            - `spoof`: Spoofing of the client IP by the proxy (value 1 to 3):
                1. Disable
                2. Enable for all requests
                3. Enable for transparent requests only

            - `pass_http`: pass HTTP X-Forwarded-For headers: Yes/No
            - `tunneling`: permit tunneling of non-http requests on http ports:
              Yes/No
            - `block_nonssl`: block tunneling of non-SSL transactions on SSL
              Ports: Yes/No
            - `log_values`: log values from X-Forwarded-For headers in place of
              incoming connection IP addresses: Yes/No
            - `throttle`: throttle content served from cache: Yes/No
            - `use_client_ip`: use client IP addresses from X-Forwarded-For headers:
              Yes/No
            - `enter_ip`: Please enter the IP addresses for trusted downstream proxies
              (comma separated): list of IP addresses
            - `fwd_tcp_rst`: use client IP addresses from X-Forwarded-For headers: Yes/No
            - `wccp_health_check`: enable wccp proxy health : Yes/No
            - `disable_host_ip`: disable IP address in Host: Yes/No
            - `filter_non_http`: filter non-http responses: Yes/No
            - `schedule_proxy_restart`: schedule a proxy restart: Yes/No


        Examples:
        | Advanced Proxy Config Misc | block_nonssl=Yes | log_values=Yes |
        | Advanced Proxy Config Misc | health_chk=Yes | dynamic_adj=Yes |
        | ... | cache_https=Yes | min_idle_timeout=15 | max_idle_timeout=60 |
        | ... | mode=3 | spoof=2 | pass_http=Yes | tunneling=No |
        | ... | use_client_ip=Yes | enter_ip=1.2.3.4,1.2.3.5
        """
        kwargs = self._convert_to_dict(args)
        self._cli.advancedproxyconfig().miscellaneous(**kwargs)

    def advanced_proxy_config_proxyconn_new(self, user_agent):
        """CLI Command: advancedproxyconfig > PROXYCONN > NEW

        Parameters:
        - `user_agent`: Specify user agent that is to be added
                        (Regular expression).Required.
        Examples:
        | Advanced Proxy Config Proxyconn NEW | user_agent=[bd] |

        """
        if user_agent:
            self._cli.advancedproxyconfig().proxyconn()._add_user_agent\
            (user_agent=user_agent)

    def advanced_proxy_config_proxyconn_delete(self, user_agent):
        """CLI Command: advancedproxyconfig > PROXYCONN > DELETE

        Parameters:
        - `user_agent`: Specify user agent that is to be deleted.
                        Required.
        Examples:
        | Advanced Proxy Config Proxyconn Delete | user_agent=[bd] |

        """
        if user_agent:
            self._cli.advancedproxyconfig().proxyconn()._delete_user_agent\
            (user_agent=user_agent)

    def advanced_proxy_config_customheader_new(self, header, domains):
        """CLI Command: advancedproxyconfig > customheader > new

        Parameters:
            - `header`: header in format of field: value
            - `domains`: domains to be suffixed. in case of multiple domain seprate by comma.

        Examples:
        | Advanced Proxy Config Customheader New | header=project:WSA
                                     | domains=cisco.com,ironport.com
        """

        self._cli.advancedproxyconfig().customHeaderNew(
                        header=header,domains=domains)

    def advanced_proxy_config_customheader_edit(self, header, newheader, newdomains):
        """CLI Command: advancedproxyconfig > customheader > edit

        Parameters:
            - `header`: Old Header name which need to be changed
            - `newheader`: new name of header in format of field: value
            - `newdomains`: new domains to be suffixed. in case of multiple domain seprate by comma.

        Examples:
        | Advanced Proxy Config Customheader Edit | headernumber=1
             | header=project:WSA | domains=cisco.com,ironport.com
        """

        self._cli.advancedproxyconfig().customHeaderEdit(header=header,
                                newheader=newheader,newdomains=newdomains)

    def advanced_proxy_config_customheader_delete(self, header):
        """CLI Command: advancedproxyconfig > customheader

        Parameters:
            - `header`: Header name which need to be deleted

        Examples:
        | Advanced Proxy Config Customheader Delete | headernumber=1
        """

        self._cli.advancedproxyconfig().customHeaderDelete(header=header)

    def advanced_proxy_config_contentencoding(self, encoding_type=None, encoding_enable=None):
        kwargs={'type':encoding_type, 'enable': encoding_enable}

        """CLI Command: advancedproxyconfig > contentencoding
        Examples:
        | Advanced Proxy Config Contentencoding | encoding_type=br  encoding_enable=yes
        """
        self._cli.advancedproxyconfig().contentencoding(**kwargs)
