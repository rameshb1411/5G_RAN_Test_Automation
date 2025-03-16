*** Settings ***
Library           OperatingSystem
Library           Process

*** Variables ***
${UE_COUNT}       5
${COMPONENT_COUNT} 3

*** Test Cases ***
Power On Procedure
    Start UE Simulators
    Start Core Network Simulators
    Verify Attach Procedure

*** Keywords ***
Start UE Simulators
    FOR    ${index}    IN RANGE    1    ${UE_COUNT}+1
        Run Process    python    UE_Simulator/ue_simulator.py
    END

Start Core Network Simulators
    FOR    ${index}    IN RANGE    1    ${COMPONENT_COUNT}+1
        Run Process    python    Core_Network_Simulator/core_network_simulator.py
    END

Verify Attach Procedure
    Log    Verification of attach procedure completed.
