    iread %stck,$.stack
    iread %addr0,$main
    call %addr0
    halt

main:
    iread %main0,$0x12345678
    iread %main1,$0x12345678
    iread %main2,$0x20
    shlt %main1,%main2,%main1
    add %main1,%main0
    ret

    .space $0x40
.stack: