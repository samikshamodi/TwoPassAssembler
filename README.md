# Two Pass Assembler
A program in python for two-pass assembler for the 12 bit accumulator architecture.

This project attempts to emulate the working of an assembler by converting the assembly code to machine code.

## Usage
* Open terminal and navigate to the directory where the files are saved. 
* Type python main.py
* Enter input file name when asked.

## Working of a Two Pass Assembler
### First Pass:
![Annotation 2020-03-09 121049](https://user-images.githubusercontent.com/55681035/76188959-7377b080-61ff-11ea-92fc-12342b89da72.jpg)

### Second Pass:
![Annotation 2020-03-09 121309](https://user-images.githubusercontent.com/55681035/76189124-e84aea80-61ff-11ea-91c4-4ba5b87de057.jpg)

## Logic Used Here
The two pass assembler performs two passes over the source program.

In the first pass, it reads the entire source program. A symbol table having variables and labels with its address assigned is made. To assign address to labels, the assembler maintains a Location Counter.

In the second pass the instructions are again read and are assembled using the symbol table. Basically, the assembler goes through the program one line at a time, and generates machine code for that instruction. Then the assembler proceeds to the next instruction. In this way, the entire machine code is created. 

The program is loaded at memory address 0 by default.
The memory address of instructions should not exceed 256 as then the same address might be assigned to an instruction and a variable.

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
* A symbol has been defined more than once 
* The name in the opcode field is not a legal opcode 
* An opcode is not supplied with enough operands 
* An opcode is supplied with too many operands 
* The START statement is missing
* The END statement is missing 

## Strategy for Error Handling
The input code file is read line by line and the comments and empty lines removed.
It checks if the input code file starts with a START statment. If the START statement is not found then it shows error - The START statement is missing.
It checks if the input code file ends with an END statement. If the END statement is not found then it shows error - The END statement is missing.

During the first pass of the assembler,
it first checks if there is a label. If the label is already present in the symbol table then it shows the error - a symbol has been defined more than once.
It then searches for the opcode in the opcode table. If it is not found then it shows the error -  The name in the opcode field is not a legal opcode. 
For a legal opcode, if the length(instruction line read) is less than the required no of fields then it shows the error - an opcode not supplied with enough operands. 
For a legal opcode, if the length(instruction line read) is more than the required no of fields then it shows the error - an opcode not supplied with too many operands. 

During the second pass of the assembler,
If the symbol being printed in output.txt is not found in the declare table then it shows the error - a symbol has been used but not defined. 

## Files and There Uses
* output.txt
On successful completion of the program the output.txt will have the machine code for the said assembly code.
* error.txt
In case of Errors during Pass-One or Pass-Two the error.txt will be flooded with the error message.
* main.py
Contains the program to convert the assembly code to machine code.
