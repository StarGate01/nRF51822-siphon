#!/usr/bin/python

import sys
import telnetlib

import helpers

code_size = 0x40000

print("Connecting to Open OCD server at localhost:4444")
tn = telnetlib.Telnet("localhost", 4444)

pc = int(sys.argv[1], 0)
r_addr = int(sys.argv[2])
r_dest = int(sys.argv[3])
print("Dumping code using LDR exploit at " + hex(pc) + ", address: r" + str(r_addr) + ", destination: r" + str(r_dest))

helpers.halt(tn)

for i in xrange(0, code_size, 4):
    data = helpers.siphon(tn, i, pc, r_addr, r_dest)
    print(hex(i) + ": " + hex(data))

tn.write("exit\n")
print("Done")