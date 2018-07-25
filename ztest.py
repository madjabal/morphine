from encoder import *
import time


# f = open('Shakespeare.txt', 'r')

# s = f.read()

s = "q" * 100000

start_time = time.time()

# print('String to be encrypted:', s)
# print()

# bits = s2b(s)
# print('Bits:')
# print(bits)
# print(len(bits)/8)
# print()

t0 = time.time()

cyphers = encrypt_s(s)

t12 = time.time()

print("encryption time: " + str((t12 - t0)))

cypher = cyphers[0]
# print('Cypher:')
# print(cypher)
# print(type(cypher))
# print()

pkeys = cyphers[1]
# print('Public Keys:')
# print(pkeys)
# print(type(pkeys))
# print()

skey = cyphers[2]
# print('Private Key')
# print(skey)
# print(type(skey))
# print()

t4 = time.time()

newbits = decrypt_ca(skey, cypher)
# print('Decrypted cipher texts to bit array')
# print(newbits)
# print(type(newbits))
# print()

t5 = time.time()

newstring = decode_bita(newbits)
# print('Bits converted to string')
# print(newstring)
# print(type(newstring))
print()

elapsed_time = time.time()

print('decryption time: ' + str(t5 - t4))
print('decode from bit time: ' + str(elapsed_time - t5))
print('total time: ' + str(elapsed_time - start_time))
print('done')

# f.close()
