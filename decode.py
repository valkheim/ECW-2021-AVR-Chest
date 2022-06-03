encoded = "OUQP]by]sToWpBCUqz>8BECxw3"
rot_key = 4
for xor_key in range(0xFF):
    decoded = "".join(
        [
            chr((ord(char) - rot_key) ^ xor_key)
            for i, char in enumerate(encoded)
            if not i % 2
        ]
    )
    if decoded.casefold().startswith("ecw{"):
        print(f"{xor_key:#04x}: {decoded}")
