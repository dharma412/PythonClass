# $Id:
# $DateTime:
# $Author:

import clictorbase


class outbreakconfigclicktrackingenable(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('outbreakconfig clicktracking enable')
        outbreakconfigclicktrackingenable_output = ''
        outbreakconfigclicktrackingenable_output = self._wait_for_prompt()
        output = [y for y in (x.strip() for x in outbreakconfigclicktrackingenable_output.splitlines()) if y]
        return output[1]
