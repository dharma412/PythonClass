# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm115/cm115_offbox_dlp_policies.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from coeus1100.gui.manager.offbox_dlp_policies import OffboxDlpPolicies


class Cm110OffboxDlpPolicies(OffboxDlpPolicies):
    """
    Keywords for Web -> Configuration Master 11.5 -> External Data Loss Prevention
    """

    def _open_page(self):
        self._navigate_to('Web', 'Configuration Master 11.5', 'External Data Loss Prevention')

    def get_keyword_names(self):
        return [
            'cm115_offbox_dlp_policies_add',
            'cm115_offbox_dlp_policies_delete',
            'cm115_offbox_dlp_policies_edit',
            'cm115_offbox_dlp_policies_edit_destinations'
        ]

    def cm115_offbox_dlp_policies_add(self,
                                      name,
                                      description=None,
                                      order=1,
                                      identities='Global Identity Policy',
                                      protocols=None,
                                      proxy_ports=None,
                                      subnets=None,
                                      url_categories=None,
                                      user_agents=None,
                                      match_agents=True):
        """Add new DLP policy from Configuration Master 11.5

        *Parameters*
        - `name`: name for the policy group to add. String.
        - `description`: description for the policy. String.
        - `order`: the processing order. String.
        - `identities`: String of comma separated values of identities. Format
           of an identity is described <a href="policy_base.html#identities">here</a>
        - `protocols`: the protocols where policy is a member. String of comma
           separated values. The following values are currently accepted:
           * http
           * ftpoverhttp
           * nativeftp
           * others
           * https
        - `proxy_ports`: The ports where policy is a member. String of comma
           separated values
        - `subnets`: the nets where policy is member. String of comma separated
           values in format of IP, IP range or CIDR.
        - `url_categories`: the URL categories where policy is a member.
           String of comma separated values. The categories are described here:
           http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst
        - `user_agents`: the user agents where policy is a member.
           String of comma separated values
        - `match_agents`: match selected user agents. Boolean. Default to True.

        *Exceptions*
        - `ValueError`: wrong format of identity.
        - `ValueError`: in case of proxy ports, time ranges, subnet membership or url
            categories is disabled in advanced policy menu.

        *Examples*
        | CM115 Offbox DLP Policies Add | three | description=Adding policy  |
        | ... | order=1 | identities=Global Identity Policy |
        | ... | protocols=http, ftpoverhttp | proxy_ports=1234, 5321 |
        | ... | subnets=10.1.1.0/24, 1.2.3.44 |
        | ... | url_categories=${webcats.ADULT}, ${webcats.ARTS} |
        | ... | user_agents=ie-all | match_agents=${False} |
        | CM115 Offbox DLP Policies Add | zero |
        """
        self.offbox_dlp_policies_add(
            name,
            description=description,
            order=order,
            identities=identities,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            match_agents=match_agents)

    def cm115_offbox_dlp_policies_edit(self,
                                       name,
                                       new_name=None,
                                       description=None,
                                       order=1,
                                       identities='Global Identity Policy',
                                       protocols=None,
                                       proxy_ports=None,
                                       subnets=None,
                                       url_categories=None,
                                       user_agents=None,
                                       match_agents=True):
        """Edit DLP policy from Configuration Master 11.5

        *Parameters*
        - `name`: name for the policy group to add. String.
        - `new_name`: new name for the policy. Optional. String
        - `description`: description for the policy. String.
        - `order`: the processing order. String.
        - `identities`: String of comma separated values of identities. Format
           of an identity is described <a href="policy_base.html#identities">here</a>
        - `protocols`: the protocols where policy is a member. String of comma
           separated values. The following values are currently accepted:
           * http
           * ftpoverhttp
           * nativeftp
           * others
           * https
        - `proxy_ports`: The ports where policy is a member. String of comma
           separated values
        - `subnets`: the nets where policy is member. String of comma separated
           values in format of IP, IP range or CIDR.
        - `url_categories`: the URL categories where policy is a member.
           String of comma separated values. The categories are described here:
           http://eng.ironport.com/docs/qa/sarf/keyword/common/webcats.rst
        - `user_agents`: the user agents where policy is a member.
           String of comma separated values
        - `match_agents`: match selected user agents. Boolean. Default to True.

        *Exceptions*
        - `ValueError`: wrong format of identity.
        - `ValueError`: in case of proxy ports, time ranges, subnet membership or url
            categories is disabled in advanced policy menu.

        *Examples*
        | CM115 Offbox DLP Policies Edit |
        | ... | three | description=Editing policy |
        | ... | order=1 | identities=Global Identity Policy |
        | ... | protocols=http, ftpoverhttp | proxy_ports=12345, 54321 |
        | ... | subnets=10.1.1.0/24 | url_categories=${webcats.ADULT} |
        | ... | user_agents=ie-all, ff3 |
        | CM115 Offbox DLP Policies Edit | zero | protocols=others |
        """
        self.offbox_dlp_policies_edit(
            name,
            new_name=new_name,
            description=description,
            order=order,
            identities=identities,
            protocols=protocols,
            proxy_ports=proxy_ports,
            subnets=subnets,
            url_categories=url_categories,
            user_agents=user_agents,
            match_agents=match_agents)

    def cm115_offbox_dlp_policies_delete(self, name):
        """Delete DLP policy from Configuration Master 11.5

        *Parameters*
        - `name`: name of the policy to delete.

        *Exception*
        - `GuiControlNotFoundError`: policy with such name not presents.

        *Examples*
        | CM115 Offbox DLP Policies Delete | three |
        """
        self.offbox_dlp_policies_delete(name)

    def cm115_offbox_dlp_policies_edit_destinations(self,
                                                    name,
                                                    scan_uploads=None,
                                                    url_categories=None,
                                                    settings_type=None):
        """Edit the WBRS and anti-malware for the DLP policy
         from Configuration Master 11.5

        *Parameters*
        - `name`: name of the policy to edit.
        - `scan_uploads`:
           * off -> Do not scan any uploads
           * all  -> Scan all uploads
           * except -> Scan uploads to specified custom URL categories
        - `url_categories`: List of excluded in scan custom URL categories
        - `settings_type`: settings type to use. Accepted values:
           * 'global' - Use Destinations scanning Global Policy Settings
           * 'custom' - Define Destinations scanning Custom Settings
           * 'disable' - Disable Destinations scanning for this Policy


        *Exceptions*
        - `GuiControlNotFoundError`: if such category not present.
        - `ValueError`: if blocking settings are invalid.

        *Examples*
        It is expected that custom url categories 'cat1' and 'dog2' exist
        | OffboxDLP Policies Edit Destinations | three |
        | ... | scan_uploads=except | url_categories=cat1, dog2 |
        | ... | settings_type=custom |
        | OffboxDLP Policies Edit Destinations | zero | scan_uploads= all |
        """
        self.offbox_dlp_policies_edit_destinations(
            name,
            scan_uploads=scan_uploads,
            url_categories=url_categories,
            settings_type=settings_type)
