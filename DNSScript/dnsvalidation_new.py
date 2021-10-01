import MySQLdb
import django
import os
import sys
import re
import logging
import atexit
import multiprocessing
import json
import socket

try:
    atlas_home = os.environ.get('ATLAS_HOME',
                                '/usr/local/ironport/atlas/')
    sys.path.append(atlas_home)
    # Need to include automator for util & common packages
    sys.path.append("%s/automator" % (atlas_home,))
    sys.path.append("%s/automator/util" %(atlas_home,))
except KeyError:
    print 'Please set ATLAS_HOME environment variable.'
    sys.exit(1)

os.environ['DJANGO_SETTINGS_MODULE'] = 'etc.django_settings'
django.setup()
from django.conf import settings
from MySQLdb import cursors
from ConfigParser import SafeConfigParser
from time import time
from multiprocessing import Pool
from atlas_server.atlas.models import *
from automator.util.configuration import Configuration
from automator.util.raise_jira_ticket import create_jira_ticket
from django import db

IPTYPE_VIP = 3  # VIP IP Type
IPTYPEO365VIP = 4  # O365VIP IP Type
atlas_home    =  os.environ['ATLAS_HOME']
EXTERNAL_FILE =  os.path.join(atlas_home,'bin/external_view.txt')
INTERNAL_FILE =  os.path.join(atlas_home,'bin/internal_view.txt')
LOG_FILE     = '/var/log/atlas/dnsvalidation.log'
LOG_LEVEL    = settings.LOG_LEVEL
LOG_FORMAT   = settings.LOG_FORMAT
MAX_BYTES    = settings.MAX_BYTES
HOST         = settings.DATABASES['default']['HOST']
USER         = settings.DATABASES['default']['USER']
PASSWORD     = settings.DATABASES['default']['PASSWORD']
DB           = settings.DATABASES['default']['NAME']
PORT         = int(settings.DATABASES['default']['PORT'])

logging.basicConfig(filename=LOG_FILE,level=LOG_LEVEL,format=LOG_FORMAT)
manager = multiprocessing.Manager()
dbconnopenlist = manager.list()
dbconncloselist = manager.list()

jiralist = manager.dict()

dedintprocesses = []
lbintprocesses = []
lbprocesses = []

statuslist = manager.list()
failedlist = manager.dict()
skippedlist = manager.list()
lbstatuslist = manager.list()
lbfailedlist = manager.dict()
lbskippedlist = manager.list()
failed_lb_servers = manager.dict()
failed_dedicated_servers = manager.dict()

povclusters = []

def raise_jira_ticket(data):
    summary = '{}: DNS Validation Failures'.format(settings.DC_SUBTYPE)
    description = data
    script_name = 'DNS_Validation'
    create_jira_ticket(summary, description, script_name)

class DNSVerificationScript:
    def __init__(self):
        self.atlasdbc = None#self.get_connection()
        #atexit.register(self.closeconnection)

    def get_connection(self):
        try:
            #logging.info("Open Connection")
            dbconnopenlist.append(1)
            self.atlas_dbc = MySQLdb.connect(user=USER,
                                        passwd=PASSWORD,
                                        host=HOST,
                                        db=DB)
            self.atlas_dbc.autocommit(1)
        except MySQLdb.Error:
            logging.critical("Error setting up connection to atlas database.  " \
                         "Traceback below:", exc_info=True)
            sys.exit(1)
        return self.atlas_dbc

    def closeconnection(self, dbobj):
        if dbobj:
            #logging.info("Close Connection")
            dbconncloselist.append(0)
            dbobj.close()

def execute_query(atlasdbc, querystring):
    """
     Purpose: executes the select query on the datbase
     Args: query: select query to be executed
     Returns: list of rows
    """
    try:
        cur = atlasdbc.cursor(cursors.DictCursor)
        cur.execute(querystring)
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        logging.error("Exception occured during query execution :{}".format(str(e)))
        logging.error("Get Connection again and retry")
        sys.exit(1)
        #atlasdbc = self.get_connection()
        #execute_query(atlasdbc, querystring)

def getpovclusters():
    c = Cluster.objects.all()
    for i in c:
        cobj = Configuration(i.bundle.id)
        if cobj.config_data.has_key('pov_mode_enabled'):
            povenabled = cobj.config_data.get('pov_mode_enabled')
            if povenabled:
                povclusters.append(str(i.name))

def get_dedicated_allocation_data():
    """
    Purpose :  exeute the select query and returns rows of cluster_id and names
    """
    dbobj = DNSVerificationScript()
    connobj = dbobj.get_connection()
    row_data_dedicated = execute_query(connobj, "select atlas_cluster.id,atlas_cluster.name from atlas_cluster where atlas_cluster.id NOT IN (select DISTINCT(cluster_id)  from atlas_ipaddress where cluster_id IS NOT NULL)")
    dbobj.closeconnection(connobj)
    return row_data_dedicated

def get_lb_allocation_data():
    """
    Purpose  : execute the select query and returns rows of cluster_id and clusternames for lb type
    """
    dbobj = DNSVerificationScript()
    connobj = dbobj.get_connection()
    row_data_allocation = execute_query(connobj, "select atlas_cluster.id,atlas_cluster.name from atlas_cluster where atlas_cluster.id IN (select DISTINCT(cluster_id) from atlas_ipaddress where cluster_id IS NOT NULL)")
    dbobj.closeconnection(connobj)
    return row_data_allocation

def fetch_dnsfile(dnsrecordfile):
    """
    Purpose :  Read and Return the external file records
    """
    with open(dnsrecordfile) as fileobject:
         dnstext = fileobject.read()
    return str(dnstext)

def get_dns_records(filepath,id, dh=None):
    """
    Purpose : This method retunrs the DNS records of the cluster id.
    Argumnets :
       id     : cluster id of the customer
       dh     : dh value of the cluster default is None
    Return  :  Returs the DNS records of the given cluster id
    """
    dnsobj = DNSVerificationScript()
    connobj = dnsobj.get_connection()
    allocation_name_query = "select name from atlas_cluster where id={}".format(id)
    allocation_name = execute_query(connobj, allocation_name_query)
    dnsrecord_text = fetch_dnsfile(filepath)
    regex = ".*%s.* |%s*-.*|\d{1,3}.+ PTR [esa|sma]{0,9}.+%s.*|%s.[a-zA-Z0-9.]+com. 3600 IN MX 5|esa.%s.[a-zA-Z0-9.]+com. IN TXT \"v=spf1 ip4:[0-9].+\s-all\""\
                    %(allocation_name[0].get('name'), dh, allocation_name[0].get('name'), allocation_name[0].get('name'), allocation_name[0].get('name'))
    pattern = re.compile(regex)
    list_of_dedicated_records = re.findall(pattern, dnsrecord_text)
    dnsobj.closeconnection(connobj)
    return list_of_dedicated_records, allocation_name[0].get('name')

def get_ob_records(id):
    """
    Purpose : get the ob records of the cluster id
    Returns : Returns list of ob records.
    """
    dnsobj = DNSVerificationScript()
    connobj = dnsobj.get_connection()
    query = '''select COUNT(*) from atlas_mxname where name like '%%ob%%' and cluster_id=%s''' %(id)
    obrecords = int(execute_query(connobj, query)[0].values()[0])
    dnsobj.closeconnection(connobj)
    return obrecords

def split_ips(iplist):
    """
    Purpose : separate the ip4 and ip6 ip's from the given list.
    """
    ipv4 = []
    ipv6 = []
    for cidr in iplist:
        if not "::" in cidr:
           ipv4.append(cidr)
        else:
           ipv6.append(cidr)
    return (ipv4,ipv6)

def ip6_convert(ipv_list):
    """
    Purpose : this method add 14 bit to each ip in the list
    """
    converted_ip= []
    for item in ipv_list:
        templist = item.split(":")

        for i in range(0,len(templist)):
            if not templist[i]:
               templist[i] = "00000000000000"
               templist = ''.join(templist)
               templist = '.'.join(templist)
               converted_ip.append(templist)
    return converted_ip

def get_ip_dedicated(id):
    """
    Purpose : Get the All dedicated customers ip
    Arguments :
     id       : Cluster id of the customer
    """
    dbobj = DNSVerificationScript()
    connobj = dbobj.get_connection()
    for row in get_dedicated_allocation_data():
        query_get_dedicated_ip='''SELECT
        atlas_instance.id AS instance_id,
        atlas_instance.instance_type_id,
        atlas_instance.internal_name,
        atlas_instance.external_name,
        atlas_instance.state_id AS instance_state,
        atlas_instance.spf_record,
        atlas_server.rack_id AS rack_id,
        atlas_ipaddress.ip,
        atlas_ipaddress.prefix_length,
        atlas_serverinterface.primary,
        atlas_ipaddress.ipv6,
        atlas_ipaddress.ip_type_id,
        atlas_proxyurl.url
        FROM
        atlas_instance
        INNER JOIN atlas_server ON atlas_instance.server_id=atlas_server.id
        INNER JOIN atlas_serverinterface ON atlas_serverinterface.server_id = atlas_server.id
        INNER JOIN atlas_ipaddress ON atlas_ipaddress.server_interface_id = atlas_serverinterface.id
        INNER JOIN atlas_proxyurl ON atlas_instance.id=atlas_proxyurl.instance_id
        WHERE
        atlas_instance.state_id=2 and atlas_instance.cluster_id={}
        ORDER BY instance_id ASC'''.format(id)
        ip_table_dedicated = execute_query(connobj, query_get_dedicated_ip)
    dbobj.closeconnection(connobj)
    return ip_table_dedicated

def get_pvt_ip_lb(id):
    """
    Purpose   :  Get the all the private IP's list of lb customers
    Arguments :  Cluster id of th customer
    Returns   :    Returns all rows of IP's
    """
#atlas_instance.state_id=2 and
    query_get_dedicated_ip='''SELECT
    atlas_instance.id AS instance_id,
    atlas_instance.instance_type_id,
    atlas_instance.internal_name,
    atlas_instance.external_name,
    atlas_instance.state_id AS instance_state,
    atlas_instance.spf_record,
    atlas_server.rack_id AS rack_id,
    atlas_pvt_ip_pools.ip,
    atlas_pvt_ip_pools.prefix_length,
    atlas_serverinterface.primary,
    atlas_pvt_ip_pools.ipv6,
    atlas_proxyurl.url
    FROM
    atlas_instance
    INNER JOIN atlas_server ON atlas_instance.server_id=atlas_server.id
    INNER JOIN atlas_serverinterface ON atlas_serverinterface.server_id = atlas_server.id
    INNER JOIN atlas_pvt_ip_pools ON atlas_pvt_ip_pools.server_interface_id = atlas_serverinterface.id
    INNER JOIN atlas_proxyurl ON atlas_instance.id=atlas_proxyurl.instance_id
    WHERE
    atlas_instance.state_id=2 and atlas_instance.cluster_id={}
    ORDER BY instance_id ASC'''.format(id)
    dbobj = DNSVerificationScript()
    connobj = dbobj.get_connection()
    pvt_ip_table_lb = execute_query(connobj, query_get_dedicated_ip)
    dbobj.closeconnection(connobj)
    return pvt_ip_table_lb

def get_dedicated_servers():
    """
    Purpose : Get the all dedicated servers
    Arguments : None
    Returns : Returns the list of dedicated customers
    """
    query_get_dedicated_server='''SELECT atlas_server.id,
    atlas_server.name,
    atlas_ipaddress.ip,
    atlas_ipaddress.prefix_length,
    atlas_ipaddress.ipv6
    FROM atlas_server,
    atlas_ipaddress,
    atlas_serverinterface
    WHERE  atlas_server.id = atlas_serverinterface.server_id AND
    atlas_ipaddress.server_interface_id = atlas_serverinterface.id AND atlas_serverinterface.primary = 1'''

    dbobj = DNSVerificationScript()
    connobj = dbobj.get_connection()
    dedicated_server_list = execute_query(connobj, query_get_dedicated_server)
    dbobj.closeconnection(connobj)
    return  dedicated_server_list

def get_lb_servers():
    """
    Purpose   : Get the all the servers of the lb customer.
    Arguments : None
    Returns   : Retunrs row of lb servers
    """
    query_get_lb_server = '''SELECT atlas_server.id,
    atlas_server.name,
    atlas_pvt_ip_pools.ip,
    atlas_pvt_ip_pools.prefix_length,
    atlas_pvt_ip_pools.ipv6 FROM
    atlas_server, atlas_pvt_ip_pools,
    atlas_serverinterface WHERE
    atlas_server.id = atlas_serverinterface.server_id AND
    atlas_pvt_ip_pools.server_interface_id = atlas_serverinterface.id AND
    atlas_serverinterface.primary = 1'''
    dbobj = DNSVerificationScript()
    connobj = dbobj.get_connection()
    dedicated_lb_server_list = execute_query(connobj,query_get_lb_server)
    dbobj.closeconnection(connobj)
    return dedicated_lb_server_list

def get_lb_vip_ips(id):
    """
    Purpose : Get all the VIP Ip's of the given customer cluster ID.
    Arguments: id : customer cluster id
    Return: rows of all the VIP ip's
    """
    query_get_vip_ip='''SELECT
    ip, ip_type_id
    FROM
    atlas_ipaddress
    WHERE
    cluster_id={}
    ORDER BY ip ASC'''.format(id)
    dbobj = DNSVerificationScript()
    connobj = dbobj.get_connection()
    vipip_table = execute_query(connobj, query_get_vip_ip)
    dbobj.closeconnection(connobj)
    return vipip_table

######################### Dedicated internal and External Verification  ####################
def wrapperforvalidation(clsid, statuslist, failedlist, skippedlist):
    perform_validation(clsid, statuslist, failedlist, skippedlist)
    #logging.info("------------------------------------------------")
    #logging.info("Dedicated Cluster Validation")
    #logging.info("Success List :{} \n{}".format(len(statuslist), statuslist))
    #logging.info("Failed List :{} \n{}".format(len(failedlist), failedlist))
    #logging.info("Skipped list :{} \n{}".format(len(skippedlist), skippedlist))
    #logging.info("------------------------------------------------")

def wrapper_for_internal_validation(clsid, statuslist, failedlist, skippedlist):
    perform_internal_validation(clsid, statuslist, failedlist, skippedlist)
    #logging.info("------------------------------------------------")
    #logging.info("Dedicated Cluster Validation")
    #logging.info("Success List :{} \n{}".format(len(statuslist), statuslist))
    #logging.info("Failed List :{} \n{}".format(len(failedlist), failedlist))
    #logging.info("Skipped list :{} \n{}".format(len(skippedlist), skippedlist))
    #logging.info("------------------------------------------------")

def perform_validation(clsid, status_list, failed_clus_list, skipped_clus_list):
    ip_table, o365iptable, dh_table, spf_record, external_name, esa_external_names, \
    reverse_ip_list, reverse_ip6_list, ip6_table_converted, esalist, \
    smalist, ip_list_dedicated , o365iptable, dh_table, spf_record, \
    external_name,esa_external_names, reverse_ip_list, reverse_ip6_list, \
    ip6_table_converted, esalist, smalist, ip_list_dedicated = ([] for _ in range(23))

    #logging.info("CLuster ID to be Processed :{}".format(clsid))
    ip_list_dedicated = get_ip_dedicated(clsid)
    if not ip_list_dedicated:
        skipped_clus_list.append(clsid)
        #continue
        return
    getdhurl = ip_list_dedicated[0].get("url")
    getdhurl = getdhurl.split("-")[0]
    dns_recordsList_dedicated, alloc_name  = get_dns_records(EXTERNAL_FILE,clsid, dh=getdhurl)
    logging.info("[{}][Start Validation]: Processing Cluster : {}".format(alloc_name, alloc_name))
    for i in range(0, len(ip_list_dedicated)):
        if ip_list_dedicated[i].get('primary'):
            if ip_list_dedicated[i].get('instance_type_id') == IPTYPE_VIP:
                esalist.append(ip_list_dedicated[i]['ip'])
                spf_record.append(ip_list_dedicated[i]['spf_record'])
            if ip_list_dedicated[i].get('instance_type_id') == IPTYPEO365VIP:
                smalist.append(ip_list_dedicated[i]['ip'])
            ip_table.append(ip_list_dedicated[i]['ip'])
            dh_table.append(ip_list_dedicated[i]['url'])
            external_name.append(ip_list_dedicated[i]['external_name'])
        else:
            o365iptable.append(ip_list_dedicated[i]['ip'])

    ip_table=list(set(ip_table))
    dh_table=list(set(dh_table))
    spf_record=list(set(spf_record))
    spf_record = [i for i in spf_record if i]
    external_name = list(set(external_name))
    ip4_table,ip6_table = split_ips(ip_table)

    for ip in ip4_table:
        reverse_ip_list.append(".".join(reversed(ip.split('.'))))
    ptr_result = \
    [True if re.findall(item+".in-addr.arpa.*", str(dns_recordsList_dedicated)) else False for item in reverse_ip_list]
    logging.info("{}-1: Performing PTR Record Check: Expected :{} - Validated: {}".format(alloc_name, len(reverse_ip_list), len(ptr_result)))
    if not all(ptr_result):
        failed_clus_list[str(alloc_name)] = "PTR Record Validation Failed"
        logging.info("{}-ERROR Analyis ------------ ".format(alloc_name))
        logging.info("Reverse IP list :{}".format(reverse_ip_list))
        logging.info("PTR Result check :{}".format(ptr_result))
        logging.info("PTR Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    if ip6_table:
        ip6_table_converted = ip6_convert(ip6_table)
        for ip6 in ip6_table_converted:
            reverse_ip6_list.append(".".join(reversed(ip6.split('.'))))
        ptr_result_ip6 = \
        [True if re.findall(item+".ip6.arpa.*   PTR", str(dns_recordsList_dedicated)) else False for item in reverse_ip6_list]
        logging.info("{}-1.1: Performing PTR  Check for IP6: Expected :{} - Validated: {}".format(alloc_name, len(reverse_ip6_list), len(ptr_result_ip6)))
        if not all(ptr_result_ip6):
            failed_clus_list[str(alloc_name)] = "PTR Record Validation Failed for IP6"
            logging.info("ERROR Analyis ------------ ")
            logging.info("Reverse IP6 list :{}".format(reverse_ip_list))
            logging.info("PTR Result check for IP6 :{}".format(ptr_result))
            logging.info("PTR Record Validation Failed for IP6. Continue to Next Cluster")
            #continue
            return

    dh_result = [True if re.search(item+".  IN CNAME",str(dns_recordsList_dedicated)) else False for item in dh_table]
    logging.info("{}-2: Performing DH Records Check : Expected: {} - Validated: {}".format(alloc_name, len(dh_table), len(dh_result)))
    if not all(dh_result):
        failed_clus_list[str(alloc_name)] = "DH Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("DH records check :{}".format(dh_result))
        logging.info("DH Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    noofmx = len(esalist) * 2
    mxrecordvalidate = re.findall("mx[1-2]\.", str(dns_recordsList_dedicated))
    if noofmx == len(mxrecordvalidate):
        logging.info("{}-3: Performing MX Records Check : Expected: {} - Validated :{}".format(alloc_name, noofmx, len(mxrecordvalidate)))
    else:
        failed_clus_list[str(alloc_name)] = "MX Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("MX Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    isobrecordpresent = get_ob_records(clsid)
    if isobrecordpresent:
        obrecordvalidate = re.findall("ob[1-2]\.", str(dns_recordsList_dedicated))
        noofobs = len(o365iptable)
        if noofobs == len(obrecordvalidate):
            logging.info("{}-4: Performing OB Records Check : Expected: {} - Validated :{}".format(alloc_name, noofobs, len(obrecordvalidate)))
        else:
            failed_clus_list[str(alloc_name)] = "OB Record Validation Failed"
            logging.info("ERROR Analyis ------------ ")
            logging.info("OB Record Validation Failed. Continue to Next Cluster")
            #continue
            return

    external_name_result = [True if re.findall(item+".  IN A*", str(dns_recordsList_dedicated)) else False for item in external_name]
    logging.info("{}-5: Performing A Records Check: Expected: {} - Validated: {}".format(alloc_name, len(ip4_table), len(external_name_result)))
    if not all(external_name_result):
        failed_clus_list[str(alloc_name)] = "A Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("A Records  Result check for IP4 :{}".format(external_name_result))
        logging.info("A Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    if ip6_table:
        for item in external_name:
            if 'esa' in item:
                esa_external_names.append(item)
        external_AAAA_result_ip6 = [True if re.findall(item+".  IN AAAA", str(dns_recordsList_dedicated)) else False for item in esa_external_names]
        logging.info("{}-5.1: Performing AAAA  Record Check for IP6: Expected :{} - Validated: {}".format(alloc_name, len(ip6_table), len(external_AAAA_result_ip6)))
        if not all(external_AAAA_result_ip6):
            failed_clus_list[str(alloc_name)] = "AAAA Record Validation Failed"
            logging.info("ERROR Analyis ------------ ")
            logging.info("A Records check for IP6 :{}".format(external_AAAA_result_ip6))
            logging.info("AAAA Record Validation Failed. Continue to Next Cluster")
            #continue
            return

    TXT_result=[True if re.findall(item+". IN TXT", str(dns_recordsList_dedicated)) else False for item in external_name if "esa" in item]
    logging.info("{}-6: Performing TXT Records Check: Expected: {} - Validated: {}".format(alloc_name, len(esalist), TXT_result.count(True)))
    if not all(TXT_result):
        failed_clus_list[str(alloc_name)] = "TXT Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("TXT Records Results check for :{}".format(TXT_result))
        logging.info("TXT Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    spf_result = [True if re.findall(item, str(dns_recordsList_dedicated)) else False for item in spf_record]
    logging.info("{}-7: Performing SPF IN A  Check: Excepted: {} - Validated: {}".format(alloc_name, len(esalist), len(spf_result)))
    if not all(spf_result):
        failed_clus_list[str(alloc_name)] = "SPF IN A Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("SPF IN A Records Check  :{}".format(sfp_result))
        logging.info("SPF Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    if "MX 5" in str(dns_recordsList_dedicated):
        if alloc_name in povclusters:
            logging.info("{}-8: Check Journal Records for Dedicated Customer :{}".format(alloc_name, alloc_name))
            journalvalidate = re.findall("{}.[a-zA-Z0-9.]+com. 3600 IN MX 5".format(alloc_name), str(dns_recordsList_dedicated))
            if len(journalvalidate) == 2:
                logging.info("JOurnal Records Verified")
            else:
                failed_clus_list[str(alloc_name)] = "Journal Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("Missing Journal Records: {}".format(journalvalidate))
                return
        else:
            logging.error("Journaling Mode Not Enabled")

    status_list.append(alloc_name)
    #logging.info("Success list: {}".format(status_list))
    logging.info("[End Validation]: Processed Cluster ID: {}-{}".format(alloc_name, clsid))

def perform_internal_validation(clsid, status_list, failed_clus_list, skipped_clus_list):
    ip_table, o365iptable, dh_table, spf_record, external_name, esa_external_names, \
    reverse_ip_list, reverse_ip6_list, ip6_table_converted, esalist, \
    smalist, ip_list_dedicated , o365iptable, dh_table, spf_record, \
    external_name, internal_names,esa_external_names, reverse_ip_list, reverse_ip6_list, \
    ip6_table_converted, esalist, smalist, ip_list_dedicated = ([] for _ in range(23))

    #logging.info("CLuster ID to be Processed :{}".format(clsid))
    ip_list_dedicated = get_ip_dedicated(clsid)
    if not ip_list_dedicated:
        skipped_clus_list.append(clsid)
        #continue
        return
    getdhurl = ip_list_dedicated[0].get("url")
    getdhurl = getdhurl.split("-")[0]
    dns_recordsList_dedicated, alloc_name  = get_dns_records(INTERNAL_FILE,clsid, dh=getdhurl)
    logging.info("[{}][Start Validation]: Processing Cluster : {}".format(alloc_name, alloc_name))
    for i in range(0, len(ip_list_dedicated)):
        if ip_list_dedicated[i].get('primary'):
            if ip_list_dedicated[i].get('instance_type_id') == IPTYPE_VIP:
                esalist.append(ip_list_dedicated[i]['ip'])
                spf_record.append(ip_list_dedicated[i]['spf_record'])
            if ip_list_dedicated[i].get('instance_type_id') == IPTYPEO365VIP:
                smalist.append(ip_list_dedicated[i]['ip'])
            ip_table.append(ip_list_dedicated[i]['ip'])
            dh_table.append(ip_list_dedicated[i]['url'])
            external_name.append(ip_list_dedicated[i]['external_name'])
            internal_names.append(ip_list_dedicated[i]['internal_name'])
        else:
            o365iptable.append(ip_list_dedicated[i]['ip'])

    ip_table=list(set(ip_table))
    dh_table=list(set(dh_table))
    spf_record=list(set(spf_record))
    spf_record = [i for i in spf_record if i]
    external_name = list(set(external_name))
    ip4_table,ip6_table = split_ips(ip_table)
    internal_names = list(set(internal_names))

    for ip in ip4_table:
        reverse_ip_list.append(".".join(reversed(ip.split('.'))))
    ptr_result = \
    [True if re.findall(item+".in-addr.arpa.*", str(dns_recordsList_dedicated)) else False for item in reverse_ip_list]
    logging.info("{}-1: Performing PTR Record Check: Expected :{} - Validated: {}".format(alloc_name, len(reverse_ip_list), len(ptr_result)))
    if not all(ptr_result):
        failed_clus_list[str(alloc_name)] = "PTR Record Validation Failed"
        logging.info("{}-ERROR Analyis ------------ ".format(alloc_name))
        logging.info("Reverse IP list :{}".format(reverse_ip_list))
        logging.info("PTR Result check :{}".format(ptr_result))
        logging.info("PTR Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    if ip6_table:
        ip6_table_converted = ip6_convert(ip6_table)
        for ip6 in ip6_table_converted:
            reverse_ip6_list.append(".".join(reversed(ip6.split('.'))))
        ptr_result_ip6 = \
        [True if re.findall(item+".ip6.arpa.*   PTR", str(dns_recordsList_dedicated)) else False for item in reverse_ip6_list]
        logging.info("{}-1.1: Performing PTR  Check for IP6: Expected :{} - Validated: {}".format(alloc_name, len(reverse_ip6_list), len(ptr_result_ip6)))
        if not all(ptr_result_ip6):
            failed_clus_list[str(alloc_name)] = "PTR Record Validation Failed for IP6"
            logging.info("ERROR Analyis ------------ ")
            logging.info("Reverse IP6 list :{}".format(reverse_ip_list))
            logging.info("PTR Result check for IP6 :{}".format(ptr_result))
            logging.info("PTR Record Validation Failed for IP6. Continue to Next Cluster")
            #continue
            return

    #dh_result = [True if re.search(item+".  IN CNAME",str(dns_recordsList_dedicated)) else False for item in dh_table]
    dh_result = []
    for i, j in zip(dh_table, internal_names):
        print(i, j)
        pattern = i + "  IN CNAME" + '  ' + j
        dh_result.append([True if re.findall(pattern, str(dns_recordsList_dedicated)) else False])
    logging.info("{}-2: Performing DH Records Check : Expected: {} - Validated: {}".format(alloc_name, len(dh_table), len(dh_result)))
    if not all(dh_result):
        failed_clus_list[str(alloc_name)] = "DH Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("DH records check :{}".format(dh_result))
        logging.info("DH Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    noofmx = len(esalist) * 2
    mxrecordvalidate = re.findall("mx[1-2]\.", str(dns_recordsList_dedicated))
    if noofmx == len(mxrecordvalidate):
        logging.info("{}-3: Performing MX Records Check : Expected: {} - Validated :{}".format(alloc_name, noofmx, len(mxrecordvalidate)))
    else:
        failed_clus_list[str(alloc_name)] = "MX Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("MX Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    isobrecordpresent = get_ob_records(clsid)
    if isobrecordpresent:
        obrecordvalidate = re.findall("ob[1-2]\.", str(dns_recordsList_dedicated))
        noofobs = len(o365iptable)
        if noofobs == len(obrecordvalidate):
            logging.info("{}-4: Performing OB Records Check : Expected: {} - Validated :{}".format(alloc_name, noofobs, len(obrecordvalidate)))
        else:
            failed_clus_list[str(alloc_name)] = "OB Record Validation Failed"
            logging.info("ERROR Analyis ------------ ")
            logging.info("OB Record Validation Failed. Continue to Next Cluster")
            #continue
            return

    external_name_result = [True if re.findall(item+".  IN A*", str(dns_recordsList_dedicated)) else False for item in external_name]
    logging.info("{}-5: Performing A Records Check: Expected: {} - Validated: {}".format(alloc_name, len(ip4_table), len(external_name_result)))
    if not all(external_name_result):
        failed_clus_list[str(alloc_name)] = "A Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("A Records  Result check for IP4 :{}".format(external_name_result))
        logging.info("A Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    if ip6_table:
        for item in external_name:
            if 'esa' in item:
                esa_external_names.append(item)
        external_AAAA_result_ip6 = [True if re.findall(item+".  IN AAAA", str(dns_recordsList_dedicated)) else False for item in esa_external_names]
        logging.info("{}-5.1: Performing AAAA  Record Check for IP6: Expected :{} - Validated: {}".format(alloc_name, len(ip6_table), len(external_AAAA_result_ip6)))
        if not all(external_AAAA_result_ip6):
            failed_clus_list[str(alloc_name)] = "AAAA Record Validation Failed"
            logging.info("ERROR Analyis ------------ ")
            logging.info("A Records check for IP6 :{}".format(external_AAAA_result_ip6))
            logging.info("AAAA Record Validation Failed. Continue to Next Cluster")
            #continue
            return

    TXT_result=[True if re.findall(item+". IN TXT", str(dns_recordsList_dedicated)) else False for item in external_name if "esa" in item]
    logging.info("{}-6: Performing TXT Records Check: Expected: {} - Validated: {}".format(alloc_name, len(esalist), TXT_result.count(True)))
    if not all(TXT_result):
        failed_clus_list[str(alloc_name)] = "TXT Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("TXT Records Results check for :{}".format(TXT_result))
        logging.info("TXT Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    spf_result = [True if re.findall(item, str(dns_recordsList_dedicated)) else False for item in spf_record]
    logging.info("{}-7: Performing SPF IN A  Check: Excepted: {} - Validated: {}".format(alloc_name, len(esalist), len(spf_result)))
    if not all(spf_result):
        failed_clus_list[str(alloc_name)] = "SPF IN A Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("SPF IN A Records Check  :{}".format(sfp_result))
        logging.info("SPF Record Validation Failed. Continue to Next Cluster")
        #continue
        return

    if "MX 5" in str(dns_recordsList_dedicated):
        if alloc_name in povclusters:
            logging.info("{}-8: Check Journal Records for Dedicated Customer :{}".format(alloc_name, alloc_name))
            journalvalidate = re.findall("{}.[a-zA-Z0-9.]+com. 3600 IN MX 5".format(alloc_name), str(dns_recordsList_dedicated))
            if len(journalvalidate) == 2:
                logging.info("JOurnal Records Verified")
            else:
                failed_clus_list[str(alloc_name)] = "Journal Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("Missing Journal Records: {}".format(journalvalidate))
                return
        else:
            logging.error("Journaling Mode Not Enabled")

    status_list.append(alloc_name)
    #logging.info("Success list: {}".format(status_list))
    logging.info("[End Validation]: Processed Cluster ID: {}-{}".format(alloc_name, clsid))

def dedicated_customer_verification():
    """
    Purpose:  validates the all dedicated customer records for each cluster name
    """
    dedicated_id_list, dedprocesses = [], []
    for row in get_dedicated_allocation_data():
        dedicated_id_list.append(int(row['id']))

    n = 60
    splitlist = [dedicated_id_list[i:i + n] for i in range(0, len(dedicated_id_list), n)]
    logging.info("[External View]: No of CLusters to be Validated :{}".format(len(dedicated_id_list)))

    count = 0
    for i in splitlist:
        for clsid in i:
            process = multiprocessing.Process(target=wrapperforvalidation, args=(clsid, statuslist, failedlist, skippedlist))
            dedprocesses.append(process)
            process.start()

        for proc in dedprocesses:
            proc.join()
        count += 1
        logging.info("Set {} Done Processing {} Clusters".format(count, len(i)))
        logging.info("------------------------------------")

    logging.info("Total no of Connections Open & Closed : {} - {}".format(len(dbconnopenlist), len(dbconncloselist)))
    if len(dbconnopenlist) > len(dbconncloselist):
        logging.error("Open SQL Connections getting drained")

    #logging.info("------------------------------------")
    #logging.info("Final List of Clusters : \n")
    #logging.info("Success List :{}".format(len(statuslist)))
    #for i in statuslist:
    #    logging.info(i)
    #logging.info("------------------------------------\n")
    #logging.info("Failed List: {}".format(len(failedlist)))
    #for k, v in failedlist.items():
    #    logging.info(k + ':    Error:' + v)
    #logging.info("------------------------------------\n")
    #logging.info("Skipped List : {}".format(len(skippedlist)))
    #for i in skippedlist:
    #    logging.info(i)
    logging.info("----- End of all processes -----")

def dedicated_customer_internal_verification():
    """
    Purpose:  validates the all dedicated customer records for each cluster name
    """
    dedicated_id_list, dedprocesses = [], []
    for row in get_dedicated_allocation_data():
        dedicated_id_list.append(int(row['id']))

    n = 60
    splitlist = [dedicated_id_list[i:i + n] for i in range(0, len(dedicated_id_list), n)]
    logging.info("[External View]: No of CLusters to be Validated :{}".format(len(dedicated_id_list)))

    count = 0
    for i in splitlist:
        for clsid in i:
            process = multiprocessing.Process(target=wrapper_for_internal_validation, args=(clsid, statuslist, failedlist, skippedlist))
            dedprocesses.append(process)
            process.start()

        for proc in dedprocesses:
            proc.join()
        count += 1
        logging.info("Set {} Done Processing {} Clusters".format(count, len(i)))
        logging.info("------------------------------------")

    logging.info("Total no of Connections Open & Closed : {} - {}".format(len(dbconnopenlist), len(dbconncloselist)))
    if len(dbconnopenlist) > len(dbconncloselist):
        logging.error("Open SQL Connections getting drained")

    #logging.info("------------------------------------")
    #logging.info("Final List of Clusters : \n")
    #logging.info("Success List :{}".format(len(statuslist)))
    #for i in statuslist:
    #    logging.info(i)
    #logging.info("------------------------------------\n")
    #logging.info("Failed List: {}".format(len(failedlist)))
    #for k, v in failedlist.items():
    #    logging.info(k + ':    Error:' + v)
    #logging.info("------------------------------------\n")
    #logging.info("Skipped List : {}".format(len(skippedlist)))
    #for i in skippedlist:
    #    logging.info(i)
    logging.info("----- End of all processes -----")


################################### Lb External and Internal Verification Verification #########################################

def wrapperforlbvalidation(clsid, lbstatuslist, lbfailedlist, lbskippedlist):
    perform_lbvalidation(clsid, lbstatuslist, lbfailedlist, lbskippedlist)
    #logging.info("------------------------------------------------")
    #logging.info("Dedicated Cluster Validation")
    #logging.info("Success List :{} \n{}".format(len(statuslist), statuslist))
    #logging.info("Failed List :{} \n{}".format(len(failedlist), failedlist))
    #logging.info("Skipped list :{} \n{}".format(len(skippedlist), skippedlist))
    #logging.info("------------------------------------------------")

def wrapper_for_lb_Internal_validation(clsid, lbstatuslist, lbfailedlist, lbskippedlist):
    perform_lb_internal_validation(clsid, lbstatuslist, lbfailedlist, lbskippedlist)
    #logging.info("------------------------------------------------")
    #logging.info("Dedicated Cluster Validation")
    #logging.info("Success List :{} \n{}".format(len(statuslist), statuslist))
    #logging.info("Failed List :{} \n{}".format(len(failedlist), failedlist))
    #logging.info("Skipped list :{} \n{}".format(len(skippedlist), skippedlist))
    #logging.info("------------------------------------------------")

def lb_customer_verification():
    lb_cluster_id_list, lbprocesses = [], []

    for row in get_lb_allocation_data():
        lb_cluster_id_list.append(int(row['id']))

    n = 60
    splitlist = [lb_cluster_id_list[i:i + n] for i in range(0, len(lb_cluster_id_list), n)]
    logging.info("[LB External View]: No of CLusters to be Validated :{}".format(len(lb_cluster_id_list)))

    count = 0
    for i in splitlist:
        for clsid in i:
            process = multiprocessing.Process(target=wrapperforlbvalidation, args=(clsid, lbstatuslist, lbfailedlist, lbskippedlist))
            lbprocesses.append(process)
            process.start()

        for proc in lbprocesses:
            proc.join()
        count += 1
        logging.info("Set {} Done Processing {} clusters.".format(count, len(i)))
        logging.info("------------------------------------")

    logging.info("Total no of Connections Open & Closed : {} - {}".format(len(dbconnopenlist), len(dbconncloselist)))
    if len(dbconnopenlist) > len(dbconncloselist):
        logging.error("Open SQL Connections getting drained")

    logging.debug("------------------------------------")
    logging.debug("Final List of Clusters : \n")
    #logging.info("Success List :{}".format(len(statuslist)))
    #for i in statuslist:
    #    logging.info(i)
    #logging.info("------------------------------------\n")
    #logging.info("Failed List: {}".format(len(failedlist)))
    #for k, v in lbfailedlist.items():
    #    logging.info(k + ':    Error:' + v)
    #logging.info("------------------------------------\n")
    #logging.info("Skipped List : {}".format(len(skippedlist)))
    #for i in skippedlist:
    #    logging.info(i)
    logging.info("----- End of all processes -----")

def lb_customer_Internal_verification():
    lb_cluster_id_list, lbprocesses = [], []

    for row in get_lb_allocation_data():
        lb_cluster_id_list.append(int(row['id']))

    n = 60
    splitlist = [lb_cluster_id_list[i:i + n] for i in range(0, len(lb_cluster_id_list), n)]
    logging.info("[LB External View]: No of CLusters to be Validated :{}".format(len(lb_cluster_id_list)))

    count = 0
    for i in splitlist:
        for clsid in i:
            process = multiprocessing.Process(target=wrapper_for_lb_Internal_validation, args=(clsid, lbstatuslist, lbfailedlist, lbskippedlist))
            lbprocesses.append(process)
            process.start()

        for proc in lbprocesses:
            proc.join()
        count += 1
        logging.info("Set {} Done Processing {} clusters.".format(count, len(i)))
        logging.info("------------------------------------")

    logging.info("Total no of Connections Open & Closed : {} - {}".format(len(dbconnopenlist), len(dbconncloselist)))
    if len(dbconnopenlist) > len(dbconncloselist):
        logging.error("Open SQL Connections getting drained")

    logging.debug("------------------------------------")
    logging.debug("Final List of Clusters : \n")
    #logging.info("Success List :{}".format(len(statuslist)))
    #for i in statuslist:
    #    logging.info(i)
    #logging.info("------------------------------------\n")
    #logging.info("Failed List: {}".format(len(failedlist)))
    #for k, v in lbfailedlist.items():
    #    logging.info(k + ':    Error:' + v)
    #logging.info("------------------------------------\n")
    #logging.info("Skipped List : {}".format(len(skippedlist)))
    #for i in skippedlist:
    #    logging.info(i)
    logging.info("----- End of all processes -----")

def perform_lbvalidation(clsid, status_list_lb, failed_clus_list_lb, skippedlist):
    """
    Purpose   : this method validate the all records of lb customer type.
    Arguments : None
    Returns   : returns the dictionary of failed clusters and success of dedicated clusters.
    """
    ip_table_lb, dh_table_lb, spf_record_lb, \
    reverse_ip_list_lb, natips, vipips, \
    ip6_table_converted, reverse_ip6_list = ([] for _ in range(8))
    lb_table_details = get_pvt_ip_lb(clsid)
    vip_table_details = get_lb_vip_ips(clsid)
    noofnats = 0
    noofo365vips = 0
    for i in range(0, len(vip_table_details)):
        ip_table_lb.append(vip_table_details[i]['ip'])
        if vip_table_details[i]['ip_type_id'] == 5:
            noofnats += 1
            natips.append(vip_table_details[i]['ip'])
        if vip_table_details[i]['ip_type_id'] == 4:
            noofo365vips += 1
        if vip_table_details[i]['ip_type_id'] == 3:
            vipips.append(vip_table_details[i]['ip'])
    getdhurl = lb_table_details[0].get("url")
    getdhurl = getdhurl.split("-")[0]
    dns_records_lb, alloc_name = get_dns_records(EXTERNAL_FILE,clsid, dh=getdhurl)
    logging.info("[Start Validation]: Processing Cluster : {}\n".format(alloc_name))
    for i in range(0, len(lb_table_details)):
        dh_table_lb.append(lb_table_details[i]['url'])

    ip_table_lb = list(set(ip_table_lb))
    ip4_table,ip6_table = split_ips(ip_table_lb)
    dh_table_lb = list(set(dh_table_lb))

    for ip in ip_table_lb:
        reverse_ip_list_lb.append(".".join(reversed(ip.split('.'))))
    ptr_result =  [True if re.findall(item+".in-addr.arpa.*", str(dns_records_lb)) else False for item in reverse_ip_list_lb]
    logging.info("2: Performing PTR Record Check: Expected :{} - Validated: {}".format(len(reverse_ip_list_lb), len(ptr_result)))
    if not all(ptr_result):
        failed_clus_list_lb[str(alloc_name)] = "PTR Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("PTR Records Results check for :{}".format(ptr_result))
        logging.info("PTR Record Validation Failed.  Continue to Next Cluster")
        return

    if ip6_table:
        ip6_table_converted = ip6_convert(ip6_table)
        for ip6 in ip6_table_converted:
            reverse_ip6_list.append(".".join(reversed(ip6.split('.'))))
        ptr_result_ip6=\
        [True if re.findall(item+".in-addr.arpa.*", str(dns_records_lb)) else False for item in reverse_ip6_list]
        logging.info("2.1: Performing PTR Record Check IP6: Expected :{} - Validated: {}".format(len(reverse_ip6_list), len(ptr_result_ip6)))
        if not all(ptr_result_ip6):
            failed_clus_list_lb[str(alloc_name)] = "PTR Record Validation Failed"
            logging.info("ERROR Analyis ------------ ")
            logging.info("PTR Records Results check for IP6 :{}".format(ptr_result_ip6))
            logging.info("PTR Record Validation Failed for IP6.  Continue to Next Cluster")
            return


    dh_result_lb = [True if re.search(item+".  IN CNAME",str(dns_records_lb)) else False for item in dh_table_lb]
    logging.info("3: Performing DH Records Check : Expected: {} - Validated: {}".format(len(dh_table_lb), len(dh_result_lb)))
    if not all(dh_result_lb):
        failed_clus_list_lb[str(alloc_name)] = "DH Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("DH Record Validation Failed.  Continue to Next Cluster")
        return

    noofmx = len(vipips) * 2
    mxrecordvalidate = re.findall("mx[1-2]\.", str(dns_records_lb))
    if noofmx == len(mxrecordvalidate):
        logging.info("4: Performing MX Records Check : Expected: {} - Validated :{}".format(noofmx, len(mxrecordvalidate)))
    else:
        failed_clus_list_lb[str(alloc_name)] = "MX Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("No of MX: {}".format(noofmx))
        logging.info("IP TABLE LB: {}".format(ip_table_lb))
        logging.info("MX Record Validation Failed. Continue to Next Cluster")
        return

    isobrecordpresent = get_ob_records(clsid)
    if isobrecordpresent:
        obrecordvalidate = re.findall("ob[1-2]\.", str(dns_records_lb))
        if noofo365vips == len(obrecordvalidate):
            logging.info("5: Performing OB Records Check : Expected: {} - Validated :{}".format(noofo365vips, len(obrecordvalidate)))
        else:
            failed_clus_list_lb[str(alloc_name)] = "OB Record Validation Failed"
            logging.info("ERROR Analyis ------------ ")
            logging.info("OB Record Validation Failed.  Continue to Next Cluster")
            return

    external_name_lb_result = re.findall("esa.{}.[a-zA-Z0-9.]+com.  IN A".format(str(alloc_name)), str(dns_records_lb))
    logging.info("5: Performing A Records Check: Expected: {} - Validated: {}".format(len(ip_table_lb), len(external_name_lb_result)))
    if not all(external_name_lb_result):
        failed_clus_list_lb[str(alloc_name)] = "A Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("A Record Validation Failed.  Continue to Next Cluster")
        return

    if ip6_table:
        external_name_lb_result_ip6 = re.findall("esa.{}.[a-zA-Z0-9.]+com.  IN AAAA".format(str(alloc_name)), str(dns_records_lb))
        logging.info("5.1: Performing AAAA Records Check: Expected: {} - Validated: {}".format(len(ip6_table), len(external_name_lb_result_ip6)))
        if not all(external_name_lb_result):
            failed_clus_list_lb[str(alloc_name)] = "AAAA Record Validation Failed for IP6"
            logging.info("ERROR Analyis ------------ ")
            logging.info("AAAA Record Validation Failed.  Continue to Next Cluster")
            return

    txtregex = "esa.{}.[a-zA-Z0-9.]+com. IN TXT \"v=spf1 ip4:[0-9].+\s-all".format(alloc_name)
    TXT_result_lb = re.findall(txtregex, fetch_dnsfile(EXTERNAL_FILE))
    logging.debug("TO BE FOUND :{} ------ MATCH FOUND :{}".format(txtregex, TXT_result_lb))
    expectedcount = 0
    for i in natips:
        if TXT_result_lb and i in TXT_result_lb[0]:
            expectedcount += 1
    logging.info("5: Performing TXT Records Check: Expected: {} - Validated: {}".format(expectedcount, noofnats))
    if expectedcount != noofnats:
        failed_clus_list_lb[str(alloc_name)] = "TXT Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("TXT Record Validation Failed.  Continue to Next Cluster")
        return

    for i in natips:
        spfregex = "%s.spf.%s.* IN A\s+127.0.0.2" %(i, alloc_name)
        logging.debug("TO BE FOUND : {} --- MATCH FOUND :{}".format(spfregex, re.findall(spfregex, fetch_dnsfile(EXTERNAL_FILE))))
        spf_record_lb.extend(re.findall(spfregex, fetch_dnsfile(EXTERNAL_FILE)))
    logging.debug("6: Performing SPF IN A  Check: Excepted: {} - Validated: {}".format(noofnats, len(spf_record_lb)))
    if noofnats != len(spf_record_lb):
        failed_clus_list_lb[str(alloc_name)] = "SPF IN A Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("SPF Record Validation Failed.  Continue to Next Cluster")
        return

    if "MX 5" in str(dns_records_lb):
        if alloc_name in povclusters:
            logging.info("7: Check Journal Records for LB Customer :{}".format(alloc_name))
            logging.info("{}.[a-zA-Z0-9.]+com. 3600 IN MX 5".format(alloc_name))
            journalvalidate = re.findall("{}.[a-zA-Z0-9.]+com. 3600 IN MX 5 ".format(alloc_name), str(dns_records_lb))
            if len(journalvalidate) == 2:
                logging.info("JOurnal Records Verified")
            else:
                failed_clus_list_lb[str(alloc_name)] = "Journal Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("Missing Journal Records: {}".format(journalvalidate))
                return

    status_list_lb.append(alloc_name)
    logging.debug("\n**********************************************\n")
    logging.info("[End Validation]: Processed Cluster ID: {}\n".format(clsid))

def perform_lb_internal_validation(clsid, status_list_lb, failed_clus_list_lb, skippedlist):
    """
    Purpose   : this method validate the all records of lb customer type.
    Arguments : None
    Returns   : returns the dictionary of failed clusters and success of dedicated clusters.
    """
    ip_table_lb, dh_table_lb, spf_record_lb, \
    reverse_ip_list_lb, natips, vipips, \
    ip6_table_converted, reverse_ip6_list , internal_names = ([] for _ in range(8))
    lb_table_details = get_pvt_ip_lb(clsid)
    vip_table_details = get_lb_vip_ips(clsid)
    noofnats = 0
    noofo365vips = 0
    for i in range(0,len(lb_table_details)):
        internal_names.append(lb_table_details[i]['internal_name'])

    for i in range(0, len(vip_table_details)):
        ip_table_lb.append(vip_table_details[i]['ip'])
        if vip_table_details[i]['ip_type_id'] == 5:
            noofnats += 1
            natips.append(vip_table_details[i]['ip'])
        if vip_table_details[i]['ip_type_id'] == 4:
            noofo365vips += 1
        if vip_table_details[i]['ip_type_id'] == 3:
            vipips.append(vip_table_details[i]['ip'])
    getdhurl = lb_table_details[0].get("url")
    getdhurl = getdhurl.split("-")[0]
    dns_records_lb, alloc_name = get_dns_records(EXTERNAL_FILE,clsid, dh=getdhurl)
    logging.info("[Start Validation]: Processing Cluster : {}\n".format(alloc_name))
    for i in range(0, len(lb_table_details)):
        dh_table_lb.append(lb_table_details[i]['url'])

    ip_table_lb = list(set(ip_table_lb))
    ip4_table,ip6_table = split_ips(ip_table_lb)
    dh_table_lb = list(set(dh_table_lb))
    internal_names = list(set(internal_names))

    for ip in ip_table_lb:
        reverse_ip_list_lb.append(".".join(reversed(ip.split('.'))))
    ptr_result =  [True if re.findall(item+".in-addr.arpa.*", str(dns_records_lb)) else False for item in reverse_ip_list_lb]
    logging.info("2: Performing PTR Record Check: Expected :{} - Validated: {}".format(len(reverse_ip_list_lb), len(ptr_result)))
    if not all(ptr_result):
        failed_clus_list_lb[str(alloc_name)] = "PTR Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("PTR Records Results check for :{}".format(ptr_result))
        logging.info("PTR Record Validation Failed.  Continue to Next Cluster")
        return

    if ip6_table:
        ip6_table_converted = ip6_convert(ip6_table)
        for ip6 in ip6_table_converted:
            reverse_ip6_list.append(".".join(reversed(ip6.split('.'))))
        ptr_result_ip6=\
        [True if re.findall(item+".in-addr.arpa.*", str(dns_records_lb)) else False for item in reverse_ip6_list]
        logging.info("2.1: Performing PTR Record Check IP6: Expected :{} - Validated: {}".format(len(reverse_ip6_list), len(ptr_result_ip6)))
        if not all(ptr_result_ip6):
            failed_clus_list_lb[str(alloc_name)] = "PTR Record Validation Failed"
            logging.info("ERROR Analyis ------------ ")
            logging.info("PTR Records Results check for IP6 :{}".format(ptr_result_ip6))
            logging.info("PTR Record Validation Failed for IP6.  Continue to Next Cluster")
            return

    dh_result_lb = []
    for i ,j in zip(dh_table_lb,internal_names):
         pattern=i+"  IN CNAME"+'  '+j
         dh_result_lb.append([True if re.findall(pattern, str(dns_records_lb)) else False])
    #dh_result_lb = [True if re.search(item+".  IN CNAME",str(dns_records_lb)) else False for item in dh_table_lb]
    logging.info("3: Performing DH Records Check : Expected: {} - Validated: {}".format(len(dh_table_lb), len(dh_result_lb)))
    if not all(dh_result_lb):
        failed_clus_list_lb[str(alloc_name)] = "DH Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("DH Record Validation Failed.  Continue to Next Cluster")
        return

    noofmx = len(vipips) * 2
    mxrecordvalidate = re.findall("mx[1-2]\.", str(dns_records_lb))
    if noofmx == len(mxrecordvalidate):
        logging.info("4: Performing MX Records Check : Expected: {} - Validated :{}".format(noofmx, len(mxrecordvalidate)))
    else:
        failed_clus_list_lb[str(alloc_name)] = "MX Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("No of MX: {}".format(noofmx))
        logging.info("IP TABLE LB: {}".format(ip_table_lb))
        logging.info("MX Record Validation Failed. Continue to Next Cluster")
        return

    isobrecordpresent = get_ob_records(clsid)
    if isobrecordpresent:
        obrecordvalidate = re.findall("ob[1-2]\.", str(dns_records_lb))
        if noofo365vips == len(obrecordvalidate):
            logging.info("5: Performing OB Records Check : Expected: {} - Validated :{}".format(noofo365vips, len(obrecordvalidate)))
        else:
            failed_clus_list_lb[str(alloc_name)] = "OB Record Validation Failed"
            logging.info("ERROR Analyis ------------ ")
            logging.info("OB Record Validation Failed.  Continue to Next Cluster")
            return

    external_name_lb_result = re.findall("esa.{}.[a-zA-Z0-9.]+com.  IN A".format(str(alloc_name)), str(dns_records_lb))
    logging.info("5: Performing A Records Check: Expected: {} - Validated: {}".format(len(ip_table_lb), len(external_name_lb_result)))
    if not all(external_name_lb_result):
        failed_clus_list_lb[str(alloc_name)] = "A Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("A Record Validation Failed.  Continue to Next Cluster")
        return

    if ip6_table:
        external_name_lb_result_ip6 = re.findall("esa.{}.[a-zA-Z0-9.]+com.  IN AAAA".format(str(alloc_name)), str(dns_records_lb))
        logging.info("5.1: Performing AAAA Records Check: Expected: {} - Validated: {}".format(len(ip6_table), len(external_name_lb_result_ip6)))
        if not all(external_name_lb_result):
            failed_clus_list_lb[str(alloc_name)] = "AAAA Record Validation Failed for IP6"
            logging.info("ERROR Analyis ------------ ")
            logging.info("AAAA Record Validation Failed.  Continue to Next Cluster")
            return

    txtregex = "esa.{}.[a-zA-Z0-9.]+com. IN TXT \"v=spf1 ip4:[0-9].+\s-all".format(alloc_name)
    TXT_result_lb = re.findall(txtregex, fetch_dnsfile(EXTERNAL_FILE))
    logging.debug("TO BE FOUND :{} ------ MATCH FOUND :{}".format(txtregex, TXT_result_lb))
    expectedcount = 0
    for i in natips:
        if TXT_result_lb and i in TXT_result_lb[0]:
            expectedcount += 1
    logging.info("5: Performing TXT Records Check: Expected: {} - Validated: {}".format(expectedcount, noofnats))
    if expectedcount != noofnats:
        failed_clus_list_lb[str(alloc_name)] = "TXT Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("TXT Record Validation Failed.  Continue to Next Cluster")
        return

    for i in natips:
        spfregex = "%s.spf.%s.* IN A\s+127.0.0.2" %(i, alloc_name)
        logging.debug("TO BE FOUND : {} --- MATCH FOUND :{}".format(spfregex, re.findall(spfregex, fetch_dnsfile(EXTERNAL_FILE))))
        spf_record_lb.extend(re.findall(spfregex, fetch_dnsfile(EXTERNAL_FILE)))
    logging.debug("6: Performing SPF IN A  Check: Excepted: {} - Validated: {}".format(noofnats, len(spf_record_lb)))
    if noofnats != len(spf_record_lb):
        failed_clus_list_lb[str(alloc_name)] = "SPF IN A Record Validation Failed"
        logging.info("ERROR Analyis ------------ ")
        logging.info("SPF Record Validation Failed.  Continue to Next Cluster")
        return

    if "MX 5" in str(dns_records_lb):
        if alloc_name in povclusters:
            logging.info("7: Check Journal Records for LB Customer :{}".format(alloc_name))
            logging.info("{}.[a-zA-Z0-9.]+com. 3600 IN MX 5".format(alloc_name))
            journalvalidate = re.findall("{}.[a-zA-Z0-9.]+com. 3600 IN MX 5 ".format(alloc_name), str(dns_records_lb))
            if len(journalvalidate) == 2:
                logging.info("JOurnal Records Verified")
            else:
                failed_clus_list_lb[str(alloc_name)] = "Journal Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("Missing Journal Records: {}".format(journalvalidate))
                return

    status_list_lb.append(alloc_name)
    logging.debug("\n**********************************************\n")
    logging.info("[End Validation]: Processed Cluster ID: {}\n".format(clsid))


############################ Internal Servers Verification ######################################

def processlb_customer_internal_verification():
    process = multiprocessing.Process(target=lb_customer_internal_verification, args=(failed_lb_servers,))
    lbintprocesses.append(process)
    process.start()

    '''
    for proc in lbintprocesses:
        proc.join()

    logging.info("Customer Internal View Verifcation Complete")
    return failed_lb_servers
    '''

def lb_customer_internal_verification(failed_lb_servers):
    """
    Purpose : Validates all the internal records of the lb customer.
    Parametrs : None
    Retuns    : None
    """
    lb_ip4_server, lb_ip6_server, duplicate_servers  = [], [], []
    lb_server_ip_map_dict = {}
    lb_servers = get_lb_servers()

    for row in lb_servers:
        if row['name'] in lb_server_ip_map_dict.keys():
            logging.info("Duplicate Server Detected: {}".format(row['name']))
            duplicate_servers.append(row['ip'])
        lb_server_ip_map_dict[row['ip']] = row['name']

    logging.info("LB servers :{}".format(len(lb_servers)))
    logging.info("Duplicates :{}".format(len(duplicate_servers)))
    Total = len(lb_servers) - len(duplicate_servers)
    logging.info("Total Servers excluding Dups :{}".format(Total))
    dns_internal_records = fetch_dnsfile(INTERNAL_FILE)
    for ip, server in lb_server_ip_map_dict.items():
        if not '::' in ip:
           pattern=server+".  IN A"+"      "+str(ip)
           if re.findall(pattern, dns_internal_records):
               lb_ip4_server.append(re.findall(pattern,dns_internal_records))
           else:
               failed_lb_servers.extend([server,ip])
        else:
            patter=server+".  IN AAAA"+"   "+str(ip)
            if re.findall(patter,dns_internal_records):
                lb_ip6_server.append(re.findall(patter,dns_internal_records))
            else:
                failed_lb_servers.extend([server,ip])
    if (len(lb_ip4_server) + len(lb_ip6_server)) != Total:
        logging.info("[Internal View]: No of LB Servers failed :{} and the Servers are :\n{}"\
                .format(len(failed_lb_servers),str(failed_lb_servers)))
    else:
        logging.info("[Internal View]: No of LB Servers check: Expected :{} and validated servers are {}"\
                .format(Total, (len(lb_ip4_server) + len(lb_ip6_server))))

def processded_customer_internal_verification():
    process = multiprocessing.Process(target=dedicate_customer_internal_verification, args=(failed_dedicated_servers,))
    dedintprocesses.append(process)
    process.start()

    '''
    for proc in dedintprocesses:
        proc.join()

    logging.info("Customer Internal View Verifcation Complete")
    return failed_dedicated_servers
    '''

def dedicate_customer_internal_verification(failed_dedicated_servers):
    """
    Purpose   : Validate all the internal records of the dedicated customers.
    """
    dedicated_ip4_servers, dedicated_ip6_servers = [], []
    dns_internal_records = fetch_dnsfile(INTERNAL_FILE)
    dedicated_servers = get_dedicated_servers()
    dedicated_servers_ip_map= {}
    duplicate_servers = []
    for row in dedicated_servers:
        if row['ip'] in dedicated_servers_ip_map.keys():
            logging.info("Server is a Duplicate :{}-{}".format(row['name'], row['ip']))
            duplicate_servers.append(row['ip'])
        #dedicated_servers_ip_map[row['name']] = row['ip']
        dedicated_servers_ip_map[row['ip']] = row['name']

    logging.info("Total servers :{}".format(len(dedicated_servers)))
    logging.info("Duplicates :{}".format(len(duplicate_servers)))
    Total = len(dedicated_servers) - len(duplicate_servers)
    logging.info("Total Servers excluding Dups :{}".format(Total))
    for ip, server in dedicated_servers_ip_map.items():
        if not '::' in ip:
            pattern = server+".  IN A"+"      "+str(ip)
            if re.findall(pattern, dns_internal_records):
                dedicated_ip4_servers.append(re.findall(pattern, dns_internal_records))
            else:
                failed_dedicated_servers.extend([server,ip])
        else:
            pattern = server+".  IN AAAA"+"   "+str(ip)
            if re.findall(pattern, dns_internal_records):
                dedicated_ip6_servers.append(re.findall(pattern, dns_internal_records))
            else:
                failed_dedicated_servers.extend([server,ip])

    if (len(dedicated_ip4_servers) + len(dedicated_ip6_servers)) != Total:
        logging.info("[Internal View]: No of Dedicated Servers failed :{} and servers are {}".format(len(failed_dedicated_servers),str(failed_dedicated_servers)))
    else:
        logging.info("[Internal View]: No of Dedicated Servers check: Expected :{} and validated servers are {}"\
                .format(Total, (len(dedicated_ip4_servers) + len(dedicated_ip6_servers))))

def main():
    global jiralist
    start = time()
    logging.info("DNS Validation - Start :{}".format(start))
    logging.info("****************************************************************")
    logging.info("External & Internal View Validation Start..")
    logging.info("Start of Dedicated Customer External View Validation")
    getpovclusters()
    dedicated_customer_verification()
    logging.info("End of Dedicated Customer External View Validation")
    logging.info("Start of LB Customer External View Validation")
    lb_customer_verification()
    logging.info("End of LB Customer External View Validation")
    jiralist["external_view_ded_failures"] = failedlist
    jiralist["external_view_lb_failures"] = lbfailedlist
    logging.info("Start of Internal View Validation")
    processded_customer_internal_verification()
    processlb_customer_internal_verification()

    prslist = []
    prslist.extend(dedintprocesses)
    prslist.extend(lbintprocesses)
    for proc in prslist:
        proc.join()
    jiralist["internal_view_ded_failures"] = failed_dedicated_servers
    jiralist["internal_view_lb_failures"] = failed_lb_servers
    logging.info("End of Internal View Validation")

    logging.info("Total View Failures :{}".format(len(jiralist.keys())))
    logging.info("DNS Validation Ends ...")
    logging.info("****************************************************************")
    end = time()
    logging.info("DNS Validation End Tmetaken:%2f" %(end-start))
    jiralist["hostname"] = socket.gethostname()
    print(jiralist)
    raise_jira_ticket(json.dumps(jiralist.copy()))

if __name__ == "__main__":
    main()
