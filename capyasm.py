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
import parse

def main(argv):
    in_file = None
    out_file = None
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
            
    if in_file is not None and out_file is not None:
        inter = None
        with open(in_file) as f:
            inter = parse.Interpreter(f.readlines(),"")
        with open(out_file,"wb") as f:
            inter.run(f)
    else:
        print("Error: Invalid IO files")

if __name__ == "__main__":
   main(sys.argv[1:])