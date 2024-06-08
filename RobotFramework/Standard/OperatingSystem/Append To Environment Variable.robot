*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
ConvertTitileCase
    Append To Environment Variable	NAME	first
    Should Be Equal	 %{NAME}	 first
    Append To Environment Variable	NAME	second	third
    Should Be Equal	 %{NAME}	first${:}second${:}third
    log to console   %{NAME}