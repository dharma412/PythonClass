
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

    RETURN    ${fetch_resp_jsonformate}

Create Repo
    [Tags]    Repo
    ${req_body}    Set Variable    {"name":"RepoName12385858"}
    ${fetch_resp}=    POST On Session   endpoint    url=${RepoCreate}    data=${req_body}   headers=${HEADERS}
    should be equal as integers    ${fetch_resp.status_code}    201    msg=codes are ot same
    RETURN    ${fetch_resp}


Update Repo
    [Tags]    Repo
    ${req_body}    set variable    {"name":"6/17/2024-updatedreponame","description":"We have updated repository name"}
    ${fetch_resp2}=  PATCH On Session    endpoint     url=${RepoPatch}    data=${req_body}    headers=${HEADERS}
    should be equal as integers    ${fetch_resp2.status_code}    200    msg=codes are ot same
    RETURN    ${fetch_resp2}
