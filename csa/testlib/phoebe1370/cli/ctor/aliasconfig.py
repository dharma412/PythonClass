#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/aliasconfig.py#1 $

"""
IAF 2 CLI command: aliasconfig
"""


import clictorbase as ccb
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO
REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
DEBUG = True


class aliasconfig(ccb.IafCliConfiguratorBase):




    class NewCommandError(ccb.IafCliError): pass
    class AliasAlreadyDefinedError(ccb.IafCliError): pass
    class RecursiveAliasError(ccb.IafCliError): pass
    class AliasFormatError(ccb.IafCliError): pass
    class AliasAddError(ccb.IafCliError): pass
    class AliasDestinationError(ccb.IafCliError): pass
    class AliasReferredError(ccb.IafCliError): pass
    class AliasDefinedError(ccb.IafCliError): pass
    class AliasUnresolvedError(ccb.IafCliError): pass
    class AliasDomainExistAliasesError(ccb.IafCliError): pass
    class AliasGlobalDomainExistError(ccb.IafCliError): pass
    class AliasExportError(ccb.IafCliError): pass
    class AliasMachineError(ccb.IafCliError): pass
    class AliasOperationError(ccb.IafCliError): pass
    class AliasSaveError(ccb.IafCliError): pass
    class AliasWriteFileError(ccb.IafCliError): pass
    class AliasUnknownUserError(ccb.IafCliError): pass
    class AliasImportError(ccb.IafCliError): pass
    class AliasFileError(ccb.IafCliError): pass
    class AliasEmptyFileError(ccb.IafCliError): pass
    class AliasExistFileError(ccb.IafCliError): pass
    class AliasPermissionFileError(ccb.IafCliError): pass
    class AliasReadFileError(ccb.IafCliError): pass
    class AliasExistError(ccb.IafCliError): pass
    class AliasDomainAliasesExistError(ccb.IafCliError): pass
    class AliasDomainAllAliasesExistError(ccb.IafCliError): pass
    class AliasDomainExistError(ccb.IafCliError): pass
    class AliasDeleteError(ccb.IafCliError): pass
    class AliasInvalidDomain(ccb.IafCliError): pass

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('"NEW" command aborted', EXACT): self.NewCommandError,
            ('already defined in context',
                                  EXACT): self.AliasAlreadyDefinedError,
            ('recursive alias detected', EXACT): self.RecursiveAliasError,
            ('Format error', EXACT) : self.AliasFormatError,
            ('adding this alias would cause', EXACT): self.AliasAddError,
            ('Unresolved destination alias', EXACT): self.AliasDestinationError,
            ('Undefined alias \S+ referred', REGEX): self.AliasReferredError,
            ('All aliases must be defined before finishing',
                                  EXACT): self.AliasDefinedError,
            ('Unresolved aliases exist', EXACT): self.AliasUnresolvedError,
            ('The domain context \S+ has no aliases',
                                  REGEX): self.AliasDomainExistAliasesError,
            ('no aliases in the global domain context',
                                  EXACT): self.AliasGlobalDomainExistError,
            ('Export failed', EXACT): self.AliasExportError,
            ('Could not reach target machine', EXACT): self.AliasMachineError,
            ('Unable to perform operation due to an I/O error',
                                  EXACT): self.AliasOperationError,
            ('cannot be saved', EXACT) : self.AliasSaveError,
            ('Error writing file', EXACT): self.AliasWriteFileError,
            ('account appears to have been removed',
                                  EXACT): self.AliasUnknownUserError,
            ('Failed to import file', EXACT): self.AliasImportError,
            ('No aliases found in file', EXACT): self.AliasFileError,
            ('Error: empty file', EXACT): self.AliasEmptyFileError,
            ('the file \S+ does not exist.', REGEX): self.AliasExistFileError,
            ('not have permissions to read',
                                  EXACT): self.AliasPermissionFileError,
            ('Error reading file', EXACT): self.AliasReadFileError,
            ('The alias \S+ does not exist', REGEX): self.AliasExistError,
            ('The domain \S+ has no aliases',
                                  REGEX): self.AliasDomainAliasesExistError,
            ('no aliases that apply to all domains',
                                  EXACT): self.AliasDomainAllAliasesExistError,
            ('The domain \S+ does not exist',
                                   REGEX): self.AliasDomainExistError,
            ('No aliases were deleted', EXACT): self.AliasDeleteError,
            ('Invalid domain name',  EXACT): self.AliasInvalidDomain
            })

    def __call__(self):
        self._writeln('aliasconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['aliases_apply']  = \
                      ['How do you want your aliases to apply', DEFAULT, True]
        param_map['aliases']        = \
                      ['Enter the alias(es) to match on.', REQUIRED]
        param_map['address']        = ['Enter address(es) for', REQUIRED]
        param_map['another_alias']  = \
                      ['Do you want to add another alias', DEFAULT]
        param_map['domain_context'] = \
                      ['Enter new domain context.', REQUIRED]
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['domain_context'] = \
                         ['Which domain context do you want?', DEFAULT, True]
        param_map['alias']          = \
                         ['Enter the alias you want to edit.', DEFAULT, True]
        param_map['address']        = ['Enter new address(es) for', REQUIRED]
        param_map.update(input_dict or kwargs)

        self._query_response('EDIT')
        return self._process_input(param_map)

    def print_aliases(self):
        self.level=1
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw

    def clear(self):
        self.level=1
        self._query_response('CLEAR')
        self._to_the_top(self.level)

    def import_aliases(self, import_file=REQUIRED):
        self.level=1
        self._query_response('IMPORT')
        self._query_response(import_file)
        self._to_the_top(self.level)

    def export_aliases(self, export_file=REQUIRED):
        self.level=1
        self._query_response('EXPORT')
        self._query_response(export_file)
        self._to_the_top(self.level)

    def delete(self, domain=DEFAULT, alias=REQUIRED):
        self.level=1
        self._query_response('DELETE')
        self._query_select_list_item(domain)
        self._query_select_list_item(alias)
        if self._get_input_list_length() > 1:
            self.level=2
        self._to_the_top(self.level)

if __name__ == '__main__':

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    alc = aliasconfig(cli_sess)

    alc().new(aliases_apply='Add a new domain context',
              domain_context='domain.context', aliases='aliases',
              address='address@ua.com', another_alias=YES)
    print alc().print_aliases()
    alc().new(aliases_apply='Globally', aliases='aliases1',
              address='address1@ua.com', another_alias=YES)
    alc().edit(domain_context='domain.context',
               alias='aliases: address@ua.com',
               address='address@new.com')
    alc().delete(domain='2', alias='aliases: address@new.com')
    alc().export_aliases(export_file='file')
    alc().clear()
    alc().import_aliases(import_file='file')
    print alc().print_aliases()
    alc().clear()
