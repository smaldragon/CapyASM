"""
8-bit subleq
"""

macro = """
"""

registers = []
addr_tokens = ["[","]"]

extension = ".sbl"

opcodes = {
  "subleq":{
    "###":  ["#","#","#"],
    "##":  ["#","#","NEXT"],
  }
}