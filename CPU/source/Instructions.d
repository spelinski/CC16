import std.array : split;
import std.conv;
import dunit.toolkit;
import std.stdio : writeln;
import SpecialPurposeRegister : SpecialPurposeRegister;

interface CpuInstruction {
    SpecialPurposeRegister perform_operation(SpecialPurposeRegister reg);
}

class Increment : CpuInstruction {
    byte register = 0;

    this(byte reg) {
        register = reg;
    }
    override bool opEquals(Object o) {
        return register == (cast(Increment)o).register;
    }
    SpecialPurposeRegister perform_operation(SpecialPurposeRegister reg) {
        reg.registers[register]++;
        reg.instruction_pointer++;
        return reg;
    }
}

class Decrement : CpuInstruction {
    byte register = 0;

    this(byte reg) {
        register = reg;
    }
    override bool opEquals(Object o) {
        return register == (cast(Decrement)o).register;
    }
    SpecialPurposeRegister perform_operation(SpecialPurposeRegister reg) {
        reg.registers[register]--;
        reg.instruction_pointer++;
        return reg;
    }
}

class Jump : CpuInstruction {
    byte offset = 0;

    this( byte off ) {
        offset = off;
    }
    override bool opEquals(Object o) {
        return offset == (cast(Jump)o).offset;
    }
    SpecialPurposeRegister perform_operation(SpecialPurposeRegister reg) {
        reg.instruction_pointer += ( offset / 2 );
        return reg;
    }
}

class JumpZero : CpuInstruction {
    byte offset = 0;
    byte register = 0;

    this( byte reg, byte off ) {
        offset = off;
        register = reg;
    }
    override bool opEquals(Object o) {
        return register == (cast(JumpZero)o).register &&
               offset == (cast(JumpZero)o).offset;
    }
    SpecialPurposeRegister perform_operation(SpecialPurposeRegister reg) {
        if( reg.registers[register] == 0 ) {
            reg.instruction_pointer += ( offset / 2 );
        } else {
            reg.instruction_pointer++;
        }
        return reg;
    }
}

class Move : CpuInstruction {
    byte destination = 0;
    byte source = 0;

    this(byte dst, byte src) {
        destination = dst;
        source = src;
    }
    override bool opEquals(Object o) {
        return destination == (cast(Move)o).destination &&
               source == (cast(Move)o).source;
    }
    SpecialPurposeRegister perform_operation(SpecialPurposeRegister reg) {
        reg.registers[destination] = reg.registers[source];
        reg.instruction_pointer++;
        return reg;
    }
}

@system
unittest
{
    SpecialPurposeRegister spr = SpecialPurposeRegister();
    auto instr =  new Increment(0);
    spr = instr.perform_operation(spr);
    spr.registers[0].assertEqual(1);
    spr = instr.perform_operation(spr);
    spr.registers[0].assertEqual(2);
    instr = new Increment(1);
    spr = instr.perform_operation(spr);
    spr.registers[1].assertEqual(1);
}

@system
unittest
{
    SpecialPurposeRegister spr = SpecialPurposeRegister();
    auto instr =  new Decrement(0);
    spr = instr.perform_operation(spr);
    spr.registers[0].assertEqual(-1);
    spr = instr.perform_operation(spr);
    spr.registers[0].assertEqual(-2);
    instr = new Decrement(1);
    spr = instr.perform_operation(spr);
    spr.registers[1].assertEqual(-1);
}

@system
unittest
{
    SpecialPurposeRegister spr = SpecialPurposeRegister();
    spr.registers[0] = 3; spr.registers[1] = 4;

    auto instr =  new Move(2, 0);
    spr = instr.perform_operation(spr);
    spr.registers[2].assertEqual(3);

    instr =  new Move(3, 1);
    spr = instr.perform_operation(spr);
    spr.registers[3].assertEqual(4);
}

@system
unittest
{
    SpecialPurposeRegister spr = SpecialPurposeRegister();

    auto instr =  new Jump(4);
    spr = instr.perform_operation(spr);
    spr.instruction_pointer.assertEqual(2);

    instr =  new Jump(-2);
    spr = instr.perform_operation(spr);
    spr.instruction_pointer.assertEqual(1);
}

@system
unittest
{
    SpecialPurposeRegister spr = SpecialPurposeRegister();

    auto instr =  new JumpZero(0, 4);
    spr.registers[0] = 1;
    spr = instr.perform_operation(spr);
    spr.instruction_pointer.assertEqual(1);

    instr =  new JumpZero(0, 4);
    spr.registers[0] = 0;
    spr = instr.perform_operation(spr);
    spr.instruction_pointer.assertEqual(3);

    instr =  new JumpZero(0, -2);
    spr.registers[0] = 1;
    spr = instr.perform_operation(spr);
    spr.instruction_pointer.assertEqual(4);

    instr =  new JumpZero(0, -2);
    spr.registers[0] = 0;
    spr = instr.perform_operation(spr);
    spr.instruction_pointer.assertEqual(3);
}