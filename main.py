# Samiksha Modi - 2019331
# Vasu Yadav - 2019344
opcode_table = {'CLA': '0000', 'LAC': '0001', 'SAC': '0010', 'ADD': '0011', 'SUB': '0100', 'BRZ': '0101',
                'BRN': '0110', 'BRP': '0111', 'INP': '1000', 'DSP': '1001', 'MUL': '1010', 'DIV': '1011', 'STP': '1100'}
symbol_table = {}
label_table = {}
declare_table = []
END_flag = False  # False if no END in program, True if END is present in program
i = 1
program_counter = 0


def declaration_table(input_file):
    global declare_table
    temp_table = []
    # Appending the 'DC' 'DS line in declare_table
    for line in input_file:
        if len(line[0]) == 2:
            declare_table.append(line)

    # Removing 'DC' 'DS' line from input file by storing it in res then return res to input_file
    res = [tt for tt in input_file if tt not in declare_table]

    # Appending just the variable name from declare_table to temp_table
    for line in declare_table:
        temp_table.append(line[1])

    # Copying temp_table to declare_table
    declare_table = temp_table

    # Removing '=' sign from elements in declare_table
    for i, element in enumerate(declare_table):
        if '=' in element:
            declare_table[i] = element[:element.find('=')]

    # Checking if any symbol has been declared twice and removing it
    for element in declare_table:
        temp = declare_table.count(element)
        if temp > 1:
            error_file.write(
                "\n Symbol defined more than once: " + str(element))
            cnt = 1
            while cnt < temp:
                declare_table.remove(element)
                cnt = cnt+1

    return res


def to_binary(data):
    return('{:012b}'.format(int(data)))


def process(input_file):
    # Read it one list element at a time
    for line in input_file:
        # Remove lines having only comment
        if (line.startswith('//')):
            input_file.remove(line)
        # Remove empty lines
        if(line == ''):
            input_file.remove('')

    # Removing all the comments in the line eg CLA //Clear Accumulator converts to CLA
    for iter, line in enumerate(input_file):
        temp = line.find('//')
        if (temp != -1):
            line = line[:temp]
            input_file[iter] = line

    temp = []  # empty list

    for line in input_file:
        line = line.split(' ')
        for element in line:
            # Removing empty elements from line eg ['CLA','']
            if(element == ''):
                line.remove(element)
        temp.append(line)

    # Removing [] from temp
    temp2 = [x for x in temp if x != []]
    return temp2


def pass_one(input_file):

    # Builds the label table
    def build_label_table():
        global program_counter
        for j, line in enumerate(input_file):
            if line[0][-1] == ':':  # The line has a label
                label_table[line[0][:-1]] = j+program_counter

    # Builds the symbol table
    def build_symbol_table():
        global END_flag
        global i
        for line in input_file:
            if(line[0][-1] == ':'):  # The line has a label
                if(line[1] == 'CLA' or line[1] == 'STP' or line[1] == 'END'):
                    if(line[1] == 'END'):
                        END_flag = True
                    if len(line) > 2:
                        error_file.write("\n Too many operands"+str(line))
                elif (line[1] in opcode_table):
                    if len(line) > 3:
                        error_file.write("\n Too many operands"+str(line))
                    if len(line) < 3:
                        error_file.write("\n Too few operands"+str(line))
                    if(line[2] not in label_table):
                        if(line[2] not in symbol_table):
                            if(line[2].isdigit()):
                                symbol_table[line[2]] = int(line[2])
                            else:
                                symbol_table[line[2]] = 256+i
                                i += 1
                else:
                    error_file.write("\n Invalid opcode"+str(line))
                    input_file.remove(line)

            else:  # The line does not have a label
                if(line[0] == 'CLA' or line[0] == 'STP' or line[0] == 'END'):
                    if(line[0] == 'END'):
                        END_flag = True
                    if len(line) > 1:
                        error_file.write("\n Too many operands"+str(line))
                elif (line[0] in opcode_table):
                    if len(line) > 2:
                        error_file.write("\n Too many operands"+str(line))
                    if len(line) < 2:
                        error_file.write("\n Too few operands"+str(line))
                    if(line[1] not in label_table):
                        if(line[1] not in symbol_table):
                            if(line[1].isdigit()):
                                symbol_table[line[1]] = int(line[1])
                            else:
                                symbol_table[line[1]] = 256+i
                                i += 1
                else:
                    error_file.write("\n Invalid opcode"+str(line))
                    input_file.remove(line)

        if(END_flag == False):
            error_file.write("\n END statement is missing")

    build_label_table()
    build_symbol_table()

    print("\n Label table: ", label_table)
    print("\n Symbol table: ", symbol_table)

    for element in symbol_table:
        error_flag = True  # assuming error is there that is a symbol in the symbol is not defined. That is a symbol in the symbol table is not present in declare table
        if element in declare_table:
            error_flag = False
        if error_flag == True:
            error_file.write("\n Symbol used but not defined: " + str(element))

    # Add label table to the symbol table
    symbol_table.update(label_table)
    print("\n Updated symbol table: ", symbol_table)


"""
def pass_two(input_file):
    # Layout in memory
    global program_counter
    for program_counter, line in enumerate(input_file):
        if(line[0][-1] == ':'):  # The line has a label
            if(line[1] == 'CLA' or line[1] == 'STP'):
                output_file.write("\n"+to_binary(program_counter))
                output_file.write("\t"+opcode_table[line[1]])
            else:
                output_file.write("\n"+to_binary(program_counter))
                output_file.write("\t"+opcode_table[line[1]])
                output_file.write("\t"+to_binary(str(symbol_table[line[2]])))
        else:  # The line does not have a label
            if(line[0] == 'CLA' or line[0] == 'STP'):
                output_file.write("\n"+to_binary(program_counter))
                output_file.write("\t"+opcode_table[line[0]])
            else:
                output_file.write("\n"+to_binary(program_counter))
                output_file.write("\t"+opcode_table[line[0]])
                output_file.write("\t"+to_binary(str(symbol_table[line[1]])))"""


def pass_two(input_file):
    global program_counter
    for program_counter, line in enumerate(input_file):
        if(line[0][-1] == ':'):  # The line has a label
            if(line[1] == 'END'):
                continue
            if(line[1] == 'CLA' or line[1] == 'STP'):
                # output_file.write("\n"+to_binary(program_counter))
                output_file.write("\n"+opcode_table[line[1]])
            else:
                # output_file.write("\n"+to_binary(program_counter))
                output_file.write("\n"+opcode_table[line[1]])
                output_file.write("\t"+to_binary(str(symbol_table[line[2]])))
        else:  # The line does not have a label
            if(line[0] == 'END'):
                continue
            if(line[0] == 'CLA' or line[0] == 'STP'):
                # output_file.write("\n"+to_binary(program_counter))
                output_file.write("\n"+opcode_table[line[0]])
            else:
                # output_file.write("\n"+to_binary(program_counter))
                output_file.write("\n"+opcode_table[line[0]])
                output_file.write("\t"+to_binary(str(symbol_table[line[1]])))


def other_errors(input_file):
    # Error: symbol not used
    for element in label_table:
        # error_flag is True if the element in label table is not found as an operand
        error_flag = True
        for line in input_file:
            if(line[0][-1] == ':'):  # The line has a label
                if(line[1] != 'CLA' and line[1] != 'STP' and line[1] != 'END'):
                    # error_flag is made False if the element in label table is found as an operand
                    if element == line[2]:
                        error_flag = False
                        break
            else:  # The line does not have a label
                if(line[0] != 'CLA' and line[0] != 'STP' and line[0] != 'END'):
                    # error_flag is made False if the element in label table is found as an operand
                    if element == line[1]:
                        error_flag = False
                        break

        if error_flag == True:
            error_file.write("\n Symbol not used: "+str(element))

    # Error symbol defined more than once
    for element in label_table:
        error_flag = 0  # error_flag is 0 denoting the element has occurred 0 times so far
        for line in input_file:
            # The line has a label and element in label table is found in the program
            if(line[0][-1] == ':' and line[0][:-1] == element):
                error_flag = error_flag+1   # Increasing error_flag count by 1

        if error_flag > 1:  # element in label table occurs more than once
            error_file.write("\n Symbol defined more than once "+str(element))


# Erasing output.txt file every time the program is run
open("output.txt", "w").close()
output_file = open("output.txt", "a")

# Erasing error.txt file every time the program is run
open("error.txt", "w").close()
error_file = open("error.txt", "a")

# Takes the file name where the assembly language program is stored
input_file_name = input("Enter input file name: ")
#input_file_name = "input.txt"

try:
    input_file = open(input_file_name, "r")
except FileNotFoundError:
    print("No file found. Please retry.")
    exit()

# Reads the entire input file
input_file = input_file.read()

# Splits the input file at new line and converts it to list
input_file = input_file.split("\n")
print("\n", input_file)

# Removes the comments and empty lines
input_file = process(input_file)

# Stores the symbols that have been declared and are not labels
input_file = declaration_table(input_file)
print("\n Declare table: ", declare_table)

# Checks if START is missing. If missing, it reports the error. If present it removes it from input_file list
if input_file[0][0] == 'START':
    if (len(input_file[0])) > 1:
        program_counter = int(input_file[0][1])
    input_file.remove(input_file[0])

else:
    error_file.write("\n START statement is missing")

print("\n", input_file)

# Checking if the no of instructions exceed the maximum no of instructions
if(len(input_file)+program_counter > 256):
    error_file.write("\n Memory address of instructions exceed 256")

# Calls pass_one of the assembler
pass_one(input_file)

# Finds other errors in the assembly language program like symbol not used
other_errors(input_file)

# Write the machine code in output.txt
pass_two(input_file)

