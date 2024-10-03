import random
from tqdm import tqdm


def xor(sa, sb):  
    return bytes(a^b for a, b in zip(sa, sb))


if __name__ == '__main__':
    original = 'perfil.png'
    enc = 'perfil.png.enc'

    with open(enc, 'rb') as f:
        b = f.read()
        n = len(b)

    print(n)
    with open('random_bytes', 'rb') as f:
        h = f.read()
        print(len(h))
        h = h[:16]

    for i in tqdm(range(1000000, 9999999999)):
        random.seed(i)
        r1 = random.randbytes(n)
        r2 = random.randbytes(n)
        if r1[:16] == h or r2[:16] == h:
            print("SEED: ", i)
            break
