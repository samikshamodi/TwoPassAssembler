opcode_table = {'CLA': '0000', 'LAC': '0001', 'SAC': '0010', 'ADD': '0011', 'SUB': '0100', 'BRZ': '0101',
                'BRN': '0110', 'BRP': '0111', 'INP': '1000', 'DSP': '1001', 'MUL': '1010', 'DIV': '1011', 'STP': '1100'}
length_of_inst = {'CLA': 1, 'LAC': 2, 'SAC': 2, 'ADD': 2, 'SUB': 2, 'BRZ': 2,
                  'BRN': 2, 'BRP': 2, 'INP': 2, 'DSP': 2, 'MUL': 2, 'DIV': 2, 'STP': 1}
symbol_table = {}
declare_table = []
global input_file
global location_counter
ilc = 256


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


def declaration_table():
    global declare_table
    temp_table = []
    # Appending the 'DC' 'DS line in declare_table
    while len(input_file[-1]) == 3 and (input_file[-1][1] == 'DS' or input_file[-1][1] == 'DC'):
        declare_table.append(input_file[-1][0])
        input_file.remove(input_file[-1])

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


def pass_one():
    global location_counter
    global ilc
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
                    location_counter += 1
                    continue
                else:
                    if(len(line) <= length_of_inst[line[1]]):
                        error_file.write("\n Too few operands: " + str(line))
                    location_counter += 1
                    continue

            if(line[1] in opcode_table):  # Checking if it is a valid opcode
                if(len(line) > length_of_inst[line[1]]+1):
                    error_file.write("\n Too many operands: " + str(line))
                symbol_table[line[2]] = ilc  # Add variable to symbol table
                ilc += 1
            else:
                error_file.write("\n Invalid opcode: " + str(line[1]))

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
                    location_counter += 1
                    continue
                else:
                    if(len(line) < length_of_inst[line[0]]):
                        error_file.write("\n Too few operands: " + str(line))
                    location_counter += 1
                    continue
            if(line[0] in opcode_table):  # Checking if it is a valid opcode
                if(len(line) > length_of_inst[line[0]]):
                    error_file.write("\n Too many operands: " + str(line))
                location_counter += 1
                if line[1] not in symbol_table:
                    symbol_table[line[1]] = ilc  # Add variable to symbol table
                    ilc += 1
            else:
                error_file.write("\n Invalid opcode: " + str(line[0]))


# TODO error used but not defined in not in declare table OR in symbol table.
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


# Stores the symbols that have been declared and are not labels
# declaration_table()
#print("\n Declare table: ", declare_table)

print("\n", input_file)

pass_one()
print(symbol_table)
print("\n Declare table: ", declare_table)
