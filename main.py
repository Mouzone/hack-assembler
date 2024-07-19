# prompt and search test_files for the file name
def binaryToDecimal(integer):
    output = ""
    while integer > 0:
        output = integer % 2 + output
        integer = integer // 2

    zeroes_to_add = 16 - len(output)
    return zeroes_to_add * "0" + output


def readASMFile(file_name):
    line_number = 0
    with open(f"./test_files/{file_name}") as file:
        parseLabels(file)
        parseVariables(file)
        parseInstructions(file)
    return


def parseLabels(file):
    # fill symbols with labels and the appropriate line number
    return


def parseVariables(file):
    # fill symbols with variables and the appropriate register number
    # starts at 16
    return


def parseInstructions(file):
    # write to output file
    return


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
