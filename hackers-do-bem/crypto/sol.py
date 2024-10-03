from math import gcd
from Crypto.Util.number import inverse
import binascii
(N, e) = (0x8cc3b128b728555455ff6337e5385ec3ff95eb35a355de75ddae96f6195a62efbab7e625605060919892ecd557f4f03fc3f34f28b8a2ac568b0b7f7ef3d6aa8eb8d98df06bbf5e2f4bdb7c78476445b0b73bd44ba6026a5490fe643794110fa7c11b2e5c83f89a24c6f08fc9ce5a50f96d050bd2d8a962eb711d4f47f57ecd1f, 0x10001)

#Onde (N, e) é a chave, mf é a flag encriptada e mp o primo encriptado.
mf = 0x6f3bc275659169a9cc4feac3eb084fbcfbef7de5b2af11256a942e28f6b4f64b8596eb3694b558962a7db274ebb7c0dfeec3e50a6102ac8c736d60659546e3079d4c2df67529bd0628012e4a06047a3efc6fa0645c36112e54bce956b6593b823a1fd4ed4a619b9dfd2824bb66f85a6e64e113e38c72ab165db62b8d00791b86

mp = 0x7d21937be700e1fff8fe806e51ed3b8faf9c84a6bc24dc0da03dc6a81e09f2d7933b89a86696f0c2214ac3a6d88df85ba177fa5710ee869be0866c522765777fb76a2167a147dba3a66de9f37dde6c1c63f72b53adf98bcbfa900e559e19442b2b51920e815ac6cda94ff0787257c23c8fd35e96e757be53a4be56e150989796


p = gcd(mp,N)
q = N//p
print(p)
print(q)

phi = (p-1)*(q-1)
d = inverse(e, phi)

m = pow(mf, d, N)
print(binascii.unhexlify(hex(m)[2:]))
