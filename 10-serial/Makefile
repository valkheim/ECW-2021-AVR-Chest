include config.mk

CC=avr-gcc
NAME=serial
MCU=atmega328p
QEMU_MCU=uno # see qemu-system-avr -machine help for a full list
CFLAGS=-Wall -Werror -mmcu=$(MCU)
CFLAGS+=$(CONFIG)

all: $(NAME).elf
	avr-size --format=avr --mcu=$(MCU) $(NAME).elf

release: CFLAGS += -Os
release: clean $(NAME).elf $(NAME).hex
	avr-strip $(NAME).elf

$(NAME).elf:
	$(CC) $(CFLAGS) -o $(NAME).elf $(NAME).c

$(NAME).hex:
	avr-objcopy -O ihex $(NAME).elf $(NAME).hex
	#avr-objcopy -j .text -O ihex $(NAME).elf $(NAME).hex

test: debug
	tmux new -d -s debug
	tmux send 'qemu-system-avr -S -s -nographic -serial tcp::5678,server=on,wait=off -machine $(QEMU_MCU) -bios $(NAME).elf' ENTER
	tmux split-window
	tmux send 'avr-gdb -ex "target remote :1234" $(NAME).elf' ENTER
	tmux split-window
	tmux send 'telnet localhost 5678' ENTER
	tmux a

clean:
	rm -f $(NAME).elf
	rm -f $(NAME).hex

re: clean all

debug: CFLAGS += -gdwarf -g3 -O0 -DDEBUG
debug: re
