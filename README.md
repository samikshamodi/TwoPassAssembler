# two-pass-assembler
A program in python for two-pass assembler for the 12 bit accumulator architecture.

This project attempts to emulate the working of an assembler by converting the assembly code to machine code.

## Usage
* Open terminal and navigate to the directory where the files are saved. 
* Type python main.py
* Enter input file name when asked.

## Logic & Working
The two pass assembler performs two passes over the source program.

In the first pass, it reads the entire source program. A symbol table having variables and labels with its address assigned is made. To assign address to labels, the assembler maintains a Program Counter.

In the second pass the instructions are again read and are assembled using the symbol table. Basically, the assembler goes through the program one line at a time, and generates machine code for that instruction. Then the assembler proceeds to the next instruction. In this way, the entire machine code is created. 

The program is loaded at memory address 0000 0000 0000 by default.
The number of instructions should not exceed 256.

## Assembler Opcodes
| Opcode | Meaning |	Assembly Opcode |
| ---- | ----------------- | --- |
| 0000 | Clear accumulator |	CLA |
| 0001 | Load into accumulator from address | LAC |
| 0010 | Store accumulator contents into address |	SAC |
| 0011 | Add address contents to accumulator contents | ADD |
| 0100 | Subtract address contents from accumulator contents	| SUB |
| 0101 | Branch to address if accumulator contains zero | BRZ |
| 0110 | Branch to address if accumulator contains negative value | BRN |
| 0111 | Branch to address if accumulator contains positive value | BRP |
| 1000 | Read from terminal and put in address | INP |
| 1000 | Display value in address on terminal | DSP |
| 1010 | Multiply accumulator and address contents | MUL |
| 1011 | Divide accumulator contents by address content. Quotient in R1 and remainder in R2 | DIV |
| 1100 | Stop execution | STP |

## Errors Handled
The folowing are the errors handles in this program
* A symbol has been used but not defined
* A symbol has been defined but not used
* A symbol has been defined more than once 
* The name in the opcode field is not a legal opcode 
* An opcode is not supplied with enough operands 
* An opcode is supplied with too many operands 
* The START statement is missing
* The END statement is missing 
* The number of instructions exceed 256

## Files and There Uses
* output.txt
On successful completion of the program the output.txt will have the machine code for the said assembly code.
* error.txt
In case of Errors during Pass-One or Pass-Two the error.txt will be flooded with the error message.
* main.py
Contains the program to convert the assembly code to machine code.
