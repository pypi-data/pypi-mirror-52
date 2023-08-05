*** Settings ***
Documentation    Resource 2 settings documentation

*** Variables ***
${RESOURCE_2_VARIABLE}=    Resource 2

*** Keywords ***
Resource 2 Keyword
    [Documentation]    Resource 2 keyword documentation
    [Arguments]    ${resource_2_argument}
    [Return]    ${resource_2_argument}


*** Test Cases ***
Resource 2 Test
    [Documentation]   Resource 2 test documentation
    ${ret}=    Resource 2 Keyword  ${RESOURCE_2_VARIABLE}
    Should Be Equal   ${ret}  ${RESOURCE_2_VARIABLE
