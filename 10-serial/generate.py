#!/usr/bin/env python3

import random
import operator
import string
import itertools
import sys

pf = lambda flag: print(f"Flag (in brackets): [{flag}]")

corpus = string.ascii_letters + string.digits
print(f"Corpus: {corpus}")

rc = lambda: random.choice(corpus)

flag = "s3ri4l_r3v3rse"
pf(flag)
flag = "ECW{" + flag + "}"
pf(flag)
flag = "".join([char + rc() for char in flag])
pf(flag)

transform = lambda op, xs, key: "".join(chr(op(ord(x), key)) for x in xs)

xor = lambda string, key: transform(operator.xor, string, key)

xor_key = random.randint(0, 0x7F)
rand_str = "".join([rc() for _ in range(10)])
assert xor("ABCD", 6) == "GDEB"
assert xor("GDEB", 6) == "ABCD"
assert xor(xor(rand_str, xor_key), xor_key) == rand_str

printable = lambda xs: all(x in string.printable for x in xs)

while "non printable":
    xor_key = random.randint(0, 0x7F)
    xor_flag = xor(flag, xor_key)
    if printable(xor_flag) and xor_key != 0:
        flag = xor_flag
        break

print(f"XOR key: {xor_key} or 0x{xor_key:02x}")
pf(flag)

rot = lambda string, key: transform(operator.add, string, key)

rot_key = random.randint(0, len(corpus))
assert rot("ABCD", 1) == "BCDE"
assert rot("ABCD", -1) == "@ABC"  # ascii rot
assert rot(rot("ABCD", rot_key), -rot_key) == "ABCD"

while "non printable":
    rot_key = random.randint(0, len(string.printable)) % 26
    rot_flag = rot(flag, rot_key)
    if printable(rot_flag) and rot_key != 0:
        flag = rot_flag
        break

print(f"ROT key: {rot_key} or 0x{rot_key:02x}")
pf(flag)

config = (
    f'CONFIG=-DFLAG="{flag}"\n'
    f"CONFIG+=-DXOR_KEY=0x{xor_key:02x}\n"
    f"CONFIG+=-DROT_KEY=0x{rot_key:02x}"
)
with open("config.mk", "wt") as fh:
    fh.write(config)
