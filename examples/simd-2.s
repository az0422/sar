    iread %stck,$.stack
    call $main
    halt

main:
    iread %main0,$0x11111111
    iread %main1,$32
    iread %addr0,$.result
    iread %addr1,$8

    shlt %main0,%main1,%main2
    or %main2,%main0
    rcopy %main0,%main1

    rcopyns128 %main0,%s128b0l
    rcopyns128all %main1,%s128b1
    addts128 %s128b0,%s128b1,%s128b0
    addts128 %s128b1,%s128b1,%s128b1
    
    rcopyns128 %addr0,%s128b8h
    add %addr1,%addr0
    rcopyns128 %addr0,%s128b8l
    add %addr1,%addr1
    rcopyns128all %addr1,%s128b9
    
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func
    call $func

    ret

func:
    rcopysn128d %s128b0,%data0,%data1
    rcopysn128d %s128b8,%addr0,%addr1

    mwrite %data0,%addr0
    mwrite %data1,%addr1

    addts128 %s128b0,%s128b1,%s128b0
    addts128 %s128b8,%s128b9,%s128b8

    ret

    .space $0x40
.stack:

    .space $0x40

.result:
    .space $0x100