*** Variables ***





*** Test Cases ***
    @{list}=  CREATE LIST  1  2  3

    :FOR   ${i}  IN  @{list}:
            log to console  ${i}
     END