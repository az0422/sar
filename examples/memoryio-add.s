    iread %stck,$.stack
    call $main

.array:
    .data $0x1234567800000000
    .data $0x0000000012345678

main:
    iread %addr0,$.array
    iread %addr3,$.result
    iread %addr1,$0x8

    add %addr1,%addr3
    add %addr0,%addr1

    mread %addr0,%main0
    mread %addr1,%main1
    add %main1,%main0
    
    mwrite %main0,%addr3

    .space $0x40
.stack:

.result:
    .space $0x20