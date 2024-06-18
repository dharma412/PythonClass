
*** Settings ***
Library    RequestsLibrary
Resource    CommonAPI_Keywords.robot

*** Keywords ***
FetchRepoDetails
    [Tags]    Repo
#    Create GIT_HUB Creation
    ${fetch_resp}=    GET On Session    endpoint    url=${FetchRepo}
    ${statu_code_value}=  Set Variable    ${fetch_resp.status_code}
    should be equal as integers    ${statu_code_value}    200    msg=codes are ot same
    ${fetch_resp_jsonformate}    set variable    ${fetch_resp.json()}

    [Return]    ${fetch_resp_jsonformate}

Create Repo
    [Tags]    Repo
    ${req_body}    Set Variable    {"name":${Repo_Name}}
    ${fetch_resp}=    POST On Session   endpoint    url=${RepoCreate}    data=${req_body}   headers=${HEADERS}
    should be equal as integers    ${fetch_resp.status_code}    201    msg=codes are ot same
    [Return]    ${fetch_resp}

Delete Repo
    [Tags]    Delete
    log to console    ${Delete_repo}${Repo_Name}
    ${dele_resp}=    DELETE On Session    endpoint    url=${Delete_repo}${Repo_Name}    headers=${HEADERS}
    should be equal as integers    ${dele_resp.status_code}     204

