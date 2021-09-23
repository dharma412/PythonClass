# $Id: //prod/main/sarf_centos/testlib/GuiLibraryEveryTest.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from GuiLibrary import GuiLibrary


class GuiLibraryEveryTest(GuiLibrary):
    """ Library that is loaded with every test
    That takes more time, but is required when product's version changes
    after upgrade or revert
    """
    ROBOT_LIBRARY_SCOPE = 'TEST CASE'
