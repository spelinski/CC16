import std.stdio;
import std.string;
import std.algorithm;
import std.getopt;
import std.conv;
import InstructionParser;

void main(string[] args)
{
	string outputFile, inputFile;
	getopt(args, std.getopt.config.required, "output", &outputFile,
		     std.getopt.config.required, "input", &inputFile );

	auto in_file = File(inputFile);
	auto out_file = File(outputFile, "w");
	auto range = in_file.byLine();
	foreach (line; range)
	{
		string line_string = to!string(line);
		auto parser = new InstructionParser();
		out_file.rawWrite([parser.parse_instruction(line_string)]);
	}
	in_file.close();
	out_file.close();
}
