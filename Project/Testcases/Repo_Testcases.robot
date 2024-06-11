*** Settings ***
Resource        ../Keywords/CommonAPI_Keywords.robot
Resource        ../Keywords/RepoKeyords.robot
Suite Setup   GITHUB COMMON SETUP

*** Variables ***

*** Test Cases ***
FetchAllRepos
    ${resp}=    FetchRepoDetails
    log    ${resp}

CreateRepoTest
    ${resp}=    Create Repo
    log to console    ${resp}

