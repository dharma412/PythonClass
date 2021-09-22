#!/usr/bin/env python
import os, commands, ConfigParser, time, sys
from ConfigParser import SafeConfigParser

def check_inventory():
    os.system('cp /data/var/log/atlas/vm_inventory/vm_inventory.log /data/var/log/atlas/vm_inventory/vm_inventory_backup.log')
    os.system(''' export ATLAS_HOME=/usr/local/ironport/atlas && python /usr/local/ironport/atlas/automator/resourceprovisioner/VmManager.py''')
    commandset = ('cat /data/var/log/atlas/vm_inventory/vm_inventory.log | grep -iE "All ESA/SMA model VMs are more than set threshold value"')
    status=os.system(commandset)
    if(status==0):
        print('Unlock vmmanager cron')
        os.system('mysql -h 10.9.130.31 -uatlas -patlas atlas_auto_dev1 -e "update crons set result=0, mon_lock=NULL, fail_count=0 where command=\'vm_manager\';"')
	return False
    configerror = ('cat /data/var/log/atlas/vm_inventory/vm_inventory.log | grep -iE "A host with default ip : 192.168.42.42 already exist."')
    status=os.system(configerror)
    if(status==0):
        return True
    command1=('cat /data/var/log/atlas/vm_inventory/vm_inventory.log | grep -iE "VM created successfully with name :"')
    status=os.system(command1)
    if(status==0):
        print('Server creation is successful.Check for configuration of servers')
    else:
        print('Inventory is failing at Server creation step')
        raise Exception
    commands.getstatusoutput('cat /data/var/log/atlas/vm_inventory/vm_inventory.log | grep -iE "VM created successfully with name :" > Server_data')
    ServerName=os.system("awk '{ print $11 }' Server_data > ServerName")
    with open ('ServerName' , 'r') as file:
        ServerCreated=file.readline()
    configurepattern = 'Successfully configured & imported' + " {}".format(ServerCreated.strip())
    print('checking autoimport logs for configuration of server')
    command2= 'grep "{}"'.format(configurepattern) + ' /data/var/log/atlas/vm_inventory/vm_inventory.log'
    configurestatus=os.system(command2)
    if(configurestatus==0):
        print('Server is configured. IP Address allocation is complete. Verify if server is imported to database')
    else:
        print('Inventory creation is failing at Configuration step')
        raise Exception
    importpattern = "Server {}".format(ServerCreated.strip()) + " got imported successfully"
    command3= 'grep "{}"'.format(importpattern) + ' /data/var/log/atlas/vm_inventory/vm_inventory.log' + "| awk '{print $6 }'"
    importstatus=os.system(command3)
    if(importstatus==0):
        print('Server is imported to Database.Inventory creation is complete')
    else:
        print('Inventory creation is failing at Import to Database step')
        raise Exception
    print('Roll over the existing VM Inventory logs')
    os.system('du -s /data/var/log/atlas/vm_inventory/vm_inventory.log')
    os.system('cat /dev/null > /data/var/log/atlas/vm_inventory/vm_inventory.log')
    os.system('du -s /data/var/log/atlas/vm_inventory/vm_inventory.log')
    return True

parser = SafeConfigParser()
parser.read('/usr/local/ironport/atlas/etc/vm_inventory.conf')
datacenter = parser.get('inventory', 'datacenter')
model = parser.get('inventory', 'vm_models')
print('Inventory will run for  %s' % (datacenter))
print('VM model is %s' % (model))
if(datacenter=='DC1' and  model=='C100V' or  model=='C100V,M100V'):
    status = check_inventory()
    parser.set('inventory', 'vm_models', 'C100V')
    parser.set('inventory', 'datacenter', 'DC2')
    parser.set('inventory', 'num_vm_upper_limit','10')
    with open('/usr/local/ironport/atlas/etc/vm_inventory.conf', 'w') as configfile:
        parser.write(configfile)
    datacenter = parser.get('inventory', 'datacenter')
    model = parser.get('inventory', 'vm_models')
    print('Next Run for Inventory will be for  %s and %s' % (datacenter, model))
    if (not status):
        print("Exiting the inventory creation script...")
        sys.exit()
elif(datacenter=='DC2' and model=='C100V' or model=='C100V,M100V'):
    status = check_inventory()
    parser.set('inventory', 'datacenter', 'DC1')
    parser.set('inventory', 'vm_models', 'M100V')
    parser.set('inventory', 'num_vm_upper_limit','5')
    with open('/usr/local/ironport/atlas/etc/vm_inventory.conf', 'w') as configfile:
        parser.write(configfile)
    datacenter = parser.get('inventory', 'datacenter')
    model = parser.get('inventory', 'vm_models')
    print('Next Run for Inventory will be  for  %s and %s' % (datacenter, model))
    if (not status):
        print("Exiting the inventory creation script...")
        sys.exit()
elif(datacenter=='DC1' and model=='M100V' or model=='C100V,M100V'):
    status = check_inventory()
    parser.set('inventory', 'datacenter', 'DC1')
    parser.set('inventory', 'vm_models', 'C100V')
    parser.set('inventory', 'num_vm_upper_limit','5')
    with open('/usr/local/ironport/atlas/etc/vm_inventory.conf', 'w') as configfile:
        parser.write(configfile)
    datacenter = parser.get('inventory', 'datacenter')
    model = parser.get('inventory', 'vm_models')
    print('Next Run for Inventory will be  for  %s and %s' % (datacenter, model))
    if (not status):
        print("Exiting the inventory creation script...")
        sys.exit()
