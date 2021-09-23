#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/ocsp_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT
import re


class OcspConfig(CliKeywordBase):
    """OCSP Configuration."""

    def get_keyword_names(self):
        return [
            'ocsp_config',
        ]

    def _ocsp_config_enable(self,
                             val_cache_t=DEFAULT,
                             inval_cache_t=DEFAULT,
                             net_cache_t=DEFAULT,
                             clock_skew=DEFAULT,
                             max_time_resp=DEFAULT,
                             upstream_proxy='N',
                             upstream_proxy_grp=DEFAULT,
                             crypt_nonce ='N',
                             exempted_server=DEFAULT,
                             delete_exempted=DEFAULT,
                             clear_all_exempted=DEFAULT
                           ):
        """Enables OCSP through CLI"""
        kwargs = { }

        if(all([exempted_server,delete_exempted,\
         clear_all_exempted]) or all([exempted_server,\
            delete_exempted]) or all([delete_exempted,\
                clear_all_exempted]) or all([exempted_server,\
                    clear_all_exempted])):
            raise ValueError('You must specify only one of the following-' \
                             'exempted_server or delete_exempted or '\
                             'clear_all_exempted')

        kwargs['OCSP_ValidCacheTimeout'] = val_cache_t
        kwargs['OCSP_InvalidCacheTimeout'] = inval_cache_t
        kwargs['OCSP_NetworkErrorCacheTimeout'] = net_cache_t
        kwargs['OCSP_ClockSkew'] = clock_skew
        kwargs['OCSP_MaxTimeForOCSPResponse'] = max_time_resp
        """ Set upstream_proxy implicitly to 'Y'
        if upstream_proxy_grp is specified .
        """
        if upstream_proxy_grp:
            upstream_proxy = 'Y'
        upstream_proxy = self._process_yes_no(upstream_proxy)
        kwargs['OCSP_UpstreamProxy'] = upstream_proxy
        crypt_nonce = self._process_yes_no(crypt_nonce)
        kwargs['OCSP_cryptnonce'] = crypt_nonce

        if(any([exempted_server,delete_exempted,\
                clear_all_exempted])):
                kwargs['OCSP_ServerExempt'] = 'Y'
                kwargs['OCSP_UpstreamProxy'] = 'Y'
                kwargs['OCSP_UpstreamProxySelect'] = upstream_proxy_grp

        p = re.compile('y',re.IGNORECASE)
        m = p.match( kwargs['OCSP_UpstreamProxy'] )
        if m:
            kwargs['OCSP_UpstreamProxySelect'] = upstream_proxy_grp
            kwargs['OCSP_ServerExempt'] = 'N'

            if exempted_server:
                kwargs['OCSP_ServerExemptACTION'] = 'NEW'
                kwargs['OCSP_ServerExemptList'] =  exempted_server
                self._cli.ocspconfig()._processwithserverExemption(**kwargs)
                return
            if clear_all_exempted:
                kwargs['OCSP_ServerExemptACTION'] = 'CLEAR'
                self._cli.ocspconfig()._processwithserverExemption(**kwargs)
                return
            if delete_exempted:
                kwargs['OCSP_ServerExemptACTION'] = 'DELETE'
                kwargs['OCSP_ServerExemptList'] = delete_exempted
                self._cli.ocspconfig()._processwithserverExemption(**kwargs)
                return
        self._cli.ocspconfig().enable(**kwargs)

    def _ocsp_config_disable(self):
        """Disables OCSP through CLI"""
        kwargs = { }
        self._cli.ocspconfig().disable(**kwargs)

    def ocsp_config(self,enable_ocsp=DEFAULT,
                         val_cache_t=DEFAULT,
                         inval_cache_t=DEFAULT,
                         net_cache_t=DEFAULT,
                         clock_skew=DEFAULT,
                         max_time_resp=DEFAULT,
                         upstream_proxy='N',
                         upstream_proxy_grp=DEFAULT,
                         crypt_nonce='N',
                         exempted_server=DEFAULT,
                         delete_exempted=DEFAULT,
                         clear_all_exempted=DEFAULT
                           ):
        """ Enables or Disables OCSP(Online Certificate Status Protocol)
              with the settings provided .

        cli -> ocspconfig

        Parameters:
        - `enable_ocsp`: Used to either enable or disable OCSP
                               Either True or False
        - `val_cache_t`: Valid response cache timeout(between
                              1 second and 7 days).
                            Use a trailing 's' for seconds, 'm' for minutes
                               'h' for hours or 'd' for days.

        - `inval_cache_t`: Invalid response cache timeout(between
                                 1 second and 7 days).
                                Use a trailing 's' for seconds, 'm' for minutes
                                 'h' for hours or 'd' for days.

        - `net_cache_t`: Network error cache timeout(between
                                     1 second and 24 hours).
                                      Use a trailing 's' for seconds,
                                      'm' for minutes or 'h' for hours.

        - `clock_skew`: Allowed clock skew between the OCSP responder and WSA
                       (between 1 second and 60 minutes).
                       Use a trailing 's' for seconds or 'm' for minutes.

        - `max_time_resp`: Maximum time for the WSA to wait for an OCSP
                                   response(between 1 second and 10 minutes).
                                    Use a trailing 's' for seconds or
                                    'm' for minutes.

        - `crypt_nonce`: Use nonce to cryptographically bind OCSP
                        requests and responses.
                        Either 'Yes' or 'No'.

        - `upstream_proxy`: Use an upstream proxy for OCSP checking.
                           Either 'Yes' or 'No'.
                           Note - Upstream Proxy is disabled by default.

        - `upstream_proxy_grp`: Select an upstream proxy group
                                for OCSP checking.
                                 Note- The first proxy group is selected
                                 if None is specified.

        - `exempted_server`: Specify servers exempt from upstream proxy
                            in a comma or space separated format

        - `delete_exempted`: Specify the server to be deleted
                                   from the exemption list

        - `clear_all_exempted`: Delete all servers from the exemption list
                                       Specify 'Yes' or 'Y' to clear all
                                       servers from the exemption list

        Note: Either exempted_server or delete_exempted or
                                        clear_all_exempted operation
                                        can be specified at a time

        Prerequisites: 1.HTTPS Proxy Needs to be Enabled for OCSP settings
                       to be enabled
                       2.Atleast one Upstream Proxy group needs to be present
                       for operations related to Upstream Proxy group.

        Examples:

        |  OCSP Config  |
        | ... |  enable_ocsp=${True} |
        | ... |  clock_skew=5m  |
        | ... |  inval_cache_t=5m   |
        | ... |  val_cache_t=5m  |
        | ... |  max_time_resp=5m |
        | ... |  crypt_nonce=Y  |
        | ... |  net_cache_t=5m  |
        | ... |  upstream_proxy_grp=grp1  |
        | ... |  exempted_server= 1.1.1.1 2.2.2.2  |

        | OCSP Config  |
        | ...|  enable_ocsp=${True} |
        |...|  clear_all_exempted=Y |

        | OCSP Config  |
        | ...|  enable_ocsp=${False} |

        """
        if not enable_ocsp:
            self._ocsp_config_disable()
        else:
            self._ocsp_config_enable(val_cache_t=val_cache_t,
                                     inval_cache_t=inval_cache_t,
                                     net_cache_t=net_cache_t,
                                     clock_skew=clock_skew,
                                     max_time_resp=max_time_resp,
                                     upstream_proxy=upstream_proxy,
                                     upstream_proxy_grp=upstream_proxy_grp,
                                     crypt_nonce=crypt_nonce,
                                     exempted_server=exempted_server,
                                     delete_exempted=delete_exempted,
                                     clear_all_exempted=clear_all_exempted)
