    iread %stck,$stack
    call $main
    halt

main:
    iread %main0,$0
    iread %cycl0,$1
    iread %cycl1,$0x10
    iread %addr0,$.result
    iread %addr1,$8

    jump $.cond
.loop:
    add %cycl0,%main0
    mwrite %main0,%addr0
    add %addr1,%addr0

    cmp %cycl1,%main0

.cond:
    jg $.loop
    ret

.result:

    .space $0x200
stack: