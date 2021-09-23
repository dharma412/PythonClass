#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/encryption_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class EncryptionConfig(CliKeywordBase):
    """
    Manage PXE Email Encryption settings.
    CLI command: encryptionconfig
    """

    def get_keyword_names(self):
        return ['encryption_config_setup',
                'encryption_config_provision',
                'encryption_config_profiles_new',
                'encryption_config_profiles_delete',
                'encryption_config_profiles_print',
                'encryption_config_profiles_clear',
                'encryption_config_profiles_proxy',
                'encryption_config_profiles_edit_name',
                'encryption_config_profiles_edit_url_external',
                'encryption_config_profiles_edit_url_internal',
                'encryption_config_profiles_edit_proxy',
                'encryption_config_profiles_edit_algorithm',
                'encryption_config_profiles_edit_payload',
                'encryption_config_profiles_edit_security',
                'encryption_config_profiles_edit_receipt',
                'encryption_config_profiles_edit_forward',
                'encryption_config_profiles_edit_replyall',
                'encryption_config_profiles_edit_applet',
                'encryption_config_profiles_edit_url',
                'encryption_config_profiles_edit_bounce_subject',
                'encryption_config_profiles_edit_timeout',
                'encryption_config_profiles_edit_filename',
                'encryption_config_profiles_edit_localized_envelope',
                'encryption_config_profiles_edit_default_locale']

    def encryption_config_setup(self, *args):
        """Enable/Disable IronPort Email Encryption.

        CLI command: encryptionconfig > setup

        *Parameters:*
        - `use_pxe`: Use PXE Email Encryption. YES or NO. YES by default.
        - `confirm_disable`: Confirm disabling PXE. Either YES or NO.
        - `license_agreement`: Accept agreement. YES or NO.
        - `max_enc_msg_size` : Maximum message size for encryption
                               Add a trailing K for kilobytes, M for megabytes,
                                or no letters for bytes
        - `email_address` : email address of the encryption account administrator

        *Return:*
        None

        *Examples:*
        | Encryption Config Setup | use_pxe=yes | license_agreement=y |
        | Encryption Config Setup | use_pxe=no | confirm_disable=y |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().setup(**kwargs)

    def encryption_config_provision(self, *args):
        """Provision encryption profile.

        CLI command: encryptionconfig > setup

        *Parameters:*
        - `name`: The encryption profile to provision. String.

        *Return:*
        None

        *Examples:*
        | Encryption Config Provision | name=${cisco1} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().provision(**kwargs)

    def encryption_config_profiles_new(self, *args):
        """Create new encryption profile.

        CLI command: encryptionconfig > profiles > new

        *Parameters:*
        - `type`: A key service type. Either 'Cisco' or 'IronPort'.
        - `name`: A name for the encryption profile. String.
        - `alter_cisco_url`: Alter the Cisco Registered Envelope Service URL. Either YES or NO.
        - `cisco_url`: The new URL.
        - `external_url`': An external URL.
        - `internal_url`: An internal URL.
        - `use_proxy`:  Use the configured key server proxy. Either YES or NO.
        - `algorithm`: The encryption algorithm to use when encrypting envelopes.
        Either 'ARC4', 'AES-192' or 'AES-256'.
        - `enable_read_receipts`:  Enable read receipts. Either YES or NO.
        - `security_level`: Envelope security level.
        - `enable_secure_reply`: Enable "Secure Reply All". Either YES or NO.
        - `enable_secure_forward`: Enable "Secure Forward". Either YES or NO.
        - `logo_url`: Link for the envelope logo image. Optional.
        - `max_sec_in_queue`: The maximum number of seconds for which a message could remain queued waiting to be encrypted. Optional.
        - `fail_notification`: The subject to use for failure notifications. Optional.
        - `notif_tmpl`: Select a text notification template.
        - `notif_html_tmpl`: Select an HTML notification template.
        - `payload_url`: Configure the Payload Transport URL. Use either '1', '2' or '3':
        | _1_ | _Use envelope service URL with HTTP_ |
        | _2_ | _Use the envelope service URL with HTTPS_ |
        | _3_ | _Specify a separate URL for payload transport_ |
        - `separate_url`: An URL for payload transport.
        - `env_filename`: The file name of the envelope attached.
        - `assign_user`: Assign any user roles. Either YES or NO.
        - `action`: Add or Delete user role. Either 'Add' or 'Delete'.
        - `role`: The role to add/delete. Select one or more user role names, separated by a comma.
        - `display_language`: envelopes to be displayed in a language other than English ? Either YES or NO

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles New |
        | ... | type=IronPort |
        | ... | name=iron1 |
        | ... | external_url=http://internal.qa |
        | ... | internal_url=http://external.qa |
        | ... | algorithm=AES-192 |
        | ... | enable_read_receipts=yes |
        | ... | enable_secure_reply=yes |
        | ... | enable_secure_forward=yes |
        | ... | security_level=high |
        | ... | logo_url=http://logo.img |
        | ... | max_sec_in_queue=14000 |
        | ... | payload_url=3 |
        | ... | separate_url=http://separate.qa |
        | ... | fail_notification=ENCRYPTION FAILURE IRON |

        | Encryption Config Profiles New |
        | ... | type=Cisco |
        | ... | name=cisco1 |
        | ... | alter_cisco_url=yes |
        | ... | cisco_url=http://cres.local.qa |
        | ... | algorithm=AES-256 |
        | ... | payload_url=1 |
        | ... | enable_read_receipts=yes |
        | ... | enable_secure_reply=no |
        | ... | enable_secure_forward=yes |
        | ... | security_level=medium |
        | ... | logo_url=http://logo.img |
        | ... | max_sec_in_queue=10000 |
        | ... | fail_notification=ENCRYPTION FAILURE CISCO |
        | ... | env_filename=securedoc_boo.html |
        | ... | use_proxy=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles().new(**kwargs)

    def encryption_config_profiles_delete(self, *args):
        """Delete encryption profile.

        CLI command: encryptionconfig > profiles > delete

        *Parameters:*
        - `name`: A name of the encryption profile to delete.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Delete | name=iron1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles().delete(**kwargs)

    def encryption_config_profiles_print(self, *args):
        """Print the list of encryption profiles.

        CLI command: encryptionconfig > profiles > print

        *Parameters:*
        - `raw`: The output(raw or formatted). Either YES or NO. NO by default.

        *Return:*
        None

        *Examples:*
        | ${profiles}= | Encryption Config Profiles Print |
        | Log List | ${profiles} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.encryptionconfig().profiles().print_profiles(**kwargs)

    def encryption_config_profiles_clear(self):
        """Clear the list of encryption profiles.

        CLI command: encryptionconfig > profiles > clear

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Clear |
        """
        self._cli.encryptionconfig().profiles().clear()

    def encryption_config_profiles_proxy(self, *args):
        """Configure a key server proxy.

        CLI command: encryptionconfig > profiles > proxy

        *Parameters:*
        - `type`: The type of proxy.
        Either 'Web' or 'SOCKS4' or 'SOCKS5'.
        - `hostname`: The proxy hostname.
        - `port`: The proxy port.
        - `user`: The proxy user.
        - `password`: The proxy user's password.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Proxy |
        | ... | type=Web |
        | ... | hostname=proxy.qa |
        | ... | port=8888 |
        | ... | user=admin |
        | ... | password=ironport |

        | Encryption Config Profiles Proxy |
        | ... | type=SOCKS4 |
        | ... | hostname=proxys.qa |
        | ... | port=2233 |
        | ... | user=admin |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles().proxy(**kwargs)

    def encryption_config_profiles_edit_name(self, *args):
        """Change profile name.

        CLI command: encryptionconfig > profiles > edit > name

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `new_name`: The new name of the encryption profile. String. Optional.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Name | name=old_name | new_name=new_name |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).name(**kwargs)

    def encryption_config_profiles_edit_url_external(self, *args):
        """Change external URL.

        CLI command: encryptionconfig > profiles > edit > external

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `url`: The new external URL value. String. Optional.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Url External | name=profile_name | url=http://new_babar.qa |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).external(**kwargs)

    def encryption_config_profiles_edit_url_internal(self, *args):
        """Change internal URL.

        CLI command: encryptionconfig > profiles > edit > internal

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `url`: The new internal URL value. String. Optional.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Url Internal | name=profile_name | url=http://new_boo.qa |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).internal(**kwargs)

    def encryption_config_profiles_edit_proxy(self, *args):
        """Change internal URL.

        CLI command: encryptionconfig > profiles > edit > proxy

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `use_proxy`: Use configured key server proxy. Either YES or NO.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Proxy | name=some_name | use_proxy=y |
        | Encryption Config Profiles Edit Proxy | name=some_name | use_proxy=n |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).proxy(**kwargs)

    def encryption_config_profiles_edit_algorithm(self, *args):
        """Change encryption algorithm.

        CLI command: encryptionconfig > profiles > edit > algorithm

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `algorithm`: Change encryption algorithm. String.
        Either 'ARC4', 'AES-192' or 'AES-256'.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Algorithm | name=pr_name | algorithm=ARC4 |
        | Encryption Config Profiles Edit Algorithm | name=pr_name | algorithm=AES-192 |
        | Encryption Config Profiles Edit Algorithm | name=pr_name | algorithm=AES-256 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).algorithm(**kwargs)

    def encryption_config_profiles_edit_payload(self, *args):
        """Change the payload transport URL.

        CLI command: encryptionconfig > profiles > edit > payload

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `payload_url`: Configure the Payload Transport URL. Use either '1', '2' or '3':
        | _1_ | _Use envelope service URL with HTTP_ |
        | _2_ | _Use the envelope service URL with HTTPS_ |
        | _3_ | _Specify a separate URL for payload transport_ |
        - `separate_url`: The URL for payload transport. Optional.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Payload | name=pr_name | payload_url=1 |
        | Encryption Config Profiles Edit Payload | name=pr_name | payload_url=3 | separate_url=http://sep.qa |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).payload(**kwargs)

    def encryption_config_profiles_edit_security(self, *args):
        """Change envelope security.

        CLI command: encryptionconfig > profiles > edit > security

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `level`: The envelope security level.
        Either 'High Security', 'Medium Security', or 'No Password Required'.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Security | name=pr_name | level=medium |
        | Encryption Config Profiles Edit Security | name=pr_name | level=high |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).security(**kwargs)

    def encryption_config_profiles_edit_receipt(self, *args):
        """Change return receipt handling.

        CLI command: encryptionconfig > profiles > edit > receipt

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `enable`: Enable read receipts. Either YES or NO.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Receipt | name=${iron_renamed} | enable=no |
        | Encryption Config Profiles Edit Receipt | name=${iron_renamed} | enable=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).receipt(**kwargs)

    def encryption_config_profiles_edit_forward(self, *args):
        """Change "Secure Forward" setting.

        CLI command: encryptionconfig > profiles > edit > forward

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `enable`: Enable "Secure Forward". Either YES or NO.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Forward | name=${iron_renamed} | enable=no |
        | Encryption Config Profiles Edit Forward | name=${iron_renamed} | enable=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).forward(**kwargs)

    def encryption_config_profiles_edit_replyall(self, *args):
        """Change "Secure Reply All" setting.

        CLI command: encryptionconfig > profiles > edit > replyall

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `enable`: Enable "Secure Reply All". Either YES or NO.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Replyall| name=${iron_renamed} | enable=no |
        | Encryption Config Profiles Edit Replyall| name=${iron_renamed} | enable=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).replyall(**kwargs)

    def encryption_config_profiles_edit_applet(self, *args):
        """Change applet suppression setting.

        CLI command: encryptionconfig > profiles > edit > applet

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `suppress`: Suppress encryption applet functionality. Either YES or NO.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Applet | name=${iron_renamed} | suppress=yes |
        | Encryption Config Profiles Edit Applet | name=${iron_renamed} | suppress=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).applet(**kwargs)

    def encryption_config_profiles_edit_url(self, *args):
        """Change URL associated with logo image.

        CLI command: encryptionconfig > profiles > edit > url

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `logo_url`: An URL to serve as a link for the envelope logo image (may be blank). Optional.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Url | name=${iron_renamed} | logo_url=http://new_logo.img |
        | Encryption Config Profiles Edit Url | name=${iron_renamed} | logo_url=${EMPTY} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).logo_url(**kwargs)

    def encryption_config_profiles_edit_bounce_subject(self, *args):
        """Change failure notification subject.

        CLI command: encryptionconfig > profiles > edit > bounce_subject

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `subject`: The subject to use for failure notifications. Optional.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Bounce Subject | name=${iron_renamed} | subject=FAILED NEW |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).bounce_subject(**kwargs)

    def encryption_config_profiles_edit_timeout(self, *args):
        """Change maximum time message waits in encryption queue.

        CLI command: encryptionconfig > profiles > edit > timeout

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `timeout`: The maximum number of seconds for which a message could remain queued
        waiting to be encrypted.
        Optional.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Timeout | name=${iron_renamed} | timeout=5000 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).timeout(**kwargs)

    def encryption_config_profiles_edit_filename(self, *args):
        """Change the file name of the envelope attached to the encryption notification.

        CLI command: encryptionconfig > profiles > edit > filename

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `filename`: The file name of the envelope attached to the encryption notification. Optional.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Filename | name=${iron_renamed} | filename=new_name.html |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).filename(**kwargs)

    def encryption_config_profiles_edit_assign(self, *args):
        """Change the file name of the envelope attached to the encryption notification.

        CLI command: encryptionconfig > profiles > edit > assign

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `action`: Add or Delete user role. Either 'Add' or 'Delete'.
        - `role`: The role to add/delete.
        Select one or more user role names, separated by a comma.

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Assign | name=${iron_renamed} | action=add | role=some_role |
        | Encryption Config Profiles Edit Assign | name=${iron_renamed} | action=delete | role=some_role |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).assign(**kwargs)

    def encryption_config_profiles_edit_localized_envelope(self, *args):
        """Enable or disable display of envelopes in languages other than English

        CLI command: encryptionconfig > profiles > edit > Localized_envelope

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `display_language`: envelopes to be displayed in a language other than English.
                              Either YES or NO

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Localized_Envelope | name=${iron_renamed} | display_language=Yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).localized_envelope(**kwargs)

    def encryption_config_profiles_edit_default_locale(self, *args):
        """Set/Change default locale

        CLI command: encryptionconfig > profiles > edit > default locale

        *Parameters:*
        - `name`: A name of the encryption profile. String.
        - `language`: Set/Change default locale. String

        *Return:*
        None

        *Examples:*
        | Encryption Config Profiles Edit Default Locale | name=${iron_renamed} | language=en-English |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.encryptionconfig().profiles(). \
            edit(kwargs.pop('name', None)).default_locale(**kwargs)
