#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/create_computer_object.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class CreateComputerObject(CliKeywordBase):
    """Create the computer object at the specified location."""

    def get_keyword_names(self):
        return [
            'create_computer_object',
        ]

    def create_computer_object(self,
                               location=DEFAULT,
                               user=None,
                               password=None):

        """Create computer object

        createcomputerobject

        Parameters:
        - `location`: location where the Computer Object must be created.
        - `user`: username with the privileges to create the Computer Object
                in the specified location. The default location is 'Computers'
                folder.

        - `password`:  password for the specified user.

        Examples:
        | Create Computer Object | location=Computers | user=foo | password=bar |
        | Create Computer Object | user=foo | password=bar |
        """

        if all([user, password]):
            output = self._cli.createcomputerobject(location, user, password)
            self._info(output)

        else:
            raise ValueError('You must specify username and password.')

