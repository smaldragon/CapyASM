"""
Western Design Center 65c02
"""
from . import mos6502

macro = mos6502.macro
registers = mos6502.registers
opcodes = mos6502.opcodes.copy()

opcodes.update({
    # Unconditional Branch
    "bra":{
        "r":    [0x80,"r"],
        "#":    [0x80,"i"]
    },
    # Push X to stack
    "phx":{
        "i":    [0xDA]
    },
    # Push Y to stack
    "phy":{
        "i":    [0x5A]
    },
    # Pull X from stack
    "plx":{
        "i":    [0xFA]
    },
    # Pull Y from stack
    "ply":{
        "i":    [0x7A]
    },
    # Stop processor until RESET
    "stp":{
        "i":    [0xDB]
    },
    # Wait until Interrupt
    "wai":{
        "i":    [0xCB]
    },
    # Store Zero
    "stz":{
        "a":    [0x9C,"al","ah"],
        "a+x":  [0x9E,"al","ah"],
        "z":    [0x64,"z"],
        "z+x":  [0x74,"z"],
    },
    # Test and Clear(Reset)/Set bits
    # - here A is a bitmask of the bits to change at a memory location
    # - the Z flag is set as if a BIT instruction had been performed
    "trb":{
        "a":    [0x1C,"al","ah"],
        "z":    [0x14,"z"],
    },
    "tcb":{
        "a":    [0x1C,"al","ah"],
        "z":    [0x14,"z"],
    },
    "tsb":{
        "a":    [0x0C,"al","ah"],
        "z":    [0x04,"z"],
    },
    # bbr/bbs
    # - Branches if a specific bit at a zero page address is Set/Cleared(Reset)
    "bbr0":{
        "zr":   [0x0F,"z","r"]
    },
    "bbr1":{
        "zr":   [0x1F,"z","r"]
    },
    "bbr2":{
        "zr":   [0x2F,"z","r"]
    },
    "bbr3":{
        "zr":   [0x3F,"z","r"]
    },
    "bbr4":{
        "zr":   [0x4F,"z","r"]
    },
    "bbr5":{
        "zr":   [0x5F,"z","r"]
    },
    "bbr6":{
        "zr":   [0x6F,"z","r"]
    },
    "bbr7":{
        "zr":   [0x7F,"z","r"]
    },
    "bbc0":{
        "zr":   [0x0F,"z","r"]
    },
    "bbc1":{
        "zr":   [0x1F,"z","r"]
    },
    "bbc2":{
        "zr":   [0x2F,"z","r"]
    },
    "bbc3":{
        "zr":   [0x3F,"z","r"]
    },
    "bbc4":{
        "zr":   [0x4F,"z","r"]
    },
    "bbc5":{
        "zr":   [0x5F,"z","r"]
    },
    "bbc6":{
        "zr":   [0x6F,"z","r"]
    },
    "bbc7":{
        "zr":   [0x7F,"z","r"]
    },
    "bbs0":{
        "zr":   [0x8F,"z","r"]
    },
    "bbs1":{
        "zr":   [0x9F,"z","r"]
    },
    "bbs2":{
        "zr":   [0xAF,"z","r"]
    },
    "bbs3":{
        "zr":   [0xBF,"z","r"]
    },
    "bbs4":{
        "zr":   [0xCF,"z","r"]
    },
    "bbs5":{
        "zr":   [0xDF,"z","r"]
    },
    "bbs6":{
        "zr":   [0xEF,"z","r"]
    },
    "bbs7":{
        "zr":   [0xFF,"z","r"]
    },
    "rmb0":{
        "z":    [0x07,"z"]
    },
    "rmb1":{
        "z":    [0x17,"z"]
    },
    "rmb2":{
        "z":    [0x27,"z"]
    },
    "rmb3":{
        "z":    [0x37,"z"]
    },
    "rmb4":{
        "z":    [0x47,"z"]
    },
    "rmb5":{
        "z":    [0x57,"z"]
    },
    "rmb6":{
        "z":    [0x67,"z"]
    },
    "rmb7":{
        "z":    [0x77,"z"]
    },
    "cmb0":{
        "z":    [0x07,"z"]
    },
    "cmb1":{
        "z":    [0x17,"z"]
    },
    "cmb2":{
        "z":    [0x27,"z"]
    },
    "cmb3":{
        "z":    [0x37,"z"]
    },
    "cmb4":{
        "z":    [0x47,"z"]
    },
    "cmb5":{
        "z":    [0x57,"z"]
    },
    "cmb6":{
        "z":    [0x67,"z"]
    },
    "cmb7":{
        "z":    [0x77,"z"]
    },
    "smb0":{
        "z":    [0x87,"z"]
    },
    "smb1":{
        "z":    [0x97,"z"]
    },
    "smb2":{
        "z":    [0xA7,"z"]
    },
    "smb3":{
        "z":    [0xB7,"z"]
    },
    "smb4":{
        "z":    [0xC7,"z"]
    },
    "smb5":{
        "z":    [0xD7,"z"]
    },
    "smb6":{
        "z":    [0xE7,"z"]
    },
    "smb7":{
        "z":    [0xF7,"z"]
    }
})

# Instructios with additional address modes
opcodes["adc"].update({
    "(z)":  [0x72,"z"]
})
opcodes["and"].update({
    "(z)":  [0x32,"z"],
})
opcodes["bit"].update({
    "a+x":  [0x3C,"al","ah"],
    "#":    [0x89,"#"],
    "z+x":  [0x34,"z"],
})
opcodes["cmp"].update({
    "(z)":  [0xD2,"z"],
})
opcodes["dec"].update({
    "(z)":  [0xD2,"z"],
    "A":    [0x3A],
})
opcodes["eor"].update({
    "(z)":  [0x52,"z"],
})
opcodes["xor"].update({
    "(z)":  [0x52,"z"],
})
opcodes["inc"].update({
    "A":    [0x1A],
    "i":    [0x1A],
})
opcodes["jmp"].update({
    "(a+x)":    [0x7C,"al","ah"],
})
opcodes["lda"].update({
    "(z)":  [0xB2,"z"],
})
opcodes["ora"].update({
    "(z)":  [0x12,"z"],
})
opcodes["psh"].update({
    "X":    [0xDA],
    "Y":    [0x5A],
})
opcodes["pul"].update({
    "X":    [0xFA],
    "Y":    [0x7A],
})
opcodes["sbc"].update({
    "(z)":  [0xF2,"z"],
})
opcodes["sta"].update({
    "(z)":  [0x92,"z"],
})