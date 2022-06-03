# Chest

## Public resources

* the `chest.hex` code
* a tcp access to the docker container running the code

## What's inside

The challenge consists of finding a key to open a chest and reveal a flag.

The code uses the following to decode the flag:

- rotate buffer
- xor buffer
- traverse with a step of 2

You can use `generate.py` to generate a flag and a Makefile config:

```
$ python3 generate.py
orpus:   0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&*+-./:<=>?[]^_|~
clear:    ECW{7ecdf276}
mixed:    E|CzWo{x7=e~cld=fE2^7P6*}S
xor 0x0e: KrMtYauv93kpmbj3hK<P9^8$s]
rot 0x01: LsNuZbvw:4lqnck4iL=Q:_9%t^
config.mk written
flag written
```

Config:

```
$ cat config.mk                                                                                                                                                                                                                      130 ⨯
CONFIG=-DFLAG="LsNuZbvw:4lqnck4iL=Q:_9%t^"
CONFIG+=-DXOR_KEY=0xe
CONFIG+=-DROT_KEY=0x1
```

flag:

```
$ cat flag   
LsNuZbvw:4lqnck4iL=Q:_9%t^
```

The Makefile config can now be used to generate the challenge:

```
$ make release
rm -f chest.elf
rm -f chest.hex
avr-gcc -Wall -Werror -mmcu=atmega328p -DFLAG="LsNuZbvw:4lqnck4iL=Q:_9%t^" -DXOR_KEY=0xe -DROT_KEY=0x1 -Os -o chest.elf chest.c
avr-objcopy -O ihex chest.elf chest.hex
#avr-objcopy -j .text -O ihex chest.elf chest.hex
avr-strip chest.elf
                                                                                                                                                                                                                                             
$ file chest.elf
chest.elf: ELF 32-bit LSB executable, Atmel AVR 8-bit, version 1 (SYSV), statically linked, stripped
                                                                                                                                                                                                                                             
$ cat chest.hex
:100000000C9434000C9449000C9449000C94490061
:100010000C9449000C9449000C9449000C9449003C
:100020000C9449000C9449000C9449000C9449002C
:100030000C9449000C9449000C9449000C9449001C
:100040000C9449000C9449000C9449000C9449000C
:100050000C9449000C9449000C9449000C944900FC
:100060000C9449000C94490011241FBECFEFD8E036
:10007000DEBFCDBF11E0A0E0B1E0E8EAF1E002C0F0
:1000800005900D92A632B107D9F70E94CA000C94D0
:10009000D2000C9400001092C5008093C40088E147
:1000A0008093C10086E08093C20008959091C000C3
:1000B00095FFFCCF8093C60008950F931F93CF93B5
:1000C000DF93EC018C01060F111DC017D10721F041
:1000D00089910E945600F9CFDF91CF911F910F9126
:1000E00008958091C00087FFFCCF8091C6000895DD
:1000F0000F931F93CF93DF93EC018C01060F111D1B
:10010000C017D10721F00E9471008993F9CFDF91C8
:10011000CF911F910F910895CF93DF93CDB7DEB7A5
:100120002B970FB6F894DEBF0FBECDBF8BE0EBE18F
:10013000F1E0DE01119601900D928A95E1F76BE0F6
:10014000CE0101960E945D000E9471002B960FB6B1
:10015000F894DEBF0FBECDBFDF91CF910895FF921F
:100160000F931F93CF93DF93F82EC0E0D1E00CE103
:1001700011E0888181508F250E94560022960C172D
:100180001D07B9F78AE0DF91CF911F910F91FF9082
:100190000C94560087E60E944B000E948C000E943F
:0801A000AF00FBCFF894FFCF84
:1001A8004C734E755A6276773A346C716E636B3461
:1001B800694C3D513A5F3925745E00456E7465722D
:0601C800206B65790A00BE
:00000001FF
```

You can test it with `make test`. Tmux will open with the following screens:

* running qemu
* gdb breaking at 0x00
* a telnet session on qemu for serial I/O

By reading the code, you should to understand that you need to provide the XOR
key needed to decode the embeeded flag.

```
$ printf "\xe" | nc localhost 5678                                                                                                                                                                                                     1 ⨯
ECW{7ecdf276}
```

## Docker

You can use `Dockerfile` to build an image capable of :

* generating a flag
* compiling the challenge
* running the code on qemu
* exposing the serial interface on a random tcp port

Consider bindmounting a volume to access the following files from the host:

* `/chest/chest.hex`: the code in HEX (Intel) format to be reversed
* `/chest/flag`: the flag

Examples:

* Build image: `docker build --tag chest .`
* Run container:  `docker run --detach --publish-all --name chest --rm chest`
* Stopping container: `docker container stop chest`
