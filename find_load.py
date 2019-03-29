#!/usr/bin/python

import sys
import telnetlib

def halt(tn):
    tn.write("reset halt\n")
    tn.read_until("xPSR")
    tn.read_until("> ")

def reg_all(tn, val):
    for i in range(0, 13):
        tn.write("reg r" + str(i) + " " + str(val) + "\n")
        tn.read_until("> ")
    tn.write("reg sp " + str(val) + "\n")
    tn.read_until("> ")

def reg_dump(tn):
    tn.write("reg\n")
    tn.read_until("arm v7m registers")
    print tn.read_until("=====")

def pc_set(tn, addr):
    tn.write("reg pc " + str(addr) + "\n")
    tn.read_until("> ")

def pc_get(tn):
    tn.write("reg pc\n")
    tn.read_until(": ")
    return int(tn.read_until("\n"), 0)
    
def step(tn):
    tn.write("step\n")
    tn.read_until("> ")


reg_cont = 0
search_length = 64

tn = telnetlib.Telnet("localhost", 4444)

print("Halting target")
halt(tn)
pc = pc_get(tn)
print("Program counter is " + str(pc))

for i in xrange(pc, pc + (search_length * 2), 2):
    print("Setting program counter to " + str(i))
    pc_set(tn, i)
    print("Zeroing registers")
    reg_all(tn, 0)
    print("Executing current instruction")
    step(tn)
    print("Dumping registers")
    reg_dump(tn)

tn.write("exit\n")