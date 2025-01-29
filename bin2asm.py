#-------------------------------------------------------------------------------
# Name:        Bin2Asm
# Purpose:     Binary 2 Asm C51 Translator
#
# Author:      Sehktel
#
# Created:     28.01.2025
# Copyright:   (c) Sehktel 2025
# Licence:     MIT
#-------------------------------------------------------------------------------

# Read Correct IntelHex Format File
# Disassemble it into
# Address: Hex: Assember code

from instructions import Instructions_Full
from instructions import Instructions_NoCode


import binascii

mem_len = 4096 # 4k memory
memory = [0x00] * mem_len
DEBUG = False

def opcode1(address, opcode, b1, b2):
    print(f"0x{address:04X} : {opcode[1]}")


def opcode2(address, opcode, b1, b2):
    tag = opcode[4]
    match tag:
        case '':
            print(f"0x{address:04X} : {opcode[1]} 0x{b1:02X}")
        case '#':
            print(f"0x{address:04X} : {opcode[1]}, #0x{b1:02X}")
        case '/':
            print(f"0x{address:04X} : {opcode[1]}, /0x{b1:02X}")
        case _:
            print(f"0x{address:04X} : {opcode[1]} 0x{b1:02X}, {tag}")

def opcode3(address, opcode, b1, b2):
    tag = opcode[4]
    match opcode[2]:
        case 1:
            match tag:
                case '':
                    print(f"0x{address:04X} : {opcode[1]} 0x{b1:02X}, 0x{b2:02X}")
                case '#':
                    print(f"0x{address:04X} : {opcode[1]} 0x{b1:02X}, #0x{b2:02X}")
                case '$':
                    print(f"0x{address:04X} : {opcode[1]} #0x{b1:02X}, 0x{b2:02X}")

        case 2:
            match tag:
                case '':
                    print(f"0x{address:04X} : {opcode[1]} 0x{b1:02X}{b2:02X}")
                case '#':
                    print(f"0x{address:04X} : {opcode[1]} #0x{b1:02X}{b2:02X}")

def disasmMemory():
    global mem_len, memory
    i = 0
    while i < mem_len:
        if memory[i] != 0x00:
            instruction_len = Instructions_NoCode[memory[i]][0]
            match instruction_len:
                case 1:
                    opcode1(i, Instructions_NoCode[memory[i]], 0x00,        0x00)
                case 2:
                    opcode2(i, Instructions_NoCode[memory[i]], memory[i+1], 0x00)
                case 3:
                    opcode3(i, Instructions_NoCode[memory[i]], memory[i+1], memory[i+2])
            i += instruction_len
        else:
            i += 1

def printMemory():
    global mem_len, memory
    page = 32
    blank = [0] * page

    for i in range(0, mem_len - page, page):
        if (memory [i: i + page] != blank):
            print(f'{i:04X}:', end = '')
            for p in range(page):
                print('  ', end='') if p % 8 == 0 else None
                print(f'{memory[i + p]:02X}', end = '')
            print()

def parse(file = './test.hex'):
    global DEBUG, mem_len, memory

    f = open(file, 'r', encoding="utf-8")
    for line in f.readlines():
        line = line.strip()
        print(line) if DEBUG else None
        if line != ':00000001FF':
            length = int(line[1:3], 16)
            offset = int(line[3:7], 16)
            optype = int(line[7:9], 16)
            data = [0] * length
            data = binascii.unhexlify(line[9: -2])
            checksum = int(line[-2:], 16)

            memory[offset: offset + len(data)] = data

            cc = binascii.unhexlify(line[1:-2])
            csum = 0
            for c in cc:
                csum += c
            csum = ((~csum) + 1) & 0xFF
##            csum = (0x100 - (csum & 0xFF)) & 0xFF

            if DEBUG or csum != checksum:
                print(f' {length:02X}{offset:04X}{optype:02X}', end='', sep='')
                for byte in data:
                    print(f'{byte:02X}', end='', sep='')
                print(f'{checksum:02X}   {csum:02X} -- ', checksum == csum)
        else:
            print (':00000001FF -- finish') if DEBUG else None

    printMemory()
    disasmMemory()

if __name__ == '__main__':
    parse('./ihtfg.hex')













memory = [0] * 4096 # 4K ОЗУ

def parseIntelHex(file):
    pass

def main():
    pass

if __name__ == '__main__':
    main()
