```
$ avr-objcopy -I ihex serial.hex -O binary serial.bin
$ file serial.bin
serial.bin: data
$ xxd serial.bin
00000000: 0c94 3400 0c94 4900 0c94 4900 0c94 4900  ..4...I...I...I.
00000010: 0c94 4900 0c94 4900 0c94 4900 0c94 4900  ..I...I...I...I.
00000020: 0c94 4900 0c94 4900 0c94 4900 0c94 4900  ..I...I...I...I.
00000030: 0c94 4900 0c94 4900 0c94 4900 0c94 4900  ..I...I...I...I.
00000040: 0c94 4900 0c94 4900 0c94 4900 0c94 4900  ..I...I...I...I.
00000050: 0c94 4900 0c94 4900 0c94 4900 0c94 4900  ..I...I...I...I.
00000060: 0c94 4900 0c94 4900 1124 1fbe cfef d8e0  ..I...I..$......
00000070: debf cdbf 11e0 a0e0 b1e0 ecef f1e0 02c0  ................
00000080: 0590 0d92 a634 b107 d9f7 0e94 f000 0c94  .....4..........
00000090: fc00 0c94 0000 1092 c500 8093 c400 88e1  ................
000000a0: 8093 c100 86e0 8093 c200 0895 9091 c000  ................
000000b0: 95ff fccf 8093 c600 0895 0f93 1f93 cf93  ................
000000c0: df93 ec01 8c01 060f 111d c017 d107 21f0  ..............!.
000000d0: 8991 0e94 5600 f9cf df91 cf91 1f91 0f91  ....V...........
000000e0: 0895 8091 c000 87ff fccf 8091 c600 0895  ................
000000f0: 0f93 1f93 cf93 df93 ec01 8c01 060f 111d  ................
00000100: c017 d107 21f0 0e94 7100 8993 f9cf df91  ....!...q.......
00000110: cf91 1f91 0f91 0895 cf93 df93 cdb7 deb7  ................
00000120: 6e97 0fb6 f894 debf 0fbe cdbf 8ee1 e0e0  n...............
00000130: f1e0 de01 1196 0190 0d92 8a95 e1f7 6ee1  ..............n.
00000140: ce01 0196 0e94 5d00 0e94 7100 91e0 8935  ......]...q....5
00000150: 09f0 90e0 892f 6e96 0fb6 f894 debf 0fbe  ...../n.........
00000160: cdbf df91 cf91 0895 df92 ef92 ff92 0f93  ................
00000170: 1f93 cf93 df93 cdb7 deb7 a797 0fb6 f894  ................
00000180: debf 0fbe cdbf 87e2 eee1 f1e0 de01 1196  ................
00000190: 0190 0d92 8a95 e1f7 8e01 0f5f 1f4f 7e01  ..........._.O~.
000001a0: 89e2 e80e f11c 8ae0 d82e f801 8081 8150  ...............P
000001b0: 8d25 0e94 5600 0e5f 1f4f e016 f106 a9f7  .%..V.._.O......
000001c0: 8ae0 a796 0fb6 f894 debf 0fbe cdbf df91  ................
000001d0: cf91 1f91 0f91 ff90 ef90 df90 0c94 5600  ..............V.
000001e0: 87e6 0e94 4b00 0e94 8c00 8823 e1f3 0e94  ....K......#....
000001f0: b400 80e0 90e0 0895 f894 ffcf            ............
```

Ok, it looks like structure data (see that big array at the beginning?).
Let's try to disassemble it.

```
$ avr-objdump -i

[...]

ihex
 (header endianness unknown, data endianness unknown)
  plugin
  avr

[...]

$ avr-objdump -D -m avr serial.hex > serial.dump
$ less serial.dump

serial.hex:     file format ihex


Disassembly of section .sec1:

00000000 <.sec1>:
   0:    0c 94 34 00     jmp    0x68    ;  0x68
   4:    0c 94 49 00     jmp    0x92    ;  0x92
   8:    0c 94 49 00     jmp    0x92    ;  0x92

[...]
```

Ok this looks like valid code! We know this is code is targeting an Atmel AVR
microcontroller, but which one? Here is a list of the most common ones:

https://gcc.gnu.org/onlinedocs/gcc/AVR-Options.html

And here is a matrix listing some of their available features:

https://www-lisic.univ-littoral.fr/~hebert/microcontroleur/fichiers/famille_avr_8_bits.png

To answer that, we can try to decompile an 'empty' code with all the different
MCU types supported by `avr-gcc` and use some correlation techniques with our
dump. This would allow us to:

* Identify the potential architectures this was compiled for
* Reduce the analysis area

But googling the problem is actually faster and less painful. Here is a
corresponding dump from an ATmega328P (a very popular one since it was
introduced in most of the Arduinos and derivatives):

https://stackoverflow.com/questions/17323757/going-through-avr-assembler-hello-world-code

And the AVR instruction set is here:

http://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf

Let's annotate our dump:

```
        __vectors:
           0:    0c 94 34 00     jmp     0x68    ;  0x68        ; RESET     ; __ctors_end
           4:    0c 94 49 00     jmp     0x92    ;  0x92        ; INT0      ; __bad_interrupt
           8:    0c 94 49 00     jmp     0x92    ;  0x92        ; INT1
           c:    0c 94 49 00     jmp     0x92    ;  0x92        ; PCINT0
          10:    0c 94 49 00     jmp     0x92    ;  0x92        ; PCINT1
          14:    0c 94 49 00     jmp     0x92    ;  0x92        ; PCINT2
          18:    0c 94 49 00     jmp     0x92    ;  0x92        ; WDT
          1c:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER2 COMPA
          20:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER2 COMPB
          24:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER2 OVF
          28:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER1 CAPT
          2c:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER1 COMPA
          30:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER1 COMPB
          34:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER1 OVF
          38:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER0 COMPA
          3c:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER0 COMPB
          40:    0c 94 49 00     jmp     0x92    ;  0x92        ; TIMER0 OVF
          44:    0c 94 49 00     jmp     0x92    ;  0x92        ; SPI,STC
          48:    0c 94 49 00     jmp     0x92    ;  0x92        ; USART,RX
          4c:    0c 94 49 00     jmp     0x92    ;  0x92        ; USART,UDRE
          50:    0c 94 49 00     jmp     0x92    ;  0x92        ; USART,TX
          54:    0c 94 49 00     jmp     0x92    ;  0x92        ; ADC
          58:    0c 94 49 00     jmp     0x92    ;  0x92        ; EE READY
          5c:    0c 94 49 00     jmp     0x92    ;  0x92        ; ANALOG COMP
          60:    0c 94 49 00     jmp     0x92    ;  0x92        ; TWI
          64:    0c 94 49 00     jmp     0x92    ;  0x92        ; SPM READY
        
        __ctors_end:
          68:    11 24           eor     r1, r1       ; r1 = 0
          6a:    1f be           out     0x3f, r1     ; clear 0x3f (SREG)
                                                      ; Initialise stack pointer at 0x08FF
          6c:    cf ef           ldi     r28, 0xFF    ; 255
          6e:    d8 e0           ldi     r29, 0x08    ; 8
          70:    de bf           out     0x3e, r29    ; 0x3e is the high portion of the stack pointer
          72:    cd bf           out     0x3d, r28    ; 0x3d is the low  portion of the stack pointer
        
        __do_copy_data:
          74:    11 e0           ldi     r17, 0x01    ; 1
          76:    a0 e0           ldi     r26, 0x00    ; 0
          78:    b1 e0           ldi     r27, 0x01    ; 1
          7a:    ec ef           ldi     r30, 0xFC    ; low  portion of the data at 0x01fc
          7c:    f1 e0           ldi     r31, 0x01    ; high portion of the data at 0x01fc
     ,--- 7e:    02 c0           rjmp    .+4          ; 0x84
   ,----> 80:    05 90           lpm     r0, 2+
   | |    82:    0d 92           st      X+, r0
   | `--> 84:    a6 34           cpi     r26, 0x46    ; size of data section
   |      86:    b1 07           cpc     r27, r17
   `----- 88:    d9 f7           brne    .-10         ;  0x80

          8a:    0e 94 f0 00     call    0x1e0        ; __main
          8e:    0c 94 fc 00     jmp     0x1f8        ; __exit
        
        __bad_interrupt:
          92:    0c 94 00 00     jmp     0    ;  0x0
  
        __uart_init:                                    ; from avr/iom328p.h
 ,------> 96:    10 92 c5 00     sts     0x00C5, r1     ; UBRR0H or _SFR_MEM8(0xC5)
 |        9a:    80 93 c4 00     sts     0x00C4, r24    ; UBRR0L
 |        9e:    88 e1           ldi     r24, 0x18      ; 24 or 00011000b
 |        a0:    80 93 c1 00     sts     0x00C1, r24    ; UCSR0B
 |        a4:    86 e0           ldi     r24, 0x06      ; 06 or 00000110b
 |        a6:    80 93 c2 00     sts     0x00C2, r24    ; UCSR0C
 |        aa:    08 95           ret
 |      
 |      __uart_transmit_byte:                              ; while (!(UCSR0A & (1 << UDRE0));
 |   ,,--,-> ac:    90 91 c0 00     lds     r25, 0x00C0    ; r25 = UCSR0A
 |   ||| |   b0:    95 ff           sbrs    r25, 5         ; Skip if bit 5 (UDRE0) in r25 is set
 |   ||| `-- b2:    fc cf           rjmp    .-8            ; loop
 |   |||     b4:    80 93 c6 00     sts     0x00C6, r24    ; UDR0 = r24
 |   |||     b8:    08 95           ret
 |   |||  
 |   |||        __uart_transmit_bytes:
 |   ||| ,------> ba:    0f 93           push    r16
 |   ||| |        bc:    1f 93           push    r17
 |   ||| |        be:    cf 93           push    r28
 |   ||| |        c0:    df 93           push    r29
 |   ||| |        c2:    ec 01           movw    r28, r24     ; r28 = r24
 |   ||| |        c4:    8c 01           movw    r16, r24     ; r16 = r24
 |   ||| |        c6:    06 0f           add     r16, r22     ; r16 += r22
 |   ||| |        c8:    11 1d           adc     r17, r1      ; r17 += r1 (with carry)
 |   ||| |   ,--> ca:    c0 17           cp      r28, r16     ; r28 == r16?
 |   ||| |   |    cc:    d1 07           cpc     r29, r17     ; r29 == r17? (with carry)
 |   ||| | ,----- ce:    21 f0           breq    .+8          ; 0xd8
 |   ||  | | |
 |   ||| | | |    d0:    89 91           ld      r24, Y+      ; load indirect from data space using index Y (post inc)
 |   ||`--------- d2:    0e 94 56 00     call    0xac         ; __uart_transmit_byte(r24)
 |   ||  | | |
 |   ||  | | `--- d6:    f9 cf           rjmp    .-14         ;  0xca
 |   ||  | | |
 |   ||  | `----> d8:    df 91           pop     r29
 |   ||  |        da:    cf 91           pop     r28
 |   ||  |        dc:    1f 91           pop     r17
 |   ||  |        de:    0f 91           pop     r16
 |   ||  |        e0:    08 95           ret
 |   ||  |
 |   ||  |  __uart_receive_byte:
 |   ||  | ,-,-> loop_in:                                      ; while (!(UCSR0A & (1 << RXC0)));
 |   ||  | | |   e2:    80 91 c0 00     lds     r24, 0x00C0    ; r24 = UCSR0A
 |   ||  | | |   e6:    87 ff           sbrs    r24, 7         ; skip if bit 7 (RXC0) in r24 is set
 |   ||  | | `-- e8:    fc cf           rjmp    .-8            ; loop
 |   ||  | |     ea:    80 91 c6 00     lds     r24, 0x00C6    ; UDR0
 |   ||  | |     ee:    08 95           ret
 |   ||  | |
 |   ||  | |     f0:    0f 93           push    r16
 |   ||  | |     f2:    1f 93           push    r17
 |   ||  | |     f4:    cf 93           push    r28
 |   ||  | |     f6:    df 93           push    r29
 |   ||  | |     f8:    ec 01           movw    r28, r24
 |   ||  | |     fa:    8c 01           movw    r16, r24
 |   ||  | |     fc:    06 0f           add     r16, r22
 |   ||  | |     fe:    11 1d           adc     r17, r1
 |   ||  | |    100:    c0 17           cp      r28, r16
 |   ||  | |    102:    d1 07           cpc     r29, r17
 |   ||  | |    104:    21 f0           breq    .+8          ;  0x10e
 |   ||  | |
 |   ||  | |    106:    0e 94 71 00     call    0xe2         ;  0xe2
 |   ||  | |    10a:    89 93           st      Y+, r24
 |   ||  | |    10c:    f9 cf           rjmp    .-14         ;  0x100
 |   ||  | |    loop_out:
 |   ||  | |    10e:    df 91           pop     r29
 |   ||  | |    110:    cf 91           pop     r28
 |   ||  | |    112:    1f 91           pop     r17
 |   ||  | |    114:    0f 91           pop     r16
 |   ||  | |    116:    08 95           ret
 |   ||  | |  
 | ,---------> __display_prompt:
 | | ||  | |      118:    cf 93           push    r28
 | | ||  | |      11a:    df 93           push    r29
 | | ||  | |      11c:    cd b7           in      r28, 0x3d     ; save SP low
 | | ||  | |      11e:    de b7           in      r29, 0x3e     ; save SP high
 | | ||  | |      120:    6e 97           sbiw    r28, 0x1e     ; r28 -= strlen(prompt) + 1
 | | ||  | |      122:    0f b6           in      r0, 0x3f      ; save SREG
 | | ||  | |      124:    f8 94           cli                   ; clear interrupts
 | | ||  | |      126:    de bf           out     0x3e, r29     ; restore SP high
 | | ||  | |      128:    0f be           out     0x3f, r0      ; restore SREG
 | | ||  | |      12a:    cd bf           out     0x3d, r28     ; restore SP low
 | | ||  | |      12c:    8e e1           ldi     r24, 0x1E     ; strlen(_prompt) + 1
 | | ||  | |      12e:    e0 e0           ldi     r30, 0x00     ; 0
 | | ||  | |      130:    f1 e0           ldi     r31, 0x01     ; 1
 | | ||  | |      132:    de 01           movw    r26, r28
 | | ||  | |      134:    11 96           adiw    r26, 0x01     ; 1
 | | ||  | |
 | | ||  | | ,--> 136:    01 90           ld      r0, Z+
 | | ||  | | |    138:    0d 92           st      X+, r0
 | | ||  | | |    13a:    8a 95           dec     r24
 | | ||  | | `--  13c:    e1 f7           brne    .-8          ; loop
 | | ||  | |
 | | ||  | |      13e:    6e e1           ldi     r22, 0x1E    ; strlen(_prompt) + 1
 | | ||  | |      140:    ce 01           movw    r24, r28
 | | ||  | |      142:    01 96           adiw    r24, 0x01    ; increment r24 poitner
 | | ||  `-|----- 144:    0e 94 5d 00     call    0xba         ; __uart_transmit_bytes(r24, r22)
 | | ||    |
 | | ||    `----- 148:    0e 94 71 00     call    0xe2         ; r24 = __uart_receive_byte()
 | | ||  
 | | ||           14c:    91 e0           ldi     r25, 0x01    ; r25 is true
 | | ||           14e:    89 35           cpi     r24, 0x59    ; Compare r24 (uart input) with 0x59 or 'Y'
 | | ||       ,-- 150:    09 f0           breq    .+2          ; 0x154
 | | ||       |   152:    90 e0           ldi     r25, 0x00    ; r25 is false
 | | ||       `-> 154:    89 2f           mov     r24, r25     ; r24 = __uart_receive_byte == 'Y'
 | | ||           156:    6e 96           adiw    r28, 0x1e    ; move r28 at the end of _prompt
 | | ||           158:    0f b6           in      r0, 0x3f     ; save SREG
 | | ||           15a:    f8 94           cli
 | | ||           15c:    de bf           out     0x3e, r29    ; restore SP high (not touched)
 | | ||           15e:    0f be           out     0x3f, r0     ; restore SREG
 | | ||           160:    cd bf           out     0x3d, r28    ; restore SP low (end of _prompt, beginning of _flag)
 | | ||           162:    df 91           pop     r29
 | | ||           164:    cf 91           pop     r28
 | | ||           166:    08 95           ret
 | | ||  
 | | ||  __sub_168:
 | | ||  ,-> 168:    df 92           push    r13
 | | ||  |   16a:    ef 92           push    r14
 | | ||  |   16c:    ff 92           push    r15
 | | ||  |   16e:    0f 93           push    r16
 | | ||  |   170:    1f 93           push    r17
 | | ||  | 
 | | ||  |  __sub_172:
 | | ||  |      172:    cf 93           push    r28
 | | ||  |      174:    df 93           push    r29
 | | ||  |      176:    cd b7           in      r28, 0x3d             ; save SP low
 | | ||  |      178:    de b7           in      r29, 0x3e             ; save SP high
 | | ||  |      17a:    a7 97           sbiw    r28, 0x27             ; r28 -= strlen(_flag) + 1
 | | ||  |      17c:    0f b6           in      r0, 0x3f              ; save SREG
 | | ||  |      17e:    f8 94           cli
 | | ||  |      180:    de bf           out     0x3e, r29             ; restore SP high
 | | ||  |      182:    0f be           out     0x3f, r0              ; restore SREG
 | | ||  |      184:    cd bf           out     0x3d, r28             ; restore SP low
 | | ||  |      186:    87 e2           ldi     r24, 0x27             ; r24 = strlen(_flag) + 1
 | | ||  |      188:    ee e1           ldi     r30, 0x1E             ; 30
 | | ||  |      18a:    f1 e0           ldi     r31, 0x01             ; 1
 | | ||  |      18c:    de 01           movw    r26, r28              ; 
 | | ||  |      18e:    11 96           adiw    r26, 0x01             ; r26 points to the beginning of _flag
 | | ||  |
 | | ||  | ,--> 190:    01 90           ld      r0, Z+
 | | ||  | |    192:    0d 92           st      X+, r0
 | | ||  | |    194:    8a 95           dec     r24
 | | ||  | `--- 196:    e1 f7           brne    .-8                   ; loop
 | | ||  |
 | | ||  |      198:    8e 01           movw    r16, r28
 | | ||  |      19a:    0f 5f           subi    r16, 0xFF             ; init loop counter (16bits) 
 | | ||  |      19c:    1f 4f           sbci    r17, 0xFF             ; init loop counter
 | | ||  |      19e:    7e 01           movw    r14, r28
 | | ||  |      1a0:    89 e2           ldi     r24, 0x29             ; 41
 | | ||  |      1a2:    e8 0e           add     r14, r24
 | | ||  |      1a4:    f1 1c           adc     r15, r1
 | | ||  |      1a6:    8a e0           ldi     r24, 0x0A             ; r24 = 0xA = 10 = '\n'
 | | ||  |      1a8:    d8 2e           mov     r13, r24              ; r13 = r24
 | | ||  |     loop:
 | | ||  | ,--> 1aa:    f8 01           movw    r30, r16
 | | ||  | |    1ac:    80 81           ld      r24, Z                ; load r24 pointed by the Z pointer reg
 | | ||  | |    1ae:    81 50           subi    r24, 0x01             ; _flag - 1
 | | ||  | |    1b0:    8d 25           eor     r24, r13              ; Exclusive OR: r24 = r24 ^ 0x0A
 | | |`-------- 1b2:    0e 94 56 00     call    0xac                  ; __uart_transmit_byte(r24)
 | | |   | |    1b6:    0e 5f           subi    r16, 0xFE             ; r16 -= 0xfe (254)
 | | |   | |    1b8:    1f 4f           sbci    r17, 0xFF             ; r17 -= 0xff (255) (with carry)
 | | |   | |    1ba:    e0 16           cp      r14, r16              ; r14 == r16?
 | | |   | |    1bc:    f1 06           cpc     r15, r17              ; r15 == r17? (with carry)
 | | |   | `--- 1be:    a9 f7           brne    .-22                  ; loop
 | | |   |
 | | |   |      1c0:    8a e0           ldi     r24, 0x0A             ; 10 = '\n'
 | | |   |      1c2:    a7 96           adiw    r28, 0x27             ; r28 points after _flag
 | | |   |      1c4:    0f b6           in      r0, 0x3f              ; save SREG
 | | |   |      1c6:    f8 94           cli
 | | |   |      1c8:    de bf           out     0x3e, r29             ; restore SP high
 | | |   |      1ca:    0f be           out     0x3f, r0              ; restore SREG
 | | |   |      1cc:    cd bf           out     0x3d, r28             ; restore SP low
 | | |   |      1ce:    df 91           pop     r29
 | | |   |      1d0:    cf 91           pop     r28
 | | |   |      1d2:    1f 91           pop     r17
 | | |   |      1d4:    0f 91           pop     r16
 | | |   |      1d6:    ff 90           pop     r15
 | | |   |      1d8:    ef 90           pop     r14
 | | |   |      1da:    df 90           pop     r13
 | | `------    1dc:    0c 94 56 00     jmp     0xac                 ; __uart_transmit_byte('\n')
 | |     |
 | |     |     __main:
 | |     |      1e0:    87 e6           ldi     r24, 0x67            ; UBRR
 `----------    1e2:    0e 94 4b 00     call    0x96                 ; __uart_init()
   |     | 
   |     | ,--> 1e6:    0e 94 8c 00     call    0x118                ; 0x118
   `------------'                                                    ; __display_prompt()
         | |
         | |    1ea:    88 23           and    r24, r24              ; keep displaying prompt?
         | `--- 1ec:    e1 f3           breq    .-8                  ; loop
         `----- 1ee:    0e 94 b4 00     call    0x168                ; 0x168
         
                1f2:    80 e0           ldi    r24, 0x00             ; 0
                1f4:    90 e0           ldi    r25, 0x00             ; 0
                1f6:    08 95           ret
         
         _exit:
          1f8:    f8 94           cli
         
         _stop_program:
          1fa:    ff cf           rjmp    .-2          ;  0x1fa

         _prompt:
          1fc:    44 6f ; Do you need that flag? [Y/N]\n\0
          1fe:    20 79
          200:    6f 75
          202:    20 6e
          204:    65 65
          206:    64 20
          208:    74 68
          20a:    61 74
          20c:    20 66
          20e:    6c 61
          210:    67 3f
          212:    20 5b
          214:    59 2f
          216:    4e 5d
          218:    0a 00

         _flag:         ; Only printable ascii characters 
          21a:    50 5f ; P_J]^grMzf:Py]d[?jgLVJyQ:D}z:~yqz?pYx@
          21c:    4a 5d
          21e:    5e 67
          220:    72 4d
          222:    7a 66
          224:    3a 50
          226:    79 5d
          228:    64 5b
          22a:    3f 6a
          22c:    67 4c
          22e:    56 4a
          230:    79 51
          232:    3a 44
          234:    7d 7a
          236:    3a 7e
          238:    79 71
          23a:    7a 3f
          23c:    70 59
          23e:    78 40
```

So now I can be able to read the flag using this static analysis:

```
$ cat decode.py
flag = "P_J]^grMzf:Py]d[?jgLVJyQ:D}z:~yqz?pYx@"
decoded = ''.join([
    chr((ord(char) - 1) ^ ord('\n'))
    for char in flag
])
print(decoded)
$ python3 decode.py
ETCVWl{Fso3ErViP4clA_CrZ3Ivs3wrzs4eR}5
```

Well, It looks like the flag was written every other character and
that I missed that loop condition.

```
ETCVWl{Fso3ErViP4clA_CrZ3Ivs3wrzs4eR}5
E C W { s 3 r i 4 l _ r 3 v 3 r s e } 
ECW{s3ri4l_r3v3rse}
```

My methodology was the following:

* Find code such as the interrupts vector table and the initialisation sequence
* Decode the rodata section
* Discover UART routines with the constants and the use of <avr/iom328p.h>
* Follow status (SREG) and stack pointer (SP) registers
* Find the decryption routine with the unique eor (apart from eor x, x)

Useful links:

* https://en.wikipedia.org/wiki/Atmel_AVR_instruction_set
* http://www.rjhcoding.com/avr-asm-uart.php
* https://electronics.stackexchange.com/a/383028
