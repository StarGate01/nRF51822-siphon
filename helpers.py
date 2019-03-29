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
    halt(tn)
    reg_set(tn, "pc", pc)
    reg_set_all(tn, 0)
    reg_set(tn, "r" + str(r_addr), addr)
    step(tn)
    return reg_get(tn, "r" + str(r_dest))

def find_pcs(tn):
    halt(tn)
    pc = reg_get(tn, "pc")
    msp = reg_get(tn, "msp")
    return pc, msp