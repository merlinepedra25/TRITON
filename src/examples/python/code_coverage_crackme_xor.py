#!/usr/bin/env python3
## -*- coding: utf-8 -*-
##
## Output:
##
##  $ ./code_coverage_crackme_xor.py
##  Seed injected: {4096: '?'}
##  Seed injected: {4096: 'e'}
##  Seed injected: {4096: '\x00'}
##  Seed injected: {4097: 'l', 4096: 'e'}
##  Seed injected: {4097: 'p', 4096: 'e'}
##  Seed injected: {4097: 'l', 4096: 'e', 4098: 'i'}
##  Seed injected: {4097: '\x00', 4096: 'e'}
##  Seed injected: {4097: 'l', 4096: 'e', 4098: '$'}
##  Seed injected: {4097: 'l', 4096: 'e', 4098: 'i', 4099: 't'}
##  Seed injected: {4096: 'e', 4097: '\x0c'}
##  Seed injected: {4096: 'e', 4098: 'l', 4097: 'l'}
##  Seed injected: {4096: 'e', 4099: '\x00', 4098: 'i', 4097: 'l'}
##  Seed injected: {4096: 'e', 4099: 't', 4098: 'i', 4097: 'l', 4100: 'e'}
##  Seed injected: {4097: 'l', 4096: 'e', 4098: '@'}
##  Seed injected: {4098: 'i', 4099: 't', 4096: 'e', 4100: '\x00', 4097: 'l'}
##  Seed injected: {4097: 'P', 4096: 'e'}
##  Seed injected: {4097: 'l', 4098: 'L', 4096: 'e'}
##  Seed injected: {4099: 'l', 4097: 'l', 4098: 'i', 4096: 'e'}
##  Seed injected: {4098: '\x00', 4096: 'e', 4097: 'l'}
##

from __future__ import print_function
from triton     import TritonContext, ARCH, Instruction, MemoryAccess, CPUSIZE, MODE
import  sys


# Isolated function code which must be cover. The source code
# of this function is basically:
#
#     /* Global serial */
#     char *serial = "\x31\x3e\x3d\x26\x31";
#
#     int check(char *ptr)
#     {
#       int i = 0;
#
#       while (i < 5){
#         if (((ptr[i] - 1) ^ 0x55) != serial[i])
#           return 1;
#         i++;
#       }
#       return 0;
#     }
#
# The objective is to cover this function and so return 1.
#
function = {
                                               #   <serial> function
  0x40056d: b"\x55",                           #   push    rbp
  0x40056e: b"\x48\x89\xe5",                   #   mov     rbp,rsp
  0x400571: b"\x48\x89\x7d\xe8",               #   mov     QWORD PTR [rbp-0x18],rdi
  0x400575: b"\xc7\x45\xfc\x00\x00\x00\x00",   #   mov     DWORD PTR [rbp-0x4],0x0
  0x40057c: b"\xeb\x3f",                       #   jmp     4005bd <check+0x50>
  0x40057e: b"\x8b\x45\xfc",                   #   mov     eax,DWORD PTR [rbp-0x4]
  0x400581: b"\x48\x63\xd0",                   #   movsxd  rdx,eax
  0x400584: b"\x48\x8b\x45\xe8",               #   mov     rax,QWORD PTR [rbp-0x18]
  0x400588: b"\x48\x01\xd0",                   #   add     rax,rdx
  0x40058b: b"\x0f\xb6\x00",                   #   movzx   eax,BYTE PTR [rax]
  0x40058e: b"\x0f\xbe\xc0",                   #   movsx   eax,al
  0x400591: b"\x83\xe8\x01",                   #   sub     eax,0x1
  0x400594: b"\x83\xf0\x55",                   #   xor     eax,0x55
  0x400597: b"\x89\xc1",                       #   mov     ecx,eax
  0x400599: b"\x48\x8b\x15\xa0\x0a\x20\x00",   #   mov     rdx,QWORD PTR [rip+0x200aa0]        # 601040 <serial>
  0x4005a0: b"\x8b\x45\xfc",                   #   mov     eax,DWORD PTR [rbp-0x4]
  0x4005a3: b"\x48\x98",                       #   cdqe
  0x4005a5: b"\x48\x01\xd0",                   #   add     rax,rdx
  0x4005a8: b"\x0f\xb6\x00",                   #   movzx   eax,BYTE PTR [rax]
  0x4005ab: b"\x0f\xbe\xc0",                   #   movsx   eax,al
  0x4005ae: b"\x39\xc1",                       #   cmp     ecx,eax
  0x4005b0: b"\x74\x07",                       #   je      4005b9 <check+0x4c>
  0x4005b2: b"\xb8\x01\x00\x00\x00",           #   mov     eax,0x1
  0x4005b7: b"\xeb\x0f",                       #   jmp     4005c8 <check+0x5b>
  0x4005b9: b"\x83\x45\xfc\x01",               #   add     DWORD PTR [rbp-0x4],0x1
  0x4005bd: b"\x83\x7d\xfc\x04",               #   cmp     DWORD PTR [rbp-0x4],0x4
  0x4005c1: b"\x7e\xbb",                       #   jle     40057e <check+0x11>
  0x4005c3: b"\xb8\x00\x00\x00\x00",           #   mov     eax,0x0
  0x4005c8: b"\x5d",                           #   pop     rbp
  0x4005c9: b"\xc3",                           #   ret
}

Triton = TritonContext()



# This function emulates the code.
def run(ip):
    while ip in function:
        # Build an instruction
        inst = Instruction()

        # Setup opcode
        inst.setOpcode(function[ip])

        # Setup Address
        inst.setAddress(ip)

        # Process everything
        Triton.processing(inst)

        # Display instruction
        #print(inst)

        # Next instruction
        ip = Triton.getRegisterAst(Triton.registers.rip).evaluate()
    return



# This function initializes the context memory.
def initContext():
    # Define the address of the serial pointer. The address of the serial pointer
    # must be the same that the one hardcoded into the targeted function. However,
    # the serial pointer (here 0x900000) is arbitrary.
    Triton.setConcreteMemoryValue(0x601040, 0x00)
    Triton.setConcreteMemoryValue(0x601041, 0x00)
    Triton.setConcreteMemoryValue(0x601042, 0x90)

    # Define the serial context. We store the serial content located on our arbitrary
    # serial pointer (0x900000).
    Triton.setConcreteMemoryValue(0x900000, 0x31)
    Triton.setConcreteMemoryValue(0x900001, 0x3e)
    Triton.setConcreteMemoryValue(0x900002, 0x3d)
    Triton.setConcreteMemoryValue(0x900003, 0x26)
    Triton.setConcreteMemoryValue(0x900004, 0x31)

    # Point RDI on our buffer. The address of our buffer is arbitrary. We just need
    # to point the RDI register on it as first argument of our targeted function.
    Triton.setConcreteRegisterValue(Triton.registers.rdi, 0x1000)

    # Setup stack on an abitrary address.
    Triton.setConcreteRegisterValue(Triton.registers.rsp, 0x7fffffff)
    Triton.setConcreteRegisterValue(Triton.registers.rbp, 0x7fffffff)
    return



# This function returns a set of new inputs based on the last trace.
def getNewInput():
    # Set of new inputs
    inputs = list()

    # Get path constraints from the last execution
    pco = Triton.getPathConstraints()

    # Get the astContext
    astCtxt = Triton.getAstContext()

    # We start with any input. T (Top)
    previousConstraints = astCtxt.equal(astCtxt.bvtrue(), astCtxt.bvtrue())

    # Go through the path constraints
    for pc in pco:
        # If there is a condition
        if pc.isMultipleBranches():
            # Get all branches
            branches = pc.getBranchConstraints()
            for branch in branches:
                # Get the constraint of the branch which has been not taken
                if branch['isTaken'] == False:
                    # Ask for a model
                    models = Triton.getModel(astCtxt.land([previousConstraints, branch['constraint']]))
                    seed   = dict()
                    for k, v in list(models.items()):
                        # Get the symbolic variable assigned to the model
                        symVar = Triton.getSymbolicVariable(k)
                        # Save the new input as seed.
                        seed.update({symVar.getOrigin(): chr(v.getValue())})
                    if seed:
                        inputs.append(seed)

        # Update the previous constraints with true branch to keep a good path.
        previousConstraints = astCtxt.land([previousConstraints, pc.getTakenPredicate()])

    # Clear the path constraints to be clean at the next execution.
    Triton.clearPathConstraints()

    return inputs


def symbolizeInputs(seed):
    # Clean symbolic state
    Triton.concretizeAllRegister()
    Triton.concretizeAllMemory()
    for address, value in list(seed.items()):
        Triton.setConcreteMemoryValue(address, ord(value))
        Triton.symbolizeMemory(MemoryAccess(address, CPUSIZE.BYTE))
        Triton.symbolizeMemory(MemoryAccess(address+1, CPUSIZE.BYTE))
    return


if __name__ == '__main__':

    # Set the architecture
    Triton.setArchitecture(ARCH.X86_64)

    # Symbolic optimization
    Triton.setMode(MODE.ALIGNED_MEMORY, True)

    # Define entry point
    ENTRY = 0x40056d

    # We start the execution with a random value located at 0x1000.
    lastInput = list()
    worklist  = list([{0x1000: '?'}])

    while worklist:
        # Take the first seed
        seed = worklist[0]

        print('Seed injected:', seed)

        # Symbolize inputs
        symbolizeInputs(seed)

        # Init context memory
        initContext()

        # Emulate
        run(ENTRY)

        lastInput += [dict(seed)]
        del worklist[0]

        newInputs = getNewInput()
        for inputs in newInputs:
            if inputs not in lastInput and inputs not in worklist:
                worklist += [dict(inputs)]

    sys.exit(0)

