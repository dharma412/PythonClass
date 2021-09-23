#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/textconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class textconfig(CliKeywordBase):
    """Keywords for textconfig cli command. """

    def get_keyword_names(self):
        return ['textconfig_new',
                'textconfig_import',
                'textconfig_export',
                'textconfig_print',
                'textconfig_edit',
                'textconfig_delete',
                'textconfig_list',
                ]

    def textconfig_new(self, *args):
        """  This keyword is used to Create a new text resource.

        The various parameters are:
        - `resource_type` : The kind of resources we would like to create.
           The various options are:
           | Value | Options |
           | 1 | Anti-Virus Container Template |
           | 2 | Anti-Virus Notification Template |
           | 3 | DLP Notification Template |
           | 4 | Bounce and Encryption Failure Notification Template |
           | 5 | Message Disclaimer |
           | 6 | Encryption Notification Template (HTML) |
           | 7 | Encryption Notification Template (text) |
           | 8 | Notification Template |
       - `resource_name` : name for the container template
          Can be any text.
       - `encoding_type` : encoding for the template.
          The various paramters are:
         | 1 | US-ASCII |
         | 2 | Unicode (UTF-8) |
         | 3 | Unicode (UTF-16) |
         | 4 | Western European/Latin-1 (ISO 8859-1) |
         | 5 | Western European/Latin-1 (Windows CP1252) |
         | 6 | Traditional Chinese (Big 5) |
         | 7 | Simplified Chinese (GB 2312) |
         | 8 | Simplified Chinese (HZ GB 2312) |
         | 9 | Korean (ISO 2022-KR) |
         | 10 | Korean (KS-C-5601/EUC-KR) |
         | 11 | Japanese (Shift-JIS (X0123)) |
         | 12 | Japanese (ISO-2022-JP) |
         | 13 | Japanese (EUC) |
       - `notification_template` : Enter the notification template.
          Can be any text.
       - `auto_diff` : This option is used to specify if
         | 1 | Use the auto-generated plain text version |
         | 2 | Enter a different plain text version |
         The values can be the numbers.
         This option is available only when the resource
          tye is 5.
       - `plain_template` : This option is used to enter  the plain text
          version of the message disclaimer. This option is active only when
          2 is chosen in the auto_diff.

       Examples:

       |  Textconfig New | resource_type=1 | resource_name=test_virus |
       | ... |  encoding_type=3 | notification_template=testing |

       | Textconfig New | resource_type=5 | resource_name=test123 |
       | ... | encoding_type=5 | notification_template=cool_test |
       | ... | auto_diff=2 | plain_template=done |

       """
        kwargs = self._convert_to_dict(args)
        self._cli.textconfig().new(**kwargs)

    def textconfig_import(self, *args):
        """  This keyword is used to Import a text resource from a file.

        The various parameters are:
        - `resource_type` : The kind of resources we would like to create.
           The various options are:
           | Value | Options |
           | 1 | Anti-Virus Container Template |
           | 2 | Anti-Virus Notification Template |
           | 3 | DLP Notification Template |
           | 4 | Bounce and Encryption Failure Notification Template |
           | 5 | Message Disclaimer |
           | 6 | Encryption Notification Template (HTML) |
           | 7 | Encryption Notification Template (text) |
           | 8 | Notification Template |
       - `resource_name` : name for the container template
          Can be any text.
       - `file_name` : Name of the file to import.
          The file should be present in /data/pub/configuration directory.
       - `encoding_type` :  encoding for the template.
          The various paramters are:
         | 1 | US-ASCII |
         | 2 | Unicode (UTF-8) |
         | 3 | Unicode (UTF-16) |
         | 4 | Western European/Latin-1 (ISO 8859-1) |
         | 5 | Western European/Latin-1 (Windows CP1252) |
         | 6 | Traditional Chinese (Big 5) |
         | 7 | Simplified Chinese (GB 2312) |
         | 8 | Simplified Chinese (HZ GB 2312) |
         | 9 | Korean (ISO 2022-KR) |
         | 10 | Korean (KS-C-5601/EUC-KR) |
         | 11 | Japanese (Shift-JIS (X0123)) |
         | 12 | Japanese (ISO-2022-JP) |
         | 13 | Japanese (EUC) |

        Example:
         | Textconfig Import | resource_type=1 | resource_name=test1 |
         | ... | file_name=test.txt | encoding_type=5 |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.textconfig().import_method(**kwargs)

    def textconfig_export(self, *args):
        """  This keyword is used to Export text resource to a file.

        The various parameters are:
        - `resource_name` : the name or number of the resource to export
        - `file_name` : The name of the file to export.
        - `encoding_type` :  encoding for the template.
          The various paramters are:
         | 1 | US-ASCII |
         | 2 | Unicode (UTF-8) |
         | 3 | Unicode (UTF-16) |
         | 4 | Western European/Latin-1 (ISO 8859-1) |
         | 5 | Western European/Latin-1 (Windows CP1252) |
         | 6 | Traditional Chinese (Big 5) |
         | 7 | Simplified Chinese (GB 2312) |
         | 8 | Simplified Chinese (HZ GB 2312) |
         | 9 | Korean (ISO 2022-KR) |
         | 10 | Korean (KS-C-5601/EUC-KR) |
         | 11 | Japanese (Shift-JIS (X0123)) |
         | 12 | Japanese (ISO-2022-JP) |
         | 13 | Japanese (EUC) |

         Examples:
         | Textconfig Export | resource_name=test1 | file_name=testing |
         | ... | encoding_type=5 |

         """

        kwargs = self._convert_to_dict(args)
        self._cli.textconfig().export(**kwargs)

    def textconfig_print(self, *args):
        """  This keyword is used to Display the content of a resource

        The parameter is :
        - `resource_name` : name or number of the resource to display.

        Examples:
        | ${log}= |  Textconfig Print | resource_name=1 |

        """
        kwargs = self._convert_to_dict(args)
        return str(self._cli.textconfig().print_method(**kwargs))

    def textconfig_edit(self, *args):
        """  This keyword is used to Modify a resource.

        The parameters are:
        - `resource_name` : the name or number of the resource to edit.
        - `encoding_type` :  encoding for the template.
          The various paramters are:
         | 1 | US-ASCII |
         | 2 | Unicode (UTF-8) |
         | 3 | Unicode (UTF-16) |
         | 4 | Western European/Latin-1 (ISO 8859-1) |
         | 5 | Western European/Latin-1 (Windows CP1252) |
         | 6 | Traditional Chinese (Big 5) |
         | 7 | Simplified Chinese (GB 2312) |
         | 8 | Simplified Chinese (HZ GB 2312) |
         | 9 | Korean (ISO 2022-KR) |
         | 10 | Korean (KS-C-5601/EUC-KR) |
         | 11 | Japanese (Shift-JIS (X0123)) |
         | 12 | Japanese (ISO-2022-JP) |
         | 13 | Japanese (EUC) |
        - `new_text` : Enter the notification template.
          Can be any text.
       - `auto_diff` : This option is used to specify if
         | 1 | Use the auto-generated plain text version |
         | 2 | Enter a different plain text version |
         The values can be the numbers.
         This option is available only when the resource
          tye is 5.
       - `plain_template` : This option is used to enter  the plain text
          version of the message disclaimer. This option is active only when
          2 is chosen in the auto_diff.

        """
        kwargs = self._convert_to_dict(args)
        self._cli.textconfig().edit(**kwargs)

    def textconfig_list(self, *args):
        """  This keyword is used to List configured resources.

        *Return*
        - The name of the Text Resource
        - The type of the Resource.

        Example:

        | ${log}= |  Textconfig List |
        """
        kwargs = self._convert_to_dict(args)
        return str(self._cli.textconfig().list(**kwargs))

    def textconfig_delete(self, *args):
        """  This keyword is used to Remove a resource from the system.

        Parameter:
        The parameter for this function is
        - `resource_name` : the name or number of the resource to delete.

        Examples:

        | Textconfig Delete | resource_name=1 |

        | TextConfig Delete | resource_name=test123 |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.textconfig().delete(**kwargs)
