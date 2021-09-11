*** Settings ***
Library             CreateCustomer.py
Library             pages/atlas_login/Atlasloginpage.py
Library             pages/activations_renewals/Approvalpage.py
Library             pages/common/Topnav.py
Library             pages/cluster/server/ClusterPage.py
Library             pages/activations_renewals/Neworderpage.py
Variables           AtlasTestConstants.py

*** Variables ***
${data_center1}                 ${ATLAS_CONSTANTS['primary_datacenter']}
${data_center2}                 ${ATLAS_CONSTANTS['secondary_datacenter']}
${esa_model}                    ${ATLAS_CONSTANTS['C100V']}
${sma_model}                    ${ATLAS_CONSTANTS['M100V']}
${export_customer_name}         ${ATLAS_EXPORT_CUSTOMER_DATA['customer_name']}

*** Keywords ***
CustomerProvisionFromExportsAndLogin
      Atlasloginpage.Login To Atlas
      LOG TO CONSOLE        Checking if the customer is present
      ${customer_status}=   CreateCustomer.Is Customer Present               ${export_customer_name}
      Run Keyword If     ${customer_status} == True        DeleteAllocation
      LOG TO CONSOLE       Waiting for servers in inventory in the atlas...
      CreateCustomer.Wait For Model In Dc Inventory    ${sma_model}  ${data_center1}     1
      CreateCustomer.Wait For Model In Dc Inventory    ${esa_model}  ${data_center1}     1
      CreateCustomer.Wait For Model In Dc Inventory    ${esa_model}  ${data_center2}     1
      LOG TO CONSOLE      Waiting for customer is fetched from the exportsdb...
      CreateCustomer.Provision Exports Customer         ${export_customer_name}
      LOG TO CONSOLE      Waiting for customer is provisioned in atlas
      CreateCustomer.Is Customer Provisioned            ${export_customer_name}

DeleteAllocation
      Topnav.Click On Activations Renewals
      Topnav.Search Customer Name          ${export_customer_name}
      Topnav.Click On Customer Name        ${export_customer_name}
      Activationsrenewalspage.Click On Allocation Name
      ClusterPage.Click On Delete Allocation

DeleteAllocationLogoutOfAtlas
      Topnav.Click On Activations Renewals
      Topnav.Search Customer Name                 ${export_customer_name}
      Topnav.Click On Customer Name               ${export_customer_name}
      Activationsrenewalspage.Click On Allocation Name    
      @{servers_name}=  Servers In Allocation
      Click On Delete Allocation
      Check Servers In Cluster P1 Alert         ${servers_name}
      Check Servers In Cluster P2 Alert         ${servers_name}
      Check Servers In Cluster P3 Alert         ${servers_name}
      Execute Inventory Delete
      Logout Of Atlas 

