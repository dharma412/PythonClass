#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/wsa_reset_gateway.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import sys

sys.path.append('~/work/sarf/testlib/')
import time
import paramiko
import argparse
from sal import time as salTime
from credentials import TESTUSER, \
    TESTUSER_PASSWORD, \
    RTESTUSER, \
    RTESTUSER_PASSWORD

# IBAUTO Related Changes
login_prompt = "password:"
wsa_prompt = "]"
ibauto_csr_ip = "10.8.63.1"
pfsense_ip = "10.8.63.254"
cel_hostname = "bglgrp1216-cel.cisco.com"


def send_command(obj_shell, command, prompt_string):
    obj_shell.send(command)
    output_buffer = ''

    while not output_buffer.endswith(prompt_string):
        resp = obj_shell.recv(9999)
        output_buffer += str(resp).strip()

    # If the user wants to validate anything from output, return buffer.
    return output_buffer


def is_ibauto_dut_pingable_from_csr(cel_ssh_session, hostname, timeout=300):
    cmd_out = ""
    ping_timer = salTime.CountDownTimer(timeout).start()
    ping_command = 'ping -c 1 -t 5 %s' % hostname

    while ping_timer.is_active():
        stdin, stdout, stderr = cel_ssh_session.exec_command(ping_command)
        cmd_out = stdout.read()
        sys.stdout.write("Command Output: Ping: %s\n" % cmd_out)

        # If the output contains NO PACKET LOSS, ping test PASSED.
        if cmd_out.find(" 0% packet loss") != -1:
            return True

        sys.stdout.write("Device not reachable yet.\n")
        time.sleep(30)

    sys.stdout.write("Device not reachable from CSR within timeout: %d.\n" % timeout)
    return False


def is_dut_port22_reachable_from_csr(hostname, prompt_string, timeout):
    flag_port22_up = False
    output_buffer = ''
    port_timer = salTime.CountDownTimer(timeout).start()
    dut_connection_string = "ssh %s@%s\n" % (RTESTUSER, hostname)

    cel_ssh_client = paramiko.SSHClient()
    cel_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cel_ssh_client.connect(cel_hostname, username=TESTUSER, password=TESTUSER_PASSWORD)
    cel_ssh_shell = cel_ssh_client.invoke_shell()
    sys.stdout.write("Connected to CEL Client for WSA Port 22 Check.\n")

    sys.stdout.write("Check Port Status: CSR > DUT\n")
    loop_ctr = 1
    while True:
        try:
            sys.stdout.write("Check Port Status: CSR> DUT: Attempt...%d\n" % loop_ctr)
            loop_ctr += 1

            sys.stdout.write("Check Port Status: Send> %s\n" % dut_connection_string)
            cel_ssh_shell.send(dut_connection_string)

            if cel_ssh_shell.recv_ready():
                sys.stdout.write("Shell is receive ready.\n")
                resp = cel_ssh_shell.recv(9999)
                if resp:
                    output_buffer += str(resp).strip()
                if output_buffer.endswith(prompt_string):
                    sys.stdout.write("DUT is at Prompt: %s\n" % prompt_string)
                    flag_port22_up = True
                    break
        except:
            pass

        time.sleep(60)
        if not port_timer.is_active():
            break
    try:
        if cel_ssh_shell:
            cel_ssh_shell.close()
        if cel_ssh_client:
            cel_ssh_client.close()
    except:
        pass

    return flag_port22_up


def change_gateway_to_csr(celhost, hostname):
    cel_ssh_client = paramiko.SSHClient()

    setfib_command = "setfib 0 route change default %s\n" \
                     % ibauto_csr_ip
    edit_config_cmd = \
        "sed -i -e 's/%s/%s/' /etc/rc.conf.local\n" \
        % (pfsense_ip, ibauto_csr_ip)
    edit_route_cmd = \
        "sed -i -e 's/%s/%s/' /data/db/config/system.network/data.cfg.factory\n" \
        % (pfsense_ip, ibauto_csr_ip)
    dut_connection_string = "ssh %s@%s\n" % (RTESTUSER, hostname)

    cel_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        cel_ssh_client.connect(celhost, username=TESTUSER, password=TESTUSER_PASSWORD)
        sys.stdout.write("Connected to CEL Client.\n")

        if is_ibauto_dut_pingable_from_csr(cel_ssh_client, hostname, 300):
            sys.stdout.write("Device is Pingable from CSR.\n")

            flag_dut_ssh_ready = False
            try:
                # See if the DUT port 22 is accessible in 60 Minutes.
                flag_dut_ssh_ready = is_dut_port22_reachable_from_csr(
                    hostname,
                    login_prompt,
                    3600
                )
            except:
                pass

            if flag_dut_ssh_ready:
                sys.stdout.write("Port 22 Is Reachable from CSR.\n")
                cel_ssh_shell = cel_ssh_client.invoke_shell()

                sys.stdout.write("Make the IBAUTO Gateway changes to WSA.\n")
                sys.stdout.write("Login to DUT.\n")
                send_command(cel_ssh_shell, dut_connection_string, login_prompt)
                send_command(cel_ssh_shell, '%s\n' % RTESTUSER_PASSWORD, wsa_prompt)

                sys.stdout.write("FreeBSD Route and Config Changes...\n")
                sys.stdout.write("Route Change: %s\n" % setfib_command)
                send_command(cel_ssh_shell, setfib_command, wsa_prompt)
                sys.stdout.write("[rc.conf.local] Change: %s\n" % edit_config_cmd)
                send_command(cel_ssh_shell, edit_config_cmd, wsa_prompt)
                sys.stdout.write(
                    "[/data/db/config/system.network/data.cfg.factory] Change: %s\n"
                    % edit_route_cmd
                )
                send_command(cel_ssh_shell, edit_route_cmd, wsa_prompt)

                sys.stdout.write("Set CLI> setgateway in WSA and Commit.\n")
                send_command(cel_ssh_shell, "cli\n", ">")
                send_command(cel_ssh_shell, "setgateway\n", ">")
                send_command(cel_ssh_shell, "1\n", ">")
                send_command(cel_ssh_shell, "%s\n" % ibauto_csr_ip, ">")
                send_command(cel_ssh_shell, "commit\n", ">")
                send_command(cel_ssh_shell, "\n", ">")
                sys.stdout.write("Gateway has been changed from PFSENSE to CSR.\n")
                cel_ssh_shell.close()
                cel_ssh_client.close()
            else:
                sys.stdout.write("ERROR | TIMEOUT: 60 MINUTES | "
                                 "DUT IS NOT SSH READY. Device: %s.\n" % hostname)
                sys.stdout.write('Please connect to WSA: %s from: %s\n' % (hostname, celhost))
                sys.stdout.write('--------------------------------------------\n')
                sys.stdout.write('  Run the following commands on WSA\n')
                sys.stdout.write('--------------------------------------------\n')
                sys.stdout.write('  1. WSA FreeBSD Prompt:\n')
                sys.stdout.write('    a. %s\n' % setfib_command)
                sys.stdout.write('    b. %s\n' % edit_config_cmd)
                sys.stdout.write('    c. %s\n' % edit_route_cmd)
                sys.stdout.write('  2. WSA CLI:\n')
                sys.stdout.write('    > setgateway\n')
                sys.stdout.write('    > 1\n')
                sys.stdout.write('    > commit\n')
                sys.stdout.write('--------------------------------------------\n')
                raise Exception("DUT is not ssh ready. Device: %s.\n" % hostname)

        else:
            raise Exception("Device not Pingable. Device: %s." % hostname)

    except Exception as e:
        raise Exception(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--wsa",
        type=str,
        help="WSA Hostname",
        default=""
    )

    prog_args = parser.parse_args()
    wsa_hostname = prog_args.wsa
    if wsa_hostname.split('.')[-1].lower() == 'ibauto':
        sys.exit(change_gateway_to_csr(cel_hostname, prog_args.wsa))


if __name__ == '__main__':
    sys.exit(main())
