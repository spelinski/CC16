import std.array : split;
import std.conv;
import dunit.toolkit;
import std.stdio : writeln;
import Instructions;

class InstructionDecoder {

    CpuInstruction parse_instruction(short instruction) {
        byte opcode = (instruction & 0xF000) >> 12;
        byte reg_1 = (instruction & 0x0F00) >> 8;
        byte reg_2 = (instruction & 0x00F0) >> 4;
        byte offset = cast(byte)(instruction & 0x00FF);
        switch( opcode ) {
            case 0:
                return new Increment(reg_1);
            case 1:
                return new Decrement(reg_1);
            case 2:
                return new Move(reg_1, reg_2);
            case 3:
                return new Jump(offset);
            case 4:
                return new JumpZero(reg_1, offset);
            default:
                assert(0);
        }
    }
}


@system
unittest {
    auto parser = new InstructionDecoder();
    parser.parse_instruction(0x0000).assertEqual(new Increment(0));
    parser.parse_instruction(0x1100).assertEqual(new Decrement(1));
    parser.parse_instruction(0x2230).assertEqual(new Move(2,3));
    parser.parse_instruction(0x3040).assertEqual(new Jump(64));
    parser.parse_instruction(0x4140).assertEqual(new JumpZero(1, 64));
    parser.parse_instruction(0x4280).assertEqual(new JumpZero(2, -128));
    parser.parse_instruction(0x43ff).assertEqual(new JumpZero(3, -1));
}
