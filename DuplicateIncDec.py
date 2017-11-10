import Util

def handle_inc_dec_mark(pc, letter, pairs_to_remove, old_instruction_hit_or_not):
    dec_pc = pc - 1
    inc_pc = pc - 1
    while pairs_to_remove > 0:
        while ("dec " + str(letter)) not in old_instruction_hit_or_not[dec_pc][0]:
            dec_pc -= 1
        old_instruction_hit_or_not[dec_pc][5] = "yes"
        while ("inc " + str(letter)) not in old_instruction_hit_or_not[inc_pc][0]:
            inc_pc -= 1
        old_instruction_hit_or_not[inc_pc][5] = "yes"
        pairs_to_remove -= 1


def find_and_remove_conflicting_inc_dec(old_instructions, old_instruction_hit_or_not):
    pc = 0
    done = False
    total_in_a = total_in_b = total_in_c = total_in_d = 0
    total_a_calls = total_b_calls = total_c_calls = total_d_calls = 0
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
            if pc > 0:
                if total_a_calls > abs(total_in_a):
                    pairs_to_remove = (abs(total_a_calls) - total_in_a)/2
                    handle_inc_dec_mark(pc, "a", pairs_to_remove, old_instruction_hit_or_not)
                elif total_b_calls > abs(total_in_b):
                    pairs_to_remove = (abs(total_b_calls) - total_in_b)/2
                    handle_inc_dec_mark(pc, "b", pairs_to_remove, old_instruction_hit_or_not)
                elif total_c_calls > abs(total_in_c):
                    pairs_to_remove = (abs(total_c_calls) - total_in_c)/2
                    handle_inc_dec_mark(pc, "c", pairs_to_remove, old_instruction_hit_or_not)
                elif total_d_calls > abs(total_in_d):
                    pairs_to_remove = (abs(total_d_calls) - total_in_d)/2
                    handle_inc_dec_mark(pc, "d", pairs_to_remove, old_instruction_hit_or_not)

            total_in_a = total_in_b = total_in_c = total_in_d = 0
            total_a_calls = total_b_calls = total_c_calls = total_d_calls = 0
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