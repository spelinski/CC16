import os
import argparse
import Util
from UnusedCodeFinder import find_and_remove_unhit_instructions
from UnusedIncDec import find_and_remove_unneeded_inc_dec
from DuplicateIncDec import find_and_remove_conflicting_inc_dec

parser = argparse.ArgumentParser(description="optimize an asm file")
parser.add_argument("-i","--input_file", required=True, help="path and filename of input asm file", dest="input_file_name")
parser.add_argument("-o","--output_file", required=True, help="path and filename of output asm file", dest="output_file_name")
args = parser.parse_args()
with open(args.input_file_name) as f:
    instruction_array = f.read().splitlines()
    old_instruction_hit_or_not = Util.markup_instructions(instruction_array)
    new_instruction_array = find_and_remove_unhit_instructions(instruction_array,old_instruction_hit_or_not)
    #new optimization
    old_instruction_hit_or_not = Util.markup_instructions(new_instruction_array)
    new_instruction_array = find_and_remove_unneeded_inc_dec(new_instruction_array, old_instruction_hit_or_not)
    #new optimization
    old_instruction_hit_or_not = Util.markup_instructions(new_instruction_array)
    new_instruction_array = find_and_remove_conflicting_inc_dec(new_instruction_array, old_instruction_hit_or_not)
    with open(args.output_file_name,"w") as o:
        for instruction in new_instruction_array:
            o.write(instruction+os.linesep)