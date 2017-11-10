import re
import Util

def find_and_remove_unneeded_inc_dec(old_instructions, old_instruction_hit_or_not):
    pc = 0
    done = False
    last_safe = -1
    while not done:
        exec_instruction = old_instruction_hit_or_not[pc][0]
        #currently treat postive jmp and jz as automatically unsafe since i'll need to think about it more
        if "jmp" in exec_instruction or "jz" in exec_instruction:
            if "jmp" in exec_instruction:
                number = int(int(exec_instruction.replace("jmp ", "")) / 2)
                if number > 0:
                    last_safe = pc
            else:
                last_safe = pc
        elif "mov" in exec_instruction:
            match = re.match(r'mov\s+([a-d])',exec_instruction)
            dest_reg = match.group(1)
            temp_pc = pc-1
            while temp_pc > last_safe:
                loop_instr = old_instruction_hit_or_not[temp_pc][0]
                regex_string = re.compile("(dec|inc)\s+(" + re.escape(dest_reg) + ")")
                loop_match = regex_string.match(loop_instr)
                if loop_match:
                    old_instruction_hit_or_not[temp_pc][5] = "yes"
                temp_pc -= 1
            last_safe = pc
        pc +=1
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