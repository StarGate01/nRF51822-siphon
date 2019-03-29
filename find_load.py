#!/usr/bin/python

import getpass
import sys
import telnetlib

def set_reg(tn, val):
    print("Halting target")
    tn.write("reset halt\n")
    tn.read_until("> ")
    print("Setting registers to " + str(val))
    for i in range(0, 13):
        tn.write("reg r" + str(i) + " " + str(val) + "\n")
        tn.read_until("> ")
    tn.write("reg sp " + str(val) + "\n")
    tn.read_until("> ")
    print("Registers are now " + str(val))


reg_cont = 0

tn = telnetlib.Telnet("localhost", 4444)
set_reg(tn, reg_cont)

tn.write("exit\n")