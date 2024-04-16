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
    iread %addr4,$.result
    iread %main4,$8
    iread %main5,$32

    addt %main4,%addr0,%addr1
    addt %main4,%addr1,%addr2
    addt %main4,%addr2,%addr3
    
    addt %main4,%addr4,%addr5
    addt %main4,%addr5,%addr6
    addt %main4,%addr6,%addr7

    iread %main6,$0x2
    shlt %main4,%main6,%main4

    rcopyns256all %main4,%s256b0
    rcopyns256all %main5,%s256b8
    # read address
    rcopyns256q %addr0,%addr1,%addr2,%addr3,%s256b1
    # write address
    rcopyns256q %addr4,%addr5,%addr6,%addr7,%s256b2

    call $func
    call $func
    call $func
    call $funcFinal

    ret

func:
    rcopysn256q %s256b1,%func10,%func11,%func12,%func13
    rcopysn256q %s256b2,%func18,%func19,%func1a,%func1b

    mread %func10,%func0
    mread %func11,%func1
    mread %func12,%func2
    mread %func13,%func3

    rcopyns256q %func0,%func1,%func2,%func3,%s256b9

    shlts256 %s256b9,%s256b8,%s256ba
    orts256 %s256b9,%s256ba,%s256b9

    rcopysn256q %s256b9,%data0,%data1,%data2,%data3

    mwrite %data0,%func18
    mwrite %data1,%func19
    mwrite %data2,%func1a
    mwrite %data3,%func1b

    addts256 %s256b1,%s256b0,%s256b1
    addts256 %s256b2,%s256b0,%s256b2

    ret

funcFinal:
    rcopysn256q %s256b1,%func10,%func11,%null,%null
    rcopysn256q %s256b2,%func12,%func13,%null,%null,

    mread %func10,%func0
    mread %func11,%func1

    rcopyns256q %func0,%func1,%null,%null,%s256b9

    shlts256 %s256b9,%s256b8,%s256ba
    orts256 %s256b9,%s256ba,%s256b9

    rcopysn256q %s256b9,%data0,%data1,%null,%null

    mwrite %data0,%func12
    mwrite %data1,%func13

    ret
    
    .space $0x40
.stack:
    .space $0x40
.result:
    .space $0x100