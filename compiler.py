# function to make until 1024 lines
def fillTo1024Lines(compiledText: str) -> str:
    compiledText += (1025 - len(compiledText.split('\n'))) * '0000000000000000\n'
    
    return compiledText

# Function to add 1 to a binary number in two's complement algorithm
def addOne(binaryNumber: str) -> str:
    carryOn = 1 # Start with the carry on to add 1
    InvertedResult = ''

    InvertedBinaryNumber = binaryNumber[::-1]

    for bit in InvertedBinaryNumber:
        if carryOn == 1:
            if bit == '0':
                InvertedResult += '1'
                carryOn = 0
            else: # bit == '1'
                InvertedResult += '0'
                carryOn = 1
        else:
            InvertedResult += bit

    if carryOn == 1: # Raise an exception if the result is bigger than the original number
        raise Exception('Overflow')

    result = InvertedResult[::-1]

    return result

# string with decimal to string with binary
def decimalToBinaryOrFillField(decimalNumber: str, length: int) -> str:
    isNegative = False

    # Check if the number is negative, if so, convert it to positive and set the isNegative flag
    if decimalNumber[0] == '-':
        decimalNumber = decimalNumber[1:]
        isNegative = True

    if decimalNumber[0] == 'b':
        decimalNumber = decimalNumber[1:]
        binaryRepresentation = decimalNumber
    else:
        binaryRepresentation = bin(int(decimalNumber))[2:] # Converts it to a binary string and remove the '0b' from the start
    
    # Check if the binary string is bigger than space available
    if len(binaryRepresentation) > length:
        raise Exception('Binary representation of given number is bigger than bits space available')

    # Add zeros or ones to the left
    if len(binaryRepresentation) < length:
        fillQuant = length - len(binaryRepresentation)

        binaryRepresentation = ('0' * fillQuant) + binaryRepresentation

    if isNegative:
        # Invert the bits
        binaryRepresentation = ''.join(['1' if bit == '0' else '0' for bit in binaryRepresentation])
        # Add 1 to the binary number
        binaryRepresentation = addOne(binaryRepresentation)
    
    return binaryRepresentation

# Assembly to binary compiler function
def compiler(inputFile: str, outputFile: str) -> None:
    compiledText = '' # Resulting binary string

    with open(inputFile, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.split('//')[0] # Remove comments
        line = line.strip()

        if(line[:5] == 'nope'): # Case the instruction is No Operation
            compiledText += '0000000000000000\n'
            continue

        inst, parameters = line.split(' ', 1) # Split the instruction and the parameters
        parameters = parameters.replace(' ', '') # Remove spaces

        match(inst):
            # Arithmetic Instructions
            case 'add':
                p1, p2, p3 = parameters.split(',')
                
                p1 = decimalToBinaryOrFillField(p1[1:], 2) # Remove the '&' or '$' from the register address
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3[1:], 4)

                compiledText += f'000001{p1}{p2}{p3}\n'
            
            case 'sub':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3[1:], 4)

                compiledText += f'000010{p1}{p2}{p3}\n'

            # Logic Instructions
            case 'not':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)

                compiledText += f'000011{p1}{p2}0000\n'

            case 'and':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3[1:], 4)

                compiledText += f'000100{p1}{p2}{p3}\n'

            case 'or':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3[1:], 4)

                compiledText += f'000101{p1}{p2}{p3}\n'

            case 'xor':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3[1:], 4)

                compiledText += f'000110{p1}{p2}{p3}\n'

            case 'nand':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3[1:], 4)

                compiledText += f'000111{p1}{p2}{p3}\n'

            case 'nor':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3[1:], 4)

                compiledText += f'001000{p1}{p2}{p3}\n'

            case 'xnor':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3[1:], 4)

                compiledText += f'001001{p1}{p2}{p3}\n'

            # Shift instructions
            case 'sll':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3, 4)

                compiledText += f'001010{p1}{p2}{p3}\n'

            case 'srl':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3, 4)

                compiledText += f'001011{p1}{p2}{p3}\n'

            case 'sra':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3, 4)

                compiledText += f'001100{p1}{p2}{p3}\n'

            case 'tasm':
                p1 = decimalToBinaryOrFillField(parameters[1:], 4)

                compiledText += f'00110100{p1}0000\n'

            case 'tssm':
                p1 = decimalToBinaryOrFillField(parameters[1:], 4)

                compiledText += f'00111000{p1}0000\n'

            # Move instructions
            case 'mtl':
                p1 = decimalToBinaryOrFillField(parameters[1:], 2)

                compiledText += f'001111{p1}00000000\n'

            case 'mfl':
                p1 = decimalToBinaryOrFillField(parameters[1:], 2)

                compiledText += f'010000{p1}00000000\n'

            case 'mth':
                p1 = decimalToBinaryOrFillField(parameters[1:], 2)

                compiledText += f'010001{p1}00000000\n'

            case 'mfh':
                p1 = decimalToBinaryOrFillField(parameters[1:], 2)

                compiledText += f'010010{p1}00000000\n'

            case 'mtac':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)

                compiledText += f'010011{p1}{p2}0000\n'

            case 'mfac':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)

                compiledText += f'010100{p1}{p2}0000\n'

            case 'slt':
                p1, p2, p3 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)
                p3 = decimalToBinaryOrFillField(p3[1:], 4)

                compiledText += f'010101{p1}{p2}{p3}\n'
            
            # Immediate instructions
            case 'addi':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'010110{p1}{p2}\n'    

            case 'subi':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'010111{p1}{p2}\n'

            case 'andi':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'011000{p1}{p2}\n'

            case 'ori':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'011001{p1}{p2}\n'

            case 'xori':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'011010{p1}{p2}\n'

            case 'nandi':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'011011{p1}{p2}\n'

            case 'nori':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'011100{p1}{p2}\n'

            case 'xnori':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'011101{p1}{p2}\n'

            case 'lli':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'011110{p1}{p2}\n'

            case 'lui':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'011111{p1}{p2}\n'

            case 'lsi':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'100000{p1}{p2}\n'

            # Memory access instructions
            case 'lwr':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)

                compiledText += f'100001{p1}{p2}0000\n'

            case 'swr':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2[1:], 4)

                compiledText += f'100010{p1}{p2}0000\n'

            case 'push':
                p1 = decimalToBinaryOrFillField(parameters[1:], 2)

                compiledText += f'100011{p1}00000000\n'

            case 'pop':
                p1 = decimalToBinaryOrFillField(parameters[1:], 2)

                compiledText += f'100100{p1}00000000\n'

            # Control instructions
            case 'jump':
                p1 = decimalToBinaryOrFillField(parameters, 10)

                compiledText += f'100101{p1}\n'

            case 'jal':
                p1 = decimalToBinaryOrFillField(parameters, 10)

                compiledText += f'100110{p1}\n'

            case 'jr':
                p1 = decimalToBinaryOrFillField(parameters[1:], 4)

                compiledText += f'10011100{p1}0000\n'

            case 'jral':
                p1 = decimalToBinaryOrFillField(parameters[1:], 4)

                compiledText += f'10100000{p1}0000\n'

            case 'jgtz':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'101001{p1}{p2}\n'

            case 'jltz':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'101010{p1}{p2}\n'

            case 'jeqz':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'101011{p1}{p2}\n'

            case 'jnez':
                p1, p2 = parameters.split(',')

                p1 = decimalToBinaryOrFillField(p1[1:], 2)
                p2 = decimalToBinaryOrFillField(p2, 8)

                compiledText += f'101100{p1}{p2}\n'

    # Write the compiled text to the output file
    with open(outputFile, 'w') as file:
        file.write(fillTo1024Lines(compiledText))

# Main function
def main():
    fileNameIn = input('Enter file name: ')
    fileNameOut = input('Enter output file name: ')

    compiler(fileNameIn, fileNameOut)

    print('Done!')

# Run the main function
if __name__ == '__main__':
    main()
