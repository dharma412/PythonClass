
*** Settings ***
Library    RequestsLibrary
Resource    CommonAPI_Keywords.robot

*** Keywords ***
FetchRepoDetails
    [Tags]    Repo
#    Create GIT_HUB Creation
    ${fetch_resp}=    GET On Session    endpoint    url=${FetchRepo}
    should be equal as integers    ${fetch_resp.status_code}    200
    ${fetch_resp}    set variable    ${fetch_resp.json()}
    [Return]    ${fetch_resp}

Create Repo
    [Tags]    Repo
    ${req_body}    Set Variable    {"name":"RepoName12"}
    ${fetch_resp}=    POST On Session   endpoint    url=${RepoCreate}    data=${req_body}   headers=${HEADERS}
    [Return]    ${fetch_resp}