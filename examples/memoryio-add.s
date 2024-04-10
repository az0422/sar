    iread %stck,$.stack
    call $main
    halt

.array:
    .data $0x1234567800000000
    .data $0x0000000012345678

main:
    iread %addr0,$0
    iread %addr1,$8
    mread %addr0,%main0,$.array
    mread %addr1,%main1,$.array
    add %main1,%main0
    mwrite %main0,%addr0,$.result

    ret

    .space $0x40
.stack:

.result:
    .space $0x20