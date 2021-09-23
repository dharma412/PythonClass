# $Id:
# $DateTime:
# $Author:

import clictorbase

class outbreakconfigclicktrackingdisable(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('outbreakconfig clicktracking disable')
        outbreakconfigclicktrackingdisable_output = ''
        outbreakconfigclicktrackingdisable_output = self._wait_for_prompt()
        output= [y for y in (x.strip() for x in outbreakconfigclicktrackingdisable_output.splitlines()) if y]
        return output[1]