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
