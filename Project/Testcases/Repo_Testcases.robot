*** Settings ***
Resource        ../Keywords/CommonAPI_Keywords.robot
Resource        ../Keywords/RepoKeyords.robot
Suite Setup   GITHUB COMMON SETUP

*** Variables ***

*** Test Cases ***
FetchAllRepos
    ${res}=    FetchRepoDetails
    log to console    ${res}

CreateRepoTest
    ${resp}=    Create Repo
    sleep    180
    log to console    ${resp}
