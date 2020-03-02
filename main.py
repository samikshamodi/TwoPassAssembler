#opcode_table = {'CLA': 0, 'LAC': 1, 'SAC': 2, 'ADD': 3, 'SUB': 4, 'BRZ': 5, 'BRN': 6, 'BRP': 7, 'INP': 8, 'DSP': 9, 'MUL': 10, 'DIV': 11, 'STP': 12, 'DW':13}
opcode_table = {'CLA': '0000', 'LAC': '0001', 'SAC': '0010', 'ADD': '0011', 'SUB': '0100', 'BRZ': '0101', 'BRN': '0110', 'BRP': '0111', 'INP': '1000', 'DSP': '1001', 'MUL': '1010', 'DIV': '1011', 'STP': '1100'}
symbol_table={}
label_table={}
STP_flag=False
i=1


def to_binary(data):
    return('{:012b}'.format(int(data)))

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

def build_label_table(input_file):
    global i
    for j,line in enumerate(input_file):
        if line[0][-1]==':':    #The line has a label
            label_table[line[0][:-1]]=j

def build_symbol_table(input_file):
    global STP_flag
    global i
    for line in input_file:
        if(line[0][-1]==':'): #It has a label
            if(line[1]=='CLA' or line[1]=='STP'):
                if(line[1]=='STP'):
                    STP_flag=True
                if len(line)>2:
                    error_file.write("Too many operands"+str(line))
            elif (line[1] in opcode_table):
                if len(line)>3:
                     error_file.write("Too many operands"+str(line))
                if len(line)<3:
                     error_file.write("Too few operands"+str(line))
                if(line[2] not in label_table):
                    if(line[2] not in symbol_table):
                        if(line[2].isdigit()):
                            symbol_table[line[2]]=int(line[2])
                        else:
                            symbol_table[line[2]]=100+i
                            i+=1
            else:
                print("Invalid opcode",line)
        else:   #It does not have a label
            if(line[0]=='CLA' or line[0]=='STP'):
                if(line[0]=='STP'):
                    STP_flag=True
                if len(line)>1:
                     error_file.write("Too many operands"+str(line))
            elif (line[0] in opcode_table):
                if len(line)>2:
                     error_file.write("Too many operands"+str(line))
                if len(line)<2:
                     error_file.write("Too few operands"+str(line))
                if(line[1] not in label_table):
                    if(line[1] not in symbol_table):
                        if(line[1].isdigit()):
                            symbol_table[line[1]]=int(line[1])
                        else:
                            symbol_table[line[1]]=100+i
                            i+=1
            else:
                 error_file.write("Invalid opcode"+str(line))
    
    if(STP_flag==False):
         error_file.write("STP missing")

def generate_machine_code(input_file):
    for i,line in enumerate(input_file):
        if(line[0][-1]==':'): #It has a label
            if(line[1]=='CLA' or line[1]=='STP'):
                output_file.write("\n"+to_binary(i))
                output_file.write("\t"+opcode_table[line[1]])
            else:
                output_file.write("\n"+to_binary(i))
                output_file.write("\t"+opcode_table[line[1]])
                output_file.write("\t"+to_binary(str(symbol_table[line[2]])))
        else:  #It does not have a label
            if(line[0]=='CLA' or line[0]=='STP'):
                output_file.write("\n"+to_binary(i))
                output_file.write("\t"+opcode_table[line[0]])
            else:
                output_file.write("\n"+to_binary(i))
                output_file.write("\t"+opcode_table[line[0]])
                output_file.write("\t"+to_binary(str(symbol_table[line[1]])))
          

#erasing output.txt file every time the program is run
open("output.txt", "w").close()  
output_file = open("output.txt","a") 

#erasing error.txt file every time the program is run
open("error.txt", "w").close()  
error_file = open("error.txt","a") 

input_file_name=input("Enter input file name: ")   #Takes the file name where the assembly language program is stored
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

#print(input_file)  
input_file = process(input_file)
print("\n",input_file)

build_label_table(input_file)
print("\n",label_table)

build_symbol_table(input_file)
print("\n",symbol_table)

#Add label_table to symbol_table
symbol_table.update(label_table)
print("\n",symbol_table)

generate_machine_code(input_file)
