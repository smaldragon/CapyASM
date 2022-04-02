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

def value_parse(symbol):
    if len(symbol)==0:
        return [0]
    # decimal
    if symbol[0] == "#":    
        return [int(symbol[1:])]
    # hexadeximal
    if symbol[0] == "$":    
        return [int(symbol[1:],16)]
    # binary
    if symbol[0] == "%":  
        return [int(symbol[1:],2)]
    # ascii
    if len(symbol)>=2:
        if symbol[0] == '"' and symbol[-1] == '"':
            out = []
            for char in symbol[1:-1]:
                out.append(ord(char))
            return out
    
    try:
        return [int(symbol)]
    except:
        return [symbol]
symbol_split = re.compile(".*,?")
value_get = re.compile('".+"|\$*%*@*[0-9a-zA-Z_]+')
modes=[]
for regex in syntax.addr:
    modes.append((re.compile(regex),syntax.addr[regex]))

def main(argv):
    in_file = ''
    out_file = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('capyasm.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_file = arg
        elif opt in ("-o", "--ofile"):
            out_file = arg
    run(in_file,out_file)

def run(in_file,out_file):
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
                        if indent <= len(cur_label):
                            cur_label = cur_label[:indent] + [label.strip('_')]
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
                                values.append(value_get.search(operand).group())
                            if addr in syntax.opcodes[opcode]:
                                for symbol in syntax.opcodes[opcode][addr]:
                                    if type(symbol) is int:
                                        to_append.append(symbol)
                                    else:
                                        if symbol == "#":
                                            to_append.extend(value_parse(values[0]))
                                        elif symbol == "al":
                                            value = value_parse(values[0])[0]
                                            if type(value) is int:
                                                to_append.append(value & 255)
                                            else:
                                                #label = '_'.join(cur_label[:-1]) + "_" + values[0]
                                                to_append.append(values[0])
                                        elif symbol == "ah":
                                            value = value_parse(values[0])[0]
                                            if type(value) is int:
                                                to_append.append(value >> 8)
                                            else:
                                                to_append.append("&high")
                                        elif symbol == "z":
                                            to_append.extend(value_parse(values[0]))
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
                                            #label = '_'.join(cur_label[:-1]) + "_" + values[0]
                                            #to_append.append([label,pc+2])
                                            to_append.append([values[0],pc+2])
                                if opcode == "org":
                                    pc = value_parse(values[0])[0]
                                if opcode == "pad":
                                    if addr == "a":
                                        to_append = [0]*(value_parse(values[0])[0]-pc)
                                        print("padded",(value_parse(values[0])[0]-pc),"bytes")
                                    if addr == "#":
                                        to_append = [0]*(value_parse(values[0])[0])                
                                        print("padded",(value_parse(values[0])[0]),"bytes")
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
                            else:
                                print(f"ERROR: Opcode '{opcode}' does not have addressing mode '{regex[1]}'")
                            
                            out.extend(to_append)
                        pc += len(to_append)
                    elif tokens[0] in macros:
                        lines = lines[:i+1] + macros[tokens[0]].format(*(tokens[1:])).split("\n") + lines[i+1:]
                    else:
                        print("ERROR: INVALID TOKEN",tokens[0])
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
        if type(s) is str:
            value = 0
            if s in labels:
                value = labels[s]
            if s in variables:
                value = variables[s]
            
            out[i] = value&255
            if i+1 < len(out) and out[i+1] == "&high":
                out[i+1] = value>>8            
        elif type(s) is list:
            out[i]   = labels[s[0]]-s[1]
            if out[i] < 0:
                out[i] = 256+out[i]
    with open(out_file,"wb") as f:
        f.write(bytearray(out))
    
if __name__ == "__main__":
   main(sys.argv[1:])