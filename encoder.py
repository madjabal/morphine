from asymmetric import *
import symmetric

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
    """Takes a private key and an array of cipher texrs and decrypts it to a an array of single bit strings"""

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
