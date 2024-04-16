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
    mwrite %main0,%addr0
    add %main1,%main0
    add %addr1,%addr0

    ret

    .space $0x40
.stack:

    .space $0x40

.result:
    .space $0x100