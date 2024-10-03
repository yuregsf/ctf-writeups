from pwn import *
from base64 import b64decode

r = remote('chal.pctf.competitivecyber.club', 9001)

for it in range(0,1000):
    print(it)
    r.recvuntil(b'Challenge: ')
    b = r.recvline().decode()

    s = b64decode(b).decode().split('|')
    b = s[0]
    n = int(s[1])

    for i in range(0,n):
        b = b64decode(b).decode()
    r.recvuntil(b'>> ')
    r.sendline(f'{b}|{it}')

r.interactive()
