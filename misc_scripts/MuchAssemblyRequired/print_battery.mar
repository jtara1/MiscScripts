HWID_BATTERY equ 0x000A
HWID_HOLO equ 0x0009

.text
    CALL print_battery

print_battery:
    PUSH A
    MOV A, 1
    HWI HWID_BATTERY
    HWI HWID_HOLO
    POP A
    RET