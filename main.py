import re
import os
import glob


# returns 16 bit binary
def decimalToBinary(integer):
    output = ""
    while integer > 0:
        output = str(integer % 2) + output
        integer = integer // 2

    zeroes_to_add = 16 - len(output)
    return zeroes_to_add * "0" + output


def cleanFile(file):
    lines = file.readlines()
    lines_no_whitespace = [line.strip() for line in lines]
    lines_no_comments = [line for line in lines_no_whitespace if line and line[0] != "/"]
    return lines_no_comments


def readASMFile(file_path, file_name):
    with open(file_path) as file:
        file_cleaned = cleanFile(file)  # remove whitespace and comments
        file_no_labels = parseLabels(file_cleaned)  # remove and parse labels
        parseVariables(file_no_labels)  # parse variables
        parseFile(file_no_labels, file_name)  # parse entirety of file
    return


def parseLabels(file):
    line_number = 0
    for line in file:
        if line[0] == "(":
            label = line[1:-1].lower()
            symbols[label] = line_number + 1
        line_number += 1

    lines_no_labels = [line for line in file if line[0] != "("]
    return lines_no_labels


def parseVariables(file):
    # starts at 16
    register = 16
    for line in file:
        if line[0] == "@" and line[1:] not in symbols.keys() and not line[1:].isdigit():
            print(line)
            symbols[line[1:]] = register
            register += 1


def parseFile(file_to_read, file_name):
    # write to output file
    # starts with @ write it as a_instruction "0 +..."
    # else write is as c_instruction "111 + a + cccccc + ddd + jjj
    file_name_cleaned = file_name.split(".")[0]
    with open(f'./output_files/{file_name_cleaned}.hack', 'w') as file_to_write:
        for line in file_to_read:
            if line[0] == "@":
                file_to_write.write(parseAInstruction(line))
            else:
                file_to_write.write(parseCInstruction(line))
            file_to_write.write("\n")


def parseAInstruction(line):
    symbol = line[1:]
    if symbol in symbols.keys():
        value = symbols[symbol]
        output = decimalToBinary(value)
    else:
        output = decimalToBinary(int(symbol))
    return output


# c_instruction "111 + a + cccccc + ddd + jjj
def parseCInstruction(line):
    output = "111"
    result = re.split(r'[=;]', line)

    jump = parseJump(result[1].strip())
    if jump == "000":
        dest = parseDest(result[0])
        comp = parseAandComp(result[1])
        output = output + comp + dest
    else:
        comp = parseAandComp(result[0])
        output = output + comp + "000"
    output += jump
    return output


def parseAandComp(comp):
    output = ""
    if "M" in comp:
        output = "1"
        comp_letter = "M"
    else:
        output = "0"
        comp_letter = "A"

    if comp == "0":
        return output + "101010"
    elif comp == "1":
        return output + "111111"
    elif comp == "-1":
        return output + "111010"
    elif comp == "D":
        return output + "001100"
    elif comp == comp_letter:
        return output + "110000"
    elif comp == "!D":
        return output + "001101"
    elif comp == f"!{comp_letter}":
        return output + "110001"
    elif comp == "-D":
        return output + "001111"
    elif comp == f"-{comp_letter}":
        return output + "110011"
    elif comp == "D+1":
        return output + "011111"
    elif comp == f"{comp_letter}+1":
        return output + "110111"
    elif comp == "D-1":
        return output + "001110"
    elif comp == f"{comp_letter}-1":
        return output + "110010"
    elif comp == f"D+{comp_letter}":
        return output + "000010"
    elif comp == f"D-{comp_letter}":
        return output + "010011"
    elif comp == f"{comp_letter}-D":
        return output + "000111"
    elif comp == f"D&{comp_letter}":
        return output + "000000"
    else:
        return output + "010101"


def parseDest(dest):
    if "A" in dest:
        output = "1"
    else:
        output = "0"

    if "D" in dest:
        output += "1"
    else:
        output += "0"

    if "M" in dest:
        output += "1"
    else:
        output += "0"

    return output


def parseJump(jump):
    if jump == "JMP":
        return "111"
    elif jump == "JGT":
        return "001"
    elif jump == "JEQ":
        return "010"
    elif jump == "JGE":
        return "010"
    elif jump == "JLT":
        return "100"
    elif jump == "JNE":
        return "101"
    elif jump == "JLE":
        return "110"
    else:
        return "000"


def cleanFolder(file_path):
    files = glob.glob(os.path.join(file_path, '*'))
    for file in files:
        try:
            os.remove(file)
            print(f'Successfully deleted {file}')
        except Exception as e:
            print(f'Error deleting {file}: {e}')


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


def run():
    input_path = "./test_files"
    output_path = "./output_files"
    cleanFolder(output_path)
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        readASMFile(file_path, filename)


run()
