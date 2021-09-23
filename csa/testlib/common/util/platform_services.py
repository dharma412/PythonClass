#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/util/platform_services.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import time

from pysphere import VIServer
import common.Variables

import sal.time
from sal.net.ipmilib import IPMIController, IpmiDisabledError, \
    is_ipmi_present_for_host


class PlatformServices(object):
    def __init__(self, dut):
        self.dut = dut
        self._controller = self._get_controller()

    def _get_controller(self):
        raise NotImplementedError('Should be implemented in subclasses')

    def power_on(self, timeout=300, poweroff_timeout=180):
        raise NotImplementedError()

    def power_off(self, timeout=300, poweron_timeout=180):
        raise NotImplementedError()

    def reset(self, poweron_timeout=180):
        raise NotImplementedError()


class IPMIServices(PlatformServices):
    SLEEP_INTERVAL = 10

    def _get_controller(self):
        if not is_ipmi_present_for_host(self.dut):
            raise IpmiDisabledError('IPMI controller not enabled or not present ' \
                                    'for host %s' % (self.dut,))
        return IPMIController(self.dut)

    def power_on(self, timeout=300, poweroff_timeout=180):
        power_strip = self._controller
        # Just to make sure the box is currently off
        tmr = sal.time.CountDownTimer(poweroff_timeout).start()
        while tmr.is_active():
            if power_strip.get_ipmi() == 'off':
                break
            time.sleep(self.SLEEP_INTERVAL)
        if power_strip.get_ipmi() == 'off':
            print('Powering on the box %s via IPMI...' % (self.dut,))
            power_strip.set_ipmi('on')
            tmr = sal.time.CountDownTimer(timeout).start()
            while tmr.is_active():
                time.sleep(self.SLEEP_INTERVAL)
                if power_strip.get_ipmi() == 'on':
                    print('Box is powered on in %s' % tmr.time_elapsed())
                    break
            else:
                raise TimeoutError, 'Too long to wait over %d seconds for box' \
                                    ' powered on' % (timeout,)

    def power_off(self, timeout=300, poweron_timeout=180):
        power_strip = self._controller
        # Just to make sure the box is currently on
        tmr = sal.time.CountDownTimer(poweron_timeout).start()
        while tmr.is_active():
            if power_strip.get_ipmi() == 'on':
                break
            time.sleep(self.SLEEP_INTERVAL)
        if power_strip.get_ipmi() == 'on':
            print('Shutting down the box %s via IPMI...' % (self.dut,))
            power_strip.set_ipmi('off')
            tmr = sal.time.CountDownTimer(timeout).start()
            while tmr.is_active():
                time.sleep(self.SLEEP_INTERVAL)
                if power_strip.get_ipmi() == 'off':
                    print('Box is powered off in %s' % tmr.time_elapsed())
                    break
            else:
                raise TimeoutError, 'Too long to wait over %d seconds for box' \
                                    ' powered off' % (timeout,)

    def reset(self, poweron_timeout=180):
        power_strip = self._controller
        # Just to make sure the box is currently on
        tmr = sal.time.CountDownTimer(poweron_timeout).start()
        while tmr.is_active():
            if power_strip.get_ipmi() == 'on':
                break
            time.sleep(self.SLEEP_INTERVAL)
        else:
            raise AssertionError('The box %s could not be reset since it is ' \
                                 'shut down' % (self.dut,))
        print('Resetting the DUT...')
        power_strip.set_ipmi('reset')

    def set_pxe_boot_device(self):
        print('Setting boot device of %s to pxe...' % (self.dut,))
        self._controller.set_boot_device_to_pxe()


class VMWareServices(PlatformServices):
    SLEEP_INTERVAL = 10

    def _get_controller(self):
        """Returns tuple of 2 elements. The first element is VIserver instance and
        the second - VIVirtualMachine instance.
        Do not forget to disconnect the VIServer instance after all necessary
        operations are finished"""
        VNODES = common.Variables.get_variables()['${VSPHERES}']
        controller = None
        server = VIServer()
        for ip, user, password in VNODES:
            server.connect(ip, user, password)
            try:
                controller = (server, server.get_vm_by_name(self.dut))
            except:
                server.disconnect()
            if controller is not None:
                print('Found VM %s in VSphere server %s' % (self.dut, ip))
                return controller
        print('Cannot find VM %s in any of VSphere servers:\n%s' % \
              (self.dut, VNODES))
        server.disconnect()
        raise ValueError('Could not find given vm name %s' % (self.dut,))

    def power_on(self, timeout=300, poweroff_timeout=180):
        server, vm = self._get_controller()
        try:
            tmr = sal.time.CountDownTimer(poweroff_timeout).start()
            while tmr.is_active():
                if vm.is_powered_off():
                    break
                time.sleep(self.SLEEP_INTERVAL)
            if vm.is_powered_off():
                print('Powering on the box %s via VSphere...' % (self.dut,))
                vm.power_on()
                tmr = sal.time.CountDownTimer(timeout).start()
                while tmr.is_active():
                    if vm.is_powered_on():
                        time.sleep(self.SLEEP_INTERVAL)
                        print('Box is powered on in %s' % tmr.time_elapsed())
                        break
                else:
                    raise TimeoutError, 'Too long to wait over %d seconds for box' \
                                        ' powered on' % (timeout,)
        finally:
            server.disconnect()

    def power_off(self, timeout=300, poweron_timeout=180):
        server, vm = self._get_controller()
        try:
            tmr = sal.time.CountDownTimer(poweron_timeout).start()
            while tmr.is_active():
                if vm.is_powered_on():
                    break
                time.sleep(self.SLEEP_INTERVAL)
            if vm.is_powered_on():
                print('Shutting down the box %s via VSphere...' % (self.dut,))
                vm.power_off()
                tmr = sal.time.CountDownTimer(timeout).start()
                while tmr.is_active():
                    time.sleep(self.SLEEP_INTERVAL)
                    if vm.is_powered_off():
                        print('Box is powered off in %s' % tmr.time_elapsed())
                        break
                else:
                    raise TimeoutError, 'Too long to wait over %d seconds for box' \
                                        ' powered off' % (timeout,)
        finally:
            server.disconnect()

    def reset(self, poweron_timeout=180):
        server, vm = self._get_controller()
        try:
            tmr = sal.time.CountDownTimer(poweron_timeout).start()
            while tmr.is_active():
                if vm.is_powered_on():
                    break
                time.sleep(self.SLEEP_INTERVAL)
            else:
                raise AssertionError('The box %s could not be reset since it is ' \
                                     'shut down' % (self.dut,))
            print('Resetting the box %s...' % (self.dut,))
            vm.reset()
        finally:
            server.disconnect()
