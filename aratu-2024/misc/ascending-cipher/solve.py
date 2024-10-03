flag = b"CQLXF\x81|9~>j=\x80mC\x87D\x85C\x81H7\x94"
c = 0x282390452cde64f2f6f59e7c04d7a0e2

j = 0
a = ''
for i in range(len(flag)):
    a += chr(c[i] + i + 1)

print(a)
