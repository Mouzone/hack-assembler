# returns 16 bit binary
def decimalToBinary(integer):
    output = ""
    while integer > 0:
        output = integer % 2 + output
        integer = integer // 2

    zeroes_to_add = 16 - len(output)
    return zeroes_to_add * "0" + output


def cleanFile(file):
    lines = file.readlines()
    lines_no_whitespace = [line.strip() for line in lines]
    lines_no_comments = [line for line in lines_no_whitespace if line[0] != "/" or line]
    return lines_no_comments


def readASMFile(file_name):
    with open(f"./test_files/{file_name}") as file:
        file_cleaned = cleanFile(file)
        file_no_labels = parseLabels(file_cleaned)
        parseVariables(file_no_labels)
        parseFile(file_no_labels)
    return


def parseLabels(file):
    line_number = 0
    for line in file:
        if line[0] == "(":
            label = line[1:-1]
            symbols[label] = line_number + 1
        line_number += 1

    lines_no_labels = [line for line in file if line[0] != "("]
    return lines_no_labels


def parseVariables(file):
    # starts at 16
    register = 16
    for line in file:
        if line[0] == "@" and line[1:] not in symbols.keys():
            symbols[line[1:]] = register
            register += 1


def parseFile(file):
    # write to output file
    # starts with @ write it as a_instruction "0 +..."
    # else write is as c_instruction "111 + a + cccccc + ddd + jjj
    for line in file:
        if line[0] == "@":
            parseAInstruction(line)
        else:
            parseCInstruction(line)
    return

# a_instruction "..."
def parseAInstruction(line):
    symbol = line[1:]
    value = symbols[symbol]
    output = decimalToBinary(value)
    return output

# c_instruction "111 + a + cccccc + ddd + jjj
def parseCInstruction(line):
    output = "111"
    

symbols = {"R0": 0,
           "R1": 1,
           "R2": 2,
           "R3": 3,
           "R4": 4,
           "R5": 5,
           "R6": 6,
           "R7": 7,
           "R8": 8,
           "R9": 9,
           "R10": 10,
           "R11": 11,
           "R12": 12,
           "R13": 13,
           "R14": 14,
           "R15": 15,
           "Screen": 16384,
           "KBD": 24576,
           "SP": 0,
           "LCL": 1,
           "ARG": 2,
           "THIS": 3,
           "THAT": 4}
file_name = input("Enter filename")
readASMFile(file_name)
