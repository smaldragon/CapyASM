from . import mos6502
from . import wdc65c02
from . import wdc65816
from . import huc6280
from . import rp2a03

def get(cpu):
    if cpu.lower() in ("2a03","2a07"):
        return rp2a03.macro,rp2a03.opcodes
    elif cpu.lower() in ("mos6502","6502"):
        return mos6502.macro,mos6502.opcodes
    elif cpu.lower() in ("wdc65c02","65c02"):
        return wdc65c02.macro,wdc65c02.opcodes
    #elif cpu.lower() in ("wdc65816","65816"):
    #    return wdc65816.macro,wdc65816.opcodes
    elif cpu.lower() in ("huc6280","c6280","6280","pc-engine","pce","turbografx-16"):
        return huc6280.macro,huc6280.opcodes
    else:
        print(f'\033[91m'+f"@{i} ERROR: Unrecognized cpu: '{cpu}'")

value = "\$*%*\"*[^<>\[\]\(\)\+:#]+"

addr = {
    f"(?i)\[{value}\]$":"a",
    f"(?i)\[\[{value}\+x\]\]$":"(a+x)",
    f"(?i)\[{value}\+x\]$":"a+x",
    f"(?i)\[{value}\+y\]$":"a+y",
    f"(?i)\[\[{value}\]\]$":"(a)",
    f"(?i){value}$":"#",
    #"":"i",
    
    #"":"s",
    
    f"(?i)<{value}>:*\({value}\)":"zr",
    f"(?i)\({value}\)$":"r",
    f"(?i)<{value}>$":"z",
    f"(?i)\[<{value}\+x>\]$":"(z+x)",
    f"(?i)<{value}\+x>$":"z+x",
    f"(?i)<{value}\+y>$":"z+y",
    f"(?i)\[<{value}>\]$":"(z)",
    f"(?i)\[<{value}>\+y\]$":"(z)+y",

    "(?i)A":"A",
    "(?i)X":"X",
    "(?i)Y":"Y",
    "(?i)P":"P",
    "(?i)C":"C",
    "(?i)D":"D",
    "(?i)I":"I",
    "(?i)V":"V",

    # HuC6820
    f"(?i)\[{value}\]:\[{value}\]:#{value}":"bmv",
    # w65816
    f"(?i)\(#{value}\)$":"rl",
    f"(?i){{{value}}}:{{{value}}}$":"xyc",
    f"(?i)\[#{value}\]$":"al",
    f"(?i)\[#\[{value}\]\]$":"[a]",
    f"(?i)\[#<{value}>\]$":"[d]",
    f"(?i)\[#<{value}>\+y\]$":"[d]+y",
}

modes = {
    "":"i",
    "[i]":"a",
    "[[i+X]]":"(a+x)",
    "[i+X]":"a+x",
    "[i+Y]":"a+y",
    "[[i]]":"(a)",
    "i":"#",
    
    "<i>(i)":"zr",
    "(i)":"r",
    "<i>":"z",
    "[<i+X>]":"(z+x)",
    "[#<i+X>]":"(z+x)",
    "<i+X>":"z+x",
    "<i+Y>":"z+y",
    "[<i>]":"(z)",
    "[#<i>]":"(z)",
    "[<i>+Y]":"(z)+y",
    "[#<i>+Y]":"(z)+y",
    
    # Registers
    "A":"A",
    "X":"X",
    "Y":"Y",
    "P":"P",
    "C":"C",
    "D":"D",
    "I":"I",
    "V":"V",
    
    # HuC6820
    "[i][i]#i":"bmv",
}

opcodes = {
    # special
    "org":{
        "a":[]
    },
    "pad":{
        "a":[],
        "#":[]
    },
    "var":{
        "#" : []
    },
    "byte":{
        "#" : ["*"]
    },
    "word":{
        "#" : ["**"]
    },
    "asm":{
        "#" : []
    },
    "bin":{
        "#" : []
    },
    "macro":{
        "#":  []
    },
    "cpu":{
        "#": []
    }
}
