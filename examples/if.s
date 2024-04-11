    iread %stck,$.stack
    call $main
    halt

main:
    iread %cycl0,$0xF
    iread %cycl1,$1
    iread %addr0,$0
    iread %addr1,$8
    iread %main3,$0x20

    and %cycl0,%cycl0

    jump $.cond
.loop:
    cmpi %cycl0,$0xF
    je $.L0

    cmpi %cycl0,$0xE
    je $.L1

    cmpi %cycl0,$0xD
    je $.L2

    cmpi %cycl0,$0xC
    je $.L3

    cmpi %cycl0,$0xB
    je $.L4

    cmpi %cycl0,$0xA
    je $.L5

    cmpi %cycl0,$0x9
    je $.L6

    cmpi %cycl0,$0x8
    je $.L7

    cmpi %cycl0,$0x7
    je $.L8

    cmpi %cycl0,$0x6
    je $.L9

    cmpi %cycl0,$0x5
    je $.L10

    cmpi %cycl0,$0x4
    je $.L11

    cmpi %cycl0,$0x3
    je $.L12

    cmpi %cycl0,$0x2
    je $.L13

    cmpi %cycl0,$0x1
    je $.L14

.retp:
    mwrite %main0,%addr0,$.result
    add %addr1,%addr0

    subt %cycl0,%cycl1,%cycl0

.cond:
    jne $.loop
    ret

.L0:
    iread %main0,$0x11111111
    iread %main1,$0x11111111
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L1:
    iread %main0,$0x22222222
    iread %main1,$0x22222222
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L2:
    iread %main0,$0x33333333
    iread %main1,$0x33333333
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L3:
    iread %main0,$0x44444444
    iread %main1,$0x44444444
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L4:
    iread %main0,$0x55555555
    iread %main1,$0x55555555
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L5:
    iread %main0,$0x66666666
    iread %main1,$0x66666666
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L6:
    iread %main0,$0x77777777
    iread %main1,$0x77777777
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L7:
    iread %main0,$0x88888888
    iread %main1,$0x88888888
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L8:
    iread %main0,$0x99999999
    iread %main1,$0x99999999
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L9:
    iread %main0,$0xAAAAAAAA
    iread %main1,$0xAAAAAAAA
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L10:
    iread %main0,$0xBBBBBBBB
    iread %main1,$0xBBBBBBBB
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L11:
    iread %main0,$0xCCCCCCCC
    iread %main1,$0xCCCCCCCC
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L12:
    iread %main0,$0xDDDDDDDD
    iread %main1,$0xDDDDDDDD
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L13:
    iread %main0,$0xEEEEEEEE
    iread %main1,$0xEEEEEEEE
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp
.L14:
    iread %main0,$0xFFFFFFFF
    iread %main1,$0xFFFFFFFF
    shlt %main0,%main3,%main0
    or %main1,%main0
    jump $.retp


    .space $0x40
.stack:

    .space $0x40

.result:
    .space $0x100