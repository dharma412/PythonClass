***Settings***
Library     CesCliLibrary
Resource    esa/global.txt


***Keywords***
Write Ces Cli Output To Html File
    [Arguments]  ${filename}=${None}  ${data}=${EMPTY}

    ${html_head}=  Catenate  SEPARATOR=\n
    ...  <html>
    ...  <body>
    ...  <div>
    Append To File  ${filename}  ${html_head}

    FOR  ${line}  IN  @{data}
        Append To File  ${filename}  <p>${line}</p>
    END

    ${html_tail}=  Catenate  SEPARATOR=\n
    ...  </div>
    ...  </body>
    ...  </html>
    Append To File  ${filename}  ${html_tail}

Write Cli Output To File
    [Arguments]  ${filename}=${None}  ${data}=${EMPTY}

    Create File  ${filename}
    FOR  ${line}  IN  @{data}
        Append To File  ${filename}  ${line}\n
    END