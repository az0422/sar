def arr2const(arr):
    result = 0

    for index, element in enumerate(arr):
        result += element << (index << 3)
    
    return result

def const2arr(const, length=8):
    result = bytearray()

    for _ in range(length):
        result.append(const & 0xFF)
        const >>= 8
    
    return result



    