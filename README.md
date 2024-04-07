# Simple Architecture RISC Simulator

## Outline
* This archictecture has only one pattern instruction.
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
* 4-7th byte: constant
* 8th byte: reserved

### Instruction set

| opcode (hex)  | format (assembly)  | format (bytecode)  | Explain                                   |
|---------------|--------------------|--------------------|-------------------------------------------|
| 00            | halt               | 00 FF FF 00000000  | halt                                      |
| 10            | nop                | 10 FF FF 00000000  | nop                                       |
| 20            | mread %rA,%rB      | 20 rA rB 00000000  | read from memory (addr: rA, dest: rB)     |
| 21            | pop %rB            | 21 FF rB 00000000  | pop (dest: rB)                            |
| 30            | mwrite %rA, %rB    | 30 rA rB 00000000  | write to memory (data: rA, dest: rB)      |
| 31            | push %rA           | 31 rA FF 00000000  | push (data: rA)                           |
| 40            | iread %rA,$constant| 40 FF rA constant  | constant to rB                            |
| 50            | add %rA,%rB        | 50 rA rB 00000000  | rB = rA + rB                              |
| 51            | sub %rA,%rB        | 51 rA rB 00000000  | rB = rA - rB                              |
| 52            | shr %rA,%rB        | 52 rA rB 00000000  | rB = rA >> rB                             |
| 53            | shl %rA,%rB        | 53 rA rB 00000000  | rB = rA << rB                             |
| 54            | and %rA,%rB        | 54 rA rB 00000000  | rB = rA & rB                              |
| 55            | or %rA,%rB         | 55 rA rB 00000000  | rB = rA | rB                              |
| 56            | not %rA,%rB        | 56 rA rB 00000000  | rB = ~rA                                  |
| 57            | xor %rA,%rB        | 57 rA rB 00000000  | rB = rA ^ rB                              |
| 60            | jump $constant     | 60 FF FF constant  | jump (dest: constant)                     |
| 61            | jl $constant       | 61 FF FF constant  | jl (dest: constant)                       |
| 62            | jle $constant      | 62 FF FF constant  | jle (dest: constant)                      |
| 63            | je $constant       | 63 FF FF constant  | je (dest: constant)                       |
| 64            | jge $constant      | 64 FF FF constant  | jge (dest: constant)                      |
| 65            | jg $constant       | 65 FF FF constant  | jg (dest: constant)                       |
| 66            | jne $constant      | 66 FF FF constant  | jne (dest: constant)                      |
| 70            | call $constant     | 70 FF FF constant  | call (dest: constant)                     |
| 71            | ret                | 71 FF FF 00000000  | ret                                       |

### Registers
* Generic Registers: 00-FD

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

## TODO
* Find the bugs and fix
* Add some features for architecture
* Add more examples
