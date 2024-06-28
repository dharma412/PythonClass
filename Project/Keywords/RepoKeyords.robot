
*** Settings ***
Library    RequestsLibrary
Resource    CommonAPI_Keywords.robot
Library    RequestsLibrary
Resource    CommonAPI_Keywords.robot


*** Keywords ***
FetchRepoDetails
    [Tags]    Fetch
#    Create GIT_HUB Creation
    ${fetch_resp}=    GET On Session    endpoint    url=${FetchRepo}
    ${statu_code_value}=  Set Variable    ${fetch_resp.status_code}
    should be equal as integers    ${statu_code_value}    200    msg=codes are ot same
    ${fetch_resp_jsonformate}    set variable    ${fetch_resp.json()}

    RETURN    ${fetch_resp_jsonformate}

Create Repo
    [Tags]    Create
    ${req_body}    Set Variable    {"name":"${RepoName}"}
    ${fetch_resp}=    POST On Session   endpoint    url=${RepoCreate}    data=${req_body}   headers=${HEADERS}
    should be equal as integers    ${fetch_resp.status_code}    201
    RETURN    ${fetch_resp}


Update Repo
    [Tags]    Update
    ${req_body}    set variable    {"name":"${UpdatedRepoName}","description":"We have updated repository name","homepage":"https://github.com","private":false,"has_issues":true,"has_projects":true,"has_wiki":true}
    ${fetch_resp2}=  PATCH On Session    endpoint     url=${RepoUpdate}${RepoName}    data=${req_body}    headers=${HEADERS}
    should be equal as integers    ${fetch_resp2.status_code}    200
    RETURN    ${fetch_resp2}


Delete Repo
    [Tags]    Delete
    log to console    ${Delete_repo}${Repo_Name}
    ${dele_resp}=    DELETE On Session    endpoint    url=${Delete_repo}${Repo_Name}    headers=${HEADERS}
    should be equal as integers    ${dele_resp.status_code}     204
