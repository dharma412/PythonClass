import MySQLdb
import os
import os.path
import re
import logging
import django
import sys
from MySQLdb import cursors
from ConfigParser import SafeConfigParser
from time import time
from etc import django_settings as  settings

IPTYPE_VIP = 3  # VIP IP Type
IPTYPEO365VIP = 4  # O365VIP IP Type
skipped_clus_list = []
atlas_home    =  os.environ['ATLAS_HOME']

try:
   atlas_home = os.environ['ATLAS_HOME']
   if atlas_home not in sys.path:
       sys.path.append(atlas_home)
   if 'DJANGO_SETTINGS_MODULE' not in os.environ:
       os.environ['DJANGO_SETTINGS_MODULE'] = 'etc.django_settings'
       django.setup()
except KeyError:
    print ("Please set ATLAS_HOME environment variable.")
    sys.exit(1)


EXTERNAL_FILE =  atlas_home+'/bin/external_data.txt'
INTERNAL_FILE =  atlas_home+'/bin/internal_view.txt'
LOG_FILE     = settings.LOG_FILE
LOG_LEVEL    = settings.LOG_LEVEL
LOG_FORMAT   = settings.LOG_FORMAT
MAX_BYTES    = settings.MAX_BYTES
HOST         = settings.DATABASES['default']['HOST']
USER         = settings.DATABASES['default']['USER']
PASSWORD     = settings.DATABASES['default']['PASSWORD']
DB           = settings.DATABASES['default']['NAME']
PORT         = settings.DATABASES['default']['PORT']

logging.basicConfig(filename=LOG_FILE,level=LOG_LEVEL,format=LOG_FORMAT)

def get_connection():
    conn = None
    retry_count = 3
    retries = 0
    while retries < retry_count:
        try:
            conn = MySQLdb.connect(host = HOST,
                                   port = PORT,
                                   user = USER,
                                   passwd = PASSWORD,
                                   db = DB)
            return conn
        except MySQLdb.Error, e:
            msg = 'Error %d: %s' % (e.args[0], e.args[1])
            retries = retries + 1
            print('Retrying again...[%d]' % (retries,))
            continue
    return conn

class DNSVerificationScript:

    def __init__(self):
        self.atlasdb_con = None
        self.atlasdb_cursor = None

    def connectdb(self):
        """
        Purpose : Connects to the Data Base

        Arguments:
             None

        Returns:
            None
        """
        atlasdb_con = get_connection()
        cursor = atlasdb_con.cursor(cursors.DictCursor)
        return cursor

    def close_db(self):
        """
        Purpose : Close the Data Base

        Arguments :
              None

        Returns :
             None
        """
        if self.atlasdb_con:
            self.atlasdb_con.close()

    def execute_query(self,querystring):
        """
         Purpose: executes the select query on the datbase

         Args:
               query       : select query to be executed

         Returns:
               list of rows
        """
        cur=self.connectdb()
        cur.execute(querystring)
        rows=cur.fetchall()
        self.close_db()
        return rows

    def get_dedicated_allocation_data(self):
        """
        Purpose :  exeute the select query and returns rows of cluster_id and names

        """
        row_data_dedicated = self.execute_query("select atlas_cluster.id,atlas_cluster.name from atlas_cluster where atlas_cluster.id NOT IN (select DISTINCT(cluster_id)  from atlas_ipaddress where cluster_id IS NOT NULL)")
        return row_data_dedicated

    def get_lb_allocation_data(self):
        """
        Purpose  : execute the select query and returns rows of cluster_id and clusternames for lb type

        """
        row_data_allocation=self.execute_query("select atlas_cluster.id,atlas_cluster.name from atlas_cluster where atlas_cluster.id IN (select DISTINCT(cluster_id) from atlas_ipaddress where cluster_id IS NOT NULL)")
        return row_data_allocation

    def fetch_externalfile(self):
        """
        Purpose :  Read and Return the external file records

        """
        with open(EXTERNAL_FILE) as fileobject:
             dnstext=fileobject.read()
        return str(dnstext)

    def fetch_internalfile(self):
        """
        Purpose :  Read and Return  Internal File records.
        """
        with open(INTERNAL_FILE) as  fileobject:
             dns_internal_text = fileobject.read()
        return  str(dns_internal_text)

    def get_dns_records(self, id, dh=None):
        """
        Purpose : This method retunrs the DNS records of the cluster id.
        Argumnets :
           id     : cluster id of the customer

           dh     : dh value of the cluster default is None

        Return  :  Returs the DNS records of the given cluster id
        """
        allocation_name_query = "select name from atlas_cluster where id={}".format(id)
        allocation_name = self.execute_query(allocation_name_query)
        dnsrecord_text = self.fetch_externalfile()
        regex = ".*%s.* |%s*-.*|\d{1,3}.+ PTR [esa|sma]{0,9}.+%s.*|esa.%s.[a-zA-Z0-9.]+com. IN TXT \"v=spf1 ip4:[0-9].+\s-all\""\
                        %(allocation_name[0].get('name'), dh, allocation_name[0].get('name'), allocation_name[0].get('name'))
        pattern = re.compile(regex)
        list_of_dedicated_records = re.findall(pattern, dnsrecord_text)
        return list_of_dedicated_records, allocation_name[0].get('name')

    def get_ob_records(self, id):
        """
        Purpose : get the ob records of the cluster id

        Returns : Returns list of ob records.
        """
        query = '''select COUNT(*) from atlas_mxname where name like '%%ob%%' and cluster_id=%s''' %(id)
        return int(self.execute_query(query)[0].values()[0])

    def split_ips(self,iplist):
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

    def ip6_convert(self,ipv_list):
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

    def get_ip_dedicated(self,id):
        """
        Purpose : Get the All dedicated customers ip
        Arguments :
         id       : Cluster id of the customer
        """
        for row in self.get_dedicated_allocation_data():
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
            atlas_instance.cluster_id={}
            ORDER BY instance_id ASC'''.format(id)
            ip_table_dedicated=self.execute_query(query_get_dedicated_ip)
        return ip_table_dedicated

    def get_pvt_ip_lb(self,id):
        """
        Purpose   :  Get the all the private IP's list of lb customers

        Arguments :  Cluster id of th customer

        Returns   :    Returns all rows of IP's

        """
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
        atlas_instance.cluster_id={}
        ORDER BY instance_id ASC'''.format(id)
        pvt_ip_table_lb = self.execute_query(query_get_dedicated_ip)
        return pvt_ip_table_lb

    def get_dedicated_servers(self):
        """
        Purpose : Get the all dedicated servers

        Arguments :
              None
        Returns    : Retunrs the list of dedicated customers

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

        dedicated_server_list = self.execute_query(query_get_dedicated_server)
        return  dedicated_server_list

    def get_lb_servers(self):
        """
        Purpose   : Get the all the servers of the lb customer.
        Arguments :
               None
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
        dedicated_lb_server_list = self.execute_query(query_get_lb_server)
        return dedicated_lb_server_list


    def get_lb_vip_ips(self, id):
        """
        Purpose : Get all the VIP Ip's of the given customer cluster ID.
        Arguments:
                id : customer cluster id
        Return:
             rows of all the VIP ip's
        """
        query_get_vip_ip='''SELECT
        ip, ip_type_id
        FROM
        atlas_ipaddress
        WHERE
        cluster_id={}
        ORDER BY ip ASC'''.format(id)
        vipip_table = self.execute_query(query_get_vip_ip)
        return vipip_table

    def dedicate_customer_internal_verification(self):
        """
        Purpose   : Validate all the internal records of the dedicated customers.
        """
        dedicated_ip4_servers = []
        dedicated_ip6_servers = []
        failed_dedicated_servers = []
        dns_internal_records = self.fetch_internalfile()
        dedicated_servers = self.get_dedicated_servers()
        dedicated_servers_ip_map = {}
        for row in dedicated_servers:
            dedicated_servers_ip_map[row['name']] = row['ip']

        for server,ip in dedicated_servers_ip_map.items():
            if not '::' in ip:
                patter=server+".  IN A"+"      "+str(ip)
                if re.findall(patter,dns_internal_records):
                    dedicated_ip4_servers.append(re.findall(patter,dns_internal_records))
                else:
                    failed_dedicated_servers.extend([server,ip])
            else:
                 patter=server+".  IN AAAA"+"   "+str(ip)
                 if re.findall(patter,dns_internal_records):
                    dedicated_ip6_servers.append(re.findall(patter,dns_internal_records))
                 else:
                     failed_dedicated_servers.extend([server,ip])
        if len(dedicated_ip4_servers)+len(dedicated_ip6_servers) != len(dedicated_servers):
           logging.info("[Internal View]: No of Dedicated Servers failed :{} and servers are {}".format(len(failed_dedicated_servers),str(failed_dedicated_servers)))

    def dedicated_customer_verification(self):
        """
        Purpose:  validates the all dedicated customer records for each cluster name
        """
        dedicated_id_list = []
        ip_list_dedicated = []
        cname_list_dedicated = []
        status_list = []
        failed_clus_list = {}
        for row in self.get_dedicated_allocation_data():
            dedicated_id_list.append(int(row['id']))

        logging.info("[External View]: No of CLusters to be Validated :{}".format(len(dedicated_id_list)))

        for clsid in dedicated_id_list:
            ip_table = []
            o365iptable = []
            dh_table = []
            spf_record = []
            external_name = []
            esa_external_names = []
            reverse_ip_list = []
            reverse_ip6_list = []
            ip6_table_converted = []
            logging.info("CLuster ID to be Processed :{}".format(clsid))
            ip_list_dedicated = self.get_ip_dedicated(clsid)
            if not ip_list_dedicated:
                skipped_clus_list.append(clsid)
                continue
            getdhurl = ip_list_dedicated[0].get("url")
            getdhurl = getdhurl.split("-")[0]
            dns_recordsList_dedicated, alloc_name  = self.get_dns_records(clsid, dh=getdhurl)
            logging.info("[Start Validation]: Processing Cluster : {}\n".format(alloc_name))
            esalist = []
            smalist = []
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
            ip4_table,ip6_table = self.split_ips(ip_table)

            for ip in ip4_table:
                reverse_ip_list.append(".".join(reversed(ip.split('.'))))
            ptr_result = \
            [True if re.findall(item+".in-addr.arpa.*", str(dns_recordsList_dedicated)) else False for item in reverse_ip_list]
            logging.info("1: Performing PTR Record Check: Expected :{} - Validated: {}".format(len(reverse_ip_list), len(ptr_result)))
            if not all(ptr_result):
                failed_clus_list[str(clsid)+'-'+str(alloc_name)] = "PTR Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("Reverse IP list :{}".format(reverse_ip_list))
                logging.info("PTR Result check :{}".format(ptr_result))
                logging.info("PTR Record Validation Failed. Continue to Next Cluster")
                continue

            if ip6_table:
                ip6_table_converted = self.ip6_convert(ip6_table)
                for ip6 in ip6_table_converted:
                    reverse_ip6_list.append(".".join(reversed(ip6.split('.'))))
                ptr_result_ip6 = \
                [True if re.findall(item+".ip6.arpa.*   PTR", str(dns_recordsList_dedicated)) else False for item in reverse_ip6_list]
                logging.info("1.1: Performing PTR  Check for IP6: Expected :{} - Validated: {}".format(len(reverse_ip6_list), len(ptr_result_ip6)))
                if not all(ptr_result_ip6):
                    failed_clus_list[str(clsid)+'-'+str(alloc_name)] = "PTR Record Validation Failed for IP6"
                    logging.info("ERROR Analyis ------------ ")
                    logging.info("Reverse IP6 list :{}".format(reverse_ip_list))
                    loggin.info("PTR Result check for IP6 :{}".format(ptr_result))
                    logging.info("PTR Record Validation Failed for IP6. Continue to Next Cluster")
                    continue

            dh_result = [True if re.search(item+".  IN CNAME",str(dns_recordsList_dedicated)) else False for item in dh_table]
            logging.info("2: Performing DH Records Check : Expected: {} - Validated: {}".format(len(dh_table), len(dh_result)))
            if not all(dh_result):
                failed_clus_list[str(clsid)+'-'+str(alloc_name)] = "DH Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                loggin.info("DH records check :{}".format(dh_result))
                logging.info("DH Record Validation Failed. Continue to Next Cluster")
                continue

            noofmx = len(esalist) * 2
            mxrecordvalidate = re.findall("mx[1-2]\.", str(dns_recordsList_dedicated))
            if noofmx == len(mxrecordvalidate):
                logging.info("3: Performing MX Records Check : Expected: {} - Validated :{}".format(noofmx, len(mxrecordvalidate)))
            else:
                failed_clus_list[str(clsid)+'-'+str(alloc_name)] = "MX Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("MX Record Validation Failed. Continue to Next Cluster")
                continue

            isobrecordpresent = self.get_ob_records(clsid)
            if isobrecordpresent:
                obrecordvalidate = re.findall("ob[1-2]\.", str(dns_recordsList_dedicated))
                noofobs = len(o365iptable)
                if noofobs == len(obrecordvalidate):
                    logging.info("4: Performing OB Records Check : Expected: {} - Validated :{}".format(noofobs, len(obrecordvalidate)))
                else:
                    failed_clus_list[str(clsid)+'-'+str(alloc_name)] = "OB Record Validation Failed"
                    logging.info("ERROR Analyis ------------ ")
                    logging.info("OB Record Validation Failed. Continue to Next Cluster")
                    continue

            external_name_result = [True if re.findall(item+".  IN A*", str(dns_recordsList_dedicated)) else False for item in external_name]
            logging.info("5: Performing A Records Check: Expected: {} - Validated: {}".format(len(ip4_table), len(external_name_result)))
            if not all(external_name_result):
                failed_clus_list[str(clsid)+'-'+str(alloc_name)] = "A Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                loggin.info("A Records  Result check for IP4 :{}".format(external_name_result))
                logging.info("A Record Validation Failed. Continue to Next Cluster")
                continue

            if ip6_table:
                for item in external_name:
                    if 'esa' in item:
                        esa_external_names.append(item)
                external_AAAA_result_ip6 = [True if re.findall(item+".  IN AAAA", str(dns_recordsList_dedicated)) else False for item in esa_external_names]
                logging.info("5.1: Performing AAAA  Record Check for IP6: Expected :{} - Validated: {}".format(len(ip6_table), len(external_AAAA_result_ip6)))
                if not all(external_AAAA_result_ip6):
                    failed_clus_list[str(clsid)+'-'+str(alloc_name)] = "AAAA Record Validation Failed"
                    logging.info("ERROR Analyis ------------ ")
                    logging.info("A Records check for IP6 :{}".format(external_AAAA_result_ip6))
                    logging.info("AAAA Record Validation Failed. Continue to Next Cluster")
                    continue


            TXT_result=[True if re.findall(item+". IN TXT", str(dns_recordsList_dedicated)) else False for item in external_name if "esa" in item]
            logging.info("6: Performing TXT Records Check: Expected: {} - Validated: {}".format(len(esalist), TXT_result.count(True)))
            if not all(TXT_result):
                failed_clus_list[str(clsid)+'-'+str(alloc_name)] = "TXT Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                loggin.info("TXT Records Results check for :{}".format(TXT_result))
                logging.info("TXT Record Validation Failed. Continue to Next Cluster")
                continue


            spf_result = [True if re.findall(item, str(dns_recordsList_dedicated)) else False for item in spf_record]
            logging.info("7: Performing SPF IN A  Check: Excepted: {} - Validated: {}".format(len(esalist), len(spf_result)))
            if not all(spf_result):
                failed_clus_list[str(clsid)+'-'+str(alloc_name)] = "SPF IN A Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                loggin.info("SPF IN A Records Check  :{}".format(sfp_result))
                logging.info("SPF Record Validation Failed. Continue to Next Cluster")
                continue

            status_list.append(alloc_name)
            logging.info("[End Validation]: Processed Cluster ID: {}\n".format(clsid))
        return  (status_list, failed_clus_list)

    def lb_customer_internal_verification(self):

        """
        Purpose : Validates all the internal records of the lb customer.

        Parametrs : None

        Retuns    : None

        """
        lb_server_ip_map_dic={}
        dns_internal_records = self.fetch_internalfile()
        lb_ip4_server = []
        failed_lb_servers = []
        lb_ip6_server = []
        lb_servers = self.get_lb_servers()

        for row in lb_servers:
            lb_server_ip_map_dic[row['name']] = row['ip']
        for server,ip in lb_server_ip_map_dic.items():
            if not '::' in ip:
               pattern=server+".  IN A"+"      "+str(ip)
               if re.findall(pattern,dns_internal_records):
                  lb_ip4_server.append(re.findall(pattern,dns_internal_records))
               else:
                   failed_lb_servers.extend([server,ip])
            else:
                patter=server+".  IN AAAA"+"   "+str(ip)
                if re.findall(patter,dns_internal_records):
                    lb_ip6_server.append(re.findall(patter,dns_internal_records))
                else:
                    failed_lb_servers.extend([server,ip])
        if len(lb_ip4_server)+len(lb_ip6_server) != len(lb_servers):
            logging.info("[Internal View]: No of LB Servers failed :{} and servers are {}".format(len(failed_lb_servers),str(failed_lb_servers)))
        else:
            logging.info("[Internal View]: No of LB Servers check: Expected  :{} and validated servers are {}".format(len(lb_servers),len(lb_ip4_server)+len(lb_ip6_server)))


    def lb_customer_verification(self):
        """
        Purpose   : this method validate the all records of lb customer type.

        Arguments : None

        Returns   : returns the dictionary of failed clusters and success of dedicated clusters.
        """
        lb_cluster_id_list = []
        failed_clus_list_lb = {}
        status_list_lb = []
        for row in self.get_lb_allocation_data():
            lb_cluster_id_list.append(int(row['id']))

        logging.info("[External View]: No of CLusters to be Validated :{}".format(len(lb_cluster_id_list)))

        for clsid in lb_cluster_id_list:
            ip_table_lb = []
            dh_table_lb = []
            spf_record_lb = []
            reverse_ip_list_lb = []
            lb_table_details = self.get_pvt_ip_lb(clsid)
            vip_table_details = self.get_lb_vip_ips(clsid)
            noofnats = 0
            natips = []
            noofo365vips = 0
            vipips = []
            ip6_table_converted = []
            reverse_ip6_list = []
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
            dns_records_lb, alloc_name = self.get_dns_records(clsid, dh=getdhurl)
            logging.info("[Start Validation]: Processing Cluster : {}\n".format(alloc_name))
            for i in range(0, len(lb_table_details)):
                dh_table_lb.append(lb_table_details[i]['url'])

            ip_table_lb = list(set(ip_table_lb))
            ip4_table,ip6_table = self.split_ips(ip_table_lb)
            dh_table_lb = list(set(dh_table_lb))

            for ip in ip_table_lb:
                reverse_ip_list_lb.append(".".join(reversed(ip.split('.'))))
            ptr_result =  [True if re.findall(item+".in-addr.arpa.*", str(dns_records_lb)) else False for item in reverse_ip_list_lb]
            logging.info("2: Performing PTR Record Check: Expected :{} - Validated: {}".format(len(reverse_ip_list_lb), len(ptr_result)))
            if not all(ptr_result):
                failed_clus_list_lb[str(clsid)+str(alloc_name)] = "PTR Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                loggin.info("PTR Records Results check for :{}".format(ptr_result))
                logging.info("PTR Record Validation Failed.  Continue to Next Cluster")
                continue

            if ip6_table:
                ip6_table_converted = self.ip6_convert(ip6_table)
                for ip6 in ip6_table_converted:
                    reverse_ip6_list.append(".".join(reversed(ip6.split('.'))))
                ptr_result_ip6=\
                [True if re.findall(item+".in-addr.arpa.*", str(dns_records_lb)) else False for item in reverse_ip6_list]
                logging.info("2.1: Performing PTR Record Check IP6: Expected :{} - Validated: {}".format(len(reverse_ip6_list), len(ptr_result_ip6)))
                if not all(ptr_result_ip6):
                    failed_clus_list_lb[str(clsid)+str(alloc_name)] = "PTR Record Validation Failed"
                    logging.info("ERROR Analyis ------------ ")
                    loggin.info("PTR Records Results check for IP6 :{}".format(ptr_result_ip6))
                    logging.info("PTR Record Validation Failed for IP6.  Continue to Next Cluster")
                    continue


            dh_result_lb = [True if re.search(item+".  IN CNAME",str(dns_records_lb)) else False for item in dh_table_lb]
            logging.info("3: Performing DH Records Check : Expected: {} - Validated: {}".format(len(dh_table_lb), len(dh_result_lb)))
            if not all(dh_result_lb):
                failed_clus_list_lb[str(clsid)+str(alloc_name)] = "DH Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("DH Record Validation Failed.  Continue to Next Cluster")
                continue

            noofmx = len(vipips) * 2
            mxrecordvalidate = re.findall("mx[1-2]\.", str(dns_records_lb))
            if noofmx == len(mxrecordvalidate):
                logging.info("4: Performing MX Records Check : Expected: {} - Validated :{}".format(noofmx, len(mxrecordvalidate)))
            else:
                failed_clus_list_lb[str(clsid)+str(alloc_name)] = "MX Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("No of MX: {}".format(noofmx))
                logging.info("IP TABLE LB: {}".format(ip_table_lb))
                logging.info("MX Record Validation Failed.  Continue to Next Cluster")
                continue

            isobrecordpresent = self.get_ob_records(clsid)
            if isobrecordpresent:
                obrecordvalidate = re.findall("ob[1-2]\.", str(dns_records_lb))
                if noofo365vips == len(obrecordvalidate):
                    logging.info("5: Performing OB Records Check : Expected: {} - Validated :{}".format(noofo365vips, len(obrecordvalidate)))
                else:
                    failed_clus_list_lb[str(clsid)+str(alloc_name)] = "OB Record Validation Failed"
                    logging.info("ERROR Analyis ------------ ")
                    logging.info("OB Record Validation Failed.  Continue to Next Cluster")
                    continue

            external_name_lb_result = re.findall("esa.{}.[a-zA-Z0-9.]+com.  IN A".format(str(alloc_name)), str(dns_records_lb))
            logging.info("5: Performing A Records Check: Expected: {} - Validated: {}".format(len(ip_table_lb), len(external_name_lb_result)))
            if not all(external_name_lb_result):
                failed_clus_list_lb[str(clsid)+str(alloc_name)] = "A Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("A Record Validation Failed.  Continue to Next Cluster")
                continue

            if ip6_table:
                external_name_lb_result_ip6 = re.findall("esa.{}.[a-zA-Z0-9.]+com.  IN AAAA".format(str(alloc_name)), str(dns_records_lb))
                logging.info("5.1: Performing AAAA Records Check: Expected: {} - Validated: {}".format(len(ip6_table), len(external_name_lb_result_ip6)))
                if not all(external_name_lb_result):
                   failed_clus_list_lb[str(clsid)+str(alloc_name)] = "AAAA Record Validation Failed for IP6"
                   logging.info("ERROR Analyis ------------ ")
                   loggin.info("AAAA Record Validation Failed.  Continue to Next Cluster")
                   continue

            txtregex = "esa.{}.[a-zA-Z0-9.]+com. IN TXT \"v=spf1 ip4:[0-9].+\s-all".format(alloc_name)
            TXT_result_lb = re.findall(txtregex, self.fetch_externalfile())
            logging.debug("TO BE FOUND :{} ------ MATCH FOUND :{}".format(txtregex, TXT_result_lb))
            expectedcount = 0
            for i in natips:
                if TXT_result_lb and i in TXT_result_lb[0]:
                    expectedcount += 1
            logging.info("5: Performing TXT Records Check: Expected: {} - Validated: {}".format(expectedcount, noofnats))
            if expectedcount != noofnats:
                failed_clus_list_lb[str(clsid)+str(alloc_name)] = "TXT Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("TXT Record Validation Failed.  Continue to Next Cluster")
                continue

            for i in natips:
                spfregex = "%s.spf.%s.* IN A\s+127.0.0.2" %(i, alloc_name)
                logging.debug("TO BE FOUND : {} --- MATCH FOUND :{}".format(spfregex, re.findall(spfregex, self.fetch_externalfile())))
                spf_record_lb.extend(re.findall(spfregex, self.fetch_externalfile()))
            logging.debug("6: Performing SPF IN A  Check: Excepted: {} - Validated: {}".format(noofnats, len(spf_record_lb)))
            if noofnats != len(spf_record_lb):
                failed_clus_list_lb[str(clsid)+str(alloc_name)] = "SPF IN A Record Validation Failed"
                logging.info("ERROR Analyis ------------ ")
                logging.info("SPF Record Validation Failed.  Continue to Next Cluster")
                continue

            status_list_lb.append(alloc_name)
            logging.debug("\n**********************************************\n")
            logging.info("[End Validation]: Processed Cluster ID: {}\n".format(clsid))
        return (status_list_lb, failed_clus_list_lb)

if __name__ == "__main__":
    start = time()
    logging.info("DNS Validation - Start :{}".format(start))
    object1 = DNSVerificationScript()
    logging.info("Dedicated Customers Validation starts ...")
    logging.info("------------------------")
    successlist_ded, failedlist_ded = object1.dedicated_customer_verification()
    logging.info("LB Customers Validation starts...")
    logging.info("------------------------")
    successlist_lb, failedlist_lb = object1.lb_customer_verification()
    logging.info("\n\n----------------------------------------------------------------\n")
    logging.info("Success List Dedicated and LB : ---- {}\n\n".format(len(successlist_ded) + len(successlist_lb)))
    logging.info("All Success Cluster Names...\n\n")
    for i in successlist_ded:
        logging.info(i)
    for i in successlist_lb:
        logging.info(i)
    if failedlist_ded or failedlist_lb:
        logging.info("Failed List: ---- \n\n")
        logging.info("Dedicated Customer Failed List:")
        for i,j in failedlist_ded.items():
            logging.info("ID and allocation Name {} and Failure : {}".format(i,j))

        logging.info("LB Customer Failed List:")
        for i,j in failedlist_lb.items():
            logging.info("ID and allocation Name {} and Failure : {}".format(i,j))
    else:
        logging.info("0 Failures. All Cluster Records Validated")
    logging.info("\n\n")
    if skipped_clus_list:
        logging.info("Clusters Skipped : {}".format(skipped_clus_list))
    logging.info("\n\n----------------------------------------------------------------\n")
    logging.info("DNS Validation Complete for {} Clusters.".format(len(successlist_ded) + len(successlist_lb,)))
    logging.info("****************************************************************")
    logging.info("*********************Internal View Validation begins*********************************")
    logging.info("********************** Dedicated Customer ****************")
    object1.dedicate_customer_internal_verification()
    logging.info("*********Lb customer lb validation***************")
    object1.lb_customer_internal_verification()
    end = time()
    logging.info("DNS Validation End Tmetaken:%2f" %(end-start))
