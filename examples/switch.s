    iread %stck,$.stack
    call $main
    halt

.switchs:
    .data $.L0
    .data $.L1
    .data $.L2
    .data $.L3
    .data $.L4
    .data $.L5
    .data $.L6
    .data $.L7
    .data $.L8
    .data $.L9
    .data $.L10
    .data $.L11
    .data $.L12
    .data $.L13
    .data $.L14

main:
    iread %cycl0,$0xF
    iread %cycl1,$1
    iread %addr0,$0
    iread %addr1,$8
    iread %main3,$0x20

    and %cycl0,%cycl0

    jump $.cond
.loop:
    mread %addr0,%addr2,$.switchs
    call %addr2
    mwrite %main0,%addr0,$.result
    add %addr1,%addr0
    subt %cycl0,%cycl1,%cycl0
.cond:
    jg $.loop
    ret

.L0:
    iread %main0,$0x11111111
    iread %main1,$0x11111111
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L1:
    iread %main0,$0x22222222
    iread %main1,$0x22222222
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L2:
    iread %main0,$0x33333333
    iread %main1,$0x33333333
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L3:
    iread %main0,$0x44444444
    iread %main1,$0x44444444
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L4:
    iread %main0,$0x55555555
    iread %main1,$0x55555555
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L5:
    iread %main0,$0x66666666
    iread %main1,$0x66666666
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L6:
    iread %main0,$0x77777777
    iread %main1,$0x77777777
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L7:
    iread %main0,$0x88888888
    iread %main1,$0x88888888
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L8:
    iread %main0,$0x99999999
    iread %main1,$0x99999999
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L9:
    iread %main0,$0xAAAAAAAA
    iread %main1,$0xAAAAAAAA
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L10:
    iread %main0,$0xBBBBBBBB
    iread %main1,$0xBBBBBBBB
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L11:
    iread %main0,$0xCCCCCCCC
    iread %main1,$0xCCCCCCCC
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L12:
    iread %main0,$0xDDDDDDDD
    iread %main1,$0xDDDDDDDD
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L13:
    iread %main0,$0xEEEEEEEE
    iread %main1,$0xEEEEEEEE
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret
.L14:
    iread %main0,$0xFFFFFFFF
    iread %main1,$0xFFFFFFFF
    shlt %main0,%main3,%main0
    or %main1,%main0
    ret


    .space $0x40
.stack:

    .space $0x40

.result:
    .space $0x100