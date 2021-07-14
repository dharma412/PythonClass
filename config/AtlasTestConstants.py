import json
import os
import subprocess
import string
import random

from  collections import namedtuple


path = os.path.dirname(os.path.abspath(__file__))
atlas_filepath = os.path.join(path,'atlas_filepath.json')
atlas_servers = os.path.join(path,'atlas_servers.json')
atlas_customer = os.path.join(path,'atlas_customer.json')
atlas_config = os.path.join(path,'atlas_config.json')
atlas_constant = os.path.join(path,'atlas_constants.conf')

with open(atlas_servers) as jsonfile:
    server_config = json.load(jsonfile)

with open(atlas_customer) as jsonfile:
    customer_data = json.load(jsonfile)

with open(atlas_filepath) as jsonfile:
    file_path = json.load(jsonfile)

ATLAS_CONSTANTS= {}
with open(atlas_constant) as f:
    for line in f.readlines():
        (key,val) = line.split("=")
        ATLAS_CONSTANTS[key.strip()]= val.strip()

def get_namedtuple(dictionary):
    return namedtuple('atlas', dictionary.keys())(**dictionary)

JENKINS_SERVER = get_namedtuple(server_config['jenkins_server'])
ATLAS_SERVER = get_namedtuple(server_config['atlas_server'])
ATLAS_UI = get_namedtuple(server_config['atlas_ui'])
allowed_characters = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase+string.digits) for _ in range(5))
customer_data['customer']['customer_name']= customer_data['customer']['customer_name']+allowed_characters
customer_data['customer']['purchase_order']=customer_data['customer']['purchase_order']+allowed_characters
customer_data['customer']['sales_order']=customer_data['customer']['sales_order']+allowed_characters
ATLAS_CUSTOMER_DATA = get_namedtuple(customer_data['customer'])
ATLAS_APPLIANCE= get_namedtuple(server_config['atlas_appliance'])

def get_exportsdb_details(name):
    sql_stmt_dc = 'select virtual_serial  from customer where customer like \'{}\''.format(name)
    Db = ['mysql',
          '-h',ATLAS_CONSTANTS['exports_db_host'],
          '-u',ATLAS_CONSTANTS['exports_db_user'] ,
          '-p'+ ATLAS_CONSTANTS['django_db_passwd'],
          '-D',ATLAS_CONSTANTS['exports_db_name'],
          '-e',sql_stmt_dc]
    data_centers = subprocess.Popen(Db,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    virtual_serial=  str(data_centers.communicate()).split('\\n')[2]
    sql_stmt_dc = 'select virtual_serial, cust_email,salesrep_email,partner_email from hosted_notifications where virtual_serial = \'{}\' '.format(virtual_serial)
    Db = ['mysql','-h',ATLAS_CONSTANTS['exports_db_host'], '-u',ATLAS_CONSTANTS['exports_db_user'] , '-p'+ATLAS_CONSTANTS['django_db_passwd'], '-D',ATLAS_CONSTANTS['exports_db_name'],'-e',sql_stmt_dc]
    data_centers = subprocess.Popen(Db,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    return str(data_centers.communicate()).split('\\n')[2].split('\\t')

ATLAS_EXPORT_CUSTOMER_DATA = {}
ATLAS_EXPORT_CUSTOMER_DATA['customer_name'] = customer_data['exports_customer']['customer_name']
ATLAS_EXPORT_CUSTOMER_DATA['customer_type'] = customer_data['exports_customer']['customer_type']
ATLAS_EXPORT_CUSTOMER_DATA['customer_sub_type'] = customer_data['exports_customer']['customer_sub_type']
ATLAS_EXPORT_CUSTOMER_DATA['virtual_serial'],ATLAS_EXPORT_CUSTOMER_DATA['cust_email'],ATLAS_EXPORT_CUSTOMER_DATA['salesrep_email'],\
ATLAS_EXPORT_CUSTOMER_DATA['partner_email'] = get_exportsdb_details(ATLAS_EXPORT_CUSTOMER_DATA['customer_name'])

def get_datacenters():
   sql_stmt_dc = ' select location from atlas_datacenter'
   Db = ['mysql',
         '-h',ATLAS_CONSTANTS['django_db_host'],
         '-u',ATLAS_CONSTANTS['django_db_user'] ,
         '-p'+ATLAS_CONSTANTS['django_db_passwd'],
         '-D',ATLAS_CONSTANTS['django_db_name'],
         '-e',sql_stmt_dc]
   data_centers = subprocess.Popen(Db,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)

   return  str(data_centers.communicate()).split('\\n')[2:4]

def get_devicemodels():
    sql_stmt_server_model= 'select name from atlas_devicemodel'
    Db = ['mysql',
          '-h',ATLAS_CONSTANTS['django_db_host'],
          '-u',ATLAS_CONSTANTS['django_db_user'] ,
          '-p'+ATLAS_CONSTANTS['django_db_passwd'],
          '-D',ATLAS_CONSTANTS['django_db_name'],
          '-e',sql_stmt_server_model]
    data_centers = subprocess.Popen(Db,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)

    return  str(data_centers.communicate()).split('\\n')

ATLAS_CONSTANTS['appliance_user'] = ATLAS_APPLIANCE.user
ATLAS_CONSTANTS['appliance_password'] =  ATLAS_APPLIANCE.password   
ATLAS_CONSTANTS['primary_datacenter'],ATLAS_CONSTANTS['secondary_datacenter'] = get_datacenters()
for server_model in get_devicemodels()[1:-1]:
    ATLAS_CONSTANTS[server_model] = server_model

for path in file_path:
    for script_config_path in file_path[path]:
        ATLAS_CONSTANTS[script_config_path] = file_path[path][script_config_path]

