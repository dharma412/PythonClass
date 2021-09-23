import clictorbase as ccb
from sal.deprecated.expect import EXACT, REGEX

class csaconfig(ccb.IafCliConfiguratorBase):

    class EmptyTokenError(ccb.IafCliError): pass
    class PollingIntervalTimeError(ccb.IafCliError): pass

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('The CSA token should not',
                           EXACT): self.EmptyTokenError,
             ('The polling interval must be a time interval between 1 hour and 7 days',
                           EXACT): self.PollingIntervalTimeError, 
              })
             
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def enable(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['csa_region'] = ['Select the CSA region to connect', ccb.DEFAULT, 1]
        param_map['csa_token'] = ['Please enter the CSA token for the region selected', ccb.REQUIRED]
        param_map['csa_polling_interval'] = ['Please specify the Poll Interval', ccb.DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('ENABLE')
        self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['csa_region'] = ['Select the CSA region to connect', ccb.DEFAULT, 1]
        param_map['csa_set_token'] = ['Do you want to set the token', ccb.DEFAULT]
        param_map['csa_token'] = ['Please enter the CSA token for the region selected', ccb.REQUIRED]
        param_map['csa_polling_interval'] = ['Please specify the Poll Interval', ccb.DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('EDIT')
        self._process_input(param_map)

    def disable(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['csa_disable'] = ['Are you sure you want to disable CSA', ccb.DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('DISABLE')
        self._process_input(param_map)

    def showlist(self):
        self._query_response('SHOW_LIST')
        csalist = [(r'Report ID\s+:\s+(\d.+)\nLast Updated\s+:\s+(\d.+)\nList Status\s+:\s+(.+)\n', REGEX)]
        mo = self._expect(csalist, timeout=60)
        if mo:
            report_id = int(mo.group(1))
            last_updated = mo.group(2)
            list_status = mo.group(3)
            self._to_the_top(1)
            return  showlistCsa(report_id, last_updated, list_status)
        else:
            # Failed to get showlist information 
            self._to_the_top(1)
            raise ConfigError, "Couldn't parse output from show_list command"    
     
    def updatelist(self):
        self.clearbuf()
        self._query_response('UPDATE_LIST')
        self._writeln('\n')
        output = self._wait_for_prompt()
        return output
 
class showlistCsa:
    def __init__(self, report_id='', last_updated='', list_status=''):
        self.report_id = report_id
        self.last_updated = last_updated
        self.list_status = list_status

    def __str__(self):
        return 'Report_id :    %\s\nLast Updated :  %s\nList Status :  %s' %(self.report_id, self.last_updated, self.list_status)  

