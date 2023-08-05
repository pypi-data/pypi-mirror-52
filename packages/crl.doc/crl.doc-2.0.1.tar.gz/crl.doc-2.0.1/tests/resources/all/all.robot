*** Settings ***
Documentation    Example settings documentation

*** Variables ***
${EXAMPLE_VARIABLE}=    Example

*** Keywords ***
Example Keyword
    [Documentation]    Example keyword documentation
    [Arguments]    ${example_argument}
    [Return]    ${example_argument}


*** Test Cases ***
Example Test
    [Documentation]   Example test case documentation
    Log   Example
