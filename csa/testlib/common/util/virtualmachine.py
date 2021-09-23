# $Id: //prod/main/sarf_centos/testlib/common/util/virtualmachine.py#2 $
# $DateTime: 2019/05/09 05:20:37 $
# $Author: bimmanue $

from pysphere import VIServer
import time
from common.util.utilcommon import UtilCommon
from common.util.systools import SysTools

import common.Variables
import ssl

class VMNotFoundError(Exception): pass
class VMSnapshotNotFoundError(Exception): pass


class VirtualMachine(UtilCommon):
    """This class has methods that interact with the VMs that we use in our
       automation.
    """

    def get_keyword_names(self):
        return [
                'reset_virtual_machine',
                'is_virtual_machine',
                ]

    def _connect_to_esx_server(self, ip, user, password):
        default_context = ssl._create_default_https_context
        ssl._create_default_https_context = ssl._create_unverified_context
        self.server = VIServer()
        self.server.connect(ip, user, password)

    def _find_virtual_machine(self, virtualmachine=None):
        """This method tries to find the vm in all our vsphere servers.
         If VM is found it sets self.vm to the VIVirtualMachine object
         retrieved from the VSphere
         If VM is not found it throws a VMNotFoundError exception"""
        self.vm = None
        for ip, user, password in common.Variables.get_variables()['@{VSPHERES}']:
            self._connect_to_esx_server(ip, user, password)
            try:
                self.vm = self.server.get_vm_by_name(virtualmachine)
                self._debug('Found VM %s in vsphere server %s' % \
                            (virtualmachine, ip))
                break
            except:
                self.server.disconnect()
        if not self.vm:
            self._debug('Cannot find VM  %s in any of our vsphere servers' % \
                        (virtualmachine))
            self.server.disconnect()
            raise VMNotFoundError, 'could not find given vm name -%s'  \
                % (virtualmachine)
        return

    def is_virtual_machine(self, vmname=None):
        'Returns True if virtual else returns False'
        try:
            if vmname.split('.')[1] in ['aws']:
                return True
            self._find_virtual_machine(virtualmachine=vmname)
            self._debug('Yes, %s is a virtual machine' % (vmname))
            return True
        except Exception as error:
            self._debug('No, %s is not a virtual machine\nERROR:%s' % (vmname, error))
            return False

    def reset_virtual_machine(self, vmname=None, wait_for_ports=None):
        """Resets virtual machine

        Parameters:
            - `vmname`: The name of the VM that is to be resetted.
                        By default uses value of variable DUT

            - `wait_for_ports`: string of comma separated pairs
               [interface:]port. If interface is skip then Management interface
               is used.

        Examples:
        | Reset Virtual Machine | vmname=wsa081.wga |"""

        vmname = vmname or self.dut
        if not vmname:
            raise ValueError, 'Attribute vmname cannot be blank/None.Given- %s' \
                % (vmname)
        self._debug('using vmname as %s' % (vmname))
        if self.is_virtual_machine(vmname):
            myvm = self.vm
        if myvm:
            # Pre-check for reset - If DUT is up then return
            try:
                SysTools(vmname, None).wait_until_dut_is_accessible(timeout=3, \
                                                wait_for_ports=wait_for_ports)
                self._debug('VM %s is up and accessible' % (vmname))
                return
            except:
                # power the VM ON if it is just shutdown
                if not myvm.is_powered_on():
                    myvm.power_on()
                time.sleep(60)
                # Reset the VM once its powered ON
                if myvm.is_powered_on():
                    myvm.reset()
            # Post-check for reset - Check if DUT is up
            try:
                SysTools(vmname, None).wait_until_dut_is_accessible(timeout=120, \
                                                wait_for_ports=wait_for_ports)
            except:
                self._debug('Recovery Failed! for VM %s' % (vmname))
                raise
        self.server.disconnect()

