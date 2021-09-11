*** Settings ***
Library             CreateCustomer.py 
Library             pages/atlas_login/Atlasloginpage.py
Library             pages/activations_renewals/Approvalpage.py
Library             pages/common/Topnav.py
Library             pages/cluster/server/ClusterPage.py
Library             pages/activations_renewals/Neworderpage.py
Library             pages/activations_renewals/Newpoorderpage.py
Library             libs/CreateCustomer.py
Variables           AtlasTestConstants.py

*** Variables ***
${data_center1}          ${ATLAS_CONSTANTS['primary_datacenter']}
${data_center2}          ${ATLAS_CONSTANTS['secondary_datacenter']}
${esa_model}             ${ATLAS_CONSTANTS['C100V']}
${sma_model}             ${ATLAS_CONSTANTS['M100V']}
${customer_name}         ${ATLAS_CUSTOMER_DATA.customer_name}
${jenkins_privateip}     ${JENKINS_SERVER.jenkins_private_ip}
${jenkins_user}          ${JENKINS_SERVER.jenkins_user}
${jenkins_password}      ${JENKINS_SERVER.jenkins_password}

*** Keywords ***
LoginToAtlas
       Wait For Model In Dc Inventory    ${sma_model}  ${data_center1}     1
       Log To Console                    SMA is available in DC1
       Wait For Model In Dc Inventory    ${esa_model}  ${data_center1}     1
       Log To Console                    ESA is available in DC1
       Wait For Model In Dc Inventory    ${esa_model}  ${data_center2}     1
       Log To Console                    ESA is available in DC2
       Log To Console                    Clearing Atlas Logs
       Execute Atlas Command             cat /dev/null > /data/var/log/atlas/allocator.log
       Execute Atlas Command             cat /dev/null > /data/var/log/atlas/autoconfig.log
       Execute Atlas Command             cat /dev/null > /data/var/log/atlas/autoconfig_pexpect.log
       Execute Atlas Command             cat /dev/null > /data/var/log/atlas/feature_expiry_monitor.log
       Log To Console                    Atlas Logs are Cleared Now
       Log To Console                    Started Suite Setup
       Atlasloginpage.Login To Atlas
       Log To Console                    Logged Into Atlas UI
       Click On Activations Renewals
       Log To Console                    Create New Customer and Verify If Customer got Provisioned
       Click On New Order
       Create Default Customer
       ${provisionedStatus}=  Is Customer Provisioned  ${customer_name}
       Should Be True  ${provisionedStatus}  Customer Provisioning Has Failed
       Log To Console                    Customer Got Provisioned Moving To Testcases

DeleteAllocationLogoutOfAtlas
      Log To Console                     Copying Logs to Jenkins
      Execute Atlas Command              scp -rp /data/var/log/atlas/allocator.log ${jenkins_user}@${jenkins_privateip}:/automation_result
      Execute Atlas Command              scp -rp /data/var/log/atlas/autoconfig.log ${jenkins_user}@${jenkins_privateip}:/automation_result
      Execute Atlas Command              scp -rp /data/var/log/atlas/autoconfig_pexpect.log ${jenkins_user}@${jenkins_privateip}:/automation_result
      Log To Console                     Logs are pushed to Jenkins
      Log To Console                     Starting test suite tear down
      Click On Activations Renewals
      Search Customer Name                      ${customer_name}
      Topnav.Click On Customer Name             ${customer_name}
      Click On Allocation Name    
      Click On Delete Allocation
      Log To Console                     Servers In RMA State Are
      @{servers_in_rma}=    Get Servers In Rma
      Log To Console                            ${servers_in_rma}
      Log To Console                     Checking for p1 p2 p3 alerts
      Check Servers In Cluster P1 Alert         ${servers_in_rma}
      Check Servers In Cluster P2 Alert         ${servers_in_rma}
      Check Servers In Cluster P3 Alert         ${servers_in_rma}
      Execute Inventory Delete
      Log To Console                     Completed test suite tear down and logging out of atlas 
      Logout Of Atlas 
