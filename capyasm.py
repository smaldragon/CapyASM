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

import argparse
import logging
import parse

def main(args):
    in_file = args.input
    out_file = args.output
    debug = args.debug
    
    valid_args = True
    
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
    
    if not in_file:
        logging.error("No input file specified") 
        valid_args = False
    else:
        inter = None
        try:
            with open(in_file) as f:
                inter = parse.Interpreter(f.readlines(),"")
        except:
            logging.error(f"Failed to open input file '{in_file}'")
            valid_args = False

        if valid_args and inter:
            try:            
                with open(out_file,"wb") as f:
                    inter.run(f)
            except:
                logging.error(f"Failed to open output file '{out_file}'")
        
    if not valid_args:
        logging.info('Usage: capyasm.py -i <inputfile> -o <outputfile>')

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    logging.addLevelName(logging.ERROR,"\x1b[31;1m"+"Error"+"\x1b[0m")
    logging.addLevelName(logging.INFO,"Info")
    

    parser.add_argument("-i","--input", help="The file to assemble", action = "store")
    parser.add_argument("-o","--output", help="The output file", action = "store")
    parser.add_argument("-d","--debug", help = "Debug output", action = "store_true")
    main(parser.parse_args())
   