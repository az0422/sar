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
    iread %addr2,$.result
    iread %main4,$8
    iread %main5,$32
    addt %main4,%addr0,%addr1
    addt %main4,%addr2,%addr3
    add %main4,%main4

    rcopyns128all %main4,%s128b0
    rcopyns128all %main5,%s128b8
    # read address
    rcopyns128d %addr0,%addr1,%s128b1
    # write address
    rcopyns128d %addr2,%addr3,%s128b2

    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func

    ret

func:
    rcopysn128d %s128b1,%addr0,%addr1
    rcopysn128d %s128b2,%addr2,%addr3

    mread %addr0,%main0
    mread %addr1,%main1

    rcopyns128d %main0,%main1,%s128b9
    shlts128 %s128b9,%s128b8,%s128ba
    orts128 %s128b9,%s128ba,%s128b9

    rcopysn128d %s128b9,%data0,%data1

    mwrite %data0,%addr2
    mwrite %data1,%addr3

    addts128 %s128b1,%s128b0,%s128b1
    addts128 %s128b2,%s128b0,%s128b2

    ret
    
    .space $0x40
.stack:
    .space $0x40
.result:
    .space $0x100