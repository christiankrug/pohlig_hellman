#!/usr/bin/env python

from sympy import primefactors, mod_inverse

# DHKE public parameters
# Prime p
p = 11805217175667888115840516101006175607012549121531103
# Generator g
alpha = 5
# Order q
q = 11805217175667888115840516101006175607012549121531102

beta = 4032711556121367277019211297170761294880287059585401

kE = [8273782814589194927701588484643684555498937821545627,
      6291990094196915525598471517067640507118315262674655, 4090958692816020661033660723660354023677053210384520]
m = [6965274808237214170619679618884723891503993817736079,
     520050629966662693626740787735245846840108150512380, 1956599535193462098871516319653323001368701874579404]


# decodes integers to the original message bytes
# from: https://github.com/RyanRiddle/elgamal/blob/master/elgamal.py
def decode(aiPlaintext, iNumBits):
    bytes_array = []
    k = iNumBits // 8
    for num in aiPlaintext:
        for i in range(k):
            temp = num
            for j in range(i + 1, k):
                temp = temp % (2 ** (8 * j))
            letter = temp // (2 ** (8 * i))
            bytes_array.append(letter)
            num = num - (letter * (2 ** (8 * i)))
    decodedText = bytearray(b for b in bytes_array).decode('utf-8')
    return decodedText
    

# Square and Multiply
def sqm(a, b, n):
    res = 1
    binarray = [int(x) for x in bin(int(b))[2:]]
    for i in binarray:
        if i == 1:
            res = (res * res * a) % n
        else:
            res = (res * res) % n
    return res


def find_prime_factors(j):
    factors = []
    n = 2
    # Brute Force Primes
    while n <= j:
        if j % n == 0:
            # Found factor
            factors += [n]
            j //= n
        else:
            n += 1
    return factors


def calculate_subgrp_congruences(pub, pi):
    gi = sqm(alpha, q // pi, p)
    hi = sqm(beta, q // pi, p)
    # we are looking for: gi ^ di = hi mod p (di is the unknown)
    c = 1
    while c < p:
        if sqm(gi, c, p) % p == hi % p:
            return c
        c += 1
    return -1


def solve_crt(dlogs, factors):
    n = 1
    for i in factors:
        n *= i
    x = 0
    for i in range(len(dlogs)):
        yi = n // factors[i]
        zi = mod_inverse(yi, factors[i])
        x += dlogs[i] * yi * zi
    return x % n


def decrypt(key):
    # individual integers of the message m are decrypted (x = y * K_ab^-1 mod p)
    # then, use the decode function to get an ASCII string
    x = []
    for i in range(len(m)):
        x.append((m[i] * mod_inverse(sqm(kE[i], key, p), p)) % p)
    dec = decode(x, 168)
    return dec


def main():
    factors = find_prime_factors(q)
    dlogs = []
    print("The prime factors found are {}.".format(factors))
    for factor in factors:
        dlogs.append(calculate_subgrp_congruences(beta, factor))
    print("The Dlogs found are {}.".format(dlogs))
    key = solve_crt(dlogs, factors)
    print("The Private Key is {}.".format(key))
    cleartext = decrypt(key)
    print("The decrypted text is '{}'".format(cleartext))


if __name__ == "__main__":
    main()
