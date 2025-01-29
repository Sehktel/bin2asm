#-------------------------------------------------------------------------------
# Name:        IHTFG
# Purpose:     IntelHex Test File Generator
#
# Author:      Sehktel
#
# Created:     29.01.2025
# Copyright:   (c) Sehktel 2025
# Licence:     MIT
#-------------------------------------------------------------------------------

def checksum(line):
    sum = 0
    aa = bytes.fromhex(line)
    for a in aa:
        sum += a
    sum = ((~sum) + 1) & 0xFF
    return sum



def main():
    addr = 0x0000
    for i in range (0xFF + 1):
        instructions = ''
        for j in range(6):
            instructions += format(i, '02X')

        ih_line = '06' + format(addr, '04X') + '00' + instructions
        cc = checksum(ih_line)
        ih_line = ':' + ih_line + format(cc, '02X')
        addr += 6
        print(ih_line)
    print(':00000001FF')

if __name__ == '__main__':
    main()
