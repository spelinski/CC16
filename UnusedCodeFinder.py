import Util

def find_and_remove_unhit_instructions(old_instructions,old_instruction_hit_or_not):
    i = 0
    while i < len(old_instruction_hit_or_not):
        if old_instruction_hit_or_not[i][1] == 0:
            old_instruction_hit_or_not[i][5] = "yes"
            for pc in old_instruction_hit_or_not[i][4]:
                Util.handle_jump_num_update(pc, old_instruction_hit_or_not, old_instructions)
        i += 1
    i = len(old_instruction_hit_or_not) - 1
    while i >= 0:
        if old_instruction_hit_or_not[i][5] == "yes":
            del old_instructions[i]
        i -= 1

    return old_instructions