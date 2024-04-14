    iread %stck,$.stack
    call $main
    halt

.array:
    .data $0x11111111
    .data $0x22222222
    .data $0x33333333
    .data $0x44444444
    .data $0x55555555
    .data $0x66666666
    .data $0x77777777
    .data $0x88888888
    .data $0x99999999
    .data $0xAAAAAAAA
    .data $0xBBBBBBBB
    .data $0xCCCCCCCC
    .data $0xDDDDDDDD
    .data $0xEEEEEEEE

main:
    iread %addr0,$.array
    iread %addr1,$.result
    iread %main1,$8
    iread %main2,$32

    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func

    ret
func:
    mread %addr0,%main0 # 1
    shlt %main0,%main2,%data0
    or %main0,%data0
    mwrite %data0,%addr1

    add %main1,%addr0
    add %main1,%addr1

    ret

    .space $0x40
.stack:
    .space $0x40
.result:
    .space $0x100