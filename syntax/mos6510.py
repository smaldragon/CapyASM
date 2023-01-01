from . import mos6502
"""
MOS 6510

6502 variant used on the C64/128
- extra I/O port mapped to the start of zero page
"""

registers = mos6502.registers

macro = mos6502.macro+"""
    .var DDR $00
    .var PORT $01
"""

opcodes = mos6502.opcodes