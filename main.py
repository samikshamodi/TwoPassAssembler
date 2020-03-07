# Samiksha Modi - 2019331
# Vasu Yadav - 2019344
opcode_table = {'CLA': '0000', 'LAC': '0001', 'SAC': '0010', 'ADD': '0011', 'SUB': '0100', 'BRZ': '0101',
                'BRN': '0110', 'BRP': '0111', 'INP': '1000', 'DSP': '1001', 'MUL': '1010', 'DIV': '1011', 'STP': '1100'}
words = {'CLA': 1, 'LAC': 2, 'SAC': 2, 'ADD': 2, 'SUB': 2, 'BRZ': 2,
         'BRN': 2, 'BRP': 2, 'INP': 2, 'DSP': 2, 'MUL': 2, 'DIV': 2, 'STP': 1}
symbol_table = {}  # Stores all the labels and variables
declare_table = []  # Stores all the variables that have been declared
global input_file
global location_counter
ilc = 256  # ilc is instruction location counter


def to_binary(data):
    return('{:012b}'.format(int(data)))


def process():
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


def pass_one():
    global location_counter
    global ilc
    todelete = []  # invalid instructions are daved here to be deleted later
    for line in input_file:
        if line[0][-1] == ':':  # The line has a label
            if line[0][:-1] in symbol_table:
                error_file.write(
                    "\n Symbol defined more than once: " + str(line[0][:-1]))
            else:
                # Add label to symbol table
                symbol_table[line[0][:-1]] = location_counter
                location_counter += 1

            if len(line) == 2:
                if (line[1] != 'CLA' and line[1] != 'STP' and line[1] not in opcode_table):
                    error_file.write("\n Invalid opcode: " + str(line[1]))
                    todelete.append(line)
                    location_counter += 1
                    continue
                else:
                    if(len(line) <= words[line[1]]):
                        error_file.write("\n Too few operands: " + str(line))
                        todelete.append(line)
                    location_counter += 1
                    continue

            if(line[1] in opcode_table):  # Checking if it is a valid opcode
                if(len(line) > words[line[1]]+1):
                    error_file.write("\n Too many operands: " + str(line))
                symbol_table[line[2]] = ilc  # Add variable to symbol table
                ilc += 1
            else:
                error_file.write("\n Invalid opcode: " + str(line[1]))
                todelete.append(line)

        elif len(line) > 1 and (line[1] == 'DS' or line[1] == 'DC'):
            if line[0] in declare_table:
                error_file.write(
                    "\n Symbol defined more than once: " + str(line[0]))
            else:
                declare_table.append(line[0])
                location_counter += 1

        else:  # There is no label
            if len(line) == 1:
                if (line[0] != 'CLA' and line[0] != 'STP' and line[0] not in opcode_table):
                    error_file.write("\n Invalid opcode: " + str(line[0]))
                    todelete.append(line)
                    location_counter += 1
                    continue
                else:
                    if(len(line) < words[line[0]]):
                        error_file.write("\n Too few operands: " + str(line))
                        todelete.append(line)
                    location_counter += 1
                    continue
            if(line[0] in opcode_table):  # Checking if it is a valid opcode
                if(len(line) > words[line[0]]):
                    error_file.write("\n Too many operands: " + str(line))
                location_counter += 1
                if line[1] not in symbol_table:
                    symbol_table[line[1]] = ilc  # Add variable to symbol table
                    ilc += 1
            else:
                error_file.write("\n Invalid opcode: " + str(line[0]))
                todelete.append(line)

    # Removing declarative statements from input_file
    while len(input_file[-1]) == 3 and (input_file[-1][1] == 'DS' or input_file[-1][1] == 'DC'):
        input_file.remove(input_file[-1])

    # Removing todelete from input_file
    for i in todelete:
        input_file.remove(i)


def pass_two():
    for line in input_file:
        if(line[0][-1] == ':'):  # The line has a label
            if(line[1]in opcode_table and line[1] == 'CLA' or line[1] == 'STP'):
                output_file.write("\n"+opcode_table[line[1]])
            elif line[1] in opcode_table:
                output_file.write("\n"+opcode_table[line[1]])
                output_file.write("\t"+to_binary(str(symbol_table[line[2]])))
                # Displays error if symbol is used but not defined
                if((line[2] not in declare_table) or (line[2] not in symbol_table)):
                    error_file.write(
                        "\n Symbol used but not defined: " + str(line[2]))

        else:  # The line does not have a label
            if(line[0]in opcode_table and line[0] == 'CLA' or line[0] == 'STP'):
                output_file.write("\n"+opcode_table[line[0]])
            elif line[0] in opcode_table:
                output_file.write("\n"+opcode_table[line[0]])
                output_file.write("\t"+to_binary(str(symbol_table[line[1]])))
                # Displays error if symbol is used but not defined
                if((line[1] not in declare_table) or (line[1] not in symbol_table)):
                    error_file.write(
                        "\n Symbol used but not defined: " + str(line[1]))


# Erasing output.txt file every time the program is run
open("output.txt", "w").close()
output_file = open("output.txt", "a")

# Erasing error.txt file every time the program is run
open("error.txt", "w").close()
error_file = open("error.txt", "a")

# Takes the file name where the assembly language program is stored
#input_file_name = input("Enter input file name: ")
input_file_name = "input.txt"

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
input_file = process()

# Checks if START is missing. If missing, it reports the error. If present it removes it from input_file list
if input_file[0][0] == 'START':
    if (len(input_file[0])) > 1:
        location_counter = int(input_file[0][1])
        input_file.remove(input_file[0])

else:
    location_counter = 0
    error_file.write("\n START statement is missing")

# Checks if END is missing. If missing, it reports the error. If present it removes it from input_file list
if input_file[-1][0] == 'END':
    input_file.remove(input_file[-1])
else:
    error_file.write("\n END statement is missing")

print("\n", input_file)

# Calls pass_one of the assembler
pass_one()

print("\n Symbol table: ", symbol_table)
print("\n Declare table: ", declare_table)

# Because the address where the program is loaded might overlap with the address where the variable is stored
if(location_counter >= 256):
    error_file.write("\n Memory address of instructions exceed 256")

print("\n New: ", input_file)
pass_two()
