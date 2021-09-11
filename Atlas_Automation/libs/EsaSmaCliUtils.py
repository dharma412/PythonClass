import re

from datetime import datetime
from datetime import timedelta
from robot.api import logger

from AtlasTestConstants import ATLAS_CONSTANTS
from AtlasDbUtils import AtlasDbUtils
from CliUtils import CliUtils

def featurekey_on_appliance(host, type='ESA',timeout=45):
    """
    Purpose: Executes the featurekey command on atlas server

    Args:
        command       : featurekey command is executed on appliance
        type          : [Optional] ESA or SMA appliance type 
        timeout       : [Optional] time to wait for command execution

    Returns:
        Returns the output of featurekey command

    """
    host = host.strip()
    esa_features = ['IronPort Image Analysis','Outbreak Filters','IronPort Anti-Spam','McAfee',\
                    'Sophos Anti-Virus','Bounce Verification','Incoming Mail Handling','IronPort Email Encryption',\
                    'Data Loss Prevention','Cisco IronPort Spam Quarantine','Cloud Administration',\
                    'Cisco Centralized Email Reporting','Cisco IronPort Centralized Email Message Tracking',\
                    'Incoming Mail Handling','File Analysis','File Reputation','Graymail Safe Unsubscription']

    sma_features = ['Cisco IronPort Spam Quarantine', 'Cloud Administration Mode', 'Cisco Centralized Email Reporting',\
                     'Cisco IronPort Centralized Email Message Tracking','Incoming Mail Handling']
    if type == 'ESA':
        features = esa_features
    else:
        features = sma_features
    current_feature = []
    appliance_cli = CliUtils()
    appliance_cli.ssh_login_to_appliance(host,ATLAS_CONSTANTS['appliance_user'],ATLAS_CONSTANTS['appliance_password'],"appliance-cli")
    logger.info("SSH Login to {} appliance complete".format(host))
    output = appliance_cli.execute_command('featurekey',prompt='>',wait_time=timeout).replace('\r','').replace('\n','')
    regular_exp = re.findall('Expiration Date(.*?)Choose the operation you want to perform',output)
    if regular_exp:
        for feature in features:
            if feature in regular_exp[0]:
                r  = re.findall('{}(.*?)days'.format(feature),regular_exp[0])[0].split()
                if type == 'ESA':
                    current_feature.append({'feature':feature,'quantity':r[0],'status':r[1],'days_left':r[2]})
                else:
                    current_feature.append({'feature':feature,'status':r[0],'days_left':r[1]})
    appliance_cli.close_session()
    return current_feature

def is_feature_activated(current_feature,name):
    """
    Purpose: Checks specific feature is present on the applaince

    Args:
        current_feature : list of features in the appliance
        name            : Expected prompt after command execution

    Returns:
         Returns true if the feature in present in the applaince output else raise error
    """
    for f in current_feature:
        if f['feature'] == name and f['status'] in ('Active','Dormant') :
            logger.info("{} present".format(name))
            return True
    raise FeatureNotActivatedException("Feature {} is not present ".format(current_feature))

def verify_feature_activation(feature_name, actual_feature):
    """
    Purpose: Check the features are present on appliance based on input base bundle or addon  

    Args:
        feature_name    : Base bundle or addon like L-CES-ESO-LIC,L-CES-ESP-LIC etc.
        actual_feature  : The result of executing featurekey command against ESA or SMA

    Returns:
        Raises FeatureNotActivatedException  if feature NOT in present in the applaince output
    """
    master_featurelist = { 'L-CES-ESO-LIC':['Data Loss Prevention','IronPort Email Encryption'],\
                           'L-CES-ESI-LIC':['Sophos Anti-Virus','IronPort Anti-Spam','Outbreak Filters'],\
                           'L-CES-ESP-LIC':['Data Loss Prevention','IronPort Email Encryption','Sophos Anti-Virus','IronPort Anti-Spam','Outbreak Filters'],\
                           'L-CES-ESI-LIC':['IronPort Anti-Spam','Outbreak Filters','Sophos Anti-Virus'],\
                           'L-CES-O365I-LIC':['IronPort Anti-Spam' , 'Outbreak Filters'],\
                           'L-CES-O365P-LIC':['IronPort Anti-Spam','Data Loss Prevention','IronPort Email Encryption','Outbreak Filters'],\
                           'L-CES-AMP-LIC':['Cloud Administration','File Analysis','File Reputation'],\
                           'L-CES-GSU-LIC':['Graymail Safe Unsubscription'],\
                           'L-CES-DLP-LIC':['Data Loss Prevention'],\
                           'L-CES-MFE-LIC':['McAfee'],\
                           'L-CES-IA-LIC':['IronPort Image Analysis']
                         }
    for feature in master_featurelist.get(feature_name):
        is_feature_activated(actual_feature,feature)

def interface_config_server(host, type='ESA',timeout=45):
    """
    Purpose: Executes the clustermode cluster and interfaceconfig command on atlas server and to verify the data 2 IP

    Args:
        command       : Interfaceconfig command is executed on appliance
        type          : [Optional] ESA
        timeout       : [Optional] time to wait for command execution

    Returns:
        Returns the output of command
    """

    host = host.strip()
    appliance_cli = CliUtils()
    appliance_cli.ssh_login_to_appliance(host, ATLAS_CONSTANTS['appliance_user'], ATLAS_CONSTANTS['appliance_password'],
                                         "appliance-cli")
    logger.info("SSH Login to {} appliance complete".format(host))
    output = appliance_cli.execute_command('interfaceconfig', prompt='>', wait_time=timeout).replace('\r', '').replace('\n','')
    logger.info("entered interfaceconfig")
    return output



def verify_certificate_is_availabe_and_used_by_all_services(host, cert, services):
    """
    Purpose: ciscossl_certificate is verified for active status
             certificate is verified whether it is used by all services

    Args:
        host          : host ip
        cert          : certificate name
        services      :list of services

    Returns:
        Returns True is certificate is available , active and used by all service
    """

    host = host.strip()
    appliance_cli = CliUtils()
    appliance_cli.ssh_login_to_appliance(host, ATLAS_CONSTANTS['appliance_user'], ATLAS_CONSTANTS['appliance_password'],
                                         "appliance-cli")
    logger.info("SSH Login to {} appliance complete".format(host))
    cluster_mode_output = execute_clustermode_cluster_cmd(appliance_cli)
    cert_config_output = execute_certconfig_cmd(appliance_cli)
    cert_list = execute_certificate_cmd(appliance_cli)
    certificate_present = verify_certconfig_cmd_output_contains_expected_certificate(cert_list, cert)
    print_cert_list = execute_print_cmd(appliance_cli)
    used_by_serivces = verify_certificate_is_used_by_all_service(print_cert_list, cert, services)

    if cluster_mode_output and cert_config_output and cert_list and print_cert_list:
        if certificate_present == used_by_serivces == True:
                return True
        else:
                return False
    else:
        return False


def execute_clustermode_cluster_cmd(appliance_cli,timeout=45):
    """
    Purpose: Execute clustermode cluster in cli to enable clustermode

    Args:
        appliance_cli       : Utilities to interact with cli
        timeout             : [Optional] time to wait for command execution

    Returns:
        Returns the output of command
    """

    output = appliance_cli.execute_command('clustermode cluster', prompt='>', wait_time=timeout).replace('\r', '').replace('\n',
                                                                                                                  '')
    logger.info("Entered clustermode cluster")
    return output


def execute_certconfig_cmd(appliance_cli, timeout=45):
    """
    Purpose: Execute certconfig command in cli

    Args:
        appliance_cli       : Utilities to interact with cli
        timeout             : [Optional] time to wait for command execution

    Returns:
        Returns the output of  command
    """

    output = appliance_cli.execute_command('certconfig', prompt='>', wait_time=timeout).replace('\r', '').replace('\n',
                                                                                                                  '')
    logger.info("Entered certconfig")
    return output


def execute_certificate_cmd(appliance_cli, timeout=45):
    """
    Purpose: Execute certificate command in cli

    Args:
        appliance_cli       : Utilities to interact with cli
        timeout             : [Optional] time to wait for command execution

    Returns:
        Returns the output of  command as list
    """

    output = appliance_cli.execute_command_and_return_command_output_as_list('certificate', prompt='>', wait_time=timeout)
    logger.info("Entered certificate")
    return output


def execute_print_cmd(appliance_cli, timeout=45):
    """
    Purpose: Execute print command in cli

    Args:
        appliance_cli       : Utilities to interact with cli
        timeout             : [Optional] time to wait for command execution

    Returns:
        Returns the output of  command as list
    """

    output = appliance_cli.execute_command_and_return_command_output_as_list('print', prompt='>', wait_time=timeout)
    logger.info("Entered print")
    return output


def verify_certconfig_cmd_output_contains_expected_certificate(cert_list, cert):
    """
        Purpose: To verify expected certificate is present in list of certificate
        Args:
            cert_config_output       : output of cert_config command
            cert                    : certificate to be searched

        Returns:
            Returns the True if certificate is present else False would be returned
    """
    cert_list_counter = 0
    if cert_list:
        for ele in cert_list:
            if cert in ele and 'Active' in ele:
                logger.info("ciscossl_ certificate is active")
                cert_list_counter +=1
        if cert_list_counter == 1:
            return True
    else:
        return False


def verify_certificate_is_used_by_all_service(print_cert_list,cert, services):
    """
        Purpose: To verify certificate is used by all services
                 output of print command is checked for certificate name and then verified for service names

        Args:
            print_cert_list      : output of print command as list
            cert                 : certificate name
            services             :list of services

        Returns:
            Returns True if all services are used , else False
    """

    used_by_counter = 0
    for ele in print_cert_list:
        if cert in ele :
            for i in range(0, len(services)):
                if services[i] in ele:
                    used_by_counter += 1

    if used_by_counter == len(services):
        return True
    else:
        return False