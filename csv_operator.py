from encoder import *
import pandas as pd
import csv


def csv_to_usable(csv1):
    csv_list = []
    with open(csv1) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            csv_list.append(row)

    col_dict = {}

    for i in range(len(csv_list[0])):
        col_dict[csv_list[0][i]] = []
        for j in range(1, len(csv_list)):
            col_dict[csv_list[0][i]].append(int(csv_list[j][i]))

    return col_dict


def csv_to_df(csv_name):
    """Takes in the name of a csv and returns it as a dataframe"""
    return pd.read_csv(str(csv_name) + '.csv')


def encrypt_fields(dataframe, fields_list, pkey):
    """Encrypts the list of fields given within a dataframe"""

    for i in fields_list:
        encrypt_col(dataframe, i, pkey)


def encrypt_col_old(dataframe, col, pkey):
    """Encrypts a given column in a given data frame"""

    new_col = []

    for i in dataframe[col]:
        new_col.append(encrypt_n(pkey, i))
    dataframe[col + ' Encrypted'] = pd.Series(new_col)


def encrypt_col(dataframe, col, pkey):
    """Encrypts a given column in a given data frame"""

    new_col = []

    for i in dataframe[col]:
        new_col.append(encrypt_n(pkey, i))
    dataframe[col + ' Encrypted'] = new_col


def mult_encrypt_col(dataframe, col1, col2, pkey, skey):
    """Multiplies two encrypted columns and outputs them in a new column on the right"""

    new_col = []

    for i in range(len(dataframe[col2])):
        decode_bin(decrypt_ca(skey, dataframe[col2][i])), decode_bin(decrypt_ca(skey, dataframe[col1][i]))
        ca = mult_ca(dataframe[col2][i], dataframe[col1][i], pkey, skey)
        # ca = mult_ca(dataframe['Age Encrypted'][i], dataframe['Balance Encrypted'][i], pkey, skey)
        new_col.append(ca)

    # dataframe[str(col1) + '*' + str(col2)] = pd.Series(new_col)

    return new_col


def mult_encrypt_col2(dataframe, col1, col2, pkey, skey):
    """Multiplies two encrypted columns and outputs them in a new column on the right"""

    new_col = []

    for i in range(len(dataframe[col1])):
        ca = mult_ca(dataframe['Age Encrypted'][i], dataframe['Balance Encrypted'][i], pkey, skey)
        new_col.append(ca)

    # dataframe[str(col1) + '*' + str(col2)] = pd.Series(new_col)

    return new_col


def sum_encrypt_col(dataframe, col, pkey, skey):
    """Sums the entire encrypted column and returns it"""

    col_sum = dataframe[col][0]

    for i in range(1, len(dataframe[col])):
        col_sum = add_ca(col_sum, dataframe[col][i], pkey, skey)

    return col_sum


def sum_encrypt_col2(col, pkey, skey):
    """Sums the entire encrypted column without a data frame and returns it"""

    col_sum = col[0]

    for i in range(1, len(col)):
        col_sum = add_ca(col_sum, col[i], pkey, skey)

    return col_sum


def lin_reg(dataframe, col1, col2, pkey, skey):
    """Runs a linear regression on the two columns"""

    number_list = []

    col1 = str(col1 + ' Encrypted')
    col2 = str(col2 + ' Encrypted')

    m = len(dataframe[col1])

    n = encrypt_n(pkey, m)

    decode_bin(decrypt_ca(skey, n))

    sum_x = sum_encrypt_col(dataframe, col1, pkey, skey)

    refresh_ca(sum_x, pkey, skey)

    decode_bin(decrypt_ca(skey, mult_ca(sum_x, sum_x, pkey, skey)))

    # sum_x_2 = mult_ca(sum_x, sum_x, pkey, skey)

    sum_x = decode_bin(decrypt_ca(skey, sum_x))

    decode_bin(decrypt_ca(skey, mult_ca(encrypt_n(pkey, sum_x), encrypt_n(pkey, sum_x), pkey, skey)))

    sum_x_2 = mult_ca(encrypt_n(pkey, sum_x), encrypt_n(pkey, sum_x), pkey, skey)

    sum_x = encrypt_n(pkey, sum_x)

    sum_y = sum_encrypt_col(dataframe, col2, pkey, skey)

    sum_x2 = sum_encrypt_col2(mult_encrypt_col(dataframe, col1, col1, pkey, skey), pkey, skey)

    decode_bin((decrypt_ca(skey, mult_encrypt_col2(dataframe, col1, col2, pkey, skey)[1])))

    sum_xy = sum_encrypt_col2(mult_encrypt_col2(dataframe, col1, col2, pkey, skey), pkey, skey)

    refresh_ca(sum_y, pkey, skey)
    refresh_ca(sum_x2, pkey, skey)
    refresh_ca(sum_xy, pkey, skey)
    refresh_ca(sum_x_2, pkey, skey)

    decode_bin(decrypt_ca(skey, sum_x))
    decode_bin(decrypt_ca(skey, sum_y))
    decode_bin(decrypt_ca(skey, sum_x2))
    print(decode_bin(decrypt_ca(skey, sum_xy)))
    # new_sum_xy = sum_xy
    decode_bin(decrypt_ca(skey, sum_x_2))

    const_tl = mult_ca(sum_y, sum_x2, pkey, skey)
    number_list.append(const_tl.copy())
    const_tr = mult_ca(sum_x, sum_xy, pkey, skey)
    number_list.append(const_tr.copy())
    const_bl = mult_ca(n, sum_x2, pkey, skey)
    # slope_bl = mult_ca(n, sum_x2, pkey, skey)
    # number_list.append(slope_bl.copy())
    const_br = sum_x_2
    number_list.append(const_br.copy())

    # print(decode_bin(decrypt_ca(skey, mult_ca(n, sum_xy, pkey, skey))))
    decode_bin(decrypt_ca(skey, mult_ca(sum_x, sum_y, pkey, skey)))

    # help1 = decode_bin((decrypt_ca(skey, sum_xy)))

    # helpe = encrypt_n(help1, pkey)

    # news = mult_ca(helpe, helpe, pkey, skey)

    slope_tl = mult_ca(n, sum_xy, pkey, skey)
    # number_list.append(slope_tl.copy())
    # slope_tr = mult_ca(sum_x, sum_y, pkey, skey)
    # number_list.append(slope_tr.copy())
    slope_bl = mult_ca(n, sum_x2, pkey, skey)
    number_list.append(slope_bl.copy())
    number_list.append(sum_x_2.copy())
    const_bl = slope_bl

    # slope_tl = mult_ca(n, sum_xy, pkey, skey)

    slope_br = sum_x_2

    slope_tl = m * decode_bin(decrypt_ca(skey, sum_xy))
    print(slope_tl, m, decode_bin(decrypt_ca(skey, sum_xy)))

    slope_tr = decode_bin(decrypt_ca(skey, sum_x)) * decode_bin(decrypt_ca(skey, sum_y))

    return [const_tl, const_tr, const_bl, const_br, slope_tl, slope_tr, slope_bl,slope_br]
    # return number_list

# def lin_reg2(dataframe, col1, col2, pkey, skey):
#     """Runs a linear regression on the two columns"""
#
#     number_list = []
#
#     col1 = str(col1 + ' Encrypted')
#     col2 = str(col2 + ' Encrypted')
#
#     m = len(dataframe[col1])
#
#     n = encrypt_n(pkey, m)
#
#     sum_x = sum_encrypt_col(dataframe, col1, pkey, skey)
#
#     refresh_ca(sum_x, pkey, skey)
#
#     decode_bin(decrypt_ca(skey, mult_ca(sum_x, sum_x, pkey, skey)))
#
#     sum_x_2 = mult_ca(sum_x, sum_x, pkey, skey)
#
#     sum_x = decode_bin(decrypt_ca(skey, sum_x))
#
#     decode_bin(decrypt_ca(skey, mult_ca(encrypt_n(pkey, sum_x), encrypt_n(pkey, sum_x), pkey, skey)))
#
#     sum_x_2 = mult_ca(encrypt_n(pkey, sum_x), encrypt_n(pkey, sum_x), pkey, skey)
#
#     sum_x = encrypt_n(pkey, sum_x)
#
#     sum_y = sum_encrypt_col(dataframe, col2, pkey, skey)
#
#     sum_x2 = sum_encrypt_col2(mult_encrypt_col(dataframe, col1, col1, pkey, skey), pkey, skey)
#
#     decode_bin((decrypt_ca(skey, mult_encrypt_col2(dataframe, col1, col2, pkey, skey)[1])))
#
#     sum_xy = sum_encrypt_col2(mult_encrypt_col2(dataframe, col1, col2, pkey, skey), pkey, skey)
#
#     refresh_ca(sum_y, pkey, skey)
#     refresh_ca(sum_x2, pkey, skey)
#     refresh_ca(sum_xy, pkey, skey)
#     refresh_ca(sum_x_2, pkey, skey)
#
#     decode_bin(decrypt_ca(skey, sum_x))
#     decode_bin(decrypt_ca(skey, sum_y))
#     decode_bin(decrypt_ca(skey, sum_x2))
#     decode_bin(decrypt_ca(skey, sum_xy))
#     new_sum_xy = sum_xy
#     decode_bin(decrypt_ca(skey, sum_x_2))
#
#     const_tl = mult_ca(sum_y, sum_x2, pkey, skey)
#     # number_list.append(const_tl.copy())
#     const_tr = mult_ca(sum_x, sum_xy, pkey, skey)
#     # number_list.append(const_tr.copy())
#     const_bl = mult_ca(n, sum_x2, pkey, skey)
#     slope_bl = mult_ca(n, sum_x2, pkey, skey)
#     # number_list.append(slope_bl.copy())
#     const_br = sum_x_2
#     # number_list.append(const_br.copy())
#
#     # decode_bin(decrypt_ca(skey, mult_ca(n, sum_xy, pkey, skey)))
#     # decode_bin(decrypt_ca(skey, mult_ca(sum_x, sum_y, pkey, skey)))
#
#     slope_tl = mult_ca(n, sum_xy, pkey, skey)
#     number_list.append(slope_tl.copy())
#     slope_tr = mult_ca(sum_x, sum_y, pkey, skey)
#     number_list.append(slope_tr.copy())
#     slope_bl = mult_ca(n, sum_x2, pkey, skey)
#     number_list.append(slope_bl.copy())
#     number_list.append(sum_x_2.copy())
#     const_bl = slope_bl
#
#     slope_br = sum_x_2
#
#     # return [slope_tl, slope_tr, slope_bl, slope_br]
#     return number_list


def get_mult_cols(dataframe, col1, col2, pkey, skey):

    col1 = str(col1 + ' Encrypted')
    col2 = str(col2 + ' Encrypted')

    x2 = mult_encrypt_col(dataframe, col1, col1, pkey, skey)

    xy = mult_encrypt_col(dataframe, col1, col2, pkey, skey)

    return [x2, xy]


def get_sums(dataframe, x, y, x2, xy, pkey, skey):

    x = str(x + ' Encrypted')
    y = str(y + ' Encrypted')

    sum_x = sum_encrypt_col(dataframe, x, pkey, skey)
    sum_y = sum_encrypt_col(dataframe, y, pkey, skey)
    sum_x2 = sum_encrypt_col2(x2, pkey, skey)
    sum_xy = sum_encrypt_col2(xy, pkey, skey)

    print(decode_bin(decrypt_ca(skey, sum_x)))

    return [sum_x, sum_y, sum_x2, sum_xy]


def lin_reg_fin(sum_x, sum_y, sum_x2, sum_xy, n, pkey, skey):

    n = encrypt_n(pkey, n)

    sum_x_2 = mult_ca(sum_x, sum_x, pkey, skey)

    const_tl = mult_ca(sum_y, sum_x2, pkey, skey)
    const_tr = mult_ca(sum_x, sum_xy, pkey, skey)
    const_bl = mult_ca(n, sum_x2, pkey, skey)
    const_br = sum_x_2

    slope_tl = mult_ca(n, sum_xy, pkey, skey)
    slope_tr = mult_ca(sum_x, sum_y, pkey, skey)
    slope_bl = mult_ca(n, sum_x2, pkey, skey)

    const_bl = slope_bl

    slope_br = sum_x_2

    print(decode_bin(decrypt_ca(skey, sum_y)))
    print(decode_bin(decrypt_ca(skey, sum_x2)))
    print(decode_bin(decrypt_ca(skey, sum_xy)))
    print(decode_bin(decrypt_ca(skey, sum_x_2)))

    return [const_tl, const_tr, const_bl, const_br, slope_tl, slope_tr, slope_bl, slope_br]


def decrypt_ca_list(ca_list, skey):
    sol_list = []
    for i in ca_list:
        if type(i) == list:
            sol_list.append(decode_bin(decrypt_ca(skey, i)))
        else:
            sol_list.append(i)

    return sol_list


def lin_reg_solver(solve_list):
    intercept = (solve_list[0] - solve_list[1]) / (solve_list[2] - solve_list[3])
    slope = (solve_list[4] - solve_list[5]) / (solve_list[6] - solve_list[7])
    return {'slope': slope, 'intercept': intercept}
