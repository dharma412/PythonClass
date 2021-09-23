#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/destconfig.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase


class destconfig(CliKeywordBase):

    """Keywords for dnsconfig CLI command."""

    def get_keyword_names(self):
        return ['destconfig_new',
                'destconfig_edit',
                'destconfig_delete',
                'destconfig_default',
                'destconfig_detail',
                'destconfig_clear',
                'destconfig_setup',
                'destconfig_list']

    def destconfig_new(self, domain, *args):
        """Create new config for outbound host limits and delivery settings.

        destconfig > new

        *Parameters:*
        - `domain`: domain name, that needs to be configured, mandatory
        - `concurrency_config`: whether to configure concurrency limit, yes or no
        - `concurrency`: the maximum concurrency limit for a specific host, number
        - `limit_config`: whether to apply a recipient limit, yes or no
        - `limit`: the number of minutes used to measure the recipient limit, number
        - `recipients`: max number of recipients to limit per <limit> minutes of time,
        number
        - `limits_apply`: how you want to apply the limits for domain, either
        | 1 | One limit applies to the entire domain |
        | 2 | Separate limit for each mail exchanger IP address |
        - `limits_enforced`: how the limits will be enforced, either
        | 1 | System Wide |
        | 2 | Per Virtual Gateway(tm) |
        - `messages_apply`: whether to apply a messages-per-connection limit, yes or no
        - `messages_limit`: max number of messages to deliver per connection., number
        - `tls_apply`: whether to apply a specific TLS setting, yes or no
        - `tls_use`: whether TLS should be on, off, or required for
        a given host. Either
        | 1 | off |
        | 2 | on |
        | 3 | require |
        | 4 | on_verify |
        | 5 | require_verify |
        - `dane_apply`: whether to apply a specific DANE setting, yes or no
        - `dane_use`: whether DANE should be on, No, or Preferred for
        a given host. Either
        | 1 | No |
        | 2 | Opportunistic |
        | 3 | Mandatory |
        - `demo_certificate`: path to a demo certificate
        - `address_apply`: whether to apply a specific bounce verification, yes or no
        - `address_perform`: whether to perform bounce verification address tagging,
        yes or no
        - `profile_apply`: whether apply a specific bounce profile to this domain, yes or no
        - `profile`: a bounce profile to apply, either
        | 1 | Default |
        | 2 | New Profile |
        - `profile_name`: the bounce profile name to use (if new)
        - `ip_preference_apply`: whether to apply IP sort preferences, yes or no
        - `ip_preference`: how should the appliance sort IP addresses within an MX
        preference level, either
        | 1 | Prefer IPv4 |
        | 2 | Prefer IPv6 |
        | 3 | Require IPv4 |
        | 4 | Require IPv6 |

        *Return:*
        Raw output

        *Examples:*
        | Destconfig New | 191.1.1.1 | concurrency_config=YES | concurrency=400 |
        | ... | limit_config=YES | limit=40 | recipients=300 |
        | ... | limits_apply=Separate limit | limits_enforced=System Wide |
        | ... | tls_apply=YES | tls_use=Preferred | profile_apply=YES |
        | ... | profile=New Profile | profile_name=profile |
        | ... | ip_preference_apply=YES | ip_preference=Require IPv6 |
        | Destconfig New | 1.1.1.1 | limit_config=yes |
        | ... | limit=60 | recipients=1 | limits_apply=1 | limits_enforced=1 |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.destconfig().new(domain=domain, **kwargs)

    def destconfig_edit(self, domain, *args):
        """Edit existing config for outbound host limits and delivery settings.

        destconfig > edit

        *Parameters:*
        - `domain`: domain name, that needs to be configured, mandatory
        - `concurrency_config`: whether to configure concurrency limit, yes or no
        - `concurrency`: the maximum concurrency limit for a specific host, number
        - `limit_config`: whether to apply a recipient limit, yes or no
        - `limit`: the number of minutes used to measure the recipient limit, number
        - `recipients`: max number of recipients to limit per <limit> minutes of time,
        number
        - `limits_apply`: how you want to apply the limits for domain, either
        | 1 | One limit applies to the entire domain |
        | 2 | Separate limit for each mail exchanger IP address |
        - `limits_enforced`: how the limits will be enforced, either
        | 1 | System Wide |
        | 2 | Per Virtual Gateway(tm) |
        - `messages_apply`: whether to apply a messages-per-connection limit, yes or no
        - `messages_limit`: max number of messages to deliver per connection., number
        - `tls_apply`: whether to apply a specific TLS setting, yes or no
        - `tls_use`: whether TLS should be on, off, or required for
        a given host. Either
        | 1 | off |
        | 2 | on |
        | 3 | require |
        | 4 | on_verify |
        | 5 | require_verify |
        - `dane_apply`: whether to apply a specific DANE setting, yes or no
        - `dane_use`: whether DANE should be on, No, or Preferred for
        a given host. Either
        | 1 | No |
        | 2 | Opportunistic |
        | 3 | Mandatory |

        - `demo_certificate`: path to a demo certificate (if TLS required)
        - `address_apply`: whether to apply a specific bounce verification, yes or no
        - `address_perform`: whether to perform bounce verification address tagging,
        yes or no
        - `profile_apply`: whether apply a specific bounce profile to this domain, yes or no
        - `profile`: a bounce profile to apply, either
        | 1 | Default |
        | 2 | New Profile |
        - `profile_name`: the bounce profile name to use (if new)
        - `ip_preference_apply`: whether to apply IP sort preferences, yes or no
        - `ip_preference`: how should the appliance sort IP addresses within an MX
        preference level, either
        | 1 | Prefer IPv4 |
        | 2 | Prefer IPv6 |
        | 3 | Require IPv4 |
        | 4 | Require IPv6 |

        *Return:*
        Raw output

        *Examples:*
        | Destconfig Edit | 1.1.1.1 | concurrency_config=yes | concurrency=1 |
        | Destconfig Edit | 1.1.1.1 | limit_config=yes |
        | ... | limit=60 | recipients=1 | limits_apply=1 | limits_enforced=1 |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.destconfig().edit(domain=domain, **kwargs)

    def destconfig_delete(self, domain):
        """Delete existing config for outbound host limits and delivery settings.

        destconfig > delete

        *Parameters:*
        - `domain`: existing domain name, that needs to be deleted, mandatory

        *Examples:*
        | Destconfig Delete | 1.1.1.1 |
        """
        self._cli.destconfig().delete(domain)

    def destconfig_default(self, *args):
        """Edit default parameters for all existing outbound host
        limits and delivery settings

        destconfig > default

        *Parameters:*
        - `concurrency`: the default maximum concurrency limit , number
        - `limit_config`: whether to specify a default recipient limit, yes or no
        - `limit': number of minutes used to measure recipient limit
        - `recipients` : number of allowed recipients per <limit> min
        - `limits_apply`: how you want to apply the limits for domain, either
        | 1 | One limit applies to the entire domain |
        | 2 | Separate limit for each mail exchanger IP address |
        - `limits_enforced`: how the limits will be enforced, either
        | 1 | System Wide |
        | 2 | Per Virtual Gateway(tm) |
        - `messages_limit`: the default maximum number of messages to send per connection
        - `tls_use`: whether TLS should be on, off, or required for
        a given host. Either
        | 1 | off |
        | 2 | on |
        | 3 | require |
        | 4 | on_verify |
        | 5 | require_verify |
        - `dane_use`: whether DANE should be on, No, or Preferred for
        a given host. Either
        | 1 | No |
        | 2 | Opportunistic |
        | 3 | Mandatory |

        - `demo_certificate`: path to a demo certificate (if TLS required)
        - `address_perform`: whether to perform bounce verification address tagging,
        yes or no
        - `ip_preference`: how should the appliance sort IP addresses within an MX
        preference level, either
        | 1 | Prefer IPv4 |
        | 2 | Prefer IPv6 |
        | 3 | Require IPv4 |
        | 4 | Require IPv6 |

        *Examples:*
        | Destconfig Default | 1.1.1.1 | concurrency=500 | limit_config=yes |
        | ... | limit=60 | recipients=2 |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.destconfig().default(**kwargs)

    def destconfig_detail(self, domain='all'):
        """Show details for all existing outbound host limits and delivery settings

        destconfig > detail

        *Parameters:*
        - `domain`: domain name to show details for ('all' by default)

        *Return:*
        Raw output

        *Examples:*
        | ${details} | Destconfig Detail |
        | Log | ${details} |
        """
        return self._cli.destconfig().detail(domain)

    def destconfig_list(self):
        """List all existing outbound host limits and delivery settings

        destconfig > list

        *Return:*
        Raw output

        *Examples:*
        | ${all_domains} | Destconfig List |
        | Log | ${all_domains} |
        """
        return self._cli.destconfig().list()

    def destconfig_clear(self):
        """Clear configs for all existing outbound host
        limits and delivery settings

        destconfig > clear

        *Examples:*
        | Destconfig Clear |
        """
        self._cli.destconfig().clear()

    def destconfig_setup(self, *args):
        """Change global settings for all destination domain

        destconfig > setup

        *Parameters:*
        - `cert_name`: path to demo certificate (if not configured)
        - `send_alert`: whether to send an alert when a required TLS connection fails,
        yes or no

        *Return:*
        Raw output

        *Examples:*
        | ${details} | Destconfig Setup | cert_name=123.cert | send_alert=yes |
        | Log | ${details} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.destconfig().setup(**kwargs)
