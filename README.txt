So a lot of us are programming in C++.  But I think it's time to get back to our roots.  For this challenge, I think I'm going to have to Assemble something a little differently.

 

We're going to define our own assembly language for a 16-bit CPU.  This CPU will have 4 registers (all set to zero to begin with, a,b,c,d).  Each register is 16 bits, and can hold any value between -32768 and 32767.  They are allowed to overflow/underflow (adding 1 to 32767 for example will give you -32768)

We'll also define 5 commands:
inc <reg>	a letter (a,b,c,d) that is the register	Adds 1 to the value in the register
dec <reg>	a letter (a,b,c,d) that is the register	Subtracts 1 to the value in the register
mov <dest-reg> <src-reg>	each param is a single letter (a,b,c,d) indicating register	Copies the value from <src-reg> into <dest-reg>
jmp (offset)	a positive or negative number to unconditionally jump to (the current address is 0x0000 offset) This is the number of bytes to jump	Goes to the instruction at offset.
jnz <reg> offset	

Register is a single letter (a,b,c,d) corresponding register

Offset is a positive or negative number (current address is 0x0000 offset) This is the number of bytes to jump
	Goes to the instruction at offset if the register is not zero

Offsets are limited to 8 bits (from -128 to 127)

The program ends if your current instruction pointer is past any valid instruction

 

So for example:
inc a
inc a
inc a
inc a
inc a
mov b a
dec a
mov c a
jnz c 8
inc b
dec c
jmp -6
mov d a

In this example, we increment a 5 times (a=5), set b to a (a=5, b=5), decrement a (a=4, b=5), set c to a (a=4, b=5, c=4), skip the jump since c is not zero, and then for four times, increment b and decrement c (a=4, b=9, c=0), and then copy a to d (a=4, b=9, c=0, d=4)

Each instruction should be 2 bytes (16 bits).  

For this challenge: we are going to write an assembler and a virtual CPU to execute our instructions.

 

First, you need to write an assembler.  An assember's job is to convert assembly to machine code.  

Create a program that reads in a file containing assembly instructions.  It should create a new file that contains binary instructions for a virtual CPU (which you will also write).  

 

Secondly, its time to write the virtual CPU (it can be the same program with different command line switches if you wish)

Write a program that takes the file that you produced in step 1 and executes the instructions.  At the end of the program, output the contents of each register.

 

Here are the test files I will use
Input 1 - INC, DEC, and MOV only
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
	
inc a
inc b
inc a
inc c
dec b
mov c a
inc c
inc c
inc c
dec d
inc b
mov b a
mov c d
inc d
inc b
dec d
dec d
dec d
inc a
inc a
mov c a
mov b a
mov c b
dec a
mov b a
inc a
Input 2 - Adding jmps
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
	
inc a
inc b
jmp 2
inc a
inc c
dec b
mov c a
inc c
inc c
inc c
dec d
jmp 4
inc b
mov b a
mov c d
jmp 2
jmp 8
inc d
inc b
dec d
jmp 6
dec d
dec d
inc a
inc a
mov c a
mov b a
mov c b
dec a
mov b a
jmp 12
inc a
jmp -2
Input 3 - Adding jnz
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
	
inc a
jnz b 4
inc b
jmp 4
jmp 0
inc a
inc c
inc c
inc c
inc c
inc c
jnz c 8
dec c
inc b
jmp -6
dec b
mov c a
inc c
inc c
inc c
dec d
jmp 4
inc b
mov b a
mov c d
jmp 2
jmp 8
inc d
inc b
dec d
jmp 6
dec d
dec d
jnz d 10
dec d
inc a
dec c
jmp -8
inc a
inc a
mov c a
mov b a
mov c b
dec a
mov b a
jmp 12
inc a
jmp -2

 
Goal/Scoring

Your goal is to fix the bugs in the program to get the correct standard deviation.  There are 3 bugs (that I know of) that are directly contributing to this problem.  

Scoring:

+100 for writing a working assembler

+50 points if you document what bit mapping each instruction has (can be in a comment if you want)

+100 for solving input 1

+ 100 for solving input 2

+150 for solving input 3

+20 if you can tell me what you can change to make the program smaller in size (you must keep it a 16 bit architecture, and the instructions must stay the same).  What trade-offs do you have if you make your change?



