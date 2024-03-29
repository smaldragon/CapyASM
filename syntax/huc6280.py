"""
Hudson C6820 (pc-engine)
"""
from syntax.wdc65c02 import *

macro = """
    .val MPR0        %0000_0001
    .val MPR1        %0000_0010
    .val MPR2        %0000_0100
    .val MPR3        %0000_1000
    .val MPR4        %0001_0000
    .val MPR5        %0010_0000
    .val MPR6        %0100_0000
    .val MPR7        %1000_0000
"""

opcodes.update({
    # New HUC6280 Instructions
    "clr":{
        "A":    [0x62],
        "X":    [0x82],
        "Y":    [0xC2],
    },
    "cla":{
        "i":    [0x62]
    },
    "clx":{
        "i":    [0x82]
    },
    "cly":{
        "i":    [0xC2]
    },
    "csh":{
        "i":    [0xD4]
    },
    "csl":{
        "i":    [0x54]
    },
    "sax":{
        "i":    [0x22]
    },
    "say":{
        "i":    [0x42]
    },
    "sxy":{
        "i":    [0x02]
    },
    "set":{
        "i":    [0xF4]
    },
    "st0":{
        "#":    [0x03,"#"]
    },
    "st1":{
        "#":    [0x13,"#"]
    },
    "st2":{
        "#":    [0x23,"#"]
    },
    "tam":{
        "#":    [0x53,"#"]
    },
    "tma":{
        "#":    [0x43,"#"]
    },
    # Block Moves
    "tia":{
        "bmv":  [0xE3,"al","ah","al","ah","al","ah"]
    },
    "tdd":{
        "bmv":  [0xC3,"al","ah","al","ah","al","ah"]
    },
    "tin":{
        "bmv":  [0xD3,"al","ah","al","ah","al","ah"]
    },
    "tii":{
        "bmv":  [0x73,"al","ah","al","ah","al","ah"]
    },
})