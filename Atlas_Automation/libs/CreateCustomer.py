import pexpect
import polling
import re
from datetime import date
from datetime import datetime
from datetime import timedelta
from collections import namedtuple
from robot.api import logger
from AtlasDbUtils import AtlasDbUtils
from Logger import exec_log
from CliUtils import CliUtils,DEFAULT_PROMPTS
from AtlasTestConstants import ATLAS_SERVER,ATLAS_UI,ATLAS_CONSTANTS,\
                                      ATLAS_CUSTOMER_DATA,ATLAS_EXPORT_CUSTOMER_DATA
from AtlasException import *

@exec_log
def execute_atlas_command(command,prompt=DEFAULT_PROMPTS['ROOT_PROMPT'],timeout=20):
    """
    Purpose: Executes the input command on atlas server

    Args:
        command       : command to be executed
        prompt        : Expected prompt after command execution
        timeout       : [Optional] time to wait for command execution

    Returns:
        Returns the output of the command

    """
    
    atlascli = CliUtils()
    atlascli.ssh_login(ATLAS_CONSTANTS['atlas_host_ip'],ATLAS_SERVER.user,ATLAS_SERVER.password,"atlas-cli")
    atlascli.execute_command('sudo bash')
    output = atlascli.execute_command(command,prompt=prompt,wait_time=timeout)
    atlascli.close_session()
    return output

@exec_log
def update_atlas_configuration(key,value,filename):
    """
    Purpose: Updates the specified configuration file based on the input

    Args:
        key       : configuration name
        value     : Configuration value
        filename  : Name of the file where configuration that needs to be updated

    Returns:
        None

    """

    logger.debug("Modifying {} with {} in file {}".format(key,value,filename))
    execute_atlas_command( '''sed -i 's/{0}.*=.*/{0}={1}/' {2} '''.format(key,value,filename))

@exec_log
def update_fetch_new_customer_timestamp(value,filename):
    """
    Purpose: Updates the fetch customer configuration file based on the input

    Args:
        value     : Configuration value
        filename  : Name of the file where configuration that needs to be updated

    Returns:
        None

    """

    update_atlas_configuration('FETCH_NEW_MINS_INTERVAL',value.strip(),filename)
    execute_atlas_command( '''sed -i 's/{0}\s*=.*/{0} = {1}/' {2} '''.format(key,value,filename))

@exec_log
def change_rma_timestamp(days_before=10):
    """
    Purpose: Changes the timestamp based on the specified date in the atlas_serverdeletestate table

    Args:
        days_before (int): The days from current date for generating epoch time 

    Returns:
         None

    """
    days_before = int(days_before)
    command ='date --date="{} days ago" +%s'.format(days_before)
    time_stamp = execute_atlas_command(command).split('\n')[1]
    db = AtlasDbUtils()
    db.execute_db_update_query(''' update atlas_serverdeletestate set rma_timestamp={} '''.format(time_stamp))   

@exec_log
def get_servers_in_rma():
    """
    Purpose: Gets the list of servers in RMA state

    Args:
      None

    Returns:
        list: This returns the list of servers in RMA state

    """

    db = AtlasDbUtils()
    servers = db.execute_db_select_query('''select name from atlas_server where state_id=(select id from atlas_state where name='RMA')''')
    servers = { server[0] for server in servers }
    logger.info("Available servers - {} ".format(servers))
    return servers

@exec_log
def delete_servers_in_rma():
    ret = execute_atlas_command('clean_rma_servers  && echo $?').split('\n')[1]
    if ret == 0:
        logger.info("There were servers in RMA")
    else:
        logger.info("There were no servers in RMA")


@exec_log
def run_inventory_cleaner(datacenter):
    update_atlas_configuration('datacenter',datacenter,ATLAS_CONSTANTS['vm_inventory'])
    execute_atlas_command("export ATLAS_HOME={} && python {}".format(ATLAS_CONSTANTS['atlas_home'],ATLAS_CONSTANTS['inventory_cleaner']),DEFAULT_PROMPTS['ROOT_PROMPT'],1200)
    update_atlas_configuration('vm_models',ATLAS_CONSTANTS['C100V'],ATLAS_CONSTANTS['vm_inventory'])
    
@exec_log
def get_unassigned_server_datacenter(model,datacenter):
    """
    Purpose: Fetches and returns the list of unassigned servers in the specific data center 

    Args:
        model (str)   : ESA or SMA model - Eg:  C100V, M100V
        datacenter (str)  : Datacenter name 

    Returns:
        list: list of unassigned servers in the atlas database

    """

    db = AtlasDbUtils()
    servers = db.execute_db_select_query(''' select name from atlas_server where state_id=3 \
                                             and rack_id = (select site_id from atlas_datacenter where location= '{}') \
                                             and device_model_id=(select id from atlas_devicemodel where name ='{}') '''.format(datacenter,model))
    logger.debug("Unassigned servers -{} in the datacenter - {} ".format(servers,datacenter)) 
    return  [  server[0] for server in servers]

@exec_log
def get_unassigned_server_count_in_dc(model,datacenter):
    """
    Purpose: Returns  unassigned server count for specified datacenter

    Args:
        model (str)   : ESA or SMA model - Eg:  C100V, M100V
        datacenter (str)  : Datacenter name

    Returns:
        int: number of servers in unassigned state in the specified datacenter

    """

    return len(get_unassigned_server_datacenter(model,datacenter))

@exec_log
def get_servers_name_for_allocation(allocation_name):
    """
    Purpose: Returns  external server name for specified allocation name

    Args:
        datacenter (str)  : allocation name

    Returns:
        list of str: list of external server names for an allocation

    """
    db = AtlasDbUtils()
    sql_stmt = 'select external_name from atlas_instance where cluster_id in(select id from atlas_cluster where name=\'{}\')'.format(allocation_name)
    result = db.execute_db_select_query('''{0}'''.format(sql_stmt))   
    external_servers_names = [server[0] for server in result]
    return external_servers_names

@exec_log
def get_internal_server_name_for_allocation(allocation_name):
    """
    Purpose: Returns  internal server name for specified allocation name

    Args:
        datacenter (str)  : allocation name

    Returns:
        list of str: list of internal server names for an allocation

    """
    db = AtlasDbUtils()
    sql_stmt = 'select internal_name from atlas_instance where cluster_id in(select id from atlas_cluster where name=\'{}\')'.format(allocation_name)
    result = db.execute_db_select_query('''{0}'''.format(sql_stmt))
    internal_servers_names = [server[0] for server in result]
    return internal_servers_names
   
@exec_log
def run_license_pusher():
    """
    Purpose: Executes license pusher command

    Args:
        None

    Returns:
       None

    """

    execute_atlas_command('export ATLAS_HOME={} && python {}'.format(ATLAS_CONSTANTS['atlas_home'],ATLAS_CONSTANTS['license_pusher']))

@exec_log
def get_min_from_now(min=2):
    """
    Purpose: Returns the minutes ahead of current time from atlas server
 
    Args:
        min (int): number of minutes from current time

    Returns:
        int: returns the time 

    """

    date_command = ''' date -d "+ {} minutes"'''.format(min) +'''| awk '{print $4}' | cut -f 2 -d ":" '''
    future_minutes = execute_atlas_command(date_command).strip().split("\n")[1]
    return future_minutes

@exec_log
def get_notification():
    """
    Purpose: Returns the notification information from atlas_notificationemail table of atlas db

    Args:
        None

    Returns:
        list of tuple: Returns the list of entries from atlas_notificationemail table

    """

    db = AtlasDbUtils()
    notification_stmt = 'select id,created_date,mail_from,mail_to,subject,text from atlas_notificationemail'
    rows = db.execute_db_select_query('''{0}'''.format(notification_stmt))
    return rows

@exec_log
def get_all_inventory_cleaner_notifications():
    """
    Purpose: Returns all inventory cleaner notification information from atlas_notificationemail table of atlas db

    Args:
        None

    Returns:
        list: Returns the list of entries specific to inventory cleaner from atlas_notificationemail table

    """
    return [s for s in get_notification()  if 'Inventory Cleaner Status' in s[4] ]

@exec_log
def get_last_inventory_cleaner_alert():
    """
    Purpose: Returns all inventory cleaner notification information from atlas_notificationemail table of atlas db

    Args:
        None

    Returns:
        list: Returns last inventory cleaner details from atlas_notificationemail table

    """
    last_alert = get_all_inventory_cleaner_notifications()[-1]
    subject = last_alert[5].replace('\n','')
    l =[servers_info.strip() for servers_info in re.findall(r'Remaining days:.*?day/s[-]+(.*?)Remaining days:.*?day/s[-]+(.*?)Remaining days:.*?day/s[-]+(.*?)Please',subject)[0]]
    alerts = namedtuple('cleaner_alert',['p1_alert','p2_alert','p3_alert'])
    cleaner_alerts = alerts(*l)
    return cleaner_alerts

@exec_log
def is_customer_present(cust_name):
    """
    Purpose: Checks if the customer is present in the atlas 

    Args:
        cust_name (str): name of customer to be searched

    Returns:
        bool: The returns True if customer is present,otherwise False.

    """

    db = AtlasDbUtils()
    rows = db.execute_db_select_query('''select * from atlas_customer where name='{}' '''.format(cust_name))
    if rows:
        logger.info('Customer {} is present'.format(cust_name))
        return True
    else:
        logger.info('Customer {} is NOT present'.format(cust_name))
        return False

@exec_log
def fetch_all_customer_atlas():
    """
    Purpose: Returns all the customer names in atlas

    Args:
     None

    Returns:
        list of str: Returns list of customer names in atlas

    """
    db = AtlasDbUtils()
    customer_names = db.execute_db_select_query('select name from atlas_customer ')
    return [ customer_name[0] for customer_name in customer_names ]


@exec_log
def reset_atlas_fetch_customer_new_cron():
    """
    Purpose: Removes Lock on fetchcustomers_new for  cron table

    Args:
       None

    Returns:
       None

    """

    db = AtlasDbUtils()
    db.execute_db_update_query(''' update crons set mon_lock=NULL, result=0,frequency=60 where command= 'fetchcustomers_new' ''')

@exec_log
def fetch_all_customerids():
    """
    Purpose: Returns all the customer ids in atlas

    Args:
     None

    Returns:
        list of int: Returns list of customer id in atlas

    """

    db = AtlasDbUtils()
    customer_ids = db.execute_db_select_query('select id from atlas_bundle ')
    return [ customer_id[0] for customer_id in customer_ids ]

@exec_log
def get_customer_details_for_name(name):
    """
    Purpose: Returns customer  information for specified customer name  

    Args:
        name (str): customer name

    Returns:
        nametuple object: object having customer details

    """

    db = AtlasDbUtils()
    customer_attributes = ['id','created_date','modified_date','bundle_id','description','quantity','start_date','end_date','stage',\
                           'sku','order_type','activated_date','license_data','sma_license_data','customer_id','extended_state_id',\
                           'state_id','type_id','purchase_order','sales_order','deal_id', 'notification_state']
    Customer = namedtuple('Customer',customer_attributes)
    inner_query = ''' select id from atlas_customer where name='{0}' '''.format(name)
    try:
        rows = db.execute_db_select_query('''select * from atlas_bundle where customer_id = ({0})'''.format(inner_query))
        return Customer(*rows[0])
    except:
        raise Exception('Input Customer {} is not present'.format(name))

@exec_log
def get_current_state(cust_id):
    """
    Purpose: Returns the state id for the customer id

    Args:
        cust_id (int): customer id

    Returns:
        int: current state id of the customer

    """

    db = AtlasDbUtils()
    state = db.execute_db_select_query('select state_id from atlas_bundle where customer_id={}'.format(cust_id))[0][0]
    if state == 15:
        raise TemporaryAllocationException("Customer provisioning failed due to temporary allocation")
    if state == 12:
        raise ConfigErrorException("Customer provisioning failed due to config error")

    return state

@exec_log
def is_customer_provisioned(cust_name, m_timeout=2048, m_step=30):
    """
    Purpose: Waits for specified time for the customer to be provisioned specified in input 

    Args:
        cust_name (str) : Name of the customer in exports db
        m_timeout (int) : Max. wait time in seconds for customer to be provisioned
        m_step (int)    : polling interval

    Returns:
        bool: The return value. True if customer is provisioned, False otherwise.

    """

    logger.info("Customer name is {}".format(cust_name))
    db = AtlasDbUtils()
    id = db.execute_db_select_query('''select id from atlas_bundlestate where name='PROVISIONED' ''')[0][0]
    status = False
    try:
        cust_id = get_customer_details_for_name(cust_name).customer_id
        logger.info("Waiting for customer to be provisioned")
        status  = polling.poll(lambda: get_current_state(cust_id) == id,
                               timeout=m_timeout,
                               step=m_step,
                              )
    except TemporaryAllocationException as e:
        raise TemporaryAllocationException("Customer provisioning failed due to Temporary allocation - {}".format(cust_name))
    except ConfigErrorException as e:
        raise ConfigErrorException("Customer provisioning failed due to config error - {}".format(cust_name))
    except polling.TimeoutException:
        status = False
    if status == False:
        raise CustomerNotProvisionedException("Customer - {} failed to get provisioned ".format(cust_name))
    else:
        logger.info("Customer - {} is provisioned...".format(cust_name))
        return status

@exec_log
def wait_server_until_assigned(server_name, m_timeout=1240, m_step=30):
    """
    Purpose: wait until server is moved to assigned state

    Args:
        server_name (str): server name which has to be moved to assigned state
        m_timeout (int) : Max. wait time in seconds for customer to be provisioned
        m_step (int)    : polling interval
      
    Returns:
        bool: True if the customer gets provisioned in the give wait time else False

    """

    logger.info("server_name is {}".format(server_name))
    db = AtlasDbUtils()
    status = False
    try:
        logger.info("Waiting for server to be assigned")
        status  = polling.poll(lambda: db.execute_db_select_query('''select state_id from atlas_server where name='{}' '''.format(server_name))[0][0] ==2,
                               timeout=m_timeout,
                               step=m_step,
                              )
    except:
        status = False
    if status == False:
        logger.info("Server  - {} was not  assigned...".format(server_name))
        raise AtlasServerUnAssignedException("Server - {} was not assigned ".format(server_name))
    else:
        logger.info("Server - {} is configured to assigned...".format(server_name))
        return status

@exec_log
def is_notifications_present(notification1,notification2,subject,mail_to,mail_from):
    """
    Purpose: check the notification is present in notification table in atlas db

    Args:
        notification1   : First set of notifications 
        notification2   : Second set of notifications
        subject         : Subject in the email
        mail_to         : Email address of mail recipient
        mail_from       : Email address of mail sender

    Returns:
        bool: Returns True if input notification is present, False otherwise.

    """

    list1 = [ (subject,mail_from,mail_to) for id,created_date,mail_from,mail_to,subject,text in notification1 ]
    length1 = len(list1)
    list2 = [ (subject,mail_from,mail_to) for id,created_date,mail_from,mail_to,subject,text in notification2 ]
    length2 = len(list2)
    if length1 == length2:
        return False
    else:
        notifications = list2[length1:]
        for notification in notifications:
            if (subject.strip(),mail_from,mail_to) == notification:
                return True
        return False

@exec_log
def get_internal_servername():
    """
    Purpose: Gets the collection of server names in atlas_instance

    Args:

    Returns:
        set of strings: Returns list of servers

    """

    db = AtlasDbUtils()
    servers = db.execute_db_select_query('select internal_name from atlas_instance')
    servers = { server[0] for server in servers }
    return servers

@exec_log
def get_unassigned_servers():
    """
    Purpose: Gets the list of unassigned servers

    Args:

    Returns:
        list of strings: Returns list of servers


    """

    db = AtlasDbUtils()
    servers =  db.execute_db_select_query('''select name from atlas_server where state_id=(select id from atlas_state where name='UNASSIGNED')''')
    servers = { server[0] for server in servers }
    logger.info("Available servers - {} ".format(servers))
    return servers

@exec_log
def wait_for_model_in_dc_inventory(model,datacenter,count):
    """
    Purpose: Forever wait untill the specified model is ready in datacenter

    Args:
        model (str)      : ESA SMA model
        datacenter (str) : Primary or secondary datacenter
        count(int)       : Number of servers in the datacenter

    Returns:
       None

    """
 
    polling.poll(lambda: get_unassigned_server_count_in_dc(model,datacenter)>=int(count) ,
                               poll_forever=True,
                               step=30,
                              ) 

@exec_log
def is_welcome_letter_present(customer,email):
    """
    Purpose: Checks if welcome letter is sent to the customer

    Args:
        customer (str): customer for which the welcome letter to be checked
        email (str)   : email address of customer

    Returns:
         Returns True if welcome letter is sent to customer , raises exception otherwise.

    """
    for e in get_notification():
        if "{}: Welcome to Cisco CES Email Security Services".format(customer) in e[4] and e[3]==email:
           return True
    raise WelcomeLetterNotPresentException("Welcome Letter is not sent to customer {} for email address {}".format(customer,email))

@exec_log
def is_notification_present(customer,email,notificationtext):
    """
    Purpose: Checks if notification is sent to the customer

    Args:
        customer (str): customer for which the configuration notification to be checked
        email (str)   : email address of customer
        notificationtext: notificationstring to be check in db.

    Returns:
         Returns True if notification is present.

    """
    for e in get_notification():
        if notificationtext+" "+"{}".format(customer) in e[4] and e[3]==email:
           return True

@exec_log 
def is_ready(model,datacenter,count):
    """
    Purpose: Check if inventory has specific number of server model in a datacenter

    Args:
        model(str)      : ESA or SMA model - Eg:C100V,M100V
        datacenter(str) : Primary or secondary datacenter
        count(int)      : Number of servers necessary

    Returns:
        bool: Returns True is specific model of server in datacenter is available, False otherwise

    """
    try:
        wait_for_model_in_dc_inventory(model,datacenter,count)
    except:
        raise Exception("Atlas does not have {} {} model in {} datacenter in inventory".format(count,model,datacenter))

@exec_log
def update_include_fetch_customer_filter():
    """
    Purpose: Updates the customer type and sub type for pulling customer from exportdb

    Args:
          None
    Returns:
          None
    """
    cmd = r'echo -e "[include]\ncustomer_type={}\ncustomer_sub_type={}\n[exclude]\n" > $ATLAS_HOME/etc/{}'.\
    format(ATLAS_EXPORT_CUSTOMER_DATA['customer_type'],ATLAS_EXPORT_CUSTOMER_DATA['customer_sub_type'],ATLAS_CONSTANTS['include_exclude_default_config'])
    logger.debug("Updating the fetch customer filers in file {}".format(cmd))
    execute_atlas_command(cmd)

@exec_log
def is_cron_locked(cron):
    """
    Purpose: Checks if cron is locked

    Args:
        cron (str) : Name of the customer in exports db

    Returns:
        bool: Returns True if the cron is locked else false

    """
    db = AtlasDbUtils()
    stmt = ''' select mon_lock from crons where command='{}' '''.format(cron)
    mon_status =  db.execute_db_select_query(stmt)[0][0] 
    return mon_status is not None

@exec_log
def provision_exports_customer(cust_name,min_from_now=2,m_timeout=180,m_step=30):
    """
    Purpose: Checks for provisioned customer from exportdb

    Args:
        cust_name (str)    : Name of the customer in exports db
        min_from_now (int) : Minutes from current time
        m_timeout (int)    : Max. wait time in seconds for customer to be provisioned
        m_step (int)       : polling interval

    Returns:
        bool: Returns True if the customer is added to atlas

    """
    update_include_fetch_customer_filter()
    mod_min = get_min_from_now(min_from_now).strip()
    if mod_min.startswith("0"):
        mod_min=mod_min[1:]
    update_fetch_new_customer_timestamp(mod_min,ATLAS_CONSTANTS['django_settings'])
    execute_atlas_command('systemctl restart celery',prompt=DEFAULT_PROMPTS['ROOT_PROMPT'])
    if is_cron_locked('fetchcustomers_new'):
        reset_atlas_fetch_customer_new_cron()
    db = AtlasDbUtils()
    status = False
    try:
        logger.info("Waiting for export customer {} to be provisioned ".format(cust_name))
        status  = polling.poll(lambda:is_customer_present(cust_name) == True,
                               timeout=m_timeout,
                               step=m_step,
                              )
    except polling.TimeoutException:
        logger.debug("Polling timeout exception occured while waiting for customer... ")

    if status == False:
        logger.info("Export Customer Name - {} was not added to atlas...".format(cust_name))
        raise ExportCustomerImportFailedException("Export Customer was NOT added to atlas")
    else:
        logger.info("Export Customer Name - {} is added to atlas successfully...".format(cust_name))
        if is_customer_provisioned(cust_name):
            if is_cron_locked('fetchcustomers_new'):
                raise FetchCustomerCronLockedException("Fetch customer Cron is locked")
        else:
            raise CustomerNotProvisionedException("Export Customer is NOT provisioned")
        return status

def get_days_from_now(days=30):
    """
    Purpose: Number of days from current date in atlas

    Args:
        days(int): number of days

    Returns:
       returns date from today
    """
    date_command = ''' date -d "+ {} days" "+%m/%d/%Y" '''.format(days)
    future_date = execute_atlas_command(date_command).strip().split("\n")[1]
    return future_date

@exec_log
def get_current_extended_state(customer_name):
    """
    Purpose: Check current bundle extended state for the customer

    Args:
        customer_name(str): customer name

    Returns:
       int: returns the extended state i.e 0 or 1 indicating LOAD_LICENSE_FILE OR DEFAULT

    """
    cmd = 'select extended_state_id from atlas_bundle where license_data LIKE  "%<company>%{}%</company>%"'.format(customer_name)
    db = AtlasDbUtils()
    customer_extended_state = db.execute_db_select_query(cmd)
    if customer_extended_state:
        return customer_extended_state[0][0]
    else:
        raise NoSuchAtlasCustomerException("No such customer {}".format(customer_name))

@exec_log
def run_license_pusher_get_customer_extended_state(customer_name):
    """
    Purpose: Executes license pusher command

    Args:
        customer_name(str): customer name

    Returns:
       int: returns the extended state for the input customer

    """

    execute_atlas_command('export ATLAS_HOME={} && python {}'.format(ATLAS_CONSTANTS['atlas_home'],ATLAS_CONSTANTS['license_pusher']), timeout=120)
    logger.info("running license pusher on atlas")
    return get_current_extended_state(customer_name)

@exec_log
def run_license_pusher():
    """
    Purpose: Executes license pusher command

    Args:
        None

    Returns:
       None

    """
    execute_atlas_command('export ATLAS_HOME={} && python {}'.format(ATLAS_CONSTANTS['atlas_home'],ATLAS_CONSTANTS['license_pusher']), timeout=120)

@exec_log
def check_extended_state_by_running_license_pusher(customer_name):
    """
    Purpose: Executes license pusher command by verifying customer bundle extended state of customer

    Args:
        customer_name(str): customer name

    Returns:
        Return true of license pusher run succeeds else raises exception

    """
    if run_license_pusher_get_customer_extended_state(customer_name) == 1:
        try:
            status  = polling.poll(lambda: run_license_pusher_get_customer_extended_state(customer_name) == 2,
                               timeout=240,
                               step=120,
                              )
        except polling.TimeoutException:
            status = False
            logger.debug("License pusher failed to be pushed on ESA/SMA")
   
        if status == False:
            raise LicensePushFailException("License pusher failed to push license to ESA/SMA - {}".format(customer_name))
        else:
            logger.info("License pusher - {} pushed  license on re-trying...".format((customer_name)))
            return status
    else:
        logger.info("License pusher pushed on to customer {} successfully in first attempt".format(customer_name))

@exec_log
def update_purchase_order_end_dates(end_days,so_name):
    """
    Purpose: Modifies end dates for the input sales order

    Args:
        end_days(str)   : Modifies end dates of the sales order
        so_name(str)    : sales order

    Returns:
        None
    """
    db = AtlasDbUtils()
    end_days= get_days_from_now(str(end_days)).strip()
    end_days = datetime.strptime(end_days, "%m/%d/%Y").strftime("%Y-%m-%d")
    sql_stmt = '''update atlas_customerpoorders set fb_end_date='{0}' where sales_order='{1}' '''.format(end_days,str(so_name))
    db.execute_db_update_query(sql_stmt)

@exec_log
def check_license_expiry(customer_name, days):
    cmd = 'select bundle_id from atlas_feature'
    db = AtlasDbUtils()
    bundleids = db.execute_db_select_query(cmd)
    bundle_id = bundleids[0][0]
    license_expiry_check = date.today() + timedelta(int(days))
    cmd2 = '''update  atlas_feature set end_date='{0}' where bundle_id='{1}' '''.format(license_expiry_check,bundle_id)
    updated_date = db.execute_db_update_query(cmd2)

@exec_log
def check_license_expiry_with_featurename(customer_name, days,featurenames):
    cmd = 'select bundle_id from atlas_feature'
    db = AtlasDbUtils()
    bundleids = db.execute_db_select_query(cmd)
    bundle_id = bundleids[0][0]
    license_expiry_check = date.today() + timedelta(int(days))
    cmd2 = '''update  atlas_feature set end_date='{0}' where bundle_id='{1}' and name IN '{2}'} '''.format(license_expiry_check,bundle_id,featurenames)
    updated_date = db.execute_db_update_query(cmd2)


@exec_log
def run_feature_expiry_monitor():
    """
    Purpose: Executes Feature Expiry Monitor

    Args:
        None

    Returns:
       None

    """
    execute_atlas_command('export ATLAS_HOME={} && python {}'.format(ATLAS_CONSTANTS['atlas_home'],ATLAS_CONSTANTS['feature_expiry_monitor']))


@exec_log
def is_featureexpirynotification_present(customername):
      db = AtlasDbUtils()
      sqlstmt = '''select * from atlas_notificationemail where subject="Feature expiration notification for {} "'''.format(customername)
      query = db.execute_db_select_query(sqlstmt)
      if query:
          return query[0][5]
      else:
          raise Exception('Feature Expiry notification for Customer {} is not present'.format(customername))

@exec_log
def newuser_permission(user):
    """
        Purpose: update user permission for given user in DB.

        Args   : Username as String

        Returns: None

    """
    db = AtlasDbUtils()
    db.execute_db_update_query(''' update auth_user set is_staff='1', is_active='1',is_superuser='1' where username= '{}' '''.format(user))

@exec_log
def read_file(file_name,prompt=DEFAULT_PROMPTS['ROOT_PROMPT'], timeout=20):
    """
        Purpose: read a file from command prompt using cat command

        Args:
            file_name : Name of the file which needs to be opened and read
            prompt    : command prompt
            timeout   : wait time before timeout

        Returns:
               content of the file

    """
    atlascli = CliUtils()
    atlascli.ssh_login(ATLAS_CONSTANTS['atlas_host_ip'], ATLAS_SERVER.user, ATLAS_SERVER.password, "atlas-cli")
    atlascli.execute_command('sudo bash')
    read_file_cmd = 'cat '+file_name
    file_output = atlascli.execute_command(read_file_cmd)
    return file_output


@exec_log
def search_expiry_date_in_log(file_output):
    """
        Purpose: To search for the expiry dates in file output

        Args:
          file_output: content of the file

        Returns:
          True if expected expiry dates are matching else False

    """
    date_to_be_searched = expected_feature_date()
    output = search_text_in_file_output(file_output,date_to_be_searched)
    return output


@exec_log
def expected_feature_date():
    """
        Purpose: To create Expected expiry dates based on days duration

        Args:
            None

        Returns:
            Expected expiry dates as string

    """

    date_duration = [90,60,30,15,10,5,1]
    expected_feature_expiry_date = "["
    for i in date_duration:
            new_date = date.today()+timedelta(days=i)
            expected_feature_expiry_date = expected_feature_expiry_date + "'" + str(new_date) + "', "
    expected_feature_expiry_date = expected_feature_expiry_date[:-2] + "]"
    logger.info("The Expected Feature Expiry dates for days interval {0} are {1}".format(date_duration,expected_feature_expiry_date))
    return expected_feature_expiry_date


@exec_log
def search_text_in_file_output(file_output, text):
    """
    Purpose: To search for the text in file output

    Args:
        file_output: content of the file
        text:text to be searched in output

    Returns:
        True if expected text is present else False

    """
    logger.info("The text to be searched is {}".format(text))
    if text in file_output:
       logger.info("The text {} is present in file output".format(text))
       return True

    else:
        logger.info("The text {} is not present in file output".format(text))
        return False



@exec_log
def get_free_ip_address_count(data_center):
    """
    Purpose: Returns  free ip count

    Args:
        data_center   : data center

    Returns:
        int: number of free ip address

    """

    return len(get_ip_address("Free",data_center))

@exec_log
def get_ip_address(state,dc):
    """
    Purpose: Fetches and returns the list of ip address based on state

    Args:
        state  : state of Ip address
        dc     : data center

    Returns:
        list: list of Ip address

    """
    try:
        if state == "Free":
            status_id = 1
        elif state == "Assigned":
            status_id = 2
        elif state == "Blacklisted":
            status_id = 3

        db = AtlasDbUtils()
        ip_address = db.execute_db_select_query(''' select ip from atlas_ipaddress where ip_status_id = {} and data_center_id ={}'''.format(status_id,dc))
        logger.debug("Ip Address {}".format(ip_address))
        return  [ip_address[0] for ip in ip_address]
    except:
        raise Exception('Unable to find Ip address')

@exec_log
def update_feature_expiry_monitor_file(filepath,attribute,value):
    """
        Purpose: Update the value of any config file  in feature_expiry_monitor.conf

        Args:
            filepath     : FilePath
            attribute    : Attribute of config file to be changed
            value        : value to updated for given attribute.
    """
    cmd = "cat"+" "+str(filepath)+" "+"| grep -iE"+ " '"+str(attribute)+"='"
    cmd_output = execute_atlas_command(cmd)
    if cmd_output:
        edit_cmd="sed -i 's/"+str(attribute)+"=.*/"+str(attribute)+"=" + str(value) + "/'"+" "+str(filepath)
        execute_atlas_command(edit_cmd)

@exec_log
def get_feature_expiry_monitor_file_values(sections,attribute):
    """
        Purpose: Update the value of include_expired_features in feature_expiry_monitor.conf

        Args:
            conifg_path  : FilePath
            value        : value to be stored

        Returns          : Returns True if value is updated in file
    """
    parser = SafeConfigParser()
    conifg_path='/usr/local/ironport/atlas/etc/feature_expiry_monitor.conf'
    parser.read(conifg_path)
    attribute_value=parser.get(sections, attribute)
    if attribute_value:
        return attribute_value
    else:
        return False




