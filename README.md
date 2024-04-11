# Simple Architecture RISC Simulator

## Outline
* Instruction length is only 8 bytes (7+1 bytes.)
* Structure of this architecture is very simple.
* I drunk highball, that was delicious and made my brain smart (just for a moment.)

## How to use
### Assembler
`python3 assembler.py <assembly.s>`

example: `python3 assembler.py test.s`

### Simulator
`python3 simulator.py <programfile.bin>`

example: `python3 simulator.py examples/add.bin`

## Instruction
### Format

* length: 7+1 bytes
* 1st byte: opcode
* 2nd byte: rA
* 3rd byte: rB
* 4th byte: rC (only some opcodes)
* 4-7th byte: constant
* 8th byte: tail

### Instruction set

| opcode and tail<br>(hex)  | format<br>(assembly)         | format<br>(bytecode)     | Explain                                              |
|---------------------------|------------------------------|--------------------------|------------------------------------------------------|
| 00, FF                    | halt                         | 00 FF FF 00000000 FF     | halt                                                 |
| 10, FF                    | nop                          | 10 FF FF 00000000 FF     | nop                                                  |
| 20, FF                    | mread %rA,%rB,$constant      | 20 rA rB 00000000 FF     | read from memory (addr: rA + constant, dest: rB)     |
| 21, FF                    | pop %rB                      | 21 FF rB 00000000 FF     | pop (dest: rB)                                       |
| 30, FF                    | mwrite %rA,%rB,$constant     | 30 rA rB 00000000 FF     | write to memory (data: rA, dest: rB + constant)      |
| 31, FF                    | push %rA                     | 31 rA FF 00000000 FF     | push (data: rA)                                      |
| 40, FF                    | iread %rB,$constant          | 40 FF rB constant FF     | constant to rB                                       |
| 50, FF                    | add %rA,%rB                  | 50 rA rB 00000000 FF     | rB = rA + rB                                         |
| 51, FF                    | sub %rA,%rB                  | 51 rA rB 00000000 FF     | rB = rA - rB                                         |
| 52, FF                    | shr %rA,%rB                  | 52 rA rB 00000000 FF     | rB = rA >> rB                                        |
| 53, FF                    | shl %rA,%rB                  | 53 rA rB 00000000 FF     | rB = rA << rB                                        |
| 54, FF                    | and %rA,%rB                  | 54 rA rB 00000000 FF     | rB = rA & rB                                         |
| 55, FF                    | or %rA,%rB                   | 55 rA rB 00000000 FF     | rB = rA | rB                                         |
| 56, FF                    | not %rA,%rB                  | 56 rA rB 00000000 FF     | rB = ~rA                                             |
| 57, FF                    | xor %rA,%rB                  | 57 rA rB 00000000 FF     | rB = rA ^ rB                                         |
| 58, FF                    | cmp %rA,%rB                  | 58 rA rB 00000000 FF     | null = rA - rB                                       |
| 60, FF                    | jump %rB,$constant           | 60 FF rB constant FF     | jump (dest: rB + constant)                           |
| 61, FF                    | jl %rB,$constant             | 61 FF rB constant FF     | jl (dest: rB + constant)                             |
| 62, FF                    | jle %rB,$constant            | 62 FF rB constant FF     | jle (dest: rB + constant)                            |
| 63, FF                    | je %rB,$constant             | 63 FF rB constant FF     | je (dest: rB + constant)                             |
| 64, FF                    | jge %rB,$constant            | 64 FF rB constant FF     | jge (dest: rB + constant)                            |
| 65, FF                    | jg %rB,$constant             | 65 FF rB constant FF     | jg (dest: rB + constant)                             |
| 66, FF                    | jne %rB,$constant            | 66 FF rB constant FF     | jne (dest: rB + constant)                            |
| 70, FF                    | call %rB,$constant           | 70 FF rB constant FF     | call (dest: rB + constant)                           |
| 71, FF                    | ret                          | 71 FF FF 00000000 FF     | return                                               |
| 50, 01                    | addt %rA,%rB,%rC             | 50 rA rB rC 000000 01    | rC = rA + rB                                         |
| 51, 01                    | subt %rA,%rB,%rC             | 51 rA rB rC 000000 01    | rC = rA - rB                                         |
| 52, 01                    | shrt %rA,%rB,%rC             | 52 rA rB rC 000000 01    | rC = rA >> rB                                        |
| 53, 01                    | shlt %rA,%rB,%rC             | 53 rA rB rC 000000 01    | rC = rA << rB                                        |
| 54, 01                    | andt %rA,%rB,%rC             | 54 rA rB rC 000000 01    | rC = rA & rB                                         |
| 55, 01                    | ort %rA,%rB,%rC              | 55 rA rB rC 000000 01    | rC = rA | rB                                         |
| 56, 01                    | nott %rA,%rB,%rC             | 56 rA rB rC 000000 01    | rC = ~rA                                             |
| 57, 01                    | xort %rA,%rB,%rC             | 57 rA rB rC 000000 01    | rC = rA ^ rB                                         |


### Registers
* Generic Registers: 00-FD

| Index (hex)   | Name    | Explain                                   |
|---------------|---------|-------------------------------------------|
| 00 - 1F       | main0-1f| main                                      |
| 20 - 3F       | cycl0-1f| cycle                                     |
| 40 - 5F       | data0-1f| data                                      |
| 60 - 7F       | addr0-1f| memory address                            |
| 80 - 9F       | args0-1f| arguments of function                     |
| A0 - BF       | func0-1f| for inside of function                    |
| C0 - CF       | iovr0-1f| IO data                                   |
| E0 - FD       | sysm0-1d| system variable                           |
| FE            | stck    | stack point                               |
| FF            | null    | null (constant of 0)                      |
| PC            | -       | Program Counter                           |

## TODO
* Add more examples
* Implement SIMD functions
