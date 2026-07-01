"""
MOS 6510
"""

macro = """
    .val ZERO_PAGE   $00
    .val STACK       $100

    .val VECTORS     $FFFA
    .val VECTOR_NMI  $FFFA
    .val VECTOR_RST  $FFFC
    .val VECTOR_IRQ  $FFFE
    .val VECTOR_BRK  $FFFE
"""
extension = ".65x"
registers = ["A","X","Y","P","C","D","I","V"]
addr_tokens = ["<",">","(",")","[","]","+X","+Y","#",'+']

opcodes = {
    # opcodes
    "adc":{
        "a":    [0x6D,"al","ah"],
        "a+x":  [0x7D,"al","ah"],
        "a+y":  [0x79,"al","ah"],
        "#":    [0x69,"#"],
        "z":    [0x65,"z"],
        "(z+x)":[0x61,"z"],
        "z+x":  [0x75,"z"],
        "(z)+y":[0x71,"z"],
    },
    "add":{
        "a":    [0x18,0x6D,"al","ah"],
        "a+x":  [0x18,0x7D,"al","ah"],
        "a+y":  [0x18,0x79,"al","ah"],
        "#":    [0x18,0x69,"#"],
        "z":    [0x18,0x65,"z"],
        "(z+x)":[0x18,0x61,"z"],
        "z+x":  [0x18,0x75,"z"],
        "(z)+y":[0x18,0x71,"z"],
    },
    "and":{
        "a":    [0x2D,"al","ah"],
        "a+x":  [0x3D,"al","ah"],
        "a+y":  [0x39,"al","ah"],
        "#":    [0x29,"#"],
        "z":    [0x25,"z"],
        "(z+x)":[0x21,"z"],
        "z+x":  [0x35,"z"],
        "(z)+y":[0x31,"z"],
    },
    "asl":{
        "a":    [0x0E,"al","ah"],
        "a+x":  [0x1E,"al","ah"],
        "A":    [0x0A],
        "i":    [0x0A],
        "z":    [0x06,"z"],
        "z+x":  [0x16,"z"],
    },
    "bit":{
        "a":    [0x2C,"al","ah"],
        "z":    [0x24,"z"],
    },
    
    # BCC + ALIAS
    "bcc":{
        "r":    [0x90,"r"],
        "#":    [0x90,"#"]
    },"bcc:l":{
        "a":    [0xB0,0x03,0x4C,"al","ah"]
    }, "blt":{
        "r":    [0x90,"r"],
        "#":    [0x90,"#"]
    },"blt:l":{
        "a":    [0xB0,0x03,0x4C,"al","ah"]
    },
    
    # BCS + ALIAS
    "bcs":{
        "r":    [0xB0,"r"],
        "#":    [0xB0,"#"]
    },"bcs:l":{
        "a":    [0x90,0x03,0x4C,"al","ah"]
    }, "bge":{
        "r":    [0xB0,"r"],
        "#":    [0xB0,"#"]
    },"bge:l":{
        "a":    [0x90,0x03,0x4C,"al","ah"]
    },
    
    # BNE + ALIAS
    "bne":{
        "r":    [0xD0,"r"],
        "#":    [0xD0,"#"]
    },
    "bne:l":{
        "a":    [0xF0,0x03,0x4C,"al","ah"]
    },
    "bzc":{
        "r":    [0xD0,"r"],
        "#":    [0xD0,"#"]
    },
    "bzc:l":{
        "a":    [0xF0,0x03,0x4C,"al","ah"]
    },
    
    # BEQ + ALIAS
    "beq":{
        "r":    [0xF0,"r"],
        "#":    [0xF0,"#"]
    }, "bzs":{
        "r":    [0xF0,"r"],
        "#":    [0xF0,"#"]
    },
    
    "beq:l":{
        "a":    [0xD0,0x03,0x4C,"al","ah"],
    }, "bzs:l":{
        "a":    [0xD0,0x03,0x4C,"al","ah"],
    },
    
    # BPL + ALIAS
    "bpl":{
        "r":    [0x10,"r"],
        "#":    [0x10,"#"]
    }, "bnc":{
        "r":    [0x10,"r"],
        "#":    [0x10,"#"]
    },
    "bpl:l":{
        "a":    [0x30,0x03,0x4C,"al","ah"],
    }, "bnc:l":{
        "a":    [0x30,0x03,0x4C,"al","ah"],
    },
    
    # BMI + ALIAS
    "bmi":{
        "r":    [0x30,"r"],
        "#":    [0x30,"#"]
    }, "bns":{
        "r":    [0x30,"r"],
        "#":    [0x30,"#"]
    },
    "bmi:l":{
        "a":    [0x10,0x03,0x4C,"al","ah"],
    }, "bns:l":{
        "a":    [0x10,0x03,0x4C,"al","ah"],
    },
    
    
    "bvc":{
        "r":    [0x50,"r"],
        "#":    [0x50,"#"]
    },"bvc:l":{
        "a":    [0x70,0x03,0x4C,"al","ah"],
    },
    "bvs":{
        "r":    [0x70,"r"],
        "#":    [0x70,"#"]
    },"bvs:l":{
        "a":    [0x50,0x03,0x4C,"al","ah"],
    },
    
    
    "brk":{
        "i":    [0x00,0x00],
        "#":    [0x00,"#"]
    },
    "clr":{
        "C":    [0x18],
        "D":    [0xD8],
        "I":    [0x58],
        "V":    [0xB8],
    },
    "clc":{
        "i":    [0x18]
    },
    "cld":{
        "i":    [0xD8]
    },
    "cli":{
        "i":    [0x58]
    },
    "clv":{
        "i":    [0xB8]
    },
    "cmp":{
        "a":    [0xCD,"al","ah"],
        "a+x":  [0xDD,"al","ah"],
        "a+y":  [0xD9,"al","ah"],
        "#":    [0xC9,"#"],
        "z":    [0xC5,"z"],
        "(z+x)":[0xC1,"z"],
        "z+x":  [0xD5,"z"],
        "(z)+y":[0xD1,"z"]
    },
    "cpx":{
        "a":    [0xEC,"al","ah"],
        "#":    [0xE0,"#"],
        "z":    [0xE4,"z"]
    },
    "cpy":{
        "a":    [0xCC,"al","ah"],
        "#":    [0xC0,"#"],
        "z":    [0xC4,"z"]
    },
    "dec":{
        "a":    [0xCE,"al","ah"],
        "a+x":  [0xDE,"al","ah"],
        "X":    [0xCA],
        "Y":    [0x88],
        "z":    [0xC6,"z"],
        "z+x":  [0xD6,"z"],
    },
    "dex":{
        "i":    [0xCA],
    },
    "dex:w":{"i":    [0xCA,0xCA] },
    "dex:2":{"i":    [0xCA,0xCA,0xCA] },
    "dex:3":{"i":    [0xCA,0xCA,0xCA,0xCA] },
    "dex:4":{"i":    [0xCA,0xCA,0xCA,0xCA,0xCA] },
    "dex:5":{"i":    [0xCA,0xCA,0xCA,0xCA,0xCA,0xCA] },
    "dex:6":{"i":    [0xCA,0xCA,0xCA,0xCA,0xCA,0xCA,0xCA] },
    "dex:7":{"i":    [0xCA,0xCA,0xCA,0xCA,0xCA,0xCA,0xCA,0xCA] },
    "dex:8":{"i":    [0xCA,0xCA,0xCA,0xCA,0xCA,0xCA,0xCA,0xCA,0xCA] },
    
    "dey":{
        "i":    [0x88],
    },    
    "dey:w":{"i":    [0xCA,0x88] },
    "dey:2":{"i":    [0x88,0x88,0x88] },
    "dey:3":{"i":    [0x88,0x88,0x88,0x88] },
    "dey:4":{"i":    [0x88,0x88,0x88,0x88,0x88] },
    "dey:5":{"i":    [0x88,0x88,0x88,0x88,0x88,0x88] },
    "dey:6":{"i":    [0x88,0x88,0x88,0x88,0x88,0x88,0x88] },
    "dey:7":{"i":    [0x88,0x88,0x88,0x88,0x88,0x88,0x88,0x88] },
    "dey:8":{"i":    [0x88,0x88,0x88,0x88,0x88,0x88,0x88,0x88,0x88] },
    
    "eor":{
        "a":    [0x4D,"al","ah"],
        "a+x":  [0x5D,"al","ah"],
        "a+y":  [0x59,"al","ah"],
        "#":    [0x49,"#"],
        "z":    [0x45,"z"],
        "(z+x)":[0x41,"z"],
        "z+x":  [0x55,"z"],
        "(z)+y":[0x51,"z"],
    },
    "xor":{
        "a":    [0x4D,"al","ah"],
        "a+x":  [0x5D,"al","ah"],
        "a+y":  [0x59,"al","ah"],
        "#":    [0x49,"#"],
        "z":    [0x45,"z"],
        "(z+x)":[0x41,"z"],
        "z+x":  [0x55,"z"],
        "(z)+y":[0x51,"z"],
    },
    "inc":{
        "a":    [0xEE,"al","ah"],
        "a+x":  [0xFE,"al","ah"],
        "X":    [0xE8],
        "Y":    [0xC8],
        "z":    [0xE6,"z"],
        "z+x":  [0xF6,"z"],
    },
    "inx":{
        "i":    [0xE8]
    },
    "inx:w":{"i":    [0xE8,0xE8]},
    "inx:2":{"i":    [0xE8,0xE8]},
    "inx:3":{"i":    [0xE8,0xE8,0xE8]},
    "inx:4":{"i":    [0xE8,0xE8,0xE8,0xE8]},
    "inx:5":{"i":    [0xE8,0xE8,0xE8,0xE8,0xE8]},
    "inx:6":{"i":    [0xE8,0xE8,0xE8,0xE8,0xE8]},
    "inx:7":{"i":    [0xE8,0xE8,0xE8,0xE8,0xE8,0xE8]},
    "inx:8":{"i":    [0xE8,0xE8,0xE8,0xE8,0xE8,0xE8,0xE8]},
    
    "iny":{
        "i":    [0xC8]
    },
    "iny:w":{"i":    [0xC8,0xC8] },
    "iny:2":{"i":    [0xC8,0xC8] },
    "iny:3":{"i":    [0xC8,0xC8,0xC8] },
    "iny:4":{"i":    [0xC8,0xC8,0xC8,0xC8] },
    "iny:5":{"i":    [0xC8,0xC8,0xC8,0xC8,0xC8] },
    "iny:6":{"i":    [0xC8,0xC8,0xC8,0xC8,0xC8,0xC8] },
    "iny:7":{"i":    [0xC8,0xC8,0xC8,0xC8,0xC8,0xC8,0xC8] },
    "iny:8":{"i":    [0xC8,0xC8,0xC8,0xC8,0xC8,0xC8,0xC8,0xC8] },
    
    "jmp":{
        "a":    [0x4C,"al","ah"],
        "(a)":  [0x6C,"al","ah"],
    },
    "jsr":{
        "a":    [0x20,"al","ah"]
    },
    "lda":{
        "a":    [0xAD,"al","ah"],
        "a+x":  [0xBD,"al","ah"],
        "a+y":  [0xB9,"al","ah"],
        "#":    [0xA9,"#"],
        "z":    [0xA5,"z"],
        "(z+x)":[0xA1,"z"],
        "z+x":  [0xB5,"z"],
        "(z)+y":[0xB1,"z"]
    },
    "ldx":{
        "a":    [0xAE,"al","ah"],
        "a+y":  [0xBE,"al","ah"],
        "#":    [0xA2,"#"],
        "z":    [0xA6,"z"],
        "z+y":  [0xB6,"z"],
    },"ldy":{
        "a":    [0xAC,"al","ah"],
        "a+x":  [0xBC,"al","ah"],
        "#":    [0xA0,"#"],
        "z":    [0xA4,"z"],
        "z+x":  [0xB4,"z"],
    },
    "lsr":{
        "a":    [0x4E,"al","ah"],
        "a+x":  [0x5E,"al","ah"],
        "A":    [0x4A],
        "i":    [0x4A],
        "z":    [0x46,"z"],
        "z+x":  [0x56,"z"],
    },
    "nop":{
        "i":    [0xEA]
    },
    "ora":{
        "a":    [0x0D,"al","ah"],
        "a+x":  [0x1D,"al","ah"],
        "a+y":  [0x19,"al","ah"],
        "#":    [0x09,"#"],
        "z":    [0x05,"z"],
        "(z+x)":[0x01,"z"],
        "z+x":  [0x15,"z"],
        "(z)+y":[0x11,"z"],
    },
    "psh":{
        "A":    [0x48],
        "P":    [0x08],
    },
    "pha":{
        "i":    [0x48]
    },
    "php":{
        "i":    [0x08]
    },
    "pul":{
        "A":    [0x68],
        "P":    [0x28],
    },
    "pla":{
        "i":    [0x68]
    },
    "plp":{
        "i":    [0x28]
    },
    "rol":{
        "a":    [0x2E,"al","ah"],
        "a+x":  [0x3E,"al","ah"],
        "A":    [0x2A],
        "i":    [0x2A],
        "z":    [0x26,"z"],
        "z+x":  [0x36,"z"]
    },
    "ror":{
        "a":    [0x6E,"al","ah"],
        "a+x":  [0x7E,"al","ah"],
        "A":    [0x6A],
        "i":    [0x6A],
        "z":    [0x66,"z"],
        "z+x":  [0x76,"z"]
    },
    "rti":{
        "i":    [0x40]
    },
    "rts":{
        "i":    [0x60]
    },
    "sbc":{
        "a":    [0xED,"al","ah"],
        "a+x":  [0xFD,"al","ah"],
        "a+y":  [0xF9,"al","ah"],
        "#":    [0xE9,"#"],
        "z":    [0xE5,"z"],
        "(z+x)":[0xE1,"z"],
        "z+x":  [0xF5,"z"],
        "(z)+y":[0xF1,"z"],
    },
    "sub":{
        "a":    [0x38,0xED,"al","ah"],
        "a+x":  [0x38,0xFD,"al","ah"],
        "a+y":  [0x38,0xF9,"al","ah"],
        "#":    [0x38,0xE9,"#"],
        "z":    [0x38,0xE5,"z"],
        "(z+x)":[0x38,0xE1,"z"],
        "z+x":  [0x38,0xF5,"z"],
        "(z)+y":[0x38,0xF1,"z"],
    },
    "set":{
        "C":    [0x38],
        "D":    [0xF8],
        "I":    [0x78],
    },
    "sec":{
        "i":    [0x38]
    },
    "sed":{
        "i":    [0xF8]
    },
    "sei":{
        "i":    [0x78]
    },
    "sta":{
        "a":    [0x8D,"al","ah"],
        "a+x":  [0x9D,"al","ah"],
        "a+y":  [0x99,"al","ah"],
        "z":    [0x85,"z"],
        "(z+x)":[0x81,"z"],
        "z+x":  [0x95,"z"],
        "(z)+y":[0x91,"z"]
    },
    "stx":{
        "a":    [0x8E,"al","ah"],
        "z":    [0x86,"z"],
        "z+y":  [0x96,"z"],
    },
    "sty":{
        "a":    [0x8C,"al","ah"],
        "z":    [0x84,"z"],
        "z+x":  [0x94,"z"],
    },
    "tax":{
        "i":    [0xAA]
    },
    "txa":{
        "i":    [0x8A]
    },
    "tay":{
        "i":    [0xA8]
    },
    "tya":{
        "i":    [0x98]
    },
    "tsx":{
        "i":    [0xBA]
    },
    "txs":{
        "i":    [0x9A]
    },
}
