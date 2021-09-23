#!/usr/bin/env python

from common.util.utilcommon import UtilCommon


class BackdoorInterface(UtilCommon):
    """
       This is the backdoor interface tool.
       Using this scripts can be executed directly connecting to the
       process via backdoor.
    """

    def get_keyword_names(self):
        return [
            'backdoor_run',
        ]

    def backdoor_run(self, app_name=None, code_list=()):
        """Starts a process.

        Parameters:
           - `app_name`: name of process to start.
           - `code_list`: the code to be executed. Input the code as a list
                          with each member of list corresponds to a line in code
                          Refer Examples

        Examples:
        | @{code_list}= | Create List | from euq.manager import euq_shell |
        | ... | sch = euq_shell.sch  | n=sch.nscheduler |
        | ... | n.runjob(sch.Job(0,0)) | n.runjob() |

        | Backdoor Run  | app_name=euq_server | ${code_list} |
        """
        return self._shell.backdoor.run(app_name=app_name, code_list=code_list)
