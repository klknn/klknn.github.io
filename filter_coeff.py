# requires version '1.7.1
from sympy import *

s = Symbol('s')
z = Symbol('z')
Q = Symbol('Q')    # resonance
T = Symbol('T')    # sampling interval
w0 = Symbol('w0')  # cutoff freq

# z2s = 2 / T * (z - 1) / (z + 1)
s2z = 2 / T * (z - 1) / (z + 1)

def print_coeff(hs):
    hz = simplify(hs.subs(s, s2z))  # Z transform
    npole = degree(denom(hs), s)
    print("=== Transfer function ===")
    print("H(s) =", hs)  # transfer function in Laplace domain
    print("H(z) =", hz)  # transfer function in Z domain
    print("#pole =", npole)
    print("=== Filter coeffients ===")
    # FIR coeff
    dhz = collect(expand(denom(hz) * z ** -npole), z)
    nhz = collect(expand(numer(hz) * z ** -npole), z)
    a0 = dhz.coeff(z, 0)  # to normalize a0 = 1
    for i in range(npole + 1):
        print(f"b{i} =", nhz.coeff(z, -i) / a0)
    # IIR coeff
    for i in range(1, npole + 1):
        print(f"a{i} =", dhz.coeff(z, -i) / a0)


print("Filter: 1-pole LPF")
print_coeff(hs = 1 / (s / w0 + 1))
print()
print("Filter: 1-pole HPF")
print_coeff(hs = s / (s + w0))
print()
print("Filter: 2-pole LPF")
print_coeff(hs = w0**2 / (s**2 + s * w0 * Q + w0**2))
print()
print("Filter: 2-pole HPF")
print_coeff(hs = (s**2 / w0**2) / (s**2 + s * w0 * Q + w0**2))
print()
print("Filter: 2-pole BPF")
print_coeff(hs = (s / w0 / Q) / (s**2 + s * w0 * Q + w0**2))
