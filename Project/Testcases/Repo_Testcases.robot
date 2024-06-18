*** Settings ***
Resource        ../Keywords/CommonAPI_Keywords.robot
Resource        ../Keywords/RepoKeyords.robot
Suite Setup   GITHUB COMMON SETUP


*** Test Cases ***
FetchAllRepos
    ${res}=    FetchRepoDetails

CreateRepoTest
    ${resp}=    Create Repo
    log to console    ${resp}

DeleteRepoTest
    Delete Repo


