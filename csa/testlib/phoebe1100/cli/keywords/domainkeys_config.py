#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/domainkeys_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class DomainkeysConfig(CliKeywordBase):
    """
    Manage Domain Keys.
    CLI command: domainkeysconfig
    """

    def get_keyword_names(self):
        return ['domainkeys_config_setup',
                'domainkeys_config_search',
                'domainkeys_config_keys_new',
                'domainkeys_config_keys_edit_rename',
                'domainkeys_config_keys_edit_key',
                'domainkeys_config_keys_print',
                'domainkeys_config_keys_list',
                'domainkeys_config_keys_clear',
                'domainkeys_config_keys_import',
                'domainkeys_config_keys_export',
                'domainkeys_config_keys_delete',
                'domainkeys_config_keys_publickey',
                'domainkeys_config_profiles_signing_new',
                'domainkeys_config_profiles_signing_edit_new',
                'domainkeys_config_profiles_signing_edit_print',
                'domainkeys_config_profiles_signing_edit_clear',
                'domainkeys_config_profiles_signing_edit_delete',
                'domainkeys_config_profiles_signing_edit_key',
                'domainkeys_config_profiles_signing_edit_canonicalization',
                'domainkeys_config_profiles_signing_edit_selector',
                'domainkeys_config_profiles_signing_edit_domain',
                'domainkeys_config_profiles_signing_edit_rename',
                'domainkeys_config_profiles_signing_edit_bodylength',
                'domainkeys_config_profiles_signing_edit_headerselect',
                'domainkeys_config_profiles_signing_edit_customheaders',
                'domainkeys_config_profiles_signing_print',
                'domainkeys_config_profiles_signing_list',
                'domainkeys_config_profiles_signing_clear',
                'domainkeys_config_profiles_signing_import',
                'domainkeys_config_profiles_signing_export',
                'domainkeys_config_profiles_signing_delete',
                'domainkeys_config_profiles_signing_test',
                'domainkeys_config_profiles_signing_dnstxt',
                'domainkeys_config_profiles_verification_new',
                'domainkeys_config_profiles_verification_edit',
                'domainkeys_config_profiles_verification_print',
                'domainkeys_config_profiles_verification_list',
                'domainkeys_config_profiles_verification_clear',
                'domainkeys_config_profiles_verification_import',
                'domainkeys_config_profiles_verification_export',
                'domainkeys_config_profiles_verification_delete', ]

    def domainkeys_config_setup(self, *args):
        """Change global settings.

        CLI command: domainkeysconfig > setup

        *Parameters:*
        - `enable`: Allow signing of system-generated messages. YES or NO.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Setup | enable=yes |
        | Domainkeys Config Setup | enable=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().setup(**kwargs)

    def domainkeys_config_search(self, *args):
        """Search for domain profile or key.

        CLI command: domainkeysconfig > search

        *Parameters:*
        - `profile_or_key`:

        *Return:*
        Raw output.

        *Examples:*
        | ${res}= | Domainkeys Config Search | profile_or_key=${key1} |
        | Log | ${res} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.domainkeysconfig().search(**kwargs)

    def domainkeys_config_profiles_signing_new(self, *args):
        """Create a new domain profile.

        CLI command: domainkeysconfig > profiles > signing > new

        *Parameters:*
        - `name`: A name for the domain profile.
        - `profile_type`: A type of domain profile. One from:
        | 1 | dk |
        | 2 | dkim |
        - `domain_name`: The domain name of the signing domain.
        - `canonicalization_algorithm`:  One from:
        | dk |        |
        | 1 | simple |
        | 2 | nofws |
        | dkim |        |
        | 1 | simple |
        | 2 | relaxed |
        - `key_method`: The key-association method. One from:
        | 1 | Create new key |
        | 2 | Paste in key |
        | 3 | Enter key at later time |
        | 4 | Select existing key |
        - `key_name`: A name for the signing key.
        - `rsa_key`: Raw RSA private key if `key_method` is _2_.
        - `key_size`: The size (in bits) of the signing key if `key_method` is _1_.
        | 1 | 512 |
        | 2 | 768 |
        | 3 | 1024 |
        | 4 | 1536 |
        | 5 | 2048 |
        - `dkim_hdrs_algorithm`: The canonicalization algorithm for headers.
        | 1 | simple |
        | 2 | relaxed |
        - `dkim_body_algorithm`: The canonicalization algorithm for body.
        | 1 | simple |
        | 2 | relaxed |
        - `dkim_sign_hdrs`: How to sign headers.
        | 1 | Sign all existing, non-repeatable headers (except Return-Path header) |
        | 2 | Sign "well-known" headers (Date, Subject, From, To, Cc, Reply-To, Message-ID, Sender, MIME headers) |
        | 3 | Sign "well-known" headers plus a custom list of headers |
        - `dkim_custom_hdrs`: List of comma separated custom headers. String.
        - `dkim_body_length`: Which body length option to use.
        | 1 | Whole body implied. No further message modification is possible |
        | 2 | Whole body auto-determined. Appending content is possible |
        | 3 | Specify a body length |
        - `dkim_custom_body_length`: Enter body length if `dkim_body_length` is _3_.
        - `dkim_tag_tune`: Define which tags should be used in the DKIM Signature. YES or NO.
        - `i_tag`: Include "i" tag into the signature. YES or NO.
        - `dkim_identity_user`: The identity of the user or agent.
        - `q_tag`: Include "q" tag into the signature. YES or NO.
        - `t_tag`: Include "t" tag into the signature. YES or NO.
        - `x_tag`: Include "x" tag into the signature. YES or NO.
        - `z_tag`: Include "z" tag into the signature. YES or NO.
        - `dkim_expire_time`: The expiration time - number of seconds before the signature is expired.
        - `user`: A user for the signing profile.
        - `existing_key`: Key name to select for usage in profile.
        - `selector`: The selector. This value becomes the "s" tag of the DomainKeys Signature.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing New |
        | ... | name=${pr1} |
        | ... | profile_type=dk |
        | ... | domain_name=mail.qa |
        | ... | selector=sel |
        | ... | canonicalization_algorithm=simple |
        | ... | key_method=create |
        | ... | key_name=${pr1}_key1 |
        | ... | key_size=4 |

        | Domainkeys Config Profiles Signing New |
        | ... | name=${pr2} |
        | ... | profile_type=dkim |
        | ... | domain_name=mail.qa |
        | ... | selector=sel |
        | ... | key_method=create |
        | ... | key_name=${pr1}_key2 |
        | ... | key_size=3 |
        | ... | dkim_hdrs_algorithm=relaxed |
        | ... | dkim_body_algorithm=simple |
        | ... | dkim_sign_hdrs=2 |
        | ... | dkim_body_length=3 |
        | ... | dkim_custom_body_length=10000 |
        | ... | dkim_tag_tune=yes |
        | ... | i_tag=yes |
        | ... | dkim_identity_user=@mail.qa |
        | ... | q_tag=yes |
        | ... | t_tag=yes |
        | ... | x_tag=yes |
        | ... | dkim_expire_time=21536000 |
        | ... | z_tag=yes |
        | ... | user=babar@mail.qa |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing().new(**kwargs)

    def domainkeys_config_profiles_signing_edit_new(self, *args):
        """Create a new domain profile user.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > new

        *Parameters:*
        - `name`: The profile name to edit.
        - `user`: The user for signing profile.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit New |
        | ... | name=${pr2} |
        | ... | user=karabas@mail.qa |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).new(**kwargs)

    def domainkeys_config_profiles_signing_edit_print(self, *args):
        """Display list of all profile users.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > print

        *Parameters:*
        - `name`: The profile name.

        *Return:*
        Raw output.

        *Examples:*
        | ${res}= | Domainkeys Config Profiles Signing Edit Print | name=${pr2} |
        | Log | ${res} |
        | Should Contain | ${res} | andriy |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).print_list()

    def domainkeys_config_profiles_signing_edit_clear(self, *args):
        """Clear domain profile's user table.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > clear

        *Parameters:*
        - `name`: The profile name.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Clear | name=${pr2} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).clear()

    def domainkeys_config_profiles_signing_edit_delete(self, *args):
        """Delete a domain profile user.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > delete

        *Parameters:*
        - `name`: The profile name.
        - `user`: The user of signing profile.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Delete | name=${pr2} | user=andriy@mail.qa |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).delete(**kwargs)

    def domainkeys_config_profiles_signing_edit_key(self, *args):
        """Change the signing key of the domain profile.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > key

        *Parameters:*
        - `name`: The profile name to edit.
        - `key_method`: One from:
        | 1 | Create new key |
        | 2 |  Paste in key |
        | 3 | Enter key at later time |
        | 4 | Select existing key |
        - `key_name`: A name for the signing key.
        - `key_size`: The size (in bits) of the signing key if `key_method` is _1_.
        | 1 | 512 |
        | 2 | 768 |
        | 3 | 1024 |
        | 4 | 1536 |
        | 5 | 2048 |
        - `existing_key`: The name or number of a signing key if `key_method` is _4_.
        - `rsa_key`: Raw RSA private key if `key_method` is _2_.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Key |
        | ... | name=${pr2} |
        | ... | key_method=create |
        | ... | key_name=${pr2}_key2 |
        | ... | key_size=4 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).key(**kwargs)

    def domainkeys_config_profiles_signing_edit_canonicalization(self, *args):
        """Change the canonicalization of the domain profile.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > canonicalization

        *Parameters:*
        - `name`: The profile name to edit.
        - `canonicalization_algorithm`: One from:
        | dk |        |
        | 1 | simple |
        | 2 | nofws |
        | dkim |        |
        | 1 | simple |
        | 2 | relaxed |
        - `dkim_hdrs_algorithm`: The canonicalization algorithm for headers.
        | 1 | simple |
        | 2 | relaxed |
        - `dkim_body_algorithm`: The canonicalization algorithm for body.
        | 1 | simple |
        | 2 | relaxed |

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Canonicalization |
        | ... | name=${pr2} |
        | ... | dkim_hdrs_algorithm=simple |
        | ... | dkim_body_algorithm=relaxed |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).canonicalization(**kwargs)

    def domainkeys_config_profiles_signing_edit_selector(self, *args):
        """Change the selector of the domain profile.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > selector

        *Parameters:*
        - `name`: The profile name to edit.
        - `selector`: A new selector for the domain profile.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Selector |
        | ... | name=${pr2} |
        | ... | selector=mysel |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).selector(**kwargs)

    def domainkeys_config_profiles_signing_edit_domain(self, *args):
        """Change the domain of the domain profile.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > domain

        *Parameters:*
        - `name`: The profile name to edit.
        - `domain`: A new domain for the domain profile.
        - `dkim_identity_user`: The identity of the user or agent.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Domain |
        | ... | name=${pr2} |
        | ... | domain=mail.com |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).domain(**kwargs)

    def domainkeys_config_profiles_signing_edit_rename(self, *args):
        """Rename the domain profile.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > rename

        *Parameters:*
        - `name`: The profile name to edit.
        - `new_name`: A new name for thedomain profile.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Rename |
        | ... | name=${pr2} |
        | ... | new_name=${pr2_renamed} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).rename(**kwargs)

    def domainkeys_config_profiles_signing_edit_bodylength(self, *args):
        """Change the body length of the domain profile.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > bodylength

        *Parameters:*
        - `name`: The profile name to edit.
        - `body_length_opt`: The body length option to use. One from:
        | 1 | Whole body implied. No further message modification is possible |
        | 2 | Whole body auto-determined. Appending content is possible |
        | 3 | Specify a body length |
        - `custom_body_length`: The body length if `body_length_opt` is _3_.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Bodylength |
        | ... | name=${pr2} |
        | ... | body_length_opt=3 |
        | ... | custom_body_length=9999 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).bodylength(**kwargs)

    def domainkeys_config_profiles_signing_edit_headerselect(self, *args):
        """Change the headers selection method of the domain profile.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > headerselect

        *Parameters:*
        - `name`: The profile name to edit.
        - `how_to_sign`: How to sign headers. One from:
        | 1 | Sign all existing, non-repeatable headers (except Return-Path header) |
        | 2 | Sign "well-known" headers (Date, Subject, From, To, Cc, Reply-To, Message-ID, Sender, MIME headers) |
        | 3 | Sign "well-known" headers plus a custom list of headers |
        - `change_headers`: Change custom headers. YES or NO.
        - `custom_headers`: Custom headers to sign. Sting - comma separated list of custom headers.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Headerselect |
        | ... | name=${pr2} |
        | ... | how_to_sign=3 |
        | ... | change_headers=yes |
        | ... | custom_headers=yo, ya, yu |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).headerselect(**kwargs)

    def domainkeys_config_profiles_signing_edit_customheaders(self, *args):
        """Change the custom headers of the domain profile.

        CLI command: domainkeysconfig > profiles > signing > edit > SOME_PROFILE > customheaders

        *Parameters:*
        - `name`: The profile name to edit.
        - `custom_headers`: A comma separated list of custom headers. String.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Edit Customheaders |
        | ... | name=${pr2} |
        | ... | custom_headers=changedyo, changedya, changedyu |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            edit(kwargs.pop('name')).customheaders(**kwargs)

    def domainkeys_config_profiles_signing_print(self):
        """Display domain profiles.

        CLI command: domainkeysconfig > profiles > signing > print

        *Parameters:*
        None

        *Return:*
        Raw output

        *Examples:*
        | ${prs}= | Domainkeys Config Profiles Signing Print |
        | Log | ${prs} |
        """
        return self._cli.domainkeysconfig().profiles(). \
            signing().print_profiles()

    def domainkeys_config_profiles_signing_list(self):
        """List domain profiles.

        CLI command: domainkeysconfig > profiles > signing > list

        *Parameters:*
        None

        *Return:*
        Raw output

        *Examples:*
        | ${prs}= | Domainkeys Config Profiles Signing List |
        | Log | ${prs} |
        """
        return self._cli.domainkeysconfig().profiles(). \
            signing().list_profiles()

    def domainkeys_config_profiles_signing_clear(self):
        """Clear all domain profiles.

        CLI command: domainkeysconfig > profiles > signing > clear

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Clear |
        """
        self._cli.domainkeysconfig().profiles().signing().clear()

    def domainkeys_config_profiles_signing_import(self, *args):
        """Import domain profiles from a file.

        CLI command: domainkeysconfig > profiles > signing > import

        *Parameters:*
        - `filename`: The name of the file on machine to import profiles from.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Import | filename=${signing_profiles_exported} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            import_profiles(**kwargs)

    def domainkeys_config_profiles_signing_export(self, *args):
        """Export domain profiles to a file.

        CLI command: domainkeysconfig > profiles > signing > export

        *Parameters:*
        - `filename`: A name for the exported file.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Export | filename=${signing_profiles_exported} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing(). \
            export_profiles(**kwargs)

    def domainkeys_config_profiles_signing_delete(self, *args):
        """Delete a domain profile.

        CLI command: domainkeysconfig > profiles > signing > delete

        *Parameters:*
        - `name`: The name or number of a domain profile to delete.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Signing Delete | name=${pr1} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().signing().delete(**kwargs)

    def domainkeys_config_profiles_signing_test(self, *args):
        """Test if a domain profile is ready to sign.

        CLI command: domainkeysconfig > profiles > signing > test

        *Parameters:*
        - `name`: The name or number of a domain profile.

        *Return:*
        Raw output.

        *Examples:*
        | ${test}= | Domainkeys Config Profiles Signing Test | name=${pr1} |
        | Log | ${test} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.domainkeysconfig().profiles().signing().test(**kwargs)

    def domainkeys_config_profiles_signing_dnstxt(self, *args):
        """Generate a matching DNS TXT record.

        CLI command: domainkeysconfig > profiles > signing > dnstxt

        *Parameters:*
        - `name`: The name or number of a domain profile to delete.
        - `g_tag`: Constrain the local part of the signing identities. YES or NO.
        - `local_part`: The pattern to match local part of signer identity.
        - `n_tag`: Include notes that may be of interest to a human. YES or NO.
        - `note`: Enter your note.
        - `t_tag`: Indicate the "testing mode". YES or NO.

        *Return:*
        Formatted DomainKey DNS TXT record. String.

        *Examples:*
        | ${test}= | Domainkeys Config Profiles Signing Dnstxt |
        | ... | name=${pr1} |
        | ... | g_tag=yes |
        | ... | local_part=local |
        | ... | n_tag=yes |
        | ... | note=my note |
        | ... | t_tag=yes |
        | Log | ${test} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.domainkeysconfig().profiles(). \
            signing().dnstxt(**kwargs)

    def domainkeys_config_profiles_verification_new(self, *args):
        """Create a new DKIM verification profile.

        CLI command: domainkeysconfig > profiles > verification > new

        *Parameters:*
        - `name`: A name of DKIM verification profile.
        - `small_key`: The smallest key to be accepted. One from:
        | 1 | 512 |
        | 2 | 768 |
        | 3 | 1024 |
        | 4 | 1536 |
        | 5 | 2048 |
        - `largest_key`: The largest key to be accepted. One from:
        | 1 | 512 |
        | 2 | 768 |
        | 3 | 1024 |
        | 4 | 1536 |
        | 5 | 2048 |
        - `max_signatures`: A maximum number of signatures in the message to verify.
        - `time_out`: A number of seconds before the key query is timed out.
        - `tolerate`: A number of seconds to tolerate wall clock asynchronization between
        sender and verifier.
        - `body_length`: Use a body length parameter. YES or NO.
        - `SMTP_action_temp`: SMTP action to be taken in case of temporary failure.
        One from:
        | 1 | Accept |
        | 2 | Reject |
        - `SMTP_response_code_temp`: The SMTP response code.
        - `SMTP_response_text_temp`: The SMTP response text.
        - `SMTP_action_perm`: SMTP action to be taken in case of permanent failure.
        One from:
        | 1 | Accept |
        | 2 | Reject |
        - `SMTP_response_code_perm`: The SMTP response code.
        - `SMTP_response_text_perm`: The SMTP response text.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Verification New |
        | ... | name=${ver_pr1} |
        | ... | small_key=1 |
        | ... | largest_key=5 |
        | ... | max_signatures=10 |
        | ... | time_out=360 |
        | ... | tolerate=250 |
        | ... | body_length=yes |
        | ... | SMTP_action_temp=Accept |
        | ... | SMTP_action_perm=Reject |

        | Domainkeys Config Profiles Verification New |
        | ... | name=${ver_pr2} |
        | ... | small_key=1 |
        | ... | largest_key=5 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().verification().new(**kwargs)

    def domainkeys_config_profiles_verification_edit(self, *args):
        """Modify a DKIM verification profile.

        CLI command: domainkeysconfig > profiles > verification > edit

        *Parameters:*
        - `name`: A name of DKIM verification profile to edit.
        - `new_name`: New name of DKIM verification profile.
        - `small_key`: The smallest key to be accepted. One from:
        | 1 | 512 |
        | 2 | 768 |
        | 3 | 1024 |
        | 4 | 1536 |
        | 5 | 2048 |
        - `largest_key`: The largest key to be accepted. One from:
        | 1 | 512 |
        | 2 | 768 |
        | 3 | 1024 |
        | 4 | 1536 |
        | 5 | 2048 |
        - `max_signatures`: A maximum number of signatures in the message to verify.
        - `time_out`: A number of seconds before the key query is timed out.
        - `tolerate`: A number of seconds to tolerate wall clock asynchronization between
        sender and verifier.
        - `body_length`: Use a body length parameter. YES or NO.
        - `SMTP_action_temp`: SMTP action to be taken in case of temporary failure.
        One from:
        | 1 | Accept |
        | 2 | Reject |
        - `SMTP_response_code_temp`: The SMTP response code.
        - `SMTP_response_text_temp`: The SMTP response text.
        - `SMTP_action_perm`: SMTP action to be taken in case of permanent failure.
        One from:
        | 1 | Accept |
        | 2 | Reject |
        - `SMTP_response_code_perm`: The SMTP response code.
        - `SMTP_response_text_perm`: The SMTP response text.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Verification Edit |
        | ... | name=${ver_pr2} |
        | ... | new_name=${ver_pr2_renamed} |
        | ... | small_key=2 |
        | ... | largest_key=4 |
        | ... | max_signatures=10 |
        | ... | time_out=360 |
        | ... | tolerate=250 |
        | ... | body_length=yes |
        | ... | SMTP_action_temp=Accept |
        | ... | SMTP_action_perm=Reject |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().verification().edit(**kwargs)

    def domainkeys_config_profiles_verification_print(self, *args):
        """Display DKIM verification profiles.

        CLI command: domainkeysconfig > profiles > verification > print

        *Parameters:*
        - `name`:  A name of DKIM verification profile to print.

        *Return:*
        Raw output.

        *Examples:*
        | ${res}= | Domainkeys Config Profiles Verification Print | name=${ver_pr1} |
        | Log | ${res} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.domainkeysconfig().profiles(). \
            verification().print_profiles(**kwargs)

    def domainkeys_config_profiles_verification_list(self):
        """List DKIM verification profiles.

        CLI command: domainkeysconfig > profiles > verification > list

        *Parameters:*
        None

        *Return:*
        Raw output.

        *Examples:*
        | ${res}= | Domainkeys Config Profiles Verification List |
        | Log | ${res} |
        | Should Contain | ${res} | ${ver_pr1} |
        """
        return self._cli.domainkeysconfig().profiles(). \
            verification().list_profiles()

    def domainkeys_config_profiles_verification_clear(self, *args):
        """Clear all DKIM verification profiles.

        CLI command: domainkeysconfig > profiles > verification > clear

        *Parameters:*
        - `confirm`: Confirm. YES or NO.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Verification Clear | confirm=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles().verification().clear(**kwargs)

    def domainkeys_config_profiles_verification_import(self, *args):
        """Import DKIM verification profiles from a file.

        CLI command: domainkeysconfig > profiles > verification > import

        *Parameters:*
        - `filename`: The name of the file on machine to import from.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Verification Import | filename=${verification_profiles_exported} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles(). \
            verification().import_profiles(**kwargs)

    def domainkeys_config_profiles_verification_export(self, *args):
        """Export DKIM verification profiles to a file.

        CLI command: domainkeysconfig > profiles > verification > export

        *Parameters:*
        - `filename`: A name for the exported file.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Verification Export | filename=${verification_profiles_exported} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles(). \
            verification().export_profiles(**kwargs)

    def domainkeys_config_profiles_verification_delete(self, *args):
        """Delete a DKIM verification profile.

        CLI command: domainkeysconfig > profiles > verification > delete

        *Parameters:*
        - `name`: A name of DKIM verification profile to delete.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Profiles Verification Delete | name=${ver_pr1} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().profiles(). \
            verification().delete(**kwargs)

    def domainkeys_config_keys_new(self, *args):
        """Create a new signing key.

        CLI command: domainkeysconfig > keys > new

        *Parameters:*
        - `name`: A name for the signing key. Required.
        - `key_method`: Either
        | 1 | Generate a private key |
        | 2 | Enter an existing key |
        - `rsa_key`: RSA private key if `input_type` is _2_.
        - `size`: The size (in bits) of the signing key if `input_type` is _1_.
        | 1 | 512 |
        | 2 | 768 |
        | 3 | 1024 |
        | 4 | 1536 |
        | 5 | 2048 |

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Keys New |
        | ... | name=${key1} |
        | ... | key_method=1 |
        | ... | size=1 |

        | Domainkeys Config Keys New |
        | ... | name=key2 |
        | ... | key_method=generate |
        | ... | size=3 |

        | ${paste_me}= | Catenate |
        | ... | SEPARATOR=\n |
        | ... | -----BEGIN RSA PRIVATE KEY----- |
        | ... | MIIBPAIBAAJBAMRh8KF65ngudyvr7OhrdJPRmYG26g9YGQ/4QXTcjUf8lkJELHe8 |
        | ... | njPoQYyTpWiNOigZruF6awKLVoaZHODZ1H8CAwEAAQJBAJnMkmYFGIY67b4KMSn9 |
        | ... | Lfmuh2hdVoXZ2xb0uF7LdCJRP70snyPEqH4Lc+3dgSblTxwF1ADlEvgZw03tJMeS |
        | ... | mrECIQD8UBUJxcm4/WUdoxfOC5i8Is41vawwuLf37H4erMICgwIhAMdAnoowP760 |
        | ... | Reavph9DoAUmxxlNVoXgYamPHse2yNVVAiEA051+56FhnKu6AO9m6cNEKJawiNY5 |
        | ... | 8usaMO/Cn4uZdG0CIE4uccbBJdH7RE4+74zm6Pv8ejTYXrHLGCcC7E3qz6S9AiEA |
        | ... | mrUMQQb/DkK1MlNBthhoETSsXtwPYcsYTccsZLyW4Q4= |
        | ... | -----END RSA PRIVATE KEY----- |
        | Domainkeys Config Keys New |
        | ... | name=${key2} |
        | ... | key_method=enter |
        | ... | rsa_key=${paste_me} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().keys().new(**kwargs)

    def domainkeys_config_keys_edit_key(self, *args):
        """Modify a signing key. Change the key of current signing key.

        CLI command: domainkeysconfig > keys > edit > SOME_KEY > key

        *Parameters:*
        - `name`: The name or number of a signing key to edit.
        - `key_method`: Either
        | 1 | Generate a private key |
        | 2 | Enter an existing key |
        - `rsa_key`: RSA private key if `input_type` is _2_.
        - `size`: The size (in bits) of the signing key if `input_type` is _1_.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Keys Edit Key |
        | ... | name=${key1_renamed} |
        | ... | key_method=generate |
        | ... | size=3 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().keys(). \
            edit(kwargs.pop('name')).key(**kwargs)

    def domainkeys_config_keys_edit_rename(self, *args):
        """Modify a signing key. Rename.

        CLI command: domainkeysconfig > keys > edit > SOME_KEY > rename

        *Parameters:*
        - `name`: The name or number of a signing key to edit.
        - `new_name`: New name of signing key.

        *Return:*
        None.

        *Examples:*
        | Domainkeys Config Keys Edit Rename |
        | ... | name=${key1} |
        | ... | new_name=${key1_renamed} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().keys(). \
            edit(kwargs.pop('name')).rename(**kwargs)

    def domainkeys_config_keys_print(self):
        """Display signing keys.

        CLI command: domainkeysconfig > keys > print

        *Parameters:*
        None

        *Return:*
        Raw output.

        *Examples:*
        | ${keys}= | Domainkeys Config Keys Print |
        | Log | ${keys} |
        """
        return self._cli.domainkeysconfig().keys().print_keys()

    def domainkeys_config_keys_list(self):
        """Display signing keys.

        CLI command: domainkeysconfig > keys > list

        *Parameters:*
        None

        *Return:*
        Raw output.

        *Examples:*
        | ${keys}= | Domainkeys Config Keys List |
        | Log | ${keys} |
        """
        return self._cli.domainkeysconfig().keys().list_keys()

    def domainkeys_config_keys_clear(self):
        """Clear all signing keys.

        CLI command: domainkeysconfig > keys > clear

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Keys Clear |
        """
        self._cli.domainkeysconfig().keys().clear()

    def domainkeys_config_keys_import(self, *args):
        """Import signing keys from a file.

        CLI command: domainkeysconfig > keys > import

        *Parameters:*
        - `filename`: The name of the file on machine to import keys from.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Keys Import | filename=${keys_exported} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().keys().import_keys(**kwargs)

    def domainkeys_config_keys_export(self, *args):
        """Export signing keys to a file.

        CLI command: domainkeysconfig > keys > export

        *Parameters:*
        - `filename`: A name for the exported file.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Keys Export | filename=${keys_exported} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().keys().export_keys(**kwargs)

    def domainkeys_config_keys_delete(self, *args):
        """Delete a signing key.

        CLI command: domainkeysconfig > keys > delete

        *Parameters:*
        - `name`: The name or number of a signing key to delete.
        - `confirm`: Confirm delete operation.

        *Return:*
        None

        *Examples:*
        | Domainkeys Config Keys Delete | name=${key1} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainkeysconfig().keys().delete(**kwargs)

    def domainkeys_config_keys_publickey(self, *args):
        """Create a publickey from a signing key.

        CLI command: domainkeysconfig > keys > publickey

        *Parameters:*
        - `name`: The name or number of a signing key.

        *Return:*
        Public key as raw output.

        *Examples:*
        | {pk}= | Domainkeys Config Keys Publickey | name=${key1_renamed} |
        | Log | ${pk} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.domainkeysconfig().keys().publickey(**kwargs)
