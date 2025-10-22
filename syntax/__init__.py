import logging

from . import mos6502
from . import wdc65c02
from . import wdc65816
from . import huc6280
from . import rp2a03
from . import mos6510
from . import kitty
from . import subleq8
def get(cpu):
    config = None
    if cpu.lower() in ("rc2a03","rc2a07","2a03","2a07"):
        config = rp2a03
    elif cpu.lower() in ("mos6502"):
        config = mos6502
    elif cpu.lower() in ("mos6510"):
        config = mos6510
    elif cpu.lower() in ("wdc65c02","65c02"):
        config = wdc65c02
    #elif cpu.lower() in ("wdc65816","65816"):
    #    return wdc65816.macro,wdc65816.opcodes
    elif cpu.lower() in ("huc6280","c6280","6280","pc-engine","pce","turbografx-16"):
        config = huc6280
    elif cpu.lower() == "kitty":
        config = kitty
    elif cpu.lower() == "subleq8":
        config = subleq8
    
    if config:
        return config.macro, config.opcodes, config.registers, config.extension, config.addr_tokens
    else:
        logging.error(f'Unrecognized cpu')

value = "\$*%*\"*[^<>\[\]\(\)\+:#]+"

addr = {
    f"(?i)\[\[{value}\]\]$":"(a)",
    f"(?i)\[{value}\]$":"a",
    f"(?i)\[\[{value}\+x\]\]$":"(a+x)",
    f"(?i)\[{value}\+x\]$":"a+x",
    f"(?i)\[{value}\+y\]$":"a+y",
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
    
    f"(?i){value}:{value}:{value}":"###",
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
    
    "iii":"###",
    "ii":"##",
    
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
    "[i][i]@i":"bmv",
}

opcodes = {
    # special
}
