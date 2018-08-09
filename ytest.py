from encoder import *
from config import *

def add_test(num, nn1, nn2):
    """Tests the accuracy of addition, takes the number of trials and teo numbers and returns the accuracy"""

    count_array = [0] * NUM_BITS

    for i in range(num):
        keys = keygen()
        pubkey = keys[1]
        skey = keys[0]

        n1 = encrypt_n(pubkey, nn1)
        n2 = encrypt_n(pubkey, nn2)
        n3 = add_ca(n1, n2, pubkey, skey)

        cbit_array = list(bin((nn1 + nn2))[2:])

        cbit_array = ['0'] * (NUM_BITS - len(cbit_array)) + cbit_array

        dbit_array = decrypt_ca(skey, n3)

        num_array = []

        # print(cbit_array)
        # print(dbit_array)
        # print()

        for i in range(len(dbit_array)):
            num_array.append(decode_bin(dbit_array))
            if dbit_array[i] == cbit_array[i]:
                count_array[i] += 1

    return [count_array[i]/num*100 for i in range(len(count_array))]


# print(add_test(10, 500, 30))


# keys = keygen()
# pubkey = keys[1]
# skey = keys[0]




def reg_add_test(n1, n2):

    # bita1 = list((bin(n1)[2:]))
    # bita2 = list((bin(n2)[2:]))
    #
    # bita1 = ['0'] * (NUM_BITS - len(bita1)) + bita1
    # bita2 = ['0'] * (NUM_BITS - len(bita2)) + bita2

    bita1 = n1
    bita2 = n2

    c = 0
    b1 = 0
    b2 = 0
    b3 = 0

    bita1.reverse()
    bita2.reverse()

    sol = []

    for i in range(len(bita1)):
        c = (b1 + b2 + b3) % 2
        sol.append(str((c + int(bita1[i]) + int(bita2[i])) % 2))
        b1 = int(bita1[i]) * c
        b2 = int(bita2[i]) * c
        b3 = int(bita1[i]) * int(bita2[i])

    sol.reverse()

    return sol


def count(num):

    count = 0

    for i in range(num):
        for j in range(num):
            num1 = reg_add_test(i, j)
            if decode_bin(num1) == (i + j):
                count += 1

    return count, num**2


# print(count(1000))

def mult_test(num, nn1, nn2):

    count_array = [0] * NUM_BITS

    for i in range(num):
        keys = keygen()
        pubkey = keys[1]
        skey = keys[0]

        n1 = encrypt_n(pubkey, nn1)
        n2 = encrypt_n(pubkey, nn2)
        n3 = mult_ca(n1, n2, pubkey, skey)


        cbit_array = list(bin((nn1 * nn2))[2:])

        dbit_array = decrypt_ca(skey, n3)

        cbit_array = ['0'] * (len(dbit_array) - len(cbit_array)) + cbit_array

        num_array = []

        # print(cbit_array)
        # print(dbit_array)
        # print()

        for i in range(len(dbit_array)):
            num_array.append(decode_bin(dbit_array))
            if dbit_array[i] == cbit_array[i]:
                count_array[i] += 1

        # for i in range(len(dbit_array)):
        #     print(symmetric.noise(skey, int(dbit_array[i])))

    return [count_array[i] / num * 100 for i in range(len(count_array))]


print(mult_test(100, 2579, 2579))


def reg_mult_test(n1, n2):

    bita1 = list((bin(n1)[2:]))
    bita2 = list((bin(n2)[2:]))

    bita1 = ['0'] * (NUM_BITS//2 - len(bita1)) + bita1
    bita2 = ['0'] * (NUM_BITS//2 - len(bita2)) + bita2

    bita1.reverse()
    bita2.reverse()

    post_mult = []

    for i in range(len(bita1)):

        mult1_ca = [] + i * [0]

        for j in range(len(bita2)):

            bit_product = int(bita1[i]) * int(bita2[j])

            mult1_ca.append(bit_product)

        mult1_ca.reverse()
        post_mult.append(mult1_ca)

    for i in range(len(post_mult)):
        if i == len(post_mult) - 1:
            return post_mult[i]

        else:
            post_mult[i + 1] = reg_add_test(post_mult[i], post_mult[i + 1])


# print(reg_mult_test(2, 2))
