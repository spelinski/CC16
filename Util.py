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


def handle_jump_two_or_less(pc, number, old_instruction_hit_or_not):
    if number ==  0:
        old_instruction_hit_or_not[pc][5] = "yes"
        return True
    elif number == 2:
        old_instruction_hit_or_not[pc][5] = "yes"
        return True
    else:
        return False


def handle_jump_num_update(pc, old_instruction_hit_or_not, old_instructions):
    if "jmp" in old_instruction_hit_or_not[pc][0]:
        number = int(old_instruction_hit_or_not[pc][0].replace("jmp ", ""))
        if number > 0:
            number -= 2
        elif number < 0:
            number += 2
        if not handle_jump_two_or_less(pc, number, old_instruction_hit_or_not):
            old_instruction_hit_or_not[pc][0] = "jmp " + str(number)
            old_instructions[pc] = "jmp " + str(number)
    elif "jz" in old_instruction_hit_or_not[pc][0]:
        if "jz a" in old_instruction_hit_or_not[pc][0]:
            number = int(old_instruction_hit_or_not[pc][0].replace("jz a ", ""))
            if number > 0:
                number -= 2
            elif number < 0:
                number += 2
            if not handle_jump_two_or_less(pc, number, old_instruction_hit_or_not):
                old_instruction_hit_or_not[pc][0] = "jz a " + str(number)
                old_instructions[pc] = "jz a " + str(number)
        elif "jz b" in old_instruction_hit_or_not[pc][0]:
            number = int(old_instruction_hit_or_not[pc][0].replace("jz b ", ""))
            if number > 0:
                number -= 2
            elif number < 0:
                number += 2
            if not handle_jump_two_or_less(pc, number, old_instruction_hit_or_not):
                old_instruction_hit_or_not[pc][0] = "jz b " + str(number)
                old_instructions[pc] = "jz b " + str(number)
        elif "jz c" in old_instruction_hit_or_not[pc][0]:
            number = int(old_instruction_hit_or_not[pc][0].replace("jz c ", ""))
            if number > 0:
                number -= 2
            elif number < 0:
                number += 2
            if not handle_jump_two_or_less(pc, number, old_instruction_hit_or_not):
                old_instruction_hit_or_not[pc][0] = "jz c " + str(number)
                old_instructions[pc] = "jz c " + str(number)
        elif "jz d" in old_instruction_hit_or_not[pc][0]:
            number = int(old_instruction_hit_or_not[pc][0].replace("jz d ", ""))
            if number > 0:
                number -= 2
            elif number < 0:
                number += 2
            if not handle_jump_two_or_less(pc, number, old_instruction_hit_or_not):
                old_instruction_hit_or_not[pc][0] = "jz d " + str(number)
                old_instructions[pc] = "jz d " + str(number)


def markup_instructions(old_instructions):
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
    return old_instruction_hit_or_not
