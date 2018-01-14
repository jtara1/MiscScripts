.text
    ;call print_sp
    call print_key

print_key:
    mov A, 1
    HWI 4 ; fetch key & store in B register
    HWI 9 ; print B register
    ret

print_sp:
    ;push 44
    ;push 45
    mov A, 1
    mov B, SP ; SP value is decremented after push
    HWI 9     ; print B register
    ret
    