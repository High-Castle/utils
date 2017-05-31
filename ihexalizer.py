#!/usr/bin/env python3
#
# Given an Intel hex file (or MCS file), print the data records (address and
# number of bytes)

import sys

class IHexAlizer:
    line_count = 0
    extended = 0

    def __init__(self, f):
        line = f.readline()
        while line:
            self.line_count += 1

            if line[0] != ':':
                print("Unexpected format on line %d" % self.line_count)
                break
            
            count = int(line[1:3], 16)
            address = int(line[3:7], 16)
            rtype = int(line[7:9], 16)

            if rtype == 1: # End Of File
                break
            elif rtype == 4: # Extended Linear Address
                self.extended = (int(line[9:13], 16) << 16)
            elif rtype == 0: # Data
                print('0x%X (%d bytes)' % (address + self.extended, count))

            line = f.readline()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ihexalizer.py <ihex file>')
        sys.exit(0)

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print('Unable to open \"%s\"' % sys.argv[1])
        sys.exit(1)

    IHexAlizer(f)
    f.close()
