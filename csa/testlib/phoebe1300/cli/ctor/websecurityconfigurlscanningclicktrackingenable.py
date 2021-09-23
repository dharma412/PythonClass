# $Id:
# $DateTime:
# $Author:

import clictorbase


class websecurityconfigurlscanningclicktrackingenable(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('websecurityconfig urlscanning clicktracking enable')
        websecurityconfigurlscanningclicktrackingenable_output = ''
        websecurityconfigurlscanningclicktrackingenable_output = self._wait_for_prompt()
        output = [y for y in (x.strip() for x in websecurityconfigurlscanningclicktrackingenable_output.splitlines()) if
                  y]
        return output[1]
