#!/usr/bin/env python
""" Generate a feature key for an appliance component.

    The available components are:
        imh nsub body_contains Brightmail mcafee
        sophos clustering VOF throttle throttle_dynamic
        throttle_increment RemoteUpgrades ipas

    See usage() for more information.
"""

import sys
import getopt
import time
import warnings
import os

# dynamically add path to testlib
sys.path.append(os.path.join(os.environ['SARF_HOME'],'testlib'))

from sal.net import ping
from common.util import qabd

# Don't enter pdb on exception
sys.excepthook = sys.__excepthook__

try:
    from common.util import featurekey
except:
    print """The featurekey.py module in the godspeed/hermes
             directory must be available to the python interpreter
             for this script to work."""
    sys.exit(0)

# command line options available to this script.
cfg_options = (
        'component=',
        'duration=',
        'duration_additive=',
        'enter_after=',
        'enter_by=',
        'expiry=',
        'hardware_address=',
        'quantity=',
        'clear=',
        'noise=',
        )

short_cut = {
        # short component names
        'Brightmail':'Brightmail',
        'bm':'Brightmail',
        'sophos':'sophos',
}

# cfg_options that require the argument to be an integer
int_options = {'duration':True, 'duration_additive':True,
                'enter_after':True, 'enter_by':True, 'quantity':True}

# features that we can generate keys for
component_dict = {
    'imh':True,
    'unsub':True, # 50000
    'body_contains':True,
    'Brightmail':True,
    'mcafee':True,
    'sophos':True,
    'clustering':True,
    'VOF':True,
    'throttle':True,
    'throttle_dynamic':True,
    'throttle_increment':True,
    'RemoteUpgrades':True,# duration=90
    'ipas':True,
    'max_interfaces':True,
    'case':True,
}

verbose = False

def usage():
    usage = """
Generate a feature key for an appliance's component.

Example:
%s  -v --hardware_address='00065BFE7C7A-8PCM631' --component='ipas' --quantity=1 --duration=3600

Command line options:
        --component           [str: see 'component' list below]
        --duration            [int: seconds] use 0 to create Perpetual key
        --duration_additive   [int: 0, 1]
        --enter_after         [int: seconds]
        --enter_by            [int: seconds]
        --hardware_address    [str: hw address string]
        --quantity            [int: seconds]
        --clear               [str: Yes, No]
        -h                    help screen
        -v                    verbose

Shortcut options
        --Brightmail:       same as --component=Brightmail
        --bm:               same as --component=Brightmail
        --sophos:           same as --component=sophos

Components:
    body_contains Brightmail injection_control max_interfaces
    imh merge_xmrg mailflow SenderBase sophos throttle unsub
    init_max_concurrency default_public_injector clustering VOF
    case

NOTE: See featurekey.py in the godspeed/hermes directory
      for an explanation of each option.
""" % sys.argv[0]
    print usage

def get_args():
    """parse sys.argv and store values in fkey_cfg"""
    global verbose

    if len(sys.argv) <= 1:
        usage()
        sys.exit(0)
    if '-v' in sys.argv[1:]:
        verbose = True
    if '-h' in sys.argv[1:]:
        usage()
        sys.exit(0)

    optlist, args = getopt.getopt(sys.argv[1:], 'vh', cfg_options + tuple(short_cut.keys()))

    today = time.time()
    days_90 = 90 * 24 * 3600
    # set some defaults

    fkey_cfg = {
        'hardware_address': None,
        'component':        'ipas',
        'duration':         30*24*3600,
        'enter_by':         today + days_90,
        'quantity':         1,
    }

    # notes
    #   duration_additive & clear: argument both do nothing!!
    #                   setting either to 0 or 1 will result in
    #                   it being set to None (in feature_keys.py)
    #   enter_by: argument MUST be specified to add short keys
    #       to existing key. Otherwise short key
    #       will simply overwrite existing key!!

    for opt_name, opt_val in optlist:
        opt_name = opt_name[2:]
        if int_options.has_key(opt_name):
            if opt_val == 'forever': opt_val = '0'
            fkey_cfg[opt_name] = eval(opt_val)
        elif short_cut.has_key(opt_name):
            fkey_cfg['component'] = short_cut[opt_name]
        else:
            fkey_cfg[opt_name] = opt_val

        if opt_name == 'component':
            if component_dict.get(opt_val, None) == None:
                print >>sys.stderr, 'warning: component does not exist:',opt_val

    # go out on the network and get the appliance's serial number
    if fkey_cfg['hardware_address'] == None:
        host = iafcfg.get_hostname()
        if not ping.ping(host):
            print >> sys.stderr, host, 'not reachable.'
            print >> sys.stderr, 'Try specifying --hardware_address=<serial#>'
            raise

        # download serial number using DUT's http backdoor
        try:
            dut_info = qabd.QABackdoor(host).get_info()
            fkey_cfg['hardware_address'] = dut_info['serial_number']
        except:
            # use cinnamon.qa serial number
            print "WARNING: Using cinnamon.qa's serial number"
            fkey_cfg['hardware_address'] = '00065BFE7C7A-8PCM631'

    return fkey_cfg

def pretty_print_args(arg_dict):
    """Format and print  the command line arguments."""
    for k in cfg_options:
        k = k[:-1]
        if arg_dict.has_key(k):
            print '%20s %-20s' % (k,arg_dict[k])

if __name__ == '__main__':
    fkey_cfg = get_args()
    noise = fkey_cfg.get('noise', None)
    if noise != None: noise = int(noise)

    fkey = featurekey.generate(fkey_cfg['hardware_address'], noise, fkey_cfg)
    if verbose:
        pretty_print_args(fkey_cfg)
        print fkey_cfg['component'], 'feature key:', fkey
    else:
        print  fkey
