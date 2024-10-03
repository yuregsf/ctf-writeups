import hashlib
import random

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A, B = 0, 7 
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
def padd(P1, P2):
    if P1 is None: return P2
    if P2 is None: return P1
    if P1 == P2:
        slope = (3 * P1[0] * P1[0] * pow(2 * P1[1], P - 2, P)) % P
    else:
        slope = ((P2[1] - P1[1]) * pow(P2[0] - P1[0], P - 2, P)) % P
    x3 = (slope * slope - P1[0] - P2[0]) % P
    y3 = (slope * (P1[0] - x3) - P1[1]) % P
    return (x3, y3)
def pmultp(k, P):
    result,addend = None, P
    while k:
        if k & 1:
            result = padd(result, addend)
        addend = padd(addend, addend)
        k >>= 1
    return result
def kpgen():
    priv = random.randrange(1, N)
    pub = pmultp(priv, (Gx, Gy))
    return priv, pub
def sha256(msg):
    return int(hashlib.sha256(msg.encode()).hexdigest(), 16)
def sign(priv, msg, k=None):
    if k is None:
        k = random.randrange(1, N)
    hash_msg = sha256(msg)
    r, _ = pmultp(k, (Gx, Gy))
    r %= N
    s = (pow(k, -1, N) * (hash_msg + r * priv)) % N
    return (r, s), k
def verify(pub, msg, signature):
    r, s = signature
    hash_msg = sha256(msg)
    w = pow(s, -1, N)
    u1 = (hash_msg * w) % N
    u2 = (r * w) % N
    X, Y = padd(pmultp(u1, (Gx, Gy)), pmultp(u2, pub))
    return r == X % N
priv, pub = kpgen()
k = random.randrange(1, N)
fsign, kx = sign(priv, "6BIYFjS95yhaGs9PREUlS6V2jD160NgwEMCcfUnejg", k)
ssign, ky = sign(priv, "8BKOGc3GVhaGs9PREUlhEwDEMCcfUnejgw1Vge60QB", k)
[r1, s1], [r2, s2] = fsign, ssign 
print(f"r1:{r1}")
print(f"s1:{s1}")
print(f"r2:{r2}")
print(f"s2:{s2}")
print(f"pub:{pub[0]:x}{pub[1]:x}")
secret = ""
csecret = ''.join(f'{b:02x}' for b in ([ord(c) ^ (priv & 0xFF) for c in secret[::-1]]))  
print(f"csecret:{csecret}")
