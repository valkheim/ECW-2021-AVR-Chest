#!/usr/bin/env python3

import random
import operator
import secrets

pf = lambda flag: print(f"Flag (in brackets): [{flag}]")
corpus = (
    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&*+-./:<=>?[]^_|~"
)
rc = lambda: random.choice(corpus)

transform = lambda op, xs, key: "".join(chr(op(ord(x), key)) for x in xs)
xor = lambda string, key: transform(operator.xor, string, key)
printable = lambda xs: all(x in corpus for x in xs)
rot = lambda string, key: transform(operator.add, string, key)

# Test xor
xor_key = random.randint(0, 0x7F)
rand_str = "".join([rc() for _ in range(10)])
assert xor("ABCD", 6) == "GDEB"
assert xor("GDEB", 6) == "ABCD"
assert xor(xor(rand_str, xor_key), xor_key) == rand_str

# Test rot
rot_key = random.randint(0, len(corpus))
assert rot("ABCD", 1) == "BCDE"
assert rot("ABCD", -1) == "@ABC"  # ascii rot
assert rot(rot("ABCD", rot_key), -rot_key) == "ABCD"


def get_flag():
    flag = secrets.token_hex(4)
    clear = "ECW{" + flag + "}"
    flag = "".join([char + rc() for char in clear])
    return clear, flag


def try_generate(generator, max_amount):
    if max_amount <= 0:
        return False, None, None

    key, flag = generator()
    if printable(flag) and key != 0:
        return True, key, flag

    return try_generate(generator, max_amount - 1)


def xorify(mixed_flag):
    def _gen_xor():
        nonlocal mixed_flag
        key = random.randint(0, 0x7F)
        flag = xor(mixed_flag, key)
        return key, flag

    return try_generate(_gen_xor, 0x7F)


def rotify(xored_flag):
    def _gen_rot():
        nonlocal xored_flag
        key = random.randint(0, len(corpus))
        flag = rot(xored_flag, key)
        return key, flag

    return try_generate(_gen_rot, len(corpus))


def demix(mixed_flag):
    return "".join([char for char in mixed_flag[0::2]])


while "generate valid combination":
    clear_flag, mixed_flag = get_flag()
    assert clear_flag == demix(mixed_flag)
    ok, xor_key, xor_flag = xorify(mixed_flag)
    if not ok:
        continue

    assert xor(xor_flag, xor_key) == mixed_flag
    ok, rot_key, rot_flag = rotify(xor_flag)
    if not ok:
        continue

    assert rot(rot_flag, -rot_key) == xor_flag
    break

print(f"Corpus:   {corpus}")
print(f"clear:    {clear_flag}")
print(f"mixed:    {mixed_flag}")
print(f"xor 0x{xor_key:02x}: {xor_flag}")
print(f"rot 0x{rot_key:02x}: {rot_flag}")

config = (
    f'CONFIG=-DFLAG="{rot_flag}"\n'
    f"CONFIG+=-DXOR_KEY={xor_key:#02x}\n"
    f"CONFIG+=-DROT_KEY={rot_key:#02x}"
)

with open("config.mk", "wt") as fh:
    fh.write(config)

print("config.mk written")
with open("flag", "wt") as fh:
    fh.write(rot_flag)

print("flag written")
