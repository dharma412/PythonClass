# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm115/cm115_custom_url_categories.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm115/cm115_custom_url_categories.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from coeus1100.gui.manager.custom_url_categories import CustomUrlCategories

class Cm110CustomUrlCategories(CustomUrlCategories):

    """
    Keywords library for WebUI page  Web -> Configuration Master 11.5 -> Custom URL Categories
    """

    def _open_page(self):
        self._navigate_to('Web', 'Configuration Master 11.5', 'Custom and External URL Categories')

    def get_keyword_names(self):
        return [
             'cm115_custom_url_categories_add',
             'cm115_custom_url_categories_delete',
             'cm115_custom_url_categories_edit',
             'cm115_custom_url_categories_get_list',
             ]

    def cm115_custom_url_categories_get_list(self):
        """
        Returns: list of custom url categories

        Examples:

        | ${policies}= | CM115 Custom URL Category Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | 'category1' in ${policies} |
        """
        self._open_page()
        return self._get_policies().keys()

    def cm115_custom_url_categories_add(self,
             name,
             sites=None,
             order=1,
             regexes=None):
        """Adds the custom URL category

        *Parameters*
        - `name`: name of the custom URL category. Mandatory.
        - `order`: processing order. Optional, '1' by default.
        - `sites`: partial urls or IP addresses the category should match.
             A string with comma separated values. Define either a URL
             or regular expression. At least one of these
             fields  must contain a value.
        - `regexes`: regular expressions for the urls the category
             should m atch. A string with comma separated values. Define either a URL
             or regular expression. At least one of these
             fields must contain a value.

        *Example*
        | CM115 Custom Url Categories Add | nameOfCategory | site1.com, site2.com | order=1 |
        | CM115 Custom Url Categories Add | nameOfCategory | order=1 | regexes=regex1, regex2 |
        """
        self.custom_url_category_add(
             name,
             sites=sites,
             order=order,
             regexes=regexes,
             )

    def cm115_custom_url_categories_edit(self,
             name,
             sites=None,
             order=None,
             regexes=None):
        """Updates the custom URL category

        *Parameters*
        - `name`: name of the custom URL category. Mandatory.
        - `order`: processing order. Optional, '1' by default.
        - `sites`: partial urls or IP addresses the category should match.
             A string with comma separated values. Define either a URL
             or regular expression. At least one of these
             fields must contain a value.
        - `regexes`: regular expressions for the urls the category
             should match. A string with comma separated values. Define either a URL
             or regular expression. At least one of these
             fields must contain a value.

        *Exceptions*
        - GuiControlNotFoundError:xxx Custom URL Categories

        *Examples*
        | CM115 Custom Url Categories Edit | nameOfCategory | site1.com, site2.com | order=1 |
        | CM115 Custom Url Categories Edit | nameOfCategory | order=1 | regexes=regex1 |
        """
        self.custom_url_category_edit(
             name,
             sites=sites,
             order=order,
             regexes=regexes,
             )

    def cm115_custom_url_categories_delete(self, name):
        """Deletes the custom URL category

        *Parameters*
        - `name`: The name of the edited policy. String. Mandatory.

        *Exceptions*
        - GuiControlNotFoundError:Custom URL category "xxx" missing

        *Examples*
        | CM115 Custom Url Categories Delete | nameOfCategory |
        | CM115 Custom Url Categories Delete | Category1 |
        """
        self.custom_url_category_delete(name)
