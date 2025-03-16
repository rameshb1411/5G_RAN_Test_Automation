*** Settings ***
Library    Process
Library    BuiltIn

*** Variables ***
${EXPECTED_MIB}                Broadcasting MIB... -> SFN=
${EXPECTED_SIB1}               Broadcasting SIB1... -> PLMN=00101
${EXPECTED_ALL_SIBS}           ALL_SIBS_BROADCASTED
${EXPECTED_UE_DECODE_MIB}      Decoded MIB:
${EXPECTED_UE_DECODE_SIB}      Decoded SIB:
${TIMESTAMP_REGEX}             \[\d{2}:\d{2}:\d{2}\.\d{3}\]

*** Test Cases ***
Test MIB Broadcasting
    ${result}=    Run Process    python    gnb_simulator.py    --duration    10    shell=True    timeout=15
    Log    ${result.stdout}
    Should Contain    ${result.stdout}    ${EXPECTED_MIB}

Test SIB1 Broadcasting
    ${result}=    Run Process    python    gnb_simulator.py    --duration    10    shell=True    timeout=15
    Log    ${result.stdout}
    Should Contain    ${result.stdout}    ${EXPECTED_SIB1}

Test All SIBs Broadcast Confirmation
    ${result}=    Run Process    python    gnb_simulator.py    --duration    10    shell=True    timeout=15
    Log    ${result.stdout}
    Should Contain    ${result.stdout}    ${EXPECTED_ALL_SIBS}

Test MIB and SIB Periodicity
    ${result}=    Run Process    python    gnb_simulator.py    --duration    10    shell=True    timeout=15
    Log    ${result.stdout}
    ${mib_count}=    Evaluate    len(re.findall("Broadcasting MIB", '''${result.stdout}'''))    modules=re
    ${sib1_count}=   Evaluate    len(re.findall("Broadcasting SIB1", '''${result.stdout}'''))    modules=re
    Log    MIB count: ${mib_count}, SIB1 count: ${sib1_count}
    Should Be True    ${mib_count} >= 100
    Should Be True    ${sib1_count} >= 100

Test Log Capture with Timestamps
    ${result}=    Run Process    python    gnb_simulator.py    --duration    10    shell=True    timeout=15
    Log    ${result.stdout}
    Should Match Regexp    ${result.stdout}    ${TIMESTAMP_REGEX}
    Should Contain    ${result.stdout}    scs30or120
    Should Contain    ${result.stdout}    Offset=8
    Should Contain    ${result.stdout}    DMRS=pos2
    Should Contain    ${result.stdout}    PDCCH=32
    Should Contain    ${result.stdout}    CellBarred=notBarred

Test UE Decoding
    ${result}=    Run Process    python    ue_simulator.py    --duration    10    shell=True    timeout=15
    Log    ${result.stdout}
    Should Contain    ${result.stdout}    ${EXPECTED_UE_DECODE_MIB}
    Should Contain    ${result.stdout}    ${EXPECTED_UE_DECODE_SIB}
