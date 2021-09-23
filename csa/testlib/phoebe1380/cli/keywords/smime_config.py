#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/smime_config.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class smimeconfig(CliKeywordBase):
    """
    cli -> smimeconfig

    Configure smimeconfig.
    """
    def get_keyword_names(self):
        return ['smime_config_gatewayVerificationNewImport',
                'smime_config_gatewayVerificationNewPaste',
                'smime_config_gatewayVerificationEditImport',
                'smime_config_gatewayVerificationEditPaste',
                'smime_config_gatewayVerificationEdit',
                'smime_config_gatewayVerificationDelete',
                'smime_config_gatewayVerificationExport',
                'smime_config_gatewayVerificationImport',
                'smime_config_gatewayVerificationPrint',
                'smime_config_gatewaySendingNewEncrypt',
                'smime_config_gatewaySendingNewSign',
                'smime_config_gatewaySendingNewTriple',
                'smime_config_gatewaySendingNewSignandEncrypt',
                'smime_config_gatewaySendingEditEncrypt',
                'smime_config_gatewaySendingEditSign',
                'smime_config_gatewaySendingEditTriple',
                'smime_config_gatewaySendingEditSignandEncrypt',
                'smime_config_gatewaySendingDelete',
                'smime_config_gatewaySendingExport',
                'smime_config_gatewaySendingImport',
                'smime_config_gatewaySendingPrint']

    def smime_config_gatewayVerificationNewImport(self, *args):
        """Create new Gateway Verification Profile with Import option

        smimeconfig -> gateway -> verification -> new

        *Parameters:*
        - `profile_name`: Enter a name for Profile, REQUIRED
        - `import_filename`: Filename of cert to be imported, REQUIRED

        *Examples:*
        | Smime Config GatewayVerificationNewImport | profile_name=test | import_filename=cert.pem |
        | Smime Config GatewayVerificationNewImport | profile_name=test1 | import_filename=cert1.pem |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewayVerificationNewImport(**kwargs)

    def smime_config_gatewayVerificationNewPaste(self, *args):
        """Create new Gateway Verification Profile with Paste option

        smimeconfig -> gateway -> verification -> new

        *Parameters:*
        - `profile_name`: Enter a name for Profile, REQUIRED
        - `paste_certificate`: Enter the certificate details, REQUIRED

        *Examples:*
        | Smime Config GatewayVerificationNewPaste | profile_name=test2 | paste_certificate=${cert} |
        | Smime Config GatewayVerificationNewPaste | profile_name=test3 | paste_certificate=${cert1} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewayVerificationNewPaste(**kwargs)

    def smime_config_gatewayVerificationEditImport(self, *args):
        """Edits Gateway Verification Profile with Import option

        smimeconfig -> gateway -> verification -> edit

        *Parameters:*
        - `profile_number`: No of the profile to edit, REQUIRED
        - `import_filename`: Name of the file to import, REQUIRED

        *Examples:*
        | Smime Config GatewayVerificationEditImport | profile_number=1 | import_filename=cert.pem |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewayVerificationEditImport(**kwargs)

    def smime_config_gatewayVerificationEditPaste(self, *args):
        """Edits Gateway Verification Profile with Paste option

        smimeconfig -> gateway -> verification -> edit

        *Parameters:*
        - `profile_number`: No of the profile to edit, REQUIRED
        - `paste_certificate`: Enter the certificate details, REQUIRED

        *Examples:*
        | Smime Config GatewayVerificationEditPaste | profile_number=1 | paste_certificate=${cert} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewayVerificationEditPaste(**kwargs)

    def smime_config_gatewayVerificationEdit(self, *args):
        """Edits Gateway Verification Profile with No option

        smimeconfig -> gateway -> verification -> edit

        *Parameters:*
        - `profile_number`: No of the profile to edit, REQUIRED

        *Examples:*
        | Smime Config GatewayVerificationEdit | profile_number=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewayVerificationEdit(**kwargs)

    def smime_config_gatewayVerificationDelete(self, *args):
        """Deletes Gateway Verification Profile 'profile_number'

        smimeconfig -> gateway -> verification -> delete

        *Parameters:*
        - `profile_number`: No of the profile to delete, REQUIRED

        *Examples:*
        | Smime Config GatewayVerificationDelete | profile_number=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewayVerificationDelete(**kwargs)

    def smime_config_gatewayVerificationExport(self, *args):
        """Exports Gateway Verification Profile to 'export_filename'

        smimeconfig -> gateway -> verification -> export

        *Parameters:*
        - `export_filename`: Name of the file to which profile is to be exported, REQUIRED

        *Examples:*
        | Smime Config GatewayVerificationExport | export_filename=hello |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewayVerificationExport(**kwargs)

    def smime_config_gatewayVerificationImport(self, *args):
        """Imports Gateway Verification Profile from 'import_filename'

        smimeconfig -> gateway -> verification -> import

        *Parameters:*
        - `import_filename`: Name of the file from which profile is to be imported, REQUIRED

        *Examples:*
        | Smime Config GatewayVerificationImport | import_filename=hello |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewayVerificationImport(**kwargs)

    def smime_config_gatewayVerificationPrint(self):
        """Prints Gateway Verification Profile

        smimeconfig -> gateway -> verification -> print

        *Examples:*
        | Smime Config GatewayVerificationPrint |
        """
        self._cli.smimeconfig().gatewayVerificationPrint()

    def smime_config_gatewaySendingDelete(self, *args):
        """Deletes Gateway Sending Profile 'profile_number'

        smimeconfig -> gateway -> sending -> delete

        *Parameters:*
        - `profile_number`: No of the profile to delete, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingDelete | profile_number=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingDelete(**kwargs)

    def smime_config_gatewaySendingExport(self, *args):
        """Exports Gateway Sending Profile to 'export_filename'

        smimeconfig -> gateway -> sending -> export

        *Parameters:*
        - `export_filename`: Name of the file to which profile is to be exported, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingExport | export_filename=hello1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingExport(**kwargs)

    def smime_config_gatewaySendingImport(self, *args):
        """Imports Gateway Sending Profile from 'import_filename'

        smimeconfig -> gateway -> sending -> import

        *Parameters:*
        - `import_filename`: Name of the file from which profile is to be imported, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingImport | import_filename=hello1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingImport(**kwargs)

    def smime_config_gatewaySendingPrint(self):
        """Prints Gateway Sending Profile

        smimeconfig -> gateway -> sending -> print

        *Examples:*
        | Smime Config GatewaySendingPrint |
        """
        self._cli.smimeconfig().gatewaySendingPrint()

    def smime_config_gatewaySendingNewEncrypt(self, *args):
        """Create new Gateway Sending Profile with Encrypt option

        smimeconfig -> gateway -> sending -> new

        *Parameters:*
        - `profile_name`: Enter a name for Profile, REQUIRED
        - `smime_action`: Enter S/MIME action no, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingNewEncrypt | profile_name=test11 | smime_action=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingNewEncrypt(**kwargs)

    def smime_config_gatewaySendingNewSign(self, *args):
        """Create new Gateway Sending Profile with Sign option

        smimeconfig -> gateway -> sending -> new

        *Parameters:*
        - `profile_name`: Enter a name for Profile, REQUIRED
        - `smime_certificate`: Enter S/MIME certificate no, REQUIRED
        - `smime_signmode`: Enter S/MIME sign mode no, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingNewSign | profile_name=test12 | smime_certificate=1 | smime_signmode=2 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingNewSign(**kwargs)

    def smime_config_gatewaySendingNewTriple(self, *args):
        """Create new Gateway Sending Profile with Triple option

        smimeconfig -> gateway -> sending -> new

        *Parameters:*
        - `profile_name`: Enter a name for Profile, REQUIRED
        - `smime_certificate`: Enter S/MIME certificate no, REQUIRED
        - `smime_signmode`: Enter S/MIME sign mode no, REQUIRED
        - `smime_action`: Enter S/MIME action no, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingNewTriple | profile_name=test12 | smime_certificate=1 | smime_signmode=2 | smime_action=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingNewTriple(**kwargs)

    def smime_config_gatewaySendingNewSignandEncrypt(self, *args):
        """Create new Gateway Sending Profile with SignandEncrypt option

        smimeconfig -> gateway -> sending -> new

        *Parameters:*
        - `profile_name`: Enter a name for Profile, REQUIRED
        - `smime_certificate`: Enter S/MIME certificate no, REQUIRED
        - `smime_signmode`: Enter S/MIME sign mode no, REQUIRED
        - `smime_action`: Enter S/MIME action no, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingNewSignandEncrypt | profile_name=test13 | smime_certificate=1 | smime_signmode=2 | smime_action=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingNewSignandEncrypt(**kwargs)

    def smime_config_gatewaySendingEditEncrypt(self, *args):
        """Edits Gateway Sending Profile with Encrypt option

        smimeconfig -> gateway -> sending -> edit

        *Parameters:*
        - `profile_number`: Enter the no of Profile to Edit, REQUIRED
        - `smime_action`: Enter S/MIME action no, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingEditEncrypt | profile_number=1 | smime_action=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingEditEncrypt(**kwargs)

    def smime_config_gatewaySendingEditSign(self, *args):
        """Edits Gateway Sending Profile with Sign option

        smimeconfig -> gateway -> sending -> edit

        *Parameters:*
        - `profile_number`: Enter the no of Profile to Edit, REQUIRED
        - `smime_certificate`: Enter S/MIME certificate no, REQUIRED
        - `smime_signmode`: Enter S/MIME sign mode no, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingEditSign | profile_number=1 | smime_certificate=1 | smime_signmode=2 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingEditSign(**kwargs)

    def smime_config_gatewaySendingEditTriple(self, *args):
        """Edits Gateway Sending Profile with Triple option

        smimeconfig -> gateway -> sending -> edit

        *Parameters:*
        - `profile_number`: Enter the no of Profile to Edit, REQUIRED
        - `smime_certificate`: Enter S/MIME certificate no, REQUIRED
        - `smime_signmode`: Enter S/MIME sign mode no, REQUIRED
        - `smime_action`: Enter S/MIME action no, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingEditTriple | profile_number=1 | smime_certificate=1 | smime_signmode=2 | smime_action=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingEditTriple(**kwargs)

    def smime_config_gatewaySendingEditSignandEncrypt(self, *args):
        """Edits Gateway Sending Profile with SignandEncrypt option

        smimeconfig -> gateway -> sending -> edit

        *Parameters:*
        - `profile_number`: Enter the no of Profile to Edit, REQUIRED
        - `smime_certificate`: Enter S/MIME certificate no, REQUIRED
        - `smime_signmode`: Enter S/MIME sign mode no, REQUIRED
        - `smime_action`: Enter S/MIME action no, REQUIRED

        *Examples:*
        | Smime Config GatewaySendingEditSignandEncrypt | profile_number=1 | smime_certificate=1 | smime_signmode=2 | smime_action=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smimeconfig().gatewaySendingEditSignandEncrypt(**kwargs)