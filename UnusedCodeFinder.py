import Util

def handle_postive_jump(pc, number, old_instruction_hit_or_not):
    old_pc = pc
    skip_destination = pc + number
    pc += 1
    while pc < skip_destination:
        old_instruction_hit_or_not[pc][4].add(old_pc)
        pc += 1
    return pc

def handle_negative_jump(pc, number, old_instruction_hit_or_not):
    old_pc = pc
    skip_destination = pc + number
    pc -= 1
    while pc > skip_destination:
        old_instruction_hit_or_not[pc][4].add(old_pc)
        pc -= 1
    return pc


def find_and_remove_unhit_instructions(old_instructions):
    old_instruction_hit_or_not = []
    for instruct in old_instructions:
        old_instruction_hit_or_not.append([instruct, 0, 0, 0, set(), "no"])
    rerun = True
    while rerun:
        rerun = False
        pc = 0
        done = False
        while not done:
            old_instruction_hit_or_not[pc][1] = 1
            exec_instruction = old_instruction_hit_or_not[pc][0]
            if "jmp" in exec_instruction or "jz" in exec_instruction:
                if "jmp" in exec_instruction:
                    number = int(int(exec_instruction.replace("jmp ",""))/2)
                    if number > 0:
                        pc = handle_postive_jump(pc, number, old_instruction_hit_or_not)
                    else:
                        pc = handle_negative_jump(pc, number, old_instruction_hit_or_not)
                else:
                    number = int(int(exec_instruction.replace("jz a ", "").replace("jz b ", "").replace("jz c ", "").replace("jz d ",""))/2)
                    if old_instruction_hit_or_not[pc][2] == 0 or old_instruction_hit_or_not[pc][3] == 0:
                        rerun = True
                    if number < 0 and old_instruction_hit_or_not[pc][3] == 0:
                        old_instruction_hit_or_not[pc][3] = 1
                        pc += number
                    elif old_instruction_hit_or_not[pc][2] == 0:
                        old_instruction_hit_or_not[pc][2] = 1
                        pc += 1
                    else:
                        old_instruction_hit_or_not[pc][3] = 1
                        if number > 0:
                            pc = handle_postive_jump(pc, number, old_instruction_hit_or_not)
                        else:
                            pc += number
            else:
                pc += 1
            if pc >= len(old_instruction_hit_or_not):
                done = True

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
            del old_instruction_hit_or_not[i]
        i -= 1

    return old_instructions,old_instruction_hit_or_not