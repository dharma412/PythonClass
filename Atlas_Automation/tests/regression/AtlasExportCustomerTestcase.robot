*** Settings ***
Resource              regression/atlas_exports_customer.robot

Suite Setup            CustomerProvisionFromExportsAndLogin
Suite Teardown         DeleteAllocationLogoutOfAtlas

*** Variables ***
${customer_name}           ${ATLAS_EXPORT_CUSTOMER_DATA['customer_name']}
${esa_model}               ${ATLAS_CONSTANTS['C100V']}
${sma_model}               ${ATLAS_CONSTANTS['M100V']}


*** Test Cases ***
001_Verify_SMA_Is_Accessible_After_Customer_Provisioning
      Click On Activations Renewals
      Search Customer Name                 ${customer_name}
      Topnav.Click On Customer Name        ${customer_name}
      Click On Allocation Name
      Access SMA

002_Verify_ESA_Is_Accessible_After_Customer_Provisioning
      Click On Activations Renewals
      Search Customer Name                 ${customer_name}
      Topnav.Click On Customer Name        ${customer_name}
      Click On Allocation Name
      Access ESA


