from asymmetric import *
from encoder import *

keys = keygen()
pubkey = keys[1]
skey = keys[0]

num1 = 5
num2 = 6

# bin1 = bin(num1)[2:]
# bin2 = bin(num1)[2:]
#
# ct1 = encrypt(pubkey, 1,)
# ct2 = encrypt(pubkey, 1,)
#
# print(ct1)
# print(ct2)
# print(ct1 + ct1)
# print(decrypt(skey, 0))

n1 = encrypt_n(pubkey, 2)
n2 = encrypt_n(pubkey, 2)

# print(n1)
# print(n2)

# print(n1+n2)

# add_ca(n1, n2)

n3 = mult_ca(n1, n2, pubkey, skey)

print(decrypt_ca(skey, n1), decode_bin(decrypt_ca(skey, n1)))

for i in n1:
    print(symmetric.noise(skey, i))

for i in n2:
    print(symmetric.noise(skey, i))

print(decrypt_ca(skey, n2), decode_bin(decrypt_ca(skey, n2)))
print()

n3 = add_ca(n1, n2, pubkey, skey)

for i in n3:
    print(symmetric.noise(skey, i))

print(decrypt_ca(skey, n3), decode_bin(decrypt_ca(skey, n3)))
