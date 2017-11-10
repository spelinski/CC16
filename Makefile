all: example input1 input2 input3

test:
	cd Assembler; dub test
	cd CPU; dub test

example: assembler cpu
	Assembler/assembler --input example.asm --output example.bin
	CPU/cpu --input example.bin

input1: assembler cpu
	Assembler/assembler --input input1.asm --output input1.bin
	CPU/cpu --input input1.bin

input2: assembler cpu
	Assembler/assembler --input input2.asm --output input2.bin
	CPU/cpu --input input2.bin

input3: assembler cpu
	Assembler/assembler --input input3.asm --output input3.bin
	CPU/cpu --input input3.bin

assembler:
	cd Assembler; dub build

cpu:
	cd CPU; dub build

clean:
	cd Assembler; dub clean
	cd CPU; dub clean

