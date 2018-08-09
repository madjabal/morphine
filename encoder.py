from asymmetric import *
import symmetric
import numpy as np

import time


def s2b(s):
    """Takes a string, turns it to its ordinal, and converts that to 8 bits"""
    t1 = time.time()
    ord_bit_array = []
    for c in s:
        ord_bit_array.append(format(ord(c), 'b'))
    t2 = time.time()
    for i in range(len(ord_bit_array)):
        ord_bit_array[i] = (8 - len(ord_bit_array[i])) * '0' + str(ord_bit_array[i])
    t3 = time.time()
    ord_bit_array = ''.join(ord_bit_array)
    t4 = time.time()
    print('string to bad bit array: ' + str(t2 - t1))
    print('bad bit array to good bit array: ' + str(t3 - t2))
    print('good bit array to bitstring: ' + str(t4 - t3))
    return ord_bit_array


def encrypt_s(s):
    """Takes a string and returns a tuple that is the cypher texts in an array, list of public keys, and secret key"""

    keys = keygen()
    pkeys = keys[1]
    skey = keys[0]
    bits = s2b(s)
    cypher_array = []

    for bit in bits:
        cypher_array.append(encrypt(pkeys, int(bit),))

    return cypher_array, pkeys, skey


def ca2s(cypher_array):
    """Takes a cipher array and converts it to a string of cipher texts instead of integers"""

    for i in range(len(cypher_array)):
        cypher_array[i] = str(cypher_array[i])

    return "".join(cypher_array)


def s2ca(s):
    """Takes a string of cipher texts and returns it as an array of cipher texts"""

    cypher_array = []
    for i in range(int((len(s))/314)):
        cypher_array.append(s[i:i+314])

    return cypher_array


def decrypt_ca(sk, cypher_array):
    """Takes a private key and an array of cipher texts and decrypts it to a an array of single bit strings"""

    bit_array = []
    for cypher in cypher_array:
        bit_array.append(str(symmetric.decrypt(int(sk), int(cypher))))

    return bit_array


def decode_bita(bit_array):
    """Takes a bit array and returns the corresponding string"""

    bits = ''.join(bit_array)
    string_array = []

    for i in range(int(len(bits)/8)):
        string_array.append(chr(int(bits[i*8:(i*8)+8], 2)))

    return ''.join(string_array)


def encrypt_n(pkey, n):
    """Encrypts a given number up to 20 bits"""

    cypher_array = []
    bits = bin(n)[2:]
    encrypt_zero = encrypt(pkey, 0,)

    for bit in bits:
        cypher_array.append(encrypt(pkey, int(bit), ))
    if n > 2**(NUM_BITS//2):
        cypher_array = [encrypt_zero] * (NUM_BITS - len(cypher_array)) + cypher_array
    else:
        cypher_array = [encrypt_zero] * (NUM_BITS - len(cypher_array)) + cypher_array

    return cypher_array


def decode_bin(bin_array):
    """Takes in an array of bits and returns the number associated"""
    bitstring = ''.join(bin_array)
    number = int(bitstring, 2)
    return number


def add_ca(ca1, ca2, pkey, skey):
    """Adds 2 numbers in cypher text"""

    count = 0

    c = 0
    b1 = 0
    b2 = 0
    b3 = 0

    ca1.reverse()
    ca2.reverse()

    sol = []

    for i in range(len(ca1)):

        sol.append(c + ca1[i] + ca2[i])

        b1 = ca1[i] * c
        b2 = ca2[i] * c
        b3 = ca1[i] * ca2[i]

        c = b1 + b2 + b3

        if count % 2 == 0:

            c = decrypt(skey, c)
            c = encrypt(pkey, c,)

        count += 1

    for i in range(len(sol)):
        sol[i] = decrypt(skey, sol[i])
        sol[i] = encrypt(pkey, sol[i],)

    sol.reverse()

    return sol


def mult_ca(ca1, ca2, pkey, skey):
    """Multiplies two numbers in cypher array"""

    ca1.reverse()
    ca2.reverse()

    # print(decode_bin(decrypt_ca(skey, ca1)))
    # print(decode_bin(decrypt_ca(skey, ca2)))

    post_mult = []

    zero_encrypt = encrypt(pkey, 0,)

    for i in range(len(ca1)):

        mult1_ca = [] + i * [zero_encrypt]

        for j in range(len(ca2)):

            bit_product = ca1[i] * ca2[j]

            bit_product = decrypt(skey, bit_product)
            bit_product = encrypt(pkey, bit_product,)

            mult1_ca.append(bit_product)

        mult1_ca.reverse()
        post_mult.append(mult1_ca)

    sum_mult = []

    for i in range(len(post_mult)):

        if i == len(post_mult) - 1:
            sum_mult = post_mult[len(post_mult) - 1]
            break

        else:
            post_mult[i+1] = add_ca(post_mult[i], post_mult[i + 1], pkey, skey)

    refresh_ca(sum_mult, pkey, skey)

    # print(decode_bin(decrypt_ca(skey, sum_mult)))

    return sum_mult


def refresh_ca(ca, pkey, skey):
    for i in range(len(ca)):
        ca[i] = decrypt(skey, ca[i])
        ca[i] = encrypt(pkey, ca[i])