    iread %stck,$.stack
    call $main
    halt

main:
    iread %main0,$0x12345678
    iread %main1,$0x12345678
    iread %main2,$0x20
    shl %main1,%main2
    add %main2,%main0
    ret

    .space $0x40
.stack: