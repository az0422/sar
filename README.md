# Simple Architecture RISC Computer Simulator

## Instruction
### Format

* length 7+1 bytes
* 1st byte: opcode
* 2nd byte: rA
* 3rd byte: rB
* 4-7th byte: constant
* 8th byte: reserved

### Instruction set

| opcode (hex)  | Explain                                   |
|---------------|-------------------------------------------|
| 00            | halt                                      |
| 10            | nop                                       |
| 20            | read from memory (addr: rA, dest: rB)     |
| 21            | pop (dest: rB)                            |
| 30            | write to memory (data: rA, dest: rB)      |
| 31            | push (data: rA)                           |
| 40            | constant to rB                            |
| 50            | rB += rA                                  |
| 51            | rB -= rA                                  |
| 52            | rB >>= rA                                 |
| 53            | rB <<= rA                                 |
| 54            | rB &= rA                                  |
| 55            | rB |= rA                                  |
| 56            | rB = ~rA                                  |
| 57            | rB ^= rA                                  |
| 60            | jump (dest: constant)                     |
| 61            | jle (dest: constant)                      |
| 62            | jl (dest: constant)                       |
| 63            | je (dest: constant)                       |
| 64            | jge (dest: constant)                      |
| 65            | jg (dest: constant)                       |
| 66            | jne (dest: constant)                      |
| 70            | call (dest: constant)                     |
| 71            | ret                                       |

### Registers
| Index (hex)   | Explain                                   |
|---------------|-------------------------------------------|
| 00 - 1F       | main                                      |
| 20 - 3F       | cycle                                     |
| 40 - 5F       | data                                      |
| 60 - 7F       | memory address                            |
| 80 - 9F       | arguments of function                     |
| A0 - BF       | for inside of function                    |
| C0 - CF       | IO data                                   |
| E0 - FD       | system variable                           |
| FE            | stack point                               |
| FF            | null (constant of 0)                      |
| PC            | Program Counter                           |