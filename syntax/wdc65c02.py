# Western Design Center 65c02

macro = """
    var ZERO_PAGE $00
    var STACK     $100

    var VECTORS     $FFFA
    var VECTOR_NMI  $FFFA
    var VECTOR_RST  $FFFC
    var VECTOR_IRQ  $FFFE
    var VECTOR_BRK  $FFFE
"""

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
        "(z)":  [0x72,"z"],
        "(z)+y":[0x71,"z"],
    },
    "and":{
        "a":    [0x2D,"al","ah"],
        "a+x":  [0x3D,"al","ah"],
        "a+y":  [0x39,"al","ah"],
        "#":    [0x29,"#"],
        "z":    [0x25,"z"],
        "(z+x)":[0x21,"z"],
        "z+x":  [0x35,"z"],
        "(z)":  [0x32,"z"],
        "(z)+y":[0x31,"z"],
    },
    "asl":{
        "a":    [0x0E,"al","ah"],
        "a+x":  [0x1E,"al","ah"],
        "A":    [0x0A],
        "z":    [0x06,"z"],
        "z+x":  [0x16,"z"],
    },
    "bit":{
        "a":    [0x2C,"al","ah"],
        "a+x":  [0x3C,"al","ah"],
        "#":    [0x89,"#"],
        "z":    [0x24,"z"],
        "z+x":  [0x34,"z"],
    },
    "bcc":{
        "r":    [0x90,"r"]
    },
    "bcs":{
        "r":    [0xB0,"r"]
    },
    "bne":{
        "r":    [0xD0,"r"]
    },
    "beq":{
        "r":    [0xF0,"r"]
    },
    "bzc":{
        "r":    [0xD0,"r"]
    },
    "bzs":{
        "r":    [0xF0,"r"]
    },
    "bpl":{
        "r":    [0x10,"r"]
    },
    "bmi":{
        "r":    [0x30,"r"]
    },
    "bnc":{
        "r":    [0x10,"r"]
    },
    "bns":{
        "r":    [0x30,"r"]
    },
    "bvc":{
        "r":    [0x50,"r"]
    },
    "bvs":{
        "r":    [0x70,"r"]
    },
    "bra":{
        "r":    [0x80,"r"]
    },
    "brk":{
        "i":    [0x00]
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
        "(z)":  [0xD2,"z"],
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
        "A":    [0x3A],
        "X":    [0xCA],
        "Y":    [0x88],
        "z":    [0xC6,"z"],
        "z+x":  [0xD6,"z"],
        "i":    [0x3A]
    },
    "dex":{
        "i":    [0xCA],
    },
    "dey":{
        "i":    [0x88],
    },
    "eor":{
        "a":    [0x4D,"al","ah"],
        "a+x":  [0x5D,"al","ah"],
        "a+y":  [0x59,"al","ah"],
        "#":    [0x49,"#"],
        "z":    [0x45,"z"],
        "(z+x)":[0x41,"z"],
        "z+x":  [0x55,"z"],
        "(z)":  [0x52,"z"],
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
        "(z)":  [0x52,"z"],
        "(z)+y":[0x51,"z"],
    },
    "inc":{
        "a":    [0xEE,"al","ah"],
        "a+x":  [0xFE,"al","ah"],
        "A":    [0x1A],
        "X":    [0xE8],
        "Y":    [0xC8],
        "z":    [0xE6,"z"],
        "z+x":  [0xF6,"z"],
        "i":    [0x1A]
    },
    "inx":{
        "i":    [0xE8]
    },
    "iny":{
        "i":    [0xC8]
    },
    "jmp":{
        "a":    [0x4C,"al","ah"],
        "(a+x)":[0x7C,"al","ah"],
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
        "(z)":  [0xB2,"z"],
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
        "(z)":  [0x12,"z"],
        "(z)+y":[0x11,"z"],
    },
    "psh":{
        "A":    [0x48],
        "P":    [0x08],
        "X":    [0xDA],
        "Z":    [0x5A],
    },
    "pha":{
        "i":    [0x48]
    },
    "php":{
        "i":    [0x08]
    },
    "phx":{
        "i":    [0xDA]
    },
    "phy":{
        "i":    [0x5A]
    },
    "pul":{
        "A":    [0x68],
        "P":    [0x28],
        "X":    [0xFA],
        "Y":    [0x7A],
    },
    "pha":{
        "i":    [0x68]
    },
    "php":{
        "i":    [0x28]
    },
    "phx":{
        "i":    [0xFA]
    },
    "phy":{
        "i":    [0x7A]
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
        "(z)":  [0xF2,"z"],
        "(z)+y":[0xF1,"z"],
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
        "(z)":  [0x92,"z"],
        "(z)+y":[0x91,"z"]
    },
    "stp":{
        "i":    [0xDB]
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
    "stz":{
        "a":    [0x9C,"al","ah"],
        "a+x":  [0x9E,"al","ah"],
        "z":    [0x64,"z"],
        "z+x":  [0x74,"z"],
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
    "wai":{
        "i":    [0xCB]
    },
    # 65c02 bbr/bbs
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
}