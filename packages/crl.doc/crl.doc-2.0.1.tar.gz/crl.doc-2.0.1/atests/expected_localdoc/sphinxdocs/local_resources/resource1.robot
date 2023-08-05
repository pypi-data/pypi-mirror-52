*** Settings ***
Documentation    Resource 1 settings documentation

*** Variables ***
${RESOURCE_1_VARIABLE}=    Resource 1

*** Keywords ***
Resource 1 Keyword
    [Documentation]    Resource 1 keyword documentation
    [Arguments]    ${resource_1_argument}
    [Return]    ${resource_1_argument}

*** Test Cases ***
Resource 1 Test
    [Documentation]   Resource 1 test documentation
    ${ret}=    Resource 1 Keyword  ${RESOURCE_1_VARIABLE}
    Should Be Equal   ${ret}  ${RESOURCE_1_VARIABLE}
