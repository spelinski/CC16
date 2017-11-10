import SpecialPurposeRegister : SpecialPurposeRegister;
import InstructionDecoder : InstructionDecoder;
import Instructions : CpuInstruction;
import std.stdio : writefln, writeln, File;
import dunit.toolkit;

SpecialPurposeRegister run_simulation(string inputFile) {
	auto decoder = new InstructionDecoder();
	auto in_file = File(inputFile);
	CpuInstruction[] instructions;
	while (!in_file.eof())
	{
		auto instruction = in_file.rawRead(new short[1]);
		if( instruction.length == 1 ) {
			instructions ~= decoder.parse_instruction(instruction[0]);
		}
	}
	in_file.close();
	auto spr = SpecialPurposeRegister();
	while( spr.instruction_pointer < instructions.length ) {
		spr = instructions[spr.instruction_pointer].perform_operation(spr);
	}
	return spr;
}

@system
unittest
{
	auto spr = run_simulation("example.bin");
	spr.registers.assertEqual([4,9,0,4]);
}

@system
unittest
{
	auto spr = run_simulation("input1.bin");
	spr.registers.assertEqual([4,3,4,-3]);
}

@system
unittest
{
	auto spr = run_simulation("input2.bin");
	spr.registers.assertEqual([3,3,4,-1]);
}

@system
unittest
{
	auto spr = run_simulation("input3.bin");
	spr.registers.assertEqual([2,2,3,0]);
}