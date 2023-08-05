# Copyright (C) 2019, Nokia

*** Settings ***

Library    crl.remotesession.remotesession.RemoteSession
...        WITH NAME    RemoteSession

Library    filehelper.py
Library    MyCreator.py
Library    Collections
Suite Setup    Create Random File
Suite Teardown    RemoteSession.Close
Test Setup    Set Targets
Force Tags     remotecompare

*** Variables ***

&{DEFAULT_RUNNER_PROPERTIES}=  default_executable=/bin/bash
...                     max_processes_in_target=${100}
...                     prompt_timeout=${30}
...                     termination_timeout=${10}
...                     update_env_dict=&{EMPTY}

&{DEFAULT_TARGET_PROPERTIES}=
...                       cleanup=${True}
...                       connection break is error=${True}
...                       connection failure is error=${True}
...                       login prompt=login:${SPACE}
...                       login timeout=${60}
...                       max connection attempts=${10}
...                       nonzero status is error=${False}
...                       password prompt=Password:${SPACE}
...                       port=${None}
...                       prompt=\$${SPACE}
...                       prompt is regexp=${False}
...                       su password=${None}
...                       su username=${None}
...                       use sudo user=${False}

&{HOST1}=    host=10.102.227.10
...          user=root
...          password=root

&{HOST2}=    host=10.20.105.90
...          user=root
...          password=root

&{SSHHOST}
@{SHELLDICTS1}=    ${HOST1}
@{SHELLDICTS2}=    ${HOST2}
@{SHELLDICTS3}=    ${SSHHOST}
${TESTFILESIZE}=    1000000
&{DEFAULT_TARGET}=        cleanup=${True}
...                       connection break is error=${True}
...                       connection failure is error=${True}
...                       login prompt=login:${SPACE}
...                       login timeout=${60}
...                       max connection attempts=${10}
...                       nonzero status is error=${False}
...                       password prompt=Password:${SPACE}
...                       port=${None}
...                       prompt=\$${SPACE}
...                       su password=${None}
...                       su username=${None}
...                       use sudo user=${False}

${COMMAND}=     echo foo;echo bar >&2
${SRC_FILE}=    ${CURDIR}/sourcedict.sh
@{RUNNER_TARGETS}=    runner1  runner2
@{TARGETS}=     script1  script2
${TEST_VALUE}=  ${None}

*** Keywords ***
Create Random File
    filehelper.Create Random File    targetlocal    ${TESTFILESIZE}

Set Targets
    Set RemoteScript Targets
    Set RemoteRunner Targets

Set RemoteRunner Targets
    RemoteSession.Set Runner Target    shelldicts=${SHELLDICTS1}
    ...                                name=runner1

    RemoteSession.Set Runner Target    shelldicts=${SHELLDICTS2}
    ...                                name=runner2

Set RemoteScript Targets
    RemoteSession.Set Target    host=${HOST1.host}
    ...                         username=${HOST1.user}
    ...                         password=${HOST1.password}
    ...                         name=script1

    RemoteSession.Set Target    host=${HOST2.host}
    ...                         username=${HOST2.user}
    ...                         password=${HOST2.password}
    ...                         name=script2

    RemoteSession.Set Target With Sshkeyfile
    ...                         host=${SSHHOST.host}
    ...                         username=${SSHHOST.user}
    ...                         sshkeyfile=${SSHHOST.key}
    ...                         name=sshtarget



*** Keywords ***

Compare Results
    [Arguments]    ${result1}    ${result2}
    Should Be True
    ...    '${result1.status}' == '${result2.status}' or '${result2.status}' == 'unknown'
    Should Be Equal    ${result1.stdout}    ${result2.stdout}
    Should Be Equal    ${result1.stderr}    ${result2.stderr}

Compare Execute Command In Target
    [Arguments]     ${runner}  ${script}
    ${ret_from_runner}=    RemoteSession.Execute Command In Target
    ...    command=${COMMAND}
    ...    target=${runner}
    ...    timeout=1
    ${ret_from_script}=    RemoteSession.Execute Command In Target
    ...    command=${COMMAND}
    ...    target=${script}
    ...    timeout=1
    Compare Results    ${ret_from_runner}    ${ret_from_script}

Compare Copy Directory To Target
    [Arguments]     ${runner}  ${script}
    ${ret_from_runner}=     RemoteSession.Copy Directory To Target
    ...    tests/
    ...    /tmp/runner/
    ...    0744
    ...    target=${runner}
    ${ret_from_script}=     RemoteSession.Copy Directory To Target
    ...    tests/
    ...    /tmp/script/
    ...    0744
    ...    target=${script}
    ${diff}=    RemoteSession.Execute Command In Target
    ...    diff -r /tmp/runner/ /tmp/script/    ${runner}
    Should Be Equal    ${diff.status}    0
    Compare Results    ${ret_from_runner}    ${ret_from_script}

Compare Create Directory In Target
    [Arguments]     ${runner}  ${script}
    ${ret_of_runner}=    RemoteSession.Create Directory In Target
    ...    /tmp/runnercreate/
    ...    0444
    ...   ${runner}

    ${ret_of_script}=    RemoteSession.Create Directory In Target
    ...    /tmp/scriptcreate
    ...    0444
    ...   ${script}
    ${diff}=    RemoteSession.Execute Command In Target
    ...    diff -r /tmp/runnercreate/ /tmp/scriptcreate/    ${runner}
    Should Be Equal    ${diff.status}    0
    Compare Results    ${ret_of_runner}    ${ret_of_script}

Compare Execute Background Command In Target
    [Arguments]     ${target}
    FOR    ${i}    IN RANGE    2
         RemoteSession.Execute Background Command In Target
         ...    echo out;>&2 echo err;sleep 10
         ...    ${target}
         ...    test
         Sleep    1
         RemoteSession.Kill Background Execution    test
         ${runner}=    RemoteSession.Wait Background Execution    test
    END
    # No comparison with the RemoteScript can be done because there is a bugs
    # in the RemotScript background execution functionality Using instead
    # comparison with results which RemoteScript should ideally return

    Should Be Equal    ${runner.status}    -15
    Should Be Equal    ${runner.stdout}    out
    Should Be Equal    ${runner.stderr}    err

Test Get Source Update Env Dict
    [Arguments]     ${src_path}  ${target}
    ${updated_dict}=    Get Source Update Env Dict
    ...     path=${src_path}
    ...     target=${target}
    Set Runner Target Property
    ...     target_name=${target}
    ...     property_name=update_env_dict
    ...     property_value=${updated_dict}
    ${ret_from_command}=    Execute Command In Target
    ...     command=echo $foo;echo $bar
    ...     target=${target}
    Should Be Equal
    ...     ${ret_from_command.stdout}  Hello\nWorld!     ${ret_from_command}

Set All Default Target Properties
    [Arguments]  ${new_value}  ${keys}  ${setter_method}
    FOR  ${key}    IN    @{keys}
        Run Keyword  ${setter_method}
        ...     property_name=${key}
        ...     property_value=${new_value}
    END


Reset All Default Target Properties
    [Arguments]  ${default_keys}  ${default_dictionary}  ${setter_method}
    FOR  ${key}  IN  @{default_keys}
        ${value}=   Get From Dictionary
        ...         dictionary=${default_dictionary}
        ...         key=${key}
        Run Keyword  ${setter_method}
        ...     property_name=${key}
        ...     property_value=${value}
    END

Check That Targets Have Original Values
    [Arguments]     ${targets}  ${original_property_dict}  ${target_setter}
    Run Keyword  ${target_setter}
    FOR     ${i}   IN  @{targets}
        ${check_default_properties}=  Get Target Properties  target=${i}
        Check Property Equalities
        ...     orig_properties=${original_property_dict}
        ...     properties=${check_default_properties}
    END

Check Property Equalities
    [Arguments]  ${orig_properties}  ${properties}
    Dictionary Should Contain Sub Dictionary
    ...     dict1=${properties}
    ...     dict2=${orig_properties}

Check Value Equals All List Values
    [Arguments]  ${value}  ${value_list}
    FOR     ${value_in_list}  IN  @{value_list}
        Should Be Equal     ${value_in_list}    ${value}   ${value_in_list}
    END

Test Set Envcreator
    [Arguments]  ${target}
    ${envcreator}=      Get Library Instance  MyCreator
    Set Envcreator  ${envcreator}
    ${ret}=  Execute Command In Target
    ...     command=echo $foo
    ...     target=${target}.foo
    Should Be Equal As Integers  ${ret.status}  0  ${ret}
    Should Be Equal  ${ret.stdout}  barfoo  ${ret}

*** Test Cases ***

Template Test Set Envcreator
    [Template]  Test Set Envcreator
    runner1
    runner2

Template Test Get Source Update Env Dict
    [Template]  Test Get Source Update Env Dict
    ${SRC_FILE}  runner1
    ${SRC_FILE}  runner2

Template Compare Execute Command In Target
    [Template]  Compare Execute Command In Target
    runner1  script1
    runner2  script2

Template Compare Copy Directory To Target
    [Template]  Compare Copy Directory To Target
    runner1  script1
    runner2  script2

Template Compare Create Directory In Target
    [Template]  Compare Create Directory In Target
    runner1  script1
    runner2  script2

Template Compare Execute Background Command In Target
    [Template]  Compare Execute Background Command In Target
    runner1
    runner2

Test Set Runner Default Target Property
    ${default_keys}=    Get Dictionary Keys  dictionary=${DEFAULT_RUNNER_PROPERTIES}
    Set All Default Target Properties
    ...     new_value=${TEST_VALUE}
    ...     keys=${default_keys}
    ...     setter_method=RemoteSession.Set Runner Default Target Property
    FOR  ${target}   IN  @{RUNNER_TARGETS}
        RemoteSession.Set Runner Target
        ...                 shelldicts=${SHELLDICTS1}
        ...                 name=${target}
        ${properties}=   RemoteSession.Get Target Properties  target=${target}
        ${prop_values}=     Get Dictionary Values  dictionary=${properties}
        Check Value Equals All List Values
        ...     value=${TEST_VALUE}
        ...     value_list=${prop_values}
    END
    Reset All Default Target Properties
    ...     default_keys=${default_keys}
    ...     default_dictionary=${DEFAULT_RUNNER_PROPERTIES}
    ...     setter_method=RemoteSession.Set Runner Default Target Property
    [Teardown]  Check That Targets Have Original Values
    ...         targets=${RUNNER_TARGETS}
    ...         original_property_dict=${DEFAULT_RUNNER_PROPERTIES}
    ...         target_setter=Set RemoteRunner Targets

Test Set Default Target Property
    ${target_props}=    RemoteSession.Get Target Properties  target=script1
    ${tmpdir}=  Get From Dictionary
    ...     ${target_props}
    ...     tempdir
    ${DEFAULT_TARGET_PROPERTIES}=   Set To Dictionary
    ...     ${DEFAULT_TARGET_PROPERTIES}
    ...     tempdir
    ...     ${tmpdir}
    ${default_keys}=    Get Dictionary Keys  dictionary=${DEFAULT_TARGET_PROPERTIES}
    Set All Default Target Properties
    ...     new_value=${TEST_VALUE}
    ...     keys=${default_keys}
    ...     setter_method=RemoteSession.Set Default Target Property
    FOR  ${target}   IN  @{TARGETS}
        RemoteSession.Set Target
        ...                 host=${HOST1.host}
        ...                 username=${HOST1.user}
        ...                 password=${HOST1.password}
        ...                 name=${target}
        ${properties}=   RemoteSession.Get Target Properties  target=${target}
        ${prop_values}=     Get Dictionary Values  dictionary=${properties}
        Check Value Equals All List Values
        ...     value=${TEST_VALUE}
        ...     value_list=${prop_values}
    END
    Reset All Default Target Properties
    ...     default_keys=${default_keys}
    ...     default_dictionary=${DEFAULT_TARGET_PROPERTIES}
    ...     setter_method=RemoteSession.Set Default Target Property
    [Teardown]  Check That Targets Have Original Values
    ...         targets=${TARGETS}
    ...         original_property_dict=${DEFAULT_TARGET_PROPERTIES}
    ...         target_setter=Set RemoteScript Targets

Test Set Target With Sshkeyfile
    ${ret_of_command}=      Execute Command In Target
    ...     command=${COMMAND}
    ...     target=sshtarget
    Should Be Equal As Integers  ${ret_of_command.status}       0       ${ret_of_command}

Compare File Copying
    ${runner1}=    RemoteSession.Copy File To Target
    ...    targetlocal
    ...    .
    ...    0755
    ...    runner1
    ${runner2}=    RemoteSession.Copy File Between Targets
    ...     runner1
    ...     targetlocal
    ...     runner2
    ...     .
    ...     0755

    ${runner3}=    RemoteSession.Copy File From Target
    ...    targetlocal
    ...    remoterunnerfile
    ...    target=runner2
    filehelper.diff files    targetlocal    remoterunnerfile

    ${script1}=    RemoteSession.Copy File To Target
    ...    targetlocal
    ...    .
    ...    0755
    ...    script1

    ${script2}=    RemoteSession.Copy File Between Targets
    ...     script1
    ...     targetlocal
    ...     script2
    ...     .
    ...     0755

    ${script3}=    RemoteSession.Copy File From Target
    ...    targetlocal
    ...    remotescriptfile
    ...    target=script2

    ${mixed11}=    RemoteSession.Copy File To Target
    ...    targetlocal
    ...    .
    ...    0755
    ...    script1

    ${mixed12}=    RemoteSession.Copy File Between Targets
    ...     script1
    ...     targetlocal
    ...     runner2
    ...     .
    ...     0755

    ${mixed13}=    RemoteSession.Copy File From Target
    ...    targetlocal
    ...    mixedfile1
    ...    target=script2


    filehelper.diff files    targetlocal    mixedfile1

    ${mixed21}=    RemoteSession.Copy File To Target
    ...    targetlocal
    ...    .
    ...    0755
    ...    runner1

    ${mixed22}=    RemoteSession.Copy File Between Targets
    ...     runner1
    ...     targetlocal
    ...     script2
    ...     .
    ...     0755

    ${mixed33}=    RemoteSession.Copy File From Target
    ...    targetlocal
    ...    mixedfile2
    ...    target=script2

    filehelper.diff files    targetlocal    mixedfile2

    Compare Results    ${runner1}    ${script1}
    Compare Results    ${runner2}    ${script2}
    Compare Results    ${runner3}    ${script3}
    Compare Results    ${runner1}    ${mixed11}
    Compare Results    ${runner2}    ${mixed12}
    Compare Results    ${runner3}    ${mixed13}

Test Get Remoterunner Targets
    ${targets}=     Get Remoterunner Targets
    FOR     ${i}    IN  runner1  runner2
        Dictionary Should Contain Key
        ...     dictionary=${targets}
        ...     key=${i}
    END

Test Get Remotescript Targets
    ${targets}=     Get Remotescript Targets
    FOR     ${i}    IN    script1  script2  sshtarget
        Dictionary Should Contain Key
        ...     dictionary=${targets}
        ...     key=${i}
    END

Test Get Target Properties
    FOR     ${i}    IN      script1  script2  sshtarget
        ${properties}=     Get Target Properties
        ...     target=${i}
        Dictionary Should Contain Sub Dictionary
        ...         ${properties}
        ...         ${DEFAULT_TARGET}
    END
