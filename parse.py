from colorama import Fore, Back, Style
import operator
import syntax

ASM_OPS = [
    "cpu",
    "var",
    "org",
    "pad",
    "byte",
    "word",
    "asm",
    "bin",
    "macro",
]

CPU_OPS = {}

BIN_OPS = {
    "+":operator.add,
    "-":operator.sub,
    "/":operator.floordiv,
    "*":operator.mul,
}
def operator_b0(a):
    return a & 255

def operator_b1(a):
    return (a >> 8) & 255

def operator_b2(a):
    return (a >> 16) & 255

def operator_b3(a):
    return (a >> 24) & 255


PRE_OPS = {
    "-":operator.neg,
}
POST_OPS = {
    ".b0":operator_b0,
    ".b1":operator_b1,
    ".b2":operator_b2,
    ".b3":operator_b3,
    ".lo":operator_b0,
    ".hi":operator_b1,
}

ADDR_TOKENS = ["<",">","(",")","[","]","+X","+Y","#"]
REGISTERS = ["A","X","Y","P","C","D","I","V"]

class Interpreter:
    def __init__(self,lines,folder):
        self.lines    = lines
        self.folder   = folder
        
        self.cur_line = 0
        self.out = []
        self.variables = {}
        self.macros    = {}
        self.cur_label = []
        self.labels    = {}
        self.pc        = 0
        
        self.in_macro  = None
        self.cur_macro = ""
    
    def log(self,message):
        print(Fore.YELLOW + "LOG:" + message + Fore.RESET )
    def error(self,message):
        print(Back.RED + "ERROR:" + message + Back.RESET)
    def run(self,out_f):
        # Pass 1 - Go line by line and execute it
        print("PASS 1")
        pass_1 = []
        while self.cur_line < len(self.lines):
            if self.in_macro is None:
                #print("\n")
                #print("LINE:",self.lines[self.cur_line].strip())
                tokens  = self.getTokens(self.lines[self.cur_line])
                #print("TOKENS:",tokens)
                symbols = self.getSymbols(tokens)
                #print("SYMBOLS",symbols)
                lineout = self.getCompile(symbols)
                #print("OUT",lineout)
                pass_1.append(lineout)
            else:
                if self.lines[self.cur_line].strip() == "endmacro":
                    self.macros[self.in_macro] = self.cur_macro
                    self.in_macro = None
                else:
                    self.cur_macro+=self.lines[self.cur_line]
                
            self.cur_line += 1
        #print(pass_1)
        # Pass 2 - Calculate math, labels and relatives
        print("PASS 2")
        pass_2 = []
        for _,p in enumerate(pass_1):
            if p[0]:
                cur_int = []
                for d in p[0]:
                    if d[0] == "&code":
                        cur_int.append(d[1])
                    elif d[0] == "&byte":
                        cur_int.append(self.processExpression(d[1]))
                    elif d[0] == "&low":
                        cur_int.append(self.processExpression(d[1])&255)
                    elif d[0] == "&high":
                        cur_int.append((self.processExpression(d[1])>>8)&255)
                    elif d[0] == "&rel":
                        v = self.processExpression(d[1])-(p[1]+len(cur_int)+1)
                        cur_int.append(v)
                    elif d[0] == "&bytes":
                        cur_int.extend(d[1])
                pass_2.extend(cur_int)
        print("PASS 3")
        # Pass 3 - Output to binary file
        
        for b in pass_2:
            if b < 0:
                b+=256
            if b < 0 or b > 255:
                self.error("INVALID BYTE")
            else:
                out_f.write(bytearray([b]))
                    
    def processExpression(self,expr):
        def parse_value(value):
            out = [value]
            if value[0] in ("'",'"'):
                for c in value[1:]:
                    out.append(ord(c))
                if value[0] == '"':
                    out.append(0)
            elif value.isdigit():
                out.append(int(value))
            elif value[0] == "$":
                out.append(int(value[1:],16))
            elif value[0] == "%":
                out.append(int(value[1:],2))
                
            return out
        
        symbols = []
        
        operand   = None
        value = None
        
        for i,token in enumerate(expr):
            if token in self.variables:
                value = [token,self.variables[token]]
            elif token in self.labels:
                value = [token,self.labels[token]]
            elif token in BIN_OPS or token in PRE_OPS or token in POST_OPS:
                operand = token
                value = None
            else:
                value = parse_value(token)
                
            # BinOp
            if operand in BIN_OPS and value is not None and i >= 2:
                symbols[-1][1] = BIN_OPS[operand](symbols[-1][1],value[1])
            elif operand in POST_OPS and value is None:
                symbols[-1][1] = POST_OPS[operand](symbols[-1][1])
            elif operand in PRE_OPS and value is not None:
                symbols.append([value[0],PRE_OPS[operand](value[1])])
            elif value is not None:
                symbols.append(value)
        return symbols[0][1]
        
    # Step 1 - Parse a line of code and return tokens
    def getTokens(self,line):
        cur_token = ""
        tokens = []
        string = None
        
        def append_token(cur_token,tokens):
            if cur_token != "":
                tokens.append(cur_token)
            cur_token = ""
            return cur_token,tokens
            
        for _,c in enumerate(line):
            # We are in a string
            if string is not None:
                if c == string:
                    string = None
                    cur_token,tokens=append_token(cur_token,tokens)
                else:
                    cur_token += c
            # We are not in a string
            else:
                if c == "\n":
                    break
                if c == ";" and string is None:
                    break
                elif c == ":" or c == "," or c == " ":
                    cur_token,tokens=append_token(cur_token,tokens)
                elif c in ('"',"'"):
                    cur_token,tokens=append_token(cur_token,tokens)
                    cur_token += c
                    string = c
                elif c in ("[","]","(",")","<",">","+","-","*","/","#"):
                    cur_token,tokens=append_token(cur_token,tokens)
                    cur_token = c
                    cur_token,tokens=append_token(cur_token,tokens)
                elif c in ("$","%","."):
                    cur_token,tokens=append_token(cur_token,tokens)
                    cur_token = c
                else:
                    cur_token += c
        
        cur_token,tokens=append_token(cur_token,tokens)
        return tokens
    # Step 2 - Take tokens and return calculated symbols with variables and compile-time math
    def getSymbols(self,tokens):
        symbols = []
        cur_symbol :List[List] = []
        prev_token = True
        for i,token in enumerate(tokens):
            if i == 0:
                symbols.append([token])
                continue
            if token in REGISTERS and len(cur_symbol)>=1 and cur_symbol[-1] == '+':
                cur_symbol = cur_symbol[:-1]
                symbols.append(cur_symbol.copy())
                symbols.append(["+"+token])
                cur_symbol = []
                continue
            
            if token in BIN_OPS or token in PRE_OPS or token in POST_OPS:
                prev_token = True
            else:
                if prev_token == False:
                    symbols.append(cur_symbol.copy())
                    cur_symbol = []
                prev_token = False
            cur_symbol.append(token)
        
        if cur_symbol != []:
            symbols.append(cur_symbol)
        return symbols
    # Step 3 - Compile a symbol array (1st pass)
    def getCompile(self,symbols):
        output = []
        cur_pc = self.pc
        if symbols and len(symbols[0]) == 1:
            opcode = symbols[0][0]
            # Label
            if opcode[0] == "_":
                ident = 0
                for c in opcode[1:]:
                    if c == '_':
                        ident+= 1
                    else:
                        break
                if ident > len(self.cur_label):
                    self.cur_label.extend(['']*(ident-len(self.cur_label)-1))
                    self.cur_label.append(opcode[1:])
                else:
                    self.cur_label = self.cur_label[:ident] + [opcode[1:]]
                self.labels["".join(self.cur_label)] = self.pc
            # ASSEMBLER INSTRUCTION
            elif opcode in ASM_OPS:
                if opcode == "cpu":
                    cpu_macro,cpu_opcodes=syntax.get(symbols[1][0])
                    CPU_OPS.update(cpu_opcodes)
                    self.lines = self.lines[:self.cur_line+1] + cpu_macro.split("\n") + self.lines[self.cur_line+1:]
                if opcode == "var":
                    try:
                        value = self.processExpression(symbols[2])
                        self.variables[symbols[1][0]] = value
                    except:
                        self.error("Unable to process variable")
                if opcode == "org":
                    self.pc = self.processExpression(symbols[1])
                if opcode == "pad":
                    if symbols[1][0] == '[':
                        output = [("&bytes",[0]*(self.processExpression(symbols[2])-self.pc))]
                    else:
                        output = [("&bytes",[0]*self.processExpression(symbols[1]))]
                    #else:
                    #    self.error("Invalid values for pad")
                if opcode == "byte":
                    for s in symbols[1:]:
                        if s[0][0] in ("'",'"'):
                            string = []
                            for c in s[0][1:]:
                                string.append(ord(c))
                            if s[0][0] == '"':
                                string.append(0)
                            output.append(("&bytes",string))
                        else:
                            output.append(("&byte",s))
                if opcode == "word":
                    for s in symbols[1:]:
                        output.extend([("&low",s),("&high",s)])
                if opcode == "asm":
                    with open(self.folder+symbols[1][0][1:]) as f:
                        self.lines = self.lines[:self.cur_line+1] + f.read().split("\n") + self.lines[self.cur_line+1:]
                        self.log(f" Inserted assembly file \"{symbols[1][0][1:]}\"")
                if opcode == "bin":
                    with open(self.folder+symbols[1][0][1:],"rb") as f:
                        bn = []
                        for b in f.read():
                            bn.append(b)
                        output.append(("&bytes",bn))
                        self.log(f" Inserted binary file \"{symbols[1][0][1:]}\"")
                if opcode == "macro":
                    self.in_macro = symbols[1][0]
            # CPU INSTRUCTION
            elif opcode in CPU_OPS:
                mode = ''
                param = []
                for symbol in symbols[1:]:
                    if symbol[0] in ADDR_TOKENS or symbol[0] in REGISTERS:
                        mode += symbol[0]
                    else:
                        mode += "i"
                        param.append(symbol)
                if mode in syntax.modes:
                    addr = syntax.modes[mode]
                    if addr in CPU_OPS[opcode]:
                        param_i = 0
                        for code in CPU_OPS[opcode][addr]:
                            if type(code) is int:
                                output.append(("&code",code))
                            elif code == "r":
                                output.append(("&rel",param[param_i]))
                                param_i += 1
                            elif code == "#":
                                output.append(("&byte",param[param_i]))
                                param_i += 1
                            elif code == "z":
                                output.append(("&byte",param[param_i]))
                                param_i += 1
                            elif code == "al":
                                output.append(("&low",param[param_i]))
                            elif code == "ah":
                                output.append(("&high",param[param_i]))
                                param_i += 1
                    else:
                        self.error(f"Opcode {opcode} does not support Addressing Mode {addr}")
                else:
                    self.error(f"Unkown Addressing Mode {mode}")
                        
                #print(f"mode: '{mode}'")
            elif opcode in self.macros:
                values = self.lines[self.cur_line].strip().split(" ")[1].split(",")
                try:
                    self.lines = self.lines[:self.cur_line+1] + self.macros[opcode].format(*(values)).split("\n") + self.lines[self.cur_line+1:]
                except:
                    self.error("Invalid Macro") 
            else:
                self.error(f"Unkown Opcode {opcode}")
        for v in output:
            if v[0] == "&bytes":
                self.pc += len(v[1])
            else:
                self.pc += 1
        return (output,cur_pc)