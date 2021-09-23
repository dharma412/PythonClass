#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/dest_config.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class DestConfig(CliKeywordBase):
    """Destination Configuration."""

    def get_keyword_names(self):
        return ['dest_config_new',
                'dest_config_edit',
                'dest_config_default',
                'dest_config_detail',
                'dest_config_list',
                'dest_config_delete',
                'dest_config_clear',
                'dest_config_setup']

    def dest_config_new(self, *args):
        """Create a new destination.

        destconfig > new

        Parameters:
        - `domain`: an IP address or a hostname. Ex: 192.168.1.1 or dest.com
        - `concurrency_config`: configure or not a concurrency limit for domain.
        Either _Yes_ or _No_.
        - `concurrency`: maximum concurrency limit. Default is _500_.
        - `msg_per_conn`: apply or not a messages-per-connection limit to domain.
        Either _Yes_ or _No_.
        - `msg_per_conn_limit`: maximum number of messages to deliver per
        connection. Default is _50_.
        - `limit_config`: apply or not a recipient limit to domain.
        Either _Yes_ or _No_.
        - `limit`: number of minutes used to measure the recipients limit.
        Default is _60_.
        - `recipients`: maximum number of recipients per `limit` minutes for
        domain. Required parameter if limit_config=yes
        - `limits_apply`: specify how to apply the limits for each host.
        Either _'One limit'_(1) or _'Separate limit'_(2).
        - `limits_enforced`: specify how limits will be enforced. Either
        _'System Wide'_(1) or _'Per Virtual Gateway(tm)'_(2).
        - `tls_apply`: apply or not a specific TLS setting for domain.
        Either _Yes_ or _No_.
        - `tls_use`: use or not TLS support. Can be _No_(1), _Preferred_(2),
        _Required_(3), _Preferred(Verify)_(4) or _Required(Verify)_(5).
        - `address_apply`: apply or not a specific bounce verification address
        tagging setting for domain. Either _Yes_ or _No_.
        - `address_perform`: perform or not bounce verification address tagging.
        Either _Yes_ or _No_.
        - `profile_apply`: apply or not a specific bounce profile to domain.
        Either _Yes_ or _No_.
        - `profile`: choose a bounce profile to apply: _Default_(1) or
        _New Profile_(2)
        - `profile_name`: name of profile. Required parameter if profile=2

        Examples:
        | Dest Config New |
        | ... | domain=test.com |

        | Dest Config New |
        | ... | domain=191.1.1.1 |
        | ... | concurrency_config=YES |
        | ... | concurrency=400 |
        | ... | msg_per_conn=YES |
        | ... | msg_per_conn_limit=55 |
        | ... | limit_config=YES |
        | ... | limit=40 |
        | ... | recipients=300 |
        | ... | limits_apply=Separate limit |
        | ... | limits_enforced=System Wide |
        | ... | tls_apply=YES |
        | ... | tls_use=Preferred |
        | ... | profile_apply=YES |
        | ... | profile=New Profile |
        | ... | profile_name=profile |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.destconfig().new(**kwargs)

    def dest_config_edit(self, *args):
        """Modify a destination.

        destconfig > edit

        Parameters:
        - `domain`: an IP address or a hostname. Ex: 192.168.1.1 or dest.com
        - `concurrency_config`: configure or not a concurrency limit to domain.
        Either _Yes_ or _No_.
        - `concurrency`: maximum concurrency limit. Default is _500_.
        - `msg_per_conn`: apply or not a messages-per-connection limit to domain.
        Either _Yes_ or _No_.
        - `msg_per_conn_limit`: maximum number of messages to deliver per
        connection. Default is _50_.
        - `limit_config`: apply or not a recipient limit to domain.
        Either _Yes_ or _No_.
        - `limit`: number of minutes used to measure the recipients limit.
        Default is _60_.
        - `recipients`: maximum number of recipients per `limit` minutes for
        domain.
        - `limits_apply`: specify how to apply the limits for each host.
        Either _'One limit'_(1) or _'Separate limit'_(2).
        - `limits_enforced`: specify how limits will be enforced. Either
        _'System Wide'_(1) or _'Per Virtual Gateway(tm)'_(2).
        - `tls_apply`: apply or not a specific TLS setting for domain.
        Either _Yes_ or _No_.
        - `tls_use`: use or not TLS support. Can be _No_(1), _Preferred_(2),
        _Required_(3), _Preferred(Verify)_(4) or _Required(Verify)_(5).
        - `address_apply`: apply or not a specific bounce verification address
        tagging setting for domain. Either _Yes_ or _No_.
        - `address_perform`: perform or not bounce verification address tagging.
        Either _Yes_ or _No_.
        - `profile_apply`: apply or not a specific bounce profile to domain.
        Either _Yes_ or _No_.
        - `profile`: choose a bounce profile to apply: _Default_(1) or
        _New Profile_(2)
        - `profile_name`: name of profile.

        Examples:
        | Dest Config Edit |
        | ... | domain=191.1.1.2 |
        | ... | concurrency_config=YES |
        | ... | concurrency=123 |
        | ... | msg_per_conn=YES |
        | ... | msg_per_conn_limit=60 |
        | ... | limit_config=YES |
        | ... | limit=40 |
        | ... | recipients=300 |
        | ... | limits_apply=One limit |
        | ... | limits_enforced=Per Virtual Gateway(tm) |
        | ... | tls_apply=YES |
        | ... | tls_use=Preferred(Verify) |
        | ... | profile_apply=YES |
        | ... | profile=2 |
        | ... | profile_name=profile3 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.destconfig().edit(**kwargs)

    def dest_config_default(self, *args):
        """Change the default destination.

        destconfig > default

        Parameters:
        - `concurrency`: maximum concurrency limit. Default is _500_.
        - `msg_per_conn_limit`: maximum number of messages to send per
        connection. Default is _50_.
        - `limit_config`: specify or not a default recipient limit.
        Either _Yes_ or _No_.
        - `limit`: number of minutes used to measure recipient limit.
        Default is _60_.
        - `recipients`: number of recipients. Default is _500_.
        - `limits_apply`: specify how to apply the limits for each host.
        Either _'One limit'_(1) or _'Separate limit'_(2).
        - `limits_enforced`: specify how limits will be enforced. Either
        _'System wide'_(1) or _'Per Virtual Gateway(tm)'_(2).
        - `tls_use`: use or not TLS support. Can be _No_(1), _Preferred_(2),
        _Required_(3), _Preferred(Verify)_(4) or _Required(Verify)_(5).
        - `address_perform`: perform or not bounce verification address
        tagging. Either _Yes_ or _No_.

        Examples:
        | Dest Config Default |
        | ... | concurrency=123 |
        | ... | msg_per_conn_limit=52 |
        | ... | limit_config=YES |
        | ... | limit=40 |
        | ... | recipients=300 |
        | ... | limits_apply=One limit |
        | ... | limits_enforced=Per Virtual Gateway |
        | ... | tls_use=Preferred(Verify) |
        | ... | address_perform=NO |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.destconfig().default(**kwargs)

    def dest_config_detail(self, domain):
        """Display details for one destination or all destinations.

        destconfig > detail

        Parameters:
        - `domain`: accepts the domain name to view, _DEFAULT_ to view details
        for the default, or _ALL_ to view details for all

        Examples:
        | Dest Config Detail | 191.1.1.1 |
        | Dest Config Detail | all |
        | Dest Config Detail | default |
        """
        out = self._cli.destconfig().detail(domain)
        self._info(out)
        return out

    def dest_config_list(self):
        """Display a summary list of all destinations.

        destconfig > list

        Examples:
        | Dest Config List |
        """
        out = self._cli.destconfig().list()
        self._info(out)
        return out

    def dest_config_delete(self, domain):
        """Remove a destination.

        destconfig > delete

        Parameters:
        - `domain`: an IP address or a hostname. Ex: 192.168.1.1 or dest.com

        Examples:
        | Dest Config Delete | 191.1.1.1 |
        """
        self._cli.destconfig().delete(domain)

    def dest_config_clear(self):
        """Remove all destinations.

        destconfig > clear

        Examples:
        | Dest Config Clear |
        """
        self._cli.destconfig().clear()

    def dest_config_setup(self, *args):
        """Change global settings.

        destconfig > setup

        Parameters:
        - `send_alert`: to send or not an alert when TLS connection fails.
        Either _Yes_ or _No_.

        Examples:
        | Dest Config Setup |
        | Dest Config Setup | Yes |
        | Dest Config Setup | No |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.destconfig().setup(**kwargs)
