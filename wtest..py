from csv_operator import *

# data = pd.read_csv('test_linear_regression2.csv')

data = csv_to_usable('test_linear_regression.csv')

keys = keygen()
skey = keys[0]
pkey = keys[1]

start_time = time.time()

encrypt_fields(data, ['Age', 'Balance'], pkey)

print(data)

time1 = time.time()

totals = lin_reg(data, 'Age', 'Balance', pkey, skey)

solutions1 = decrypt_ca_list(totals, skey).copy()

# totals2 = lin_reg2(data, 'Age', 'Balance', pkey, skey)

# solutions2 = decrypt_ca_list(totals2, skey)

print(solutions1)

# mult_cols = get_mult_cols(data, 'Age', 'Balance', pkey, skey)
#
# x2 = mult_cols[0]
# xy = mult_cols[1]
#
# sums = get_sums(data, 'Age', 'Balance', x2, xy, pkey, skey)
#
# sum_x = sums[0]
# sum_y = sums[1]
# sum_x2 = sums[2]
# sum_xy = sums[3]
#
# lin_reg_fin(sum_x, sum_y, sum_x2, sum_xy, len(data['Age']), pkey, skey)

# totals = lin_reg_fin(sum_x, sum_y, sum_x2, sum_xy, len(data['Age']), pkey, skey)

# totals = totals1 + totals2

time2 = time.time()

print(totals)

solutions = decrypt_ca_list(totals, skey)

print(solutions)

print(lin_reg_solver(solutions))

# print(data.to_string())

# print(sum_encrypt_col(data, 'Age Encrypted*Age Encrypted', pkey, skey))

print(time2 - time1)

# ca = mult_ca(data['Age Encrypted'][0], data['Balance Encrypted'][0], pkey, skey)
# print(ca)
# print(decode_bin(decrypt_ca(skey, ca)))
