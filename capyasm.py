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
import docs
import os

def main(args):
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
    
    if args.docs:
        docs.read()
        return

    valid_args = True

    if not args.input:
        logging.error("No input file specified") 
        valid_args = False
    else:
        inter = None
        try:
            with open(args.input) as f:
                inter = parse.Interpreter(f.readlines(),"")
        except Exception(e):
            print(e)
            logging.error(f"Failed to open input file '{args.input}'")
            valid_args = False

        if valid_args and inter:
            output = args.output
            
            try:
                with open(".temp","wb") as f:
                    inter.run(f)

                if inter.warnings:
                    logging.info(f"{len(inter.errors)} warnings")
                    for warning in inter.warnings:
                        msg = warning[0]
                        if warning[1] > 0:
                            msg += f" @ line {warning[1]}"
                        logging.warning(msg)
                if inter.errors:
                    logging.info(f"{len(inter.errors)} errors")
                    for error in inter.errors:
                        msg = error[0]
                        if error[1] > 0:
                            msg += f" @ line {error[1]}"
                        logging.error(msg)
                else:
                    if not output:
                        output = os.path.splitext(args.input)[0] + inter.extension

                    os.rename(".temp",output)

            except Exception as e:
                print(e)
                logging.error(f"Failed to open output file '{output}'")
        
    if not valid_args:
        logging.info('Usage: capyasm.py -i <inputfile> -o <args.output>')

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    logging.addLevelName(logging.ERROR,"\x1b[31;1m"+"Error"+"\x1b[0m")
    logging.addLevelName(logging.INFO,"Info")
    
    parser.add_argument("-i","--input", help="The file to assemble", action = "store")
    parser.add_argument("-o","--output", help="The output file", action = "store")
    parser.add_argument("-d","--debug", help = "Debug output", action = "store_true")
    parser.add_argument("--docs", help = "Print Documentation", action = "store_true")
    
    main(parser.parse_args())
   