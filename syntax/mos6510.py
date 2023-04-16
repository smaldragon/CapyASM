from syntax.mos6502 import *
"""
MOS 6510

6502 variant used on the C64/128
- extra I/O port mapped to the start of zero page
"""

macro +="""

    .var DDR $00
    .var PORT $01
"""