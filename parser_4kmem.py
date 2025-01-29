#-------------------------------------------------------------------------------
# Name:        IntelHex Parser
# Purpose:     IntelHex Parser
#
# Author:      Sehktel
#
# Created:     17.10.2024
# Copyright:   (c) Sehktel 2024
# Licence:     MIT
#-------------------------------------------------------------------------------

import binascii

mem_len = 4096 # 4k memory
memory = [0x00] * mem_len
DEBUG = False

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
##            csum = 0x100 - (csum & 0xFF)

            if DEBUG or csum != checksum:
                print(f' {length:02X}{offset:04X}{optype:02X}', end='', sep='')
                for byte in data:
                    print(f'{byte:02X}', end='', sep='')
                print(f'{checksum:02X}   {csum:02X} -- ', checksum == csum)
        else:
            print (':00000001FF -- finish') if DEBUG else None

    printMemory()

if __name__ == '__main__':
    parse('./blink_p3.hex')











