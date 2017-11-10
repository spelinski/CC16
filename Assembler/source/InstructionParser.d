import std.array : split;
import std.conv;
import dunit.toolkit;
import std.stdio : write;

class InstructionParser {
      enum short[string] op_map = [
		"inc": 0x0000,
		"dec": 0x1000,
		"mov": 0x2000,
		"jmp": 0x3000,
		"jz" : 0x4000];

    short parse_instruction(string instruction) {
	auto words = split(instruction);
	auto opcode = words[0];
	auto arguments = words[1..$];
	auto machine_instruction = op_map[opcode];
	switch( opcode ) {
		case "inc":
		case "dec":
			machine_instruction |= (parse_register(arguments[0]) << 8);
			break;
		case "mov":
			machine_instruction |= (parse_register(arguments[0]) << 8);
			machine_instruction |= (parse_register(arguments[1]) << 4);
			break;
		case "jmp":
			machine_instruction |= (0xFF & parse_offset(arguments[0]));
			break;
		case "jz":
			machine_instruction |= (parse_register(arguments[0]) << 8);
			machine_instruction |= (0xFF & parse_offset(arguments[1]));
			break;
		default:
			assert(0);
	}
	return machine_instruction;
    }

    byte parse_register(string register) {
	    enum byte[string] reg_map = ["a": 0, "b": 1, "c": 2, "d": 3];
	    return reg_map[register];
    }
    byte parse_offset(string offset) {
	    return to!byte(offset);
    }
}

@system
unittest {
    auto parser = new InstructionParser();
    parser.parse_instruction("inc a").assertEqual(0x0000);
    parser.parse_instruction("dec b").assertEqual(0x1100);
    parser.parse_instruction("mov c d").assertEqual(0x2230);
    parser.parse_instruction("jmp 64").assertEqual(0x3040);
	parser.parse_instruction("jmp -1").assertEqual(0x30ff);
    parser.parse_instruction("jz b 64").assertEqual(0x4140);
    parser.parse_instruction("jz a -128").assertEqual(0x4080);
    parser.parse_instruction("jz a -1").assertEqual(0x40ff);
}
