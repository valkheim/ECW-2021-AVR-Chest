flag = "P_J]^grMzf:Py]d[?jgLVJyQ:D}z:~yqz?pYx@"
decoded = ''.join([
    chr((ord(char) - 1) ^ ord('\n'))
    for i, char in enumerate(flag) if not i % 2
])
print(decoded)
