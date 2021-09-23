import clictorbase
import re   
from clictorbase import DEFAULT, REQUIRED, IafCliParamMap, IafCliConfiguratorBase
from sal.containers.yesnodefault import YES, is_yes
from sal.deprecated.expect import REGEX, EXACT


class oidcconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {
                ('An http/https URL must consist', EXACT): clictorbase.IafCliValueError,
                ('Please enter a value', EXACT): clictorbase.IafCliValueError,
                ('At least one group mapping has to be created', EXACT): clictorbase.IafCliValueError,
                ('Unknown option.  Select one of the listed options', EXACT): clictorbase.IafCliValueError
            },
            use_global_err_dict=False
        )
        self._global_err_dict = {}
    
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(
            end_of_command='Create a new external group mapping')
        param_map['metadata_url'] = [
            'Enter the value for metadata URL', REQUIRED]
        param_map['issuer'] = ['Enter the value for "issuer"', REQUIRED]
        param_map['role'] = [
            'Enter the value for "claim" that contains role information', REQUIRED]
        param_map['audience'] = ['Enter the value for "audience"', REQUIRED]
        param_map['create_group_mappings'] = [
            'Do you want to create an external group mappings', DEFAULT]
        
        # Create a temp kwargs dictionary to avoid Unanswered Question error for 'mappings' param.
        # Use the temp kwargs in param map -> update and _process_input
        tmp_kwargs = kwargs.copy()
        del tmp_kwargs['role_mappings']

        param_map.update(input_dict or tmp_kwargs)
        self._query_response('SETUP')
        self._process_input(param_map, do_restart=False)

        if 'create_group_mappings' in kwargs and is_yes(kwargs['create_group_mappings']):
            self._add_role_mappings(**kwargs)
        else:
            self._to_the_top(3)
    
    def edit(self, input_dict=None, **kwargs):
        self._configure_oidc_settings(input_dict, **kwargs)
        if 'mappings_edit_action' in kwargs:
            if kwargs['mappings_edit_action'].lower() == 'add':
                self._add_role_mappings(**kwargs)
            elif kwargs['mappings_edit_action'].lower() == 'edit':
                self._edit_role_mappings(**kwargs)
            elif  kwargs['mappings_edit_action'].lower() == 'delete':
                self._delete_role_mappings(**kwargs)
        else:
            self._to_the_top(3)

    def delete(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['remove_oidc_config'] = ['Are you sure you want to remove all', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('DELETE')
        self._process_input(param_map)

    def mapping_new(self, input_dict=None, **kwargs):
        self._configure_oidc_settings(input_dict, **kwargs)
        self._add_role_mappings(**kwargs)

    def mapping_edit(self, input_dict=None, **kwargs):
        self._configure_oidc_settings(input_dict, **kwargs)
        self._edit_role_mappings(**kwargs)

    def mapping_delete(self, input_dict=None, **kwargs):
        self._configure_oidc_settings(input_dict, **kwargs)
        self._delete_role_mappings(**kwargs)

    def mapping_print(self, input_dict=None, **kwargs):
        self._configure_oidc_settings(input_dict, **kwargs)
        self.clearbuf()
        self._query_response('PRINT')
        self._to_the_top(2)
        return re.findall(r'(\d+\.\s+.*->.*)\r', self.getbuf())

    # Helper Methods
    def _configure_oidc_settings(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Create a new external group mapping')
        param_map['metadata_url'] = ['Enter the value for metadata URL', DEFAULT]
        param_map['issuer'] = ['Enter the value for "issuer"', DEFAULT]
        param_map['role'] = ['Enter the value for "claim" that contains role information', DEFAULT]
        param_map['audience'] = ['Enter the value for "audience"', DEFAULT]
        param_map['create_group_mappings'] = ['Do you want to create an external group mappings', DEFAULT]

        # Create a temp kwargs dictionary to avoid Unanswered Question error for 'mappings' param.
        # Use the temp kwargs in param map -> update and _process_input
        tmp_kwargs = kwargs.copy()
        if 'role_mappings' in kwargs:
            del tmp_kwargs['role_mappings']
        if 'mappings_edit_action' in kwargs:
            del tmp_kwargs['mappings_edit_action']

        param_map.update(input_dict or tmp_kwargs)
        self._query_response('SETUP')
        self._process_input(param_map, do_restart=False)

    def _add_role_mappings(self, **kwargs):        
        self._query_response('NEW')
        for group_name, role in eval(kwargs['role_mappings']).items():
            self._query_response(group_name)
            self._query_select_list_item(role)
        else:
            self._to_the_top(4)

    def _edit_role_mappings(self, **kwargs):        
        self._query_response('EDIT')
        for group_name, role in eval(kwargs['role_mappings']).items():
            self._query_select_list_item(group_name)
            self._query_select_list_item(role)
        else:
            self._to_the_top(3)
    
    def _delete_role_mappings(self, **kwargs):
        for mapping in eval(kwargs['role_mappings']):
            self._query_response('DELETE')
            self._query_select_list_item(mapping)
        else:
            self._to_the_top(3)

