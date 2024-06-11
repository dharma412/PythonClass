*** Settings ***
Resource        Keywords/GithubKeywords.robot

Suite Setup   GithubKeywords.Session Creation

*** Variables ***
${FetchRepo}    /users/dharma412/repos

*** Test Cases ***
FetchAllRepos
    ${resp}=    GET On Session    endpoint    url=${FetchRepo}

