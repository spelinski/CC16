import Cpu : run_simulation;
import SpecialPurposeRegister : SpecialPurposeRegister;
import std.algorithm;
import std.conv;
import std.format;
import std.getopt;
import std.stdio : writefln;
import std.string;

void main(string[] args)
{
	string inputFile;	
	getopt(args, std.getopt.config.required, "input", &inputFile );

	auto spr = run_simulation( inputFile );

	writefln("Registers:\r\nA: %d B: %d C: %d D: %d",
		spr.registers[0], spr.registers[1], spr.registers[2], spr.registers[3]);
	
}
