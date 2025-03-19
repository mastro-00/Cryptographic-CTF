# 1. General Factorization

from Crypto.Util.number import long_to_bytes
from factordb.factordb import FactorDB # pip install factordb-pycli

n = 180210299477107234107018310851575181787 # n = p*q

f = FactorDB(n)
f.connect()
factors = f.get_factor_list()
print(factors)

p = factors[0]
q = factors[1]

phi = (p-1) * (q-1)

e = 65537

d = pow(e, -1, phi)

c = 27280721977455203409121284566485400046 # c = pow(m, e, n) => m = ?, m = pow(c, d, n)

m = pow(c, d, n)

print(long_to_bytes(m))