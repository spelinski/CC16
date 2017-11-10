import os
import argparse
import Util
from UnusedCodeFinder import find_and_remove_unhit_instructions
from UnusedIncDec import find_and_remove_unneeded_inc_dec

#old_instruction_hit_or_not.append([instruct, 0, 0, 0, set(), "no"])
def find_and_remove_conflicting_inc_dec(old_instructions, old_instruction_hit_or_not):
    pc = 0
    done = False
    total_in_a = 0
    total_in_b = 0
    total_in_c = 0
    total_in_d = 0
    total_a_calls = 0
    total_b_calls = 0
    total_c_calls = 0
    total_d_calls = 0
    while not done:
        exec_instruction = old_instruction_hit_or_not[pc][0]
        # currently treat postive jmp and jz as automatically unsafe since i'll need to think about it more
        if "inc" in exec_instruction or "dec" in exec_instruction:
            if "inc" in exec_instruction:
                letter = exec_instruction.replace("inc ","")
                if letter == "a":
                    total_in_a += 1
                    total_a_calls += 1
                elif letter == "b":
                    total_in_b += 1
                    total_b_calls += 1
                elif letter == "c":
                    total_in_c += 1
                    total_c_calls += 1
                elif letter == "d":
                    total_in_d += 1
                    total_d_calls += 1
            else:
                letter = exec_instruction.replace("dec ","")
                if letter == "a":
                    total_in_a -= 1
                    total_a_calls += 1
                elif letter == "b":
                    total_in_b -= 1
                    total_b_calls += 1
                elif letter == "c":
                    total_in_c -= 1
                    total_c_calls += 1
                elif letter == "d":
                    total_in_d -= 1
                    total_d_calls += 1
        else:
            print(total_in_a)
            print(total_in_b)
            print(total_in_c)
            print(total_in_d)
            print(total_a_calls)
            print(total_b_calls)
            print(total_c_calls)
            print(total_d_calls)
            if pc > 0:
                if total_a_calls > abs(total_in_a):
                    dec_pc = pc - 1
                    inc_pc = pc - 1
                    pairs_to_remove = (abs(total_a_calls) - total_in_a)/2
                    while pairs_to_remove > 0:
                        while "dec a" not in old_instruction_hit_or_not[dec_pc][0]:
                            dec_pc -= 1
                        old_instruction_hit_or_not[dec_pc][5] = "yes"
                        while "inc a" not in old_instruction_hit_or_not[inc_pc][0]:
                            inc_pc -= 1
                        old_instruction_hit_or_not[inc_pc][5] = "yes"
                        pairs_to_remove -= 1
                elif total_b_calls > abs(total_in_b):
                    dec_pc = pc - 1
                    inc_pc = pc - 1
                    pairs_to_remove = (abs(total_b_calls) - total_in_b)/2
                    while pairs_to_remove > 0:
                        while "dec b" not in old_instruction_hit_or_not[dec_pc][0]:
                            dec_pc -= 1
                        old_instruction_hit_or_not[dec_pc][5] = "yes"
                        while "inc b" not in old_instruction_hit_or_not[inc_pc][0]:
                            inc_pc -= 1
                        old_instruction_hit_or_not[inc_pc][5] = "yes"
                        pairs_to_remove -= 1
                elif total_c_calls > abs(total_in_c):
                    dec_pc = pc - 1
                    inc_pc = pc - 1
                    pairs_to_remove = (abs(total_c_calls) - total_in_c)/2
                    while pairs_to_remove > 0:
                        while "dec c" not in old_instruction_hit_or_not[dec_pc][0]:
                            dec_pc -= 1
                        old_instruction_hit_or_not[dec_pc][5] = "yes"
                        while "inc c" not in old_instruction_hit_or_not[inc_pc][0]:
                            inc_pc -= 1
                        old_instruction_hit_or_not[inc_pc][5] = "yes"
                        pairs_to_remove -= 1
                elif total_d_calls > abs(total_in_d):
                    dec_pc = pc - 1
                    inc_pc = pc - 1
                    pairs_to_remove = (abs(total_d_calls) - total_in_d)/2
                    while pairs_to_remove > 0:
                        while "dec d" not in old_instruction_hit_or_not[dec_pc][0]:
                            dec_pc -= 1
                        old_instruction_hit_or_not[dec_pc][5] = "yes"
                        while "inc d" not in old_instruction_hit_or_not[inc_pc][0]:
                            inc_pc -= 1
                        old_instruction_hit_or_not[inc_pc][5] = "yes"
                        pairs_to_remove -= 1

            total_in_a = 0
            total_in_b = 0
            total_in_c = 0
            total_in_d = 0
            total_a_calls = 0
            total_b_calls = 0
            total_c_calls = 0
            total_d_calls = 0
        pc += 1
        if pc >= len(old_instruction_hit_or_not):
            done = True

    i = 0
    while i < len(old_instruction_hit_or_not):
        if old_instruction_hit_or_not[i][5] == "yes":
            for pc in old_instruction_hit_or_not[i][4]:
                Util.handle_jump_num_update(pc, old_instruction_hit_or_not, old_instructions)
        i += 1

    i = len(old_instruction_hit_or_not) - 1
    while i >= 0:
        if old_instruction_hit_or_not[i][5] == "yes":
            del old_instructions[i]
            del old_instruction_hit_or_not[i]
        i -= 1

    return old_instructions

parser = argparse.ArgumentParser(description="optimize an asm file")
parser.add_argument("-i","--input_file", required=True, help="path and filename of input asm file", dest="input_file_name")
parser.add_argument("-o","--output_file", required=True, help="path and filename of output asm file", dest="output_file_name")
args = parser.parse_args()
with open(args.input_file_name) as f:
    instruction_array = f.read().splitlines()
    new_instruction_array,old_instruction_hit_or_not = find_and_remove_unhit_instructions(instruction_array)
    #run a second time for fun
    new_instruction_array, old_instruction_hit_or_not = find_and_remove_unhit_instructions(instruction_array)
    #new optimization
    new_instruction_array = find_and_remove_unneeded_inc_dec(new_instruction_array, old_instruction_hit_or_not)
    # run a third time for fun
    new_instruction_array, old_instruction_hit_or_not = find_and_remove_unhit_instructions(instruction_array)
    #new optimization
    new_instruction_array = find_and_remove_conflicting_inc_dec(new_instruction_array, old_instruction_hit_or_not)
    with open(args.output_file_name,"w") as o:
        for instruction in new_instruction_array:
            o.write(instruction+os.linesep)