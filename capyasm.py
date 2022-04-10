#!/usr/bin/python3
# __CapyASM__
#                                 .;o,
#        __."iIoi,._              ;pI __-"-xx.,_
#      `.3"P3PPPoie-,.            .d' `;.     `p;
#     `O"dP"````""`PdEe._       .;'   .     `  `|  
#    "$#"'            ``"P4rdddsP'  .F.    ` `` ; 
#   i/"""     *"Sp.               .dPff.  _.,;Gw'
#   ;l"'     "  `dp..            "sWf;fe|'
#  `l;          .rPi .    . "" "dW;;doe;
#   $          .;PE`'       " "sW;.d.d;
#   $$        .$"`     `"saed;lW;.d.d.i
#   .$M       ;              ``  ' ld;.p.
#__ _`$o,.-__  "ei-Mu~,.__ ___ `_-dee3'o-ii~m. ____

import sys
import getopt
import syntax
import re

symbol_split = re.compile(".*,?")
value_get = re.compile(f'".+"|{syntax.value}')
modes=[]
for regex in syntax.addr:
    modes.append((re.compile(regex),syntax.addr[regex]))

def main(argv):
    in_file = ''
    out_file = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv,"vhi:o:",["ifile=","ofile=","verbose"])
    except getopt.GetoptError:
        print('capyasm.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_file = arg
        elif opt in ("-o", "--ofile"):
            out_file = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
    run(in_file,out_file,verbose)

def run(in_file,out_file,verbose):

    def value_parse(symbol):
        out = []
        
        if symbol[0] in ("'",'"') and symbol[-1] in ("'",'"'):
            for char in symbol[1:-1]:
                out.append(ord(char))
            if symbol[0] == '"':
                out.append(0)
            return out
        else:
            for operator in re.split(" ",symbol):
                sign = 1
                if operator[0] == "-":
                    operator = operator[1:]
                    sign = -1
                if operator.isdigit():
                    out.append(int(operator)*sign)
                elif operator[0] == "$":
                    out.append(int(operator[1:],16)*sign)
                elif operator[0] == "%":
                    out.append(int(operator[1:],2)*sign)
                elif operator in variables:
                    out.append(variables[operator]*sign)
                else:
                    out.append(operator)
            return out

        return [symbol]
    # get file folder
    folder = "/".join(in_file.split('/')[:-1])
    if len(folder) > 0:
        folder+='/'
    
    pc  = 0
    variables = {}
    labels = {}
    macros = {}
    in_macro = False
    cur_macro = ""
    cur_label = []
    out = []

    with open(in_file) as f:
        lines = f.readlines()
        i = 0
        opcodes = syntax.opcodes
        # 1st Pass -> Read and Parse tokens
        while i < len(lines):
            line=lines[i]
            if not in_macro:
                # Remove comments
                if ";" in line:
                    line = line[:line.find(";")]
                # Get Tokens for this line
                tokens = re.findall(r'".+"|[^,\s]+', line.strip())
                if len(tokens)>=1:
                    if len(tokens[0]) == 0:
                        continue
                    # Labels
                    if tokens[0].startswith('_'):
                        indent = 0
                        label = tokens[0][1:]
                        for c in label:
                            if c == '_':
                                indent+=1
                            else:
                                break
                        if indent <= len(cur_label):
                            prefix = []
                            if indent >= 1:
                                prefix = cur_label[:indent]
                            cur_label = prefix + [label.strip('_')]
                        else:
                            cur_label.append(label.strip('_'))
                        labels["_".join(cur_label)]=pc
                    elif tokens[0] in syntax.opcodes:
                        opcode = tokens[0]
                        addr = "i"
                        to_append = []
                        values = []
                        if len(tokens)>=1:
                            for operand in tokens[1:]:
                                for regex in modes:
                                    if regex[0].match(operand):
                                        addr = regex[1]
                                values.extend(value_get.findall(operand))
                            if addr in syntax.opcodes[opcode]:
                                value_index = 0
                                for symbol in syntax.opcodes[opcode][addr]:
                                    if type(symbol) is int:
                                        to_append.append(symbol)
                                    else:
                                        if symbol == "#":
                                            to_append.extend(value_parse(values[value_index]))
                                            value_index+=1
                                        elif symbol == "al":
                                            value = value_parse(values[value_index])[0]
                                            if type(value) is int:
                                                to_append.append(value & 255)
                                            else:
                                                to_append.append(values[value_index])
                                        elif symbol == "ah":
                                            value = value_parse(values[value_index])[0]
                                            if type(value) is int:
                                                to_append.append(value >> 8)
                                            else:
                                                to_append.append("&high")
                                            value_index+=1
                                        elif symbol == "z":
                                            to_append.extend(value_parse(values[value_index]))
                                            value_index+=1
                                        elif symbol == "*":
                                            for value in values:
                                                to_append.extend(value_parse(value))
                                        elif symbol == "**":
                                            for value in values:
                                                v = value_parse(value)
                                                if type(v[0]) is int:
                                                    to_append.append(value_parse(value)[0]&255)
                                                    to_append.append(value_parse(value)[0]>>8)
                                                else:
                                                    to_append.append(v[0])
                                                    to_append.append("&high")
                                        elif symbol == "r":
                                            to_append.append([values[value_index],pc+2+value_index])
                                if opcode == "org":
                                    pc = value_parse(values[0])[0]
                                if opcode == "pad":
                                    if addr == "a":
                                        to_append = [0]*(value_parse(values[0])[0]-pc)
                                        print('\033[93m'+"padded",(value_parse(values[0])[0]-pc),"bytes")
                                    if addr == "#":
                                        to_append = [0]*(value_parse(values[0])[0])                
                                        print('\033[93m'+"padded",(value_parse(values[0])[0]),"bytes")
                                if opcode == "var":
                                    variables[values[0]]=value_parse(values[1])[0]
                                if opcode == "asm":
                                    with open(folder+values[0].strip('"'),"r") as f:
                                        lines = lines[:i+1] + f.readlines() + lines[i+1:]
                                if opcode == "bin":
                                    with open(folder+values[0].strip('"'),"rb") as f:
                                        bindata = f.read()
                                        out.extend(bindata)
                                if opcode == "macro":
                                    in_macro = values[0]
                                if opcode == "cpu":
                                    print(f"\033[0;37m@{i} Setting CPU to {values[0]}")
                                    cpu_macro,cpu_opcodes = syntax.get(values[0])
                                    for k,v in cpu_opcodes.items():
                                        if not k in opcodes:
                                            opcodes[k] = v
                                        else:
                                            opcodes[k].update(v)
                                    lines = lines[:i+1] + cpu_macro.split("\n") + lines[i+1:]
                            else:
                                print(f'\033[91m'+f"@{i} ERROR: Opcode '{opcode}' does not have addressing mode '{addr}'")
                            
                            if (verbose):
                                print("\033[0;37m",tokens,cur_label)
                            out.append((to_append,cur_label.copy()))
                        pc += len(to_append)
                    elif tokens[0] in macros:
                        lines = lines[:i+1] + macros[tokens[0]].format(*(tokens[1:])).split("\n") + lines[i+1:]
                    else:
                        print('\033[91m'+f"@{i} ERROR: INVALID TOKEN",tokens[0])
            # Macro
            else:
                if "endmacro" in line:
                    macros[in_macro] = cur_macro 
                    cur_macro = ""
                    in_macro = False
                else:
                    cur_macro += line
            i+=1

    # 2nd Pass -> Add labels and variables
    for i,s in enumerate(out):
        for u,b in enumerate(s[0]):
            # Converts a string into its corresponding var/label value
            def get_value(name,s):
                value = -1
                if name in variables:
                    value = variables[name]        
                else:
                    space = s[1]
                    while len(space)>0:
                        to_try = "_".join(space) + "_" + name
                        if to_try in labels:
                            value = labels[to_try]
                            break
                        space.pop()
                    if value == -1:
                        if name in labels:
                            value = labels[name]
                        else:
                            print("\033[91m"+f"ERROR: Could Not find label {name}")
                return value

            name = None
            value = 0
            if type(b) is int:
                continue
            # Absolute Value
            elif type(b) is str:
                name = b
                value = get_value(name,s)
                s[0][u] = value & 255  
                if u+1 < len(s[0]) and s[0][u+1] == "&high":
                    s[0][u+1] = value>>8  
            # Relative Value
            elif type(b) is list:
                name = b[0]
                value = get_value(name,s) - b[1]
                if value < 0:
                    value += 256
                s[0][u] = value
    if (verbose):
        print("\033[0;37m")
        print("Labels:",labels)
        print("Variables:",variables)
    with open(out_file,"wb") as f:
        for l in out:
            for b in l[0]:
                if b < 0:
                    b+=256
                f.write(bytearray([b]))
    
if __name__ == "__main__":
   main(sys.argv[1:])