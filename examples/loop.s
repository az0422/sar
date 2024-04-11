    iread %stck,$.stack
    call $main
    halt

main:
    iread %main0,$0x11111111
    iread %main1,$0x20
    shlt %main0,%main1,%main0
    iread %main1,$0x11111111
    or %main1,%main0 # set 0x1111111111111111
    rcopy %main0,%main1

    iread %cycl0,$0xF
    iread %cycl1,$1

    iread %addr0,$0
    iread %addr1,$8

    and %cycl0,%cycl0

    jump $.cond

.loop:
    mwrite %main0,%addr0,$.result
    add %main1,%main0
    add %addr1,%addr0

    subt %cycl0,%cycl1,%cycl0

.cond:
    jne $.loop
    ret

    .space $0x40
.stack:

.result:
    .space $0x100
