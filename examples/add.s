    iread %stck,$.stack
    call $main
    halt

main:
    iread %main0,$0x100
    iread %main1,$0x020
    add %main1,%main0
    ret

    .space $0x40

.stack: