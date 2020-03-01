"""opcode_table = {'CLA': 0, 'LAC': 1, 'SAC': 2, 'ADD': 3, 'SUB': 4, 'BRZ': 5, 'BRN': 6, 'BRP': 7, 'INP': 8, 'DSP': 9, 'MUL': 10, 'DIV': 11, 'STP': 12, 'DW':13}

print('{0:04b}'.format(opcode_table['LAC']))
"""


def process(input_file):
    """ Reads assembly file and removes unecessary data like comments and new lines"""
    # Read it one list element at a time
    for line in input_file:
        # Remove lines having only comment
        if (line.startswith('//')):
            input_file.remove(line)
        # Remove empty lines
        if(line == ''):
            input_file.remove('')

    # Removing all the comments in the line eg CLA //Clear Accumulator
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


# input_file_name=input("Enter input file address: ")   #Takes the file name where the assembly language program is stored
input_file_name = "input.txt"  # TODO remove this line later

try:
    input_file = open(input_file_name, "r")
except FileNotFoundError:
    print("No file found. Please retry.")
    exit()

# Reads the entire input file
input_file = input_file.read()

# Splits the input file at new line and converts it to list
input_file = input_file.split("\n")

print(input_file)  # TODO remove this line later
input_file = process(input_file)
print(input_file)
