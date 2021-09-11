import os
import mysql.connector as mysql
import os.path as path


ATLAS_CONSTANTS= {}
atlas_home =os.environ['ATLAS_HOME']
config_builder_path =  path.abspath(path.join(atlas_home ,"../"))
with open("{}/.configbuilder/_usr_local_ironport_atlas_etc".format(config_builder_path)) as f:
    for line in f.readlines():
        (key,val) = line.split("=")
        ATLAS_CONSTANTS[key.strip()]= val.strip()

data ={
    'host': ATLAS_CONSTANTS['django_db_host'],
    'user': ATLAS_CONSTANTS['django_db_user'],
    'password': ATLAS_CONSTANTS['django_db_passwd'],
    'database':ATLAS_CONSTANTS['django_db_name']
}

def get_datacenter(host,user,password,database):
    atlasdb_con = mysql.connect(host = host,
                                user = user,
                                password = password,
                                database= database,
                                )
    atlasdb_cursor = atlasdb_con.cursor()
    atlasdb_cursor.execute('select location from atlas_datacenter')
    rows = atlasdb_cursor.fetchall()
    atlasdb_con.close()
    return [ r[0] for r in rows]

data_centers = get_datacenter(data['host'],data['user'],data['password'],data['database'])

p = os.popen("cat {}/etc/vm_inventory.conf | grep datacenter | cut -d '=' -f 2".format(atlas_home))
current_datacenter = p.read().rstrip()

if current_datacenter == data_centers[1]:
    os.system( ''' sed -i 's/datacenter=.*/datacenter={}/' {}/etc/vm_inventory.conf '''.format(data_centers[0],atlas_home))
else:
    os.system('''sed -i 's/datacenter=.*/datacenter={}/' {}/etc/vm_inventory.conf'''.format(data_centers[1],atlas_home))

