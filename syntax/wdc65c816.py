# Western Design Center 65c816
from syntax.wdc65c02 import *
registers.append("S")
addr_tokens.append("+S")
macro += """
    .val VECTORSn  $FFE4
    .val VECTORSe  $FFF4
    
    .val pN %1000_0000
    .val pV %0100_0000
    .val pM %0010_0000
    .val pX %0001_0000
    .val pD %0000_1000
    .val pI %0000_0100
    .val pZ %0000_0010
    .val pC %0000_0001
"""
opcodes.update({
    # opcodes
    "cop":{
        "i":    [0x02,0x00],
        "#":    [0x02,"#"]
    },
    "wdm":{
        "i":    [0x42,0x00],
        "#":    [0x42,"#"]
    },
    
    # A
    "ora:l": {
        "a":    [0x0F,"al","ah+","bk"],
        "a+x":  [0x1F,"al","ah+","bk"],
        "(z)":  [0x07,"z"],
        "(z)+y":[0x17,"z"],
    },
    "and:l": {
        "a":    [0x2F,"al","ah+","bk"],
        "a+x":  [0x3F,"al","ah+","bk"],
        "(z)":  [0x27,"z"],
        "(z)+y":[0x37,"z"],
    },
    "eor:l": {
        "a":    [0x4F,"al","ah+","bk"],
        "a+x":  [0x5F,"al","ah+","bk"],
        "(z)":  [0x47,"z"],
        "(z)+y":[0x57,"z"],
    },
    "xor:l": {
        "a":    [0x4F,"al","ah+","bk"],
        "a+x":  [0x5F,"al","ah+","bk"],
        "(z)":  [0x47,"z"],
        "(z)+y":[0x57,"z"],
    },
    "adc:l": {
        "a":    [0x6F,"al","ah+","bk"],
        "a+x":  [0x7F,"al","ah+","bk"],
        "(z)":  [0x67,"z"],
        "(z)+y":[0x77,"z"],
    },
    "add:l": {
        "a":    [0x18,0x6F,"al","ah+","bk"],
        "a+x":  [0x18,0x7F,"al","ah+","bk"],
        "(z)":  [0x18,0x67,"z"],
        "(z)+y":[0x18,0x77,"z"],
    },
    "sta:l": {
        "a":    [0x8F,"al","ah+","bk"],
        "a+x":  [0x9F,"al","ah+","bk"],
        "(z)":  [0x87,"z"],
        "(z)+y":[0x97,"z"],
    },
    "lda:l": {
        "a":    [0xAF,"al","ah+","bk"],
        "a+x":  [0xBF,"al","ah+","bk"],
        "(z)":  [0xA7,"z"],
        "(z)+y":[0xB7,"z"],
    },
    "cmp:l": {
        "a":    [0xCF,"al","ah+","bk"],
        "a+x":  [0xDF,"al","ah+","bk"],
        "(z)":  [0xC7,"z"],
        "(z)+y":[0xD7,"z"],
    },
    "sbc:l": {
        "a":    [0xEF,"al","ah+","bk"],
        "a+x":  [0xFF,"al","ah+","bk"],
        "(z)":  [0xE7,"z"],
        "(z)+y":[0xF7,"z"],
    },
    "sub:l": {
        "a":    [0x38,0xEF,"al","ah+","bk"],
        "a+x":  [0x38,0xFF,"al","ah+","bk"],
        "(z)":  [0x38,0xE7,"z"],
        "(z)+y":[0x38,0xF7,"z"],
    },
    
    "brl":{
        "r":    [0x82,"rl","rh"],
        "##":   [0x82,"#l","#h"],
    },
    "bra:l":{
        "r":    [0x82,"rl","rh"],
        "##":   [0x82,"#l","#h"],
    },
    "mvn":{
        "##":   [0x54,"#","#"],
        "i":    [0x54,0x00,0x000],
    },
    "mvp":{
        "##":   [0x44,"#","#"],
        "i":    [0x44,0x00,0x00],
    },
    
    "jml":{
        "a":    [0x5C,"al","ah+","bk"],
    },
    "jsl":{
        "a":    [0x22,"al","ah+","bk"],
    },
    "rtl":{
        "i":    [0x6B],  
    },
    
    "pea"  :{
        "a":    [0xF4,"al","ah"],
        "#":   [0xF4,"#l","#h"],
    },
    "pei"  :{
        "z":    [0xD4,"z"],
    },
    "per"  :{
        "r":    [0x62,"rl","rh"],
        "#":    [0x62,"#l","#h"],
    },

    "psh:w"  :{
        "#":    [0xF4,"al","ah"],
        "z":    [0xD4,"z"],
        "r":    [0x62,"rl","rh"],
    },
    
    "ora:w":{   "#":    [0x09,"#l","#h"]    },
    "ora:b":{   "#":    [0x09,"#"]      },
    
    "and:w":{   "#":    [0x29,"#l","#h"]    },
    "and:b":{   "#":    [0x29,"#"]      },
    
    "eor:w":{   "#":    [0x49,"#l","#h"]    },
    "xor:w":{   "#":    [0x49,"#l","#h"]    },
    "eor:b":{   "#":    [0x49,"#"]    },
    "xor:b":{   "#":    [0x49,"#"]    },
    
    "adc:w":{   "#":    [0x69,"#l","#h"]    },
    "add:w":{   "#":    [0x18,0x69,"#l","#h"]    },
    "adc:b":{   "#":    [0x69,"#l"]    },
    "add:b":{   "#":    [0x18,0x69,"#"]    },
    
    "bit:w":{   "#":    [0x89,"#l","#h"]    },
    "bit:b":{   "#":    [0x89,"#"]    },
    
    "lda:w":{   "#":    [0xA9,"#l","#h"]    },
    "lda:b":{   "#":    [0xA9,"#"]    },
    
    "cmp:w":{   "#":    [0xC9,"#l","#h"]    },
    "cmp:b":{   "#":    [0xC9,"#"]    },
    
    "sbc:w":{   "#":    [0xE9,"#l","#h"]    },
    "sub:w":{   "#":    [0x38,0xE9,"#l","#h"]    },
    "sbc:b":{   "#":    [0xE9,"#"]    },
    "sub:b":{   "#":    [0x38,0xE9,"#"]    },
    
    "ldy:w":{   "#":    [0xA0,"#l","#h"]    },
    "ldy:b":{   "#":    [0xA0,"#"]    },
    
    "ldx:w":{   "#":    [0xA2,"#l","#h"]    },
    "ldx:b":{   "#":    [0xA2,"#"]    },
    
    "cpy:w":{   "#":    [0xC0,"#l","#h"]    },
    "cpy:b":{   "#":    [0xC0,"#"]    },
    
    "cpx:w":{   "#":    [0xE0,"#l","#h"]    },
    "cpx:b":{   "#":    [0xE0,"#"]    },
    
    "rep"  :{   "#":    [0xC2,"#"]    },
    "clp"  :{   "#":    [0xC2,"#"]    },
    "sep"  :{   "#":    [0xE2,"#"]    },
    
    # REP/SEP Macros
    "M16"   :{   "i":    [0xC2,0x20]},
    "X16"   :{   "i":    [0xC2,0x10]},
    "M16X16":{   "i":    [0xC2,0x30]},
    
    "M8"   :{   "i":    [0xE2,0x20]},
    "X8"   :{   "i":    [0xE2,0x10]},
    "M8X8" :{   "i":    [0xE2,0x30]},
    
    "M8X16":{   "i":    [0xE2,0x20,0xC2,0x10]},
    "M16X8":{   "i":    [0xC2,0x20,0xE2,0x10]},
    
    "sev"  :{   "i":    [0xE2,0x40] },
    "sen"  :{   "i":    [0xE2,0x80] },
    "cln"  :{   "i":    [0xC2,0x80] },
    "sez"  :{   "i":    [0xE2,0x02] },
    "clz"  :{   "i":    [0xC2,0x02] },
    
    # New Transfer Instructions
    "tcd"  :{   "i":    [0x5B]  },  "tad"  :{   "i":    [0x5B]  },
    "tcs"  :{   "i":    [0x1B]  },  "tas"  :{   "i":    [0x1B]  },
    "tdc"  :{   "i":    [0x7B]  },  "tda"  :{   "i":    [0x7B]  },
    "tsc"  :{   "i":    [0x3B]  },  "tsa"  :{   "i":    [0x3B]  },
    "txy"  :{   "i":    [0x9B]  },
    "tyx"  :{   "i":    [0xBB]  },
    
    "phb"  :{   "i":    [0x8B]  },
    "phd"  :{   "i":    [0x0B]  },
    "phk"  :{   "i":    [0x4B]  },
    "plb"  :{   "i":    [0xAB]  },
    "pld"  :{   "i":    [0x2B]  },
    
    "xce"  :{   "i":    [0xFB]  },
    "xba"  :{   "i":    [0xEB]  },  "swa"  :{   "i":    [0xEB]  },
    
})

# Stack Relative Modes
opcodes["ora"].update({"z+s":    [0x03,"z"],"(z+s)+y":[0x13,"z"]})
opcodes["and"].update({"z+s":    [0x23,"z"],"(z+s)+y":[0x33,"z"]})
opcodes["eor"].update({"z+s":    [0x43,"z"],"(z+s)+y":[0x53,"z"]})
opcodes["xor"].update({"z+s":    [0x43,"z"],"(z+s)+y":[0x53,"z"]})
opcodes["adc"].update({"z+s":    [0x63,"z"],"(z+s)+y":[0x73,"z"]})
opcodes["add"].update({"z+s":    [0x18,0x63,"z"],"(z+s)+y":[0x18,0x73,"z"]})
opcodes["sta"].update({"z+s":    [0x83,"z"],"(z+s)+y":[0x93,"z"]})
opcodes["lda"].update({"z+s":    [0xA3,"z"],"(z+s)+y":[0xB3,"z"]})
opcodes["cmp"].update({"z+s":    [0xC3,"z"],"(z+s)+y":[0xD3,"z"]})
opcodes["sbc"].update({"z+s":    [0xE3,"z"],"(z+s)+y":[0xF3,"z"]})
opcodes["sub"].update({"z+s":    [0x38,0xE3,"z"],"(z+s)+y":[0x38,0xF3,"z"]})

#"r":    [0x82,"rl","rh"],
opcodes["bcc:l"].update({   "r":    [0xB0,0x03,0x82,"rl","rh"]    })
opcodes["blt:l"].update({   "r":    [0xB0,0x03,0x82,"rl","rh"]    })
opcodes["bcs:l"].update({   "r":    [0x90,0x03,0x82,"rl","rh"]    })
opcodes["bge:l"].update({   "r":    [0x90,0x03,0x82,"rl","rh"]    })

opcodes["bne:l"].update({   "r":    [0xF0,0x03,0x82,"rl","rh"]    })
opcodes["bzc:l"].update({   "r":    [0xF0,0x03,0x82,"rl","rh"]    })
opcodes["beq:l"].update({   "r":    [0xD0,0x03,0x82,"rl","rh"]    })
opcodes["bzs:l"].update({   "r":    [0xD0,0x03,0x82,"rl","rh"]    })

opcodes["bpl:l"].update({   "r":    [0x30,0x03,0x82,"rl","rh"]    })
opcodes["bnc:l"].update({   "r":    [0x30,0x03,0x82,"rl","rh"]    })
opcodes["bmi:l"].update({   "r":    [0x10,0x03,0x82,"rl","rh"]    })
opcodes["bns:l"].update({   "r":    [0x10,0x03,0x82,"rl","rh"]    })

opcodes["bvc:l"].update({   "r":    [0x70,0x03,0x82,"rl","rh"]    })
opcodes["bvs:l"].update({   "r":    [0x50,0x03,0x82,"rl","rh"]    })

opcodes["clr"].update({   "#":      [0x90,0x03,0x82,"rl","rh"]    })
opcodes["set"].update({   "#":      [0x90,0x03,0x82,"rl","rh"]    })

opcodes["jsr"].update({
    "(a+x)":    [0xFC,"al","ah"],
})

opcodes["lda:w"] = {**opcodes["lda"],**opcodes["lda:w"]}
opcodes["lda:b"] = {**opcodes["lda"],**opcodes["lda:b"]}
opcodes["ldx:w"] = {**opcodes["ldx"],**opcodes["ldx:w"]}
opcodes["ldx:b"] = {**opcodes["ldx"],**opcodes["ldx:b"]}
opcodes["ldy:w"] = {**opcodes["ldy"],**opcodes["ldy:w"]}
opcodes["ldy:b"] = {**opcodes["ldy"],**opcodes["ldy:b"]}

opcodes["sta:w"] = opcodes["sta"]
opcodes["sta:b"] = opcodes["sta"]
opcodes["stx:w"] = opcodes["stx"]
opcodes["stx:b"] = opcodes["stx"]
opcodes["sty:w"] = opcodes["sty"]
opcodes["sty:b"] = opcodes["sty"]
opcodes["stz:w"] = opcodes["stz"]
opcodes["stz:b"] = opcodes["stz"]

opcodes["adc:w"] = {**opcodes["adc"],**opcodes["adc:w"]}
opcodes["adc:b"] = {**opcodes["adc"],**opcodes["adc:b"]}
opcodes["add:w"] = {**opcodes["add"],**opcodes["add:w"]}
opcodes["add:b"] = {**opcodes["add"],**opcodes["add:b"]}
opcodes["sbc:w"] = {**opcodes["sbc"],**opcodes["sbc:w"]}
opcodes["sbc:b"] = {**opcodes["sbc"],**opcodes["sbc:b"]}
opcodes["sub:w"] = {**opcodes["sub"],**opcodes["sub:w"]}
opcodes["sub:b"] = {**opcodes["sub"],**opcodes["sub:b"]}

opcodes["cmp:w"] = {**opcodes["cmp"],**opcodes["cmp:w"]}
opcodes["cmp:b"] = {**opcodes["cmp"],**opcodes["cmp:b"]}
opcodes["cpx:w"] = {**opcodes["cpx"],**opcodes["cpx:w"]}
opcodes["cpx:b"] = {**opcodes["cpx"],**opcodes["cpx:b"]}
opcodes["cpy:w"] = {**opcodes["cpy"],**opcodes["cpy:w"]}
opcodes["cpy:b"] = {**opcodes["cpy"],**opcodes["cpy:b"]}

opcodes["and:w"] = {**opcodes["and"],**opcodes["and:w"]}
opcodes["and:b"] = {**opcodes["and"],**opcodes["and:b"]}
opcodes["eor:w"] = {**opcodes["eor"],**opcodes["eor:w"]}
opcodes["eor:b"] = {**opcodes["eor"],**opcodes["eor:b"]}
opcodes["xor:w"] = {**opcodes["xor"],**opcodes["xor:w"]}
opcodes["xor:b"] = {**opcodes["xor"],**opcodes["xor:b"]}
opcodes["ora:w"] = {**opcodes["ora"],**opcodes["ora:w"]}
opcodes["ora:b"] = {**opcodes["ora"],**opcodes["ora:b"]}

opcodes["bit:w"] = {**opcodes["bit"],**opcodes["bit:w"]}
opcodes["bit:b"] = {**opcodes["bit"],**opcodes["bit:b"]}



opcodes["asl:w"] = opcodes["asl"]
opcodes["asl:b"] = opcodes["asl"]
opcodes["lsr:w"] = opcodes["lsr"]
opcodes["lsr:b"] = opcodes["lsr"]
opcodes["rol:w"] = opcodes["rol"]
opcodes["rol:b"] = opcodes["rol"]
opcodes["ror:w"] = opcodes["ror"]
opcodes["ror:b"] = opcodes["ror"]
opcodes["inc:w"] = opcodes["inc"]
opcodes["inc:b"] = opcodes["inc"]
opcodes["dec:w"] = opcodes["dec"]
opcodes["dec:b"] = opcodes["dec"]



opcodes["tsb:w"] = opcodes["tsb"]
opcodes["tsb:b"] = opcodes["tsb"]
opcodes["trb:w"] = opcodes["trb"]
opcodes["trb:b"] = opcodes["trb"]
