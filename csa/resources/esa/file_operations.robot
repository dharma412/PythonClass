*** Keywords ***
Generate File
    [Arguments]  ${source_file}  ${dest_file}  ${replace_string}  ${min_range}=10  ${max_range}=50
    ${random_num}=  Evaluate  random.randint(${min_range}, ${max_range})  random
    ${random}=  Generate Random String  ${random_num}
    Log  ${random}
    Convert To String  ${random}
    Run  sed 's/${replace_string}/${random}/g' ${source_file} > ${dest_file}
    [Return]  ${dest_file}

