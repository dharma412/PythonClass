# $Id:  $
# $DateTime:  $
# $Author:  $

from clictorbase import IafCliConfiguratorBase

class csnconfig(IafCliConfiguratorBase):
    """ cli->csnconfig - Change CSN configuration. """
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
	self._writeln('csnconfig')
	return self

    def enable(self):
	self.new_lines = 1
	self._writeln('enable')
	self._to_the_top(self.new_lines)

    def disable(self):
	self.new_lines = 1
	self._writeln('disable')
	self._to_the_top(self.new_lines)

